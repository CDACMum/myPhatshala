from mkanim import Anim
HEADING = "Watch it with an example: a customer with no address"
INTRO = "A delivery app stores each customer as an object. One customer skipped the address field. Follow the references and see where the famous <code>NullPointerException</code> comes from."
A = Anim("Following a reference to nowhere", frames=5, h=224)
A.box(6, 14, 348, 34, None, fill="board", stroke="board")
code = {1: "Customer c = new Customer(\"Kabir\");", 2: "// c.address was never set", 3: "String city = c.address.city;",
        4: "if (c.address != null) city = c.address.city;", 5: "else System.out.println(\"Add address\");"}
for f, t in code.items(): A.text(14, 36, t, on=str(f), cls="chalk", mono=True, size=10)
A.text(14, 70, "STACK", bold=True, size=9.5, cls="ink2"); A.text(150, 70, "HEAP", bold=True, size=9.5, cls="ink2")
A.box(10, 78, 110, 40, None, fill="soft-blue", stroke="blue")
A.text(20, 96, "c", mono=True, bold=True, size=11); A.text(20, 110, "→ #1", mono=True, size=10)
A.box(150, 78, 200, 72, None, fill="soft-green", stroke="green")
A.text(160, 96, "#1 Customer", bold=True, mono=True, size=10.5)
A.text(160, 114, "name    → \"Kabir\"", mono=True, size=10)
A.text(160, 132, "address = null", mono=True, size=10, cls="red", bold=True)
A.arrow(120, 98, 148, 98, color="blue")
A.text(262, 132, "→ ?", on="2-", mono=True, size=10, cls="red", bold=True)
A.box(10, 160, 340, 44, None, fill="soft-acc", stroke="red", on="3")
A.text(20, 178, "NullPointerException: Cannot read field", mono=True, size=9.5, cls="red", bold=True, on="3")
A.text(20, 194, "\"city\" because \"c.address\" is null", mono=True, size=9.5, cls="red", on="3")
A.box(10, 160, 340, 44, None, fill="soft-green", stroke="green", on="4-")
A.text(20, 178, "check first: address is null → skip", size=10, on="4", bold=True, cls="green")
A.text(20, 178, "Console: Add address", size=10, on="5", bold=True, mono=True, cls="green")
A.text(20, 194, "no crash; the app asks the user instead", size=9.5, on="4-", cls="ink2")
A.caps([
 "<b>Create:</b> <code>new Customer(\"Kabir\")</code> makes object #1 on the heap. The variable <code>c</code> on the stack holds a <b>reference</b> (an arrow) to it.",
 "<b>Missing data:</b> the address field is a reference too, but nobody set it, so it holds <code>null</code>: an arrow that points to no object.",
 "<b>Crash:</b> <code>c.address.city</code> follows <code>c</code> to #1 (fine), then tries to follow <code>address</code>, which leads nowhere. Java throws <code>NullPointerException</code> and names the null part.",
 "<b>Fix:</b> check <code>c.address != null</code> before following it.",
 "<b>Result:</b> the app shows “Add address” instead of crashing. Null checks at the edges (forms, APIs, database rows) prevent most NPEs in production.",
])
