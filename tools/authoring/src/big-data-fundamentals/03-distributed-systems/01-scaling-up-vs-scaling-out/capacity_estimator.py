"""Back-of-envelope capacity plan, calibrated with a real measurement on your PC.
Step 1 measures how many order events one CPU core can parse and validate per second.
Step 2 uses that number to estimate the machines needed for a festival peak."""
import json, math, time

# ---- assumptions (change these)
ORDERS_PER_DAY = 10_00_00_000      # 10 crore orders a day
PEAK_FACTOR = 5                     # peak hour is 5x the average rate
EVENTS_PER_ORDER = 20               # clicks, status updates, pings per order
BYTES_PER_EVENT = 500
CORES_PER_NODE = 16
HEADROOM = 0.6                      # run nodes at 60% so spikes and failures are absorbed

def inr(x):
    """Indian digit grouping: 115741 -> 1,15,741"""
    s = str(round(x))
    head, tail = s[:-3], s[-3:]
    while len(head) > 2:
        tail = head[-2:] + "," + tail
        head = head[:-2]
    return (head + "," + tail) if head else tail


# ---- step 1: measure one core
event = json.dumps({"order_id": "O1043", "user": "U9", "city": "Pune", "amount": 420,
                    "items": [{"dish": "thali", "qty": 1}, {"dish": "lassi", "qty": 2}], "ts": 1792411000})
n, start = 0, time.perf_counter()
while time.perf_counter() - start < 1.0:
    e = json.loads(event)
    ok = e["amount"] > 0 and e["city"] and len(e["items"]) > 0
    n += 1
per_core = n / (time.perf_counter() - start)
print(f"Measured: one core parses and checks about {inr(per_core)} events per second")

# ---- step 2: estimate
events_day = ORDERS_PER_DAY * EVENTS_PER_ORDER
avg_eps = events_day / 86_400
peak_eps = avg_eps * PEAK_FACTOR
cores = peak_eps / (per_core * HEADROOM)
nodes = math.ceil(cores / CORES_PER_NODE)
storage_tb_day = events_day * BYTES_PER_EVENT / 1024**4

print(f"\nEvents per day      : {events_day / 1e7:.0f} crore")
print(f"Average events / s  : {inr(avg_eps)}")
print(f"Peak events / s     : {inr(peak_eps)}")
print(f"Cores needed at peak: {cores:.1f}  (at {HEADROOM:.0%} target load)")
print(f"Nodes ({CORES_PER_NODE} cores each): {nodes}")
print(f"Raw event storage   : {storage_tb_day:.2f} TB per day, {storage_tb_day * 365:.0f} TB per year")
print("\nReal services do far more work per event (network, database, logging),")
print("so production capacity is usually 10-100x higher than this lower bound.")
