# blocks_and_splits.py: cut a file into HDFS-style blocks, then count records per split
# the way Hadoop's LineRecordReader does (no Hadoop needed).

FILE = "canteen_orders.csv"
BLOCK = 1024 * 1024                       # same as -D dfs.blocksize=1048576
data = open(FILE, "rb").read()
size = len(data)
starts = list(range(0, size, BLOCK))
print(f"{FILE}: {size:,} bytes -> {len(starts)} blocks of up to {BLOCK:,} bytes")

for i, start in enumerate(starts):
    end = min(start + BLOCK, size)
    pos = start
    if start != 0:                        # not the first split: skip the partial first line
        pos = data.index(b"\n", start - 1) + 1
    records = 0
    while pos < end:                      # a record that STARTS inside the split belongs to it
        nl = data.find(b"\n", pos)
        pos = size if nl == -1 else nl + 1
        records += 1
    print(f"split {i}: bytes {start:>7}-{end - 1:>7}  records {records:>6}")

cut = BLOCK                               # show the line broken by the first block boundary
line_start = data.rindex(b"\n", 0, cut) + 1
line_end = data.index(b"\n", cut)
print("record cut by block 0/1:", data[line_start:cut], "+", data[cut:line_end])
