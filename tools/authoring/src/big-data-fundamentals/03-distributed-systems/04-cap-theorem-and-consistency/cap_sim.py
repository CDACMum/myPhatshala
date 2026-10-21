"""Three replicas, then a network partition splits them {A} | {B, C}.
CP mode: only the side with a majority accepts writes.
AP mode: both sides accept writes, then merge when the network heals.
We merge a like-counter two ways: last-write-wins (loses likes) and a CRDT counter (keeps all)."""

REPLICAS = ["A", "B", "C"]
partition = [{"A"}, {"B", "C"}]


def side_of(node):
    return next(s for s in partition if node in s)


def cp_write(node, value, store):
    side = side_of(node)
    if len(side) > len(REPLICAS) // 2:
        for n in side:
            store[n] = value
        return "accepted"
    return "REFUSED (no majority on this side)"


print("CP mode (choose consistency):")
store = {n: 100 for n in REPLICAS}          # balance Rs 100 everywhere
print("  write via A:", cp_write("A", 40, store))
print("  write via B:", cp_write("B", 70, store))
print("  majority side (B, C) now holds:", store["B"], "| A must refuse reads and writes until the network heals")

print("\nAP mode (choose availability): a like counter")
likes = {"A": 1000, "B": 1000, "C": 1000}
# during the partition: 3 likes arrive at A, 5 likes at B
likes["A"] += 3
likes["B"] += 5
likes["C"] = likes["B"]                      # C is on B's side and syncs with it
print("  during partition:", likes, "-> different answers, but every request succeeded")

# merge 1: last-write-wins (keep the value written last, say B's)
lww = likes["B"]
print("  last-write-wins after healing:", lww, "(A's 3 likes are lost)")

# merge 2: a G-counter CRDT keeps a separate count per replica and adds them
increments = {"A": 3, "B": 5}
crdt = 1000 + sum(increments.values())
print("  CRDT counter after healing   :", crdt, "(every like kept)")
