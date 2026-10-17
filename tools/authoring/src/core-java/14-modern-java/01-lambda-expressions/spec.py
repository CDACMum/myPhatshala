import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from mkanim import Anim, two_view
from m14 import code, snippet, runner, quiz

def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

# ---------------- Part 5: two-view animation ----------------
S = Anim("see", frames=6, h=250, label="An anonymous Comparator class shrinks step by step into a one-line lambda that sorts prices")
S.box(8, 8, 344, 150, None, fill="board", stroke="board")
versions = {
 1: ["prices.sort(new Comparator<Integer>() {", "    public int compare(Integer a, Integer b) {", "        return a - b;", "    }", "});"],
 2: ["prices.sort(new Comparator<Integer>() {", "    public int compare(Integer a, Integer b) {", "        return a - b;", "    }", "});"],
 3: ["prices.sort((Integer a, Integer b) -> {", "    return a - b;", "});"],
 4: ["prices.sort((a, b) -> {", "    return a - b;", "});"],
 5: ["prices.sort((a, b) -> a - b);"],
 6: ["prices.sort((a, b) -> a - b);"],
}
for f, ls in versions.items():
    for i, l in enumerate(ls):
        S.text(18, 32 + i * 22, esc(l), on=str(f), mono=True, size=9.4, cls="chalk")
S.box(12, 16, 336, 72, None, fill="none", stroke="red", on="2", rx=4)
S.text(18, 148, "boilerplate: class, method name, types", on="2", size=9.2, cls="red")
S.text(18, 148, "types inferred from List<Integer>", on="4", size=9.2, cls="acc")
S.text(18, 148, "one expression: no braces, no return", on="5", size=9.2, cls="green")
lines = {1: "5 lines", 2: "5 lines", 3: "3 lines", 4: "3 lines", 5: "1 line", 6: "1 line"}
for f, t in lines.items():
    S.text(300, 150, t, on=str(f), size=9.6, bold=True, cls="ink3", anchor="middle")
S.text(10, 182, "prices:", size=10, bold=True, cls="ink2")
S.text(64, 182, "[450, 120, 899]", on="1-5", size=11, mono=True)
S.text(64, 182, "[120, 450, 899]", on="6", size=11, mono=True, bold=True, cls="green")
S.text(10, 206, "same behaviour in every version", size=9.4, cls="ink3", on="1-5")
S.text(10, 206, "sorted cheapest first", size=9.4, cls="green", on="6")
S.note({1: "The old way: an anonymous class.", 2: "Most of it is ceremony.", 3: "Keep only parameters and body.",
        4: "Drop the parameter types.", 5: "Single expression: drop braces and return.", 6: "Run it: sorted."}, y=234, size=10.5)
S.caps(["Before Java 8, passing behaviour meant writing an <b>anonymous class</b>: here a Comparator that compares two prices.",
        "Only one line, <code>return a - b;</code>, is the real logic. The rest (class, method name, types) is the same every time.",
        "A <b>lambda</b> keeps just the parameters, an arrow <code>-&gt;</code>, and the body.",
        "The compiler already knows the list holds Integers, so it can <b>infer</b> the parameter types.",
        "When the body is a single expression, drop the braces and <code>return</code>: the value is returned automatically.",
        "<code>sort</code> calls the lambda each time it needs to compare two prices. The list ends up cheapest first."])

B = Anim("behind", frames=6, h=250, label="How the JVM runs a lambda: the body becomes a private method, invokedynamic creates an object implementing the interface, and calls go through it")
B.box(6, 6, 170, 110, None, fill="board", stroke="board")
B.text(16, 24, "Main.class (compiled)", size=9.2, bold=True, cls="chalk")
B.text(16, 46, "main(): invokedynamic", size=8.8, mono=True, cls="chalk", on="2-")
B.text(16, 66, "private static int", size=8.8, mono=True, cls="chalk")
B.text(16, 84, "  lambda$main$0(a, b)", size=8.8, mono=True, cls="chalk")
B.text(16, 102, "  { return a - b; }", size=8.8, mono=True, cls="chalk")
B.box(10, 56, 162, 54, None, fill="none", stroke="track", on="1", rx=4)
B.box(186, 6, 168, 110, None, fill="soft-blue", stroke="blue")
B.text(196, 24, "HEAP", size=10, bold=True, cls="blue")
B.box(196, 34, 148, 34, None, fill="card", stroke="green", on="3-")
B.text(204, 55, "#1 lambda (Comparator)", size=8.8, bold=True, mono=True, on="3-")
B.box(196, 76, 148, 32, None, fill="card", stroke="line")
B.text(204, 96, "#2 ArrayList [3]", size=8.8, mono=True)
B.box(6, 128, 348, 80, None, fill="card2", stroke="line")
B.text(16, 146, "call path", size=9.5, bold=True, cls="ink2")
B.text(16, 168, "sort → #1.compare(450, 120)", size=9.4, mono=True, on="4-")
B.text(16, 188, "     → lambda$main$0 → 330", size=9.4, mono=True, on="4")
B.text(16, 188, "     → many compares → sorted", size=9.4, mono=True, on="5", cls="green")
B.text(16, 168, "the first time this line runs:", size=9.4, on="2-3")
B.text(16, 188, "the JVM builds a tiny class", size=9.4, on="2")
B.text(16, 188, "…and one object of it (#1)", size=9.4, on="3")
B.text(16, 168, "no captured values: the same #1", size=9.4, on="6")
B.text(16, 188, "object can be reused every time", size=9.4, on="6")
B.note({1: "The body is compiled to a method.", 2: "invokedynamic at the lambda line.", 3: "A Comparator object appears.",
        4: "sort calls compare on it.", 5: "Called once per comparison.", 6: "Stateless lambdas are reused."}, y=236, size=10.5)
B.caps(["javac compiles the lambda body into a hidden <code>private static</code> method of Main, named something like <code>lambda$main$0</code>. No separate .class file is written.",
        "Where the lambda appears, javac puts an <code>invokedynamic</code> instruction. The first time it runs, the JVM generates a small class that implements <code>Comparator</code>.",
        "invokedynamic returns an instance of that class (#1): the lambda is a real object on the heap.",
        "<code>sort</code> only knows it has a Comparator. It calls <code>compare(450, 120)</code>, which forwards to <code>lambda$main$0</code>.",
        "Sorting calls compare once per comparison; the lambda object just forwards each call.",
        "A lambda that captures nothing has no state, so the JVM can hand out the same object every time that line runs. A lambda that captures a variable gets a field holding a copy of it."])
ANIM = two_view("From anonymous class to lambda, both views", S, B)

# ---------------- Part 6: animated example ----------------
ANIM2_HEADING = "Watch it with an example: sorting restaurants in a food app"
ANIM2_INTRO = "The user taps “Sort by rating”, then “Within 3 km”. Each button simply passes a different lambda to the same list methods."
A = Anim("One list, different lambdas", frames=5, h=230, label="A restaurant list is sorted by rating with one lambda and filtered by distance with another")
rest = [("Dosa Corner", "4.1", "2.5"), ("Spice Hub", "4.6", "5.0"), ("Chai Point", "3.9", "1.2"), ("Biryani Bay", "4.4", "2.8")]
order = {1: [0, 1, 2, 3], 2: [1, 3, 0, 2], 3: [1, 3, 0, 2], 4: [3, 0, 2], 5: [3, 0, 2]}
for f, idx in order.items():
    for row, i in enumerate(idx):
        n, r, d = rest[i]
        y = 16 + row * 30
        gone = (f == 3 and i == 1)
        A.box(10, y, 200, 26, None, fill="card" if not gone else "soft-acc", stroke="line" if not gone else "red", on=str(f))
        A.text(18, y + 17, n, size=9.6, bold=True, on=str(f), cls="red" if gone else "ink")
        A.text(120, y + 17, "★" + r, size=9.2, mono=True, on=str(f), cls="acc")
        A.text(160, y + 17, d + " km", size=9.2, mono=True, on=str(f), cls="ink2")
A.box(222, 16, 130, 120, None, fill="board", stroke="board", on="2-")
A.text(230, 36, "sort:", size=9, cls="chalk", on="2-")
A.text(230, 54, "(a, b) -> Double", size=8.6, mono=True, cls="chalk", on="2-")
A.text(230, 70, ".compare(b.rating,", size=8.6, mono=True, cls="chalk", on="2-")
A.text(230, 86, "  a.rating)", size=8.6, mono=True, cls="chalk", on="2-")
A.text(230, 108, "removeIf:", size=9, cls="chalk", on="3-")
A.text(230, 126, "r -> r.km > maxKm", size=8.6, mono=True, cls="chalk", on="3-")
A.text(10, 150, "maxKm = 3 (from the filter chip)", size=9.2, cls="ink2", on="3-")
A.text(10, 172, "Showing 3 restaurants, best rated first", size=10, bold=True, cls="green", on="5")
A.note({1: "The list from the server.", 2: "Sort by rating: highest first.", 3: "Filter: farther than 3 km?",
        4: "Spice Hub removed.", 5: "Shown to the user."}, y=206, size=10.5)
A.caps(["The app has a <code>List&lt;Restaurant&gt;</code> in server order.",
        "“Sort by rating” calls <code>list.sort(…)</code> with a lambda that compares <b>b</b> with <b>a</b>, so the highest rating comes first.",
        "“Within 3 km” calls <code>removeIf</code> with a lambda that uses <code>maxKm</code>, a local variable the lambda <b>captures</b>.",
        "Spice Hub is 5 km away, so the lambda returns true for it and it's removed.",
        "No new classes were written for either button: each behaviour was a one-line lambda handed to a library method. (Real apps usually filter a copy so the original list is kept.)"])
ANIM2 = A

# ---------------- Part 8: tracer ----------------
TRACE = dict(code='''import java.util.*;

public class Main {
    public static void main(String[] args) {
        List<Integer> prices = new ArrayList<>(List.of(450, 120, 899));
        prices.sort((a, b) -> a - b);
        int budget = 500;
        prices.removeIf(p -> p > budget);
        prices.forEach(p -> System.out.println("affordable: Rs " + p));
    }
}
''', notes={
 5: "List :: = An ArrayList with three prices in server order.",
 6: "Sort :: = The lambda <code>(a, b) -> a - b</code> becomes a Comparator object. <code>sort</code> calls it for each comparison; you can watch the lambda body run below.",
 7: "Budget :: A local variable. It never changes, so it is <i>effectively final</i> and a lambda may use it.",
 8: "Filter :: = <code>removeIf</code> calls the lambda once per element; it removes those for which it returns true. The lambda captured a copy of <code>budget</code> (500).",
 9: "Each :: = <code>forEach</code> calls the third lambda once for every remaining price."})

# ---------------- Worked examples ----------------
WORKED_INTRO = "Three ways lambdas replace whole classes in everyday code: a comparator for sorting, behaviour stored in variables, and a list of tasks. Watch the lambda bodies run as separate frames on the stack."
EXAMPLES = [
dict(tag="E-commerce · orders", title="Sort orders by amount, then by customer",
 problem="<p>An admin panel lists orders. Sort them by amount (highest first); when amounts are equal, by customer name A–Z. Use a lambda comparator instead of writing a Comparator class.</p>",
 inp="Ravi 1200, Asha 450, Meena 1200, Imran 99",
 approach=["A small class <code>Order</code> with name and amount.",
           "<code>orders.sort((x, y) -> …)</code>: compare amounts in reverse; if equal, compare names.",
           "Print the sorted list."],
 code='''import java.util.*;

class Order {
    String customer;
    int amount;
    Order(String c, int a) { customer = c; amount = a; }
}

public class Main {
    public static void main(String[] args) {
        List<Order> orders = new ArrayList<>(List.of(
            new Order("Ravi", 1200), new Order("Asha", 450), new Order("Meena", 1200), new Order("Imran", 99)));
        orders.sort((x, y) -> {
            if (x.amount != y.amount) return Integer.compare(y.amount, x.amount);
            return x.customer.compareTo(y.customer);
        });
        for (Order o : orders) System.out.println(o.customer + " Rs " + o.amount);
    }
}
''', notes={11: "Orders :: = Four Order objects in arrival order.",
            13: "Comparator lambda :: = A block-bodied lambda: braces and return statements, because it needs two steps.",
            14: "Amounts :: <code>Integer.compare(y, x)</code> (y first) puts bigger amounts first.",
            15: "Tie :: Equal amounts: alphabetical by name, so Meena comes before Ravi.",
            17: "Result :: Meena 1200, Ravi 1200, Asha 450, Imran 99."},
 tryit="Press <b>Run</b>. Then sort by name only: <code>orders.sort((x, y) -> x.customer.compareTo(y.customer))</code>."),
dict(tag="Retail · offers", title="Discount rules as lambdas",
 problem="<p>A shop runs different discount rules: festival (20% off), student (Rs 50 off above Rs 300), none. Store each rule as a lambda in a variable of a small interface <code>Rule</code>, and apply all three to a Rs 800 bill.</p>",
 inp="bill Rs 800",
 approach=["Declare <code>interface Rule { double apply(double bill); }</code>: one abstract method, so lambdas fit.",
           "Assign three lambdas to three <code>Rule</code> variables.",
           "Call <code>apply</code> on each: same call, different behaviour."],
 code='''interface Rule {
    double apply(double bill);
}

public class Main {
    public static void main(String[] args) {
        Rule festival = bill -> bill * 0.8;
        Rule student = bill -> bill > 300 ? bill - 50 : bill;
        Rule none = bill -> bill;
        double bill = 800;
        System.out.println("festival: Rs " + festival.apply(bill));
        System.out.println("student:  Rs " + student.apply(bill));
        System.out.println("none:     Rs " + none.apply(bill));
    }
}
''', notes={7: "Rule 1 :: = A lambda object implementing Rule: 20% off.",
            8: "Rule 2 :: = A lambda with a condition (ternary operator).",
            9: "Rule 3 :: = The identity rule: returns the bill unchanged.",
            10: "Bill :: The amount to test.",
            11: "Apply :: = Calling <code>festival.apply(800)</code> runs the first lambda's body: 640.0.",
            12: "Apply :: = Same method name, different lambda: 750.0.",
            13: "Apply :: = 800.0."},
 tryit="Press <b>Run</b>. Then add a rule <code>weekend</code> that takes 10% off only above Rs 1,000."),
dict(tag="Notifications · tasks", title="A queue of tasks as Runnable lambdas",
 problem="<p>After an order is placed, the app must send an SMS, an email and update stock. Keep these as <code>Runnable</code> lambdas in a list and run them one by one, capturing the order id.</p>",
 inp="order id 7781",
 approach=["<code>int orderId = 7781;</code> is effectively final, so the lambdas can capture it.",
           "Put three <code>Runnable</code> lambdas in a <code>List</code>.",
           "Loop and call <code>run()</code> on each."],
 code='''import java.util.*;

public class Main {
    public static void main(String[] args) {
        int orderId = 7781;
        List<Runnable> afterOrder = new ArrayList<>();
        afterOrder.add(() -> System.out.println("SMS: order " + orderId + " confirmed"));
        afterOrder.add(() -> System.out.println("Email: invoice for " + orderId));
        afterOrder.add(() -> System.out.println("Stock: reserved items of " + orderId));
        for (Runnable task : afterOrder) {
            task.run();
        }
        System.out.println(afterOrder.size() + " tasks done");
    }
}
''', notes={5: "Order id :: Captured by all three lambdas below.",
            6: "Task list :: An empty list of Runnables.",
            7: "Task 1 :: = A lambda object with its own copy of orderId.",
            9: "Task 3 :: = The list now holds three lambda objects.",
            (11, 1): "Run :: = Calling <code>run()</code> executes the first lambda's body.",
            13: "Done :: All three ran, in list order."},
 tryit="Press <b>Run</b>. Then try <code>orderId++</code> after the lambdas: the compiler refuses, because captured variables must stay effectively final."),
]

# ---------------- Practice problems ----------------
PRACTICE_INTRO = "Write lambdas for sorting, filtering, looping and your own one-method interfaces. Every output is fixed. The last three are business tasks."
PROBLEMS = [
dict(level="easy", title="Sort names by length", stmt="<p>Sort a list of city names from shortest to longest using a lambda.</p>", inp="Mumbai, Pune, Bengaluru, Goa",
 code='''import java.util.*;

public class Main {
    public static void main(String[] args) {
        List<String> cities = new ArrayList<>(List.of("Mumbai", "Pune", "Bengaluru", "Goa"));
        cities.sort((a, b) -> a.length() - b.length());
        System.out.println(cities);
    }
}''', explain="<p><b>How it works:</b> a comparator returns negative, zero or positive. <code>List.sort</code> is stable, so equal-length names keep their order.</p>"),
dict(level="easy", title="forEach with a lambda", stmt="<p>Print each item of a shopping list in upper case using <code>forEach</code>.</p>", inp="milk, bread, eggs",
 code='''import java.util.*;

public class Main {
    public static void main(String[] args) {
        List<String> items = List.of("milk", "bread", "eggs");
        items.forEach(item -> System.out.println(item.toUpperCase()));
    }
}''', explain="<p><b>How it works:</b> forEach calls the lambda once per element. A single parameter needs no brackets.</p>"),
dict(level="easy", title="Your own functional interface", stmt="<p>Declare <code>interface Greeter { String greet(String name); }</code> and implement it with a lambda.</p>", inp="Asha",
 code='''interface Greeter {
    String greet(String name);
}

public class Main {
    public static void main(String[] args) {
        Greeter hello = name -> "Namaste, " + name + "!";
        System.out.println(hello.greet("Asha"));
    }
}''', explain="<p><b>How it works:</b> any interface with exactly one abstract method can be implemented by a lambda. The lambda's parameter and return types come from that method.</p>"),
dict(level="medium", title="Remove failed payments", stmt="<p>Remove all negative amounts (failed payments) from a list with <code>removeIf</code>.</p>", inp="[500, -1, 230, -1, 80]",
 code='''import java.util.*;

public class Main {
    public static void main(String[] args) {
        List<Integer> payments = new ArrayList<>(List.of(500, -1, 230, -1, 80));
        payments.removeIf(p -> p < 0);
        System.out.println(payments);
    }
}''', explain="<p><b>How it works:</b> removeIf is safer than removing inside a for-each loop, which throws ConcurrentModificationException (Lesson 11.7).</p>"),
dict(level="medium", title="Capture a threshold", stmt="<p>Keep only marks at or above a pass mark stored in a local variable.</p>", inp="pass 40; marks 35, 72, 40, 18, 90",
 code='''import java.util.*;

public class Main {
    public static void main(String[] args) {
        int passMark = 40;
        List<Integer> marks = new ArrayList<>(List.of(35, 72, 40, 18, 90));
        marks.removeIf(m -> m < passMark);
        System.out.println("passed: " + marks);
    }
}''', explain="<p><b>How it works:</b> the lambda captures <code>passMark</code>. It's never reassigned, so it's effectively final.</p>"),
dict(level="medium", title="Replace every value", stmt="<p>Add 18% GST to every price in a list in place, using <code>replaceAll</code>.</p>", inp="[100, 250, 40]",
 code='''import java.util.*;

public class Main {
    public static void main(String[] args) {
        List<Integer> prices = new ArrayList<>(List.of(100, 250, 40));
        prices.replaceAll(p -> p * 118 / 100);
        System.out.println(prices);
    }
}''', explain="<p><b>How it works:</b> replaceAll calls the lambda for each element and stores what it returns. Integer arithmetic truncates: 40 × 118 / 100 = 47.</p>"),
dict(level="business", title="Leaderboard sort", stmt="<p>Sort sales agents by deals closed (most first), and by name when tied. Print rank, name and deals.</p>", inp="Ravi 12, Asha 15, Meena 12, Joseph 9",
 code='''import java.util.*;

public class Main {
    public static void main(String[] args) {
        String[] names = {"Ravi", "Asha", "Meena", "Joseph"};
        int[] deals = {12, 15, 12, 9};
        List<Integer> idx = new ArrayList<>(List.of(0, 1, 2, 3));
        idx.sort((a, b) -> deals[a] != deals[b] ? deals[b] - deals[a] : names[a].compareTo(names[b]));
        for (int r = 0; r < idx.size(); r++) {
            int i = idx.get(r);
            System.out.println((r + 1) + ". " + names[i] + " - " + deals[i]);
        }
    }
}''', explain="<p><b>How it works:</b> sorting a list of indexes lets you sort parallel arrays together. The lambda reads the arrays it captured.</p>"),
dict(level="business", title="Validation rules list", stmt="<p>A signup form has rules stored as lambdas of <code>interface Check { boolean ok(String phone); }</code>. Run every rule on a phone number and print which ones fail.</p>", inp="phone \"98765x210\"",
 code='''import java.util.*;

interface Check {
    boolean ok(String phone);
}

public class Main {
    public static void main(String[] args) {
        Map<String, Check> rules = new LinkedHashMap<>();
        rules.put("10 digits", p -> p.length() == 10);
        rules.put("only numbers", p -> p.chars().allMatch(Character::isDigit));
        rules.put("starts 6-9", p -> p.charAt(0) >= '6' && p.charAt(0) <= '9');
        String phone = "98765x210";
        rules.forEach((name, rule) -> System.out.println((rule.ok(phone) ? "ok   " : "FAIL ") + name));
    }
}''', explain="<p><b>How it works:</b> rules stored as data can be added or removed without changing the checking loop. Map.forEach takes a two-parameter lambda.</p>"),
dict(level="business", title="Event handlers for a payment", stmt="<p>Register handlers (Runnables) for SUCCESS and FAILED payment events in a map, then fire the handler for an incoming status.</p>", inp="status SUCCESS",
 code='''import java.util.*;

public class Main {
    public static void main(String[] args) {
        Map<String, Runnable> handlers = new HashMap<>();
        handlers.put("SUCCESS", () -> System.out.println("Show receipt and send SMS"));
        handlers.put("FAILED", () -> System.out.println("Show retry button"));
        String status = "SUCCESS";
        handlers.getOrDefault(status, () -> System.out.println("Unknown status")).run();
    }
}''', explain="<p><b>How it works:</b> this is how button clicks and payment callbacks are wired in real apps: the code to run later is passed as a lambda now.</p>"),
]

# ---------------- Extra blocks ----------------
BLOCKS = {
'ANIM': ANIM,
'CODE_FORMS': snippet('''() -> System.out.println("hi")            // no parameters
x -> x * 2                                // one parameter: brackets optional
(a, b) -> a + b                           // two parameters
(int a, int b) -> a + b                   // explicit types (all or none)
(a, b) -> {                               // block body: braces + return
    int s = a + b;
    return s;
}'''),
'CODE_THIS': code('''public class Main {
    String name = "outer object";

    void demo() {
        Runnable lambda = () -> System.out.println("lambda sees: " + this.name);
        Runnable anon = new Runnable() {
            String name = "anonymous object";
            public void run() {
                System.out.println("anonymous sees: " + this.name);
            }
        };
        lambda.run();
        anon.run();
    }

    public static void main(String[] args) {
        new Main().demo();
    }
}'''),
'CODE_RUN': code('''import java.util.*;

public class Main {
    public static void main(String[] args) {
        List<String> dishes = new ArrayList<>(List.of("thali", "dosa", "chai", "biryani", "idli"));

        dishes.sort((a, b) -> a.compareTo(b));
        System.out.println("A-Z:        " + dishes);

        dishes.sort((a, b) -> b.length() - a.length());
        System.out.println("longest:    " + dishes);

        int maxLen = 4;
        dishes.removeIf(d -> d.length() > maxLen);
        System.out.println("short ones: " + dishes);

        dishes.forEach(d -> System.out.println("  - " + d));
    }
}'''),
'RUNNER': runner([
 dict(label="1 · Sort, filter, print", hint="Press <b>Run</b>. Then change <code>maxLen</code> to 5 and add your own sort by the last letter.",
      code='''import java.util.*;

public class Main {
    public static void main(String[] args) {
        List<String> dishes = new ArrayList<>(List.of("thali", "dosa", "chai", "biryani", "idli"));

        dishes.sort((a, b) -> a.compareTo(b));
        System.out.println("A-Z:        " + dishes);

        int maxLen = 4;
        dishes.removeIf(d -> d.length() > maxLen);
        System.out.println("short ones: " + dishes);

        dishes.forEach(d -> System.out.println("  - " + d));
    }
}'''),
 dict(label="2 · Predict: how many times?", hint="<b>Predict first:</b> how many times does the comparator lambda run while sorting 4 numbers? (It depends on the algorithm and the data.)",
      code='''import java.util.*;

public class Main {
    static int calls = 0;

    public static void main(String[] args) {
        List<Integer> n = new ArrayList<>(List.of(40, 10, 30, 20));
        n.sort((a, b) -> {
            calls++;
            System.out.println("compare " + a + " and " + b);
            return a - b;
        });
        System.out.println(n + " after " + calls + " comparisons");
    }
}'''),
 dict(label="3 · Predict: this in a lambda", hint="<b>Predict first:</b> which <code>name</code> does each line print? A lambda has no <code>this</code> of its own.",
      code='''public class Main {
    String name = "Main object";

    void show() {
        Runnable r = () -> System.out.println("lambda: " + this.name);
        r.run();
    }

    public static void main(String[] args) {
        new Main().show();
    }
}'''),
 dict(label="4 · Crash: exception inside a lambda", hint="The exception happens inside the lambda body, called by forEach. Read the stack trace: it passes through the lambda. Then skip zero with <code>if</code>.",
      code='''import java.util.*;

public class Main {
    public static void main(String[] args) {
        List<Integer> splits = List.of(4, 2, 0, 5);
        int bill = 1000;
        splits.forEach(people -> System.out.println("each pays " + bill / people));
    }
}''', _expect="exception"),
 dict(label="5 · Spot the error", hint="A lambda can't change a local variable it captures. Use an <code>int[] count = {0}</code> or, better, <code>list.size()</code> / a stream count.",
      code='''import java.util.*;

public class Main {
    public static void main(String[] args) {
        List<String> orders = List.of("A1", "B2", "C3");
        int count = 0;
        orders.forEach(o -> count++);
        System.out.println(count);
    }
}''', _expect="compile-error"),
]),
'QUIZ': quiz([
 {"q": "Which is a valid lambda for a method int apply(int x)?", "options": ["x => x * 2", "x -> x * 2", "(x) -> { x * 2 }", "-> x * 2"], "answer": 1, "why": "A block body needs return: (x) -> { return x * 2; }."},
 {"q": "Where can a lambda be used?", "options": ["Anywhere an Object is expected", "Where a functional interface (one abstract method) is expected", "Only with threads", "Only in static methods"], "answer": 1, "why": "The target type must be a functional interface."},
 {"q": "Which local variables can a lambda use?", "options": ["Any", "Only final or effectively final ones", "Only static ones", "None"], "answer": 1, "why": "The lambda captures a copy; changing the variable later would make the copy wrong."},
 {"q": "Inside a lambda, this refers to…", "options": ["the lambda object", "the enclosing object", "null", "the interface"], "answer": 1, "why": "Unlike an anonymous class, a lambda doesn't introduce a new this."},
 {"q": "How does javac compile a lambda body?", "options": ["Into a separate .class file", "Into a private method in the same class, called through invokedynamic", "Into bytecode inside the caller", "It doesn't compile it"], "answer": 1, "why": "Anonymous classes get their own .class file (Main$1); lambdas don't."},
 {"q": "(a, b) -> a - b used with list.sort gives…", "options": ["descending order", "ascending order", "random order", "a compile error"], "answer": 1, "why": "Negative when a < b means a comes first. (For very large ints, prefer Integer.compare to avoid overflow.)"},
 {"q": "Which method removes elements matching a lambda?", "options": ["forEach", "removeIf", "replaceAll", "sort"], "answer": 1, "why": "removeIf takes a Predicate (Lesson 14.2)."},
 {"q": "Can a lambda have no parameters?", "options": ["No", "Yes: () -> ...", "Only if it returns void", "Only with braces"], "answer": 1, "why": "Empty brackets are required when there are no parameters."},
]),
}
