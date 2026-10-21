# node_report.py: look at your own computer the way a cluster admin looks at a node
import os, platform, shutil

def ram_gb():
    try:                                    # Linux and macOS
        return os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES") / 1024**3
    except (ValueError, AttributeError, OSError):   # Windows
        import ctypes
        class M(ctypes.Structure):
            _fields_ = [("len", ctypes.c_ulong), ("load", ctypes.c_ulong), ("total", ctypes.c_ulonglong),
                        ("avail", ctypes.c_ulonglong), ("a", ctypes.c_ulonglong), ("b", ctypes.c_ulonglong),
                        ("c", ctypes.c_ulonglong), ("d", ctypes.c_ulonglong), ("e", ctypes.c_ulonglong)]
        m = M(); m.len = ctypes.sizeof(M)
        ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m))
        return m.total / 1024**3

cores = os.cpu_count()
ram = ram_gb()
disk = shutil.disk_usage(os.path.abspath(os.sep)).total / 1024**4      # in TB

print("Host name :", platform.node())
print("OS        :", platform.system())
print("CPU cores :", cores)
print(f"RAM       : {ram:.1f} GB")
print(f"Disk      : {disk:.2f} TB")

# a typical Hadoop worker node (approximate, 2026)
worker = {"cores": 32, "ram": 256, "disk": 12 * 12}
print("\nOne typical worker node equals about:")
print(f"  {worker['cores'] / cores:.0f} of your machines in CPU cores")
print(f"  {worker['ram'] / ram:.0f} of your machines in RAM")
print(f"  {worker['disk'] / disk:.0f} of your machines in disk")
