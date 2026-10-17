from mkanim import Anim
HEADING = "Watch it with an example: a 3-month EMI schedule"
INTRO = "Riya buys a Rs 30,000 laptop on a 3-month no-cost EMI. One <code>for</code> loop prints the whole schedule. Watch the counter, the check and the update in every round."
A = Anim("for (int m = 1; m <= 3; m++)", frames=6, h=226, label="for loop EMI schedule")
A.box(6, 14, 348, 34, None, fill="board", stroke="board")
A.text(14, 36, "for (int m = 1; m &lt;= 3; m++) { due -= 10000; … }", cls="chalk", mono=True, size=9.8)
A.box(10, 60, 104, 50, None, fill="soft-blue", stroke="blue")
A.text(62, 78, "m", anchor="middle", mono=True, bold=True, cls="blue", size=11)
for f, v in {1: "1", 2: "1", 3: "2", 4: "3", 5: "4", 6: "4"}.items(): A.text(62, 100, v, on=str(f), anchor="middle", mono=True, bold=True, size=16)
A.box(10, 122, 104, 50, None, fill="soft-acc", stroke="track")
A.text(62, 140, "due", anchor="middle", mono=True, bold=True, cls="acc", size=11)
for f, v in {1: "30000", 2: "20000", 3: "10000", 4: "0", 5: "0", 6: "0"}.items(): A.text(62, 162, v, on=str(f), anchor="middle", mono=True, bold=True, size=13)
A.box(130, 60, 224, 112, None, fill="card2", stroke="line")
A.text(140, 78, "Month   EMI     Left", mono=True, size=10, bold=True)
A.text(140, 100, "1       10000   20000", mono=True, size=10, on="2-")
A.text(140, 120, "2       10000   10000", mono=True, size=10, on="3-")
A.text(140, 140, "3       10000   0", mono=True, size=10, on="4-")
A.text(140, 162, "Paid off ✓", size=10.5, cls="green", bold=True, on="6")
notes = {1: "init: m = 1 (runs once)", 2: "1 &lt;= 3 true → body, then m++", 3: "2 &lt;= 3 true → body, then m++",
         4: "3 &lt;= 3 true → body, then m++", 5: "4 &lt;= 3 false → loop ends", 6: "3 rounds, 3 rows"}
for f, t in notes.items(): A.text(10, 196, t, on=str(f), size=10.5, mono=True, bold=True, cls="red" if f == 5 else "ink")
A.caps([
 "<b>Initialise:</b> <code>int m = 1</code> runs once, before the first round.",
 "<b>Round 1:</b> check <code>1 &lt;= 3</code>: true, so the body runs, prints month 1 and reduces <code>due</code> to 20,000. Then the update <code>m++</code> makes m = 2.",
 "<b>Round 2:</b> <code>2 &lt;= 3</code> true → month 2, due 10,000, m = 3.",
 "<b>Round 3:</b> <code>3 &lt;= 3</code> true → month 3, due 0, m = 4.",
 "<b>Exit:</b> <code>4 &lt;= 3</code> is false, so the loop stops. The check runs one more time than the body.",
 "<b>Done:</b> three rows printed by three lines of loop code. With 24 months you'd change only the 3. (No-cost EMI shown without interest, to keep it simple.)",
])
