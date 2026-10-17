from mkanim import Anim
HEADING = "Watch it with an example: one tracking page for parcels and food orders"
INTRO = "A courier parcel and a food order come from unrelated classes, but both implement <code>Trackable</code>. Watch the tracking page use the interface's abstract, default and static methods, and settle a default-method clash."
A = Anim("Trackable: one contract, unrelated classes", frames=6, h=232, label="interfaces with default and static methods in a delivery tracking page")
A.box(6, 14, 348, 30, None, fill="board", stroke="board")
code = {1: "Trackable t = new Parcel();", 2: "t = new FoodOrder();", 3: "t.summary();   // default",
        4: "Trackable.isValidAwb(\"AWB12345\")", 5: "class Parcel implements Trackable, Insurable",
        6: "label() { return Trackable.super.label(); }"}
for f, t in code.items():
    A.text(14, 34, t, on=str(f), mono=True, size=10.2, cls="chalk")
A.box(186, 54, 166, 80, None, fill="soft-blue", stroke="blue", sw=1.6)
A.text(194, 70, "«interface» Trackable", mono=True, size=9.4, bold=True, cls="blue")
A.text(194, 86, "String status();", mono=True, size=9, cls="ink2")
A.text(194, 100, "default summary()", mono=True, size=9, cls="ink2")
A.text(194, 114, "static isValidAwb()", mono=True, size=9, cls="ink2")
A.text(194, 128, "default label()", mono=True, size=9, cls="ink2", on="5-6")
A.box(190, 89, 158, 14, None, fill="none", stroke="green", on="3", sw=2, rx=3)
A.box(190, 103, 158, 14, None, fill="none", stroke="green", on="4", sw=2, rx=3)
A.box(190, 117, 158, 14, None, fill="none", stroke="red", on="5", sw=2, rx=3)
A.box(10, 54, 84, 32, "Parcel", fill="soft-acc", stroke="track", size=10, bold=True, mono=True)
A.box(10, 96, 84, 32, "FoodOrder", fill="soft-acc", stroke="track", size=10, bold=True, mono=True)
A.box(104, 74, 74, 22, "Insurable", fill="soft-green", stroke="green", size=9.5, bold=True, mono=True, on="5-6")
A.arrow(94, 80, 102, 84, dash=True, color="green", on="5-6")
A.arrow(94, 62, 184, 62, dash=True, color="blue")
A.arrow(94, 112, 184, 104, dash=True, color="blue")
A.box(10, 54, 84, 32, None, fill="none", stroke="green", on="1", sw=2.5)
A.box(10, 96, 84, 32, None, fill="none", stroke="green", on="2-3", sw=2.5)
A.text(10, 160, "t.status() → In transit", on="1", mono=True, size=10.5, bold=True, cls="green")
A.text(10, 160, "t.status() → Out for delivery", on="2", mono=True, size=10.5, bold=True, cls="green")
A.text(10, 160, "FoodOrder: Out for delivery", on="3", mono=True, size=10.5, bold=True, cls="green")
A.text(10, 160, "true  (called on the interface)", on="4", mono=True, size=10.5, bold=True, cls="green")
A.lines(10, 152, ["error: types Trackable and Insurable", "are incompatible; Parcel inherits", "unrelated defaults for label()"], on="5", mono=True, size=9.2, cls="red")
A.text(10, 160, "p.label() → tracked", on="6", mono=True, size=10.5, bold=True, cls="green")
A.note({1: "An interface type can hold any implementing object.", 2: "An unrelated class keeps the same promise.",
        3: "The default method runs on the FoodOrder.", 4: "Static methods belong to the interface itself.",
        5: "Two defaults with the same name: javac stops.", 6: "Override and pick one with X.super."}, y=214, size=10)
A.caps([
 "<b>Interface type:</b> the tracking page holds a <code>Trackable</code>. Right now it's a courier Parcel, so <code>status()</code> runs Parcel's implementation.",
 "<b>Unrelated class:</b> a FoodOrder has nothing in common with Parcel except the promise. The same variable and call work.",
 "<b>default method:</b> <code>summary()</code> is written once in the interface. It runs on the FoodOrder and calls its <code>status()</code>.",
 "<b>static method:</b> <code>Trackable.isValidAwb(...)</code> is a helper that belongs to the interface; it isn't inherited by Parcel or FoodOrder.",
 "<b>Diamond:</b> Parcel also implements <code>Insurable</code>, and both interfaces have a default <code>label()</code>. javac refuses to guess.",
 "<b>Resolved:</b> Parcel overrides <code>label()</code> and reuses Trackable's default with <code>Trackable.super.label()</code>.",
])
