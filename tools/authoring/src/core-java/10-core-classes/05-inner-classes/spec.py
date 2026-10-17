import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../..'))
from mkanim import Anim, two_view

# ---------------- Part 5: two-view animation ----------------
CODE = ['Shop k = new Shop("Kharghar");', "Shop.Bill b1 = k.new Bill(120);", "Shop.Bill b2 = k.new Bill(45);",
        "println(b1.print());", "println(Shop.Tax.gst(120));", "k = null;"]
S = Anim("see", frames=6, h=250, label="Creating a shop, two inner bills, printing, calling a static nested method, then clearing the shop variable")
S.box(8, 8, 344, 132, None, fill="board", stroke="board")
for i, line in enumerate(CODE):
    y = 30 + i * 20
    S.box(12, y - 14, 336, 19, None, fill="none", stroke="track", sw=2, on=str(i + 1), rx=4)
    S.text(20, y, line, mono=True, size=10.2, cls="chalk")
S.box(8, 150, 344, 50, None, fill="card2", stroke="line")
S.text(18, 168, "Console", size=9, cls="ink3", bold=True)
S.text(18, 188, "Kharghar: ₹120", on="4", mono=True, size=11, cls="green", bold=True)
S.text(18, 188, "Kharghar: ₹120   6", on="5-", mono=True, size=11, cls="green", bold=True)
S.note({1: "An ordinary object.", 2: "A bill created FROM the shop.", 3: "A second bill from the same shop.",
        4: "The bill prints its shop's name.", 5: "No object needed for Tax.", 6: "We drop our shop variable."}, y=226, size=10.5)
S.caps(["A <code>Shop</code> object is created as usual.",
        "<code>k.new Bill(120)</code>: the bill is created <i>from</i> shop <code>k</code>.",
        "Another bill from the same shop.",
        "<code>b1.print()</code> shows the shop's name, though <code>Bill</code> has no <code>name</code> field of its own.",
        "<code>Shop.Tax.gst(120)</code> is called on the static nested class directly: no shop, no bill.",
        "We set <code>k</code> to null. Is the shop gone? See the right side."])
B = Anim("behind", frames=6, h=250, label="Heap view: inner Bill objects hold a hidden this$0 reference to their Shop; the static nested call creates nothing")
B.text(56, 18, "Stack (main)", anchor="middle", size=10, bold=True, cls="ink2")
B.text(250, 18, "Heap", anchor="middle", size=10, bold=True, cls="ink2")
B.box(8, 26, 96, 170, None, fill="card", stroke="line")
B.box(116, 26, 236, 170, None, fill="card", stroke="line")
for i, (n, on) in enumerate([("k", "1-5"), ("b1", "2-"), ("b2", "3-")]):
    y = 36 + i * 32
    B.box(14, y, 84, 24, None, fill="soft-blue", stroke="blue", on=on, rx=5)
    B.text(20, y + 16, n, on=on, mono=True, size=10, bold=True)
    B.text(92, y + 16, "→", on=on, mono=True, size=10, anchor="end", cls="blue")
B.box(14, 36, 84, 24, None, fill="card2", stroke="line", on="6", rx=5)
B.text(20, 52, "k  null", on="6", mono=True, size=10, bold=True, cls="ink3")
B.box(220, 34, 124, 44, None, fill="soft-green", stroke="green", on="1-")
B.lines(228, 52, ["Shop", 'name "Kharghar"'], on="1-", mono=True, size=9.5, gap=14)
B.arrow(98, 48, 220, 54, on="1-5", color="blue")
B.box(126, 100, 104, 50, None, fill="soft-acc", stroke="track", on="2-")
B.lines(134, 116, ["Bill  amount 120", "this$0 →"], on="2-", mono=True, size=9, gap=16)
B.box(240, 100, 104, 50, None, fill="soft-acc", stroke="track", on="3-")
B.lines(248, 116, ["Bill  amount 45", "this$0 →"], on="3-", mono=True, size=9, gap=16)
B.arrow(98, 80, 126, 118, on="2-", color="blue")
B.arrow(98, 112, 240, 140, on="3-", color="blue", bend=-14)
B.arrow(190, 130, 250, 78, on="2-", color="track", bend=-10)
B.arrow(300, 130, 296, 78, on="3-", color="track")
B.box(126, 100, 104, 50, None, fill="none", stroke="green", sw=3, on="4")
B.text(234, 172, "this$0.name → \"Kharghar\"", on="4", anchor="middle", size=10, mono=True, cls="green", bold=True)
B.text(234, 172, "Tax.gst(120): no object created", on="5", anchor="middle", size=10, cls="blue", bold=True)
B.text(234, 172, "Shop still reachable via this$0", on="6", anchor="middle", size=10, cls="acc", bold=True)
B.box(220, 34, 124, 44, None, fill="none", stroke="track", sw=3, on="6")
B.note({1: "One Shop object on the heap.", 2: "Bill gets a hidden this$0 link to its shop.", 3: "Both bills point to the same shop.",
        4: "print() reads name through this$0.", 5: "Static nested: a plain static call.", 6: "The bills keep the shop alive."}, y=222, size=10)
B.caps(["<code>k</code> points to a new Shop object holding the name.",
        "javac compiled <code>k.new Bill(120)</code> as <code>new Shop$Bill(k, 120)</code>: the bill stores the shop in its hidden field <code>this$0</code>.",
        "The second bill also points back to the same shop through its own <code>this$0</code>.",
        "Inside <code>print()</code>, <code>name</code> really means <code>this$0.name</code>. That's how an inner object reads its outer object's fields.",
        "<code>Tax</code> is a static nested class: <code>gst</code> is an ordinary static method. No Tax object, no link to any shop.",
        "Even with <code>k</code> null, the Shop object is still reachable through the bills' <code>this$0</code>, so the garbage collector must keep it. Inner objects keep their outer object alive."])
ANIM = two_view("The hidden link from inner to outer", S, B)
BLOCKS = {'ANIM': ANIM}

# ---------------- Part 6: animated example ----------------
ANIM2_HEADING = "Watch it with an example: sorting a cricket leaderboard"
ANIM2_INTRO = "A turf-cricket app sorts batters by runs using an anonymous <code>Comparator</code>. Watch the list ask the anonymous object to compare pairs."
A = Anim("An anonymous Comparator at work", frames=5, h=220, label="Collections.sort calls the anonymous comparator's compare method on pairs of players until sorted by runs")
players = [("Om", 34), ("Riya", 71), ("Kabir", 12)]
A.box(10, 12, 342, 40, None, fill="board", stroke="board")
A.text(20, 30, "list.sort(new Comparator&lt;Player&gt;() {", mono=True, size=9.5, cls="chalk")
A.text(20, 45, "  compare(a, b) { return b.runs - a.runs; } });", mono=True, size=9.5, cls="chalk")
pos = {1: [0, 1, 2], 2: [1, 0, 2], 3: [1, 0, 2], 4: [1, 0, 2], 5: [1, 0, 2]}
for idx, (n, r) in enumerate(players):
    p = {f: f"{(pos[f].index(idx) - idx) * 114},0" for f in pos}
    A.box(14 + idx * 114, 70, 104, 44, f"{n}", sub=f"{r} runs", fill="soft-acc", stroke="track", pos=p, size=10.5, bold=True)
A.box(10, 132, 342, 44, None, fill="soft-blue", stroke="blue")
A.text(181, 150, "Main$1 (anonymous) object", anchor="middle", size=10, bold=True, cls="blue")
A.text(181, 168, "compare(Riya, Om) = 34 − 71 < 0 → Riya first", on="2", anchor="middle", size=9.8, mono=True, cls="ink")
A.text(181, 168, "compare(Kabir, Om) = 34 − 12 > 0 → Kabir after Om", on="3", anchor="middle", size=9.8, mono=True, cls="ink")
A.text(181, 168, "compare(Kabir, Riya) = 71 − 12 > 0 → stays last", on="4", anchor="middle", size=9.8, mono=True, cls="ink")
A.text(181, 168, "waiting to be asked…", on="1", anchor="middle", size=9.8, cls="ink2")
A.text(181, 168, "sorted: Riya 71, Om 34, Kabir 12", on="5", anchor="middle", size=10, bold=True, cls="green")
A.caps(["The app creates an anonymous class object implementing <code>Comparator</code> and hands it to <code>sort</code>. javac named the class <code>Main$1</code>.",
        "<code>sort</code> calls <code>compare(a, b)</code> on the anonymous object. A negative result puts <code>a</code> first. We return <code>b.runs − a.runs</code>, so more runs come first: Riya moves ahead of Om.",
        "Kabir (12) is compared with Om (34): he belongs after Om.",
        "One more comparison confirms Kabir's place at the end.",
        "The leaderboard is sorted by runs, highest first. The rule lived in a class with no name, written exactly where it was needed. (Simplified: the exact comparisons depend on the sorting algorithm.)"])
ANIM2 = A

# ---------------- Part 8: tracer ----------------
TRACE = dict(code='''public class Main {
    private String shop = "Chai Point";

    class Bill {
        int amount;

        Bill(int amount) {
            this.amount = amount;
        }

        String print() {
            return shop + ": Rs " + amount;
        }
    }

    static class Tax {
        static int gst(int amount) {
            return amount * 5 / 100;
        }
    }

    public static void main(String[] args) {
        Main counter = new Main();
        Bill b = counter.new Bill(120);
        int t = Tax.gst(b.amount);
        System.out.println(b.print() + " + GST " + t);
    }
}
''', notes={
 (23, 1): "Outer :: The outer object is created first: its constructor runs and sets the field <code>shop</code>.",
 (23, 2): "Outer :: ",
 (24, 1): "Inner :: = <code>counter.new Bill(120)</code>: a Bill object #4 is created, and javac passes <code>counter</code> to the constructor as a hidden extra argument. For a moment its <code>this$0</code> is still null.",
 7: "Link :: = Before your constructor body runs, javac's code stores the outer object: <code>this$0</code> → #1, the Main object.",
 8: "Set :: ",
 (24, 2): "Inner :: = <code>b</code> points to the Bill. Its hidden <code>this$0</code> field links it to the outer object.",
 (25, 1): "Static nested :: = <code>Tax.gst(…)</code>: a plain static call on the nested class. No Tax object, no outer object involved.",
 (25, 2): "Result :: ",
 (26, 1): "Call :: ",
 12: "Through this$0 :: = <code>shop</code> isn't a Bill field: javac compiled it as <code>this$0.shop</code>, reading the outer object's private field.",
 (26, 2): "Print :: "})

# ---------------- Worked examples ----------------
WORKED_INTRO = "Three designs using each kind of nested class. Watch the heap for <code>this$0</code> and <code>val$…</code>: the hidden fields javac adds."
EXAMPLES = [
dict(tag="Railways · inner class", title="Seats that know their train",
 problem="<p>A <code>Train</code> books seats. Each <code>Seat</code> must print its label as <code>12123/S4-32</code> using the train's number, and every booking increases the train's <code>booked</code> count.</p>",
 inp='Train "12123": book S4-32, S4-33',
 approach=["Make <code>Seat</code> a member inner class, so each seat is tied to one train.",
           "The Seat constructor increments the outer <code>booked</code> field.",
           "<code>label()</code> reads the outer <code>number</code> through the hidden link."],
 code='''class Train {
    private final String number;
    private int booked = 0;

    Train(String number) {
        this.number = number;
    }

    class Seat {
        final String code;

        Seat(String code) {
            this.code = code;
            booked++;
        }

        String label() {
            return number + "/" + code;
        }
    }

    int booked() {
        return booked;
    }
}

public class Main {
    public static void main(String[] args) {
        Train t = new Train("12123");
        Train.Seat a = t.new Seat("S4-32");
        Train.Seat b = t.new Seat("S4-33");
        System.out.println(a.label() + ", " + b.label() + " | booked " + t.booked());
    }
}
''', notes={12: "Link :: = javac's code first stores the outer object: <code>this$0</code> → #1, the train.",
            14: "Outer field :: <code>booked++</code> changes the <b>Train</b> object's field through <code>this$0</code>."},
 tryit="Press <b>Run</b>. Then create a second Train and book a seat on it: its count is separate."),
dict(tag="Restaurant · anonymous class", title="A one-off alert format that captures a variable",
 problem="<p>A kitchen screen needs alerts prefixed with the outlet name, like <code>[Chai Point] Order #12 ready</code>. Write the formatter as an anonymous class of <code>interface Alert</code>, using a local variable for the outlet name.</p>",
 inp='outlet "Chai Point", events "Order #12 ready", "Order #13 ready"',
 approach=["Declare the outlet name as a local variable; it stays effectively final.",
           "Create <code>new Alert() { … }</code>: javac copies the local into the anonymous object (hidden field <code>val$outlet</code>).",
           "Call <code>format</code> for each event."],
 code='''interface Alert {
    String format(String event);
}

public class Main {
    public static void main(String[] args) {
        String outlet = "Chai Point";
        Alert kitchen = new Alert() {
            public String format(String event) {
                return "[" + outlet + "] " + event;
            }
        };
        System.out.println(kitchen.format("Order #12 ready"));
        System.out.println(kitchen.format("Order #13 ready"));
    }
}
''', notes={(8, 1): "Anonymous :: = <code>new Alert() {…}</code> creates an object of a class with no name; javac calls it <code>Main$1</code> (the trace shows Main.1).",
            (8, 3): "Capture :: = <code>kitchen</code> = → #3. Look at #3 on the heap: the object holds <code>val$outlet</code>, a <b>copy</b> of the local variable, so it can use it even after main's frame is gone.",
            (8, 2): "Constructor done :: ",
            (10, 1): "Use the copy :: = <code>outlet</code> here is read from the hidden field <code>val$outlet</code>, not from main's frame."},
 tryit="Press <b>Run</b>. Then add <code>outlet = \"Vashi\";</code> after creating the alert and read the compile error."),
dict(tag="Food delivery · static nested", title="An order built step by step",
 problem="<p>An <code>Order</code> has a customer, an item and optional extras (express delivery, cutlery). Use a static nested <code>Builder</code> so callers can't mix up the arguments, and print the final bill.</p>",
 inp="Riya, Masala Dosa ₹120, express (+₹30)",
 approach=["<code>Order</code> has a private constructor that takes a <code>Builder</code>.",
           "<code>static class Builder</code> collects values with named methods, each returning <code>this</code>.",
           "<code>build()</code> creates the immutable Order."],
 code='''class Order {
    final String customer;
    final int total;

    private Order(Builder b) {
        this.customer = b.customer;
        this.total = b.price + (b.express ? 30 : 0);
    }

    static class Builder {
        private String customer;
        private int price;
        private boolean express;

        Builder customer(String c) {
            customer = c;
            return this;
        }

        Builder item(int p) {
            price = p;
            return this;
        }

        Builder express() {
            express = true;
            return this;
        }

        Order build() {
            return new Order(this);
        }
    }
}

public class Main {
    public static void main(String[] args) {
        Order o = new Order.Builder().customer("Riya").item(120).express().build();
        System.out.println(o.customer + " pays ₹" + o.total);
    }
}
''', notes={(37, 1): "Static nested :: = <code>new Order.Builder()</code>: no Order object exists yet, and none is needed. Look at the heap: the Builder has no <code>this$0</code>."},
 tryit="Press <b>Run</b>. Then add a <code>cutlery()</code> step that adds ₹5."),
]

# ---------------- Practice problems ----------------
PRACTICE_INTRO = "Choose the right kind of nested class and use each one correctly. The last three are business tasks."
PROBLEMS = [
dict(level="easy", title="Create an inner object", stmt="<p>Class <code>College</code> has an inner class <code>Student</code> that prints the college name with the student's name. Create one from <code>main</code>.</p>", inp='College "GES", student "Riya"',
 code='''class College {
    private final String name;
    College(String name) { this.name = name; }

    class Student {
        final String sname;
        Student(String sname) { this.sname = sname; }
        String card() { return sname + " @ " + name; }
    }
}

public class Main {
    public static void main(String[] args) {
        College c = new College("GES Law College");
        College.Student s = c.new Student("Riya");
        System.out.println(s.card());
    }
}''', explain="<p><b>How it works:</b> <code>c.new Student(...)</code> ties the student to college <code>c</code>; <code>card()</code> reads the outer <code>name</code>.</p>"),
dict(level="easy", title="Use a static nested helper", stmt="<p>Put a static nested class <code>Units</code> inside <code>Converter</code> with a method <code>kmToMiles</code>. Convert 42 km.</p>", inp="42 km",
 code='''class Converter {
    static class Units {
        static double kmToMiles(double km) { return km * 0.621371; }
    }
}

public class Main {
    public static void main(String[] args) {
        System.out.printf("%.2f miles%n", Converter.Units.kmToMiles(42));
    }
}''', explain="<p><b>How it works:</b> a static nested class is reached through the outer class name; no objects are needed.</p>"),
dict(level="easy", title="An anonymous greeting", stmt="<p>Implement <code>interface Greeter { String greet(String n); }</code> with an anonymous class that returns <code>Namaste, &lt;name&gt;!</code>.</p>", inp='"Kabir"',
 code='''interface Greeter {
    String greet(String n);
}

public class Main {
    public static void main(String[] args) {
        Greeter g = new Greeter() {
            public String greet(String n) { return "Namaste, " + n + "!"; }
        };
        System.out.println(g.greet("Kabir"));
        System.out.println(g.getClass().getName());
    }
}''', explain="<p><b>How it works:</b> the anonymous class has no source name; javac calls it <code>Main$1</code>, which <code>getClass().getName()</code> shows.</p>"),
dict(level="medium", title="Outer.this for clashing names", stmt="<p>Both <code>Account</code> and its inner class <code>Statement</code> have a field <code>id</code>. Print both from inside <code>Statement</code>.</p>", inp="account id 501, statement id 9",
 code='''class Account {
    int id = 501;

    class Statement {
        int id = 9;
        String header() {
            return "Account " + Account.this.id + ", statement " + id;
        }
    }
}

public class Main {
    public static void main(String[] args) {
        Account a = new Account();
        System.out.println(a.new Statement().header());
    }
}''', explain="<p><b>How it works:</b> plain <code>id</code> is the nearest one (Statement's); <code>Account.this.id</code> names the outer object's field.</p>"),
dict(level="medium", title="Local class with a captured variable", stmt="<p>In a method <code>report(String month, int[] sales)</code>, declare a local class that formats each line using <code>month</code>. Print two lines.</p>", inp='"Oct", {1200, 950}',
 code='''public class Main {
    static void report(String month, int[] sales) {
        class Line {
            String text(int week, int amount) {
                return month + " week " + week + ": ₹" + amount;
            }
        }
        Line l = new Line();
        for (int i = 0; i < sales.length; i++) {
            System.out.println(l.text(i + 1, sales[i]));
        }
    }

    public static void main(String[] args) {
        report("Oct", new int[]{1200, 950});
    }
}''', explain="<p><b>How it works:</b> <code>month</code> is effectively final, so the local class may capture it. The class exists only inside <code>report</code>.</p>"),
dict(level="business", title="Discount rules as anonymous classes", stmt="<p>Apply two discount rules to ₹800: a flat ₹50 off and 15% off. Implement each rule as an anonymous class of <code>interface Rule</code> and print the better price.</p>", inp="₹800",
 code='''interface Rule {
    int apply(int price);
}

public class Main {
    public static void main(String[] args) {
        Rule flat = new Rule() {
            public int apply(int price) { return price - 50; }
        };
        Rule percent = new Rule() {
            public int apply(int price) { return price - price * 15 / 100; }
        };
        int a = flat.apply(800), b = percent.apply(800);
        System.out.println("Flat: ₹" + a + ", 15%: ₹" + b + " → best ₹" + Math.min(a, b));
    }
}''', explain="<p><b>How it works:</b> two anonymous classes (<code>Main$1</code>, <code>Main$2</code>) implement the same interface differently. Callers just call <code>apply</code>.</p>"),
dict(level="business", title="Bank account with an inner transaction log", stmt="<p>A <code>Wallet</code> keeps a list of <code>Txn</code> objects. <code>Txn</code> is an inner class whose constructor updates the wallet's balance. Add ₹500, spend ₹120, and print the balance and log size.</p>", inp="+500, -120",
 code='''import java.util.ArrayList;
import java.util.List;

class Wallet {
    private int balance = 0;
    private final List<Txn> log = new ArrayList<>();

    class Txn {
        final int amount;
        Txn(int amount) {
            this.amount = amount;
            balance += amount;          // outer field
            log.add(this);              // outer list
        }
    }

    void add(int amt) { new Txn(amt); }
    void spend(int amt) { new Txn(-amt); }
    String summary() { return "Balance ₹" + balance + ", " + log.size() + " transactions"; }
}

public class Main {
    public static void main(String[] args) {
        Wallet w = new Wallet();
        w.add(500);
        w.spend(120);
        System.out.println(w.summary());
    }
}''', explain="<p><b>How it works:</b> inside Wallet's own methods, <code>new Txn(...)</code> uses <code>this</code> as the outer object automatically. Each transaction updates the balance and logs itself.</p>"),
dict(level="business", title="Pizza order builder", stmt="<p>Build a large pizza with extra cheese using a static nested <code>Builder</code>. Medium costs ₹249, large ₹399, extra cheese ₹40.</p>", inp="large + cheese",
 code='''class Pizza {
    final String size;
    final int price;

    private Pizza(Builder b) {
        this.size = b.size;
        this.price = b.price;
    }

    static class Builder {
        private String size = "Medium";
        private int price = 249;

        Builder large() { size = "Large"; price = 399; return this; }
        Builder cheese() { price += 40; return this; }
        Pizza build() { return new Pizza(this); }
    }
}

public class Main {
    public static void main(String[] args) {
        Pizza p = new Pizza.Builder().large().cheese().build();
        System.out.println(p.size + " pizza: ₹" + p.price);
    }
}''', explain="<p><b>How it works:</b> the static nested builder can call Pizza's private constructor. Chained methods make each choice readable, and the Pizza itself is immutable.</p>"),
]
