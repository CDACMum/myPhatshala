from mkanim import Anim
HEADING = "Watch it with an example: Tatkal booking at 10 AM"
INTRO = "Three people book at the same second. See why <b>multithreading</b> (one of Java's key features) matters, and how Java stops two people getting the same seat."
A = Anim("Three bookings at the same second", frames=5, h=230)
for i, n in enumerate(["Asha", "Ravi", "Meena"]):
    A.box(6, 30 + i * 56, 64, 40, n, fill="soft-blue", stroke="blue", bold=True, size=10.5)
A.box(96, 14, 258, 180, None, fill="card", stroke="line")
A.text(225, 32, "Booking server (one JVM)", anchor="middle", bold=True, size=10.5)
# single thread version
with A.g(on="2"):
    A.text(106, 54, "One thread: one request at a time", size=10, cls="ink2")
    for i, n in enumerate(["Asha", "Ravi", "Meena"]):
        A.box(106 + i * 80, 66, 72, 26, n + " 1s", fill="soft-acc", stroke="track", size=9.5)
    A.text(106, 116, "Meena waits 3 seconds.", size=10, cls="red", bold=True)
with A.g(on="3-"):
    A.text(106, 54, "Three threads work together", size=10, cls="ink2")
    for i, n in enumerate(["Asha", "Ravi", "Meena"]):
        A.box(106, 64 + i * 32, 110, 26, f"thread {i+1}: {n}", fill="soft-green", stroke="green", size=9.5)
A.box(236, 80, 108, 56, "seats left", fill="board", stroke="board", cls="chalk", size=10, on="4-", sub=None)
A.text(290, 126, "2", on="4", anchor="middle", cls="kw", bold=True, size=13, mono=True)
A.text(290, 126, "0", on="5", anchor="middle", cls="kw", bold=True, size=13, mono=True)
A.text(236, 152, "synchronized update", on="4-", size=9, cls="ink2")
A.text(106, 180, "Asha ✓  Ravi ✓  Meena: waitlist", on="5", size=10, cls="green", bold=True)
A.arrow(72, 50, 94, 50, on="1-"); A.arrow(72, 106, 94, 106, on="1-"); A.arrow(72, 162, 94, 162, on="1-")
A.caps([
 "<b>10:00:00 AM:</b> Asha, Ravi and Meena press <i>Book</i> at the same moment. All three requests reach the same booking server.",
 "<b>Without threads:</b> the server handles one request, then the next. If each takes 1 second, Meena waits 3 seconds. With lakhs of users, nobody would get a ticket.",
 "<b>With threads:</b> Java lets the server run many threads inside one program. Each request gets its own thread, so all three are handled at the same time.",
 "<b>Safety:</b> only 2 seats are left. The seat-count code is marked <code>synchronized</code>, so only one thread at a time can change it. No seat is sold twice.",
 "<b>Result:</b> Asha and Ravi get the last two seats; Meena goes to the waitlist. Fast <i>and</i> correct: this is why Java's built-in multithreading is listed as a key feature. (Simplified example.)",
])
