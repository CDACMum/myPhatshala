from mkanim import Anim
HEADING = "Watch it with an example: when the box is too small"
INTRO = "A video app counts views in an <code>int</code>. A shop adds prices in <code>double</code>. Both hit a surprise. Watch what happens to the bits, and the fix."
A = Anim("int overflow and double rounding", frames=6, h=192)
A.box(6, 14, 348, 34, None, fill="board", stroke="board")
code = {1: "int views = 2147483647;  // Integer.MAX_VALUE", 2: "views = views + 1;", 3: "long views = 2147483647L + 1;",
        4: "double total = 0.1 + 0.2;", 5: "double total = 0.1 + 0.2;", 6: "long paise = 10 + 20;  // money in paise"}
for f, c in code.items(): A.text(14, 36, c, on=str(f), cls="chalk", mono=True, size=10)
# int bar 32 bits
with A.g(on="1-2"):
    A.text(10, 70, "int: 32 bits", bold=True, size=10.5)
    A.box(10, 78, 340, 30, None, fill="soft-blue", stroke="blue", rx=4)
A.text(180, 98, "0111 1111 1111 1111 1111 1111 1111 1111", anchor="middle", mono=True, size=9.5, on="1")
A.text(180, 98, "1000 0000 0000 0000 0000 0000 0000 0000", anchor="middle", mono=True, size=9.5, on="2", cls="red", bold=True)
A.text(180, 132, "= 2,147,483,647 (largest int)", anchor="middle", size=11, on="1", bold=True)
A.text(180, 132, "= −2,147,483,648  (wrapped around!)", anchor="middle", size=11, on="2", bold=True, cls="red")
with A.g(on="3"):
    A.text(10, 70, "long: 64 bits", bold=True, size=10.5)
    A.box(10, 78, 340, 30, None, fill="soft-green", stroke="green", rx=4)
    A.text(180, 98, "0000…0000 1000 0000 0000 … 0000", anchor="middle", mono=True, size=9.5)
    A.text(180, 132, "= 2,147,483,648  ✓ room to grow", anchor="middle", size=11, bold=True, cls="green")
with A.g(on="4-5"):
    A.text(10, 70, "double: binary fractions", bold=True, size=10.5)
    A.box(10, 78, 165, 30, "0.1 ≈ 0.1000000000000000055…", fill="soft-blue", stroke="blue", size=8.5, mono=True, rx=4)
    A.box(185, 78, 165, 30, "0.2 ≈ 0.2000000000000000111…", fill="soft-blue", stroke="blue", size=8.5, mono=True, rx=4)
A.text(180, 132, "prints 0.30000000000000004", anchor="middle", size=11, on="5", bold=True, cls="red", mono=True)
with A.g(on="6"):
    A.text(10, 70, "long counts whole paise exactly", bold=True, size=10.5)
    A.box(10, 78, 340, 30, "10 + 20 = 30 paise", fill="soft-green", stroke="green", mono=True, size=10.5, rx=4)
    A.text(180, 132, "display: Rs 0.30  ✓ exact", anchor="middle", size=11, bold=True, cls="green")
A.text(180, 166, "Pick the type by the size and kind of value.", anchor="middle", size=10, cls="ink2", on="6")
A.caps([
 "<b>The limit:</b> an <code>int</code> has 32 bits. The first bit is the sign, so the largest value is 2,147,483,647 (about 214 crore).",
 "<b>Overflow:</b> add 1 and the bits roll over to 1000…0, which means the most negative int. No error is shown; the views count silently becomes negative.",
 "<b>Fix:</b> use <code>long</code> (64 bits) for counts that can grow big: views, transaction IDs, timestamps in milliseconds.",
 "<b>Fractions:</b> <code>double</code> stores numbers in binary. 0.1 and 0.2 cannot be stored exactly, only very close values.",
 "<b>Surprise:</b> the tiny errors add up, and Java prints 0.30000000000000004. Fine for distances or sensor readings, risky for money.",
 "<b>Fix for money:</b> count whole paise in a <code>long</code> (or use <code>BigDecimal</code>, later). Integers are exact.",
])
