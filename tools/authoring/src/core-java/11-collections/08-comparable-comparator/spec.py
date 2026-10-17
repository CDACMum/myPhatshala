import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../..'))
from mkanim import Anim, two_view

def esc(t): return t.replace('<', '&lt;').replace('>', '&gt;')

# ---------------- Part 5: two-view animation ----------------
S = Anim("see", frames=6, h=250, label="Sorting three students for the merit list: marks high to low, ties by roll number")
S.box(8, 8, 344, 46, None, fill="board", stroke="board")
S.text(16, 26, "merit = comparingInt(marks).reversed()", mono=True, size=9.6, cls="chalk")
S.text(16, 44, "            .thenComparingInt(roll);   list.sort(merit);", mono=True, size=9.6, cls="chalk")
cards = {"Om": "21 · 92", "Riya": "07 · 92", "Kabir": "12 · 78"}
pos = {"Om": [0, 0, 0, 1, 1, 1], "Riya": [1, 1, 1, 0, 0, 0], "Kabir": [2, 2, 2, 2, 2, 2]}
for name, sub in cards.items():
    p = {str(f + 1): f"{(pos[name][f] - pos[name][0]) * 116},0" for f in range(6)}
    S.box(8 + pos[name][0] * 116, 74, 108, 50, name, sub=sub, fill="soft-acc", stroke="track", size=11, bold=True, pos=p)
S.text(16, 146, "roll · marks", size=9, cls="ink3")
S.box(8, 160, 344, 40, None, fill="card2", stroke="line")
S.text(18, 185, "[Om, Riya, Kabir]  (unsorted)", on="1-3", mono=True, size=10.5)
S.text(18, 185, "[Riya, Om, Kabir]", on="4-5", mono=True, size=10.5)
S.text(18, 185, "[Riya, Om, Kabir]  ✓ merit order", on="6", mono=True, size=10.5, bold=True, cls="green")
S.note({1: "Three students to rank.", 2: "sort is thinking…", 3: "…still thinking…", 4: "Two cards swap.", 5: "Kabir stays last.", 6: "Done."}, y=226, size=10.5)
S.caps(["The list starts in arrival order. We ask for the merit order.", "Nothing visible happens yet.", "Still nothing visible.",
        "Riya and Om change places.", "Kabir stays where he is.", "The merit list: Riya (92, roll 7), Om (92, roll 21), Kabir (78)."])
B = Anim("behind", frames=6, h=250, label="The calls TimSort makes to the comparator and the results it uses")
B.text(8, 18, "TimSort's questions to your comparator", size=10, bold=True, cls="ink2")
calls = [("compare(Riya, Om)", "marks 92 = 92 → roll 7 vs 21", "−1: Riya before Om", "2-"),
         ("compare(Kabir, Riya)", "marks 78 vs 92 (reversed)", "+1: Kabir after Riya", "3-"),
         ("compare(Kabir, Om)", "marks 78 vs 92 (reversed)", "+1: Kabir after Om", "5-")]
for k, (c, why, res, on) in enumerate(calls):
    y = 28 + k * 50
    B.box(8, y, 344, 42, None, fill="card", stroke="line", on=on)
    B.text(16, y + 17, c, on=on, mono=True, size=10, bold=True)
    B.text(16, y + 34, why, on=on, size=9.2, cls="ink2")
    B.text(344, y + 26, res, on=on, size=9.6, bold=True, anchor="end", cls="green")
hl = {2: 28, 3: 78, 5: 128}
for f, y in hl.items():
    B.box(8, y, 344, 42, None, fill="none", stroke="track", sw=3, on=str(f))
B.box(8, 182, 344, 22, None, fill="soft-acc", stroke="track", on="4")
B.text(180, 197, "run [Om, Riya] was descending → reverse it: [Riya, Om]", on="4", anchor="middle", size=9.2, bold=True)
B.text(180, 197, "your code only answered −1 / 0 / +1; TimSort moved the elements", on="6", anchor="middle", size=9.2, bold=True, cls="acc")
B.note({1: "sort copies the list into an array.", 2: "First question: Riya vs Om.", 3: "Does the first run continue? Kabir vs Riya.",
        4: "TimSort reverses the descending run.", 5: "Insert Kabir: compare with Om.", 6: "3 comparisons for 3 elements."}, y=228, size=10)
B.caps(["<code>list.sort(merit)</code> copies the list into an array and starts TimSort. For tiny arrays it looks for an ordered run and then inserts the rest.",
        "It asks <code>merit.compare(Riya, Om)</code>. Marks are equal (92), so the tie-breaker compares rolls 7 and 21: −1. In merit order Riya comes first, so the first two elements form a <i>descending</i> run.",
        "Does the run continue? <code>compare(Kabir, Riya)</code>: 78 vs 92 with <code>reversed()</code> gives +1, so no. The run is [Om, Riya].",
        "A descending run is reversed in place: [Riya, Om, Kabir].",
        "Kabir is inserted into the sorted part using binary search: <code>compare(Kabir, Om)</code> = +1, so he goes after Om, at the end.",
        "These three calls were recorded from a real JVM. Your comparator never moves anything; it only answers with a sign."])
ANIM = two_view("How sort uses your comparator", S, B)
BLOCKS = {'ANIM': ANIM}

# ---------------- Part 6: animated example ----------------
ANIM2_HEADING = "Watch it with an example: “Sort by” on a shopping app"
ANIM2_INTRO = "The same four phones, re-sorted each time the shopper taps a different option. Each option is just a different Comparator."
A = Anim("One list, three comparators", frames=4, h=244, label="Phones re-sorted by price ascending, rating descending, and price descending with rating as tie-breaker")
phones = [("A", 14999, 4.2), ("B", 9999, 4.5), ("C", 14999, 4.6), ("D", 21999, 4.4)]
orders = {1: ["A", "B", "C", "D"], 2: ["B", "A", "C", "D"], 3: ["C", "B", "D", "A"], 4: ["D", "C", "A", "B"]}
for name, price, rating in phones:
    p = {str(f): f"0,{(orders[f].index(name) - orders[1].index(name)) * 36}" for f in orders}
    A.box(10, 40 + orders[1].index(name) * 36, 342, 30, f"Phone {name}  ₹{price:,}  ★{rating}", fill="soft-blue", stroke="blue", size=10, mono=True, pos=p)
labels = {1: "as loaded", 2: "Price: low to high", 3: "Rating: high to low", 4: "Price: high to low, then rating"}
for f, t in labels.items():
    A.text(10, 28, "Sort by: " + t, on=str(f), size=10.5, bold=True, cls="acc")
code = {2: "comparingInt(Phone::price)", 3: "comparingDouble(Phone::rating)", 4: "comparingInt(Phone::price)"}
code2 = {3: "  .reversed()", 4: "  .reversed().thenComparing(…)"}
for f, t in code.items():
    A.text(10, 194, t, on=str(f), mono=True, size=9.5, cls="acc")
for f, t in code2.items():
    A.text(10, 208, t, on=str(f), mono=True, size=9.5, cls="acc")
A.note({1: "Results arrive unsorted.", 2: "Cheapest first; A and C tie at ₹14,999.", 3: "Best rated first.", 4: "Costliest first; the tie is broken by rating."}, y=230, size=10.5)
A.caps(["The search returns four phones in no particular order.",
        "“Price: low to high” uses <code>comparingInt(Phone::price)</code>. A and C cost the same; the stable sort keeps A before C, as they were.",
        "“Rating” sorts by stars, highest first, using <code>reversed()</code>.",
        "“Price: high to low” with a rating tie-breaker: C (★4.6) now comes before A (★4.2). (Simplified: real apps sort in the database and add a unique ID as the last tie-breaker.)"])
ANIM2 = A

# ---------------- Part 8: tracer ----------------
TRACE = dict(code='''import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

class Student implements Comparable<Student> {
    int roll;
    String name;

    Student(int roll, String name) {
        this.roll = roll;
        this.name = name;
    }

    public int compareTo(Student other) {
        int result = Integer.compare(this.roll, other.roll);
        return result;
    }
}

public class Main {
    public static void main(String[] args) {
        List<Student> list = new ArrayList<>();
        list.add(new Student(21, "Om"));
        list.add(new Student(7, "Riya"));
        list.add(new Student(12, "Kabir"));
        Collections.sort(list);
        System.out.println(list.get(0).name + " " + list.get(1).name + " " + list.get(2).name);
    }
}
''', notes={
 (26, 1): "sort :: = <code>Collections.sort(list)</code> starts. You never call <code>compareTo</code>; the sorting code will. Watch frames named <code>Student.compareTo</code> appear.",
 (15, 1): "Compare :: The sort's first question: Riya (this, roll 7) vs Om (other, roll 21).",
 (16, 1): "Answer :: = Returns −1: Riya comes before Om. The sort immediately asks its next question, so a new compareTo call replaces this one.",
 (15, 2): "Compare :: Kabir (12) vs Riya (7): +1, Kabir comes after Riya.",
 (16, 2): "Reverse :: = The first two elements formed a descending run, so TimSort reversed them: the heap list is now [Riya, Om, Kabir]. Next call: <code>other</code> = Om.",
 (15, 3): "Compare :: Binary insertion of Kabir: Kabir (12) vs Om (21) → −1, Kabir belongs before Om.",
 (16, 3): "Next :: = Next call: <code>other</code> = Riya.",
 (15, 4): "Compare :: Kabir (12) vs Riya (7) → +1, after Riya.",
 (16, 4): "Place :: = Last answer. The sort moves Kabir between Riya and Om: the heap list is [Riya, Kabir, Om].",
 27: "Print :: The list is now in natural order: by roll number."})

# ---------------- Worked examples ----------------
WORKED_INTRO = "Three sorting problems from real apps, using Comparable, a custom Comparator, and a comparator inside a PriorityQueue."
EXAMPLES = [
dict(tag="Railways · Comparable", title="Trains in departure order",
 problem="<p>A station display lists trains by departure time (HHMM as an int). Give <code>Train</code> a natural order by departure and sort three trains.</p>",
 inp="12123 at 1715, 11007 at 0640, 12127 at 1015",
 approach=["<code>Train implements Comparable&lt;Train&gt;</code>; <code>compareTo</code> uses <code>Integer.compare</code> on departure.",
           "<code>Collections.sort(list)</code> needs no extra argument.",
           "Print the board."],
 code='''import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

class Train implements Comparable<Train> {
    String no;
    int departs;

    Train(String no, int departs) {
        this.no = no;
        this.departs = departs;
    }

    public int compareTo(Train other) {
        return Integer.compare(departs, other.departs);
    }
}

public class Main {
    public static void main(String[] args) {
        List<Train> board = new ArrayList<>();
        board.add(new Train("12123", 1715));
        board.add(new Train("11007", 640));
        board.add(new Train("12127", 1015));
        Collections.sort(board);
        for (Train t : board) {
            System.out.printf("%04d %s%n", t.departs, t.no);
        }
    }
}
''', tryit="Press <b>Run</b>. Then sort latest first with <code>board.sort(Collections.reverseOrder());</code>."),
dict(tag="Sales · Comparator", title="Leaderboard: revenue high to low, then name",
 problem="<p>Sales reps: Riya ₹80k, Om ₹95k, Kabir ₹80k. Sort by revenue (highest first); equal revenue by name. Write the comparator by hand as a class.</p>",
 inp="Riya 80, Om 95, Kabir 80",
 approach=["A class <code>ByRevenue implements Comparator&lt;Rep&gt;</code>.",
           "<code>compare</code>: compare revenues in reverse (<code>Integer.compare(b, a)</code>); if 0, compare names.",
           "<code>list.sort(new ByRevenue())</code>."],
 code='''import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;

class Rep {
    String name;
    int revenueK;

    Rep(String name, int revenueK) {
        this.name = name;
        this.revenueK = revenueK;
    }
}

class ByRevenue implements Comparator<Rep> {
    public int compare(Rep a, Rep b) {
        int byRevenue = Integer.compare(b.revenueK, a.revenueK);
        if (byRevenue != 0) {
            return byRevenue;
        }
        return a.name.compareTo(b.name);
    }
}

public class Main {
    public static void main(String[] args) {
        List<Rep> reps = new ArrayList<>();
        reps.add(new Rep("Riya", 80));
        reps.add(new Rep("Om", 95));
        reps.add(new Rep("Kabir", 80));
        reps.sort(new ByRevenue());
        for (Rep r : reps) {
            System.out.println(r.name + " ₹" + r.revenueK + "k");
        }
    }
}
''', tryit="Press <b>Run</b>. Then replace the class with <code>Comparator.comparingInt((Rep r) -&gt; r.revenueK).reversed().thenComparing(r -&gt; r.name)</code>."),
dict(tag="Support · PriorityQueue", title="Serve the most urgent ticket first",
 problem="<p>Tickets have a severity (1 = critical) and an arrival number. Serve by severity, and for equal severity, by earlier arrival.</p>",
 inp="(#1, sev 3), (#2, sev 1), (#3, sev 3), (#4, sev 1)",
 approach=["A <code>PriorityQueue&lt;int[]&gt;</code> with a comparator: severity first, then arrival.",
           "Offer all tickets.",
           "Poll until empty: always the most urgent, oldest first."],
 code='''import java.util.PriorityQueue;

public class Main {
    public static void main(String[] args) {
        PriorityQueue<int[]> q = new PriorityQueue<>((a, b) -> {
            int bySeverity = Integer.compare(a[1], b[1]);
            return bySeverity != 0 ? bySeverity : Integer.compare(a[0], b[0]);
        });
        q.offer(new int[]{1, 3});
        q.offer(new int[]{2, 1});
        q.offer(new int[]{3, 3});
        q.offer(new int[]{4, 1});
        StringBuilder order = new StringBuilder();
        while (!q.isEmpty()) {
            order.append("#").append(q.poll()[0]).append(" ");
        }
        System.out.println(order.toString().trim());
    }
}
''', tryit="Press <b>Run</b>. Then remove the tie-breaker: is the order of #2 and #4 still guaranteed?"),
]

# ---------------- Practice problems ----------------
PRACTICE_INTRO = "Write natural orders and comparators, chain tie-breakers and avoid overflow. The last three are business tasks."
PROBLEMS = [
dict(level="easy", title="Sort numbers descending", stmt="<p>Sort <code>[5, 1, 9, 3]</code> from highest to lowest.</p>", inp="[5, 1, 9, 3]",
 code='''import java.util.*;

public class Main {
    public static void main(String[] args) {
        List<Integer> l = new ArrayList<>(List.of(5, 1, 9, 3));
        l.sort(Comparator.reverseOrder());
        System.out.println(l);
    }
}''', explain="<p><b>How it works:</b> <code>reverseOrder()</code> flips Integer's natural order.</p>"),
dict(level="easy", title="Sort words by length", stmt="<p>Sort <code>[\"banana\", \"fig\", \"apple\"]</code> by length, shortest first.</p>", inp='["banana", "fig", "apple"]',
 code='''import java.util.*;

public class Main {
    public static void main(String[] args) {
        List<String> w = new ArrayList<>(List.of("banana", "fig", "apple"));
        w.sort(Comparator.comparingInt(String::length));
        System.out.println(w);
    }
}''', explain="<p><b>How it works:</b> <code>comparingInt(String::length)</code> builds a comparator from a key: the length of each word.</p>"),
dict(level="easy", title="Comparable product by price", stmt="<p>Make <code>Product</code> Comparable by price and sort three products.</p>", inp="Pen 10, Bag 450, Book 120",
 code='''import java.util.*;

class Product implements Comparable<Product> {
    String name; int price;
    Product(String n, int p) { name = n; price = p; }
    public int compareTo(Product o) { return Integer.compare(price, o.price); }
    public String toString() { return name + " ₹" + price; }
}

public class Main {
    public static void main(String[] args) {
        List<Product> l = new ArrayList<>(List.of(new Product("Pen", 10), new Product("Bag", 450), new Product("Book", 120)));
        Collections.sort(l);
        System.out.println(l);
    }
}''', explain="<p><b>How it works:</b> once the class is Comparable, <code>Collections.sort</code> needs no comparator.</p>"),
dict(level="medium", title="Names: case-insensitive, then by length", stmt="<p>Sort <code>[\"om\", \"Riya\", \"kabir\", \"Om\"]</code> case-insensitively; for equal names, shorter first, then natural order.</p>", inp='["om", "Riya", "kabir", "Om"]',
 code='''import java.util.*;

public class Main {
    public static void main(String[] args) {
        List<String> n = new ArrayList<>(List.of("om", "Riya", "kabir", "Om"));
        n.sort(String.CASE_INSENSITIVE_ORDER.thenComparing(Comparator.naturalOrder()));
        System.out.println(n);
    }
}''', explain="<p><b>How it works:</b> \"om\" and \"Om\" tie case-insensitively; the natural order then puts \"Om\" (capital O = 79) before \"om\" (111).</p>"),
dict(level="medium", title="Nulls last", stmt="<p>Sort <code>[\"b\", null, \"a\"]</code> with nulls at the end.</p>", inp='["b", null, "a"]',
 code='''import java.util.*;

public class Main {
    public static void main(String[] args) {
        List<String> l = new ArrayList<>(Arrays.asList("b", null, "a"));
        l.sort(Comparator.nullsLast(Comparator.naturalOrder()));
        System.out.println(l);
    }
}''', explain="<p><b>How it works:</b> without <code>nullsLast</code>, natural ordering would throw NullPointerException.</p>"),
dict(level="business", title="Delivery route by pin, then time", stmt="<p>Deliveries (pin, time): (410210, 14), (400703, 11), (410210, 9). Sort by pin, then by time.</p>", inp="3 deliveries",
 code='''import java.util.*;

public class Main {
    public static void main(String[] args) {
        List<int[]> d = new ArrayList<>(List.of(new int[]{410210, 14}, new int[]{400703, 11}, new int[]{410210, 9}));
        d.sort(Comparator.<int[]>comparingInt(x -> x[0]).thenComparingInt(x -> x[1]));
        for (int[] x : d) System.out.println(x[0] + " at " + x[1] + ":00");
    }
}''', explain="<p><b>How it works:</b> the second key only matters when the pins are equal. The <code>&lt;int[]&gt;</code> hint tells javac the element type for the lambdas.</p>"),
dict(level="business", title="Top 2 rated restaurants", stmt="<p>Restaurants with ratings: Chai Point 4.3, Dosa Hut 4.7, Vada Corner 4.5. Print the top 2 by rating.</p>", inp="3 restaurants",
 code='''import java.util.*;

public class Main {
    public static void main(String[] args) {
        Map<String, Double> rating = new HashMap<>(Map.of("Chai Point", 4.3, "Dosa Hut", 4.7, "Vada Corner", 4.5));
        List<Map.Entry<String, Double>> list = new ArrayList<>(rating.entrySet());
        list.sort(Map.Entry.<String, Double>comparingByValue().reversed());
        System.out.println(list.subList(0, 2));
    }
}''', explain="<p><b>How it works:</b> map entries can be sorted with <code>Map.Entry.comparingByValue()</code>; reversed for highest first.</p>"),
dict(level="business", title="Safe comparator for large amounts", stmt="<p>Sort transaction amounts in paise <code>[9_000_000_000L, -5L, 300L]</code> ascending, safely.</p>", inp="three long amounts",
 code='''import java.util.*;

public class Main {
    public static void main(String[] args) {
        List<Long> paise = new ArrayList<>(List.of(9_000_000_000L, -5L, 300L));
        paise.sort(Long::compare);
        System.out.println(paise);
    }
}''', explain="<p><b>How it works:</b> <code>Long.compare</code> never overflows; a subtraction cast to int would give wrong signs for values this large.</p>"),
]
