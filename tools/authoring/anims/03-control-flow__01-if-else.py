from mkanim import Anim
HEADING = "Watch it with an example: delivery charge slabs"
INTRO = "A food app charges delivery by order value. Follow two orders down the if / else-if ladder: Java checks conditions from the top and stops at the first true one."
A = Anim("Two orders through an else-if ladder", frames=6, h=232)
conds = [("if (amount < 199)", "fee = 49"), ("else if (amount < 499)", "fee = 29"), ("else", "fee = 0  (free)")]
for i, (c, r) in enumerate(conds):
    y = 40 + i * 54
    A.box(96, y, 150, 38, c.replace('<', '&lt;'), fill="card2", stroke="line", mono=True, size=10)
    A.box(256, y + 4, 98, 30, r, fill="soft-green", stroke="green", mono=True, size=9.5)
# highlight states
A.box(96, 40, 150, 38, None, fill="none", stroke="red", sw=2.5, on="2,5")
A.box(96, 94, 150, 38, None, fill="none", stroke="green", sw=2.5, on="3")
A.box(96, 94, 150, 38, None, fill="none", stroke="red", sw=2.5, on="5")
A.box(96, 148, 150, 38, None, fill="none", stroke="green", sw=2.5, on="6")
A.box(256, 98, 98, 30, None, fill="none", stroke="track", sw=3, on="3-4")
A.box(256, 152, 98, 30, None, fill="none", stroke="track", sw=3, on="6")
A.text(10, 24, "order", size=10, cls="ink2", bold=True)
A.token(10, 32, 70, 26, "Rs 349", pos={1: "0,0", 2: "0,10", 3: "0,64", 4: "0,64"}, on="1-4")
A.token(10, 32, 70, 26, "Rs 650", pos={5: "0,64", 6: "0,118"}, on="5-6", fill="soft-blue", stroke="blue")
A.text(10, 212, "349 &lt; 199? false → next check", on="2", size=10, cls="red")
A.text(10, 212, "349 &lt; 499? true → fee 29, rest skipped", on="3", size=10, cls="green", bold=True)
A.text(10, 212, "Pay 349 + 29 = 378", on="4", size=10.5, bold=True)
A.text(10, 212, "650: false, false → else", on="5", size=10, cls="red")
A.text(10, 212, "650 → free delivery. Pay 650", on="6", size=10.5, bold=True, cls="green")
A.caps([
 "<b>Order 1:</b> Rs 349 arrives. Java starts at the top of the ladder.",
 "<b>First check:</b> <code>349 &lt; 199</code> is false, so its block is skipped and Java moves to the next <code>else if</code>.",
 "<b>Second check:</b> <code>349 &lt; 499</code> is true. Its block runs: fee = 29. The rest of the ladder (the <code>else</code>) is skipped completely.",
 "<b>Bill:</b> 349 + 29 = 378. Exactly one branch ran.",
 "<b>Order 2:</b> Rs 650. Both conditions are false…",
 "<b>…so the <code>else</code> runs:</b> free delivery. Order matters: if the checks were written biggest-first, the slabs would be wrong. Real apps use the same ladder for tax slabs and discounts.",
])
