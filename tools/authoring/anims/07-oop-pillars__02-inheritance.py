from mkanim import Anim
HEADING = "Watch it with an example: finding a method up the hierarchy"
INTRO = "<code>SavingsAccount extends Account</code>. When you call a method on a savings account, the JVM looks in SavingsAccount first, then moves up to Account, then Object."
A = Anim("Method lookup: child first, then parent", frames=6, h=230, label="inheritance method lookup")
levels = [("Object", "toString(), equals() …", 16), ("Account", "deposit(), getBalance()", 80), ("SavingsAccount", "addInterest()", 144)]
for n, m, y in levels:
    A.box(10, y, 200, 52, None, fill="card2", stroke="line")
    A.text(20, y + 20, n, mono=True, bold=True, size=11)
    A.text(20, y + 38, m, mono=True, size=9.5, cls="ink2")
A.arrow(110, 144, 110, 134, color="ink"); A.arrow(110, 80, 110, 70, color="ink")
A.text(118, 140, "extends", size=8.5, cls="ink3"); A.text(118, 76, "extends", size=8.5, cls="ink3")
calls = {1: "sa.addInterest()", 2: "sa.addInterest()", 3: "sa.deposit(500)", 4: "sa.deposit(500)", 5: "sa.toString()", 6: "sa.toString()"}
for f, t in calls.items(): A.box(224, 16, 130, 30, t, on=str(f), fill="board", stroke="board", cls="chalk", mono=True, size=10)
A.box(10, 144, 200, 52, None, fill="none", stroke="green", sw=3, on="2")
A.box(10, 144, 200, 52, None, fill="none", stroke="red", sw=2.5, on="3")
A.box(10, 80, 200, 52, None, fill="none", stroke="green", sw=3, on="4")
A.box(10, 144, 200, 52, None, fill="none", stroke="red", sw=2.5, on="5")
A.box(10, 80, 200, 52, None, fill="none", stroke="red", sw=2.5, on="5")
A.box(10, 16, 200, 52, None, fill="none", stroke="green", sw=3, on="6")
notes = {1: "Where is addInterest()?", 2: "found in SavingsAccount ✓", 3: "not in SavingsAccount…", 4: "…found in Account ✓", 5: "not here, not in Account…", 6: "…found in Object ✓"}
for f, t in notes.items(): A.text(224, 72, t, on=str(f), size=10, bold=True, cls="green" if "✓" in t else "ink")
A.box(224, 100, 130, 96, None, fill="soft-green", stroke="green")
A.text(234, 118, "#1 SavingsAccount", mono=True, bold=True, size=9)
A.text(234, 138, "balance (from Account)", size=9)
A.text(234, 154, "rate (its own)", size=9)
A.text(234, 176, "one object, all fields", size=9, cls="ink2")
A.caps([
 "<b>The call:</b> <code>sa</code> refers to a SavingsAccount object. Which class's code runs for <code>addInterest()</code>?",
 "<b>Child first:</b> the JVM looks in the object's own class, SavingsAccount, and finds it there.",
 "<b>deposit(500):</b> SavingsAccount doesn't define it…",
 "<b>…so the search moves up</b> to the parent, Account, where it is found. The child reuses the parent's code without copying it.",
 "<b>toString():</b> neither SavingsAccount nor Account defines it…",
 "<b>…so it is found in Object</b>, the root of every class. Bank account types, exception classes and framework base classes all rely on this lookup. (The JVM caches the result, so it is fast.)",
])
