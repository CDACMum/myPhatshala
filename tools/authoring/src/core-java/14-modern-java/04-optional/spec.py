import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from mkanim import Anim, two_view
from m14 import code, snippet, runner, quiz

def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

# ---------------- Part 5: two-view animation ----------------
S = Anim("see", frames=6, h=250, label="A method that may not find a customer returns an Optional box: either holding the customer or empty, and the caller must deal with both")
S.box(8, 8, 344, 36, None, fill="board", stroke="board")
codes = {1: 'Customer c = findByPhone("98xxx");   // may be null', 2: 'c.getName()   // NullPointerException!',
         3: 'Optional<Customer> c = findByPhone("98xxx");', 4: 'c.map(Customer::name).orElse("Guest")',
         5: 'findByPhone("97xxx")  // not found', 6: '.map(Customer::name).orElse("Guest")'}
for f, c in codes.items():
    S.text(14, 31, esc(c), on=str(f), mono=True, size=9, cls="chalk")
S.box(14, 60, 130, 70, None, fill="card2", stroke="line", on="1-2")
S.text(24, 80, "result", size=9.5, bold=True, cls="ink2", on="1-2")
S.text(24, 108, "null", size=16, bold=True, mono=True, cls="red", on="1-2")
S.text(160, 100, "caller forgot to check →", size=9.6, cls="red", on="2")
S.text(160, 120, "app crashes", size=11, bold=True, cls="red", on="2")
S.box(14, 60, 150, 80, None, fill="soft-green", stroke="green", on="3-4")
S.text(24, 80, "Optional", size=9.5, bold=True, cls="green", on="3-4")
S.box(40, 92, 100, 36, "Customer Asha", fill="card", stroke="line", size=9.4, bold=True, on="3-4")
S.box(14, 60, 150, 80, None, fill="soft-acc", stroke="track", on="5-6")
S.text(24, 80, "Optional (empty)", size=9.5, bold=True, cls="acc", on="5-6")
S.box(40, 92, 100, 36, None, fill="none", stroke="track", on="5-6", rx=6, sw=1.4)
S.text(90, 115, "nothing", size=9, anchor="middle", cls="ink3", on="5-6")
S.arrow(166, 100, 220, 100, on="4", color="green")
S.box(222, 82, 130, 36, "\"Asha\"", fill="soft-green", stroke="green", size=12, bold=True, mono=True, on="4")
S.arrow(166, 100, 220, 100, on="6", color="track")
S.box(222, 82, 130, 36, "\"Guest\"", fill="soft-acc", stroke="track", size=12, bold=True, mono=True, on="6")
S.text(14, 170, "the type itself says: “there may be no result”", size=9.8, cls="ink2", on="3")
S.text(14, 170, "map runs only if a value is inside", size=9.8, cls="green", on="4")
S.text(14, 170, "map is skipped; orElse supplies the fallback", size=9.8, cls="acc", on="6")
S.text(14, 170, "nothing in the method's type warns you", size=9.8, cls="red", on="1")
S.note({1: "A lookup that may return null.", 2: "Forget one check: crash.", 3: "Return an Optional instead.",
        4: "Found: map then use the value.", 5: "Not found: an empty Optional.", 6: "Empty: the fallback is used."}, y=234, size=10.5)
S.caps(["<code>findByPhone</code> returns a Customer, or <code>null</code> if the number isn't registered. The signature doesn't tell callers that.",
        "One caller forgets the null check and calls a method on it: <code>NullPointerException</code> in production.",
        "With <code>Optional&lt;Customer&gt;</code> the return type itself says “maybe”. The value sits inside a box.",
        "<code>map(Customer::name)</code> transforms the value <i>if present</i>; <code>orElse(\"Guest\")</code> unwraps it.",
        "For an unknown number the method returns <code>Optional.empty()</code>: a box with nothing inside, but never null.",
        "<code>map</code> does nothing on an empty box, and <code>orElse</code> gives \"Guest\". Same code path, no if-null, no crash."])

B = Anim("behind", frames=6, h=250, label="Optional on the heap: a small object holding a reference or nothing; Optional.empty is a shared single instance")
B.box(6, 6, 348, 120, None, fill="soft-blue", stroke="blue")
B.text(16, 24, "HEAP", size=10, bold=True, cls="blue")
B.box(16, 36, 150, 44, None, fill="card", stroke="green", on="1-")
B.text(24, 54, "#1 Optional", size=9.2, bold=True, mono=True, on="1-")
B.text(24, 70, "value → #2", size=9, mono=True, on="1-")
B.box(16, 88, 150, 30, None, fill="card", stroke="line", on="1-")
B.text(24, 107, "#2 Customer \"Asha\"", size=9, mono=True, on="1-")
B.arrow(90, 80, 90, 86, on="1-", color="ink")
B.box(188, 36, 156, 44, None, fill="card", stroke="track", on="2-")
B.text(196, 54, "#3 Optional.EMPTY", size=9.2, bold=True, mono=True, on="2-")
B.text(196, 70, "value = null", size=9, mono=True, cls="ink3", on="2-")
B.text(196, 104, "one shared instance", size=8.8, cls="ink2", on="2-")
B.box(6, 136, 348, 72, None, fill="card2", stroke="line")
B.text(16, 154, "call", size=9.5, bold=True, cls="ink2")
calls = {3: ("#1.map(Customer::name)", "→ new #4 Optional[\"Asha\"]"), 4: ("#3.map(Customer::name)", "→ returns #3 (still empty)"),
         5: ("#3.orElse(\"Guest\")", "→ \"Guest\""), 6: ("#3.get()", "→ NoSuchElementException")}
for f, (a, b) in calls.items():
    B.text(16, 176, a, on=str(f), size=9.6, mono=True)
    B.text(16, 196, b, on=str(f), size=9.6, mono=True, cls="red" if f == 6 else "green")
B.text(16, 176, "Optional.of(customer) wraps a reference", size=9.6, on="1")
B.text(16, 176, "Optional.empty() returns the shared empty box", size=9.6, on="2")
B.note({1: "Optional.of: a box around a reference.", 2: "Optional.empty: one shared empty box.", 3: "map on a full box: a new box.",
        4: "map on an empty box: still empty.", 5: "orElse unwraps with a fallback.", 6: "get() on empty throws."}, y=236, size=10.5)
B.caps(["<code>Optional.of(c)</code> creates a small object (#1) whose <code>value</code> field refers to the Customer. It's an extra object, so don't wrap things in hot loops for no reason.",
        "<code>Optional.empty()</code> returns a single shared instance whose value is null. All empty Optionals of any type are that same object.",
        "<code>map</code> on a full box calls your function and wraps the result in a new Optional.",
        "<code>map</code> on the empty box doesn't call your function at all; it returns empty.",
        "<code>orElse</code> returns the value if present, otherwise the fallback.",
        "<code>get()</code> on an empty Optional throws <code>NoSuchElementException: No value present</code>. That's just a different crash, so prefer <code>orElse</code>, <code>orElseGet</code>, <code>orElseThrow</code> or <code>ifPresent</code>."])
ANIM = two_view("Optional: both views", S, B)

# ---------------- Part 6: animated example ----------------
ANIM2_HEADING = "Watch it with an example: applying a coupon that may not exist"
ANIM2_INTRO = "At checkout the app looks up the coupon code the user typed. It might be unknown, or expired. An Optional pipeline handles all cases in one chain."
A = Anim("Coupon lookup with Optional", frames=5, h=230, label="A coupon code is looked up, filtered for expiry and mapped to a discount; missing or expired coupons fall back to zero")
A.box(10, 14, 340, 36, None, fill="board", stroke="board")
A.text(18, 36, esc('find(code).filter(Coupon::valid).map(Coupon::off).orElse(0)'), mono=True, size=9, cls="chalk")
cases = [("SAVE50", "found", "valid ✓", "50", "green", 64), ("OLD20", "found", "expired ✗", "0", "red", 108), ("HELLO", "not found", "—", "0", "red", 152)]
for i, (code_, f1, f2, out, c, y) in enumerate(cases):
    on = f"{i + 2}-"
    A.box(10, y, 70, 32, code_, fill="card2", stroke="line", size=9.4, bold=True, mono=True, on=on)
    A.text(92, y + 20, f1, size=9.2, on=on, cls="ink2")
    A.text(170, y + 20, f2, size=9.2, on=on, cls=c)
    A.box(270, y, 80, 32, "₹" + out + " off", fill="soft-green" if out != "0" else "soft-acc", stroke="green" if out != "0" else "track", size=10, bold=True, on=on)
A.text(10, 80, "Three users type three codes…", size=10, cls="ink2", on="1")
A.text(10, 204, "no null checks, no if-else, no crash", size=10, bold=True, cls="green", on="5")
A.note({1: "One chain for every case.", 2: "Valid coupon: ₹50 off.", 3: "Expired: filter empties it.", 4: "Unknown: empty from the start.", 5: "All cases handled."}, y=222, size=10.5)
A.caps(["<code>find(code)</code> returns <code>Optional&lt;Coupon&gt;</code>; <code>filter</code> keeps it only if valid; <code>map</code> turns it into the discount; <code>orElse(0)</code> gives 0 otherwise.",
        "SAVE50 exists and is valid: the box flows through filter and map, and the user gets ₹50 off.",
        "OLD20 exists but has expired: <code>filter</code> returns an empty Optional, so map is skipped and orElse gives 0.",
        "HELLO doesn't exist: find returns empty, and every step passes the empty box along to orElse.",
        "The same four calls handle all three situations. The app can show “Coupon not valid” when the result is 0. (Illustrative codes.)"])
ANIM2 = A

# ---------------- Part 8: tracer ----------------
TRACE = dict(code='''import java.util.*;

public class Main {
    static Map<String, String> customers = Map.of("98100", "Asha", "98200", "Ravi");

    static Optional<String> findName(String phone) {
        return Optional.ofNullable(customers.get(phone));
    }

    public static void main(String[] args) {
        Optional<String> found = findName("98100");
        Optional<String> missing = findName("99999");
        String greet1 = found.map(n -> "Welcome back, " + n).orElse("Welcome, guest");
        String greet2 = missing.map(n -> "Welcome back, " + n).orElse("Welcome, guest");
        System.out.println(greet1 + " | " + greet2 + " | " + found.isPresent() + " " + missing.isEmpty());
    }
}
''', notes={
 11: "Found :: = <code>findName</code> runs: the map has 98100, so <code>ofNullable</code> wraps \"Asha\" in an Optional object.",
 12: "Missing :: = No customer for 99999: <code>map.get</code> returns null, and <code>ofNullable(null)</code> returns the empty Optional.",
 13: "Full box :: = <code>map</code> calls the lambda with \"Asha\" (watch its frame), wraps the greeting, and <code>orElse</code> unwraps it.",
 14: "Empty box :: = <code>map</code> skips the lambda entirely; <code>orElse</code> returns the fallback.",
 15: "Result :: Both greetings, and the presence checks."})

# ---------------- Worked examples ----------------
WORKED_INTRO = "Three common Optional patterns: a lookup with a default, a chain of optional steps, and failing loudly with <code>orElseThrow</code> when a value is required."
EXAMPLES = [
dict(tag="Telecom · lookup", title="Plan name for a mobile number",
 problem="<p>A telecom app shows the customer's plan for a mobile number. Not every number is registered. Return <code>Optional&lt;String&gt;</code> from the lookup and display “No active plan” when it's empty.</p>",
 inp="numbers 98100 (registered), 97000 (not)",
 approach=["<code>planFor</code> wraps the map lookup with <code>Optional.ofNullable</code>.",
           "The caller uses <code>orElse</code> for the default text.",
           "No null checks in the caller."],
 code='''import java.util.*;

public class Main {
    static Map<String, String> plans = Map.of("98100", "Unlimited 599", "98200", "Data 299");

    static Optional<String> planFor(String number) {
        return Optional.ofNullable(plans.get(number));
    }

    public static void main(String[] args) {
        for (String n : List.of("98100", "97000")) {
            String shown = planFor(n).orElse("No active plan");
            System.out.println(n + ": " + shown);
        }
    }
}
''', notes={(12, 1): "Registered :: = <code>planFor(\"98100\")</code> returns Optional[\"Unlimited 599\"]; orElse unwraps it.",
            (13, 1): "Show :: The plan name.",
            (12, 2): "Unknown :: = <code>plans.get</code> returns null, so an empty Optional comes back; orElse gives the default.",
            (13, 2): "Show :: The fallback text."},
 tryit="Press <b>Run</b>. Then replace <code>orElse</code> with <code>ifPresentOrElse</code> to print a different message for each case."),
dict(tag="Logistics · delivery", title="Delivery city through optional steps",
 problem="<p>An order may have a customer, and a customer may have a saved address. Get the delivery city in upper case, or \"PICKUP\" if any step is missing, without a single null check.</p>",
 inp="order 1 (customer with address in Pune), order 2 (customer without address)",
 approach=["Model optional parts as <code>Optional</code> getters.",
           "Chain with <code>flatMap</code> (the step itself returns an Optional) and <code>map</code> (plain value).",
           "End with <code>orElse(\"PICKUP\")</code>."],
 code='''import java.util.*;

class Address {
    String city;
    Address(String c) { city = c; }
}

class Customer {
    Address address;
    Customer(Address a) { address = a; }
    Optional<Address> address() { return Optional.ofNullable(address); }
}

class Order {
    Customer customer;
    Order(Customer c) { customer = c; }
    Optional<Customer> customer() { return Optional.ofNullable(customer); }
}

public class Main {
    static String deliveryCity(Order o) {
        return o.customer()
                .flatMap(Customer::address)
                .map(a -> a.city.toUpperCase())
                .orElse("PICKUP");
    }

    public static void main(String[] args) {
        Order withAddress = new Order(new Customer(new Address("Pune")));
        Order noAddress = new Order(new Customer(null));
        System.out.println(deliveryCity(withAddress) + ", " + deliveryCity(noAddress));
    }
}
''', notes={29: "Order 1 :: = Order → Customer → Address(\"Pune\").",
            30: "Order 2 :: = A customer with no saved address.",
            31: "Two lookups :: = For order 1 every step has a value: PUNE. For order 2, <code>flatMap(Customer::address)</code> gives empty, so map is skipped: PICKUP."},
 tryit="Press <b>Run</b>. Then use <code>map</code> instead of <code>flatMap</code> on the address step and read the compile error: you'd get <code>Optional&lt;Optional&lt;Address&gt;&gt;</code>."),
dict(tag="Payments · required data", title="Fail fast when a value is required",
 problem="<p>A refund needs the original payment. If the payment id isn't found, the refund must stop with a clear error, not continue with missing data. Use <code>orElseThrow</code>.</p>",
 inp="refund for PAY-1 (exists), PAY-9 (missing)",
 approach=["<code>findPayment</code> returns <code>Optional&lt;Integer&gt;</code> (the amount).",
           "<code>orElseThrow(() -&gt; new IllegalArgumentException(...))</code> unwraps or throws.",
           "The caller catches the exception and reports it."],
 code='''import java.util.*;

public class Main {
    static Map<String, Integer> payments = Map.of("PAY-1", 640, "PAY-2", 1200);

    static Optional<Integer> findPayment(String id) {
        return Optional.ofNullable(payments.get(id));
    }

    static String refund(String id) {
        int amount = findPayment(id)
                .orElseThrow(() -> new IllegalArgumentException("unknown payment " + id));
        return "refunded Rs " + amount + " for " + id;
    }

    public static void main(String[] args) {
        for (String id : List.of("PAY-1", "PAY-9")) {
            try {
                System.out.println(refund(id));
            } catch (IllegalArgumentException e) {
                System.out.println("refund failed: " + e.getMessage());
            }
        }
    }
}
''', notes={(19, 1): "PAY-1 :: = The payment exists: orElseThrow returns 640 and the refund goes ahead.",
            (19, 2): "PAY-9 :: = Not found: the Supplier lambda creates the exception and orElseThrow throws it.",
            (21, 1): "Caught :: The caller reports a clear message instead of refunding ₹0 or crashing with NullPointerException."},
 tryit="Press <b>Run</b>. Then try <code>orElseThrow()</code> with no arguments: it throws <code>NoSuchElementException</code>, a less helpful message."),
]

# ---------------- Practice problems ----------------
PRACTICE_INTRO = "Create Optionals, unwrap them safely, and chain map, filter and flatMap. Every output is fixed. The last three are business tasks."
PROBLEMS = [
dict(level="easy", title="of, empty, ofNullable", stmt="<p>Create an Optional with a value, an empty one, and one from a null reference, and print all three.</p>", inp="(none)",
 code='''import java.util.Optional;

public class Main {
    public static void main(String[] args) {
        String missing = null;
        System.out.println(Optional.of("chai") + " " + Optional.empty() + " " + Optional.ofNullable(missing));
    }
}''', explain="<p><b>How it works:</b> <code>of</code> requires a non-null value (it throws NPE on null); <code>ofNullable</code> accepts null and returns empty.</p>"),
dict(level="easy", title="orElse", stmt="<p>Print the nickname of a user if present, else their full name.</p>", inp="nickname missing",
 code='''import java.util.Optional;

public class Main {
    public static void main(String[] args) {
        Optional<String> nickname = Optional.empty();
        String fullName = "Meenakshi Iyer";
        System.out.println("Hello, " + nickname.orElse(fullName));
    }
}''', explain="<p><b>How it works:</b> orElse returns the value or the given fallback.</p>"),
dict(level="easy", title="ifPresent", stmt="<p>Print an SMS only if a phone number is present. Try with one present and one empty.</p>", inp="98100 / none",
 code='''import java.util.Optional;

public class Main {
    public static void main(String[] args) {
        Optional<String> p1 = Optional.of("98100");
        Optional<String> p2 = Optional.empty();
        p1.ifPresent(n -> System.out.println("SMS sent to " + n));
        p2.ifPresent(n -> System.out.println("SMS sent to " + n));
        System.out.println("done");
    }
}''', explain="<p><b>How it works:</b> the Consumer runs only when a value is present; nothing happens for empty.</p>"),
dict(level="medium", title="orElse vs orElseGet", stmt="<p>Show that <code>orElse</code> evaluates its argument even when a value is present, while <code>orElseGet</code> doesn't.</p>", inp="(none)",
 code='''import java.util.Optional;

public class Main {
    static String loadDefault() {
        System.out.println("  (loading default from server...)");
        return "default";
    }

    public static void main(String[] args) {
        Optional<String> theme = Optional.of("dark");
        System.out.println("orElse:");
        System.out.println(theme.orElse(loadDefault()));
        System.out.println("orElseGet:");
        System.out.println(theme.orElseGet(Main::loadDefault));
    }
}''', explain="<p><b>How it works:</b> <code>orElse(x)</code> receives an already-computed value, so <code>loadDefault()</code> runs first anyway. <code>orElseGet</code> takes a Supplier and calls it only when empty: use it when the fallback is expensive.</p>"),
dict(level="medium", title="map and filter on Optional", stmt="<p>From an optional email, keep it only if it ends with \"@company.in\", and return the part before @, else \"external\".</p>", inp="asha@company.in / ravi@gmail.com",
 code='''import java.util.Optional;

public class Main {
    static String userId(Optional<String> email) {
        return email.filter(e -> e.endsWith("@company.in"))
                    .map(e -> e.substring(0, e.indexOf('@')))
                    .orElse("external");
    }

    public static void main(String[] args) {
        System.out.println(userId(Optional.of("asha@company.in")) + ", " + userId(Optional.of("ravi@gmail.com")));
    }
}''', explain="<p><b>How it works:</b> filter turns a full box empty if the test fails; map transforms only full boxes.</p>"),
dict(level="medium", title="Optional from a stream", stmt="<p>Find the first order above ₹5,000; print it or \"none\". Then find the cheapest order.</p>", inp="450, 1200, 2600",
 code='''import java.util.*;

public class Main {
    public static void main(String[] args) {
        List<Integer> orders = List.of(450, 1200, 2600);
        Optional<Integer> big = orders.stream().filter(o -> o > 5000).findFirst();
        Optional<Integer> cheapest = orders.stream().min(Integer::compare);
        System.out.println("big: " + big.map(String::valueOf).orElse("none") + ", cheapest: " + cheapest.orElse(0));
    }
}''', explain="<p><b>How it works:</b> stream methods that might have no answer (findFirst, min, max, reduce without identity) return Optional.</p>"),
dict(level="business", title="Loyalty points or welcome bonus", stmt="<p>Look up loyalty points by customer id; new customers get a 50-point welcome bonus. Use <code>Optional.ofNullable</code> on a map lookup.</p>", inp="ids C1 (320 points), C9 (new)",
 code='''import java.util.*;

public class Main {
    static Map<String, Integer> points = Map.of("C1", 320, "C2", 75);

    static int pointsFor(String id) {
        return Optional.ofNullable(points.get(id)).orElse(50);
    }

    public static void main(String[] args) {
        System.out.println("C1: " + pointsFor("C1") + ", C9: " + pointsFor("C9"));
    }
}''', explain="<p><b>How it works:</b> wrapping a possibly-null lookup at the boundary keeps nulls from spreading. (For maps alone, <code>getOrDefault</code> does the same job.)</p>"),
dict(level="business", title="Shipping charge rule chain", stmt="<p>An order may have a pincode. If present and it starts with \"4\" (Maharashtra), shipping is ₹0; if present but elsewhere, ₹49; if missing, ask for it.</p>", inp="pincodes 411001, 560001, none",
 code='''import java.util.*;

public class Main {
    static String shipping(Optional<String> pin) {
        return pin.map(p -> p.startsWith("4") ? "free shipping" : "Rs 49 shipping")
                  .orElse("please enter a pincode");
    }

    public static void main(String[] args) {
        System.out.println(shipping(Optional.of("411001")));
        System.out.println(shipping(Optional.of("560001")));
        System.out.println(shipping(Optional.empty()));
    }
}''', explain="<p><b>How it works:</b> map handles the “present” logic, orElse the “missing” case. (Illustrative rule.)</p>"),
dict(level="business", title="Required config value", stmt="<p>An app reads the GST rate from config. If it's missing, startup must fail with a clear message. Show both cases.</p>", inp="config with and without gst.rate",
 code='''import java.util.*;

public class Main {
    static double gstRate(Map<String, String> config) {
        return Optional.ofNullable(config.get("gst.rate"))
                .map(Double::parseDouble)
                .orElseThrow(() -> new IllegalStateException("gst.rate missing in config"));
    }

    public static void main(String[] args) {
        System.out.println("rate: " + gstRate(Map.of("gst.rate", "0.18")));
        try {
            gstRate(Map.of());
        } catch (IllegalStateException e) {
            System.out.println("startup stopped: " + e.getMessage());
        }
    }
}''', explain="<p><b>How it works:</b> failing at startup with a precise message is far better than running with a wrong tax rate. orElseThrow makes “required” explicit.</p>"),
]

# ---------------- Extra blocks ----------------
BLOCKS = {
'ANIM': ANIM,
'CODE_API': snippet('''// create
Optional.of(value)          // value must not be null
Optional.ofNullable(maybe)  // null becomes empty
Optional.empty()
// check and unwrap
opt.isPresent()   opt.isEmpty()
opt.orElse(fallback)        opt.orElseGet(() -> compute())
opt.orElseThrow()           opt.orElseThrow(() -> new XyzException("..."))
opt.ifPresent(v -> ...)     opt.ifPresentOrElse(v -> ..., () -> ...)
// transform (return Optionals)
opt.map(Function)   opt.filter(Predicate)   opt.flatMap(v -> anotherOptional)   opt.or(() -> otherOptional)'''),
'CODE_GET': code('''import java.util.*;

public class Main {
    public static void main(String[] args) {
        Optional<String> coupon = Optional.empty();
        System.out.println("isPresent: " + coupon.isPresent());
        try {
            System.out.println(coupon.get());
        } catch (NoSuchElementException e) {
            System.out.println("get() on empty: " + e.getMessage());
        }
        System.out.println("safe: " + coupon.orElse("no coupon"));
    }
}'''),
'CODE_RUN': code('''import java.util.*;

public class Main {
    static Map<String, String> customers = Map.of("98100", "Asha", "98200", "Ravi");

    static Optional<String> findName(String phone) {
        return Optional.ofNullable(customers.get(phone));
    }

    public static void main(String[] args) {
        for (String phone : List.of("98100", "99999", "98200")) {
            String greeting = findName(phone)
                    .map(name -> "Welcome back, " + name)
                    .orElse("Welcome! Please sign up");
            System.out.println(phone + " -> " + greeting);
        }
        findName("98200").ifPresent(n -> System.out.println("Sending offer to " + n));
        findName("99999").ifPresentOrElse(
                n -> System.out.println("Sending offer to " + n),
                () -> System.out.println("No customer for 99999"));
    }
}'''),
'RUNNER': runner([
 dict(label="1 · Greet by phone number", hint="Press <b>Run</b>. Then add another number to the map, and try <code>orElseThrow</code> for an unknown number.",
      code='''import java.util.*;

public class Main {
    static Map<String, String> customers = Map.of("98100", "Asha", "98200", "Ravi");

    static Optional<String> findName(String phone) {
        return Optional.ofNullable(customers.get(phone));
    }

    public static void main(String[] args) {
        for (String phone : List.of("98100", "99999", "98200")) {
            String greeting = findName(phone)
                    .map(name -> "Welcome back, " + name)
                    .orElse("Welcome! Please sign up");
            System.out.println(phone + " -> " + greeting);
        }
    }
}'''),
 dict(label="2 · Predict: does the fallback run?", hint="<b>Predict first:</b> how many times is “building fallback” printed? Then switch to <code>orElseGet(Main::fallback)</code>.",
      code='''import java.util.Optional;

public class Main {
    static String fallback() {
        System.out.println("building fallback");
        return "Guest";
    }

    public static void main(String[] args) {
        Optional<String> name = Optional.of("Asha");
        System.out.println(name.orElse(fallback()));
        System.out.println(name.orElse(fallback()));
    }
}'''),
 dict(label="3 · Predict: map on empty", hint="<b>Predict first:</b> does the lambda inside <code>map</code> print anything?",
      code='''import java.util.Optional;

public class Main {
    public static void main(String[] args) {
        Optional<Integer> discount = Optional.empty();
        int result = discount.map(d -> {
            System.out.println("calculating with " + d);
            return d * 2;
        }).orElse(0);
        System.out.println("result " + result);
    }
}'''),
 dict(label="4 · Crash: get() on empty", hint="<code>get()</code> on an empty Optional throws. Use <code>orElse</code> or <code>ifPresent</code> instead.",
      code='''import java.util.*;

public class Main {
    public static void main(String[] args) {
        Optional<String> promo = List.of("SAVE10", "FLAT50").stream()
                .filter(c -> c.startsWith("NEW"))
                .findFirst();
        System.out.println("Applying " + promo.get());
    }
}''', _expect="exception"),
 dict(label="5 · Spot the error", hint="The method returns <code>Optional&lt;String&gt;</code>, not <code>String</code>. Unwrap it with <code>orElse(...)</code> first.",
      code='''import java.util.*;

public class Main {
    static Optional<String> nickname(String user) {
        return user.equals("asha") ? Optional.of("Ashu") : Optional.empty();
    }

    public static void main(String[] args) {
        String shown = nickname("ravi");
        System.out.println(shown);
    }
}''', _expect="compile-error"),
]),
'QUIZ': quiz([
 {"q": "What is Optional mainly for?", "options": ["Replacing all null fields", "Return types that may have no result", "Faster code", "Thread safety"], "answer": 1, "why": "It makes 'maybe no value' explicit in a method's signature."},
 {"q": "Optional.of(null) …", "options": ["returns empty", "throws NullPointerException", "returns Optional[null]", "doesn't compile"], "answer": 1, "why": "Use ofNullable when the value may be null."},
 {"q": "Optional.empty().get() throws…", "options": ["NullPointerException", "NoSuchElementException", "IllegalStateException", "nothing"], "answer": 1, "why": "Message: No value present."},
 {"q": "Which never evaluates its fallback when a value is present?", "options": ["orElse(compute())", "orElseGet(() -> compute())", "both", "neither"], "answer": 1, "why": "orElse's argument is evaluated before the call."},
 {"q": "opt.map(f) on an empty Optional…", "options": ["calls f with null", "returns empty without calling f", "throws", "returns Optional[null]"], "answer": 1, "why": "map only runs on a present value."},
 {"q": "When do you use flatMap instead of map?", "options": ["Always", "When the function itself returns an Optional", "For lists only", "For numbers"], "answer": 1, "why": "flatMap avoids Optional<Optional<T>>."},
 {"q": "Which is NOT a recommended use of Optional?", "options": ["Return type of a finder method", "Result of stream.findFirst()", "Method parameter and entity field", "Result of max()"], "answer": 2, "why": "Optional isn't Serializable and adds noise as fields/parameters; use it for return values."},
 {"q": "isPresent() then get() is…", "options": ["the best style", "allowed but usually replaced by map/orElse/ifPresent", "a compile error", "faster than orElse"], "answer": 1, "why": "It's just a null check in disguise."},
]),
}
