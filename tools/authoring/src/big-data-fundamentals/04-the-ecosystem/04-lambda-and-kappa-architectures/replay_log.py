import json, os

# ---------- An append-only event log, like a Kafka topic ----------
LOG = "orders.log"
raw = [("O1", 120, "sale"), ("O2", 250, "sale"), ("O3", 90, "sale"), ("O2", 250, "refund"),
       ("O4", 300, "sale"), ("O5", 140, "sale"), ("O6", 60, "sale"), ("O4", 300, "refund")]
with open(LOG, "w") as f:
    for offset, (oid, amount, kind) in enumerate(raw):
        f.write(json.dumps({"offset": offset, "order": oid, "amount": amount, "type": kind}) + "\n")
print(f"Log written: {len(raw)} events (offsets 0-{len(raw) - 1}), never edited afterwards\n")


def consume(logic, start=0, end=None):
    """Read the log from an offset, like a consumer reading a Kafka partition."""
    total = 0
    with open(LOG) as f:
        for line in f:
            e = json.loads(line)
            if e["offset"] < start or (end is not None and e["offset"] >= end):
                continue
            total = logic(total, e)
    return total


def v1(total, e):                      # BUG: treats refunds as sales
    return total + e["amount"]


def v2(total, e):                      # FIXED: refunds reduce revenue
    return total - e["amount"] if e["type"] == "refund" else total + e["amount"]


# ---------- KAPPA: one streaming code path; fix a bug by replaying the log ----------
print("KAPPA")
print(f"  {'v1 job (live since morning) says revenue':44}: Rs {consume(v1)}")
print("  bug found -> deploy v2, replay from offset 0")
print(f"  {'v2 job after replay says revenue':44}: Rs {consume(v2)}")

# ---------- LAMBDA: batch view (complete but late) + speed view (recent, fast) ----------
print("\nLAMBDA")
batch_upto = 5                         # last night's batch job processed offsets 0-4
batch_view = consume(v2, 0, batch_upto)
speed_view = consume(v2, batch_upto)   # events that arrived since the batch ran
print(f"  {'batch view (offsets 0-4, computed at 02:00)':44}: Rs {batch_view}")
print(f"  {'speed view (offsets 5-7, live since then)':44}: Rs {speed_view}")
print(f"  {'query answer = batch view + speed view':44}: Rs {batch_view + speed_view}")
