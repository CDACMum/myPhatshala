from mkanim import Anim
HEADING = "Watch it with an example: checkout rules at an online store"
INTRO = "Cart total Rs 850, the customer is a member. Watch each operator do its job, in the order Java evaluates them."
A = Anim("Operators deciding a discount", frames=6, h=226)
A.box(6, 14, 348, 34, None, fill="board", stroke="board")
code = {1: "int total = 850;  boolean member = true;", 2: "int gst = total * 18 / 100;", 3: "boolean big = total >= 500;",
        4: "if (big && member) discount = 100;", 5: "int fee = (total >= 999) ? 0 : 40;", 6: "pay = total + gst - discount + fee;"}
for f, t in code.items(): A.text(14, 36, t.replace('>', '&gt;').replace('&&', '&amp;&amp;'), on=str(f), cls="chalk", mono=True, size=10)
rows = [("total", "850", "1-"), ("gst", "153", "2-"), ("big", "true", "3-"), ("discount", "100", "4-"), ("fee", "40", "5-"), ("pay", "943", "6")]
for i, (n, v, on) in enumerate(rows):
    y = 62 + i * 25
    A.box(14, y, 150, 21, None, fill="soft-blue", stroke="blue", on=on, rx=5)
    A.text(22, y + 15, n, on=on, mono=True, size=10, bold=True)
    A.text(156, y + 15, v, on=on, mono=True, size=10.5, anchor="end", bold=True, cls="acc")
expl = {1: "Start values", 2: "* and / left to right:", 3: "Relational >= gives", 4: "&amp;&amp;: both must be true", 5: "Ternary ? : picks one", 6: "Arithmetic, left to right"}
expl2 = {1: "", 2: "850*18 = 15300, /100 = 153", 3: "a boolean: true", 4: "true &amp;&amp; true → true", 5: "850 >= 999 false → 40", 6: "850+153−100+40 = 943"}
for f in expl:
    A.text(180, 92, expl[f], on=str(f), size=10.5, bold=True)
    A.text(180, 110, expl2[f].replace('>=', '&gt;='), on=str(f), size=10, mono=True, cls="ink2")
A.box(180, 150, 170, 40, "Pay Rs 943", fill="soft-green", stroke="green", on="6", bold=True, size=13)
A.caps([
 "<b>Inputs:</b> cart total is 850 and the customer is a member.",
 "<b>GST:</b> <code>*</code> and <code>/</code> have the same precedence, so Java goes left to right: 850 × 18 = 15,300, then ÷ 100 = 153 (integer result).",
 "<b>Comparison:</b> <code>total &gt;= 500</code> doesn't change anything; it produces a <code>boolean</code>, here <code>true</code>.",
 "<b>Logical AND:</b> <code>big &amp;&amp; member</code> is true only if both are true. If <code>big</code> were false, Java would not even look at <code>member</code> (short-circuit).",
 "<b>Ternary:</b> <code>condition ? a : b</code> picks a value in one line. 850 is below 999, so delivery costs 40.",
 "<b>Final bill:</b> 850 + 153 − 100 + 40 = 943. Real checkouts use the same operators, just with more rules (and paise instead of rupees).",
])
