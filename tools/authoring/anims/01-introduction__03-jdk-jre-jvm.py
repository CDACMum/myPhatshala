from mkanim import Anim
HEADING = "Watch it with an example: Riya's chai-bill app goes to the shop"
INTRO = "Riya builds the app on her laptop (JDK) and the chai shop only runs it (runtime only). See which part does which job."
A = Anim("Build on a JDK, run on a runtime", frames=6, h=232)
A.box(6, 14, 168, 176, None, fill="card", stroke="blue")
A.text(90, 32, "Riya's laptop: JDK", anchor="middle", bold=True, cls="blue", size=10.5)
A.box(186, 14, 168, 176, None, fill="card", stroke="green")
A.text(270, 32, "Shop's PC: JRE only", anchor="middle", bold=True, cls="green", size=10.5)
A.box(16, 44, 72, 30, "Bill.java", fill="board", stroke="board", cls="chalk", mono=True, size=10, on="1-")
A.box(96, 44, 68, 30, "javac", fill="soft-blue", stroke="blue", size=10, bold=True, on="2-", mono=True)
A.box(16, 92, 72, 30, "Bill.class", fill="soft-acc", stroke="track", mono=True, size=10, on="2-")
A.arrow(52, 76, 52, 90, on="2-")
A.token(16, 92, 72, 30, "Bill.class", pos={3: "180,0"}, on="3-", mono=True, rx=6)
A.box(196, 134, 148, 46, None, fill="soft-green", stroke="green", on="4-")
A.text(270, 152, "JVM: load, verify, run", anchor="middle", size=10, bold=True, on="4-")
A.text(270, 168, "main(...)", anchor="middle", size=10, mono=True, on="4-")
A.arrow(232, 124, 232, 134, on="4-", color="green")
A.box(16, 140, 148, 40, "Total: Rs 75", fill="board", stroke="board", cls="chalk", mono=True, size=10.5, on="5", )
A.box(196, 44, 148, 30, "Total: Rs 75", fill="board", stroke="board", cls="chalk", mono=True, size=10.5, on="5")
A.box(196, 44, 148, 30, "javac: not found", fill="soft-acc", stroke="red", cls="red", mono=True, size=10, on="6", bold=True)
A.caps([
 "<b>Write:</b> Riya types <code>Bill.java</code> on her laptop. Her laptop has the full <b>JDK</b> (tools + runtime).",
 "<b>Compile:</b> <code>javac</code>, a tool that comes only with the JDK, turns Bill.java into <code>Bill.class</code> (bytecode).",
 "<b>Ship:</b> she copies only <code>Bill.class</code> to the shop's PC. The shop doesn't need the source code.",
 "<b>Run:</b> the shop's PC has a Java runtime (JRE). Its <b>JVM</b> loads the class, checks the bytecode, and runs <code>main</code>.",
 "<b>Same output:</b> both computers print the same bill, because the same bytecode runs on any JVM.",
 "<b>But:</b> typing <code>javac</code> on the shop's PC fails. A runtime can run programs but has no compiler. Developers need the JDK; users only need a runtime.",
])
