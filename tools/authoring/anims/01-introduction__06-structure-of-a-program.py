from mkanim import Anim
HEADING = "Watch it with an example: a three-class fee app"
INTRO = "Real programs have many classes. Watch how the JVM starts from the one class that has <code>main</code> and loads the others only when they are needed."
A = Anim("java App → main → other classes", frames=5, h=226)
for i, (n, sub) in enumerate([("App", "has main()"), ("Student", "name, roll"), ("Fee", "amount()")]):
    A.box(6, 18 + i * 64, 110, 50, n + ".class", fill="card2", stroke="line", mono=True, size=10.5, bold=True, sub=sub)
A.box(140, 14, 214, 196, None, fill="card", stroke="green")
A.text(247, 32, "JVM memory", anchor="middle", bold=True, cls="green", size=10.5)
A.box(150, 44, 194, 30, "App loaded", fill="soft-green", stroke="green", size=10, on="1-")
A.box(150, 80, 194, 30, "main() running", fill="soft-acc", stroke="track", size=10, on="2-", mono=True)
A.box(150, 116, 194, 30, "Student loaded", fill="soft-green", stroke="green", size=10, on="3-")
A.box(150, 152, 194, 30, "Fee loaded", fill="soft-green", stroke="green", size=10, on="4-")
A.arrow(118, 43, 148, 59, on="1-", color="green")
A.arrow(118, 107, 148, 131, on="3-", color="green")
A.arrow(118, 171, 148, 167, on="4-", color="green")
A.text(247, 200, "Riya: fee Rs 45,000", anchor="middle", mono=True, size=10, on="5", bold=True)
A.caps([
 "<b>java App:</b> you name the class that has <code>main</code>. The JVM loads <code>App.class</code> first.",
 "<b>main starts:</b> the JVM calls <code>App.main(args)</code>. This is the only method it calls on its own.",
 "<b>new Student(...):</b> main uses Student for the first time, so now the JVM finds and loads <code>Student.class</code>.",
 "<b>Fee.amount(...):</b> the same happens for Fee. Classes are loaded <i>lazily</i>, on first use.",
 "<b>Output:</b> main prints the result and ends. One file per public class, one <code>main</code> to start: that's the structure of every Java app, big or small.",
])
