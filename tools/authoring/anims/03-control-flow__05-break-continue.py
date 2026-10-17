from mkanim import Anim
HEADING = "Watch it with an example: finding the first free window seat"
INTRO = "A train coach's seats are checked one by one. <code>continue</code> skips booked seats; <code>break</code> stops the search as soon as a free window seat is found."
A = Anim("continue on booked, break on found", frames=6, h=210, label="break and continue in seat search")
A.box(6, 14, 348, 34, None, fill="board", stroke="board")
A.text(14, 36, "if (booked[s]) continue;   if (window[s]) break;", cls="chalk", mono=True, size=10)
seats = [("1", "W", True), ("2", "M", False), ("3", "A", True), ("4", "W", False), ("5", "M", False), ("6", "W", False)]
for i, (n, t, b) in enumerate(seats):
    x = 10 + i * 58
    A.box(x, 62, 50, 54, None, fill="soft-acc" if b else "card2", stroke="red" if b else "line")
    A.text(x + 25, 84, n, anchor="middle", bold=True, size=13, mono=True)
    A.text(x + 25, 102, {"W": "window", "M": "middle", "A": "aisle"}[t], anchor="middle", size=9, cls="ink2")
    if b: A.text(x + 25, 132, "booked", anchor="middle", size=9, cls="red", bold=True)
A.token(10, 140, 50, 22, "s", pos={1: "0,0", 2: "58,0", 3: "116,0", 4: "174,0", 5: "174,0", 6: "174,0"}, mono=True)
A.box(184, 62, 50, 54, None, fill="none", stroke="green", sw=3, on="4-")
notes = {1: "seat 1 booked → continue (skip)", 2: "seat 2 free, but middle → keep looking", 3: "seat 3 booked → continue",
         4: "seat 4 free and window → break!", 5: "seats 5 and 6 are never checked", 6: "Allotted seat 4 (window)"}
for f, t in notes.items(): A.text(10, 188, t, on=str(f), size=10.5, bold=True, cls="green" if f in (4, 6) else "ink")
A.caps([
 "<b>s = 1:</b> booked. <code>continue</code> jumps straight to the next round; the rest of the body is skipped.",
 "<b>s = 2:</b> free, but it's a middle seat, so the <code>break</code> condition is false. The loop goes on.",
 "<b>s = 3:</b> booked → <code>continue</code> again.",
 "<b>s = 4:</b> free and a window seat. <code>break</code> leaves the loop immediately.",
 "<b>Saved work:</b> seats 5 and 6 are never looked at. With 72 seats per coach and many coaches, stopping early matters.",
 "<b>Result:</b> seat 4 is allotted. Booking systems use this “skip bad ones, stop at the first good one” pattern all the time. (Simplified example.)",
])
