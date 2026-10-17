from mkanim import Anim
HEADING = "Watch it with an example: a delivery app that offers pickup instead"
INTRO = "A food-delivery backend can't deliver to some PIN codes. Its custom exception carries the PIN and the nearest hub, so the app can offer pickup without reading any message text."
A = Anim("NotServiceableException carries the data the app needs", frames=6, h=226, label="a custom exception with pincode and nearest hub fields travels to the app, which offers pickup")
A.box(6, 14, 348, 30, None, fill="board", stroke="board")
code = {1: "placeOrder(\"Biryani\", \"400099\");",
        2: "if (!served(pin)) throw new NotServ…",
        3: "super(msg); this.nearestHub = hub;",
        4: "catch (NotServiceableException e)",
        5: "e.getNearestHub()  // \"Andheri\"",
        6: "app.offerPickup(e.getNearestHub());"}
for f, t in code.items():
    A.text(14, 34, t, on=str(f), mono=True, size=10, cls="chalk")
A.box(10, 60, 110, 44, "Customer", fill="soft-blue", stroke="blue", size=10.5, bold=True, sub="PIN 400099")
A.box(10, 120, 110, 44, "Order service", fill="card2", stroke="line", size=10.5, bold=True, sub="served: 4000xx?")
A.arrow(65, 104, 65, 118, on="1", color="blue")
A.box(10, 120, 110, 44, None, fill="none", stroke="red", sw=2.5, on="2")
A.box(140, 56, 212, 96, None, fill="soft-acc", stroke="red", on="3-5")
A.text(148, 74, "#1 NotServiceableException", mono=True, size=9.4, bold=True, cls="red", on="3-5")
A.text(148, 94, "message: \"Can't deliver", mono=True, size=9, on="3-5")
A.text(148, 108, "          to 400099\"", mono=True, size=9, on="3-5")
A.text(148, 126, "pincode    = \"400099\"", mono=True, size=9, cls="acc", bold=True, on="3-5")
A.text(148, 142, "nearestHub = \"Andheri\"", mono=True, size=9, cls="acc", bold=True, on="3-5")
A.box(146, 132, 200, 16, None, fill="none", stroke="green", sw=2, on="5", rx=4)
A.arrow(120, 142, 138, 104, on="2", color="red")
A.text(148, 100, "throw!", size=11, bold=True, cls="red", on="2")
A.arrow(140, 90, 122, 82, on="4", color="red")
A.box(140, 56, 212, 96, None, fill="soft-green", stroke="green", on="6")
A.text(150, 78, "Delivery not available", size=10.5, bold=True, on="6")
A.text(150, 98, "Pick up from Andheri hub?", size=10, on="6")
A.box(150, 112, 90, 26, "Yes, pickup", fill="card2", stroke="green", size=9.5, bold=True, on="6")
A.note({1: "The customer orders to PIN 400099.",
        2: "That PIN isn't served: the service throws.",
        3: "The object carries the PIN and the nearest hub.",
        4: "The app's catch picks it out by its type.",
        5: "A getter gives the hub; no text parsing.",
        6: "Result: a useful pickup offer, not just an error."}, y=196, size=10)
A.caps([
 "<b>The order:</b> a customer in PIN 400099 orders biryani from a restaurant that delivers only to nearby areas.",
 "<b>Rule broken:</b> the order service finds the PIN isn't served and throws <code>NotServiceableException</code>, a class written by the team.",
 "<b>Inside the object:</b> its constructor passes the message to <code>super</code> and stores two extra fields, <code>pincode</code> and <code>nearestHub</code>.",
 "<b>Caught by type:</b> the app's catch for <code>NotServiceableException</code> matches. Other errors would go to other handlers.",
 "<b>Data, not text:</b> <code>getNearestHub()</code> returns \"Andheri\". If someone rewords the message tomorrow, this still works.",
 "<b>Better result:</b> instead of a dead end, the customer gets a pickup offer. That is the point of a custom exception: a name for the situation and the data to handle it.",
])
