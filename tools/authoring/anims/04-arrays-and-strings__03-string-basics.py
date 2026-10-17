from mkanim import Anim
HEADING = "Watch it with an example: is this password strong?"
INTRO = "A sign-up form needs at least 8 characters, one digit and one capital letter. Watch the loop read the String one character at a time with <code>charAt(i)</code>."
A = Anim("Checking \"Riya@2025\" with charAt()", frames=6, h=210, label="password check using charAt loop")
pw = "Riya@2025"
for i, ch in enumerate(pw):
    x = 10 + i * 38
    A.box(x, 30, 34, 36, ch, fill="soft-blue", stroke="blue", mono=True, bold=True, size=14)
    A.text(x + 17, 82, str(i), anchor="middle", mono=True, size=9, cls="ink2")
A.text(10, 20, "length() = 9", on="1-", mono=True, size=10, bold=True, cls="acc")
A.token(10, 90, 34, 20, "i", pos={2: "0,0", 3: "152,0", 4: "190,0", 5: "190,0"}, on="2-4", mono=True, size=10)
A.box(10, 30, 34, 36, None, fill="none", stroke="green", sw=3, on="2-")
A.box(200, 30, 34, 36, None, fill="none", stroke="green", sw=3, on="4-")
rows = [("length ≥ 8", "1-", "✓ 9"), ("has capital", "2-", "✓ 'R' at 0"), ("has digit", "4-", "✓ '2' at 5")]
for k, (n, on, v) in enumerate(rows):
    A.text(20, 136 + k * 20, n, size=10.5, on=on)
    A.text(150, 136 + k * 20, v, size=10.5, on=on, bold=True, cls="green", mono=True)
A.text(20, 156, "has capital", size=10.5, on="1", cls="ink3")
A.text(20, 176, "has digit", size=10.5, on="1-3", cls="ink3")
A.text(240, 136, "'@' is neither", on="3", size=10, cls="ink2")
A.box(220, 146, 134, 40, "STRONG ✓", fill="soft-green", stroke="green", on="5-", bold=True, size=13)
A.text(180, 202, "pw itself never changed: Strings are read, not edited", anchor="middle", on="6", size=9.5, cls="ink2")
A.caps([
 "<b>A String is a sequence of chars</b> with indexes 0 to <code>length() − 1</code>. Length 9 passes the first rule.",
 "<b>i = 0:</b> <code>pw.charAt(0)</code> is 'R'. <code>Character.isUpperCase('R')</code> is true → has a capital.",
 "<b>i = 1 … 4:</b> 'i', 'y', 'a', '@': not digits. The loop keeps going.",
 "<b>i = 5:</b> '2'. <code>Character.isDigit('2')</code> is true → has a digit. The loop could stop now.",
 "<b>Verdict:</b> all three rules pass. Real sign-up forms run checks like this (plus more) before saving a password, and store only a hash, never the text.",
 "<b>Read-only:</b> <code>charAt</code> only reads. A String object can never be changed after it is created; that's immutability.",
])
