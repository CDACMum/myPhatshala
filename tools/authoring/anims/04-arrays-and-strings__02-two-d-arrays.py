from mkanim import Anim
HEADING = "Watch it with an example: a class marks sheet"
INTRO = "3 students × 3 subjects in one <code>int[][]</code>. Watch the nested loops add each row, and see how Java really stores it: an array of row arrays."
A = Anim("int[][] marks = new int[3][3]", frames=6, h=264, label="2D array marks table with row totals")
names = ["Riya", "Kabir", "Asha"]; M = [[78, 85, 90], [65, 70, 72], [88, 92, 95]]
A.text(70, 22, "Maths  Phys  Chem   Total", size=9.5, bold=True, cls="ink2", mono=True)
for r in range(3):
    y = 30 + r * 40
    A.text(8, y + 22, names[r], size=10, bold=True)
    for c in range(3):
        A.box(64 + c * 48, y, 44, 32, str(M[r][c]), fill="card2", stroke="line", mono=True, size=11)
    tot = sum(M[r])
    A.box(214, y, 52, 32, str(tot), fill="soft-green", stroke="green", mono=True, bold=True, size=11, on=f"{r+2}-")
    A.box(60, y - 3, 152, 38, None, fill="none", stroke="track", sw=2.5, on=str(r + 2))
A.text(280, 52, "r = 0", on="2", mono=True, size=10, bold=True, cls="acc")
A.text(280, 92, "r = 1", on="3", mono=True, size=10, bold=True, cls="acc")
A.text(280, 132, "r = 2", on="4", mono=True, size=10, bold=True, cls="acc")
A.text(180, 176, "Topper: Asha (275)", anchor="middle", on="5", size=11, bold=True, cls="green")
with A.g(on="6"):
    A.box(6, 166, 100, 92, None, fill="soft-blue", stroke="blue")
    A.text(56, 182, "marks", anchor="middle", mono=True, bold=True, size=10.5)
    for r in range(3):
        A.box(16, 190 + r * 22, 80, 18, f"[{r}] → row", fill="card2", stroke="line", size=9, mono=True, rx=3)
        A.arrow(98, 199 + r * 22, 134, 181 + r * 28, color="blue", sw=1.4)
        A.box(136, 170 + r * 28, 124, 22, "{" + ", ".join(map(str, M[r])) + "}", fill="card2", stroke="blue", size=10, mono=True, rx=4)
    A.text(268, 196, "each row is its", size=9.5, cls="ink2")
    A.text(268, 209, "own int[] object", size=9.5, cls="ink2")
A.caps([
 "<b>The table:</b> <code>marks[r][c]</code> is student r's mark in subject c. <code>marks[1][2]</code> is Kabir's Chem mark, 72.",
 "<b>Outer loop r = 0:</b> the inner loop walks across Riya's row: 78 + 85 + 90 = 253.",
 "<b>r = 1:</b> Kabir's row: 65 + 70 + 72 = 207. The inner loop always restarts at column 0.",
 "<b>r = 2:</b> Asha's row: 88 + 92 + 95 = 275.",
 "<b>Result:</b> the highest total is Asha's 275. School ERPs and report cards work on exactly this shape of data.",
 "<b>Behind the screen:</b> Java has no single grid. <code>marks</code> refers to an array of 3 references, and each points to its own row array. That's why rows can even have different lengths (jagged arrays).",
])
