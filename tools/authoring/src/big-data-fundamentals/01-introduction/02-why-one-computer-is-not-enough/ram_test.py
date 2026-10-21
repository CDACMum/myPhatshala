import os, shutil, tracemalloc

print("CPU cores :", os.cpu_count())
total, used, free = shutil.disk_usage(".")
print("Disk      :", round(total / 1024**3), "GB total,", round(free / 1024**3), "GB free")

# How much memory do 10 lakh small payment records take inside Python?
tracemalloc.start()
records = [{"id": i, "item": "chai", "amount": 20} for i in range(1_000_000)]
used_mb = tracemalloc.get_traced_memory()[0] / 1024**2
tracemalloc.stop()
print("10 lakh records in a list use", round(used_mb), "MB of RAM")

per_record = used_mb * 1024**2 / len(records)
print("That is about", round(per_record), "bytes per record")
for n, label in [(100_000_000, "10 crore"), (10_000_000_000, "1,000 crore")]:
    gb = n * per_record / 1024**3
    print(f"{label:>11} records would need about {gb:,.0f} GB of RAM")
