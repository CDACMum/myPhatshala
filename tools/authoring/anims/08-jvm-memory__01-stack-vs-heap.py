from mkanim import Anim
HEADING = "Watch it with an example: two customers, two threads, one heap"
INTRO = "A shopping server handles Asha and Ravi at the same time. Each request runs on its own thread with its <b>own stack</b>, but both share the <b>one heap</b>."
A = Anim("Separate stacks, shared heap", frames=5, h=252, label="two thread stacks sharing a heap")
for i, (n, t, fl, q) in enumerate([("Thread 1: Asha", "blue", "soft-blue", "2"), ("Thread 2: Ravi", "track", "soft-acc", "1")]):
    x = 6 + i * 180
    A.text(x + 84, 20, n + " (stack)", anchor="middle", size=9.5, bold=True)
    A.box(x, 26, 168, 96, None, fill="card", stroke=t)
    A.box(x + 8, 84, 152, 30, "handle()", fill=fl, stroke=t, mono=True, size=9.5, on="1-4")
    A.box(x + 8, 46, 152, 32, None, fill=fl, stroke=t, on="2-4")
    A.text(x + 16, 60, "addToCart()", mono=True, size=9.5, on="2-4", bold=True)
    A.text(x + 16, 73, "qty = " + q + "   cart → ", mono=True, size=9, on="2-4")
    A.text(x + 84, 78, "(empty)", anchor="middle", size=9.5, cls="ink3", on="5")
A.text(180, 138, "HEAP (shared by all threads)", anchor="middle", size=9.5, bold=True, cls="green")
A.box(6, 144, 348, 62, None, fill="soft-green", stroke="green")
A.box(16, 154, 96, 42, "Cart", sub="Asha", fill="card2", stroke="blue", size=10, bold=True, on="3-")
A.box(132, 154, 96, 42, "Catalog", sub="1 object", fill="card2", stroke="green", size=10, bold=True)
A.box(248, 154, 96, 42, "Cart", sub="Ravi", fill="card2", stroke="track", size=10, bold=True, on="3-")
A.arrow(124, 78, 70, 152, on="3-4", color="blue")
A.arrow(304, 78, 296, 152, on="3-4", color="track")
A.arrow(150, 90, 166, 152, on="4", color="blue")
A.arrow(210, 90, 194, 152, on="4", color="track")
notes = {1: "each thread gets its own stack", 2: "local variables live in each frame", 3: "objects live on the heap",
         4: "both threads read the same Catalog", 5: "frames gone; carts stay while referenced"}
for f, t in notes.items(): A.text(180, 226, t, on=str(f), anchor="middle", size=10.5, bold=True)
A.text(180, 242, "stack: small, private, auto-cleaned · heap: big, shared, GC", on="5", anchor="middle", size=9.2, cls="ink2")
A.caps([
 "<b>Two requests at once:</b> the server runs each on a separate thread. Every thread has its own stack, starting with a frame for <code>handle()</code>.",
 "<b>Method calls:</b> <code>addToCart()</code> pushes a frame on each thread's stack. Asha's <code>qty = 2</code> and Ravi's <code>qty = 1</code> can't interfere: they are in different stacks.",
 "<b>Objects:</b> each request creates a Cart object. Objects never live on a stack; they are on the heap, and the frames only hold references to them.",
 "<b>Shared data:</b> both threads use the same Catalog object on the heap. Sharing saves memory, but shared objects that change need care (Module 12: synchronization).",
 "<b>Finish:</b> when the methods return, their frames vanish instantly. The carts stay on the heap as long as something (say, the user's session) refers to them; the garbage collector frees them later.",
])
