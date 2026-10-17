from mkanim import Anim
HEADING = "Watch it with an example: three ways a discount method can go wrong (or right)"
INTRO = "Java always passes a copy. For an <code>int</code> that's a copy of the number; for an object it's a copy of the <b>reference</b>. Watch what each method can and can't change."
A = Anim("Copy of a value, copy of a reference", frames=6, h=232, label="pass by value with primitives and references")
A.box(6, 14, 348, 30, None, fill="board", stroke="board")
for f, t in {1: "int price = 500;  Cart cart = new Cart(500);", 2: "cut(price);  // price = price - 50 inside", 3: "// main's price is still 500", 4: "cut(cart);   // c.total = c.total - 50", 5: "reset(cart); // c = new Cart(0)", 6: "// cart still → #1, total 450"}.items():
    A.text(14, 34, t, on=str(f), mono=True, size=9.6, cls="chalk")
A.text(10, 64, "main", bold=True, size=10, cls="ink2")
A.box(10, 70, 110, 30, None, fill="soft-blue", stroke="blue")
for f, v in {1: "500", 2: "500", 3: "500", 4: "500", 5: "500", 6: "500"}.items(): pass
A.text(18, 90, "price = 500", mono=True, size=10)
A.box(10, 106, 110, 30, None, fill="soft-blue", stroke="blue")
A.text(18, 126, "cart → #1", mono=True, size=10)
A.text(140, 64, "method frame", bold=True, size=10, cls="ink2", on="2,4-5")
A.box(140, 70, 110, 30, None, fill="soft-acc", stroke="track", on="2-3")
A.text(148, 90, "p = 450", mono=True, size=10, on="2-3")
A.text(256, 90, "← own copy", size=9, cls="ink2", on="2-3")
A.box(140, 106, 110, 30, None, fill="soft-acc", stroke="track", on="4-5")
A.text(148, 126, "c → #1", mono=True, size=10, on="4")
A.text(148, 126, "c → #2", mono=True, size=10, on="5")
A.box(10, 160, 160, 56, None, fill="soft-green", stroke="green")
A.text(20, 178, "#1 Cart", mono=True, bold=True, size=10)
A.text(20, 198, "total = 500", mono=True, size=10, on="1-3")
A.text(20, 198, "total = 450", mono=True, size=10, bold=True, cls="green", on="4-")
A.arrow(66, 138, 66, 158, color="blue")
A.arrow(196, 138, 140, 162, color="track", on="4")
A.box(200, 160, 154, 56, None, fill="card2", stroke="line", on="5-")
A.text(210, 178, "#2 Cart", mono=True, bold=True, size=10, on="5-")
A.text(260, 126, "frame gone", size=9.5, cls="ink3", on="6")
A.text(210, 198, "total = 0", mono=True, size=10, on="5-")
A.arrow(196, 138, 250, 158, color="track", on="5")
A.caps([
 "<b>Setup:</b> <code>price</code> holds 500 directly. <code>cart</code> holds a reference to Cart object #1 on the heap.",
 "<b>cut(price):</b> the method gets its own copy <code>p</code> = 500 and changes it to 450. Only the copy changes.",
 "<b>Back in main:</b> <code>price</code> is still 500. A method can never change the caller's primitive variable.",
 "<b>cut(cart):</b> the copy <code>c</code> holds the same reference, so <code>c.total -= 50</code> changes object #1. main sees total 450.",
 "<b>reset(cart):</b> <code>c = new Cart(0)</code> points the <i>copy</i> at a new object #2. main's <code>cart</code> is untouched.",
 "<b>Rule:</b> Java is always pass-by-value. Through a reference copy you can change the object, but you can't make the caller's variable point somewhere else. That's why library methods like <code>Collections.sort(list)</code> work in place.",
])
