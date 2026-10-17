from mkanim import Anim
HEADING = "Watch it with an example: month-end interest at a bank"
INTRO = "One month-end job calls <code>a.interest()</code> on every account. Savings and fixed deposits override the method; a current account doesn't. Watch which version runs for each object."
A = Anim("One call, the account's own interest()", frames=6, h=230, label="method overriding for bank interest")
A.box(6, 14, 348, 30, None, fill="board", stroke="board")
code = {1: "Account a = new Savings(100000);", 2: "a.interest();", 3: "a = new FixedDeposit(100000);",
        4: "a = new Current(100000);", 5: "@Override double intrest() {…}", 6: "total += a.interest(); // each"}
for f, t in code.items():
    A.text(14, 34, t, on=str(f), mono=True, size=10.5, cls="chalk")
# variable
A.box(10, 62, 118, 30, None, fill="soft-blue", stroke="blue")
A.text(18, 81, "a : Account", mono=True, size=10, bold=True, cls="blue")
for f, t in {1: "→ Savings", 2: "→ Savings", 3: "→ FixedDeposit", 4: "→ Current", 6: "→ each account"}.items():
    A.text(18, 108, t, on=str(f), mono=True, size=9.5, cls="ink2")
# classes
rows = [("Account", "interest() → 0", 58), ("Savings", "3.5% of balance", 92), ("FixedDeposit", "7% of balance", 126), ("Current", "(no override)", 160)]
for name, sub, y in rows:
    A.box(176, y, 176, 28, None, fill="card2", stroke="line")
    A.text(184, y + 18, name, mono=True, size=10, bold=True)
    A.text(344, y + 18, sub, size=9, cls="ink2", anchor="end")
A.box(176, 92, 176, 28, None, fill="none", stroke="green", on="2", sw=2.5)
A.box(176, 126, 176, 28, None, fill="none", stroke="green", on="3", sw=2.5)
A.box(176, 160, 176, 28, None, fill="none", stroke="track", on="4", sw=2.5)
A.box(176, 58, 176, 28, None, fill="none", stroke="green", on="4", sw=2.5)
A.arrow(128, 77, 174, 104, on="2", color="green")
A.arrow(128, 77, 174, 138, on="3", color="green")
A.arrow(128, 77, 174, 172, on="4", color="track")
A.arrow(170, 168, 170, 76, on="4", color="green", dash=True)
# results
A.text(10, 134, "3500.0", on="2", mono=True, size=13, bold=True, cls="green")
A.text(10, 134, "7000.0", on="3", mono=True, size=13, bold=True, cls="green")
A.text(10, 134, "0.0", on="4", mono=True, size=13, bold=True, cls="green")
A.text(10, 152, "inherited from Account", on="4", size=9.5, cls="ink2")
A.lines(10, 128, ["error: method does", "not override or", "implement a method", "from a supertype"], on="5", size=9.5, cls="red", mono=True)
A.lines(10, 128, ["3500 + 7000 + 0", "= 10500.0"], on="6", size=11, mono=True, bold=True, cls="green")
A.note({1: "The variable's type is Account; the object is Savings.", 2: "Savings overrides interest(): 100000 × 3.5 / 100.",
        3: "Same call, new object: FixedDeposit's version.", 4: "Current has no override, so the JVM walks up.",
        5: "A typo with @Override never reaches the bank.", 6: "One loop pays every account the right interest."}, y=212, size=10)
A.caps([
 "<b>Setup:</b> the month-end job holds every account in a variable of type <code>Account</code>. Here it holds a Savings account with Rs 1,00,000.",
 "<b>Override runs:</b> <code>a.interest()</code> runs Savings' version, chosen by the object's class: 1,00,000 × 3.5 / 100 = 3,500.",
 "<b>Another object:</b> the same variable now holds a FixedDeposit. The same call runs FixedDeposit's override: 7,000.",
 "<b>No override:</b> Current doesn't declare <code>interest()</code>, so the JVM searches up to Account and uses its default of 0.",
 "<b>@Override catches typos:</b> a misspelt <code>intrest()</code> would silently be a new method and customers would get Account's 0%. With <code>@Override</code>, javac refuses to compile it.",
 "<b>The payoff:</b> one loop adds 3,500 + 7,000 + 0. Adding a senior-citizen account later means one new class with its own override; the job doesn't change.",
])
