"""Capstone: a mini lakehouse pipeline on your PC.
raw JSON lines -> bronze Parquet (partitioned by date) -> silver (clean, dedup,
quality gate, masked PII) -> gold (daily city revenue, top dishes) -> report.
Every step is idempotent: run the script twice and the results are identical.
Needs: pip install pyarrow"""
import hashlib, json, os, random, shutil, time
import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.parquet as pq

LAKE = "lake"
DATES = ["2026-10-17", "2026-10-18", "2026-10-19"]
CITIES = ["Pune", "Mumbai", "Thane", "Nashik"]
DISHES = {"Veg thali": 140, "Paneer roll": 120, "Dal khichdi": 110, "Chicken biryani": 220, "Poha": 60}


def inr(n):
    """Indian digit grouping: 1117740 -> 11,17,740"""
    s = str(int(n))
    head, tail = s[:-3], s[-3:]
    groups = []
    while len(head) > 2:
        groups.insert(0, head[-2:])
        head = head[:-2]
    return ",".join(([head] if head else []) + groups + [tail])


def log(step, msg):
    print(f"[{step:7}] {msg}")


def extract(day):
    """Simulate the app's raw export: JSON lines with real-world problems."""
    rnd = random.Random(day)                      # same day -> same data (repeatable)
    path = f"{LAKE}/raw/orders_{day}.jsonl"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    rows = []
    for i in range(rnd.randint(18_000, 22_000)):
        dish = rnd.choice(list(DISHES))
        rows.append({"order_id": f"{day[-5:].replace('-', '')}-{i:06d}", "ts": f"{day}T{rnd.randint(7, 22):02d}:{rnd.randint(0, 59):02d}:00",
                     "city": rnd.choice(CITIES), "dish": dish, "qty": rnd.choice([1, 1, 1, 2, 3]),
                     "price": DISHES[dish], "phone": f"9{rnd.randint(100000000, 999999999)}"})
    for r in rnd.sample(rows, 60):
        r["qty"] = 0                              # invalid quantity
    for r in rnd.sample(rows, 40):
        r["city"] = None                          # missing city
    rows += rnd.sample(rows, 150)                 # retries create duplicates
    with open(path, "w") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")
    return path, len(rows)


def bronze(day, raw_path):
    """Raw copy as Parquet, one folder per date. Overwrite = idempotent."""
    rows = [json.loads(line) for line in open(raw_path)]
    table = pa.Table.from_pylist(rows)
    out = f"{LAKE}/bronze/orders/date={day}"
    shutil.rmtree(out, ignore_errors=True)
    os.makedirs(out)
    pq.write_table(table, f"{out}/part-0.parquet")
    return table


def silver(day, table):
    """Deduplicate, check quality, mask PII. Stop if too many rows fail."""
    seen, keep = set(), []
    ids = table.column("order_id").to_pylist()
    for i, oid in enumerate(ids):
        if oid not in seen:
            seen.add(oid)
            keep.append(i)
    dedup = table.take(keep)
    dupes = table.num_rows - dedup.num_rows
    good_mask = pc.and_(pc.greater(dedup["qty"], 0), pc.is_valid(dedup["city"]))
    good, bad = dedup.filter(good_mask), dedup.filter(pc.invert(good_mask))
    fail_rate = bad.num_rows / dedup.num_rows
    if fail_rate > 0.02:
        raise RuntimeError(f"quality gate failed for {day}: {fail_rate:.2%}")
    keys = [hashlib.sha256(("salt:" + p).encode()).hexdigest()[:10] for p in good["phone"].to_pylist()]
    good = good.drop(["phone"]).append_column("customer_key", pa.array(keys))
    good = good.append_column("amount", pc.multiply(good["qty"], good["price"]))
    for name, t in [("orders", good), ("quarantine", bad.drop(["phone"]))]:
        out = f"{LAKE}/silver/{name}/date={day}"
        shutil.rmtree(out, ignore_errors=True)
        os.makedirs(out)
        pq.write_table(t, f"{out}/part-0.parquet")
    return good, dupes, bad.num_rows, fail_rate


def gold():
    """Business tables built from all silver partitions."""
    orders = pq.read_table(f"{LAKE}/silver/orders", columns=["date", "city", "dish", "amount", "customer_key"])
    orders = orders.set_column(0, "date", pc.cast(orders["date"], pa.string()))   # partition column -> plain text
    by_city = orders.group_by(["date", "city"]).aggregate([("amount", "sum"), ("amount", "count")])
    by_city = by_city.sort_by([("date", "ascending"), ("amount_sum", "descending")])
    by_dish = orders.group_by("dish").aggregate([("amount", "sum")]).sort_by([("amount_sum", "descending")])
    os.makedirs(f"{LAKE}/gold", exist_ok=True)
    pq.write_table(by_city, f"{LAKE}/gold/daily_city_revenue.parquet")
    pq.write_table(by_dish, f"{LAKE}/gold/dish_revenue.parquet")
    return by_city, by_dish, orders.num_rows


def run():
    start = time.time()
    for day in DATES:
        raw_path, n_raw = extract(day)
        log("extract", f"{day}: {n_raw:,} raw rows")
        t = bronze(day, raw_path)
        good, dupes, bad, rate = silver(day, t)
        log("silver", f"{day}: {good.num_rows:,} clean, {dupes} duplicates removed, {bad} quarantined ({rate:.2%})")
    by_city, by_dish, n = gold()
    log("gold", f"{n:,} orders across {len(DATES)} days -> 2 gold tables")
    return by_city, by_dish, round(time.time() - start, 1)


if __name__ == "__main__":
    shutil.rmtree(LAKE, ignore_errors=True)
    by_city, by_dish, secs = run()
    print("\nRevenue by city, 2026-10-19 (Rs):")
    for r in by_city.to_pylist():
        if r["date"] == "2026-10-19":
            print(f"  {r['city']:7} {inr(r['amount_sum']):>11}  ({inr(r['amount_count'])} orders)")
    print("Top dishes, all 3 days (Rs):")
    for r in by_dish.to_pylist()[:3]:
        print(f"  {r['dish']:16} {inr(r['amount_sum']):>11}")
    first = pq.read_table(f"{LAKE}/gold/dish_revenue.parquet").to_pylist()
    print("\nRe-running the whole pipeline to test idempotency...")
    run()
    second = pq.read_table(f"{LAKE}/gold/dish_revenue.parquet").to_pylist()
    print("Gold identical after re-run:", first == second)
    files = sum(len(fs) for _, _, fs in os.walk(LAKE))
    print(f"Lake folder: {files} files under ./{LAKE}/")
