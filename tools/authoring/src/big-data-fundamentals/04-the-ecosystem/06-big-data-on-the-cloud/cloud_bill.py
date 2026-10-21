"""Estimate a monthly cloud bill for a small data platform, and see what
partitioning, columnar files, spot instances and auto-shutdown save.
All prices are ILLUSTRATIVE round numbers in rupees, not a real price list."""

PRICE = {
    "storage_per_tb_month": 1_900,     # object storage, standard tier
    "scan_per_tb": 450,                # serverless SQL, charged per TB scanned
    "node_hour_on_demand": 40,         # one Spark worker node
    "node_hour_spot": 12,              # same node as spot / preemptible capacity
    "egress_per_tb": 7_000,            # data sent out of the cloud region
}
LAKE_TB = 60
QUERIES_PER_DAY = 400
NIGHTLY_NODES, NIGHTLY_HOURS = 20, 3


def bill(scan_tb_per_query, spot, cluster_always_on, egress_tb):
    storage = LAKE_TB * PRICE["storage_per_tb_month"]
    scans = scan_tb_per_query * QUERIES_PER_DAY * 30 * PRICE["scan_per_tb"]
    rate = PRICE["node_hour_spot"] if spot else PRICE["node_hour_on_demand"]
    hours = 24 if cluster_always_on else NIGHTLY_HOURS
    compute = NIGHTLY_NODES * hours * 30 * rate
    egress = egress_tb * PRICE["egress_per_tb"]
    return {"storage": storage, "queries": scans, "compute": compute, "egress": egress}


def show(name, b):
    total = sum(b.values())
    parts = ", ".join(f"{k} {v / 1e5:.1f}L" for k, v in b.items())
    print(f"{name:37} Rs {total / 1e5:6.1f} lakh/month  ({parts})")
    return total


before = show("1. Naive: CSV, SELECT *, always on", bill(0.8, False, True, 5))
step2 = show("2. + Parquet, partitions, columns", bill(0.02, False, True, 5))
step3 = show("3. + cluster only for the 3-hour job", bill(0.02, False, False, 5))
step4 = show("4. + spot workers", bill(0.02, True, False, 5))
after = show("5. + keep data in-region (no egress)", bill(0.02, True, False, 0))
print(f"\nSaving: {(1 - after / before) * 100:.0f}% of the original bill")
