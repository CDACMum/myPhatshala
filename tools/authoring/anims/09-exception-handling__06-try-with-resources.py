from mkanim import Anim
HEADING = "Watch it with an example: a billing counter that always locks the cash drawer"
INTRO = "A supermarket counter opens the cash drawer and the receipt printer as resources. The printer runs out of paper mid-bill. Watch Java close both, printer first, before the cashier's catch block shows a message."
A = Anim("Paper runs out, the drawer still locks", frames=6, h=226, label="two resources closed in reverse order after an exception, before the catch block")
A.box(6, 14, 348, 30, None, fill="board", stroke="board")
code = {1: "try (CashDrawer d = till.open();",
        2: "     ReceiptPrinter p = new …()) {",
        3: "  p.print(bill7712);  // out of paper!",
        4: "// auto: p.close()",
        5: "// auto: d.close()",
        6: "} catch (PrinterException e) { … }"}
for f, t in code.items():
    A.text(14, 34, t, on=str(f), mono=True, size=10, cls="chalk")
# drawer
A.box(14, 62, 150, 54, None, fill="soft-green", stroke="green", on="1-4")
A.text(89, 84, "Cash drawer", anchor="middle", size=10.5, bold=True, on="1-4")
A.text(89, 102, "OPEN", anchor="middle", size=10, mono=True, cls="green", bold=True, on="1-4")
A.box(14, 62, 150, 54, None, fill="card2", stroke="line", on="5-")
A.text(89, 84, "Cash drawer", anchor="middle", size=10.5, bold=True, on="5-")
A.text(89, 102, "LOCKED", anchor="middle", size=10, mono=True, cls="blue", bold=True, on="5-")
A.box(14, 62, 150, 54, None, fill="none", stroke="blue", sw=3, on="5")
# printer
A.box(196, 62, 150, 54, None, fill="soft-green", stroke="green", on="2")
A.box(196, 62, 150, 54, None, fill="soft-acc", stroke="red", on="3")
A.box(196, 62, 150, 54, None, fill="card2", stroke="line", on="4-")
A.box(196, 62, 150, 54, None, fill="none", stroke="blue", sw=3, on="4")
A.text(271, 84, "Receipt printer", anchor="middle", size=10.5, bold=True, on="2-")
A.text(271, 102, "ON", anchor="middle", size=10, mono=True, cls="green", bold=True, on="2")
A.text(271, 102, "OUT OF PAPER", anchor="middle", size=10, mono=True, cls="red", bold=True, on="3")
A.text(271, 102, "OFF", anchor="middle", size=10, mono=True, cls="blue", bold=True, on="4-")
A.text(89, 134, "opened 1st, closed 2nd", anchor="middle", size=9.4, cls="ink2", on="2-")
A.text(271, 134, "opened 2nd, closed 1st", anchor="middle", size=9.4, cls="ink2", on="2-")
A.token(110, 146, 140, 24, "PrinterException", pos={3: "0,0", 4: "0,0", 5: "0,0"}, on="3-5", mono=True, size=9.4, fill="soft-acc", stroke="red")
A.text(180, 184, "(held while Java closes)", anchor="middle", size=9.4, cls="ink2", on="4-5")
A.box(40, 140, 280, 34, "Bill 7712 saved. Reprint after refill.", fill="soft-blue", stroke="blue", size=10, bold=True, on="6")
A.note({1: "Resource 1: the drawer opens.",
        2: "Resource 2: the printer starts.",
        3: "Printing fails: an exception is thrown.",
        4: "Java closes the printer first (last opened).",
        5: "Then it locks the drawer.",
        6: "Only now does the catch run."}, y=200, size=10)
A.caps([
 "<b>First resource:</b> the cash drawer opens. Java notes it must be closed at the end of the block.",
 "<b>Second resource:</b> the receipt printer is switched on. Both are listed in the try brackets, so neither needs a close call in our code.",
 "<b>Failure:</b> the printer runs out of paper in the middle of bill 7712 and throws a <code>PrinterException</code>. The rest of the block is skipped.",
 "<b>Reverse order:</b> before the exception goes anywhere, Java calls <code>p.close()</code>: the last resource opened is closed first.",
 "<b>Drawer locked:</b> then <code>d.close()</code> locks the drawer. Even with a failed bill, no cash drawer is left open at the counter.",
 "<b>Catch:</b> only after both are closed does the catch block run and show the cashier a helpful message. Had a close also failed, it would be attached as a suppressed exception.",
])
