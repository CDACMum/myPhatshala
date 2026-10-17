from mkanim import Anim
HEADING = "Watch it with an example: a shop loading its UPI payment plug-in"
INTRO = "The checkout loads payment providers by name from a plug-in JAR. Watch delegation find the class, linking prepare it, and the static block run only when the first payment arrives."
A = Anim("Loaded on first payment, initialised once", frames=6, h=236, label="class loading of a payment plug-in")
A.box(6, 8, 348, 28, None, fill="board", stroke="board")
for f, t in {1: "java -cp shop.jar:upi.jar Shop",
             2: "Class.forName(\"pay.UpiProvider\")",
             3: "// app loader reads upi.jar",
             4: "// link: verify, prepare",
             5: "// initialise: static block",
             6: "Class.forName(\"pay.UpiProvider\")  // 2nd"}.items():
    A.text(14, 27, t, on=str(f), mono=True, size=10, cls="chalk")
A.box(10, 46, 120, 28, "Bootstrap", fill="soft-blue", stroke="blue", size=10, bold=True)
A.box(10, 96, 120, 28, "Platform", fill="soft-blue", stroke="blue", size=10, bold=True)
A.box(10, 146, 120, 28, "Application", fill="soft-acc", stroke="track", size=10, bold=True)
A.arrow(40, 144, 40, 127, on="2", color="blue")
A.arrow(40, 94, 40, 77, on="2", color="blue")
A.text(50, 139, "ask parent", on="2", size=9, cls="blue")
A.text(50, 89, "ask parent", on="2", size=9, cls="blue")
A.box(10, 196, 120, 24, "upi.jar", fill="card2", stroke="track", on="3-", size=9.5, mono=True)
A.arrow(70, 194, 70, 177, on="3", color="green")
A.box(144, 46, 210, 176, None, fill="card", stroke="line")
A.text(154, 64, "pay.UpiProvider", mono=True, size=10, bold=True)
A.text(154, 84, "not loaded yet", on="1-2", size=10, cls="ink2")
A.text(154, 104, "parents: not found", on="2", size=10, cls="ink2")
A.text(154, 84, "loaded by: app", on="3-", size=10, cls="green", bold=True)
A.text(154, 104, "verify ✓  prepare ✓", on="4-", size=10, cls="green")
A.text(154, 124, "static int feePaise =", on="4-", size=9.5, mono=True)
A.text(344, 124, "0", on="4", size=10, mono=True, bold=True, anchor="end")
A.text(344, 124, "200", on="5-", size=10, mono=True, bold=True, anchor="end", cls="green")
A.text(154, 146, "static block runs:", on="5", size=9.5, cls="acc", bold=True)
A.text(154, 164, "prints \"UPI ready\"", on="5", size=9.5, mono=True)
A.text(154, 146, "already initialised:", on="6", size=9.5, cls="green", bold=True)
A.text(154, 164, "nothing runs again", on="6", size=9.5)
A.text(154, 192, "CardProvider (no JAR):", on="6", size=9.5, cls="red", bold=True)
A.text(154, 208, "ClassNotFoundException", on="6", size=9.5, cls="red", mono=True)
A.caps([
 "<b>Start-up:</b> the shop starts with both JARs on the class path, but <code>UpiProvider</code> isn't loaded: no one has needed it yet.",
 "<b>First payment:</b> the checkout loads the provider by name. The application loader first asks platform, which asks bootstrap. Neither knows a class called <code>pay.UpiProvider</code>.",
 "<b>Found:</b> the application loader reads the class from <code>upi.jar</code> and defines it.",
 "<b>Linked:</b> the bytecode is verified and the static field <code>feePaise</code> is prepared with its default, 0.",
 "<b>Initialised:</b> <code>Class.forName</code> also initialises the class, so the static initializer runs once: the fee becomes 200 paise and “UPI ready” is printed.",
 "<b>Next payments:</b> the class is already loaded and initialised, so nothing runs again. A provider whose JAR is missing fails with <code>ClassNotFoundException</code>, which the checkout can catch and report.",
])
