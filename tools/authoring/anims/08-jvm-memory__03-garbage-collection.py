from mkanim import Anim
HEADING = "Watch it with an example: lunch-rush orders in a food-delivery server"
INTRO = "Every order request creates a few short-lived objects; only the customer's cart session lives on. Watch a young collection throw away the rush and keep the few objects that matter."
A = Anim("Most objects die young", frames=6, h=230, label="young and old generation during a lunch rush")
A.box(6, 8, 348, 28, None, fill="board", stroke="board")
for f, t in {1: "OrderRequest r = parse(json);   // per request",
             2: "sessions.put(userId, cart);     // kept",
             3: "// Eden full: Pause Young",
             4: "// survivors copied, Eden freed",
             5: "// many GCs later: cart is old",
             6: "// result: rush cleaned cheaply"}.items():
    A.text(14, 27, t, on=str(f), mono=True, size=10, cls="chalk")
A.box(8, 46, 206, 104, None, fill="soft-acc", stroke="track")
A.text(16, 61, "Eden", size=10, bold=True, cls="acc")
A.box(220, 46, 62, 104, None, fill="soft-green", stroke="green")
A.text(251, 61, "Survivor", size=9.5, bold=True, cls="green", anchor="middle")
A.box(288, 46, 66, 104, None, fill="soft-blue", stroke="blue")
A.text(321, 61, "Old", size=10, bold=True, cls="blue", anchor="middle")
cells = [(18, 70), (56, 70), (94, 70), (132, 70), (170, 70), (18, 110), (56, 110), (94, 110), (132, 110), (170, 110)]
names = ["req", "json", "dto", "req", "json", "dto", "req", "json", "dto", "req"]
for i, (x, y) in enumerate(cells):
    on = "1-3" if i < 4 else "2-3"
    A.box(x, y, 34, 28, names[i], fill="card2", stroke="line", on=on, size=9, mono=True)
A.box(170, 110, 34, 28, "cart", fill="soft-green", stroke="green", on="2-3", size=9, mono=True, bold=True)
for (x, y) in cells[:9]:
    A.raw(f'<path d="M{x+4} {y+4} L{x+30} {y+24} M{x+30} {y+4} L{x+4} {y+24}" style="stroke:#D64545;stroke-width:1.6"/>', on="3")
A.box(234, 80, 34, 28, "cart", fill="soft-green", stroke="green", on="4", size=9, mono=True, bold=True)
A.text(251, 124, "age 1", on="4", size=9, cls="ink2", anchor="middle")
A.box(300, 80, 42, 28, "cart", fill="soft-green", stroke="blue", on="5-6", size=9, mono=True, bold=True)
A.text(321, 124, "age 15", on="5-6", size=9, cls="ink2", anchor="middle")
A.text(111, 104, "empty again", on="4-6", size=10, cls="ink2", anchor="middle")
A.text(10, 172, "9 temporary objects, 1 cart", on="2", size=10, cls="ink2")
A.text(10, 172, "STW pause ≈ 1 ms: mark from roots", on="3", size=10, cls="red", bold=True)
A.text(10, 172, "copied 1 object, freed 9 in one go", on="4", size=10, cls="green", bold=True)
A.text(10, 172, "promoted after surviving many minor GCs", on="5", size=10, cls="blue", bold=True)
A.text(10, 172, "cost depends on live objects, not garbage", on="6", size=10, cls="green", bold=True)
A.text(10, 190, "sessions map (a root) → cart", on="2-6", size=9.5, mono=True, cls="ink2")
A.caps([
 "<b>Rush starts:</b> each order request creates temporary objects (the raw request, parsed JSON, a DTO) in Eden.",
 "<b>One keeper:</b> the customer's cart is stored in a sessions map, which is reachable from a root. Everything else is needed only until the response is sent.",
 "<b>Eden full:</b> G1 pauses the threads for a young collection. Marking from the roots reaches only the cart; the crossed objects are garbage.",
 "<b>Copy and free:</b> the cart is copied to a survivor space with age 1, and the whole of Eden is reused at once. No dead object was visited.",
 "<b>Promotion:</b> the cart keeps surviving because the customer is still shopping. After enough minor GCs (at most 15) it moves to the old generation.",
 "<b>Why it scales:</b> a young collection's cost depends on how much is <i>live</i>, so a burst of lakhs of short-lived request objects is cheap to clean.",
])
