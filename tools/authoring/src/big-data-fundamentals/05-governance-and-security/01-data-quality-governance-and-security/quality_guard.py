"""A small data-quality gate and privacy step for a batch of orders.
1) generate a realistic messy batch, 2) run quality checks,
3) quarantine bad rows, 4) mask personal data before it reaches analysts."""
import csv, hashlib, random, re
from collections import Counter

random.seed(11)
CITIES = ["Pune", "Mumbai", "Thane", "Nashik"]
rows = []
for i in range(1, 10_001):
    rows.append({"order_id": f"O{i:05d}", "phone": f"9{random.randint(100000000, 999999999)}",
                 "email": f"user{i}@example.com", "city": random.choice(CITIES),
                 "amount": str(random.randint(80, 900)), "order_date": "2026-10-19"})
# inject the kinds of problems real batches have
for i in random.sample(range(10_000), 40):
    rows[i]["amount"] = "-150"                    # negative amount
for i in random.sample(range(10_000), 25):
    rows[i]["city"] = ""                          # missing city
for i in random.sample(range(10_000), 15):
    rows[i]["phone"] = "12345"                    # invalid phone
rows += [dict(rows[i]) for i in random.sample(range(10_000), 30)]   # duplicates

CHECKS = {
    "amount is positive": lambda r: r["amount"].lstrip("-").isdigit() and int(r["amount"]) > 0,
    "city present": lambda r: r["city"] in CITIES,
    "phone is 10 digits": lambda r: re.fullmatch(r"[6-9]\d{9}", r["phone"]) is not None,
}
seen, good, bad, failures = set(), [], [], Counter()
for r in rows:
    problems = [name for name, ok in CHECKS.items() if not ok(r)]
    if r["order_id"] in seen:
        problems.append("order_id unique")
    seen.add(r["order_id"])
    for p in problems:
        failures[p] += 1
    (bad if problems else good).append(r)

print(f"batch rows      : {len(rows):,}")
for name, n in failures.most_common():
    print(f"  FAIL {name:20}: {n}")
print(f"passed          : {len(good):,}  quarantined: {len(bad)}")
fail_rate = len(bad) / len(rows) * 100
print(f"failure rate    : {fail_rate:.2f}%  ->", "PUBLISH" if fail_rate < 2 else "STOP the pipeline")

SALT = "keep-this-secret"       # in real life: from a secrets manager, never in code
def pseudonym(value):
    return hashlib.sha256((SALT + value).encode()).hexdigest()[:12]
def mask_phone(p):
    return "XXXXXX" + p[-4:]

with open("orders_clean.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["order_id", "customer_key", "phone_masked", "city", "amount", "order_date"])
    w.writeheader()
    for r in good:
        w.writerow({"order_id": r["order_id"], "customer_key": pseudonym(r["email"]), "phone_masked": mask_phone(r["phone"]),
                    "city": r["city"], "amount": r["amount"], "order_date": r["order_date"]})
print("\nwrote orders_clean.csv (no raw email or phone). First row:")
print(open("orders_clean.csv").read().splitlines()[1])
