from mkanim import Anim
HEADING = "Watch it with an example: printing a cinema seat map"
INTRO = "Rows A to C, seats 1 to 4. The outer loop picks a row; the inner loop runs completely for every row. Watch the order in which the 12 seats are printed."
A = Anim("Outer loop: rows. Inner loop: seats.", frames=6, h=222, label="nested loops seat map")
A.box(6, 14, 348, 34, None, fill="board", stroke="board")
A.text(14, 36, "for (row A..C)  for (seat 1..4)  print(row+seat)", cls="chalk", mono=True, size=10)
A.box(110, 58, 140, 16, "SCREEN", fill="soft-blue", stroke="blue", size=9, bold=True, rx=4)
order = {}
fr = {"A": [2, 2, 2, 2], "B": [3, 3, 4, 4], "C": [5, 5, 5, 5]}
for r, row in enumerate("ABC"):
    for c in range(4):
        x, y = 70 + c * 56, 86 + r * 38
        A.box(x, y, 48, 30, None, fill="card2", stroke="line")
        A.box(x, y, 48, 30, f"{row}{c+1}", fill="soft-green", stroke="green", mono=True, bold=True, size=11, on=f"{fr[row][c]}-")
    A.text(50, 106 + r * 38, row, anchor="middle", bold=True, size=11, cls="ink2")
A.box(64, 82, 230, 38, None, fill="none", stroke="track", sw=2.5, on="2")
A.box(64, 120, 230, 38, None, fill="none", stroke="track", sw=2.5, on="3-4")
A.box(64, 158, 230, 38, None, fill="none", stroke="track", sw=2.5, on="5")
notes = {1: "empty map: 3 rows × 4 seats", 2: "row A: inner loop runs 4 times", 3: "row B: inner loop starts again at 1",
         4: "B3, B4 → row B done", 5: "row C: 4 more → 12 prints", 6: "total = 3 × 4 = 12 iterations"}
for f, t in notes.items(): A.text(180, 212, t, on=str(f), size=10.5, bold=True, anchor="middle")
A.caps([
 "<b>The plan:</b> 3 rows and 4 seats per row. Two loops, one inside the other.",
 "<b>Row A:</b> the outer loop sets row = A. The inner loop then runs fully: A1, A2, A3, A4.",
 "<b>Row B:</b> the outer loop moves on. The inner loop <i>starts again from seat 1</i>: B1, B2…",
 "<b>…</b> B3, B4. Only when the inner loop finishes does the outer loop move to the next row.",
 "<b>Row C:</b> C1 to C4. That's 3 rounds of the outer loop.",
 "<b>Total work:</b> 3 × 4 = 12 inner iterations. Booking apps draw seat maps exactly like this; with 20 rows × 30 seats it's 600 iterations.",
])
