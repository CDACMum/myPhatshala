from mkanim import Anim
HEADING = "Watch it with an example: a fluent order builder"
INTRO = "Methods that end with <code>return this;</code> can be chained. Watch three calls work on the <b>same</b> object, because <code>this</code> is always “the object this method was called on”."
A = Anim("order.add(\"Tea\").add(\"Vada\").note(\"less sugar\")", frames=5, h=220, label="method chaining with return this")
A.box(6, 14, 348, 30, None, fill="board", stroke="board")
A.text(14, 34, "new Order().add(\"Tea\").add(\"Vada\").note(\"less sugar\");", mono=True, size=9.4, cls="chalk")
for i, (x, w) in enumerate([(12, 66), (76, 63), (138, 69), (206, 109)]):
    A.box(x, 19, w, 21, None, fill="none", stroke="track", sw=2, on=str(i + 1), rx=4)
A.box(170, 64, 184, 100, None, fill="soft-green", stroke="green")
A.text(180, 82, "#1 Order", mono=True, bold=True, size=10)
A.text(180, 102, "items = [ ]", mono=True, size=10, on="1")
A.text(180, 102, "items = [Tea]", mono=True, size=10, on="2")
A.text(180, 102, "items = [Tea, Vada]", mono=True, size=10, on="3-")
A.text(180, 122, "note = \"less sugar\"", mono=True, size=10, on="4-", bold=True)
A.box(10, 76, 130, 34, None, fill="soft-acc", stroke="track", on="2-4")
A.text(20, 98, "this → #1", mono=True, size=10.5, bold=True, on="2-4")
A.arrow(140, 93, 168, 100, on="2-4", color="track")
for f, t in {2: "add(\"Tea\") returns this", 3: "add(\"Vada\") returns this", 4: "note(…) returns this"}.items():
    A.text(10, 132, t, on=str(f), mono=True, size=9.5)
A.text(10, 152, "→ the next call is on #1 again", on="2-4", size=10, cls="ink2")
A.text(180, 196, "1 object, 3 calls, 0 temporary variables", anchor="middle", on="5", size=11, bold=True, cls="green")
A.caps([
 "<b>new Order():</b> creates object #1 with an empty item list.",
 "<b>add(\"Tea\"):</b> inside the method, <code>this</code> refers to #1. It adds Tea and ends with <code>return this;</code>, so the expression's value is #1.",
 "<b>.add(\"Vada\"):</b> is called on what the last call returned: the same #1. <code>this</code> is #1 again.",
 "<b>.note(\"less sugar\"):</b> same object again. Each call returns <code>this</code>, keeping the chain going.",
 "<b>Fluent style:</b> one object, built step by step in one readable line. <code>StringBuilder.append</code> and many builder classes in real libraries work exactly like this.",
])
