from mkanim import Anim
HEADING = "Watch it with an example: a KYC form with a wrong PAN"
INTRO = "A bank's account-opening form passes through three methods. The innermost one checks the PAN number and throws; watch the exception pass through the middle layer and get caught where the screen can show a message."
A = Anim("throw in the validator, catch in the controller", frames=6, h=224, label="an IllegalArgumentException thrown by a PAN validator travels up two frames to the controller")
A.box(6, 14, 348, 30, None, fill="board", stroke="board")
code = {1: "submit(form) → openAccount() → checkPan()",
        2: "throw new IllegalArgumentException(…);",
        3: "// checkPan has no catch: frame popped",
        4: "// openAccount has no catch: popped",
        5: "catch (IllegalArgumentException e)",
        6: "screen.showError(e.getMessage());"}
for f, t in code.items():
    A.text(14, 34, t, on=str(f), mono=True, size=10, cls="chalk")
A.text(90, 60, "Stack", anchor="middle", size=10, bold=True, cls="ink2")
A.box(10, 68, 160, 32, "checkPan(\"ABCD1234\")", fill="card2", stroke="line", mono=True, size=9.5, on="1-2")
A.box(10, 68, 160, 32, None, fill="none", stroke="red", sw=2.5, on="2")
A.text(90, 88, "popped", anchor="middle", size=10, cls="red", on="3-6")
A.box(10, 108, 160, 32, "openAccount(form)", fill="card2", stroke="line", mono=True, size=9.5, on="1-3")
A.box(10, 108, 160, 32, None, fill="none", stroke="red", sw=2.5, on="3")
A.text(90, 128, "popped", anchor="middle", size=10, cls="red", on="4-6")
A.box(10, 148, 160, 32, "submit(form)  try/catch", fill="card2", stroke="line", mono=True, size=9.5)
A.box(10, 148, 160, 32, None, fill="none", stroke="green", sw=2.5, on="5-6")
A.token(182, 70, 166, 28, "IllegalArgumentException", pos={2: "0,0", 3: "0,40", 4: "0,80", 5: "0,80"}, on="2-5", mono=True, size=9, fill="soft-acc", stroke="red")
A.text(265, 64, "PAN must be 10 characters", anchor="middle", size=9, cls="red", on="2")
A.box(182, 58, 166, 92, None, fill="soft-blue", stroke="blue", on="6")
A.text(192, 78, "Open account", size=10.5, bold=True, on="6")
A.text(192, 98, "PAN: ABCD1234", size=10, mono=True, on="6")
A.text(192, 118, "PAN must be 10", size=10, cls="red", bold=True, on="6")
A.text(192, 134, "characters", size=10, cls="red", bold=True, on="6")
A.note({1: "Three frames: each method waits for the next.",
        2: "8 characters: the validator throws.",
        3: "The exception skips the rest of checkPan.",
        4: "openAccount never saves the account.",
        5: "submit's catch matches the type.",
        6: "The customer sees why; nothing was saved."}, y=206, size=10)
A.caps([
 "<b>Three layers:</b> the screen's <code>submit</code> calls <code>openAccount</code>, which calls <code>checkPan</code>. Only <code>submit</code> has a try/catch.",
 "<b>throw:</b> a PAN has 10 characters; \"ABCD1234\" has 8. <code>checkPan</code> creates an <code>IllegalArgumentException</code> with a clear message and throws it.",
 "<b>Popped:</b> <code>checkPan</code> has no catch, so its frame is removed and the exception moves to its caller.",
 "<b>Passed through:</b> <code>openAccount</code> has no catch either. Its \"save account\" line is skipped, so no half-created account exists.",
 "<b>Caught:</b> <code>submit</code>'s catch matches. Because the exception is unchecked, the two methods in between needed no <code>throws</code> clause.",
 "<b>Result:</b> the message written in the validator reaches the screen unchanged. One rule, one throw, one place that shows errors.",
])
