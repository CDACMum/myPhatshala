import os, time
from multiprocessing import Pool


def count_primes(block):
    """Count the prime numbers in one block (a range of numbers)."""
    lo, hi = block
    count = 0
    for n in range(max(lo, 2), hi):
        if all(n % d for d in range(2, int(n ** 0.5) + 1)):
            count += 1
    return count


if __name__ == "__main__":           # needed on Windows for multiprocessing
    cores = os.cpu_count()
    N = 2_000_000
    step = N // cores
    blocks = [(i * step, (i + 1) * step) for i in range(cores)]

    start = time.time()
    serial = sum(count_primes(b) for b in blocks)
    t1 = time.time() - start
    print(f"Serial   (1 core) : {serial} primes in {t1:.1f} s")

    start = time.time()
    with Pool(cores) as pool:
        parallel = sum(pool.map(count_primes, blocks))
    t2 = time.time() - start
    print(f"Parallel ({cores} cores): {parallel} primes in {t2:.1f} s")
    print(f"Speed-up: {t1 / t2:.1f}x")

    # Big numbers take longer to test, so the last block is the slowest.
    # Many small blocks spread the work more evenly between the cores.
    small = N // (cores * 8)
    many = [(i * small, (i + 1) * small) for i in range(cores * 8)]
    start = time.time()
    with Pool(cores) as pool:
        balanced = sum(pool.map(count_primes, many))
    t3 = time.time() - start
    print(f"Parallel, {len(many)} small blocks: {balanced} primes in {t3:.1f} s, speed-up {t1 / t3:.1f}x")
