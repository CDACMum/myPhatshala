WORKED_INTRO = "Operators turn values into answers: arithmetic, comparison, logical, compound assignment and increment. Each program below answers a real business question with nothing but operators. Watch the variables change on the stack after each expression."
EXAMPLES = [
dict(tag="Retail · checkout", title="Build a bill with compound assignment",
 problem="<p>A checkout adds three items to a total, applies a 10% discount, adds Rs 40 delivery, and splits the bill across 3 friends. Use <code>+=</code>, <code>*=</code>, <code>/</code> and <code>%</code>.</p>",
 inp="items 450, 299, 180; 10% off; delivery 40; 3 people",
 approach=["<code>total += price</code> adds to the running total.",
           "<code>total *= 0.9</code> applies the discount.",
           "Whole-rupee share with <code>/</code>, leftover with <code>%</code>."],
 code='''public class Main {
    public static void main(String[] args) {
        double total = 0;
        total += 450;
        total += 299;
        total += 180;
        total *= 0.9;
        total += 40;
        int rounded = (int) Math.round(total);
        System.out.println("Bill: Rs " + rounded);
        System.out.println("Each pays Rs " + rounded / 3 + ", leftover Rs " + rounded % 3);
    }
}
''', notes={4: "+= :: = <code>total += 450</code> means <code>total = total + 450</code>.",
            7: "*= :: = 929 × 0.9 = 836.1 (a 10% discount).",
            9: "Round :: = 876.1 rounds to 876.",
            11: "/ and % :: 876 / 3 = 292 each, remainder 0."},
 tryit="Press <b>Run</b>. Then change the people to 4 and look at the leftover."),
dict(tag="Calendar · leap years", title="Is it a leap year? Logical operators",
 problem="<p>A billing system must know whether February has 29 days. A year is a leap year if it's divisible by 4 and not by 100, or if it's divisible by 400. Check 2024, 1900 and 2000.</p>",
 inp="2024, 1900, 2000",
 approach=["<code>year % 4 == 0</code> tests divisibility.",
           "Combine with <code>&amp;&amp;</code> (and), <code>||</code> (or), <code>!=</code> (not equal).",
           "Store each result in a boolean."],
 code='''public class Main {
    public static void main(String[] args) {
        int y1 = 2024, y2 = 1900, y3 = 2000;
        boolean leap1 = (y1 % 4 == 0 && y1 % 100 != 0) || y1 % 400 == 0;
        boolean leap2 = (y2 % 4 == 0 && y2 % 100 != 0) || y2 % 400 == 0;
        boolean leap3 = (y3 % 4 == 0 && y3 % 100 != 0) || y3 % 400 == 0;
        System.out.println(y1 + ": " + leap1);
        System.out.println(y2 + ": " + leap2);
        System.out.println(y3 + ": " + leap3);
    }
}
''', notes={4: "2024 :: = Divisible by 4 (true) and not by 100 (true): true.",
            5: "1900 :: = Divisible by 100, so the first part is false; 1900 % 400 is 300, so false.",
            6: "2000 :: = The first part is false, but 2000 % 400 == 0 makes the whole thing true."},
 tryit="Press <b>Run</b>. Then check 2100."),
dict(tag="Restaurant · tokens", title="Token numbers with ++: before or after?",
 problem="<p>A restaurant hands out tokens. <code>next++</code> gives the current number and then increases it; <code>++next</code> increases first. Hand out two tokens with <code>next++</code>, then peek at the following number with <code>++next</code>.</p>",
 inp="tokens start at 101",
 approach=["<code>int t = next++;</code>: t gets 101, next becomes 102.",
           "Repeat for the second customer.",
           "<code>++next</code> increases first, then gives the new value."],
 code='''public class Main {
    public static void main(String[] args) {
        int next = 101;
        int asha = next++;
        int ravi = next++;
        int peek = ++next;
        System.out.println("Asha: " + asha + ", Ravi: " + ravi);
        System.out.println("next is now " + next + ", peek was " + peek);
    }
}
''', notes={4: "Post-increment :: = <code>asha</code> gets the old value 101; then <code>next</code> becomes 102.",
            5: "Again :: = ravi = 102, next = 103.",
            6: "Pre-increment :: = next becomes 104 first, and that new value goes into <code>peek</code>. Token 103 was skipped: a real bug this mix-up causes."},
 tryit="Press <b>Run</b>. Then change <code>++next</code> to <code>next++</code> and compare."),
]

PRACTICE_INTRO = "Arithmetic, comparison, logical, compound and increment operators. Predict each result first. The last three are business tasks."
PROBLEMS = [
dict(level="easy", title="Remainder", stmt="<p>Print 17 % 5 and 20 % 5.</p>", inp="(none)",
 code='''public class Main {
    public static void main(String[] args) {
        System.out.println(17 % 5 + " " + 20 % 5);
    }
}''', explain="<p><b>How it works:</b> % gives the remainder after division; 0 means divisible.</p>"),
dict(level="easy", title="Even or odd as boolean", stmt="<p>Print whether 42 and 17 are even.</p>", inp="42, 17",
 code='''public class Main {
    public static void main(String[] args) {
        System.out.println((42 % 2 == 0) + " " + (17 % 2 == 0));
    }
}''', explain="<p><b>How it works:</b> comparison operators produce booleans.</p>"),
dict(level="easy", title="Compound assignment", stmt="<p>Start x at 10; do x += 5, x *= 3, x -= 7, x /= 2 and print x.</p>", inp="10",
 code='''public class Main {
    public static void main(String[] args) {
        int x = 10;
        x += 5;
        x *= 3;
        x -= 7;
        x /= 2;
        System.out.println(x);
    }
}''', explain="<p><b>How it works:</b> 10 → 15 → 45 → 38 → 19.</p>"),
dict(level="medium", title="Ternary operator", stmt="<p>Print \"PASS\" if marks (58) are 40 or more, else \"FAIL\", using <code>? :</code>.</p>", inp="58",
 code='''public class Main {
    public static void main(String[] args) {
        int marks = 58;
        System.out.println(marks >= 40 ? "PASS" : "FAIL");
    }
}''', explain="<p><b>How it works:</b> condition ? valueIfTrue : valueIfFalse picks one of two values.</p>"),
dict(level="medium", title="Short-circuit &&", stmt="<p>Show that the right side of && isn't evaluated when the left is false: divide only if the divisor isn't zero.</p>", inp="d = 0",
 code='''public class Main {
    public static void main(String[] args) {
        int d = 0;
        boolean ok = d != 0 && 100 / d > 5;
        System.out.println("ok = " + ok);
    }
}''', explain="<p><b>How it works:</b> because <code>d != 0</code> is false, Java skips <code>100 / d</code>, so there's no division by zero.</p>"),
dict(level="business", title="Free delivery check", stmt="<p>Free delivery if the cart is Rs 499+ or the user is a member. Check a Rs 350 cart for a member.</p>", inp="350, member",
 code='''public class Main {
    public static void main(String[] args) {
        int cart = 350;
        boolean member = true;
        System.out.println("Free delivery: " + (cart >= 499 || member));
    }
}''', explain="<p><b>How it works:</b> || is true if either side is true.</p>"),
dict(level="business", title="Notes for an ATM withdrawal", stmt="<p>Dispense Rs 2,800 using Rs 500 and Rs 100 notes: print how many of each.</p>", inp="2800",
 code='''public class Main {
    public static void main(String[] args) {
        int amount = 2800;
        System.out.println("500 x " + amount / 500);
        System.out.println("100 x " + amount % 500 / 100);
    }
}''', explain="<p><b>How it works:</b> / counts big notes; % gives what's left for smaller ones. % and / have the same precedence and run left to right.</p>"),
dict(level="business", title="Loan eligibility in one expression", stmt="<p>Eligible if age is 21–60 and income at least Rs 25,000. Check age 34, income 28,000.</p>", inp="34, 28000",
 code='''public class Main {
    public static void main(String[] args) {
        int age = 34, income = 28000;
        boolean eligible = age >= 21 && age <= 60 && income >= 25000;
        System.out.println("Eligible: " + eligible);
    }
}''', explain="<p><b>How it works:</b> all three conditions must be true for && to be true. (Illustrative rule.)</p>"),
]
