from mkanim import Anim
HEADING = "Watch it with an example: building a receipt line by line"
INTRO = "A shop app adds 3 items to a receipt. Compare <code>String +=</code> (a new object every time) with one <code>StringBuilder</code> that grows in place."
A = Anim("String += vs StringBuilder", frames=6, h=226, label="string concatenation objects versus a stringbuilder buffer")
A.text(10, 22, "String r = \"\";  r += item;", mono=True, size=10, bold=True, on="1-3")
A.text(10, 22, "StringBuilder sb = new StringBuilder();  sb.append(item);", mono=True, size=9.4, bold=True, on="4-6")
items = ["Tea 10;", "Tea 10;Vada 15;", "Tea 10;Vada 15;Chai 10;"]
for i, t in enumerate(items):
    y = 36 + i * 34
    A.box(10, y, 240, 28, f"#{i+1} \"{t}\"", on=f"{i+1}-3", fill="soft-blue", stroke="blue", mono=True, size=9.5)
    A.box(10, y, 240, 28, None, on=f"{i+2}-3", fill="card", stroke="line")
    A.text(20, y + 18, f"#{i+1} garbage", on=f"{i+2}-3", mono=True, size=9.5, cls="ink3")
A.text(262, 54, "r → #1", on="1", mono=True, size=10, bold=True, cls="acc")
A.text(262, 88, "r → #2", on="2", mono=True, size=10, bold=True, cls="acc")
A.text(262, 122, "r → #3", on="3", mono=True, size=10, bold=True, cls="acc")
A.text(10, 162, "3 appends = 3 new String objects (and copies)", on="3", size=10, cls="red", bold=True)
A.box(10, 40, 320, 34, None, on="4-6", fill="card2", stroke="green")
fills = {4: 7, 5: 15, 6: 22}
for f, n in fills.items():
    A.box(12, 42, n * 13.5, 30, None, on=str(f), fill="soft-green", stroke="green", rx=6)
    A.text(18, 62, items[f - 4], on=str(f), mono=True, size=9.5)
A.text(10, 92, "23 chars &gt; 16: buffer replaced once by a 34-slot one", on="6", size=9.8, cls="ink2")
A.text(10, 92, "15 of 16 slots used: still fits", on="5", size=9.8, cls="ink2")
A.text(10, 112, "sb → #1 (the same object every time)", on="4-6", mono=True, size=10, bold=True, cls="green")
A.box(10, 130, 340, 40, "sb.toString() → one final String", on="6", fill="soft-acc", stroke="track", size=10.5, bold=True)
A.text(10, 196, "In a loop of 10,000 items this is the difference between", on="6", size=9.8, cls="ink2")
A.text(10, 212, "thousands of copies and one growing buffer.", on="6", size=9.8, cls="ink2")
A.caps([
 "<b>String:</b> <code>r += \"Tea 10;\"</code> creates String #1 and points <code>r</code> to it.",
 "<b>Second item:</b> Strings can't change, so Java builds a brand-new #2 with the old text copied plus the new item. #1 becomes garbage.",
 "<b>Third item:</b> again a full copy into #3. With n items you create n objects and copy the text again and again.",
 "<b>StringBuilder:</b> one object with an internal char buffer (default capacity 16). <code>append</code> writes into the free space.",
 "<b>Second append:</b> 15 characters, still inside the 16-slot buffer. No new object, no copy.",
 "<b>Growing, then finish:</b> the third item needs 23 slots, so the buffer is replaced once by a bigger one (34 slots; it roughly doubles). <code>toString()</code> then makes the final String once. Use StringBuilder for loops that build text: reports, CSV exports, SMS and email bodies. (StringBuffer is the older, synchronized version.)",
])
