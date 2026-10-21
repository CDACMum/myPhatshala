"""A tiny orchestrator: tasks with dependencies, run in order, with retries,
one output partition per logical date, and a backfill that re-runs safely."""
import json, os, random

random.seed(1)
os.makedirs("warehouse", exist_ok=True)

ORDERS = {  # pretend source system: orders per day
    "2026-10-17": [120, 340, 90], "2026-10-18": [200, 150], "2026-10-19": [410, 80, 60, 300],
}
DAG = {"extract": [], "validate": ["extract"], "transform": ["validate"], "publish": ["transform"]}


def topo_order(dag):
    done, order = set(), []
    while len(order) < len(dag):
        for task, deps in dag.items():
            if task not in done and all(d in done for d in deps):
                order.append(task)
                done.add(task)
    return order


def run_task(task, day, state, flaky):
    if task == "extract":
        if flaky and random.random() < 0.6:      # the source API sometimes times out
            raise TimeoutError("source API timed out")
        state["rows"] = ORDERS[day]
    elif task == "validate":
        assert all(a > 0 for a in state["rows"]), "negative amount"
    elif task == "transform":
        state["summary"] = {"day": day, "orders": len(state["rows"]), "revenue": sum(state["rows"])}
    elif task == "publish":
        # idempotent: overwrite this day's partition instead of appending
        with open(f"warehouse/daily_{day}.json", "w") as f:
            json.dump(state["summary"], f)


def run_dag(day, flaky=False, retries=3, verbose=True):
    state = {}
    for task in topo_order(DAG):
        for attempt in range(1, retries + 1):
            try:
                run_task(task, day, state, flaky)
                if verbose:
                    print(f"  {day} {task:9} ok" + (f" (attempt {attempt})" if attempt > 1 else ""))
                break
            except Exception as e:
                print(f"  {day} {task:9} failed: {e}" + ("; retrying" if attempt < retries else "; giving up"))
        else:
            print(f"  {day} downstream tasks skipped, alert sent")
            return
    if not verbose:
        print(f"  {day} all tasks ok -> {state['summary']}")


print("Task order:", topo_order(DAG))
print("\nNightly run for 2026-10-19 (flaky source):")
run_dag("2026-10-19", flaky=True)

print("\nBackfill 2026-10-17 to 2026-10-19 (run twice to prove it is safe):")
for run in (1, 2):
    print(f" run {run}:")
    for day in ORDERS:
        run_dag(day, verbose=False)
files = sorted(os.listdir("warehouse"))
total = sum(json.load(open("warehouse/" + f))["revenue"] for f in files)
print(f"\nPartitions in warehouse: {files}")
print(f"Total revenue across partitions: Rs {total} (not doubled, because publish overwrites)")
