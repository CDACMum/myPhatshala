import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../..'))
from mkanim import Anim, two_view

# ---------------- Part 5: two-view animation ----------------
CODE = ["enum Coach { SL(1.0), AC3(2.5); … }", "Coach c = Coach.AC3;", "Coach d = Coach.AC3;",
        "println(c == d);", "println(c.fare(400));", "Coach[] all = Coach.values();"]
S = Anim("see", frames=6, h=250, label="Using an enum with two constants: reading a constant twice, comparing, calling a method and values()")
S.box(8, 8, 344, 132, None, fill="board", stroke="board")
for i, line in enumerate(CODE):
    y = 30 + i * 20
    S.box(12, y - 14, 336, 19, None, fill="none", stroke="track", sw=2, on=str(i + 1), rx=4)
    S.text(20, y, line, mono=True, size=10.2, cls="chalk")
S.box(8, 150, 344, 50, None, fill="card2", stroke="line")
S.text(18, 168, "Console", size=9, cls="ink3", bold=True)
S.text(18, 188, "true", on="4", mono=True, size=11, cls="green", bold=True)
S.text(18, 188, "true  1000", on="5", mono=True, size=11, cls="green", bold=True)
S.text(18, 188, "true  1000  [SL, AC3]", on="6", mono=True, size=11, cls="green", bold=True)
S.note({1: "Declaring the enum creates nothing yet.", 2: "First use of Coach.", 3: "Use it again.",
        4: "Compare with ==.", 5: "Call a method on the constant.", 6: "Ask for all constants."}, y=226, size=10.5)
S.caps(["The enum is declared with two constants, each passing a fare factor. Nothing runs yet.",
        "<code>Coach.AC3</code> is read for the first time.",
        "<code>Coach.AC3</code> is read again into another variable.",
        "<code>c == d</code> prints <b>true</b>.",
        "<code>c.fare(400)</code> uses AC3's own factor: 400 × 2.5 = 1000.",
        "<code>values()</code> returns all constants in declaration order."])
B = Anim("behind", frames=6, h=250, label="Enum class initialisation creates one object per constant; static fields and variables point to them")
B.text(60, 18, "Coach (static)", anchor="middle", size=10, bold=True, cls="ink2")
B.text(260, 18, "Heap", anchor="middle", size=10, bold=True, cls="ink2")
B.box(8, 26, 104, 92, None, fill="card", stroke="line")
B.box(124, 26, 228, 170, None, fill="card", stroke="line")
B.text(60, 70, "not initialised", on="1", anchor="middle", size=9.5, cls="ink3")
for i, n in enumerate(["SL", "AC3"]):
    y = 36 + i * 36
    B.box(14, y, 92, 26, None, fill="soft-green", stroke="green", on="2-", rx=5)
    B.text(22, y + 17, n, on="2-", mono=True, size=10, bold=True)
    B.text(100, y + 17, "→", on="2-", mono=True, size=10, anchor="end", cls="green")
B.box(136, 34, 100, 54, None, fill="soft-acc", stroke="track", on="2-")
B.lines(144, 50, ['name "SL"', "ordinal 0", "factor 1.0"], on="2-", mono=True, size=9, gap=13)
B.box(244, 34, 100, 54, None, fill="soft-acc", stroke="track", on="2-")
B.lines(252, 50, ['name "AC3"', "ordinal 1", "factor 2.5"], on="2-", mono=True, size=9, gap=13)
B.box(244, 34, 100, 54, None, fill="none", stroke="blue", sw=3, on="3-5")
B.arrow(106, 49, 136, 56, on="2-", color="green")
B.arrow(106, 85, 244, 70, on="2-", color="green", bend=12)
B.text(60, 140, "main frame", anchor="middle", size=9.5, bold=True, cls="ink2", on="2-")
B.box(14, 148, 92, 22, None, fill="soft-blue", stroke="blue", on="2-", rx=5)
B.text(22, 163, "c →", on="2-", mono=True, size=10, bold=True)
B.box(14, 174, 92, 22, None, fill="soft-blue", stroke="blue", on="3-", rx=5)
B.text(22, 189, "d →", on="3-", mono=True, size=10, bold=True)
B.arrow(106, 159, 280, 90, on="2-", color="blue", bend=-20)
B.arrow(106, 185, 300, 90, on="3-", color="blue", bend=-26)
B.box(136, 120, 208, 30, "fare(400): 400 × 2.5 = 1000", fill="card2", stroke="track", on="5", size=9.5, mono=True)
B.box(136, 160, 208, 30, "new array [→SL, →AC3] (a copy)", fill="soft-blue", stroke="blue", on="6", size=9.5, mono=True)
B.note({1: "The enum class isn't initialised until first use.", 2: "Static init: one object per constant.", 3: "d gets the same object, no new one.",
        4: "One object, so == is true.", 5: "The method reads this constant's field.", 6: "values() copies the array of constants."}, y=226, size=10)
B.caps(["Declaring an enum only defines a class. No Coach objects exist until the class is first used.",
        "First use triggers the static initialiser: <code>new Coach(\"SL\", 0, 1.0)</code> and <code>new Coach(\"AC3\", 1, 2.5)</code> are created <b>once</b> and stored in static fields. <code>c</code> gets a reference to AC3.",
        "Reading <code>Coach.AC3</code> again returns the same object. Nothing new is created; enum constructors never run again.",
        "<code>c</code> and <code>d</code> hold the same reference, so <code>==</code> is true. That's why <code>==</code> is the right way to compare enums.",
        "<code>fare</code> runs with <code>this</code> = the AC3 object and uses its <code>factor</code> field, 2.5.",
        "<code>values()</code> returns a fresh copy of the internal array, so no caller can change the real list of constants."])
ANIM = two_view("An enum's constants are created once", S, B)
BLOCKS = {'ANIM': ANIM}

# ---------------- Part 6: animated example ----------------
ANIM2_HEADING = "Watch it with an example: a delivery status page"
ANIM2_INTRO = "A food-delivery order moves through an enum's states. Watch the app call <code>next()</code> and refuse a skip from PLACED straight to DELIVERED."
A = Anim("An order moving through enum states", frames=5, h=220, label="An order status enum advances one state at a time; a skip is refused")
states = ["PLACED", "COOKING", "PICKED_UP", "DELIVERED"]
for k, st in enumerate(states):
    x = 10 + k * 87
    A.box(x, 30, 80, 40, st, fill="card2", stroke="line", size=9, mono=True, bold=True)
    if k < 3: A.arrow(x + 80, 50, x + 87, 50, color="ink", sw=1.5)
for f in range(1, 5):
    x = 10 + (f - 1) * 87
    A.box(x, 30, 80, 40, None, fill="none", stroke="green", sw=3, on=str(f))
A.box(10, 30, 80, 40, None, fill="none", stroke="red", sw=3, on="5")
A.arrow(90, 22, 270, 22, on="5", color="red", dash=True, bend=-8)
A.text(181, 14, "skip?", on="5", anchor="middle", size=9.5, bold=True, cls="red")
A.text(181, 96, "status = status.next();", on="2-4", anchor="middle", mono=True, size=10.5, cls="ink")
A.text(181, 96, "status = Status.PLACED;", on="1", anchor="middle", mono=True, size=10.5, cls="ink")
A.box(10, 110, 342, 46, None, fill="soft-green", stroke="green", on="1-4")
A.text(181, 130, "App shows: Order received", on="1", anchor="middle", size=11, bold=True, cls="green")
A.text(181, 130, "App shows: The restaurant is cooking", on="2", anchor="middle", size=11, bold=True, cls="green")
A.text(181, 130, "App shows: Rider has picked up your food", on="3", anchor="middle", size=11, bold=True, cls="green")
A.text(181, 130, "App shows: Delivered. Enjoy!", on="4", anchor="middle", size=11, bold=True, cls="green")
A.text(181, 148, "label() comes from the constant's own field", on="1-4", anchor="middle", size=9.5, cls="ink2")
A.box(10, 110, 342, 46, None, fill="soft-acc", stroke="red", on="5")
A.text(181, 130, "PLACED.canMoveTo(DELIVERED) → false", on="5", anchor="middle", size=10.5, bold=True, mono=True, cls="red")
A.text(181, 148, "a buggy request to skip ahead is refused", on="5", anchor="middle", size=9.5, cls="red")
A.caps(["A new order starts as <code>Status.PLACED</code>. Its display text comes from the constant's <code>label</code> field.",
        "When the restaurant accepts, the server calls <code>status.next()</code>, which returns the following constant: COOKING.",
        "The rider's app moves it to PICKED_UP, again with <code>next()</code>.",
        "Finally DELIVERED. Every state and its text live in one enum.",
        "If a buggy request tries to set DELIVERED while the order is still PLACED, a method like <code>canMoveTo</code> on the enum refuses it. (Simplified: real apps also record who changed the status and when.)"])
ANIM2 = A

# ---------------- Part 8: tracer ----------------
TRACE = dict(code='''enum Coach {
    SL(1.0), AC3(2.5);

    private final double factor;

    Coach(double factor) {
        this.factor = factor;
    }

    int fare(int base) {
        return (int) (base * factor);
    }
}

public class Main {
    public static void main(String[] args) {
        Coach a = Coach.SL;
        Coach c = Coach.AC3;
        Coach same = Coach.valueOf("AC3");
        System.out.println(c == same);
        int f = c.fare(400);
        System.out.println(c + " fare: " + f + ", ordinal " + c.ordinal());
    }
}
''', notes={
 17: "First use :: = First use of <code>Coach</code>: the JVM ran its static initialiser, which called the constructor once per constant, SL(1.0) and AC3(2.5). <code>a</code> = → #1, the SL object. Look at #1 on the heap: <code>name</code> and <code>ordinal</code> come from <code>java.lang.Enum</code>.",
 18: "Constant :: = <code>c</code> = → the AC3 object, already created during initialisation. No constructor runs now.",
 (19, 1): "valueOf :: = <code>Coach.valueOf(\"AC3\")</code> is called. javac generated this method for the enum, so the trace shows it on line 1, the enum's header.",
 (1, 1): "Generated :: = To look names up, Java builds a name → constant table once, using the generated <code>values()</code> method.",
 (1, 2): "Generated :: = <code>values()</code> returns; the table now knows \"SL\" and \"AC3\".",
 (1, 3): "Generated :: = <code>valueOf</code> finds \"AC3\" in the table and returns that constant.",
 (19, 2): "Result :: = <code>same</code> = → the AC3 object: <b>the same</b> object <code>c</code> points to. No new object was created.",
 20: "Compare :: Same object, so <code>==</code> is true.",
 (21, 1): "Call :: The method runs with <code>this</code> = the AC3 object.",
 11: "Compute :: Reads this constant's own <code>factor</code>: 400 × 2.5.",
 22: "Print :: <code>toString()</code> gives the name; <code>ordinal()</code> gives the position."})

# ---------------- Worked examples ----------------
WORKED_INTRO = "Three business problems where an enum carries the rules. Watch method calls run on the constant objects."
EXAMPLES = [
dict(tag="Railways · fares", title="Total fare for a family booking",
 problem="<p>A family books 2 tickets in AC3 and 1 in SL on a route with a base fare of ₹400. Each coach class multiplies the base fare. Compute the total.</p>",
 inp="AC3 × 2, SL × 1, base ₹400",
 approach=["An enum <code>Coach</code> with a factor per constant and a method <code>fare(base)</code>.",
           "A helper <code>total(Coach[] seats, int base)</code> adds up each seat's fare.",
           "Print the total."],
 code='''enum Coach {
    SL(1.0), AC3(2.5);

    private final double factor;

    Coach(double factor) {
        this.factor = factor;
    }

    int fare(int base) {
        return (int) (base * factor);
    }
}

public class Main {
    static int total(Coach[] seats, int base) {
        int sum = 0;
        for (Coach c : seats) {
            sum += c.fare(base);
        }
        return sum;
    }

    public static void main(String[] args) {
        Coach[] seats = {Coach.AC3, Coach.AC3, Coach.SL};
        System.out.println("Total: ₹" + total(seats, 400));
    }
}
''', notes={25: "Array :: = An array of three references, but only <b>two</b> Coach objects: both AC3 slots point to the same constant."},
 tryit="Press <b>Run</b>. Then add <code>AC2(3.6)</code> and book one AC2 seat."),
dict(tag="Food delivery · states", title="Move an order to its next state",
 problem="<p>An order status enum has PLACED, COOKING, PICKED_UP and DELIVERED. Write <code>next()</code> so each call moves one step forward and DELIVERED stays DELIVERED, then print the journey.</p>",
 inp="start at PLACED",
 approach=["Use <code>ordinal()</code> inside the enum to find the following constant in <code>values()</code>.",
           "Return <code>this</code> for the last state.",
           "Loop in main until DELIVERED."],
 code='''enum Status {
    PLACED, COOKING, PICKED_UP, DELIVERED;

    Status next() {
        Status[] all = values();
        if (ordinal() == all.length - 1) {
            return this;
        }
        return all[ordinal() + 1];
    }
}

public class Main {
    public static void main(String[] args) {
        Status s = Status.PLACED;
        while (s != Status.DELIVERED) {
            s = s.next();
        }
        System.out.println("Final: " + s + " after " + s.ordinal() + " steps");
    }
}
''', notes={(5, 1): "Copy :: = <code>values()</code> is called. Each call returns a <b>new</b> copy of the constants array.",
            (1, 1): "Generated :: = <code>values()</code> was generated by javac (so the trace shows line 1). It clones the enum's hidden <code>$VALUES</code> array.",
            (5, 2): "Copy :: = <code>all</code> now points to the fresh array copy."},
 tryit="Press <b>Run</b>. Then print each status inside the loop to see the whole journey."),
dict(tag="Payments · fees", title="Cheapest payment mode for an amount",
 problem="<p>Each payment mode has a fixed fee and a percentage fee: CARD ₹0 + 2%, NETBANKING ₹10 + 0%, WALLET ₹5 + 1%. For a ₹1500 purchase, find the cheapest mode.</p>",
 inp="₹1500",
 approach=["Enum <code>Mode</code> with two fields and a method <code>fee(amount)</code>.",
           "Start with the first constant as the best, then loop over <code>values()</code>, computing each fee once.",
           "Keep the mode with the smallest fee and print it."],
 code='''enum Mode {
    CARD(0, 2), NETBANKING(10, 0), WALLET(5, 1);

    private final int flat;
    private final int pct;

    Mode(int flat, int pct) {
        this.flat = flat;
        this.pct = pct;
    }

    int fee(int amount) {
        return flat + amount * pct / 100;
    }
}

public class Main {
    public static void main(String[] args) {
        int amount = 1500;
        Mode best = Mode.CARD;
        int bestFee = best.fee(amount);
        for (Mode m : Mode.values()) {
            int fee = m.fee(amount);
            if (fee < bestFee) {
                best = m;
                bestFee = fee;
            }
        }
        System.out.println(best + " fee: ₹" + bestFee);
    }
}
''', tryit="Press <b>Run</b>. Then try an amount of ₹200: which mode wins now?"),
]

# ---------------- Practice problems ----------------
PRACTICE_INTRO = "Declare enums, switch on them and give constants data and behaviour. The last three are business tasks."
PROBLEMS = [
dict(level="easy", title="Print all days with their positions", stmt="<p>Declare <code>enum Day { MON, TUE, WED, THU, FRI, SAT, SUN }</code> and print each day with its ordinal.</p>", inp="(none)",
 code='''enum Day { MON, TUE, WED, THU, FRI, SAT, SUN }

public class Main {
    public static void main(String[] args) {
        for (Day d : Day.values()) {
            System.out.print(d + "=" + d.ordinal() + " ");
        }
        System.out.println();
    }
}''', explain="<p><b>How it works:</b> <code>values()</code> returns the constants in declaration order; <code>ordinal()</code> is the zero-based position.</p>"),
dict(level="easy", title="Weekend or weekday?", stmt="<p>Write <code>isWeekend(Day d)</code> using a switch expression and test SAT and WED.</p>", inp="SAT, WED",
 code='''enum Day { MON, TUE, WED, THU, FRI, SAT, SUN }

public class Main {
    static boolean isWeekend(Day d) {
        return switch (d) {
            case SAT, SUN -> true;
            default -> false;
        };
    }

    public static void main(String[] args) {
        System.out.println("SAT: " + isWeekend(Day.SAT));
        System.out.println("WED: " + isWeekend(Day.WED));
    }
}''', explain="<p><b>How it works:</b> a case can list several constants. <code>default</code> covers the remaining five.</p>"),
dict(level="easy", title="Safe valueOf from user text", stmt="<p>Convert <code>\" medium \"</code> and <code>\"huge\"</code> into <code>Size</code> values. Print <code>MEDIUM</code> for the first and <code>Unknown size: huge</code> for the second.</p>", inp='" medium ", "huge"',
 code='''enum Size { SMALL, MEDIUM, LARGE }

public class Main {
    static void read(String text) {
        try {
            System.out.println(Size.valueOf(text.trim().toUpperCase()));
        } catch (IllegalArgumentException e) {
            System.out.println("Unknown size: " + text.trim());
        }
    }

    public static void main(String[] args) {
        read(" medium ");
        read("huge");
    }
}''', explain="<p><b>How it works:</b> <code>valueOf</code> needs the exact constant name, so normalise first and catch <code>IllegalArgumentException</code> for unknown values.</p>"),
dict(level="medium", title="Planet weights", stmt="<p>An enum <code>Planet</code> has a gravity factor relative to Earth: MERCURY 0.38, EARTH 1.0, JUPITER 2.53. Print the weight of a 60 kg person on each.</p>", inp="60 kg",
 code='''enum Planet {
    MERCURY(0.38), EARTH(1.0), JUPITER(2.53);

    private final double g;

    Planet(double g) { this.g = g; }

    double weight(double kg) { return kg * g; }
}

public class Main {
    public static void main(String[] args) {
        for (Planet p : Planet.values()) {
            System.out.printf("%-8s %.1f kg%n", p, p.weight(60));
        }
    }
}''', explain="<p><b>How it works:</b> each constant passes its own factor to the private constructor; the method uses <code>this</code> constant's field.</p>"),
dict(level="medium", title="Calculator with constant-specific methods", stmt="<p>Make <code>enum Op</code> with PLUS, MINUS and TIMES, each overriding <code>apply(a, b)</code>. Print <code>8 op 2</code> for every op.</p>", inp="8, 2",
 code='''enum Op {
    PLUS  { int apply(int a, int b) { return a + b; } },
    MINUS { int apply(int a, int b) { return a - b; } },
    TIMES { int apply(int a, int b) { return a * b; } };

    abstract int apply(int a, int b);
}

public class Main {
    public static void main(String[] args) {
        for (Op op : Op.values()) {
            System.out.println("8 " + op + " 2 = " + op.apply(8, 2));
        }
    }
}''', explain="<p><b>How it works:</b> the enum declares an abstract method and each constant supplies its own body. javac compiles each body into a small subclass (<code>Op$1</code>, <code>Op$2</code>, …).</p>"),
dict(level="business", title="Count orders by status", stmt="<p>Given statuses of 6 orders, count how many are in each status using an <code>EnumMap</code>, printed in the enum's order.</p>", inp="PACKED, PLACED, SHIPPED, PACKED, DELIVERED, PACKED",
 code='''import java.util.EnumMap;

enum Status { PLACED, PACKED, SHIPPED, DELIVERED }

public class Main {
    public static void main(String[] args) {
        Status[] orders = {Status.PACKED, Status.PLACED, Status.SHIPPED,
                           Status.PACKED, Status.DELIVERED, Status.PACKED};
        EnumMap<Status, Integer> count = new EnumMap<>(Status.class);
        for (Status s : orders) {
            count.put(s, count.getOrDefault(s, 0) + 1);
        }
        System.out.println(count);
    }
}''', explain="<p><b>How it works:</b> an <code>EnumMap</code> is backed by an array indexed by ordinal, so it's fast and always iterates in declaration order.</p>"),
dict(level="business", title="Role-based permissions", stmt="<p>Roles ADMIN, TEACHER and STUDENT each have a set of allowed actions (VIEW, EDIT_MARKS, DELETE_USER). Check whether a TEACHER may EDIT_MARKS and DELETE_USER.</p>", inp="TEACHER: EDIT_MARKS?, DELETE_USER?",
 code='''import java.util.EnumSet;

enum Action { VIEW, EDIT_MARKS, DELETE_USER }

enum Role {
    ADMIN(EnumSet.allOf(Action.class)),
    TEACHER(EnumSet.of(Action.VIEW, Action.EDIT_MARKS)),
    STUDENT(EnumSet.of(Action.VIEW));

    private final EnumSet<Action> allowed;

    Role(EnumSet<Action> allowed) { this.allowed = allowed; }

    boolean can(Action a) { return allowed.contains(a); }
}

public class Main {
    public static void main(String[] args) {
        System.out.println("TEACHER EDIT_MARKS: " + Role.TEACHER.can(Action.EDIT_MARKS));
        System.out.println("TEACHER DELETE_USER: " + Role.TEACHER.can(Action.DELETE_USER));
    }
}''', explain="<p><b>How it works:</b> each role carries its own <code>EnumSet</code> of actions; the permission rule is one method on the enum.</p>"),
dict(level="business", title="GST slab by category", stmt="<p>Product categories have GST rates: ESSENTIAL 5%, STANDARD 18%, LUXURY 28%. Print the final price of ₹1000 items in each category.</p>", inp="₹1000",
 code='''enum Category {
    ESSENTIAL(5), STANDARD(18), LUXURY(28);

    private final int gstPct;

    Category(int gstPct) { this.gstPct = gstPct; }

    int withGst(int price) { return price + price * gstPct / 100; }

    @Override
    public String toString() { return name().charAt(0) + name().substring(1).toLowerCase(); }
}

public class Main {
    public static void main(String[] args) {
        for (Category c : Category.values()) {
            System.out.println(c + ": ₹" + c.withGst(1000));
        }
    }
}''', explain="<p><b>How it works:</b> the rate lives with the category. Overriding <code>toString()</code> gives friendly text, while <code>name()</code> still returns <code>ESSENTIAL</code> for storage. (Simplified: real GST rates are set per HSN code and change by notification.)</p>"),
]
