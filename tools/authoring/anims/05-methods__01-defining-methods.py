from mkanim import Anim
HEADING = "Watch it with an example: one GST method, three bills"
INTRO = "The GST rule is written once, in <code>gst(int price)</code>, and called for every item. Watch each call push a new frame on the stack and pop it when it returns."
A = Anim("Calling gst() three times", frames=6, h=230, label="method calls pushing and popping stack frames")
A.box(6, 14, 168, 120, None, fill="board", stroke="board")
code = ["static int gst(int price) {", "  return price * 18 / 100;", "}", "", "main: total += gst(100);", "      total += gst(250);", "      total += gst(50);"]
for i, l in enumerate(code): A.text(14, 32 + i * 15, l, mono=True, size=9.2, cls="chalk")
A.box(10, 80, 160, 16, None, fill="none", stroke="track", sw=2, on="2-3", rx=3)
A.box(10, 95, 160, 16, None, fill="none", stroke="track", sw=2, on="4", rx=3)
A.box(10, 110, 160, 16, None, fill="none", stroke="track", sw=2, on="5", rx=3)
A.text(190, 24, "STACK", bold=True, size=9.5, cls="ink2")
A.box(186, 160, 168, 50, None, fill="soft-blue", stroke="blue")
A.text(196, 178, "main()", mono=True, bold=True, size=10)
for f, v in {1: "0", 2: "0", 3: "18", 4: "63", 5: "72", 6: "72"}.items():
    A.text(196, 198, "total = " + v, on=str(f), mono=True, size=10)
for f, p, r in [(2, 100, None), (4, 250, 45), (5, 50, 9)]:
    with A.g(on=str(f)):
        A.box(186, 100, 168, 52, None, fill="soft-acc", stroke="track")
        A.text(196, 118, "gst(int price)", mono=True, bold=True, size=10)
        A.text(196, 138, f"price = {p}" + (f"  → returns {r}" if r else ""), mono=True, size=10)
with A.g(on="3"):
    A.box(186, 100, 168, 52, None, fill="card", stroke="line")
    A.text(196, 130, "frame popped, 18 returned", size=10, cls="ink3")
A.text(10, 160, "Called once: frame pushed", on="2", size=10.5, bold=True)
A.text(10, 160, "Returned 18: frame popped", on="3", size=10.5, bold=True)
A.text(10, 160, "Same code, new frame", on="4-5", size=10.5, bold=True)
A.text(10, 160, "GST total: Rs 72", on="6", size=11, bold=True, cls="green")
A.text(10, 180, "1 method, 3 calls", on="6", size=10, cls="ink2")
A.caps([
 "<b>Before:</b> <code>main</code> has its frame on the stack with <code>total = 0</code>. The GST rule is written in one place.",
 "<b>Call 1:</b> <code>gst(100)</code> pushes a new frame. Its parameter <code>price</code> gets the value 100.",
 "<b>Return:</b> the method computes 18, returns it, and its frame is popped. <code>total</code> becomes 18.",
 "<b>Call 2:</b> <code>gst(250)</code>: a fresh frame with price = 250 returns 45. Total 63.",
 "<b>Call 3:</b> <code>gst(50)</code> returns 9. Total 72.",
 "<b>Why methods:</b> if the GST rate changes, you edit one line, not every bill. Real billing systems keep each business rule in one method like this.",
])
