# workers.py: a master process hands out tasks to worker processes on your own PC
import os, time
from concurrent.futures import ProcessPoolExecutor, as_completed

def task(n):
    """One task: count the even numbers in its own range of 20 lakh numbers."""
    start = n * 2_000_000
    evens = sum(1 for x in range(start, start + 2_000_000) if x % 2 == 0)
    return n, os.getpid(), evens

if __name__ == "__main__":               # this part runs only in the master
    workers = os.cpu_count()
    print("Master PID", os.getpid(), "starting", workers, "workers")
    t0 = time.time()
    with ProcessPoolExecutor(max_workers=workers) as pool:
        futures = [pool.submit(task, n) for n in range(8)]      # 8 tasks in the queue
        total = 0
        for f in as_completed(futures):
            n, pid, evens = f.result()
            total += evens
            print(f"  task {n} done by worker PID {pid}")
    print("Total evens:", total)
    print(f"Time: {time.time() - t0:.1f} s")
