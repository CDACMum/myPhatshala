from mkanim import Anim
HEADING = "Watch it with an example: one Ride class, three bookings"
INTRO = "A ride app writes the <code>Ride</code> class once. Every booking is a separate object made from it, with its own values."
A = Anim("Blueprint → objects on the heap", frames=5, h=236, label="class as blueprint and three objects")
A.box(6, 14, 120, 140, None, fill="board", stroke="board")
for i, l in enumerate(["class Ride {", "  String from;", "  String to;", "  int fare;", "  void book()", "}"]):
    A.text(14, 34 + i * 18, l, mono=True, size=9.8, cls="chalk")
A.text(240, 26, "HEAP", bold=True, size=9.5, cls="ink2", anchor="middle")
rides = [("Kharghar", "Vashi", 120), ("Panvel", "CST", 450), ("Airport", "Powai", 300)]
for i, (a, b, fa) in enumerate(rides):
    y = 34 + i * 62
    with A.g(on=f"{i+2}-"):
        A.box(150, y, 204, 54, None, fill="soft-green", stroke="green")
        A.text(160, y + 18, f"#{i+1} Ride", mono=True, bold=True, size=10)
        A.text(160, y + 34, f"{a} → {b}", size=10)
        A.text(160, y + 48, f"fare = {fa}", mono=True, size=9.5)
    A.arrow(128, 84, 148, y + 27, on=f"{i+2}", color="green")
A.box(150, 34, 204, 54, None, fill="none", stroke="track", sw=3, on="5")
A.text(10, 176, "class = 1 blueprint", on="1-", size=10.5, bold=True)
A.text(10, 196, "objects so far: 0", on="1", size=10.5, mono=True)
A.text(10, 196, "objects so far: 1", on="2", size=10.5, mono=True)
A.text(10, 196, "objects so far: 2", on="3", size=10.5, mono=True)
A.text(10, 196, "objects so far: 3", on="4-", size=10.5, mono=True)
A.text(10, 224, "r1.fare = 150 changes only #1", on="5", size=10.5, bold=True, cls="acc")
A.caps([
 "<b>The class:</b> <code>Ride</code> describes what every ride has (from, to, fare) and can do (book). Writing it creates no ride yet.",
 "<b>new Ride(…):</b> the first booking creates object #1 on the heap, with its own copy of every field.",
 "<b>Second booking:</b> object #2, same shape, different values.",
 "<b>Third booking:</b> object #3. One class, as many objects as there are bookings.",
 "<b>Independent:</b> changing <code>r1.fare</code> changes only object #1. College ERPs, shopping carts and bank accounts all work this way: one class, thousands of objects.",
])
