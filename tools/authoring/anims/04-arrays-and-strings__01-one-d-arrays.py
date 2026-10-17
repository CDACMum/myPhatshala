from mkanim import Anim
HEADING = "Watch it with an example: a week of step counts"
INTRO = "A fitness app stores 7 days of steps in one array. Watch a loop find the best day, and see what happens when the index goes one step too far."
A = Anim("int[] steps = new int[7]", frames=6, h=222, label="array of 7 step counts and finding the max")
A.box(6, 14, 348, 34, None, fill="board", stroke="board")
code = {1: "int[] steps = {4200, 8100, 6500, 9800, 3000, 7200, 5600};", 2: "int best = 0;  // index of best day", 3: "for (i = 1; i < 7; i++) if (steps[i] > steps[best]) best = i;",
        4: "for (i = 1; i < 7; i++) if (steps[i] > steps[best]) best = i;", 5: "print(days[best] + \": \" + steps[best]);", 6: "steps[7] = 100;   // 8th day?"}
for f, t in code.items(): A.text(12, 36, t.replace('<', '&lt;').replace('>', '&gt;'), on=str(f), cls="chalk", mono=True, size=8.6)
vals = [4200, 8100, 6500, 9800, 3000, 7200, 5600]; days = "Mon Tue Wed Thu Fri Sat Sun".split()
for i, v in enumerate(vals):
    x = 8 + i * 49
    h = v / 9800 * 70
    A.box(x + 6, 142 - h, 34, h, None, fill="soft-blue", stroke="blue", rx=3)
    A.text(x + 23, 136 - h, str(v), anchor="middle", size=8.5, mono=True)
    A.box(x, 148, 46, 22, f"[{i}]", fill="card2", stroke="line", mono=True, size=9.5, rx=4)
    A.text(x + 23, 182, days[i], anchor="middle", size=9, cls="ink2")
A.box(8 + 3 * 49 + 6, 72, 34, 70, None, fill="soft-green", stroke="green", rx=3, on="4-5")
A.token(8, 186, 46, 20, "best", pos={2: "0,0", 3: "49,0", 4: "147,0"}, on="2-5", mono=True, size=9)
A.box(8 + 6 * 49, 148, 46, 22, None, fill="none", stroke="red", sw=3, on="6", rx=4)
A.text(180, 212, "ArrayIndexOutOfBoundsException: Index 7 out of bounds for length 7", anchor="middle", on="6", size=8.6, cls="red", bold=True, mono=True)
A.text(180, 212, "Thu: 9800 steps ★", anchor="middle", on="5", size=11, cls="green", bold=True)
A.caps([
 "<b>One variable, seven values:</b> the array holds 7 ints side by side, numbered by index <code>[0]</code> to <code>[6]</code>. Index 0 is Monday.",
 "<b>Start:</b> assume the best day is index 0 (Monday, 4200).",
 "<b>Loop:</b> i = 1: 8100 &gt; 4200, so best = 1. i = 2: 6500 is not bigger, best stays 1.",
 "<b>i = 3:</b> 9800 &gt; 8100 → best = 3. The remaining days are all smaller, so best stays 3.",
 "<b>Answer:</b> Thursday, 9800 steps. One loop over the array, whatever its length (<code>steps.length</code>).",
 "<b>Off by one:</b> the last index of a 7-element array is 6. <code>steps[7]</code> throws <code>ArrayIndexOutOfBoundsException</code>; Java never lets you write past the end.",
])
