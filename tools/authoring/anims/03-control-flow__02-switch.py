from mkanim import Anim
HEADING = "Watch it with an example: order status messages"
INTRO = "A shopping app sends one message per order status. See switch jump to the matching case, what happens if you forget <code>break</code>, and how the arrow form avoids it."
A = Anim("switch (status) on \"SHIPPED\"", frames=5, h=262)
A.box(6, 14, 120, 30, "status = \"SHIPPED\"", fill="soft-blue", stroke="blue", mono=True, size=9.5, bold=True)
cases = ["case \"PLACED\":", "case \"SHIPPED\":", "case \"OUT\":", "default:"]
msgs = ["\"Order placed\"", "\"On the way\"", "\"Out for delivery\"", "\"Check status\""]
for i in range(4):
    y = 56 + i * 34
    A.box(6, y, 120, 28, cases[i], fill="card2", stroke="line", mono=True, size=9.5)
    A.text(134, y + 18, "print(" + msgs[i] + ")", mono=True, size=9.5)
A.box(6, 90, 120, 28, None, fill="none", stroke="green", sw=2.5, on="2-")
A.arrow(126, 29, 126, 88, on="2-", color="green", bend=-20)
A.text(250, 109, "break;", mono=True, size=9.5, cls="acc", bold=True, on="1-3,5")
A.box(6, 196, 348, 60, None, fill="board", stroke="board", on="3-")
A.text(16, 212, "Console", size=9, cls="chalk", bold=True, on="3-")
A.text(16, 230, "On the way", mono=True, size=10, cls="chalk", on="3-")
A.text(110, 230, "Out for delivery", mono=True, size=10, cls="kw", on="4")
A.text(250, 230, "Check status", mono=True, size=10, cls="kw", on="4")
A.text(16, 248, "fall-through: 3 messages instead of 1!", size=10, cls="kw", bold=True, on="4")
A.text(110, 212, "case \"SHIPPED\" -&gt;", size=9.5, cls="str", mono=True, on="5")
A.text(110, 248, "arrow form: no break needed", size=9.5, cls="str", on="5")
A.caps([
 "<b>Status:</b> the order's status string is <code>\"SHIPPED\"</code>.",
 "<b>Jump:</b> switch doesn't test every case one by one like an if-ladder; it goes straight to the matching label <code>case \"SHIPPED\":</code>.",
 "<b>With break:</b> it prints “On the way”, then <code>break</code> leaves the switch. One message, correct.",
 "<b>Forgot break?</b> Execution <i>falls through</i> into the next cases and prints all the messages below. A real bug that sends customers wrong notifications.",
 "<b>Modern fix (Java 14+):</b> <code>case \"SHIPPED\" -&gt; …</code> runs only that case. No fall-through, no break to forget.",
])
