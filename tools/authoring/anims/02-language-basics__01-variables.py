from mkanim import Anim
HEADING = "Watch it with an example: a metro card through one day"
INTRO = "One variable, <code>balance</code>, holds the card's money. Watch the value in the box change while the name stays the same."
A = Anim("int balance changes, the box stays", frames=6, h=220)
A.box(6, 14, 348, 34, None, fill="board", stroke="board")
code = {1: "int balance = 200;", 2: "balance = balance - FARE;", 3: "balance = balance - FARE;",
        4: "balance += 100;   // recharge", 5: "FARE = 50;   // not allowed", 6: "System.out.println(balance);"}
for f, c in code.items(): A.text(16, 36, c, on=str(f), cls="chalk", mono=True, size=10.5)
A.box(30, 72, 130, 88, None, fill="soft-blue", stroke="blue")
A.text(95, 92, "balance", anchor="middle", bold=True, cls="blue", mono=True, size=11)
A.text(95, 104, "int, 4 bytes", anchor="middle", size=9, cls="ink2")
for f, v in {1: "200", 2: "170", 3: "140", 4: "240", 5: "240", 6: "240"}.items():
    A.text(95, 140, v, on=str(f), anchor="middle", mono=True, bold=True, size=20)
A.box(200, 72, 130, 88, None, fill="soft-acc", stroke="track")
A.text(265, 92, "FARE", anchor="middle", bold=True, mono=True, cls="acc", size=11)
A.text(265, 104, "final int", anchor="middle", size=9, cls="ink2")
A.text(265, 140, "30", anchor="middle", mono=True, bold=True, size=20)
A.text(265, 178, "compile error: cannot assign", anchor="middle", on="5", cls="red", bold=True, size=9.5)
A.text(265, 190, "a value to final variable FARE", anchor="middle", on="5", cls="red", size=9.5)
A.text(95, 178, "200 → 170 → 140 → 240", anchor="middle", on="6", size=10, mono=True, cls="green", bold=True)
A.box(16, 186, 158, 24, "Console: 240", fill="board", stroke="board", cls="chalk", mono=True, size=10, on="6")
A.caps([
 "<b>Declare:</b> <code>int balance = 200;</code> reserves a 4-byte box named <code>balance</code> and puts 200 in it. The fare is a constant, <code>final int FARE = 30;</code>",
 "<b>Morning trip:</b> the right side is worked out first (200 − 30), then the result 170 replaces the old value. The old 200 is gone.",
 "<b>Evening trip:</b> same line, new value: 140. A variable remembers only its latest value.",
 "<b>Recharge:</b> <code>balance += 100</code> is short for <code>balance = balance + 100</code>. Now 240.",
 "<b>Constant:</b> trying to change <code>FARE</code> fails at compile time, because it is <code>final</code>. Business rules like fares and tax rates are often constants.",
 "<b>Print:</b> the program reads the box and prints 240. Same name all day; the value moved 200 → 170 → 140 → 240.",
])
