import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../..'))
from mkanim import Anim, two_view

# ---------------- Part 5: two-view animation ----------------
CODE = ["Integer total = 0;", "Integer price = 250;", "total += price;", "int n = total;", "Integer none = null;", "int bad = none;"]
JAVAC = ["Integer.valueOf(0)", "Integer.valueOf(250)", "valueOf(total.intValue() + price.intValue())",
         "total.intValue()", "(nothing to call: just null)", "none.intValue()   ← on null!"]
S = Anim("see", frames=6, h=250, label="Six lines of code using Integer variables; the last one crashes")
S.box(8, 8, 344, 132, None, fill="board", stroke="board")
for i, line in enumerate(CODE):
    y = 30 + i * 20
    S.box(12, y - 14, 336, 19, None, fill="none", stroke="track", sw=2, on=str(i + 1), rx=4)
    S.text(20, y, line, mono=True, size=10.5, cls="chalk")
S.box(8, 150, 344, 50, None, fill="card2", stroke="line")
S.text(18, 168, "Console", size=9, cls="ink3", bold=True)
S.text(18, 188, "println(total) → 250", on="3-5", mono=True, size=10.5, cls="green", bold=True)
S.text(18, 188, "NullPointerException", on="6", mono=True, size=10.5, cls="red", bold=True)
S.note({1: "Looks like storing a number.", 2: "Looks like storing a number.", 3: "Looks like simple addition.",
        4: "Looks like a plain copy.", 5: "A wrapper variable can be null.", 6: "A line with no dot crashes!"}, y=226, size=10.5)
S.caps(["You assign the number 0 to an <code>Integer</code> variable. No method call in sight.",
        "The same for 250.",
        "<code>total += price</code> reads like adding two numbers.",
        "Copying an Integer into an int looks like an ordinary assignment.",
        "<code>none</code> holds no object at all.",
        "This innocent-looking line throws <code>NullPointerException</code>. The right side shows the hidden call."])
B = Anim("behind", frames=6, h=250, label="The calls javac inserted and the objects they create on the heap")
B.box(8, 8, 344, 30, None, fill="soft-acc", stroke="track")
B.text(16, 28, "javac writes:", size=9.5, bold=True, cls="acc")
for i, t in enumerate(JAVAC):
    B.text(92, 28, t, on=str(i + 1), mono=True, size=9.2, cls="red" if i == 5 else "ink", bold=i == 5)
B.text(56, 56, "Stack", anchor="middle", size=10, bold=True, cls="ink2")
B.text(250, 56, "Heap", anchor="middle", size=10, bold=True, cls="ink2")
B.box(8, 62, 98, 140, None, fill="card", stroke="line")
B.box(128, 62, 224, 140, None, fill="card", stroke="line")
for i, (n, on, v) in enumerate([("total", "1-", "→"), ("price", "2-", "→"), ("n", "4-", "250"), ("none", "5-", "null")]):
    y = 70 + i * 32
    B.box(14, y, 86, 24, None, fill="soft-blue", stroke="blue", on=on, rx=5)
    B.text(20, y + 16, n, on=on, mono=True, size=10, bold=True)
    B.text(94, y + 16, v, on=on, mono=True, size=10, anchor="end", cls="blue" if v == "→" else ("red" if v == "null" else "ink"))
B.box(140, 70, 92, 32, "Integer 0", sub="cached", fill="soft-green", stroke="green", on="1-", size=9.5, bold=True)
B.box(246, 70, 98, 32, "Integer 250", sub="#1 price", fill="soft-acc", stroke="track", on="2-", size=9.5, bold=True)
B.box(194, 118, 104, 32, "Integer 250", sub="#2 new result", fill="soft-acc", stroke="track", on="3-", size=9.5, bold=True)
B.arrow(100, 82, 140, 84, on="1-2", color="blue")
B.arrow(100, 82, 194, 130, on="3-", color="blue", bend=-10)
B.arrow(100, 114, 246, 98, on="2-", color="blue", bend=12)
B.box(150, 164, 190, 30, "intValue() on null ✗", fill="soft-acc", stroke="red", on="6", size=10, bold=True, cls="red")
B.note({1: "0 is in the cache: no new object.", 2: "250 is outside the cache: new object #1.",
        3: "Unbox both, add as ints, box the result: object #2.", 4: "Unboxing copies 250 into a plain int.",
        5: "none points nowhere.", 6: "The hidden intValue() has no object to run on."}, y=226, size=10)
B.caps(["Autoboxing: javac replaces <code>0</code> with <code>Integer.valueOf(0)</code>, which returns the cached object for 0.",
        "<code>Integer.valueOf(250)</code> creates a new object, because 250 is outside -128..127.",
        "<code>+=</code> needs ints: javac unboxes both with <code>intValue()</code>, adds 0 + 250 as ints, then boxes 250 into a <b>new</b> object. <code>total</code> moves to it; the cached 0 is untouched.",
        "Unboxing: <code>total.intValue()</code> copies the value 250 into the primitive <code>n</code>, stored right in the frame.",
        "Assigning null needs no conversion: <code>none</code> simply holds no reference.",
        "<code>int bad = none;</code> becomes <code>none.intValue()</code>. Calling a method on null throws <code>NullPointerException</code>."])
ANIM = two_view("Autoboxing and unboxing, made visible", S, B)
BLOCKS = {'ANIM': ANIM}

# ---------------- Part 6: animated example ----------------
ANIM2_HEADING = "Watch it with an example: an exam result portal"
ANIM2_INTRO = "Marks come from a database where an absent student's mark is NULL. Watch the averaging code survive one absent student, then see the version that crashes."
A = Anim("Averaging marks with an absent student", frames=5, h=226, label="A list of Integer marks with a null; the safe loop skips it, the unsafe one crashes on unboxing")
for k, (v, on_cls) in enumerate([("78", "ink"), ("91", "ink"), ("null", "red"), ("64", "ink")]):
    x = 14 + k * 64
    A.box(x, 14, 56, 40, v, fill="soft-acc" if v != "null" else "card2", stroke="track" if v != "null" else "red", size=11, bold=True, mono=True, cls=on_cls)
    A.text(x + 28, 66, ["Riya", "Kabir", "Meera", "Arjun"][k], anchor="middle", size=9.5, cls="ink2")
A.box(272, 14, 80, 40, "List&lt;Integer&gt;", fill="none", stroke="line", size=9, mono=True, cls="ink3")
A.box(14 + 0 * 64, 14, 56, 40, None, fill="none", stroke="blue", sw=3, on="2")
A.box(14 + 2 * 64, 14, 56, 40, None, fill="none", stroke="blue", sw=3, on="3")
A.box(14 + 2 * 64, 14, 56, 40, None, fill="none", stroke="red", sw=3, on="5")
A.box(10, 84, 342, 88, None, fill="board", stroke="board")
A.lines(20, 104, ["for (Integer m : marks)", "  if (m != null) { sum += m; count++; }"], on="1-3", mono=True, size=10, cls="chalk")
A.text(20, 150, "sum += 78   (unbox 78)", on="2", mono=True, size=10, cls="str")
A.text(20, 150, "null: skipped, not counted", on="3", mono=True, size=10, cls="str")
A.lines(20, 104, ["sum = 233, count = 3", "average = 233 / 3 = 77.67"], on="4", mono=True, size=10.5, cls="chalk")
A.lines(20, 104, ["for (int m : marks)   // unboxes every element", "  sum += m;"], on="5", mono=True, size=10, cls="chalk")
A.text(20, 156, "NullPointerException at Meera", on="5", mono=True, size=10, cls="red", bold=True)
A.note({1: "Meera was absent: her mark is null, not 0.", 2: "A real mark is unboxed and added.", 3: "The null is skipped before any unboxing.",
        4: "Average of the 3 students who wrote the exam.", 5: "Declaring the loop variable as int unboxes null."}, y=200, size=10.5)
A.caps(["Marks arrive as <code>Integer</code> objects. Meera was absent, so the database gave <code>NULL</code>, which becomes <code>null</code> in Java.",
        "For Riya's 78, the check passes and <code>sum += m</code> unboxes the Integer to add it.",
        "For Meera, <code>m != null</code> is false, so nothing is unboxed and she isn't counted.",
        "Average = 233 / 3 ≈ 77.67. Using 0 for Meera would have wrongly pulled it down to about 58.",
        "The tempting shortcut <code>for (int m : marks)</code> unboxes each element automatically, and crashes on Meera's null. (Simplified: real portals also record why a mark is missing.)"])
ANIM2 = A

# ---------------- Part 8: tracer ----------------
TRACE = dict(code='''public class Main {
    public static void main(String[] args) {
        int[] prices = {120, 250, 80};
        Integer total = 0;
        for (int p : prices) {
            total += p;
        }
        int asInt = total;
        System.out.println("Bill: " + asInt);
    }
}
''', notes={
 3: "Primitives :: A plain int array: no wrapper objects yet.",
 4: "Box :: = javac wrote <code>Integer.valueOf(0)</code>. 0 is in the cache, so <code>total</code> = → #3, an object the JDK created at start-up. (The trace numbers objects the first time our code uses them.)",
 (6, 1): "Unbox, add, box :: = 0 + 120 = 120, boxed again with <code>valueOf</code>. 120 is cached too, so <code>total</code> now points to the ready-made Integer 120 (#4). Nothing new was allocated.",
 (6, 2): "Unbox, add, box :: 120 + 250 = 370. Outside the cache: a <b>new</b> Integer object.",
 (6, 3): "Unbox, add, box :: 370 + 80 = 450: <b>another</b> new object. The 370 object is now garbage.",
 8: "Unbox :: <code>total.intValue()</code> copies 450 into a primitive.",
 9: "Print :: "})

# ---------------- Worked examples ----------------
WORKED_INTRO = "Three tasks where autoboxing helps, and where one careless unboxing would crash the program."
EXAMPLES = [
dict(tag="Elections · counting", title="Count votes in a map",
 problem="<p>A class election records each vote as a name. Count the votes per candidate in a <code>HashMap&lt;String, Integer&gt;</code> without crashing on a candidate's first vote.</p>",
 inp='"Riya", "Kabir", "Riya"',
 approach=["A helper <code>vote(map, name)</code> reads the current count with <code>getOrDefault(name, 0)</code>, so a new name gives 0, not null.",
           "Store <code>now + 1</code>: unboxing for the addition, boxing for <code>put</code>.",
           "Print the map."],
 code='''import java.util.HashMap;

public class Main {
    static void vote(HashMap<String, Integer> votes, String name) {
        int now = votes.getOrDefault(name, 0);
        votes.put(name, now + 1);
    }

    public static void main(String[] args) {
        HashMap<String, Integer> votes = new HashMap<>();
        vote(votes, "Riya");
        vote(votes, "Kabir");
        vote(votes, "Riya");
        System.out.println(votes);
    }
}
''', notes={5: "Unbox :: <code>getOrDefault</code> returns an Integer (never null here); javac unboxes it into <code>now</code>.",
            6: "Box :: <code>now + 1</code> is an int; javac boxes it for <code>put</code>.", 14: "Print :: "},
 tryit="Press <b>Run</b>. Then replace <code>getOrDefault(name, 0)</code> with <code>get(name)</code> and see the crash on the first vote."),
dict(tag="EdTech · reports", title="Class average with absent students",
 problem="<p>Marks are in a <code>List&lt;Integer&gt;</code>; <code>null</code> means absent. Compute the average of the students who were present.</p>",
 inp="[78, 91, null, 64]",
 approach=["A helper <code>average(List&lt;Integer&gt; marks)</code> loops with an <code>Integer</code> loop variable, so nothing is unboxed automatically.",
           "Skip nulls; unbox the rest by adding them to an int sum.",
           "Return the average as a double and print it with two decimals."],
 code='''import java.util.Arrays;
import java.util.List;

public class Main {
    static double average(List<Integer> marks) {
        int sum = 0, count = 0;
        for (Integer m : marks) {
            if (m != null) {
                sum += m;
                count++;
            }
        }
        return (double) sum / count;
    }

    public static void main(String[] args) {
        List<Integer> marks = Arrays.asList(78, 91, null, 64);
        double avg = average(marks);
        System.out.printf("Average: %.2f%n", avg);
    }
}
''', notes={17: "Box :: <code>Arrays.asList(78, 91, null, 64)</code>: each number is autoboxed; null stays null.",
            8: "Check :: Test before unboxing.", 9: "Unbox :: <code>sum += m</code> calls <code>m.intValue()</code>.",
            13: "Return :: "},
 tryit="Press <b>Run</b>. Then change the loop to <code>for (int m : marks)</code> and read the error."),
dict(tag="E-commerce · bug fix", title="Remove a product ID, not a position",
 problem="<p>A wishlist stores product IDs <code>[7, 2, 9]</code>. The customer removes product <b>2</b>. The code <code>ids.remove(productId)</code> with an <code>int</code> removed the wrong item. Fix it.</p>",
 inp="ids = [7, 2, 9], remove product 2",
 approach=["<code>remove(int)</code> removes by <b>index</b>; <code>remove(Object)</code> removes by <b>value</b>.",
           "Passing an <code>int</code> makes javac choose <code>remove(int)</code> (no boxing needed).",
           "Box the ID explicitly with <code>Integer.valueOf</code> to call <code>remove(Object)</code>."],
 code='''import java.util.ArrayList;
import java.util.List;

public class Main {
    public static void main(String[] args) {
        int productId = 2;
        List<Integer> wrong = new ArrayList<>(List.of(7, 2, 9));
        wrong.remove(productId);
        System.out.println("By index: " + wrong);

        List<Integer> right = new ArrayList<>(List.of(7, 2, 9));
        right.remove(Integer.valueOf(productId));
        System.out.println("By value: " + right);
    }
}
''', notes={8: "Wrong call :: <code>remove(int index)</code>: removes the element at position 2, which is 9.",
            12: "Right call :: <code>remove(Object)</code>: finds the value 2 with <code>equals</code> and removes it."},
 tryit="Press <b>Run</b>. Then try <code>right.remove((Integer) productId)</code>: a cast also forces boxing."),
]

# ---------------- Practice problems ----------------
PRACTICE_INTRO = "Find the hidden calls, prevent null crashes and pick the right overload. The last three are business tasks."
PROBLEMS = [
dict(level="easy", title="Box and unbox without calling methods", stmt="<p>Store 45 in an <code>Integer</code>, add 5 to it using an <code>int</code>, and print both, writing no <code>valueOf</code> or <code>intValue</code> yourself.</p>", inp="45",
 code='''public class Main {
    public static void main(String[] args) {
        Integer boxed = 45;
        int plain = boxed + 5;
        System.out.println(boxed + " " + plain);
    }
}''', explain="<p><b>How it works:</b> line 3 is autoboxed to <code>Integer.valueOf(45)</code>; in line 4 <code>boxed</code> is unboxed with <code>intValue()</code> before adding.</p>"),
dict(level="easy", title="Safe lookup with getOrDefault", stmt="<p>A price map has only <code>\"tea\" → 15</code>. Print the price of <code>\"coffee\"</code> as 0 without crashing.</p>", inp='"coffee"',
 code='''import java.util.HashMap;

public class Main {
    public static void main(String[] args) {
        HashMap<String, Integer> price = new HashMap<>();
        price.put("tea", 15);
        int coffee = price.getOrDefault("coffee", 0);
        System.out.println("coffee: " + coffee);
    }
}''', explain="<p><b>How it works:</b> <code>get</code> would return null and unboxing it into <code>int</code> would throw. <code>getOrDefault</code> returns 0 (boxed) instead.</p>"),
dict(level="easy", title="Fix the Long literal", stmt="<p><code>Long views = 1200;</code> doesn't compile. Fix it and print views doubled.</p>", inp="1200",
 code='''public class Main {
    public static void main(String[] args) {
        Long views = 1200L;
        System.out.println(views * 2);
    }
}''', explain="<p><b>How it works:</b> 1200 is an int, which can only be boxed to Integer. The <code>L</code> suffix makes it a long, which boxes to Long.</p>"),
dict(level="medium", title="Compare two boxed scores correctly", stmt="<p>Two players scored 500 each, stored as <code>Integer</code>. Print whether they tied, correctly.</p>", inp="500, 500",
 code='''import java.util.Objects;

public class Main {
    public static void main(String[] args) {
        Integer p1 = 500, p2 = 500;
        System.out.println("== says     : " + (p1 == p2));
        System.out.println("equals says : " + Objects.equals(p1, p2));
    }
}''', explain="<p><b>How it works:</b> autoboxing 500 creates two objects, so <code>==</code> is false. <code>Objects.equals</code> compares values and is also safe if either is null.</p>"),
dict(level="medium", title="Which overload runs?", stmt="<p>Predict, then confirm, which method each call picks: <code>show(int)</code> doesn't exist, but <code>show(long)</code>, <code>show(Integer)</code> and <code>show(Object)</code> do.</p>", inp="show(5), show(Integer.valueOf(5)), show(\"x\")",
 code='''public class Main {
    static void show(long x)    { System.out.println("long"); }
    static void show(Integer x) { System.out.println("Integer"); }
    static void show(Object x)  { System.out.println("Object"); }

    public static void main(String[] args) {
        show(5);
        show(Integer.valueOf(5));
        show("x");
    }
}''', explain="<p><b>How it works:</b> for <code>show(5)</code>, javac first looks for a match without boxing: widening int → long works, so <code>show(long)</code> wins. An Integer argument matches <code>show(Integer)</code> exactly. A String only fits <code>Object</code>.</p>"),
dict(level="business", title="Shopping cart quantities", stmt="<p>Add items to a cart map: <code>pen</code>, <code>pen</code>, <code>book</code>, <code>pen</code>. Use <code>merge</code> so first-time items start at 1, then print the cart.</p>", inp='pen, pen, book, pen',
 code='''import java.util.LinkedHashMap;
import java.util.Map;

public class Main {
    public static void main(String[] args) {
        Map<String, Integer> cart = new LinkedHashMap<>();
        String[] added = {"pen", "pen", "book", "pen"};
        for (String item : added) {
            cart.merge(item, 1, Integer::sum);
        }
        System.out.println(cart);
    }
}''', explain="<p><b>How it works:</b> <code>merge</code> puts 1 for a new key, otherwise combines the old and new values with <code>Integer::sum</code> (a method reference, Lesson 14.1). No null is ever unboxed. (<code>LinkedHashMap</code> keeps insertion order; Lesson 11.6.)</p>"),
dict(level="business", title="Optional discount from a nullable field", stmt="<p>Orders have an <code>Integer discountPct</code> that may be null. Compute the final price for ₹1000 with 10% and with no discount.</p>", inp="1000 with 10, 1000 with null",
 code='''public class Main {
    static int finalPrice(int price, Integer discountPct) {
        int pct = (discountPct == null) ? 0 : discountPct;
        return price - price * pct / 100;
    }

    public static void main(String[] args) {
        System.out.println(finalPrice(1000, 10));
        System.out.println(finalPrice(1000, null));
    }
}''', explain="<p><b>How it works:</b> the null check happens <i>before</i> unboxing, inside one helper, so no caller can forget it. The literal 10 is autoboxed when passed.</p>"),
dict(level="business", title="Fast sum of daily sales", stmt="<p>Sum one million sales of ₹1 each, first with a <code>Long</code> total, then with a <code>long</code>. Print both totals (the timing is up to you to measure).</p>", inp="1,000,000 × ₹1",
 code='''public class Main {
    public static void main(String[] args) {
        Long boxedTotal = 0L;
        long plainTotal = 0L;
        for (int i = 0; i < 1_000_000; i++) {
            boxedTotal += 1;   // unbox, add, box a new Long
            plainTotal += 1;   // just add
        }
        System.out.println(boxedTotal + " " + plainTotal);
    }
}''', explain="<p><b>How it works:</b> both totals are correct, but the <code>Long</code> version creates a new object on almost every iteration. Wrap each loop with <code>System.nanoTime()</code> to see the difference on your machine.</p>"),
]
