from mkanim import Anim
HEADING = "Watch it with an example: sorting student names"
INTRO = "<code>compareTo</code> compares two Strings character by character using their Unicode numbers. Watch why “arjun” lands after “Bela”, and how <code>compareToIgnoreCase</code> fixes it."
A = Anim("\"arjun\".compareTo(\"Bela\")", frames=5, h=212, label="String compareTo character codes")
def word(x, y, w, on=None):
    for i, ch in enumerate(w):
        A.box(x + i * 30, y, 26, 28, ch, fill="soft-blue", stroke="blue", mono=True, bold=True, size=12, on=on)
        A.text(x + i * 30 + 13, y + 40, str(ord(ch)), anchor="middle", mono=True, size=9, cls="ink2", on=on)
A.text(10, 24, "1st", size=9.5, cls="ink2"); word(40, 10, "arjun")
A.text(10, 82, "2nd", size=9.5, cls="ink2"); word(40, 68, "Bela")
A.box(38, 6, 30, 82, None, fill="none", stroke="track", sw=2.5, on="2-3")
A.text(210, 30, "97 − 66 = 31", on="2-3", mono=True, size=11, bold=True)
A.text(210, 48, "positive → arjun after Bela", on="3", size=10, cls="red", bold=True)
A.box(6, 124, 348, 34, None, fill="board", stroke="board")
for f, t in {1: "Arrays.sort(names);", 2: "'a' (97) vs 'B' (66)", 3: "[\"Aman\", \"Bela\", \"arjun\"]", 4: "names.sort(String::compareToIgnoreCase);", 5: "[\"Aman\", \"arjun\", \"Bela\"]"}.items():
    A.text(14, 146, t, on=str(f), cls="chalk" if f not in (3,) else "kw", mono=True, size=10)
A.text(210, 30, "'a' vs 'b': 97−98 = −1", on="4-", mono=True, size=10, bold=True)
A.text(210, 48, "negative → arjun first ✓", on="4-", size=10, cls="green", bold=True)
A.text(180, 190, "Capital letters (65–90) come before small ones (97–122).", anchor="middle", size=9.6, cls="ink2", on="3-")
A.caps([
 "<b>Sorting:</b> <code>Arrays.sort</code> on Strings uses <code>compareTo</code>. Each character has a number (its Unicode code): 'a' is 97, 'B' is 66.",
 "<b>First difference:</b> the very first characters already differ. compareTo returns 97 − 66 = 31.",
 "<b>Positive means “after”:</b> so \"arjun\" is placed after \"Bela\". Users see a list that looks wrong: all capitalised names first.",
 "<b>Fix:</b> compare ignoring case. Now 'a' is compared with 'b': 97 − 98 = −1, negative, so arjun comes first.",
 "<b>Result:</b> Aman, arjun, Bela: the order a person expects. Contact lists and student rosters sort like this.",
])
