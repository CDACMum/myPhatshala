from mkanim import Anim
HEADING = "Watch it with an example: the JIT warms up a busy method"
INTRO = "A billing server calls <code>gst(price)</code> again and again. Watch the JVM start by interpreting it, then compile it to machine code once it becomes “hot”."
A = Anim("Interpreter first, JIT later", frames=5, h=226)
A.box(6, 14, 348, 40, None, fill="board", stroke="board")
A.text(18, 39, "for (bill : bills)  total += gst(bill);", cls="chalk", mono=True, size=10.5)
A.text(10, 76, "calls of gst():", size=10, cls="ink2")
for f, n in [(1, "1"), (2, "5,000"), (3, "10,000"), (4, "10,001"), (5, "1,00,000")]:
    A.text(104, 76, n, on=str(f), size=11, mono=True, bold=True, cls="acc")
A.box(6, 90, 166, 80, None, fill="soft-blue", stroke="blue")
A.text(89, 108, "Interpreter", anchor="middle", bold=True, cls="blue", size=10.5)
A.text(89, 124, "reads bytecode one", anchor="middle", size=9.5)
A.text(89, 137, "instruction at a time", anchor="middle", size=9.5)
A.box(188, 90, 166, 80, None, fill="soft-green", stroke="green", on="3-")
A.text(271, 108, "JIT compiler", anchor="middle", bold=True, cls="green", size=10.5, on="3-")
A.text(271, 124, "turns gst() into", anchor="middle", size=9.5, on="3-")
A.text(271, 137, "native machine code", anchor="middle", size=9.5, on="3-")
A.box(14, 146, 150, 16, None, fill="soft-acc", stroke="track", on="1-2", rx=4)
A.text(89, 158, "slow: ~ 40 units/call", anchor="middle", size=9, on="1-2")
A.text(271, 158, "fast: ~ 2 units/call", anchor="middle", size=9, on="4-", bold=True, cls="green")
A.box(120, 182, 120, 24, "HOT method!", fill="soft-acc", stroke="red", cls="red", bold=True, size=10, on="2-3", pulse=True)
A.arrow(172, 130, 186, 130, on="3-", color="green")
A.text(180, 214, "Same program, now much faster", anchor="middle", on="5", size=10.5, bold=True, cls="green")
A.caps([
 "<b>First call:</b> the JVM's interpreter runs the bytecode of <code>gst()</code> instruction by instruction. It starts quickly but runs slowly.",
 "<b>Counting:</b> the JVM counts how often each method runs. After thousands of calls, <code>gst()</code> is marked as a <i>hot</i> method.",
 "<b>JIT:</b> the Just-In-Time compiler translates the bytecode of <code>gst()</code> into native machine code for this CPU, in the background.",
 "<b>From now on:</b> calls go straight to the machine code. Each call is many times faster than interpreting.",
 "<b>Result:</b> servers often run slower in the first minutes (warm-up) and then speed up. Numbers here are illustrative; real thresholds depend on the JVM.",
])
