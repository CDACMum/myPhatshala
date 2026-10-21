"""A leader with two followers, simulated step by step on a clock.
Writes go to the leader's log; followers copy the log after a delay (asynchronous replication).
We read from a follower, crash the leader, fail over, and count what was lost.
Then we repeat with synchronous replication to one follower (semi-sync)."""


def run(mode, lag={"F1": 2, "F2": 5}, crash_at=12):
    leader_log = []
    follower_log = {"F1": [], "F2": []}
    pending = []                         # (arrival_time, follower, entry)
    acked = []
    for t in range(0, crash_at):
        if t % 2 == 0:                   # a client write every 2 ticks
            entry = f"order@{t}"
            leader_log.append(entry)
            for f, d in lag.items():
                pending.append((t + d, f, entry))
            if mode == "semi-sync":      # wait until F1 has it before saying OK
                follower_log["F1"].append(entry)
                pending = [p for p in pending if not (p[1] == "F1" and p[2] == entry)]
            acked.append(entry)
        for p in [p for p in pending if p[0] <= t]:
            follower_log[p[1]].append(p[2])
            pending.remove(p)
        if mode == "async" and t == 7:
            print(f"  t={t}: read from F2 sees {len(follower_log['F2'])} of {len(leader_log)} orders (replication lag)")
    # leader crashes; promote the follower with the longest log
    new_leader = max(follower_log, key=lambda f: len(follower_log[f]))
    lost = [e for e in acked if e not in follower_log[new_leader]]
    print(f"  leader crashed at t={crash_at}; promoted {new_leader} with {len(follower_log[new_leader])} of {len(acked)} acknowledged orders")
    print(f"  acknowledged but LOST: {lost if lost else 'none'}")


print("Asynchronous replication:")
run("async")
print("\nSemi-synchronous (leader waits for F1 before acknowledging):")
run("semi-sync")

# Quorum check for leaderless replication
print("\nQuorum reads/writes with N = 3 replicas:")
for w, r in [(1, 1), (2, 1), (2, 2), (3, 1)]:
    print(f"  W={w} R={r}: {'always reads the latest write' if r + w > 3 else 'may read stale data'}")
