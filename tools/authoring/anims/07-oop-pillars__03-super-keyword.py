from mkanim import Anim
HEADING = "Watch it with an example: the order in which constructors run"
INTRO = "<code>PremiumOrder extends Order</code>. Creating one runs three constructors. <code>super(…)</code> always runs the parent's part first, so the parent's fields are ready before the child uses them."
A = Anim("new PremiumOrder(\"A-17\")", frames=6, h=232, label="constructor chaining with super")
A.box(6, 14, 168, 112, None, fill="board", stroke="board")
code = ["PremiumOrder(String id) {", "  super(id);", "  priority = true;", "}", "Order(String id) {", "  this.id = id; time = now;"]
for i, l in enumerate(code): A.text(14, 32 + i * 16, l, mono=True, size=8.8, cls="chalk")
A.text(190, 24, "STACK", bold=True, size=9.5, cls="ink2")
stack = [("PremiumOrder(id)", "1-5"), ("Order(id)", "2-4"), ("Object()", "3")]
for i, (n, on) in enumerate(stack):
    A.box(186, 152 - i * 38, 168, 32, n, on=on, fill="soft-acc", stroke="track", mono=True, size=10)
A.box(6, 140, 168, 82, None, fill="soft-green", stroke="green", on="1-")
A.text(16, 158, "#1 PremiumOrder", mono=True, bold=True, size=10, on="1-")
A.text(16, 176, "id = null", mono=True, size=9.5, on="1-3", cls="ink3")
A.text(16, 176, "id = \"A-17\"", mono=True, size=9.5, on="4-", bold=True)
A.text(16, 192, "time = null", mono=True, size=9.5, on="1-3", cls="ink3")
A.text(16, 192, "time = 10:42", mono=True, size=9.5, on="4-", bold=True)
A.text(16, 208, "priority = false", mono=True, size=9.5, on="1-4", cls="ink3")
A.text(16, 208, "priority = true", mono=True, size=9.5, on="5-", bold=True, cls="green")
notes = {1: "child constructor called", 2: "super(id) → parent first", 3: "Order's own super(): Object", 4: "Order sets id, time", 5: "back in child: priority", 6: "fully built ✓"}
for f, t in notes.items(): A.text(190, 214, t, on=str(f), size=10, bold=True, cls="green" if f == 6 else "ink")
A.caps([
 "<b>new PremiumOrder(\"A-17\"):</b> memory for <i>all</i> fields (parent's and child's) is created with defaults, then the child constructor starts.",
 "<b>super(id):</b> its first line calls the parent constructor. If you don't write <code>super(…)</code>, Java inserts <code>super()</code> for you.",
 "<b>All the way up:</b> Order's constructor implicitly calls <code>Object()</code> first. The root always finishes first.",
 "<b>Parent's part:</b> back in Order, <code>id</code> and the creation time are set.",
 "<b>Child's part:</b> only now does PremiumOrder run its own line, <code>priority = true</code>. It can safely use <code>id</code>, because the parent already set it.",
 "<b>Order of work:</b> top-down: Object → Order → PremiumOrder. Base classes that stamp IDs and timestamps on every record rely on this.",
])
