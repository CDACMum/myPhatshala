import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from mkanim import Anim, two_view
from m14 import code, snippet, runner, quiz

def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

# ---------------- Part 5: two-view animation ----------------
S = Anim("see", frames=6, h=250, label="The four core functional interfaces as machines: Predicate tests, Function transforms, Consumer uses, Supplier produces")
S.box(8, 8, 344, 36, None, fill="board", stroke="board")
codes = {1: 'Predicate<Integer> big = amt -> amt > 1000;', 2: 'Function<Integer,Integer> gst = amt -> amt * 118 / 100;',
         3: 'Consumer<String> sms = msg -> send(msg);', 4: 'Supplier<String> orderId = () -> "ORD-" + next();',
         5: 'gst.andThen(a -> a - 50).apply(1000)', 6: '// pick the interface by its shape'}
for f, c in codes.items():
    S.text(14, 31, esc(c), on=str(f), mono=True, size=8.8, cls="chalk")
machines = [(1, "Predicate<T>", "T  →  boolean", "1500 → true", "soft-blue", "blue"),
            (2, "Function<T,R>", "T  →  R", "1000 → 1180", "soft-green", "green"),
            (3, "Consumer<T>", "T  →  (nothing)", "\"Paid\" → SMS sent", "soft-acc", "track"),
            (4, "Supplier<T>", "()  →  T", "→ \"ORD-102\"", "card2", "line")]
for f, name, shape, ex, fill, stroke in machines:
    S.box(70, 64, 220, 92, None, fill=fill, stroke=stroke, on=str(f))
    S.text(180, 92, name, on=str(f), size=13, bold=True, mono=True, anchor="middle")
    S.text(180, 118, shape, on=str(f), size=11, mono=True, anchor="middle", cls="ink2")
    S.text(180, 142, ex, on=str(f), size=10, mono=True, anchor="middle", cls="acc")
S.box(14, 70, 100, 50, "gst", fill="soft-green", stroke="green", on="5", size=11, bold=True, mono=True)
S.box(186, 70, 120, 50, "a -> a - 50", fill="soft-acc", stroke="track", on="5", size=10, bold=True, mono=True)
S.arrow(114, 95, 184, 95, on="5", color="ink")
S.text(14, 150, "1000 → 1180 → 1130", on="5", size=12, mono=True, bold=True, cls="green")
rows = [("test a condition?", "Predicate"), ("turn A into B?", "Function"), ("use it, return nothing?", "Consumer"), ("make one from nothing?", "Supplier")]
for i, (q, a) in enumerate(rows):
    S.text(20, 74 + i * 22, q, on="6", size=10, cls="ink2")
    S.text(220, 74 + i * 22, a, on="6", size=10, mono=True, bold=True)
S.note({1: "Predicate: yes or no.", 2: "Function: transform.", 3: "Consumer: use, return nothing.", 4: "Supplier: produce on demand.",
        5: "Functions can be chained.", 6: "Choose by input and output."}, y=234, size=10.5)
S.caps(["A <b>Predicate</b> takes a value and answers true or false: “is this order above ₹1,000?”. Its method is <code>test</code>.",
        "A <b>Function</b> takes a value and returns another, possibly of a different type: “add 18% GST”. Its method is <code>apply</code>.",
        "A <b>Consumer</b> takes a value and does something with it, returning nothing: “send this SMS”. Its method is <code>accept</code>.",
        "A <b>Supplier</b> takes nothing and produces a value whenever asked: “give me a new order id”. Its method is <code>get</code>.",
        "They come with default methods for combining. <code>andThen</code> runs one function and feeds its result into the next.",
        "You rarely need your own interface: ask what goes in and what comes out, then pick the matching built-in one."])

B = Anim("behind", frames=6, h=250, label="A functional interface has exactly one abstract method; default and static methods don't count; a lambda or method reference supplies the abstract one")
B.box(6, 6, 200, 200, None, fill="board", stroke="board")
lines = ["@FunctionalInterface", "interface Function<T, R> {", "  R apply(T t);  // the SAM",
         "  default <V> Function<T,V>", "    andThen(Function<R,V> after)", "  static <T> Function<T,T>", "    identity()", "}"]
for i, l in enumerate(lines):
    B.text(14, 26 + i * 22, esc(l), mono=True, size=8.6, cls="chalk")
B.box(10, 54, 192, 22, None, fill="none", stroke="green", on="2-", rx=3)
B.box(10, 76, 192, 44, None, fill="none", stroke="track", on="3", rx=3)
B.box(10, 120, 192, 44, None, fill="none", stroke="blue", on="3", rx=3)
B.box(218, 6, 136, 200, None, fill="soft-blue", stroke="blue")
B.text(228, 24, "HEAP", size=10, bold=True, cls="blue")
B.box(226, 36, 120, 44, None, fill="card", stroke="green", on="4-")
B.text(232, 54, "#1 lambda", size=9, bold=True, mono=True, on="4-")
B.text(232, 70, "(Function)", size=8.6, mono=True, cls="ink2", on="4-")
B.box(226, 90, 120, 44, None, fill="card", stroke="track", on="5-")
B.text(232, 108, "#2 method ref", size=9, bold=True, mono=True, on="5-")
B.text(232, 124, "String::length", size=8.6, mono=True, cls="ink2", on="5-")
B.box(226, 144, 120, 54, None, fill="card", stroke="line", on="6")
B.text(232, 162, "#3 andThen", size=9, bold=True, mono=True, on="6")
B.text(232, 178, "holds #1 and", size=8.6, mono=True, cls="ink2", on="6")
B.text(232, 192, "the next fn", size=8.6, mono=True, cls="ink2", on="6")
B.text(14, 196, "counts as functional: 1 abstract", size=8.8, cls="green", on="2")
B.note({1: "An interface from java.util.function.", 2: "Exactly one abstract method.", 3: "Default and static methods are extra.",
        4: "A lambda supplies apply().", 5: "So can a method reference.", 6: "andThen builds a new Function."}, y=236, size=10.5)
B.caps(["This is (simplified) how <code>java.util.function.Function</code> is declared.",
        "It has exactly <b>one abstract method</b>, <code>apply</code>. That's what makes it a functional interface, and what a lambda implements.",
        "<b>Default</b> methods (with a body) and <b>static</b> methods don't count. They give extra abilities like chaining. <code>@FunctionalInterface</code> asks the compiler to check the rule.",
        "Assigning a lambda creates an object (#1) whose <code>apply</code> runs the lambda body.",
        "A <b>method reference</b> such as <code>String::length</code> is a shorthand lambda: it also becomes an object implementing the interface.",
        "Calling <code>andThen</code> returns a <i>new</i> Function object (#3) that remembers both functions and applies them one after the other."])
ANIM = two_view("The four core functional interfaces, both views", S, B)

# ---------------- Part 6: animated example ----------------
ANIM2_HEADING = "Watch it with an example: a checkout pipeline built from small functions"
ANIM2_INTRO = "A shop's checkout applies a coupon, then GST, then rounds the total. Each step is a Function; andThen joins them into one pipeline."
A = Anim("Checkout as a chain of Functions", frames=5, h=230, label="An amount flows through coupon, GST and rounding functions joined with andThen")
steps = [("coupon", "a -> a - 100", 18), ("gst", "a -> a * 1.18", 70), ("round", "Math::round", 122)]
for name, lam, y in steps:
    A.box(100, y, 170, 40, None, fill="soft-green", stroke="green")
    A.text(110, y + 17, name, size=9.6, bold=True, cls="green")
    A.text(110, y + 33, lam, size=9, mono=True)
A.box(10, 30, 70, 30, "₹849", fill="card2", stroke="line", size=11, bold=True, mono=True, on="1")
A.box(10, 30, 70, 30, "₹749", fill="card2", stroke="line", size=11, bold=True, mono=True, on="2")
A.box(10, 82, 70, 30, "₹883.82", fill="card2", stroke="line", size=10, bold=True, mono=True, on="3")
A.box(10, 134, 70, 30, "₹884", fill="soft-green", stroke="green", size=11, bold=True, mono=True, on="4-")
A.arrow(80, 45, 98, 38, on="1", color="ink")
A.arrow(80, 45, 98, 90, on="2", color="ink")
A.arrow(80, 97, 98, 142, on="3", color="ink")
A.box(282, 18, 70, 144, None, fill="board", stroke="board", on="5")
A.text(288, 40, "checkout =", size=8.4, mono=True, cls="chalk", on="5")
A.text(288, 58, "coupon", size=8.4, mono=True, cls="chalk", on="5")
A.text(288, 76, ".andThen(", size=8.4, mono=True, cls="chalk", on="5")
A.text(288, 94, " gst)", size=8.4, mono=True, cls="chalk", on="5")
A.text(288, 112, ".andThen(", size=8.4, mono=True, cls="chalk", on="5")
A.text(288, 130, " round)", size=8.4, mono=True, cls="chalk", on="5")
A.text(10, 186, "the order of steps changes the answer", size=9.6, cls="ink2", on="4")
A.note({1: "Cart total ₹849.", 2: "Coupon: ₹100 off.", 3: "GST 18%.", 4: "Rounded: ₹884.", 5: "One Function built from three."}, y=206, size=10.5)
A.caps(["The cart total is ₹849.",
        "The coupon Function subtracts ₹100: ₹749.",
        "The GST Function multiplies by 1.18: ₹883.82.",
        "Rounding gives ₹884. If GST were applied before the coupon, the customer would pay a different amount, so the order of andThen matters.",
        "<code>coupon.andThen(gst).andThen(round)</code> is itself a Function. The shop can swap or add steps (a festival discount, delivery fee) without touching the others. (Illustrative rules.)"])
ANIM2 = A

# ---------------- Part 8: tracer ----------------
TRACE = dict(code='''import java.util.function.*;

public class Main {
    public static void main(String[] args) {
        Predicate<Integer> bigOrder = amt -> amt > 1000;
        Function<Integer, Integer> addGst = amt -> amt * 118 / 100;
        Consumer<String> notify = msg -> System.out.println("SMS: " + msg);
        Supplier<String> newId = () -> "ORD-" + (100 + 2);
        int amount = 1500;
        if (bigOrder.test(amount)) {
            int total = addGst.apply(amount);
            notify.accept(newId.get() + " total Rs " + total);
        }
    }
}
''', notes={
 5: "Predicate :: = A lambda object implementing <code>Predicate&lt;Integer&gt;</code>; its method is <code>test</code>.",
 6: "Function :: = A Function object; its method is <code>apply</code>.",
 7: "Consumer :: = A Consumer object; its method is <code>accept</code> and it returns nothing.",
 8: "Supplier :: = A Supplier object; its method is <code>get</code> and it takes no arguments.",
 9: "Amount :: The order amount.",
 10: "test :: = <code>bigOrder.test(1500)</code> runs the Predicate's lambda body: true.",
 11: "apply :: = <code>addGst.apply(1500)</code> runs the Function's lambda: 1770.",
 12: "get + accept :: = The Supplier makes the id, then the Consumer prints the SMS."})

# ---------------- Worked examples ----------------
WORKED_INTRO = "Three problems solved by plugging lambdas into the standard interfaces: Predicate rules combined with <code>and</code>/<code>or</code>, a Function pipeline, and method references for everyday conversions."
EXAMPLES = [
dict(tag="Banking · loans", title="Loan eligibility with combined Predicates",
 problem="<p>A bank pre-approves a loan if the applicant earns at least ₹30,000 a month <b>and</b> has a credit score of 700+, <b>or</b> is an existing customer with a score of 750+. Express each rule as a <code>Predicate</code> and combine them.</p>",
 inp="Asha (45000, 720, new), Ravi (25000, 780, existing), Imran (28000, 690, new)",
 approach=["A small <code>Applicant</code> class with income, score and existing flag.",
           "One Predicate per rule; combine with <code>and()</code> and <code>or()</code>.",
           "Test each applicant."],
 code='''import java.util.function.Predicate;

class Applicant {
    String name;
    int income, score;
    boolean existing;
    Applicant(String n, int i, int s, boolean e) { name = n; income = i; score = s; existing = e; }
}

public class Main {
    public static void main(String[] args) {
        Predicate<Applicant> earnsEnough = a -> a.income >= 30000;
        Predicate<Applicant> goodScore = a -> a.score >= 700;
        Predicate<Applicant> loyalHighScore = a -> a.existing && a.score >= 750;
        Predicate<Applicant> eligible = earnsEnough.and(goodScore).or(loyalHighScore);
        Applicant[] people = {new Applicant("Asha", 45000, 720, false),
                              new Applicant("Ravi", 25000, 780, true),
                              new Applicant("Imran", 28000, 690, false)};
        for (Applicant p : people) {
            System.out.println(p.name + ": " + (eligible.test(p) ? "pre-approved" : "not eligible"));
        }
    }
}
''', notes={12: "Rule 1 :: = Income at least 30,000.",
            13: "Rule 2 :: = Score 700 or more.",
            14: "Rule 3 :: = Existing customer with 750+.",
            15: "Combine :: = <code>and</code> and <code>or</code> return new Predicate objects that call the rules. Nothing is tested yet.",
            16: "Applicants :: Three Applicant objects.",
            (20, 1): "Asha :: = Income and score pass: pre-approved.",
            (20, 2): "Ravi :: = Income fails rule 1, but the loyal-customer rule passes.",
            (20, 3): "Imran :: = No rule passes."},
 tryit="Press <b>Run</b>. Then add a rule that rejects anyone with a score below 600, using <code>.and(...)</code> at the end, or <code>.negate()</code>."),
dict(tag="E-commerce · pricing", title="Price pipeline with Function.andThen",
 problem="<p>A marketplace computes a seller's payout: sale price minus 12% commission, minus ₹20 shipping fee, then rounded down to whole rupees. Build it as a chain of Functions and apply it to three sales.</p>",
 inp="sales 999, 1500, 250",
 approach=["Three small Functions: commission, shipping, rounding.",
           "Join them with <code>andThen</code> into one <code>payout</code> Function.",
           "Apply it to each sale."],
 code='''import java.util.function.Function;

public class Main {
    public static void main(String[] args) {
        Function<Double, Double> commission = p -> p * 0.88;
        Function<Double, Double> shipping = p -> p - 20;
        Function<Double, Long> rupees = p -> (long) Math.floor(p);
        Function<Double, Long> payout = commission.andThen(shipping).andThen(rupees);
        double[] sales = {999, 1500, 250};
        for (double s : sales) {
            System.out.println("sale Rs " + (long) s + " -> payout Rs " + payout.apply(s));
        }
    }
}
''', notes={5: "Step 1 :: = Keep 88% (12% commission).",
            6: "Step 2 :: = Subtract the shipping fee.",
            7: "Step 3 :: = Round down to whole rupees: a Function from Double to Long.",
            8: "Pipeline :: = One Function built from three. Its input type is Double and output type Long.",
            (11, 1): "999 :: = 999 × 0.88 = 879.12, − 20 = 859.12, floor → 859.",
            (11, 3): "250 :: = 250 × 0.88 = 220, − 20 = 200."},
 tryit="Press <b>Run</b>. Then use <code>compose</code> instead of the first <code>andThen</code> and predict how the answers change."),
dict(tag="Data · cleanup", title="Method references for everyday conversions",
 problem="<p>A CRM import has messy customer names. Trim them, convert to upper case, skip blanks, and create a <code>Customer</code> for each, using method references instead of lambdas.</p>",
 inp="\"  asha \", \"\", \" ravi\", \"meena  \"",
 approach=["<code>String::trim</code> and <code>String::toUpperCase</code> as Functions.",
           "<code>String::isBlank</code> as a Predicate (negated).",
           "<code>Customer::new</code> as a Function that calls the constructor."],
 code='''import java.util.*;
import java.util.function.*;

class Customer {
    String name;
    Customer(String name) { this.name = name; }
}

public class Main {
    public static void main(String[] args) {
        Function<String, String> clean = ((Function<String, String>) String::trim).andThen(String::toUpperCase);
        Predicate<String> blank = String::isBlank;
        Function<String, Customer> create = Customer::new;
        List<Customer> customers = new ArrayList<>();
        for (String raw : List.of("  asha ", "", " ravi", "meena  ")) {
            if (blank.negate().test(raw)) {
                customers.add(create.apply(clean.apply(raw)));
            }
        }
        for (Customer c : customers) System.out.println("[" + c.name + "]");
    }
}
''', notes={11: "Clean :: = <code>String::trim</code> then <code>String::toUpperCase</code>: unbound method references, called on the input string.",
            12: "Blank :: = A Predicate that calls <code>raw.isBlank()</code>.",
            13: "Create :: = A constructor reference: <code>create.apply(x)</code> means <code>new Customer(x)</code>.",
            (16, 1): "Not blank :: = \"  asha \" is not blank.",
            (17, 1): "Make :: = Cleaned to \"ASHA\" and a Customer is created.",
            (16, 2): "Skip :: = The empty string is blank, so it's skipped.",
            20: "Result :: Three clean customers."},
 tryit="Press <b>Run</b>. Then replace each method reference with the equivalent lambda (e.g. <code>s -> s.trim()</code>) and check the output is identical."),
]

# ---------------- Practice problems ----------------
PRACTICE_INTRO = "Pick the right built-in interface, write it as a lambda or method reference, and combine with default methods. Outputs are fixed. The last three are business tasks."
PROBLEMS = [
dict(level="easy", title="Predicate: is it even?", stmt="<p>Write a <code>Predicate&lt;Integer&gt;</code> that checks for even numbers and test 4 and 7.</p>", inp="4, 7",
 code='''import java.util.function.Predicate;

public class Main {
    public static void main(String[] args) {
        Predicate<Integer> even = n -> n % 2 == 0;
        System.out.println(even.test(4) + " " + even.test(7));
    }
}''', explain="<p><b>How it works:</b> Predicate's single method is <code>boolean test(T t)</code>.</p>"),
dict(level="easy", title="Function: name length", stmt="<p>Use <code>Function&lt;String,Integer&gt;</code> with a method reference to get the length of \"Nagpur\".</p>", inp="Nagpur",
 code='''import java.util.function.Function;

public class Main {
    public static void main(String[] args) {
        Function<String, Integer> len = String::length;
        System.out.println(len.apply("Nagpur"));
    }
}''', explain="<p><b>How it works:</b> <code>String::length</code> is the same as <code>s -&gt; s.length()</code>: the input becomes the object the method is called on.</p>"),
dict(level="easy", title="Supplier and Consumer", stmt="<p>A Supplier gives today's greeting; a Consumer prints it with a prefix.</p>", inp="(none)",
 code='''import java.util.function.*;

public class Main {
    public static void main(String[] args) {
        Supplier<String> greeting = () -> "Good morning";
        Consumer<String> show = s -> System.out.println(">> " + s);
        show.accept(greeting.get());
    }
}''', explain="<p><b>How it works:</b> Supplier: nothing in, value out (<code>get</code>). Consumer: value in, nothing out (<code>accept</code>).</p>"),
dict(level="medium", title="andThen vs compose", stmt="<p>With <code>gst = p -&gt; p * 118 / 100</code> and <code>off = p -&gt; p - 50</code>, print <code>gst.andThen(off)</code> and <code>gst.compose(off)</code> for 1000.</p>", inp="1000",
 code='''import java.util.function.Function;

public class Main {
    public static void main(String[] args) {
        Function<Integer, Integer> gst = p -> p * 118 / 100;
        Function<Integer, Integer> off = p -> p - 50;
        System.out.println("gst then off: " + gst.andThen(off).apply(1000));
        System.out.println("off then gst: " + gst.compose(off).apply(1000));
    }
}''', explain="<p><b>How it works:</b> <code>f.andThen(g)</code> = g(f(x)); <code>f.compose(g)</code> = f(g(x)). Discount before tax gives a smaller bill.</p>"),
dict(level="medium", title="BiFunction and BinaryOperator", stmt="<p>Use a <code>BiFunction&lt;Integer,Integer,Integer&gt;</code> for the bill of qty × price, and a <code>BinaryOperator&lt;Integer&gt;</code> (<code>Integer::max</code>) to find the larger of two bills.</p>", inp="3 × 120, 2 × 199",
 code='''import java.util.function.*;

public class Main {
    public static void main(String[] args) {
        BiFunction<Integer, Integer, Integer> bill = (qty, price) -> qty * price;
        BinaryOperator<Integer> larger = Integer::max;
        int a = bill.apply(3, 120), b = bill.apply(2, 199);
        System.out.println(a + " vs " + b + " -> larger " + larger.apply(a, b));
    }
}''', explain="<p><b>How it works:</b> Bi- versions take two arguments. BinaryOperator&lt;T&gt; is a BiFunction whose inputs and output are all the same type.</p>"),
dict(level="medium", title="Your own @FunctionalInterface", stmt="<p>Declare <code>@FunctionalInterface interface Converter { double convert(double inr); }</code> and use it for USD and EUR rates.</p>", inp="₹1000; rates 0.012, 0.011",
 code='''@FunctionalInterface
interface Converter {
    double convert(double inr);
}

public class Main {
    public static void main(String[] args) {
        Converter toUsd = inr -> inr * 0.012;
        Converter toEur = inr -> inr * 0.011;
        System.out.printf("USD %.2f, EUR %.2f%n", toUsd.convert(1000), toEur.convert(1000));
    }
}''', explain="<p><b>How it works:</b> a custom interface gives a domain name to the behaviour. The annotation makes the compiler reject a second abstract method. (Illustrative rates.)</p>"),
dict(level="business", title="Coupon validity rules", stmt="<p>A coupon applies if the cart is ₹499+ and the user is new, or if it's a weekend. Combine Predicates on a <code>Cart</code> and test three carts.</p>", inp="3 carts",
 code='''import java.util.function.Predicate;

class Cart {
    int total;
    boolean newUser, weekend;
    Cart(int t, boolean n, boolean w) { total = t; newUser = n; weekend = w; }
}

public class Main {
    public static void main(String[] args) {
        Predicate<Cart> bigCart = c -> c.total >= 499;
        Predicate<Cart> newUser = c -> c.newUser;
        Predicate<Cart> weekend = c -> c.weekend;
        Predicate<Cart> applies = bigCart.and(newUser).or(weekend);
        Cart[] carts = {new Cart(650, true, false), new Cart(300, true, false), new Cart(120, false, true)};
        for (Cart c : carts) System.out.println("Rs " + c.total + ": " + (applies.test(c) ? "coupon OK" : "no coupon"));
    }
}''', explain="<p><b>How it works:</b> business rules as small named Predicates are easy to read, test and change one at a time.</p>"),
dict(level="business", title="Order id generator", stmt="<p>Write a <code>Supplier&lt;String&gt;</code> that returns ids ORD-1001, ORD-1002… each time it's called. Generate three.</p>", inp="(none)",
 code='''import java.util.concurrent.atomic.AtomicInteger;
import java.util.function.Supplier;

public class Main {
    public static void main(String[] args) {
        AtomicInteger counter = new AtomicInteger(1000);
        Supplier<String> nextId = () -> "ORD-" + counter.incrementAndGet();
        for (int i = 0; i < 3; i++) System.out.println(nextId.get());
    }
}''', explain="<p><b>How it works:</b> the lambda can't change a captured int, but it can call methods on a captured object. AtomicInteger also makes the generator safe if many threads call it.</p>"),
dict(level="business", title="Notification fan-out with Consumer.andThen", stmt="<p>When a payment succeeds, send an SMS, then an email, then write an audit log, using one combined Consumer.</p>", inp="payment PAY-77, Rs 640",
 code='''import java.util.function.Consumer;

public class Main {
    public static void main(String[] args) {
        Consumer<String> sms = p -> System.out.println("SMS sent for " + p);
        Consumer<String> email = p -> System.out.println("Email sent for " + p);
        Consumer<String> audit = p -> System.out.println("Audit: " + p + " logged");
        Consumer<String> onSuccess = sms.andThen(email).andThen(audit);
        onSuccess.accept("PAY-77 Rs 640");
    }
}''', explain="<p><b>How it works:</b> <code>Consumer.andThen</code> calls each consumer in order with the same input. Adding a WhatsApp message later is one more <code>andThen</code>.</p>"),
]

# ---------------- Extra blocks ----------------
BLOCKS = {
'ANIM': ANIM,
'CODE_TABLE': snippet('''Predicate<T>          boolean test(T t)        filter, validate        n -> n > 0
Function<T,R>         R apply(T t)             transform, convert      s -> s.length()
Consumer<T>           void accept(T t)         print, save, send       s -> System.out.println(s)
Supplier<T>           T get()                  create, generate        () -> new ArrayList<>()
BiFunction<T,U,R>     R apply(T t, U u)        combine two values      (q, p) -> q * p
UnaryOperator<T>      T apply(T t)             same type in and out    s -> s.trim()
BinaryOperator<T>     T apply(T a, T b)        reduce two to one       (a, b) -> a + b
IntPredicate, IntFunction, ToIntFunction ...   primitive versions (no boxing)''', lang='text', file='java.util.function'),
'CODE_REFS': code('''import java.util.*;
import java.util.function.*;

public class Main {
    static boolean isValidPin(String pin) {
        return pin.matches("\\\\d{6}");
    }

    public static void main(String[] args) {
        Predicate<String> staticRef = Main::isValidPin;            // 1. static method
        String shop = "MyShop";
        Supplier<Integer> boundRef = shop::length;                 // 2. method of a particular object
        Function<String, String> unboundRef = String::toUpperCase;  // 3. method of the argument
        Supplier<List<String>> ctorRef = ArrayList::new;           // 4. constructor

        System.out.println(staticRef.test("411001") + " " + boundRef.get() + " "
                + unboundRef.apply("pune") + " " + ctorRef.get());
    }
}'''),
'CODE_RUN': code('''import java.util.*;
import java.util.function.*;

public class Main {
    public static void main(String[] args) {
        List<Integer> orders = List.of(450, 1200, 80, 2600, 999);

        Predicate<Integer> bigOrder = amt -> amt >= 1000;
        Function<Integer, String> label = amt -> "Rs " + amt + (bigOrder.test(amt) ? " (free delivery)" : "");
        Consumer<String> print = System.out::println;
        Supplier<String> header = () -> "Today's orders:";

        print.accept(header.get());
        for (int amt : orders) {
            print.accept(label.apply(amt));
        }
        long big = orders.stream().filter(bigOrder).count();
        print.accept(big + " orders get free delivery");
    }
}'''),
'RUNNER': runner([
 dict(label="1 · All four interfaces", hint="Press <b>Run</b>. Then change the free-delivery limit, and make <code>label</code> show amounts with GST.",
      code='''import java.util.*;
import java.util.function.*;

public class Main {
    public static void main(String[] args) {
        List<Integer> orders = List.of(450, 1200, 80, 2600, 999);

        Predicate<Integer> bigOrder = amt -> amt >= 1000;
        Function<Integer, String> label = amt -> "Rs " + amt + (bigOrder.test(amt) ? " (free delivery)" : "");
        Consumer<String> print = System.out::println;
        Supplier<String> header = () -> "Today's orders:";

        print.accept(header.get());
        for (int amt : orders) {
            print.accept(label.apply(amt));
        }
    }
}'''),
 dict(label="2 · Predict: andThen or compose?", hint="<b>Predict first:</b> what do the two lines print for 1000? Then swap the functions.",
      code='''import java.util.function.Function;

public class Main {
    public static void main(String[] args) {
        Function<Integer, Integer> doubleIt = x -> x * 2;
        Function<Integer, Integer> plus10 = x -> x + 10;
        System.out.println(doubleIt.andThen(plus10).apply(1000));
        System.out.println(doubleIt.compose(plus10).apply(1000));
    }
}'''),
 dict(label="3 · Predict: negate and or", hint="<b>Predict first:</b> which words pass the filter?",
      code='''import java.util.List;
import java.util.function.Predicate;

public class Main {
    public static void main(String[] args) {
        Predicate<String> shortWord = w -> w.length() <= 4;
        Predicate<String> startsP = w -> w.startsWith("P");
        Predicate<String> rule = shortWord.negate().or(startsP);
        for (String w : List.of("Pune", "Goa", "Delhi", "Agra", "Patna")) {
            System.out.println(w + " -> " + rule.test(w));
        }
    }
}'''),
 dict(label="4 · Crash: a Supplier that returns null", hint="The Supplier returns <code>null</code>, and the next step calls a method on it. Make the Supplier return <code>\"\"</code>, or check for null (Lesson 14.4 shows a better way).",
      code='''import java.util.function.*;

public class Main {
    public static void main(String[] args) {
        Supplier<String> couponFromServer = () -> null;
        Function<String, String> normalise = String::toUpperCase;
        System.out.println("coupon: " + normalise.apply(couponFromServer.get()));
    }
}''', _expect="exception"),
 dict(label="5 · Spot the error", hint="<code>@FunctionalInterface</code> allows only one abstract method. Remove one, or give it a body with <code>default</code>.",
      code='''@FunctionalInterface
interface Tax {
    double rate();
    double cess();
}

public class Main {
    public static void main(String[] args) {
        Tax gst = () -> 0.18;
        System.out.println(gst.rate());
    }
}''', _expect="compile-error"),
]),
'QUIZ': quiz([
 {"q": "A functional interface has…", "options": ["no methods", "exactly one abstract method", "only default methods", "exactly one method of any kind"], "answer": 1, "why": "Default and static methods don't count; methods from Object (like equals) don't either."},
 {"q": "Which interface fits 'given an Order, return its total'?", "options": ["Predicate<Order>", "Function<Order, Integer>", "Consumer<Order>", "Supplier<Order>"], "answer": 1, "why": "One input, one output of a different type."},
 {"q": "Which interface fits 'create a new empty cart'?", "options": ["Supplier<Cart>", "Consumer<Cart>", "Predicate<Cart>", "Function<Cart,Cart>"], "answer": 0, "why": "No input, one output."},
 {"q": "What is Consumer's abstract method?", "options": ["get()", "apply(T)", "accept(T)", "test(T)"], "answer": 2, "why": "accept returns void."},
 {"q": "f.andThen(g).apply(x) equals…", "options": ["f(g(x))", "g(f(x))", "f(x) + g(x)", "g(x)"], "answer": 1, "why": "andThen applies f first; compose applies the argument function first."},
 {"q": "What does @FunctionalInterface do?", "options": ["Makes the interface faster", "Makes the compiler check there is exactly one abstract method", "Is required for lambdas", "Adds default methods"], "answer": 1, "why": "It's optional but documents intent and catches mistakes."},
 {"q": "String::toUpperCase used as Function<String,String> means…", "options": ["s -> String.toUpperCase()", "s -> s.toUpperCase()", "() -> toUpperCase()", "It doesn't compile"], "answer": 1, "why": "An unbound method reference: the argument becomes the object."},
 {"q": "Why do IntPredicate and IntFunction exist?", "options": ["For older Java", "To avoid boxing int into Integer", "They're faster to write", "For threads"], "answer": 1, "why": "Primitive specialisations avoid creating Integer objects."},
]),
}
