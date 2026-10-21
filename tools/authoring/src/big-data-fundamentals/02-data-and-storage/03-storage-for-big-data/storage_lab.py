"""A tiny object store on your disk, and the small-files problem measured for real.
Only the Python standard library is used."""
import hashlib, json, os, time

STORE = "my_bucket"


def put(key, data: bytes, **metadata):
    """Store bytes under a key. 'Folders' are just part of the key."""
    path = os.path.join(STORE, "objects", hashlib.sha1(key.encode()).hexdigest())
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(data)
    meta = {"key": key, "size": len(data), "etag": hashlib.md5(data).hexdigest(), **metadata}
    with open(path + ".meta.json", "w") as f:
        json.dump(meta, f)


def get(key):
    path = os.path.join(STORE, "objects", hashlib.sha1(key.encode()).hexdigest())
    with open(path, "rb") as f:
        return f.read()


def list_prefix(prefix):
    keys = []
    for name in os.listdir(os.path.join(STORE, "objects")):
        if name.endswith(".meta.json"):
            with open(os.path.join(STORE, "objects", name)) as f:
                k = json.load(f)["key"]
            if k.startswith(prefix):
                keys.append(k)
    return sorted(keys)


put("reviews/2026/10/19/O1043.jpg", b"\xff\xd8 fake image bytes", content_type="image/jpeg", order="O1043")
put("reviews/2026/10/19/O1044.jpg", b"\xff\xd8 another image", content_type="image/jpeg", order="O1044")
put("orders/date=2026-10-19/part-0.csv", b"O1043,Pune,420\nO1044,Thane,250\n", content_type="text/csv")
print("Keys under reviews/2026/10/19/:", list_prefix("reviews/2026/10/19/"))
print("Read back:", get("orders/date=2026-10-19/part-0.csv").decode().strip().splitlines())
print("Note: there are no real folders on disk, only hashed object names + metadata files.\n")

# ---- the small-files problem: same bytes, 5,000 files vs 1 file
os.makedirs("small_files", exist_ok=True)
row = b"O1043,Pune,thali,220,2026-10-19\n"
for i in range(5000):
    with open(f"small_files/part-{i:05d}.csv", "wb") as f:
        f.write(row * 20)
with open("one_big_file.csv", "wb") as f:
    f.write(row * 20 * 5000)

t = time.perf_counter()
total = 0
for name in os.listdir("small_files"):
    with open(os.path.join("small_files", name), "rb") as f:
        total += f.read().count(b"\n")
small_s = time.perf_counter() - t

t = time.perf_counter()
with open("one_big_file.csv", "rb") as f:
    big_rows = f.read().count(b"\n")
big_s = time.perf_counter() - t

print(f"5,000 small files: {total // 100000} lakh rows read in {small_s * 1000:.0f} ms")
print(f"1 big file       : {big_rows // 100000} lakh rows read in {big_s * 1000:.0f} ms")
print(f"Same data, about {small_s / big_s:.0f}x slower as small files on this machine")
