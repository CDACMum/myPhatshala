from mkanim import Anim
HEADING = "Watch it with an example: an EMI calculator"
INTRO = "<code>emi(60000, 12)</code>: the arguments are copied into the parameters, the method works with its own copies, and one value travels back with <code>return</code>."
A = Anim("Arguments in, return value out", frames=5, h=222, label="parameters and return value")
A.box(6, 14, 348, 30, None, fill="board", stroke="board")
for f, t in {1: "int monthly = emi(60000, 12);", 2: "static int emi(int principal, int months)", 3: "  if (months <= 0) throw …;  return principal / months;", 4: "  return 5000;", 5: "int monthly = 5000;"}.items():
    A.text(14, 34, t.replace('<', '&lt;'), on=str(f), mono=True, size=10, cls="chalk")
A.box(10, 60, 150, 110, None, fill="soft-blue", stroke="blue")
A.text(20, 78, "main()", mono=True, bold=True, size=10.5)
A.text(20, 100, "args: 60000, 12", mono=True, size=10)
A.text(20, 122, "monthly = ?", mono=True, size=10, on="1-4")
A.text(20, 122, "monthly = 5000", mono=True, size=10, bold=True, cls="green", on="5")
A.box(200, 60, 154, 110, None, fill="soft-acc", stroke="track", on="2-4")
A.text(210, 78, "emi()", mono=True, bold=True, size=10.5, on="2-4")
A.text(210, 100, "principal =", mono=True, size=10, on="2-4")
A.text(282, 100, "60000", mono=True, size=10, on="3-4")
A.text(210, 120, "months    =", mono=True, size=10, on="2-4")
A.text(282, 120, "12", mono=True, size=10, on="3-4")
A.text(210, 146, "12 &gt; 0 ✓ → 5000", mono=True, size=10, on="3", cls="green", bold=True)
A.token(128, 88, 64, 22, "60000", pos={1: "0,0", 2: "150,0"}, on="1-2", mono=True, size=9.5)
A.token(128, 108, 64, 22, "12", pos={1: "0,0", 2: "150,0"}, on="1-2", mono=True, size=9.5)
A.token(250, 132, 60, 22, "5000", pos={4: "0,0"}, on="4", mono=True, fill="soft-green", stroke="green")
A.text(180, 196, "copies go in", on="2", anchor="middle", size=10.5, bold=True)
A.text(180, 196, "guard clause checks the input first", on="3", anchor="middle", size=10.5, bold=True)
A.text(180, 196, "return sends ONE value back", on="4", anchor="middle", size=10.5, bold=True)
A.text(180, 196, "the emi frame is gone; only the result stays", on="5", anchor="middle", size=10.5, bold=True, cls="green")
A.caps([
 "<b>The call:</b> <code>emi(60000, 12)</code> passes two <b>arguments</b>. Their order matters: the first goes to the first parameter.",
 "<b>Copying:</b> a new frame is created. Parameters <code>principal</code> and <code>months</code> receive <i>copies</i> of 60000 and 12.",
 "<b>Guard clause:</b> the method first rejects bad input (months must be positive), then computes 60000 / 12 = 5000.",
 "<b>return:</b> sends exactly one value back to the place it was called from. The method ends immediately.",
 "<b>Result:</b> the frame is popped and <code>monthly</code> = 5000. EMI, tax and insurance-premium calculators are all methods like this. (Real EMI formulas include interest; this is a no-cost EMI.)",
])
