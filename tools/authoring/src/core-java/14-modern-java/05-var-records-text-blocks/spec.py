import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from mkanim import Anim, two_view
from m14 import code, snippet, runner, quiz

def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

# ---------------- Part 5: two-view animation ----------------
S = Anim("see", frames=6, h=250, label="A 25-line data class becomes a one-line record; var removes repeated types; a text block replaces escaped string concatenation")
S.box(8, 8, 344, 150, None, fill="board", stroke="board")
views = {
 1: ["final class Order {", "  private final String id;", "  private final int amount;", "  Order(String id, int amount) {...}",
     "  String id() {...}  int amount() {...}", "  equals(...) {...}  hashCode() {...}", "  toString() {...}       // ~25 lines"],
 2: ["record Order(String id, int amount) { }", "", "// constructor, accessors, equals,", "// hashCode, toString: generated"],
 3: ["Map<String, List<Order>> byCity =", "        new HashMap<String, List<Order>>();"],
 4: ["var byCity = new HashMap<String, List<Order>>();", "", "// the type is still HashMap<…>,", "// inferred at compile time"],
 5: ["String json = \"{\\n\" +", "  \"  \\\"id\\\": \\\"A1\\\",\\n\" +", "  \"  \\\"amount\\\": 500\\n\" +", "  \"}\";"],
 6: ["String json = \"\"\"", "    {", "      \"id\": \"A1\",", "      \"amount\": 500", "    }", "    \"\"\";"],
}
for f, ls in views.items():
    for i, l in enumerate(ls):
        if l:
            S.text(18, 30 + i * 18, esc(l), on=str(f), mono=True, size=9, cls="chalk")
labels = {1: ("before: a data class", "red"), 2: ("record: same behaviour", "green"), 3: ("before: type written twice", "red"),
          4: ("var: type written once", "green"), 5: ("before: escapes and +", "red"), 6: ("text block: what you see", "green")}
for f, (t, c) in labels.items():
    S.text(10, 180, t, on=str(f), size=11, bold=True, cls=c)
S.text(10, 204, "Java 16", on="1-2", size=9.6, cls="ink3")
S.text(10, 204, "Java 10", on="3-4", size=9.6, cls="ink3")
S.text(10, 204, "Java 15", on="5-6", size=9.6, cls="ink3")
S.note({1: "A plain data-holder class.", 2: "One line with a record.", 3: "Long generic types, twice.",
        4: "var: let the compiler infer.", 5: "JSON as escaped strings.", 6: "A text block: readable."}, y=234, size=10.5)
S.caps(["A class that only carries data (an order id and amount) needs fields, a constructor, getters, <code>equals</code>, <code>hashCode</code> and <code>toString</code>: about 25 lines of boilerplate.",
        "A <b>record</b> declares the same thing in one line. The compiler generates all of it, and the fields are final: records are <b>immutable</b>.",
        "Long generic types often appear twice in one declaration.",
        "<code>var</code> lets the compiler infer the type of a local variable from its initializer. Java is still statically typed: <code>byCity</code> <i>is</i> a <code>HashMap&lt;String, List&lt;Order&gt;&gt;</code>.",
        "Multi-line text such as JSON, SQL or HTML used to need <code>\\n</code>, escaped quotes and <code>+</code> on every line.",
        "A <b>text block</b> (<code>\"\"\"</code>) keeps the text as you see it: no escapes for quotes, real line breaks, and the common indentation removed."])

B = Anim("behind", frames=6, h=250, label="What the compiler generates for a record and for var: final fields, a canonical constructor, accessors, equals, hashCode and toString")
B.box(6, 6, 200, 200, None, fill="board", stroke="board")
B.text(14, 24, "Order.class (generated)", size=9.2, bold=True, cls="chalk")
gen = ["final class Order extends Record", "  private final String id;", "  private final int amount;", "  Order(String id, int amount)",
       "  String id()   int amount()", "  equals / hashCode / toString"]
for i, l in enumerate(gen):
    B.text(14, 46 + i * 20, esc(l), mono=True, size=8.4, cls="chalk", on=f"{min(i + 1, 4)}-")
B.box(10, 32, 192, 22, None, fill="none", stroke="track", on="1", rx=3)
B.box(10, 52, 192, 42, None, fill="none", stroke="track", on="2", rx=3)
B.box(10, 92, 192, 62, None, fill="none", stroke="track", on="3", rx=3)
B.box(10, 152, 192, 24, None, fill="none", stroke="track", on="4", rx=3)
B.box(218, 6, 136, 120, None, fill="soft-blue", stroke="blue")
B.text(228, 24, "HEAP", size=10, bold=True, cls="blue")
B.box(226, 34, 120, 40, None, fill="card", stroke="line", on="3-")
B.text(232, 52, "#1 Order", size=9, bold=True, mono=True, on="3-")
B.text(232, 68, "id=\"A1\" amount=500", size=7.8, mono=True, on="3-")
B.box(226, 80, 120, 40, None, fill="card", stroke="line", on="5-")
B.text(232, 98, "#2 Order", size=9, bold=True, mono=True, on="5-")
B.text(232, 114, "id=\"A1\" amount=500", size=7.8, mono=True, on="5-")
B.box(218, 134, 136, 72, None, fill="card2", stroke="line")
res = {4: ["o.toString()", "Order[id=A1, amount=500]"], 5: ["o.equals(p)  → true", "o == p       → false"],
       6: ["var o = new Order(...)", "type of o: Order"]}
for f, (a, b) in res.items():
    B.text(226, 156, a, on=str(f), size=8.6, mono=True)
    B.text(226, 176, b, on=str(f), size=8.2, mono=True, cls="green")
B.text(226, 156, "record = class", on="1-3", size=9, cls="ink2")
B.text(226, 176, "with less typing", on="1-3", size=9, cls="ink2")
B.note({1: "A final class extending Record.", 2: "One private final field per component.", 3: "Canonical constructor and accessors.",
        4: "toString is generated.", 5: "equals compares values.", 6: "var: types fixed at compile time."}, y=236, size=10.5)
B.caps(["The compiler turns <code>record Order(String id, int amount)</code> into a <b>final</b> class that extends <code>java.lang.Record</code>. Records can implement interfaces but can't extend other classes.",
        "Each component becomes a <code>private final</code> field. There are no setters: once built, a record never changes.",
        "A <b>canonical constructor</b> takes all components; accessors are named after the components, <code>id()</code> and <code>amount()</code>, not <code>getId()</code>.",
        "<code>toString()</code> prints the name and all components: <code>Order[id=A1, amount=500]</code>.",
        "<code>equals</code> and <code>hashCode</code> compare the component values, so two records with the same data are equal (but still different objects). That makes records safe as HashMap keys.",
        "<code>var</code> generates nothing at run time: the compiler writes the inferred type into the bytecode. Hover over a <code>var</code> in an IDE and you'll see the real type."])
ANIM = two_view("Less boilerplate: both views", S, B)

# ---------------- Part 6: animated example ----------------
ANIM2_HEADING = "Watch it with an example: an order API response built with records and a text block"
ANIM2_INTRO = "An online shop's API turns order records into a JSON response. Records hold the data; a text block holds the JSON template."
A = Anim("Records in, JSON out", frames=5, h=230, label="Order records are created, validated, totalled and formatted into JSON with a text block")
A.box(10, 14, 160, 34, "Order(\"A1\", 450)", fill="soft-green", stroke="green", size=9.4, bold=True, mono=True, on="1-")
A.box(10, 54, 160, 34, "Order(\"A2\", 1200)", fill="soft-green", stroke="green", size=9.4, bold=True, mono=True, on="1-")
A.box(10, 94, 160, 34, "Order(\"A3\", -5)", fill="soft-acc", stroke="red", size=9.4, bold=True, mono=True, on="2")
A.text(10, 146, "compact constructor: amount must be ≥ 0", size=9, cls="red", on="2")
A.text(10, 146, "rejected before it ever existed", size=9, cls="ink3", on="3-")
A.box(186, 14, 166, 60, None, fill="card2", stroke="line", on="3-")
A.text(196, 34, "var total = orders.stream()", size=8.2, mono=True, on="3-")
A.text(196, 50, "  .mapToInt(Order::amount)", size=8.2, mono=True, on="3-")
A.text(196, 66, "  .sum();     // 1650", size=8.2, mono=True, cls="green", on="3-")
A.box(186, 84, 166, 108, None, fill="board", stroke="board", on="4-")
tb = ['"""', '{', '  "orders": %d,', '  "total": %d', '}', '""".formatted(2, total)']
for i, l in enumerate(tb):
    A.text(196, 102 + i * 15, l, size=8.6, mono=True, cls="chalk", on="4-")
A.box(10, 160, 160, 40, None, fill="soft-blue", stroke="blue", on="5")
A.text(20, 176, "{ \"orders\": 2,", size=9, mono=True, on="5")
A.text(20, 192, "  \"total\": 1650 }", size=9, mono=True, on="5")
A.note({1: "Two valid orders as records.", 2: "Invalid data is rejected.", 3: "Total with var and a stream.",
        4: "Fill a text-block template.", 5: "The JSON response."}, y=218, size=10.5)
A.caps(["Each order is a record: id and amount, immutable once created.",
        "A <b>compact constructor</b> in the record validates the amount. <code>new Order(\"A3\", -5)</code> throws, so a bad order can never exist.",
        "<code>var</code> keeps the local declaration short; the stream sums the amounts using the generated accessor <code>Order::amount</code>.",
        "The JSON template is a text block: quotes need no escaping, and <code>formatted</code> fills in the numbers.",
        "The response is ready to send. (Real APIs usually let a library like Jackson turn records into JSON, but text blocks are perfect for SQL, templates and test data.)"])
ANIM2 = A

# ---------------- Part 8: tracer ----------------
TRACE = dict(code='''record Order(String id, int amount) {
    Order {
        if (amount < 0) throw new IllegalArgumentException("negative amount");
    }

    int withGst() {
        return amount * 118 / 100;
    }
}

public class Main {
    public static void main(String[] args) {
        var a = new Order("A1", 500);
        var b = new Order("A1", 500);
        var same = a.equals(b);
        var text = """
                Order %s
                  amount: %d
                  with GST: %d
                """.formatted(a.id(), a.amount(), a.withGst());
        System.out.print(text);
        System.out.println(a + " equals b? " + same + ", same object? " + (a == b));
    }
}
''', notes={
 13: "Record :: = <code>var</code> infers the type Order. The compact constructor runs first (watch it check the amount), then the fields are set.",
 14: "Another :: = A second Order object with the same data.",
 15: "equals :: = The generated equals compares id and amount: true. <code>same</code> is a boolean.",
 16: "Text block :: = A multi-line String. The common indentation is removed; <code>formatted</code> fills the placeholders, calling the accessors and <code>withGst()</code>.",
 21: "Print :: The text block keeps its line breaks.",
 22: "toString :: The generated toString, then equality vs identity."})

# ---------------- Worked examples ----------------
WORKED_INTRO = "Three ways these features make everyday code shorter and safer: a record as an immutable value with validation, records as map keys, and a text block for a formatted receipt."
EXAMPLES = [
dict(tag="Banking · money", title="A Money record that can't go wrong",
 problem="<p>A wallet app passes amounts around as plain ints and sometimes mixes paise with rupees or allows negatives. Create a <code>Money</code> record (paise) that rejects negatives, can add another Money, and prints in rupees.</p>",
 inp="₹120.50 + ₹79.50, and an invalid −₹10",
 approach=["<code>record Money(long paise)</code> with a compact constructor that rejects negatives.",
           "A method <code>plus(Money other)</code> returns a <b>new</b> Money (records are immutable).",
           "Override <code>toString</code> to show rupees."],
 code='''record Money(long paise) {
    Money {
        if (paise < 0) throw new IllegalArgumentException("money can't be negative: " + paise);
    }

    Money plus(Money other) {
        return new Money(paise + other.paise);
    }

    @Override
    public String toString() {
        return String.format("Rs %d.%02d", paise / 100, paise % 100);
    }
}

public class Main {
    public static void main(String[] args) {
        var bill = new Money(12050);
        var tip = new Money(7950);
        var total = bill.plus(tip);
        System.out.println(bill + " + " + tip + " = " + total);
        try {
            new Money(-1000);
        } catch (IllegalArgumentException e) {
            System.out.println("rejected: " + e.getMessage());
        }
    }
}
''', notes={18: "Bill :: = A Money record of 12,050 paise; the compact constructor checked it.",
            19: "Tip :: = Another Money.",
            20: "Add :: = <code>plus</code> creates a third record; bill and tip are unchanged.",
            21: "Print :: The custom toString shows rupees.",
            23: "Invalid :: = The compact constructor throws before the object is created."},
 tryit="Press <b>Run</b>. Then add a <code>minus</code> method: what should happen if the result would be negative?"),
dict(tag="Analytics · grouping", title="Records as map keys",
 problem="<p>A sales report counts orders per (city, month). Instead of building string keys like \"Pune-10\", use a record <code>CityMonth(String city, int month)</code> as the HashMap key.</p>",
 inp="orders: Pune Oct, Pune Oct, Mumbai Oct, Pune Nov",
 approach=["<code>record CityMonth(String city, int month)</code>: equals/hashCode come free.",
           "<code>merge(key, 1, Integer::sum)</code> counts per key.",
           "A new record with the same values finds the same entry."],
 code='''import java.util.*;

record CityMonth(String city, int month) { }

public class Main {
    public static void main(String[] args) {
        var counts = new TreeMap<String, Integer>();
        var byKey = new HashMap<CityMonth, Integer>();
        String[][] orders = {{"Pune", "10"}, {"Pune", "10"}, {"Mumbai", "10"}, {"Pune", "11"}};
        for (var o : orders) {
            var key = new CityMonth(o[0], Integer.parseInt(o[1]));
            byKey.merge(key, 1, Integer::sum);
        }
        for (var e : byKey.entrySet()) counts.put(e.getKey().toString(), e.getValue());
        System.out.println(counts);
        System.out.println("Pune in October: " + byKey.get(new CityMonth("Pune", 10)));
    }
}
''', notes={7: "Sorted view :: A TreeMap used only to print in a stable order.",
            8: "Counts :: = A HashMap keyed by records.",
            (11, 1): "Key :: = A CityMonth record for Pune, October.",
            (12, 1): "Count :: = First time: stored with 1.",
            (11, 2): "Equal key :: = A different object with the same values…",
            (12, 2): "Same entry :: = …finds the same entry, because the generated hashCode and equals use the values. Count becomes 2.",
            16: "Lookup :: A brand-new key object still finds the count: 2."},
 tryit="Press <b>Run</b>. Then change CityMonth into a plain class without equals/hashCode and see the counts break."),
dict(tag="Retail · receipts", title="A formatted receipt with a text block",
 problem="<p>A shop prints a receipt: header, item lines, total and a thank-you line. Build it with a text block template and <code>formatted</code>, using records for the items.</p>",
 inp="2 × Dosa ₹80, 1 × Coffee ₹40",
 approach=["<code>record Item(String name, int qty, int price)</code> with a <code>total()</code> method.",
           "Build the item lines in a loop with <code>String.format</code>.",
           "Insert them into a text block template with <code>formatted</code>."],
 code='''import java.util.*;

record Item(String name, int qty, int price) {
    int total() { return qty * price; }
}

public class Main {
    public static void main(String[] args) {
        var items = List.of(new Item("Dosa", 2, 80), new Item("Coffee", 1, 40));
        var lines = new StringBuilder();
        int sum = 0;
        for (var it : items) {
            lines.append(String.format("%-8s x%d  Rs %4d%n", it.name(), it.qty(), it.total()));
            sum += it.total();
        }
        var receipt = """
                ===== CANTEEN 21 =====
                %s----------------------
                TOTAL          Rs %4d
                Thank you, visit again!
                """.formatted(lines, sum);
        System.out.print(receipt);
    }
}
''', notes={9: "Items :: = Two Item records in an immutable list.",
            10: "Builder :: A StringBuilder collects the item lines.",
            (13, 1): "Line 1 :: = Dosa: 2 × 80 = 160, formatted into fixed-width columns.",
            (13, 2): "Line 2 :: = Coffee: 40.",
            16: "Template :: = The text block keeps the receipt's layout exactly; %s and %d are filled in.",
            22: "Print :: The finished receipt."},
 tryit="Press <b>Run</b>. Then add a GST line to the template and pass the GST amount to <code>formatted</code>."),
]

# ---------------- Practice problems ----------------
PRACTICE_INTRO = "Use <code>var</code>, records and text blocks to write the same programs with less code. Every output is fixed. The last three are business tasks."
PROBLEMS = [
dict(level="easy", title="A simple record", stmt="<p>Declare <code>record Student(String name, int marks)</code>, create one and print it and its marks.</p>", inp="Asha, 88",
 code='''record Student(String name, int marks) { }

public class Main {
    public static void main(String[] args) {
        Student s = new Student("Asha", 88);
        System.out.println(s + " -> marks " + s.marks());
    }
}''', explain="<p><b>How it works:</b> the record gets a constructor, <code>name()</code> and <code>marks()</code> accessors, and a readable toString automatically.</p>"),
dict(level="easy", title="var with collections", stmt="<p>Use <code>var</code> for a list of prices and a loop variable, and print the total.</p>", inp="120, 80, 45",
 code='''import java.util.*;

public class Main {
    public static void main(String[] args) {
        var prices = new ArrayList<>(List.of(120, 80, 45));
        var total = 0;
        for (var p : prices) total += p;
        System.out.println("total " + total + " from a " + prices.getClass().getSimpleName());
    }
}''', explain="<p><b>How it works:</b> <code>prices</code> is an <code>ArrayList&lt;Integer&gt;</code>, <code>total</code> an int, <code>p</code> an Integer: all inferred, all fixed.</p>"),
dict(level="easy", title="A text block", stmt="<p>Print a 3-line address using a text block.</p>", inp="(none)",
 code='''public class Main {
    public static void main(String[] args) {
        String address = """
                MyPhatshala Learning Centre
                12, MG Road
                Pune 411001
                """;
        System.out.print(address);
        System.out.println("lines: " + address.lines().count());
    }
}''', explain="<p><b>How it works:</b> the indentation shared by all lines (and the closing quotes) is removed. The block ends with a line break because the closing <code>\"\"\"</code> is on its own line.</p>"),
dict(level="medium", title="Records are equal by value", stmt="<p>Create two identical <code>Point</code> records and show equals, hashCode and == results; put both in a HashSet and print its size.</p>", inp="(3, 4) twice",
 code='''import java.util.*;

record Point(int x, int y) { }

public class Main {
    public static void main(String[] args) {
        var a = new Point(3, 4);
        var b = new Point(3, 4);
        System.out.println(a.equals(b) + " " + (a.hashCode() == b.hashCode()) + " " + (a == b));
        System.out.println("set size: " + new HashSet<>(List.of(a, b)).size());
    }
}''', explain="<p><b>How it works:</b> records compare by value, so the set treats them as one element. <code>==</code> still compares references.</p>"),
dict(level="medium", title="Compact constructor validation", stmt="<p>A <code>Pincode</code> record must be exactly 6 digits. Validate in a compact constructor and try a good and a bad value.</p>", inp="411001, 41100",
 code='''record Pincode(String value) {
    Pincode {
        if (!value.matches("\\\\d{6}")) throw new IllegalArgumentException("bad pincode: " + value);
    }
}

public class Main {
    public static void main(String[] args) {
        System.out.println(new Pincode("411001"));
        try {
            new Pincode("41100");
        } catch (IllegalArgumentException e) {
            System.out.println(e.getMessage());
        }
    }
}''', explain="<p><b>How it works:</b> a compact constructor has no parameter list; it runs before the fields are assigned. Validating there means an invalid Pincode can't exist anywhere in the program.</p>"),
dict(level="medium", title="Text block with formatted", stmt="<p>Build an SMS from a text block template with name, amount and date placeholders.</p>", inp="Ravi, 1,499, 16-Oct",
 code='''public class Main {
    public static void main(String[] args) {
        String sms = """
                Hi %s, your payment of Rs %,d on %s was successful.
                Ref: %s""".formatted("Ravi", 1499, "16-Oct", "TXN8841");
        System.out.println(sms);
    }
}''', explain="<p><b>How it works:</b> <code>%,d</code> adds thousands separators. With the closing quotes right after the last line, the block has no trailing line break.</p>"),
dict(level="business", title="Invoice lines as records", stmt="<p>Represent invoice lines as records with a <code>lineTotal()</code> method; print each line and the invoice total.</p>", inp="3 lines",
 code='''import java.util.*;

record Line(String item, int qty, int rate) {
    int lineTotal() { return qty * rate; }
}

public class Main {
    public static void main(String[] args) {
        var lines = List.of(new Line("Notebook", 5, 40), new Line("Pen", 10, 10), new Line("Bag", 1, 650));
        var total = 0;
        for (var l : lines) {
            System.out.printf("%-9s %2d x %3d = %4d%n", l.item(), l.qty(), l.rate(), l.lineTotal());
            total += l.lineTotal();
        }
        System.out.println("Invoice total: Rs " + total);
    }
}''', explain="<p><b>How it works:</b> records can have methods; they just can't have extra instance fields or change their components.</p>"),
dict(level="business", title="SQL query as a text block", stmt="<p>Store a readable SQL query in a text block and print it with the city filled in.</p>", inp="city Pune",
 code='''public class Main {
    public static void main(String[] args) {
        String sql = """
                SELECT c.name, SUM(o.amount) AS total
                FROM customers c
                JOIN orders o ON o.customer_id = c.id
                WHERE c.city = '%s'
                GROUP BY c.name
                ORDER BY total DESC""".formatted("Pune");
        System.out.println(sql);
    }
}''', explain="<p><b>How it works:</b> text blocks make embedded SQL readable and easy to copy into a database tool. (In real code, pass values with PreparedStatement parameters instead of formatting them in, to prevent SQL injection.)</p>"),
dict(level="business", title="Immutable config with a record", stmt="<p>Load app settings into a <code>Config</code> record with defaults, and create a modified copy for a test environment (a “wither”).</p>", inp="prod and test",
 code='''record Config(String env, int timeoutSec, boolean sandbox) {
    Config withEnv(String newEnv) {
        return new Config(newEnv, timeoutSec, newEnv.equals("test"));
    }
}

public class Main {
    public static void main(String[] args) {
        var prod = new Config("prod", 30, false);
        var test = prod.withEnv("test");
        System.out.println(prod);
        System.out.println(test);
    }
}''', explain="<p><b>How it works:</b> since records can't change, a “with” method returns a modified copy. Immutable config objects are safe to share across threads.</p>"),
]

# ---------------- Extra blocks ----------------
BLOCKS = {
'ANIM': ANIM,
'CODE_RECORD': code('''record Order(String id, int amount) { }

public class Main {
    public static void main(String[] args) {
        Order a = new Order("A1", 500);
        Order b = new Order("A1", 500);
        System.out.println(a);
        System.out.println("id: " + a.id() + ", amount: " + a.amount());
        System.out.println("equals: " + a.equals(b) + ", same object: " + (a == b));
    }
}'''),
'CODE_VAR': snippet('''var count = 0;                         // int
var name = "Asha";                     // String
var orders = new ArrayList<Order>();   // ArrayList<Order>
for (var o : orders) { ... }           // Order
var x;                 // ✗ no initializer: can't infer
var y = null;          // ✗ null has no type
var z = {1, 2};        // ✗ array initializer needs a type
private var field;     // ✗ only local variables'''),
'CODE_TB': code('''public class Main {
    public static void main(String[] args) {
        String old = "{\\n" +
                     "  \\"item\\": \\"dosa\\",\\n" +
                     "  \\"price\\": 80\\n" +
                     "}";
        String block = """
                {
                  "item": "dosa",
                  "price": 80
                }""";
        System.out.println(block);
        System.out.println("same text? " + old.equals(block));
    }
}'''),
'CODE_RUN': code('''import java.util.*;

record Dish(String name, int price, boolean veg) { }

public class Main {
    public static void main(String[] args) {
        var menu = List.of(new Dish("Paneer Tikka", 220, true), new Dish("Chicken Biryani", 260, false),
                           new Dish("Masala Dosa", 90, true));
        var vegCount = menu.stream().filter(Dish::veg).count();
        var cheapest = menu.stream().min(Comparator.comparingInt(Dish::price)).orElseThrow();
        var card = """
                -- Today's menu --
                dishes: %d (veg: %d)
                cheapest: %s at Rs %d
                """.formatted(menu.size(), vegCount, cheapest.name(), cheapest.price());
        System.out.print(card);
        System.out.println(cheapest);
    }
}'''),
'RUNNER': runner([
 dict(label="1 · Records, var and a text block", hint="Press <b>Run</b>. Then add a dish and a line to the card showing the most expensive dish.",
      code='''import java.util.*;

record Dish(String name, int price, boolean veg) { }

public class Main {
    public static void main(String[] args) {
        var menu = List.of(new Dish("Paneer Tikka", 220, true), new Dish("Chicken Biryani", 260, false),
                           new Dish("Masala Dosa", 90, true));
        var vegCount = menu.stream().filter(Dish::veg).count();
        var card = """
                -- Today's menu --
                dishes: %d (veg: %d)
                """.formatted(menu.size(), vegCount);
        System.out.print(card);
        System.out.println(menu.get(0));
    }
}'''),
 dict(label="2 · Predict: equal records?", hint="<b>Predict first:</b> what do the three comparisons print? Then change the second record's price.",
      code='''record Ticket(String movie, int seat) { }

public class Main {
    public static void main(String[] args) {
        var t1 = new Ticket("Sholay", 14);
        var t2 = new Ticket("Sholay", 14);
        System.out.println(t1.equals(t2));
        System.out.println(t1 == t2);
        System.out.println(t1.hashCode() == t2.hashCode());
    }
}'''),
 dict(label="3 · Predict: what does var become?", hint="<b>Predict first:</b> which class names are printed? <code>var</code> uses the type of the right-hand side.",
      code='''import java.util.*;

public class Main {
    public static void main(String[] args) {
        var a = 10;
        var b = 10.0;
        var c = new ArrayList<String>();
        var d = List.of(1, 2);
        Object[] values = {a, b, c, d};
        for (Object v : values) System.out.println(v.getClass().getSimpleName());
    }
}'''),
 dict(label="4 · Crash: validation in a record", hint="The compact constructor rejects the bad rating. Read the message, then use a rating from 1 to 5.",
      code='''record Review(String dish, int stars) {
    Review {
        if (stars < 1 || stars > 5) throw new IllegalArgumentException("stars must be 1-5, got " + stars);
    }
}

public class Main {
    public static void main(String[] args) {
        System.out.println(new Review("Dosa", 5));
        System.out.println(new Review("Idli", 7));
    }
}''', _expect="exception"),
 dict(label="5 · Spot the error", hint="<code>var</code> needs an initializer to infer the type. Write <code>var total = 0;</code> (or declare <code>int total;</code>).",
      code='''public class Main {
    public static void main(String[] args) {
        var total;
        total = 250 + 180;
        System.out.println(total);
    }
}''', _expect="compile-error"),
]),
'QUIZ': quiz([
 {"q": "What does var do?", "options": ["Makes a variable dynamically typed", "Lets the compiler infer a local variable's static type", "Creates a global variable", "Makes it final"], "answer": 1, "why": "Java stays statically typed; var only saves typing."},
 {"q": "Where can var be used?", "options": ["Fields", "Method parameters", "Local variables with an initializer (and loop variables)", "Return types"], "answer": 2, "why": "Only local variables; the initializer gives the type."},
 {"q": "A record's fields are…", "options": ["public and mutable", "private final", "static", "protected"], "answer": 1, "why": "Records are immutable data carriers."},
 {"q": "For record Order(String id, int amount), the accessor for id is…", "options": ["getId()", "id()", "getid()", "id"], "answer": 1, "why": "Accessors are named after the components."},
 {"q": "Two records with the same component values are…", "options": ["== and equal", "equal but not ==", "neither", "a compile error"], "answer": 1, "why": "Generated equals compares values; == compares references."},
 {"q": "Can a record extend another class?", "options": ["Yes", "No, it implicitly extends java.lang.Record (but can implement interfaces)", "Only abstract classes", "Only other records"], "answer": 1, "why": "Records are final and already extend Record."},
 {"q": "What is a compact constructor?", "options": ["A constructor with no body", "A record constructor without a parameter list, used for validation", "A static factory", "A private constructor"], "answer": 1, "why": "It runs before the fields are assigned from the parameters."},
 {"q": "In a text block, how is indentation handled?", "options": ["Kept exactly", "The common leading whitespace is removed", "All whitespace is removed", "Tabs become spaces"], "answer": 1, "why": "Incidental indentation (shared by all lines and the closing delimiter) is stripped."},
]),
}
