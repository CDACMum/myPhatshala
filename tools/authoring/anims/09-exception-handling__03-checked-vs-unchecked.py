from mkanim import Anim
HEADING = "Watch it with an example: an exception travelling through three layers"
INTRO = "A web app's database layer gets a checked <code>SQLException</code>. Each layer decides what to do: wrap it, pass it on, or turn it into an HTTP response."
A = Anim("SQLException → wrapped → HTTP 500", frames=6, h=230, label="exception translation across layers")
layers = [("Controller", "web layer", "blue"), ("FeeService", "business rules", "green"), ("FeeDao", "database code", "track")]
for i, (n, s, c) in enumerate(layers):
    y = 16 + i * 58
    A.box(10, y, 150, 48, n, sub=s, fill="card2", stroke=c, bold=True, size=11, mono=True)
A.box(180, 132, 174, 44, None, fill="soft-acc", stroke="red", on="1-")
A.text(190, 150, "#1 SQLException (checked)", mono=True, size=9, bold=True, cls="red", on="1-")
A.text(190, 166, "\"connection refused\"", mono=True, size=9, on="1-")
A.box(180, 74, 174, 44, None, fill="soft-blue", stroke="blue", on="2-")
A.text(190, 92, "#2 FeeLoadException", mono=True, size=9, bold=True, cls="blue", on="2-")
A.text(190, 108, "(unchecked)  cause → #1", mono=True, size=9, on="2-")
A.arrow(266, 118, 266, 130, on="2-", color="track")
A.arrow(160, 160, 178, 154, on="1", color="red")
A.arrow(160, 100, 178, 96, on="3", color="blue")
A.arrow(160, 44, 180, 44, on="4-", color="blue")
A.box(180, 18, 174, 44, None, fill="board", stroke="board", on="4-")
A.text(190, 36, "HTTP 500", mono=True, size=10, bold=True, cls="kw", on="4-")
A.text(190, 52, "\"Could not load fees\"", mono=True, size=9, cls="chalk", on="4-")
A.box(10, 196, 344, 28, "log: FeeLoadException … Caused by: SQLException", on="5-", fill="board", stroke="board", cls="kw", mono=True, size=9)
A.text(180, 188, "", size=1)
A.caps([
 "<b>The failure:</b> FeeDao's JDBC call fails because the database is down: a <b>checked</b> <code>SQLException</code>.",
 "<b>Wrap once:</b> FeeDao can't fix a dead database, so it catches it and throws an unchecked <code>FeeLoadException(\"…\", e)</code> with #1 as the cause.",
 "<b>Pass through:</b> FeeService has nothing useful to do with it. Since it's unchecked, the service needs no try/catch and no <code>throws</code> clause.",
 "<b>Boundary:</b> the controller (or a global handler) catches it and sends a clean HTTP 500 response. The user sees a friendly message, not a stack trace.",
 "<b>Nothing lost:</b> the log keeps the full chain: the wrapper plus <i>Caused by: SQLException</i>, so engineers can find the real reason.",
 "<b>The pattern:</b> catch checked exceptions where they occur, wrap them with the cause, handle them once at the edge. Spring does exactly this with its <code>DataAccessException</code> family. (Simplified.)",
])
