import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../..'))
from mkanim import Anim

ANIM2_HEADING = "Watch it with an example: one pay() name, three ways to pay"
ANIM2_INTRO = "A canteen app has three <code>pay</code> methods. Each call below has different arguments, so javac connects it to a different method before the app ever runs."
A = Anim("pay(…) calls matched to overloads", frames=5, h=226, label="three overloaded pay methods and calls matched by arguments")
sigs = [("pay(int amount)", "cash"), ("pay(int amount, String upiId)", "UPI"), ("pay(int amount, String card, int cvv)", "card")]
for i, (s, k) in enumerate(sigs):
    y = 72 + i * 44
    A.box(110, y, 244, 36, None, fill="card2", stroke="line")
    A.text(120, y + 16, s, mono=True, size=9.5, bold=True)
    A.text(120, y + 30, "→ " + k + " payment", size=9, cls="ink2")
calls = {1: "pay(60)", 2: "pay(60, \"canteen@upi\")", 3: "pay(60, \"4111…\", 123)", 4: "pay(\"60\")", 5: "pay(60, 123)"}
for f, c in calls.items():
    A.box(6, 14, 348, 30, c, on=str(f), fill="board", stroke="board", cls="chalk", mono=True, size=11)
for f, i in {1: 0, 2: 1, 3: 2}.items():
    A.box(110, 72 + i * 44, 244, 36, None, fill="none", stroke="green", sw=3, on=str(f))
    A.arrow(60, 48, 108, 90 + i * 44, on=str(f), color="green")
A.box(6, 72, 96, 124, None, fill="soft-acc", stroke="red", on="4-5")
A.text(54, 100, "✗ no match", anchor="middle", size=10.5, bold=True, cls="red", on="4-5")
A.text(54, 120, "String ≠ int", anchor="middle", size=9.5, mono=True, on="4")
A.text(54, 120, "int ≠ String", anchor="middle", size=9.5, mono=True, on="5")
A.text(54, 140, "compile", anchor="middle", size=9.5, on="4-5")
A.text(54, 154, "error", anchor="middle", size=9.5, on="4-5")
A.text(56, 210, "", size=1)
A.caps([
 "<b>pay(60):</b> one int argument. Only <code>pay(int)</code> has one parameter, so this becomes a cash payment.",
 "<b>pay(60, \"canteen@upi\"):</b> an int and a String: exactly the UPI version.",
 "<b>pay(60, \"4111…\", 123):</b> int, String, int: the card version. Three calls, one name, three different methods.",
 "<b>pay(\"60\"):</b> a String where every version expects an int first. No overload fits, so the code doesn't compile. The mistake is caught before any money moves.",
 "<b>pay(60, 123):</b> two ints. The two-parameter version wants a String second, and an int can't become a String automatically. Compile error again.",
])
ANIM2 = A

TRACE = dict(code='''public class Main {
    static int total(int a, int b) {
        return total(a, b, 0);
    }

    static int total(int a, int b, int c) {
        int sum = a + b + c;
        return sum;
    }

    public static void main(String[] args) {
        int bill = total(10, 25);
        System.out.println("Bill: " + bill);
    }
}
''', notes={
 12: "Call :: javac chose <code>total(int, int)</code> because the call has two int arguments.",
 (3, 1): "Delegate :: The short version calls the full one with a default third value, 0. A second frame named <code>total</code> is pushed, but it is a <b>different method</b>: <code>total(int, int, int)</code>.",
 7: "Add :: The real work happens in one place.",
 8: "Return :: The three-parameter version returns 35.",
 (3, 2): "Return :: The value 35 travels back through the two-parameter version, which returns it unchanged.",
 (12, 2): "Assign :: Back in main, the returned 35 is stored in <code>bill</code>.",
 13: "Print :: ",
}, end='main returns and the program ends. Two frames named total existed at the same time, but they belonged to two different methods.')

WORKED_INTRO = "Three everyday problems where overloading keeps the code short. In each one, the simple versions delegate to a full version, so the real rule is written once. Run each solution, then step through it."
EXAMPLES = [
dict(tag="Mobility · ride fare", title="Fare with and without surge",
 problem="<p>A ride app charges Rs 12 per km. At peak time it multiplies the fare by a surge factor. Write <code>fare(int km)</code> and <code>fare(int km, double surge)</code>, where the first simply calls the second with a surge of 1.0. Print the fare for a 10 km ride at normal time and at 1.5× surge.</p>",
 inp="10 km normal, 10 km at 1.5x surge",
 approach=["Write the full rule once in <code>fare(int km, double surge)</code>: <code>km * 12 * surge</code>.", "<code>fare(int km)</code> returns <code>fare(km, 1.0)</code>.", "javac picks the version from the number of arguments in each call."],
 code='''public class Main {
    static double fare(int km) {
        return fare(km, 1.0);
    }

    static double fare(int km, double surge) {
        double amount = km * 12 * surge;
        return amount;
    }

    public static void main(String[] args) {
        double normal = fare(10);
        double peak = fare(10, 1.5);
        System.out.println("Normal: Rs " + normal);
        System.out.println("Peak: Rs " + peak);
    }
}
''', notes={
 12: "Call :: One argument, so javac compiled this as a call to <code>fare(int)</code>.",
 (3, 1): "Delegate :: <code>fare(int)</code> passes a default surge of 1.0 to the full version.",
 7: "Compute :: 10 × 12 × surge.",
 8: "Return :: ",
 (3, 2): "Return :: The value passes straight back.",
 (12, 2): "Store :: ",
 13: "Call :: Two arguments: this call goes directly to <code>fare(int, double)</code>.",
 14: "Print :: ", 15: "Print :: "},
 tryit="Press <b>Run</b>. Then add <code>fare(int km, double surge, int tip)</code> that adds the tip, and call it with a Rs 20 tip."),
dict(tag="Construction · estimates", title="Area of a room, a plot and a circular tank",
 problem="<p>A builder's estimator needs areas: a square room (one side), a rectangular plot (length and width) and a circular water tank (radius, a double). Write three overloads named <code>area</code> and print each result.</p>",
 inp="square side 4, plot 12 x 9, tank radius 1.5",
 approach=["<code>area(int side)</code> calls <code>area(side, side)</code>: a square is a rectangle.", "<code>area(int l, int w)</code> returns <code>l * w</code>.", "<code>area(double r)</code> uses 3.14 × r × r. The double argument selects it."],
 code='''public class Main {
    static int area(int side) {
        return area(side, side);
    }

    static int area(int l, int w) {
        return l * w;
    }

    static double area(double r) {
        return 3.14 * r * r;
    }

    public static void main(String[] args) {
        int room = area(4);
        int plot = area(12, 9);
        double tank = area(1.5);
        System.out.println("Room: " + room + " sq ft");
        System.out.println("Plot: " + plot + " sq ft");
        System.out.println("Tank: " + tank + " sq m");
    }
}
''', notes={
 15: "Call :: An int argument: <code>area(int)</code> is the exact match (area(double) would also work by widening, but is less specific).",
 (3, 1): "Delegate :: A square is a rectangle with equal sides, so it reuses <code>area(int, int)</code>.",
 7: "Return :: ",
 (3, 2): "Return :: ",
 16: "Call :: Two ints: <code>area(int, int)</code> directly.",
 17: "Call :: 1.5 is a double, so the circle version is chosen.",
 11: "Return :: 3.14 × 1.5 × 1.5.",
 18: "Print :: ", 19: "Print :: ", 20: "Print :: "},
 tryit="Press <b>Run</b>. Then call <code>area(5L)</code> with a long. Which version runs, and why?"),
dict(tag="Retail · invoices", title="Invoice lines for one item or many",
 problem="<p>A shop prints invoice lines. <code>line(String item, int price)</code> is for a single item; <code>line(String item, int price, int qty)</code> is for several. Both must print the same format, so the single-item version calls the other with qty 1.</p>",
 inp="Pen Rs 10 (1 piece), Notebook Rs 45 x 3",
 approach=["Write the formatting once in the three-parameter version.", "The two-parameter version passes qty = 1.", "main calls each version once."],
 code='''public class Main {
    static String line(String item, int price) {
        return line(item, price, 1);
    }

    static String line(String item, int price, int qty) {
        int amount = price * qty;
        return item + " x" + qty + " = Rs " + amount;
    }

    public static void main(String[] args) {
        System.out.println(line("Pen", 10));
        System.out.println(line("Notebook", 45, 3));
    }
}
''', notes={
 12: "Call :: Two arguments: <code>line(String, int)</code>.",
 (3, 1): "Delegate :: qty defaults to 1.",
 7: "Compute :: ",
 8: "Return :: A new String is built and returned.",
 (3, 2): "Return :: ",
 13: "Call :: Three arguments go straight to the full version."},
 tryit="Press <b>Run</b>. Then add an overload <code>line(String item, double price, int qty)</code> for prices with paise, and call it with 12.50."),
]

PRACTICE_INTRO = "Write overloads, predict which one javac chooses, and fix the classic mistakes. The last three are real business tasks."
PROBLEMS = [
dict(level="easy", title="max of two or three", stmt="<p>Write <code>max(int a, int b)</code> and <code>max(int a, int b, int c)</code>. The three-argument version must reuse the two-argument one.</p>",
 inp="max(4, 9), max(7, 2, 5)", code='''public class Main {
    static int max(int a, int b) {
        return a > b ? a : b;
    }

    static int max(int a, int b, int c) {
        return max(max(a, b), c);
    }

    public static void main(String[] args) {
        System.out.println(max(4, 9));
        System.out.println(max(7, 2, 5));
    }
}''', explain="<p><b>How it works:</b> the calls differ in the number of arguments, so javac picks each version from the count alone. Reusing <code>max(a, b)</code> keeps the comparison logic in one place.</p>"),
dict(level="easy", title="Describe any value", stmt="<p>Write three overloads of <code>describe</code> for an <code>int</code>, a <code>double</code> and a <code>String</code>, each printing the type and the value.</p>",
 inp="describe(42), describe(3.5), describe(\"UPI\")", code='''public class Main {
    static void describe(int x)    { System.out.println("int: " + x); }
    static void describe(double x) { System.out.println("double: " + x); }
    static void describe(String x) { System.out.println("String: " + x + " (" + x.length() + " chars)"); }

    public static void main(String[] args) {
        describe(42);
        describe(3.5);
        describe("UPI");
    }
}''', explain="<p><b>How it works:</b> overloading by parameter type. This is exactly how <code>println</code> handles different types.</p>"),
dict(level="easy", title="Predict the choice", stmt="<p>Given <code>show(int)</code> and <code>show(double)</code>, predict what each call prints: a byte, a char, a long and a float.</p>",
 inp="show((byte) 3), show('C'), show(10L), show(2.5f)", code='''public class Main {
    static void show(int x)    { System.out.println(x + " -> int"); }
    static void show(double x) { System.out.println(x + " -> double"); }

    public static void main(String[] args) {
        show((byte) 3);
        show('C');
        show(10L);
        show(2.5f);
    }
}''', explain="<p><b>How it works:</b> byte and char widen to int, and the int version is more specific than double. A long can't narrow to int, and a float can't either, but both widen to double. Note that <code>'C'</code> prints as 67 inside the int version.</p>"),
dict(level="medium", title="Widening, boxing or varargs?", stmt="<p>Three overloads exist: <code>pick(long)</code>, <code>pick(Integer)</code> and <code>pick(int...)</code>. Show which one a call with an int uses, then what happens with an Integer object and with two ints.</p>",
 inp="pick(5), pick(Integer.valueOf(5)), pick(5, 6)", code='''public class Main {
    static void pick(long x)    { System.out.println("long"); }
    static void pick(Integer x) { System.out.println("Integer"); }
    static void pick(int... x)  { System.out.println("varargs (" + x.length + " values)"); }

    public static void main(String[] args) {
        pick(5);
        pick(Integer.valueOf(5));
        pick(5, 6);
    }
}''', explain="<p><b>How it works:</b> <code>pick(5)</code>: phase 1 (widening) already finds <code>pick(long)</code>. <code>pick(Integer.valueOf(5))</code>: an Integer matches <code>pick(Integer)</code> exactly in phase 1. <code>pick(5, 6)</code>: nothing takes two parameters, so only phase 3 (varargs) works.</p>"),
dict(level="medium", title="Fix: overload by return type", stmt="<p>This code doesn't compile: <code>int convert(int x)</code> and <code>double convert(int x)</code>. Rewrite it so one method converts paise to rupees (returns double) and the other doubles an amount, with names or parameters that make the two clearly different.</p>",
 inp="250 paise, Rs 40 doubled", code='''public class Main {
    static double toRupees(int paise) {
        return paise / 100.0;
    }

    static int doubled(int amount) {
        return amount * 2;
    }

    public static void main(String[] args) {
        System.out.println(toRupees(250));
        System.out.println(doubled(40));
    }
}''', explain="<p><b>How it works:</b> two methods with signature <code>convert(int)</code> can't exist together, whatever their return types. Because they do <b>different jobs</b>, the right fix is two descriptive names, not an artificial parameter change.</p>"),
dict(level="business", title="Shipping cost with optional express", stmt="<p>An online store charges Rs 40 plus Rs 10 per kg. Express delivery adds Rs 60. Write <code>shipping(int kg)</code> and <code>shipping(int kg, boolean express)</code>; the first calls the second with <code>false</code>.</p>",
 inp="2 kg normal, 2 kg express, 5 kg normal", code='''public class Main {
    static int shipping(int kg) {
        return shipping(kg, false);
    }

    static int shipping(int kg, boolean express) {
        int cost = 40 + 10 * kg;
        if (express) {
            cost += 60;
        }
        return cost;
    }

    public static void main(String[] args) {
        System.out.println("2 kg: Rs " + shipping(2));
        System.out.println("2 kg express: Rs " + shipping(2, true));
        System.out.println("5 kg: Rs " + shipping(5));
    }
}''', explain="<p><b>How it works:</b> the optional detail (express) has a sensible default. Most callers use the short version; the pricing rule exists only once.</p>"),
dict(level="business", title="Masking a phone number or an account number", stmt="<p>A bank's SMS shows only the last 4 digits. Write <code>mask(long phone)</code> and <code>mask(String accountNo)</code>; the long version converts to a String and calls the String version.</p>",
 inp="phone 9876543210, account \"001234567890\"", code='''public class Main {
    static String mask(String accountNo) {
        int keep = 4;
        String last = accountNo.substring(accountNo.length() - keep);
        return "X".repeat(accountNo.length() - keep) + last;
    }

    static String mask(long phone) {
        return mask(String.valueOf(phone));
    }

    public static void main(String[] args) {
        System.out.println(mask(9876543210L));
        System.out.println(mask("001234567890"));
    }
}''', explain="<p><b>How it works:</b> the phone number needs <code>L</code> because 9876543210 is too big for an int. The long overload converts once and reuses the masking logic. (<code>String.repeat</code> needs Java 11+.)</p>"),
dict(level="business", title="Simple interest with a default rate", stmt="<p>A loan calculator uses 9% per year unless a rate is given. Write <code>interest(int principal, int years)</code> and <code>interest(int principal, int years, double rate)</code>, and print both results for Rs 50,000 over 2 years (default rate and 7.5%).</p>",
 inp="50000 for 2 years; at 9% and at 7.5%", code='''public class Main {
    static final double DEFAULT_RATE = 9.0;

    static double interest(int principal, int years) {
        return interest(principal, years, DEFAULT_RATE);
    }

    static double interest(int principal, int years, double rate) {
        return principal * rate * years / 100;
    }

    public static void main(String[] args) {
        System.out.println("Default 9%: Rs " + interest(50000, 2));
        System.out.println("At 7.5%:   Rs " + interest(50000, 2, 7.5));
    }
}''', explain="<p><b>How it works:</b> simple interest = P × R × T / 100. The default rate lives in a named constant, and the two-argument version passes it on, so changing the default needs one edit.</p>"),
]
