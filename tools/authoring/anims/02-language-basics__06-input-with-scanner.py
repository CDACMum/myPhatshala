from mkanim import Anim
HEADING = "Watch it with an example: the nextInt() then nextLine() trap"
INTRO = "A kiosk asks for age, then name. The user types <code>21</code> Enter <code>Riya</code> Enter, but the name comes out empty. Watch Scanner's input buffer to see why."
A = Anim("What Scanner leaves behind", frames=6, h=212)
A.box(6, 14, 348, 34, None, fill="board", stroke="board")
code = {1: "// user types: 21⏎Riya⏎", 2: "int age = sc.nextInt();", 3: "String name = sc.nextLine();",
        4: "// name is \"\"  (empty!)", 5: "sc.nextLine();  // eat the leftover ⏎", 6: "String name = sc.nextLine();"}
for f, t in code.items(): A.text(14, 36, t, on=str(f), cls="chalk", mono=True, size=10.5)
A.text(10, 72, "input buffer", bold=True, size=10, cls="ink2")
cells = ["2", "1", "⏎", "R", "i", "y", "a", "⏎"]
for i, c in enumerate(cells):
    x = 12 + i * 42
    used = {0: "2-", 1: "2-", 2: "3-", 3: "6", 4: "6", 5: "6", 6: "6", 7: "6"}[i]
    A.box(x, 80, 36, 36, c, fill="soft-blue", stroke="blue", mono=True, bold=True, size=13)
    A.box(x, 80, 36, 36, c, fill="card", stroke="line", mono=True, size=13, cls="ink3", on=used)
A.text(10, 146, "age  = 21", on="2-", mono=True, bold=True, size=11, cls="green")
A.text(190, 146, "name = \"\"", on="3-4", mono=True, bold=True, size=11, cls="red")
A.text(190, 146, "name = \"Riya\"", on="6", mono=True, bold=True, size=11, cls="green")
A.text(10, 176, "nextInt() reads the digits and stops before ⏎", on="2", size=10)
A.text(10, 176, "nextLine() reads up to the next ⏎: nothing!", on="3-4", size=10, cls="red")
A.text(10, 176, "an extra nextLine() throws the old ⏎ away", on="5", size=10)
A.text(10, 176, "now nextLine() gets the real name", on="6", size=10, cls="green", bold=True)
A.caps([
 "<b>Typing:</b> everything the user types goes into a buffer, including the Enter key (shown as ⏎).",
 "<b>nextInt():</b> reads <code>2</code> and <code>1</code>, makes the number 21, and stops. The ⏎ after it is still in the buffer.",
 "<b>nextLine():</b> reads characters until it finds a ⏎. The very first character is that leftover ⏎, so it returns an empty string.",
 "<b>The bug:</b> the program never waited for the name. This confuses almost every beginner (and appears in interviews).",
 "<b>Fix:</b> after <code>nextInt()</code>, call <code>sc.nextLine()</code> once and ignore the result. It consumes the leftover ⏎.",
 "<b>Works:</b> the next <code>nextLine()</code> reads <code>Riya</code>. Another fix: read every line with <code>nextLine()</code> and convert with <code>Integer.parseInt</code>.",
])
