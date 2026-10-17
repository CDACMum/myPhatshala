import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../..'))
from mkanim import Anim

ANIM2_HEADING = "Watch it with an example: String.format fills a receipt"
ANIM2_INTRO = "<code>String.format(String format, Object... args)</code> is a varargs method from the JDK. Watch the values you pass become an <code>Object[]</code>, and each <code>%</code> placeholder take the next one."
A = Anim("String.format(\"%s paid Rs %d via %s\", \"Riya\", 60, \"UPI\")", frames=6, h=224, label="string format with varargs object array")
A.box(6, 14, 348, 30, None, fill="board", stroke="board")
A.text(14, 34, "\"%s paid Rs %d via %s\"", mono=True, size=11, cls="kw")
ph = [(19, "%s"), (91.5, "%d"), (137.7, "%s")]
A.text(10, 70, "args (Object[3], made by javac)", size=10, bold=True, cls="ink2", on="2-")
vals = ["\"Riya\"", "60 → Integer", "\"UPI\""]
for i, v in enumerate(vals):
    A.box(10 + i * 116, 78, 108, 32, v, on="2-", fill="soft-blue", stroke="blue", mono=True, size=10)
    A.text(64 + i * 116, 124, f"[{i}]", on="2-", anchor="middle", mono=True, size=9.5, cls="ink2")
for k, (x, p) in enumerate(ph):
    A.box(x - 2, 20, 17, 20, None, fill="none", stroke="track", sw=2.5, on=str(k + 3), rx=4)
    A.box(10 + k * 116, 78, 108, 32, None, fill="none", stroke="track", sw=3, on=str(k + 3))
A.box(10, 142, 340, 34, None, fill="soft-green", stroke="green", on="3-")
A.text(20, 164, "Riya", on="3", mono=True, size=11, bold=True)
A.text(20, 164, "Riya paid Rs 60", on="4", mono=True, size=11, bold=True)
A.text(20, 164, "Riya paid Rs 60 via UPI", on="5-", mono=True, size=11, bold=True)
A.text(180, 200, "1 method, any number of values", anchor="middle", on="6", size=10.5, bold=True, cls="green")
A.text(180, 200, "the call has 4 arguments: format + 3 values", anchor="middle", on="1", size=10.5)
A.caps([
 "<b>The call:</b> one format string and three values. <code>format</code> is declared with <code>Object... args</code>, so any number of values is allowed.",
 "<b>Packing:</b> javac builds <code>new Object[]{\"Riya\", 60, \"UPI\"}</code>. The int 60 is boxed into an <code>Integer</code>, because the array holds Objects.",
 "<b>First placeholder:</b> <code>%s</code> takes <code>args[0]</code> and prints it as text: Riya.",
 "<b>Second:</b> <code>%d</code> takes <code>args[1]</code> as a whole number: 60.",
 "<b>Third:</b> the last <code>%s</code> takes <code>args[2]</code>: UPI.",
 "<b>Result:</b> “Riya paid Rs 60 via UPI”. Receipt texts, SMS templates and report lines are built this way. Pass too few values and you get a <code>MissingFormatArgumentException</code> at run time.",
])
ANIM2 = A

TRACE = dict(code='''public class Main {
    static double average(String student, int... marks) {
        int sum = 0;
        for (int m : marks) {
            sum += m;
        }
        return (double) sum / marks.length;
    }

    public static void main(String[] args) {
        double a = average("Riya", 80, 90, 70);
        System.out.println("Riya's average: " + a);
    }
}
''', notes={
 (11, 1): "Call :: javac turned this call into <code>average(\"Riya\", new int[]{80, 90, 70})</code>. The new array is on the heap, and <code>marks</code> refers to it.",
 (4, 1): "Loop :: <code>marks</code> is an ordinary int[], so a for-each loop walks through it.",
 7: "Return :: 240 / 3 as a double. <code>marks.length</code> is 3 because three values were passed.",
 (11, 2): "Result :: ",
 12: "Print :: "}, end='main returns. The int[3] created for the call is no longer referenced and will be garbage-collected.')

WORKED_INTRO = "Three business tasks where the number of values changes from call to call. In each trace, look for the array that javac creates on the heap for the varargs parameter."
EXAMPLES = [
dict(tag="Food delivery · bills", title="Order total with a delivery fee",
 problem="<p>An order has a fixed delivery fee and any number of item prices. Write <code>orderTotal(int deliveryFee, int... items)</code> and print the total for an order of three items with a Rs 30 fee.</p>",
 inp="delivery fee 30, items 120, 80, 45",
 approach=["The fixed parameter (fee) comes first, the varargs (items) last.", "Start the total at the fee, then add every item.", "The call <code>orderTotal(30, 120, 80, 45)</code> creates an int[3] for the items."],
 code='''public class Main {
    static int orderTotal(int deliveryFee, int... items) {
        int total = deliveryFee;
        for (int price : items) {
            total += price;
        }
        return total;
    }

    public static void main(String[] args) {
        int bill = orderTotal(30, 120, 80, 45);
        System.out.println("Pay Rs " + bill);
    }
}
''', notes={(11, 1): "Call :: 30 goes to <code>deliveryFee</code>; the other three values are packed into a new int[3] for <code>items</code>.",
 3: "Start :: The total starts with the delivery fee.", (11, 2): "Result :: ", 12: "Print :: "},
 tryit="Press <b>Run</b>. Then call <code>orderTotal(30)</code> with no items. What does the method receive?"),
dict(tag="Analytics · ratings", title="Highest rating, at least one required",
 problem="<p>A product page shows the best rating. Write <code>best(int first, int... rest)</code> so that calling it without any rating is a compile error, and print the best of 4, 5, 3 and 5.</p>",
 inp="ratings 4, 5, 3, 5",
 approach=["Make the first rating a normal parameter: <code>best()</code> then won't compile.", "Start with <code>first</code> as the best so far.", "Loop over <code>rest</code> and keep the larger value."],
 code='''public class Main {
    static int best(int first, int... rest) {
        int max = first;
        for (int r : rest) {
            if (r > max) {
                max = r;
            }
        }
        return max;
    }

    public static void main(String[] args) {
        int top = best(4, 5, 3, 5);
        System.out.println("Best rating: " + top + " stars");
    }
}
''', notes={(13, 1): "Call :: 4 is <code>first</code>; 5, 3, 5 go into a new int[3] for <code>rest</code>.",
 3: "Start :: The first rating is the best so far.", (13, 2): "Result :: ", 14: "Print :: "},
 tryit="Press <b>Run</b>. Then try <code>best()</code> with no arguments and read the compile error."),
dict(tag="Security · access", title="Does the user have any of these roles?",
 problem="<p>An admin panel lets a user in if they have <b>any</b> of the allowed roles. Write <code>hasAnyRole(String userRole, String... allowed)</code> and check a user with role \"OPS\" against \"ADMIN\", \"OPS\" and \"FINANCE\".</p>",
 inp="user role \"OPS\"; allowed: \"ADMIN\", \"OPS\", \"FINANCE\"",
 approach=["Loop over <code>allowed</code>.", "Return true as soon as one matches with <code>equals</code> (Lesson 4.4).", "If the loop finishes, return false."],
 code='''public class Main {
    static boolean hasAnyRole(String userRole, String... allowed) {
        for (String role : allowed) {
            if (role.equals(userRole)) {
                return true;
            }
        }
        return false;
    }

    public static void main(String[] args) {
        boolean ok = hasAnyRole("OPS", "ADMIN", "OPS", "FINANCE");
        System.out.println("Access granted: " + ok);
    }
}
''', notes={(11, 1): "Call :: The three allowed roles are packed into a new String[3].",
 5: "Match :: Found it on the second element: return immediately. The third role is never checked.",
 (11, 2): "Result :: ", 12: "Print :: "},
 tryit="Press <b>Run</b>. Then check role \"INTERN\". How many times does the loop run now?"),
]

PRACTICE_INTRO = "Write varargs methods, predict overload choices, and avoid the null and empty-array traps. The last three are real business tasks."
PROBLEMS = [
dict(level="easy", title="Sum of any numbers", stmt="<p>Write <code>sum(int... n)</code> and call it with no values, one value and five values.</p>", inp="sum(), sum(7), sum(1, 2, 3, 4, 5)",
 code='''public class Main {
    static int sum(int... n) {
        int total = 0;
        for (int x : n) total += x;
        return total;
    }

    public static void main(String[] args) {
        System.out.println(sum());
        System.out.println(sum(7));
        System.out.println(sum(1, 2, 3, 4, 5));
    }
}''', explain="<p><b>How it works:</b> with no values the method receives an empty array, so the loop doesn't run and 0 is returned.</p>"),
dict(level="easy", title="Join words with a separator", stmt="<p>Write <code>join(String sep, String... words)</code> that joins the words with the separator, using a StringBuilder.</p>", inp="join(\" | \", \"Tea\", \"Vada\", \"Samosa\"), join(\"-\", \"2025\", \"01\", \"26\")",
 code='''public class Main {
    static String join(String sep, String... words) {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < words.length; i++) {
            if (i > 0) sb.append(sep);
            sb.append(words[i]);
        }
        return sb.toString();
    }

    public static void main(String[] args) {
        System.out.println(join(" | ", "Tea", "Vada", "Samosa"));
        System.out.println(join("-", "2025", "01", "26"));
    }
}''', explain="<p><b>How it works:</b> the separator is a fixed parameter and must come first. The index loop lets us skip the separator before the first word. (The JDK's <code>String.join</code> does the same job.)</p>"),
dict(level="easy", title="Count values above a limit", stmt="<p>Write <code>countAbove(int limit, int... values)</code> and count how many day temperatures were above 35.</p>", inp="limit 35; temps 33, 36, 38, 34, 40",
 code='''public class Main {
    static int countAbove(int limit, int... values) {
        int count = 0;
        for (int v : values) {
            if (v > limit) count++;
        }
        return count;
    }

    public static void main(String[] args) {
        System.out.println("Hot days: " + countAbove(35, 33, 36, 38, 34, 40));
    }
}''', explain="<p><b>How it works:</b> the first argument always fills <code>limit</code>; everything after it goes into the array.</p>"),
dict(level="medium", title="Which overload wins?", stmt="<p>Predict the output, then run. Methods: <code>f(long)</code>, <code>f(Integer)</code>, <code>f(int...)</code>, and the calls <code>f(5)</code>, <code>f(5, 6)</code>, <code>f()</code>.</p>", inp="f(5), f(5, 6), f()",
 code='''public class Main {
    static void f(long x)    { System.out.println("long"); }
    static void f(Integer x) { System.out.println("Integer"); }
    static void f(int... x)  { System.out.println("varargs " + x.length); }

    public static void main(String[] args) {
        f(5);
        f(5, 6);
        f();
    }
}''', explain="<p><b>How it works:</b> <code>f(5)</code> is settled in phase 1 by widening to long. The other two calls have no fixed-arity match at all, so only phase 3 (varargs) can handle them.</p>"),
dict(level="medium", title="Average without dividing by zero", stmt="<p>Write <code>average(int... marks)</code> that returns 0.0 when no marks are given, instead of producing NaN.</p>", inp="average(), average(80, 90, 70)",
 code='''public class Main {
    static double average(int... marks) {
        if (marks.length == 0) return 0.0;
        int sum = 0;
        for (int m : marks) sum += m;
        return (double) sum / marks.length;
    }

    public static void main(String[] args) {
        System.out.println(average());
        System.out.println(average(80, 90, 70));
    }
}''', explain="<p><b>How it works:</b> without the check, 0.0 / 0 gives <code>NaN</code> (not a number), which then spreads through any calculation that uses it. Decide what “no values” means for your problem and handle it first.</p>"),
dict(level="business", title="GST invoice for any number of lines", stmt="<p>Write <code>invoice(int gstPercent, int... amounts)</code> that prints the subtotal, GST and grand total for a shop bill.</p>", inp="GST 18%; amounts 250, 400, 150",
 code='''public class Main {
    static void invoice(int gstPercent, int... amounts) {
        int subtotal = 0;
        for (int a : amounts) subtotal += a;
        int gst = subtotal * gstPercent / 100;
        System.out.println("Items: " + amounts.length);
        System.out.println("Subtotal: Rs " + subtotal);
        System.out.println("GST " + gstPercent + "%: Rs " + gst);
        System.out.println("Total: Rs " + (subtotal + gst));
    }

    public static void main(String[] args) {
        invoice(18, 250, 400, 150);
    }
}''', explain="<p><b>How it works:</b> the GST rate is required, so it's a fixed parameter; the line amounts vary per bill. 800 × 18 / 100 = 144.</p>"),
dict(level="business", title="Send an alert to several phone numbers", stmt="<p>Write <code>alert(String message, String... phones)</code> that prints one line per phone number and returns how many messages were sent. Phone numbers must be 10 digits; skip invalid ones.</p>", inp="message \"Exam hall changed to B-204\"; phones \"9876543210\", \"12345\", \"9123456789\"",
 code='''public class Main {
    static int alert(String message, String... phones) {
        int sent = 0;
        for (String p : phones) {
            if (p.length() != 10) {
                System.out.println("skip invalid: " + p);
                continue;
            }
            System.out.println("SMS to " + p + ": " + message);
            sent++;
        }
        return sent;
    }

    public static void main(String[] args) {
        int n = alert("Exam hall changed to B-204", "9876543210", "12345", "9123456789");
        System.out.println(n + " message(s) sent");
    }
}''', explain="<p><b>How it works:</b> the message is fixed; any number of recipients follow. <code>continue</code> (Lesson 3.5) skips bad numbers without stopping the loop.</p>"),
dict(level="business", title="Cheapest delivery option", stmt="<p>Several courier partners quote prices for a parcel. Write <code>cheapest(String... quotes)</code> where each quote looks like \"Name:price\", and return the cheapest one. Require at least one quote using a fixed first parameter.</p>", inp="\"FastShip:85\", \"QuickPost:70\", \"CityCourier:92\"",
 code='''public class Main {
    static String cheapest(String first, String... more) {
        String best = first;
        for (String q : more) {
            if (price(q) < price(best)) best = q;
        }
        return best;
    }

    static int price(String quote) {
        return Integer.parseInt(quote.substring(quote.indexOf(':') + 1));
    }

    public static void main(String[] args) {
        System.out.println("Book: " + cheapest("FastShip:85", "QuickPost:70", "CityCourier:92"));
    }
}''', explain="<p><b>How it works:</b> <code>first, ...more</code> makes an empty call impossible. A small helper method extracts the number after the colon, so the comparison stays readable.</p>"),
]
