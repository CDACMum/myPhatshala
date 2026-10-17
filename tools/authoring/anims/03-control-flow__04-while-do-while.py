from mkanim import Anim
HEADING = "Watch it with an example: three tries to enter the OTP"
INTRO = "A banking app gives you 3 attempts. A <code>while</code> loop keeps asking until the OTP is right or the attempts run out. Nobody knows in advance how many rounds it will take."
A = Anim("while (attempts < 3 && !ok)", frames=6, h=220, label="while loop OTP attempts")
A.box(6, 14, 348, 34, None, fill="board", stroke="board")
A.text(14, 36, "while (attempts &lt; 3 &amp;&amp; !ok) { read OTP; attempts++; }", cls="chalk", mono=True, size=9.6)
A.box(10, 60, 150, 110, None, fill="card2", stroke="line")
A.text(85, 78, "Phone", anchor="middle", bold=True, size=10.5)
A.text(85, 94, "OTP sent: 4821", anchor="middle", mono=True, size=10, cls="ink2")
for f, v in {2: "1111", 3: "4812", 4: "4821"}.items():
    A.box(30, 106, 110, 30, v, on=f"{f}", fill="soft-blue", stroke="blue", mono=True, bold=True, size=12)
A.text(85, 158, "✗ wrong", on="2-3", anchor="middle", cls="red", bold=True, size=10.5)
A.text(85, 158, "✓ correct", on="4-", anchor="middle", cls="green", bold=True, size=10.5)
A.box(176, 60, 178, 110, None, fill="soft-acc", stroke="track")
for i, (n, vals) in enumerate([("attempts", {1: "0", 2: "1", 3: "2", 4: "3", 5: "3", 6: "3"}), ("ok", {1: "false", 2: "false", 3: "false", 4: "true", 5: "true", 6: "true"})]):
    A.text(188, 86 + i * 30, n, mono=True, bold=True, size=10.5)
    for f, v in vals.items(): A.text(340, 86 + i * 30, v, on=str(f), mono=True, anchor="end", size=11, bold=True, cls="acc")
A.text(188, 152, "condition:", size=10, cls="ink2")
for f, v in {1: "true → enter", 2: "true → again", 3: "true → again", 4: "false → exit", 5: "false → exit", 6: "false → exit"}.items():
    A.text(250, 152, v, on=str(f), size=10, bold=True, cls="green" if "exit" not in v else "red")
A.box(10, 180, 344, 30, "Logged in on attempt 3", on="5-", fill="soft-green", stroke="green", bold=True, size=11)
A.text(180, 200, "", size=1)
A.caps([
 "<b>Start:</b> attempts = 0, ok = false. The condition is checked <i>before</i> the first round: true, so the loop body runs.",
 "<b>Try 1:</b> the user types 1111. Wrong. attempts becomes 1. Back to the condition: still true.",
 "<b>Try 2:</b> 4812 (two digits swapped). Wrong again. attempts = 2.",
 "<b>Try 3:</b> 4821. Correct: ok = true, attempts = 3.",
 "<b>Exit:</b> the condition is now false (both parts would stop it), so the loop ends and the app logs the user in.",
 "<b>while vs do-while:</b> a <code>while</code> can run zero times. A menu that must appear at least once uses <code>do { … } while (…)</code>, which checks at the end.",
])
