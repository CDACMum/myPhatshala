from mkanim import Anim
HEADING = "Watch it with an example: a product's average rating"
INTRO = "Three customers rate a phone cover 5, 4 and 5 stars. Watch how integer division loses the fraction, and how one cast fixes it."
A = Anim("int ÷ int vs (double) cast", frames=5, h=222)
A.box(6, 14, 348, 34, None, fill="board", stroke="board")
code = {1: "int sum = 5 + 4 + 5;  int count = 3;", 2: "double avg = sum / count;", 3: "double avg = (double) sum / count;",
        4: "double avg = (double) sum / count;", 5: "Math.round(avg * 10) / 10.0"}
for f, t in code.items(): A.text(14, 36, t, on=str(f), cls="chalk", mono=True, size=10)
A.box(14, 66, 70, 46, "sum", fill="soft-blue", stroke="blue", sub="14", mono=True, bold=True, size=11)
A.box(98, 66, 70, 46, "count", fill="soft-blue", stroke="blue", sub="3", mono=True, bold=True, size=11)
A.text(180, 94, "int ÷ int", on="2", size=10.5, bold=True)
A.box(220, 66, 130, 46, None, fill="soft-acc", stroke="red", on="2")
A.text(285, 86, "14 / 3 = 4", anchor="middle", on="2", mono=True, bold=True, cls="red", size=11)
A.text(285, 102, ".666 is thrown away", anchor="middle", on="2", size=9.5, cls="red")
A.text(180, 94, "cast →", on="3-", size=10.5, bold=True)
A.box(220, 66, 130, 46, None, fill="soft-green", stroke="green", on="3-")
A.text(285, 86, "14.0 / 3", anchor="middle", on="3", mono=True, bold=True, size=11)
A.text(285, 102, "double ÷ int → double", anchor="middle", on="3", size=9.5)
A.text(285, 94, "4.666666666666667", anchor="middle", on="4-", mono=True, bold=True, size=10.5, cls="green")
A.text(180, 148, "avg = 4.0   ✗ wrong rating", anchor="middle", on="2", size=11, mono=True, bold=True, cls="red")
A.text(180, 148, "avg = 4.666666666666667", anchor="middle", on="4", size=11, mono=True, bold=True)
A.box(110, 128, 140, 34, "★ 4.7", fill="soft-acc", stroke="track", on="5", size=15, bold=True)
A.text(180, 188, "Cast before dividing, round only for display.", anchor="middle", on="5", size=10, cls="ink2")
A.caps([
 "<b>Data:</b> the ratings add up to <code>sum = 14</code>, and <code>count = 3</code>. Both are <code>int</code>.",
 "<b>Bug:</b> <code>sum / count</code> divides two ints, so Java does <i>integer division</i> and drops the fraction: 4. Storing it in a double later only makes it 4.0.",
 "<b>Cast:</b> <code>(double) sum</code> widens 14 to 14.0 <i>before</i> dividing. Now one side is double, so the other is widened too.",
 "<b>Exact-ish result:</b> 4.666666666666667. The fraction is kept.",
 "<b>Display:</b> round to one decimal for the screen: ★ 4.7. Shopping and food apps do exactly this for their ratings.",
])
