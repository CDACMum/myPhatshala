from mkanim import Anim
HEADING = "Watch it with an example: the listener that never leaves (a memory leak)"
INTRO = "Each opened screen registers a listener in a <code>static</code> list. Closing the screen forgets to remove it. Watch why the garbage collector can't free those objects."
A = Anim("Reachable objects are never collected", frames=6, h=230, label="memory leak through a static list")
A.box(6, 20, 110, 70, None, fill="board", stroke="board")
A.text(16, 40, "GC roots", size=10, cls="chalk", bold=True)
A.text(16, 58, "static listeners", size=9.5, cls="kw", mono=True)
A.text(16, 74, "main's locals", size=9.5, cls="kw", mono=True)
A.box(150, 20, 204, 42, None, fill="soft-blue", stroke="blue")
A.text(160, 38, "#1 ArrayList (listeners)", mono=True, size=9.5, bold=True)
for f, v in {1: "size = 0", 2: "size = 1", 3: "size = 2", 4: "size = 2", 5: "size = 2", 6: "size = 0"}.items():
    A.text(160, 54, v, on=str(f), mono=True, size=9.5)
A.arrow(116, 58, 148, 40, color="blue")
for i, on in enumerate(["2-5", "3-5"]):
    y = 80 + i * 56
    A.box(150, y, 204, 46, None, fill="soft-green", stroke="green", on=on)
    A.text(160, y + 18, f"#{i+2} Listener → Screen #{i+4}", mono=True, size=9.5, bold=True, on=on)
    A.text(160, y + 36, "(holds the screen's images)", size=9, cls="ink2", on=on)
    A.arrow(252, 62 if i == 0 else 126, 252, y, on=on, color="green")
A.box(150, 80, 204, 46, None, fill="soft-acc", stroke="red", on="4-5")
A.text(160, 98, "#2 screen closed, still listed", mono=True, size=9.5, bold=True, cls="red", on="4-5")
A.text(160, 116, "reachable → NOT collected", size=9.5, cls="red", on="4-5")
A.text(180, 200, "GC runs… #2 survives", anchor="middle", on="5", size=10.5, bold=True, cls="red")
A.text(180, 200, "listeners.remove(l) on close → GC frees them", anchor="middle", on="6", size=10.5, bold=True, cls="green")
A.text(10, 200, "", size=1)
A.caps([
 "<b>Start:</b> a <code>static</code> list of listeners. Static fields are <b>GC roots</b>: anything reachable from them stays alive.",
 "<b>Screen opened:</b> it registers listener #2, which refers to the screen and its images.",
 "<b>Another screen:</b> listener #3 is added. Fine so far.",
 "<b>Screen closed:</b> the user leaves the first screen, but the code never removes listener #2 from the list.",
 "<b>GC can't help:</b> the collector frees only <i>unreachable</i> objects. #2 is still reachable from the static list, so it (and its screen) stays forever. Repeat this a few thousand times and the app runs out of memory.",
 "<b>Fix:</b> remove the listener when the screen closes. Now nothing refers to those objects, and the next GC frees them. This exact bug is common in Android apps and long-running servers.",
])
