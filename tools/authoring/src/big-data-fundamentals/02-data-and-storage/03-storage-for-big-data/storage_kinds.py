# storage_kinds.py: block, file and object storage behaviour, seen from Python on your own disk.
import hashlib, json, os, shutil, time

os.makedirs("lab", exist_ok=True)

# ---- 1. BLOCK level: the disk hands out fixed-size blocks ----------------
st = os.statvfs("lab") if hasattr(os, "statvfs") else None
with open("lab/one_byte.txt", "w") as f:
    f.write("x")
if st:
    info = os.stat("lab/one_byte.txt")
    print("1. BLOCK   file system block size:", st.f_bsize, "bytes")
    print("           a 1-byte file occupies  :", info.st_blocks * 512, "bytes on disk")
else:
    print("1. BLOCK   (block details are not shown by Python on Windows; try this on Linux/macOS)")

# ---- 2. FILE level: folders, rename, edit in place -------------------------
os.makedirs("lab/fs/orders/2026-10", exist_ok=True)
for i in range(2000):
    with open(f"lab/fs/orders/2026-10/part-{i:04}.csv", "w") as f:
        f.write("order_id,amount\n1,30\n")
t = time.perf_counter()
os.rename("lab/fs/orders/2026-10", "lab/fs/orders/october")          # one metadata change
print("2. FILE    rename a folder of 2000 files:", f"{(time.perf_counter() - t) * 1000:.2f} ms")
with open("lab/fs/orders/october/part-0000.csv", "r+") as f:           # change bytes in the middle
    f.seek(18); f.write("4")
print("           edit in place ->", open("lab/fs/orders/october/part-0000.csv").read().split())

# ---- 3. OBJECT level: a flat key -> (bytes + metadata) store ---------------
class MiniObjectStore:
    """Behaves like S3: whole objects, flat keys, metadata, no rename, no partial update."""
    def __init__(self, root):
        self.root = root; os.makedirs(root, exist_ok=True)
    def _path(self, key):
        return os.path.join(self.root, hashlib.sha1(key.encode()).hexdigest())
    def put(self, key, data, **meta):
        with open(self._path(key), "wb") as f: f.write(data)
        etag = hashlib.md5(data).hexdigest()
        with open(self._path(key) + ".meta", "w") as f:
            json.dump({"key": key, "size": len(data), "etag": etag, **meta}, f)
        return etag
    def get(self, key):
        return open(self._path(key), "rb").read()
    def head(self, key):
        return json.load(open(self._path(key) + ".meta"))
    def list(self, prefix):
        keys = [json.load(open(os.path.join(self.root, n)))["key"] for n in os.listdir(self.root) if n.endswith(".meta")]
        return sorted(k for k in keys if k.startswith(prefix))
    def delete(self, key):
        os.remove(self._path(key)); os.remove(self._path(key) + ".meta")

s3 = MiniObjectStore("lab/bucket")
for i in range(2000):
    s3.put(f"orders/2026-10/part-{i:04}.csv", b"order_id,amount\n1,30\n", canteen="C017")
print("3. OBJECT  keys under 'orders/2026-10/':", len(s3.list("orders/2026-10/")))
print("           metadata of one object     :", s3.head("orders/2026-10/part-0000.csv"))

t = time.perf_counter()
for key in s3.list("orders/2026-10/"):                                 # "rename" = copy + delete
    s3.put(key.replace("2026-10", "october"), s3.get(key), **{k: v for k, v in s3.head(key).items() if k == "canteen"})
    s3.delete(key)
print("           'rename' the same 2000 objects:", f"{(time.perf_counter() - t) * 1000:.0f} ms (copy + delete each)")

old = s3.get("orders/october/part-0000.csv")
new_etag = s3.put("orders/october/part-0000.csv", old.replace(b"30", b"34"))   # whole object rewritten
print("           update = rewrite whole object, new ETag:", new_etag)

shutil.rmtree("lab")
