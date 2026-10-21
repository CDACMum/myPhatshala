# loss_sim.py: how likely is data loss with 1, 2 or 3 copies? (a Monte Carlo simulation)
import random

random.seed(42)
NODES, BLOCKS = 200, 20_000
AFR = 0.04            # chance that a node fails in one year (disk, power supply, board …)
REPAIR_DAYS = 1       # time to re-copy a dead node's blocks
YEARS = 5

def lost_blocks(copies):
    placement = [random.sample(range(NODES), copies) for _ in range(BLOCKS)]
    lost = 0
    for day in range(365 * YEARS):
        # which nodes are down today (failed within the last REPAIR_DAYS)?
        down = {n for n in range(NODES) if random.random() < AFR / 365 * REPAIR_DAYS}
        if len(down) < copies:
            continue
        for p in placement:
            if all(n in down for n in p):
                lost += 1
    return lost

for c in [1, 2, 3]:
    print(f"{c} cop{'y' if c == 1 else 'ies'}: {lost_blocks(c):>6} block-loss events in {YEARS} years")
