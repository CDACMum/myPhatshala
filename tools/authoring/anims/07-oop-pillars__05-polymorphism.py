from mkanim import Anim
HEADING = "Watch it with an example: assigning a delivery to the right vehicle"
INTRO = "A dispatch screen keeps one <code>Vehicle v</code> variable. Watch what javac allows through that variable, what the JVM runs, and when a downcast is safe."
A = Anim("Vehicle v: one variable, many vehicles", frames=6, h=232, label="runtime polymorphism and safe downcasting in a delivery app")
A.box(6, 14, 348, 30, None, fill="board", stroke="board")
code = {1: "Vehicle v = new Bike();", 2: "v.eta(6);", 3: "v = new Drone(); v.eta(6);",
        4: "v.battery();", 5: "if (v instanceof Drone d) d.battery();", 6: "Bike b = (Bike) v;"}
for f, t in code.items():
    A.text(14, 34, t, on=str(f), mono=True, size=10.5, cls="chalk")
A.box(10, 58, 130, 40, None, fill="soft-blue", stroke="blue")
A.text(18, 74, "javac sees", size=9, cls="ink2")
A.text(18, 90, "v : Vehicle", mono=True, size=10.5, bold=True, cls="blue")
A.text(18, 116, "can call: eta()", mono=True, size=9.5, cls="ink2")
A.arrow(140, 78, 196, 78, color="blue")
# objects
A.box(200, 56, 152, 58, None, fill="soft-acc", stroke="track", on="1-2")
A.text(210, 74, "#1 Bike", mono=True, size=10.5, bold=True, cls="acc", on="1-2")
A.text(210, 92, "eta(km) 40 km/h +10", mono=True, size=9, cls="ink2", on="1-2")
A.box(200, 56, 152, 58, None, fill="soft-green", stroke="green", on="3-6")
A.text(210, 74, "#2 Drone", mono=True, size=10.5, bold=True, cls="green", on="3-6")
A.text(210, 92, "eta(km) 60 km/h +2", mono=True, size=9, cls="ink2", on="3-6")
A.text(210, 106, "battery() → 80%", mono=True, size=9, cls="ink2", on="3-6")
A.text(280, 130, "JVM sees the object", anchor="middle", size=9, cls="ink2")
# results
A.text(10, 154, "Bike.eta → 19 min", on="2", mono=True, size=12, bold=True, cls="green")
A.text(10, 154, "Drone.eta → 8 min", on="3", mono=True, size=12, bold=True, cls="green")
A.lines(10, 148, ["error: cannot find symbol", "  method battery()", "  location: variable v of type Vehicle"], on="4", size=9.5, mono=True, cls="red")
A.text(10, 154, "Drone? yes → d.battery() → 80%", on="5", mono=True, size=11, bold=True, cls="green")
A.lines(10, 148, ["ClassCastException:", "class Drone cannot be cast", "to class Bike"], on="6", size=9.5, mono=True, cls="red")
A.note({1: "Upcast: a Bike stored as a Vehicle, no cast needed.", 2: "The object's class decides which eta() runs.",
        3: "Same call, new object, different answer.", 4: "Through v, only Vehicle's methods are visible.",
        5: "Check first, then use the Drone-only method.", 6: "An unchecked downcast crashes at run time."}, y=214, size=10)
A.caps([
 "<b>Upcast:</b> the dispatcher stores a Bike in a <code>Vehicle</code> variable. Every Bike IS-A Vehicle, so no cast is needed.",
 "<b>Runtime polymorphism:</b> <code>v.eta(6)</code> runs Bike's override: 6 km at 40 km/h = 9 min, plus 10 min handling = 19 min.",
 "<b>Many forms:</b> the same variable now holds a Drone; the same call runs Drone's version: 6 + 2 = 8 min.",
 "<b>Compile-time limit:</b> <code>battery()</code> exists only on Drone. javac checks the variable's type, Vehicle, and refuses.",
 "<b>Safe downcast:</b> <code>instanceof Drone d</code> checks the real object and gives a Drone-typed variable, so <code>d.battery()</code> works.",
 "<b>Unsafe downcast:</b> forcing <code>(Bike) v</code> compiles, but the object is a Drone, so the JVM throws <code>ClassCastException</code>.",
])
