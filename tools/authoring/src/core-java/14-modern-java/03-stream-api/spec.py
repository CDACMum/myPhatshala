import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from mkanim import Anim, two_view
from m14 import code, snippet, runner, quiz

def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

# ---------------- Part 5: two-view animation ----------------
S = Anim("see", frames=6, h=250, label="Orders flow through filter, map and reduce: small orders are dropped, GST is added, and the totals are summed")
S.box(8, 6, 344, 46, None, fill="board", stroke="board")
S.text(14, 24, esc("orders.stream().filter(a -> a >= 999)"), mono=True, size=9, cls="chalk")
S.text(14, 42, esc("    .map(a -> a * 118 / 100).reduce(0, Integer::sum)"), mono=True, size=9, cls="chalk")
stages = [("source", 10), ("filter ≥ 999", 98), ("map +GST", 186), ("reduce sum", 274)]
for name, x in stages:
    S.box(x, 58, 78, 26, name, fill="card2", stroke="line", size=9, bold=True)
src = ["450", "1200", "80", "2600", "999"]
for i, v in enumerate(src):
    S.text(49, 104 + i * 18, v, on="1-2", mono=True, size=10, anchor="middle")
S.box(10, 58, 78, 26, None, fill="none", stroke="track", on="1", sw=2.2, rx=6)
S.box(98, 58, 78, 26, None, fill="none", stroke="track", on="2", sw=2.2, rx=6)
S.box(186, 58, 78, 26, None, fill="none", stroke="track", on="3", sw=2.2, rx=6)
S.box(274, 58, 78, 26, None, fill="none", stroke="track", on="4-5", sw=2.2, rx=6)
kept = ["1200", "2600", "999"]
dropped = ["450", "80"]
for i, v in enumerate(kept):
    S.text(137, 104 + i * 18, v, on="2-", mono=True, size=10, anchor="middle", cls="green")
for i, v in enumerate(dropped):
    S.text(137, 170 + i * 16, v + " ✗", on="2", mono=True, size=9.4, anchor="middle", cls="red")
gst = ["1416", "3068", "1178"]
for i, v in enumerate(gst):
    S.text(225, 104 + i * 18, v, on="3-", mono=True, size=10, anchor="middle", cls="blue")
S.text(313, 104, "0+1416", on="4", mono=True, size=9, anchor="middle")
S.text(313, 122, "+3068", on="4", mono=True, size=9, anchor="middle")
S.text(313, 140, "+1178", on="4", mono=True, size=9, anchor="middle")
S.text(313, 112, "5662", on="5-", mono=True, size=15, bold=True, anchor="middle", cls="green")
S.text(10, 210, "the list itself is unchanged: [450, 1200, 80, 2600, 999]", on="6", size=9.4, cls="ink2")
S.text(10, 192, "one value comes out of the pipeline", on="5", size=9.6, cls="green")
S.note({1: "Five orders go in.", 2: "filter keeps orders of ₹999+.", 3: "map adds 18% GST to each.", 4: "reduce adds them up.",
        5: "Result: ₹5,662.", 6: "The source list is untouched."}, y=234, size=10.5)
S.caps(["<code>orders.stream()</code> makes a <b>stream</b>: a pipeline that will pull the orders through, one by one.",
        "<code>filter</code> keeps only the elements for which the Predicate is true: 450 and 80 are dropped.",
        "<code>map</code> turns each element into a new value with a Function: amount → amount with GST.",
        "<code>reduce(0, Integer::sum)</code> combines all values into one, starting from 0.",
        "The pipeline gives ₹5,662: total billing of the big orders including GST.",
        "Streams don't modify their source. You describe <i>what</i> you want; the stream does the looping."])

B = Anim("behind", frames=6, h=250, label="Streams are lazy: nothing runs until the terminal operation, then each element travels through all stages before the next one starts")
B.box(6, 6, 348, 66, None, fill="board", stroke="board")
B.text(14, 26, "Stream s = orders.stream()", mono=True, size=9, cls="chalk")
B.text(14, 44, "    .filter(...).map(...);   // intermediate", mono=True, size=9, cls="chalk")
B.text(14, 62, "int total = s.reduce(0, Integer::sum);   // terminal", mono=True, size=9, cls="chalk", on="2-")
B.box(6, 82, 348, 126, None, fill="card2", stroke="line")
B.text(16, 100, "console (what each stage prints)", size=9.4, bold=True, cls="ink2")
B.text(16, 124, "(nothing yet: no terminal operation)", size=9.6, cls="ink3", on="1")
logs = {2: ["filter 450  ✗"], 3: ["filter 450  ✗", "filter 1200 → map 1200 → +1416"],
        4: ["filter 450  ✗", "filter 1200 → map 1200 → +1416", "filter 80   ✗"],
        5: ["filter 450  ✗", "filter 1200 → map 1200 → +1416", "filter 80   ✗", "filter 2600 → map 2600 → +3068",
            "filter 999  → map 999  → +1178"],
        6: ["filter 450  ✗", "filter 1200 → map 1200 → +1416", "filter 80   ✗", "filter 2600 → map 2600 → +3068",
            "filter 999  → map 999  → +1178"]}
for f, ls in logs.items():
    for i, l in enumerate(ls):
        B.text(16, 122 + i * 16, l, on=str(f), mono=True, size=8.8, cls="red" if "✗" in l else "ink")
B.text(250, 200, "total 5662", on="6", size=10, bold=True, mono=True, cls="green")
B.note({1: "Building the pipeline runs nothing.", 2: "reduce starts the flow: 450 fails.", 3: "1200 goes all the way through.",
        4: "80 fails the filter.", 5: "2600 and 999 go through.", 6: "One pass over the data."}, y=236, size=10.5)
B.caps(["<code>filter</code> and <code>map</code> are <b>intermediate</b> operations: calling them only records the steps. Nothing is printed, nothing is computed.",
        "<code>reduce</code> is a <b>terminal</b> operation: it starts the flow. The first element, 450, is tested by filter and dropped.",
        "The next element goes through <b>all</b> stages before any other element starts: filter, then map, then into the sum.",
        "Elements move one at a time, “vertically” through the pipeline, not stage by stage over the whole list.",
        "No intermediate lists are built, so streams can process huge data with little memory, and stop early when possible (<code>findFirst</code>, <code>limit</code>).",
        "After the terminal operation the stream is used up. Calling another operation on <code>s</code> throws <code>IllegalStateException</code>."])
ANIM = two_view("filter, map, reduce: both views", S, B)

# ---------------- Part 6: animated example ----------------
ANIM2_HEADING = "Watch it with an example: a city-wise sales report in one pipeline"
ANIM2_INTRO = "A restaurant chain wants total sales per city from today's orders. groupingBy collects the stream into a map."
A = Anim("Group orders by city and sum", frames=5, h=230, label="Orders are grouped by city with groupingBy and each group's amounts are summed")
orders = [("Pune", 450), ("Mumbai", 900), ("Pune", 120), ("Nagpur", 300), ("Mumbai", 640)]
for i, (c, amt) in enumerate(orders):
    A.box(10, 12 + i * 30, 120, 26, None, fill="card2", stroke="line", on="1-3")
    A.text(18, 29 + i * 30, c, size=9.4, bold=True, on="1-3")
    A.text(122, 29 + i * 30, str(amt), size=9.4, mono=True, anchor="end", on="1-3")
groups = [("Mumbai", ["900", "640"], "1540", 12), ("Nagpur", ["300"], "300", 60), ("Pune", ["450", "120"], "570", 108)]
for name, vals, tot, y in groups:
    A.box(160, y, 190, 44, None, fill="soft-blue", stroke="blue", on="2-")
    A.text(170, y + 16, name, size=9.6, bold=True, cls="blue", on="2-")
    A.text(170, y + 34, "[" + ", ".join(vals) + "]", size=9.2, mono=True, on="2-3")
    A.text(170, y + 34, "Rs " + tot, size=11, mono=True, bold=True, cls="green", on="4-")
A.arrow(130, 25, 158, 130, on="2", color="track")
A.arrow(130, 85, 158, 40, on="2", color="track")
A.text(10, 176, "groupingBy(Order::city, TreeMap::new, summingInt(Order::amount))", size=8, mono=True, cls="ink2", on="3-")
A.text(10, 198, "{Mumbai=1540, Nagpur=300, Pune=570}", size=9, mono=True, cls="green", on="5")
A.note({1: "Five orders from three cities.", 2: "groupingBy sorts them into buckets.", 3: "One collector per bucket…",
        4: "…sums each bucket.", 5: "A Map: city → total."}, y=222, size=10.5)
A.caps(["Today's orders, each with a city and an amount.",
        "<code>Collectors.groupingBy(Order::city, …)</code> puts each order into a bucket for its city. (TreeMap keeps the cities sorted.)",
        "groupingBy takes a second collector that decides what to do with each bucket.",
        "<code>summingInt(Order::amount)</code> adds up the amounts inside each bucket.",
        "The result is a <code>Map&lt;String, Integer&gt;</code> ready for the report: one pipeline instead of a loop, a map and manual updates."])
ANIM2 = A

# ---------------- Part 8: tracer ----------------
TRACE = dict(code='''import java.util.*;

public class Main {
    public static void main(String[] args) {
        List<Integer> orders = List.of(450, 1200, 80, 2600);
        int total = orders.stream()
                .filter(amt -> amt >= 999)
                .map(amt -> amt * 118 / 100)
                .reduce(0, Integer::sum);
        long small = orders.stream().filter(amt -> amt < 999).count();
        System.out.println("big orders with GST: Rs " + total + "; small orders: " + small);
    }
}
''', notes={
 5: "Source :: = An immutable list of four order amounts.",
 6: "Pipeline :: = One statement builds and runs the pipeline. Watch the lambda bodies run one element at a time: filter 450 (dropped), filter 1200, map 1200, filter 80 (dropped), filter 2600, map 2600.",
 10: "Another stream :: = A stream can be used once, so a second pipeline is created for the count. <code>count</code> is the terminal operation.",
 11: "Result :: 1416 + 3068 = 4484; two small orders. The list itself never changed."})

# ---------------- Worked examples ----------------
WORKED_INTRO = "Three report-style problems, each solved with one stream pipeline instead of loops and temporary lists. Watch the lambda frames: each element passes through all stages before the next."
EXAMPLES = [
dict(tag="Banking · statements", title="Total debits above ₹500 in a statement",
 problem="<p>From a list of transactions (positive = credit, negative = debit), find how many debits were larger than ₹500 and their total. Use streams.</p>",
 inp="+25000, -1200, -450, +3000, -8500, -90",
 approach=["<code>filter(t -&gt; t &lt; -500)</code> keeps big debits.",
           "<code>mapToInt(Math::abs)</code> turns them into positive ints, giving an <code>IntStream</code>.",
           "Use two pipelines: one to <code>count</code>, one to <code>sum</code>."],
 code='''import java.util.*;

public class Main {
    public static void main(String[] args) {
        List<Integer> txns = List.of(25000, -1200, -450, 3000, -8500, -90);
        long count = txns.stream().filter(t -> t < -500).count();
        int total = txns.stream()
                .filter(t -> t < -500)
                .mapToInt(Math::abs)
                .sum();
        System.out.println(count + " big debits, total Rs " + total);
    }
}
''', notes={5: "Transactions :: Credits are positive, debits negative.",
            6: "Count :: = A pipeline that filters and counts: 2.",
            7: "Sum :: = A second pipeline: filter, convert to positive ints, sum. <code>mapToInt</code> avoids boxing and gives <code>sum()</code>.",
            11: "Report :: 2 debits, Rs 9,700."},
 tryit="Press <b>Run</b>. Then add <code>.average()</code> on an IntStream to get the average big debit (it returns an OptionalDouble)."),
dict(tag="E-commerce · catalogue", title="Top 3 cheapest in-stock products",
 problem="<p>Show the three cheapest products that are in stock, as \"name (Rs price)\" strings, joined by commas.</p>",
 inp="6 products with price and stock",
 approach=["<code>filter</code> on stock &gt; 0.",
           "<code>sorted(Comparator.comparingInt(...))</code> by price, then <code>limit(3)</code>.",
           "<code>map</code> to a label and <code>collect(Collectors.joining(\", \"))</code>."],
 code='''import java.util.*;
import java.util.stream.*;

class Product {
    String name;
    int price, stock;
    Product(String n, int p, int s) { name = n; price = p; stock = s; }
}

public class Main {
    public static void main(String[] args) {
        List<Product> catalogue = List.of(
            new Product("Earphones", 799, 12), new Product("Cable", 199, 0),
            new Product("Cover", 299, 40), new Product("Charger", 999, 5),
            new Product("Stand", 249, 8), new Product("Card reader", 349, 3));
        String top = catalogue.stream()
                .filter(p -> p.stock > 0)
                .sorted(Comparator.comparingInt(p -> p.price))
                .limit(3)
                .map(p -> p.name + " (Rs " + p.price + ")")
                .collect(Collectors.joining(", "));
        System.out.println("Cheapest in stock: " + top);
    }
}
''', notes={12: "Catalogue :: = Six Product objects.",
            16: "Pipeline :: = filter (Cable has no stock), sort by price, keep 3, turn into labels, join. <code>sorted</code> must see every element before it can pass any on, so it's the one step that holds all elements.",
            22: "Result :: Stand, Cover, Card reader."},
 tryit="Press <b>Run</b>. Then make it the 3 <i>most expensive</i>: add <code>.reversed()</code> to the comparator (you'll need <code>Comparator.comparingInt((Product p) -&gt; p.price)</code>)."),
dict(tag="Education · results", title="Grade counts with groupingBy",
 problem="<p>Given students' marks, count how many students got each grade: A (80+), B (60–79), C (40–59), F (below 40). Print the grades in order.</p>",
 inp="marks 92, 67, 45, 81, 38, 74, 59",
 approach=["A small method <code>grade(int)</code> returns the letter.",
           "<code>groupingBy(Main::grade, TreeMap::new, counting())</code> gives a sorted map grade → count.",
           "Print the map."],
 code='''import java.util.*;
import java.util.stream.*;

public class Main {
    static String grade(int m) {
        if (m >= 80) return "A";
        if (m >= 60) return "B";
        if (m >= 40) return "C";
        return "F";
    }

    public static void main(String[] args) {
        List<Integer> marks = List.of(92, 67, 45, 81, 38, 74, 59);
        Map<String, Long> counts = marks.stream()
                .collect(Collectors.groupingBy(Main::grade, TreeMap::new, Collectors.counting()));
        System.out.println(counts);
    }
}
''', notes={13: "Marks :: Seven students' marks.",
            14: "Collect :: = For each mark, <code>grade</code> is called (watch its frames) and the mark is counted in its grade's bucket. TreeMap keeps A, B, C, F in order.",
            16: "Result :: {A=2, B=2, C=2, F=1}."},
 tryit="Press <b>Run</b>. Then replace <code>counting()</code> with <code>Collectors.toList()</code> to see which marks fell in each grade."),
]

# ---------------- Practice problems ----------------
PRACTICE_INTRO = "Replace loops with pipelines: filter, map, sorted, limit, reduce and collect. All outputs are fixed. The last three are business tasks."
PROBLEMS = [
dict(level="easy", title="Even numbers squared", stmt="<p>From 1–10, keep even numbers, square them and collect into a list.</p>", inp="1..10",
 code='''import java.util.stream.*;

public class Main {
    public static void main(String[] args) {
        System.out.println(IntStream.rangeClosed(1, 10)
                .filter(n -> n % 2 == 0)
                .map(n -> n * n)
                .boxed()
                .toList());
    }
}''', explain="<p><b>How it works:</b> <code>IntStream.rangeClosed</code> makes numbers without a list. <code>boxed()</code> turns ints into Integers so they can go into a List.</p>"),
dict(level="easy", title="Names in upper case", stmt="<p>Convert a list of names to upper case with <code>map</code> and print the new list.</p>", inp="asha, ravi, meena",
 code='''import java.util.*;

public class Main {
    public static void main(String[] args) {
        List<String> names = List.of("asha", "ravi", "meena");
        List<String> upper = names.stream().map(String::toUpperCase).toList();
        System.out.println(upper + " (original: " + names + ")");
    }
}''', explain="<p><b>How it works:</b> map creates new values; the original list is unchanged. <code>toList()</code> (Java 16+) returns an unmodifiable list.</p>"),
dict(level="easy", title="Sum and average", stmt="<p>Find the sum and average of daily sales using an IntStream.</p>", inp="1200, 950, 1800, 600",
 code='''import java.util.*;

public class Main {
    public static void main(String[] args) {
        List<Integer> sales = List.of(1200, 950, 1800, 600);
        int sum = sales.stream().mapToInt(Integer::intValue).sum();
        double avg = sales.stream().mapToInt(Integer::intValue).average().orElse(0);
        System.out.println("sum " + sum + ", average " + avg);
    }
}''', explain="<p><b>How it works:</b> primitive streams have <code>sum</code>, <code>average</code>, <code>min</code>, <code>max</code>. average returns OptionalDouble because an empty stream has no average (Lesson 14.4).</p>"),
dict(level="medium", title="Distinct sorted cities", stmt="<p>From a list of delivery cities with repeats, print the unique cities in alphabetical order, comma-separated.</p>", inp="Pune, Goa, Pune, Delhi, Goa, Agra",
 code='''import java.util.*;
import java.util.stream.*;

public class Main {
    public static void main(String[] args) {
        List<String> cities = List.of("Pune", "Goa", "Pune", "Delhi", "Goa", "Agra");
        System.out.println(cities.stream().distinct().sorted().collect(Collectors.joining(", ")));
    }
}''', explain="<p><b>How it works:</b> <code>distinct</code> removes duplicates using <code>equals</code>; <code>sorted</code> uses natural order; <code>joining</code> builds one String.</p>"),
dict(level="medium", title="Find the first match", stmt="<p>Find the first order above ₹2,000 and check whether any order is below ₹100.</p>", inp="450, 1200, 2600, 80, 3100",
 code='''import java.util.*;

public class Main {
    public static void main(String[] args) {
        List<Integer> orders = List.of(450, 1200, 2600, 80, 3100);
        int first = orders.stream().filter(o -> o > 2000).findFirst().orElse(-1);
        boolean tiny = orders.stream().anyMatch(o -> o < 100);
        System.out.println("first big order: " + first + ", any tiny order: " + tiny);
    }
}''', explain="<p><b>How it works:</b> findFirst and anyMatch are <b>short-circuiting</b>: they stop as soon as they know the answer, without looking at the rest.</p>"),
dict(level="medium", title="Word frequency", stmt="<p>Count how often each word appears in a review, case-insensitively, in alphabetical order.</p>", inp="\"Good food good price GOOD service\"",
 code='''import java.util.*;
import java.util.stream.*;

public class Main {
    public static void main(String[] args) {
        String review = "Good food good price GOOD service";
        Map<String, Long> freq = Arrays.stream(review.toLowerCase().split(" "))
                .collect(Collectors.groupingBy(w -> w, TreeMap::new, Collectors.counting()));
        System.out.println(freq);
    }
}''', explain="<p><b>How it works:</b> <code>Arrays.stream</code> streams an array. groupingBy with counting is the standard word-count pattern used in text analytics.</p>"),
dict(level="business", title="Revenue per category", stmt="<p>Sum revenue per product category from a list of sales, sorted by category name.</p>", inp="6 sales in 3 categories",
 code='''import java.util.*;
import java.util.stream.*;

class Sale {
    String category;
    int amount;
    Sale(String c, int a) { category = c; amount = a; }
}

public class Main {
    public static void main(String[] args) {
        List<Sale> sales = List.of(new Sale("Grocery", 450), new Sale("Mobile", 12999), new Sale("Grocery", 230),
                                   new Sale("Fashion", 1599), new Sale("Mobile", 499), new Sale("Fashion", 899));
        Map<String, Integer> byCat = sales.stream()
                .collect(Collectors.groupingBy(s -> s.category, TreeMap::new, Collectors.summingInt(s -> s.amount)));
        byCat.forEach((cat, total) -> System.out.println(cat + ": Rs " + total));
    }
}''', explain="<p><b>How it works:</b> this is SQL's <code>GROUP BY category SUM(amount)</code>, done in memory.</p>"),
dict(level="business", title="Top 2 customers by spend", stmt="<p>From orders (customer, amount), total each customer's spend and print the top 2 spenders.</p>", inp="7 orders, 4 customers",
 code='''import java.util.*;
import java.util.stream.*;

public class Main {
    public static void main(String[] args) {
        String[][] orders = {{"Asha", "1200"}, {"Ravi", "300"}, {"Asha", "450"}, {"Meena", "2100"},
                             {"Imran", "800"}, {"Ravi", "1900"}, {"Imran", "150"}};
        Map<String, Integer> spend = Arrays.stream(orders)
                .collect(Collectors.groupingBy(o -> o[0], Collectors.summingInt(o -> Integer.parseInt(o[1]))));
        spend.entrySet().stream()
                .sorted(Map.Entry.<String, Integer>comparingByValue().reversed())
                .limit(2)
                .forEach(e -> System.out.println(e.getKey() + " Rs " + e.getValue()));
    }
}''', explain="<p><b>How it works:</b> two pipelines: one to total per customer, one over the map's entries to rank them. Ties would need a second comparator for a stable order.</p>"),
dict(level="business", title="Pending deliveries report", stmt="<p>From delivery records, list the ids of PENDING deliveries older than 2 days, sorted, and print how many there are.</p>", inp="6 deliveries",
 code='''import java.util.*;
import java.util.stream.*;

class Delivery {
    String id, status;
    int ageDays;
    Delivery(String i, String s, int a) { id = i; status = s; ageDays = a; }
}

public class Main {
    public static void main(String[] args) {
        List<Delivery> all = List.of(new Delivery("D7", "PENDING", 3), new Delivery("D2", "DONE", 5),
                new Delivery("D9", "PENDING", 1), new Delivery("D4", "PENDING", 4),
                new Delivery("D1", "DONE", 1), new Delivery("D5", "PENDING", 6));
        List<String> late = all.stream()
                .filter(d -> d.status.equals("PENDING"))
                .filter(d -> d.ageDays > 2)
                .map(d -> d.id)
                .sorted()
                .toList();
        System.out.println(late.size() + " late deliveries: " + late);
    }
}''', explain="<p><b>How it works:</b> chaining two filters reads like the business rule. The pipeline is easy to extend: add <code>.limit(10)</code> for a dashboard widget.</p>"),
]

# ---------------- Extra blocks ----------------
BLOCKS = {
'ANIM': ANIM,
'CODE_OPS': snippet('''// create                     intermediate (lazy, return a Stream)      terminal (start the work)
list.stream()                  filter(Predicate)                         forEach(Consumer)
Arrays.stream(array)           map(Function)                             collect(Collectors.toList()) / toList()
Stream.of(a, b, c)             mapToInt / mapToDouble                    reduce(identity, BinaryOperator)
IntStream.range(0, n)          sorted() / sorted(Comparator)             count() / sum() / average()
Files.lines(path)              distinct() / limit(n) / skip(n)           findFirst() / anyMatch / allMatch
                               peek(Consumer)  (debugging)               min / max (Comparator)''', lang='text', file='Stream API'),
'CODE_LAZY': code('''import java.util.*;
import java.util.stream.*;

public class Main {
    public static void main(String[] args) {
        List<Integer> orders = List.of(450, 1200, 80, 2600);
        Stream<Integer> pipeline = orders.stream()
                .filter(a -> { System.out.println("  filter " + a); return a >= 999; })
                .map(a -> { System.out.println("  map " + a); return a * 118 / 100; });
        System.out.println("pipeline built, nothing ran yet");
        int total = pipeline.reduce(0, Integer::sum);
        System.out.println("total = " + total);
    }
}'''),
'CODE_RUN': code('''import java.util.*;
import java.util.stream.*;

public class Main {
    public static void main(String[] args) {
        List<String> orders = List.of("dosa:80", "thali:120", "chai:15", "dosa:80", "biryani:220", "chai:15");

        int revenue = orders.stream()
                .mapToInt(o -> Integer.parseInt(o.split(":")[1]))
                .sum();

        List<String> premium = orders.stream()
                .filter(o -> Integer.parseInt(o.split(":")[1]) >= 100)
                .map(o -> o.split(":")[0])
                .distinct()
                .sorted()
                .toList();

        Map<String, Long> counts = orders.stream()
                .map(o -> o.split(":")[0])
                .collect(Collectors.groupingBy(d -> d, TreeMap::new, Collectors.counting()));

        System.out.println("revenue: Rs " + revenue);
        System.out.println("premium dishes: " + premium);
        System.out.println("orders per dish: " + counts);
    }
}'''),
'RUNNER': runner([
 dict(label="1 · Canteen report", hint="Press <b>Run</b>. Then add the average order value with <code>.average()</code> on an IntStream.",
      code='''import java.util.*;
import java.util.stream.*;

public class Main {
    public static void main(String[] args) {
        List<String> orders = List.of("dosa:80", "thali:120", "chai:15", "dosa:80", "biryani:220", "chai:15");

        int revenue = orders.stream()
                .mapToInt(o -> Integer.parseInt(o.split(":")[1]))
                .sum();

        Map<String, Long> counts = orders.stream()
                .map(o -> o.split(":")[0])
                .collect(Collectors.groupingBy(d -> d, TreeMap::new, Collectors.counting()));

        System.out.println("revenue: Rs " + revenue);
        System.out.println("orders per dish: " + counts);
    }
}'''),
 dict(label="2 · Predict: which lines print?", hint="<b>Predict first:</b> no terminal operation is called. Does anything inside the lambdas print? Then add <code>.toList()</code> at the end.",
      code='''import java.util.*;

public class Main {
    public static void main(String[] args) {
        List<Integer> n = List.of(1, 2, 3);
        n.stream()
         .filter(x -> { System.out.println("checking " + x); return x > 1; })
         .map(x -> x * 10);
        System.out.println("done");
    }
}'''),
 dict(label="3 · Predict: how far does it look?", hint="<b>Predict first:</b> how many numbers does the filter check before <code>limit(2)</code> is satisfied?",
      code='''import java.util.stream.*;

public class Main {
    public static void main(String[] args) {
        var result = Stream.of(1, 2, 3, 4, 5, 6, 7, 8)
                .filter(x -> { System.out.print("check " + x + "; "); return x % 3 == 0; })
                .limit(2)
                .toList();
        System.out.println();
        System.out.println(result);
    }
}'''),
 dict(label="4 · Crash: reusing a stream", hint="A stream can be consumed only once. Create a new stream for the second operation (e.g. call <code>orders.stream()</code> again).",
      code='''import java.util.*;
import java.util.stream.*;

public class Main {
    public static void main(String[] args) {
        List<Integer> orders = List.of(450, 1200, 80);
        Stream<Integer> s = orders.stream().filter(o -> o > 100);
        System.out.println("count: " + s.count());
        System.out.println("max: " + s.max(Integer::compare).get());
    }
}''', _expect="exception"),
 dict(label="5 · Spot the error", hint="<code>map</code> returns a Stream, not a List. End the pipeline with <code>.toList()</code> or <code>.collect(Collectors.toList())</code>.",
      code='''import java.util.*;

public class Main {
    public static void main(String[] args) {
        List<String> names = List.of("asha", "ravi");
        List<String> upper = names.stream().map(String::toUpperCase);
        System.out.println(upper);
    }
}''', _expect="compile-error"),
]),
'QUIZ': quiz([
 {"q": "Which is a terminal operation?", "options": ["filter", "map", "sorted", "collect"], "answer": 3, "why": "filter, map and sorted are intermediate; collect, reduce, forEach, count are terminal."},
 {"q": "What happens when you call only filter and map on a stream?", "options": ["Both run immediately", "Nothing runs until a terminal operation", "Only filter runs", "An exception"], "answer": 1, "why": "Intermediate operations are lazy."},
 {"q": "Does stream().filter(...) change the original list?", "options": ["Yes", "No", "Only for ArrayList", "Only if sorted"], "answer": 1, "why": "Streams don't modify their source."},
 {"q": "Using a stream a second time after count() throws…", "options": ["NullPointerException", "IllegalStateException", "ConcurrentModificationException", "Nothing"], "answer": 1, "why": "\"stream has already been operated upon or closed\"."},
 {"q": "reduce(0, Integer::sum) on [3, 4, 5] gives…", "options": ["0", "12", "60", "345"], "answer": 1, "why": "0+3+4+5."},
 {"q": "Which collector gives a Map from key to count?", "options": ["toList()", "joining()", "groupingBy(key, counting())", "summingInt"], "answer": 2, "why": "groupingBy with a downstream counting collector."},
 {"q": "Why use mapToInt instead of map for numbers?", "options": ["It's required", "It avoids boxing and gives sum/average", "It sorts", "It's lazy and map isn't"], "answer": 1, "why": "IntStream works with primitive ints."},
 {"q": "In a lazy pipeline, elements are processed…", "options": ["stage by stage over the whole list", "one element at a time through all stages", "in random order", "in parallel always"], "answer": 1, "why": "Except for stateful steps like sorted, each element flows through before the next."},
]),
}
