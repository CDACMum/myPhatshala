from mkanim import Anim
HEADING = "Watch it with an example: a payroll run that can't be tampered with"
INTRO = "A payroll module fixes the PF rate, the holiday list reference and the run steps with <code>final</code>. Watch what <code>final</code> blocks, and what it doesn't."
A = Anim("final in a payroll run", frames=6, h=232, label="final constant, final reference, unmodifiable copy and final method in payroll")
A.box(6, 14, 348, 30, None, fill="board", stroke="board")
code = {1: "static final double PF = 0.12;", 2: "PF = 0.10;", 3: "holidays.add(\"Diwali\");",
        4: "holidays = new ArrayList<>();", 5: "List.copyOf(holidays).add(\"Holi\");",
        6: "class FastPayroll extends Payroll"}
for f, t in code.items():
    A.text(14, 34, t, on=str(f), mono=True, size=10.5, cls="chalk")
# left: constant and reference
A.box(10, 56, 150, 34, None, fill="soft-blue", stroke="blue")
A.text(18, 77, "PF = 0.12", mono=True, size=10.5, bold=True, cls="blue")
A.raw('<path d="M136 72 v-4 a4 4 0 0 1 8 0 v4" style="stroke:var(--green);stroke-width:1.5;fill:none"/><rect x="134" y="72" width="12" height="9" rx="2" class="s-green"/>')
A.box(10, 98, 150, 34, None, fill="card2", stroke="line")
A.text(18, 119, "holidays → #1", mono=True, size=10.5, bold=True, cls="ink")
A.raw('<path d="M136 114 v-4 a4 4 0 0 1 8 0 v4" style="stroke:var(--green);stroke-width:1.5;fill:none"/><rect x="134" y="114" width="12" height="9" rx="2" class="s-green"/>')
A.arrow(160, 115, 196, 115, color="blue")
A.box(200, 96, 152, 38, None, fill="soft-acc", stroke="track")
A.text(208, 112, "#1 ArrayList", mono=True, size=9.5, bold=True, cls="acc")
A.text(208, 127, "[]", mono=True, size=9.5, on="1-2")
A.text(208, 127, "[Diwali]", mono=True, size=9.5, bold=True, on="3-")
A.box(200, 96, 152, 38, None, fill="none", stroke="green", on="3", sw=2.5)
A.box(200, 56, 152, 34, None, fill="card2", stroke="line", on="5")
A.text(208, 77, "copy: unmodifiable", mono=True, size=9.5, cls="ink2", on="5")
A.box(200, 56, 152, 34, None, fill="soft-green", stroke="green", on="1,6")
A.text(208, 77, "final run() { … }", mono=True, size=9.5, bold=True, cls="green", on="1,6")
A.box(200, 56, 152, 34, None, fill="none", stroke="red", on="6", sw=2.5)
A.text(10, 162, "net on Rs 30,000 = Rs 26,400.0", on="1", mono=True, size=10.5, bold=True, cls="green")
A.lines(10, 156, ["error: cannot assign a value", "to final variable PF"], on="2", mono=True, size=10, cls="red")
A.text(10, 162, "allowed: the list object changes", on="3", mono=True, size=10.5, bold=True, cls="green")
A.lines(10, 156, ["error: cannot assign a value", "to final variable holidays"], on="4", mono=True, size=10, cls="red")
A.lines(10, 156, ["java.lang.UnsupportedOperation", "Exception: the copy refuses"], on="5", mono=True, size=10, cls="red")
A.lines(10, 156, ["error: run() in FastPayroll cannot", "override run() in Payroll;", "overridden method is final"], on="6", mono=True, size=9.5, cls="red")
A.note({1: "A constant fixes the PF rate for the whole run.", 2: "A second assignment never compiles.",
        3: "final fixes the arrow, not the list's contents.", 4: "Pointing it at another list is what's blocked.",
        5: "To protect contents, hand out unmodifiable copies.", 6: "No subclass can skip the payroll steps."}, y=214, size=10)
A.caps([
 "<b>Constant:</b> <code>static final double PF = 0.12</code>. Every payslip uses 12%: Rs 30,000 − 3,600 = Rs 26,400.",
 "<b>Locked value:</b> a test that writes <code>PF = 0.10</code> doesn't compile, so a stray line can't change everyone's PF.",
 "<b>final reference:</b> <code>holidays</code> is final, yet <code>add(\"Diwali\")</code> works: the list object itself is ordinary and changeable.",
 "<b>What final blocks:</b> pointing <code>holidays</code> at a different list is a compile error.",
 "<b>Protecting contents:</b> the getter hands out <code>List.copyOf(holidays)</code>; trying to add to that copy throws <code>UnsupportedOperationException</code>.",
 "<b>final method:</b> <code>run()</code> is final in Payroll, so a FastPayroll subclass can't override it to skip PF or audit steps.",
])
