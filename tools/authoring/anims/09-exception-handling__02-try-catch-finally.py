from mkanim import Anim
HEADING = "Watch it with an example: a seat lock that must always be released"
INTRO = "A cinema app locks a seat while payment runs. Whether payment succeeds or fails, <code>finally</code> releases the lock, so the seat never stays stuck."
A = Anim("finally runs on success and on failure", frames=6, h=226, label="try catch finally releasing a lock")
A.box(6, 14, 170, 140, None, fill="board", stroke="board")
code = ["lockSeat(\"F7\");", "try {", "  pay(amount);", "} catch (PaymentException e) {", "  show(\"Payment failed\");", "} finally {", "  unlockSeat(\"F7\");", "}"]
for i, l in enumerate(code): A.text(14, 32 + i * 16, l, mono=True, size=9.2, cls="chalk")
hl = {1: 0, 2: 2, 3: 6, 4: 2, 5: 4, 6: 6}
for f, i in hl.items(): A.box(9, 21 + i * 16, 164, 15, None, fill="none", stroke="track", sw=2, on=str(f), rx=3)
A.text(190, 30, "Seat F7", bold=True, size=10.5)
A.box(190, 38, 60, 50, "F7", fill="soft-acc", stroke="red", bold=True, size=14, on="1-2,4-5")
A.box(190, 38, 60, 50, "F7", fill="soft-green", stroke="green", bold=True, size=14, on="3,6")
A.text(260, 60, "locked", on="1-2,4-5", size=10, cls="red", bold=True)
A.text(260, 60, "free", on="3,6", size=10, cls="green", bold=True)
A.text(190, 112, "Run 1: payment OK", on="1-3", size=10.5, bold=True, cls="blue")
A.text(190, 112, "Run 2: bank timeout", on="4-6", size=10.5, bold=True, cls="track")
A.text(190, 132, "try → finally", on="3", size=10, mono=True)
A.text(190, 132, "exception → catch", on="5", size=10, mono=True, cls="red")
A.text(190, 132, "catch → finally", on="6", size=10, mono=True)
A.text(180, 182, "finally runs in both cases", anchor="middle", on="6", size=11, bold=True, cls="green")
A.text(180, 200, "(also on return, and even if the catch throws)", anchor="middle", on="6", size=9.5, cls="ink2")
A.caps([
 "<b>Lock:</b> seat F7 is locked so nobody else can book it during payment.",
 "<b>Run 1, try:</b> <code>pay(amount)</code> succeeds. No exception, so the catch block is skipped.",
 "<b>finally:</b> runs anyway and unlocks F7 (the booking is saved elsewhere). Code in finally runs whether or not an exception happened.",
 "<b>Run 2:</b> another customer's payment times out inside <code>pay()</code> and throws <code>PaymentException</code>.",
 "<b>catch:</b> the rest of the try is skipped; the catch shows “Payment failed”.",
 "<b>finally again:</b> the seat is released, so someone else can book it. Without finally, a failed payment would leave seats locked forever. Locks, files and database connections are released this way (or with try-with-resources, Lesson 9.6).",
])
