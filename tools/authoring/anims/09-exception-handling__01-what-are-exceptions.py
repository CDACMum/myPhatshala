from mkanim import Anim
HEADING = "Watch it with an example: a batch job that survives a bad record"
INTRO = "A nightly job imports 5 student fee records. One row has text instead of a number. With the try/catch <b>inside</b> the loop, one bad row doesn't stop the other four."
A = Anim("try/catch around each record", frames=6, h=232, label="batch processing with exceptions")
rows = [("101", "45000"), ("102", "38000"), ("103", "N/A"), ("104", "52000"), ("105", "41000")]
for i, (r, a) in enumerate(rows):
    y = 18 + i * 32
    A.box(10, y, 150, 26, None, fill="card2", stroke="line")
    A.text(18, y + 17, f"{r}, {a}", mono=True, size=10.5, cls="red" if i == 2 else "ink", bold=(i == 2))
    on = f"{i+2 if i < 2 else i+1 if i>2 else 4}-" if False else None
done = {0: "2-", 1: "3-", 2: None, 3: "5-", 4: "6"}
for i in range(5):
    y = 18 + i * 32
    if done[i]: A.text(168, y + 17, "✓ saved", on=done[i], size=10, cls="green", bold=True)
A.text(168, 18 + 2 * 32 + 17, "✗ logged", on="4-", size=10, cls="red", bold=True)
A.token(150, 18, 26, 26, "▶", pos={1: "0,0", 2: "0,0", 3: "0,32", 4: "0,64", 5: "0,96", 6: "0,128"}, size=10, on="1-5")
A.box(250, 18, 104, 92, None, fill="board", stroke="board", on="4-")
A.text(258, 36, "log", size=9, cls="chalk", bold=True, on="4-")
A.text(258, 54, "row 103:", size=9, cls="kw", mono=True, on="4-")
A.text(258, 68, "NumberFormat", size=9, cls="kw", mono=True, on="4-")
A.text(258, 82, "Exception", size=9, cls="kw", mono=True, on="4-")
A.text(258, 96, "\"N/A\"", size=9, cls="kw", mono=True, on="4-")
A.box(10, 186, 344, 36, "Imported 4 of 5. 1 error to fix.", on="6", fill="soft-green", stroke="green", bold=True, size=11)
A.box(10, 186, 344, 36, "parseInt(\"N/A\") throws → jump to catch", on="4", fill="soft-acc", stroke="red", size=10, mono=True, cls="red")
A.caps([
 "<b>The job:</b> read each line, convert the amount with <code>Integer.parseInt</code>, save it. Row 103 has the text N/A instead of an amount.",
 "<b>Row 101:</b> parsed and saved.",
 "<b>Row 102:</b> saved.",
 "<b>Row 103:</b> <code>parseInt(\"N/A\")</code> throws <code>NumberFormatException</code>. Java stops that iteration and jumps to the <code>catch</code> block, which logs the row.",
 "<b>Keep going:</b> because the try/catch is inside the loop, the loop simply moves to row 104.",
 "<b>Result:</b> 4 rows imported and one clear error in the log. Without the catch, the exception would end the whole job at row 103 and rows 104–105 would never load.",
])
