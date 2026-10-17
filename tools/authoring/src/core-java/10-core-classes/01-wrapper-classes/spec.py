import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../..'))
from mkanim import Anim, two_view

# ---------------- Part 5: two-view animation ----------------
CODE = ["int price = 120;", "Integer a = Integer.valueOf(120);", "Integer b = Integer.valueOf(120);",
        "Integer c = Integer.valueOf(500);", "Integer d = Integer.valueOf(500);", "print(a==b, c==d, c.equals(d))"]
S = Anim("see", frames=6, h=250, label="Code creating Integer objects and the printed comparison results")
S.box(8, 8, 344, 132, None, fill="board", stroke="board")
for i, line in enumerate(CODE):
    y = 30 + i * 20
    S.box(12, y - 14, 336, 19, None, fill="none", stroke="track", sw=2, on=str(i + 1), rx=4)
    S.text(20, y, line, mono=True, size=10, cls="chalk")
S.box(8, 150, 344, 50, None, fill="card2", stroke="line")
S.text(18, 168, "Console", size=9, cls="ink3", bold=True)
S.text(18, 188, "true false true", on="6", mono=True, size=11, cls="green", bold=True)
S.note({1: "A plain int: just the value 120.", 2: "Ask Integer for an object holding 120.", 3: "Ask again for 120.",
        4: "Now ask for 500.", 5: "Ask again for 500.", 6: "== says false for 500, equals says true."}, y=226, size=10.5)
S.caps(["<code>price</code> is a primitive <code>int</code>: a bare value, no object.",
        "<code>Integer.valueOf(120)</code> gives back an <code>Integer</code> object holding 120.",
        "The same call again. On screen nothing looks different.",
        "<code>valueOf(500)</code>: also an Integer object, holding 500.",
        "Again for 500. Two variables, both holding 500.",
        "<code>a == b</code> is <b>true</b>, <code>c == d</code> is <b>false</b>, yet <code>c.equals(d)</code> is <b>true</b>. The right side shows why."])
B = Anim("behind", frames=6, h=250, label="Stack variables pointing into the heap: a and b share one cached Integer, c and d point to two new objects")
B.text(60, 18, "Stack (main)", anchor="middle", size=10, bold=True, cls="ink2")
B.text(240, 18, "Heap", anchor="middle", size=10, bold=True, cls="ink2")
B.box(8, 26, 104, 170, None, fill="card", stroke="line")
B.box(124, 26, 228, 170, None, fill="card", stroke="line")
vars_ = [("price", "120", "1-"), ("a", "→", "2-"), ("b", "→", "3-"), ("c", "→", "4-"), ("d", "→", "5-")]
for i, (n, v, on) in enumerate(vars_):
    y = 36 + i * 30
    B.box(14, y, 92, 24, None, fill="soft-blue", stroke="blue", on=on, rx=5)
    B.text(22, y + 16, n, on=on, mono=True, size=10, bold=True)
    B.text(98, y + 16, v, on=on, mono=True, size=10, anchor="end", cls="blue" if v == "→" else "ink")
# cache strip
B.box(132, 36, 212, 56, None, fill="soft-green", stroke="green", rx=6)
B.text(140, 50, "IntegerCache: -128 … 127", size=9, bold=True, cls="green")
for k, lab in enumerate(["-128", "…", "119", "120", "121", "…", "127"]):
    x = 138 + k * 29
    B.box(x, 58, 26, 26, lab, fill="card", stroke="green", size=7 if len(lab) > 3 else 8, mono=True, rx=4)
B.box(225, 58, 26, 26, None, fill="none", stroke="track", sw=2.5, on="2-3", rx=4)
B.arrow(106, 78, 233, 85, on="2-", color="blue", bend=-8)
B.arrow(106, 108, 243, 86, on="3-", color="blue", bend=8)
# new objects
B.box(140, 112, 90, 34, "Integer 500", sub="new #1", fill="soft-acc", stroke="track", on="4-", size=9.5, bold=True)
B.box(246, 112, 90, 34, "Integer 500", sub="new #2", fill="soft-acc", stroke="track", on="5-", size=9.5, bold=True)
B.arrow(106, 138, 140, 130, on="4-", color="blue")
B.arrow(106, 168, 290, 147, on="5-", color="blue", bend=-14)
B.text(240, 172, "a == b: same object ✓", on="6", anchor="middle", size=9.5, bold=True, cls="green")
B.text(240, 188, "c == d: two objects ✗", on="6", anchor="middle", size=9.5, bold=True, cls="red")
B.note({1: "price holds 120 directly in main's frame.", 2: "120 is in the cache: no new object.",
        3: "Same cached object again: a and b match.", 4: "500 is outside the cache: a new object.",
        5: "Another new object for 500.", 6: "== compares arrows; equals() compares values."}, y=222, size=10)
B.caps(["A primitive lives right in the stack frame. No heap object is involved.",
        "The JDK keeps 256 ready-made Integer objects for -128 to 127. <code>valueOf(120)</code> returns the one for 120; <code>a</code> stores a reference to it.",
        "<code>valueOf(120)</code> returns <b>the same</b> cached object. Now <code>a</code> and <code>b</code> point to one object.",
        "500 isn't cached, so <code>valueOf</code> creates a new Integer object on the heap.",
        "A second call creates a <b>second</b> object. <code>c</code> and <code>d</code> point to different objects that hold the same value.",
        "<code>==</code> checks whether two references point to the same object: true for a/b, false for c/d. <code>equals()</code> compares the stored values: 500 equals 500."])
ANIM = two_view("Integer.valueOf: cached or new?", S, B)

# ---------------- Part 6: animated example ----------------
ANIM2_HEADING = "Watch it with an example: a train booking form"
ANIM2_INTRO = "A booking page sends everything as text. Watch the server turn the passenger count into a number, and refuse text that isn't one."
A = Anim("Parsing the passenger count", frames=5, h=220, label="Form text is parsed into an int; invalid text causes NumberFormatException and a friendly message")
A.box(10, 14, 150, 112, None, fill="card", stroke="line")
A.text(20, 34, "Book ticket", bold=True, size=11)
A.text(20, 56, "Passengers:", size=10, cls="ink2")
A.box(20, 64, 120, 26, None, fill="card2", stroke="line", rx=5)
A.text(30, 82, '"2"', on="1-3", mono=True, size=11, cls="ink", bold=True)
A.text(30, 82, '"two"', on="4-", mono=True, size=11, cls="ink", bold=True)
A.box(40, 98, 80, 20, "Submit", fill="soft-acc", stroke="track", size=9.5, bold=True, rx=10)
A.arrow(162, 70, 196, 70, on="2-", color="track")
A.box(198, 14, 154, 112, None, fill="board", stroke="board")
A.text(208, 34, "Server", size=10, bold=True, cls="chalk")
A.text(208, 56, "Integer.parseInt(text)", on="2-", mono=True, size=9, cls="chalk")
A.text(208, 80, "→ int 2", on="3", mono=True, size=11, cls="green", bold=True)
A.text(208, 100, "fare = 2 × 450", on="3", mono=True, size=9.5, cls="chalk")
A.text(208, 80, "NumberFormatException", on="4-", mono=True, size=9, cls="red", bold=True)
A.text(208, 100, 'For input string: "two"', on="4-", mono=True, size=8.5, cls="red")
A.box(10, 140, 342, 36, None, fill="soft-green", stroke="green", on="3")
A.text(181, 163, "Fare: ₹900 for 2 passengers", on="3", anchor="middle", size=11, bold=True, cls="green")
A.box(10, 140, 342, 36, None, fill="soft-acc", stroke="red", on="5")
A.text(181, 163, "Please enter the number of passengers in digits", on="5", anchor="middle", size=10.5, bold=True, cls="red")
A.caps(["The user types <b>2</b> in the form. Browsers send form fields as <b>text</b>, so the server receives the String <code>\"2\"</code>.",
        "The server calls <code>Integer.parseInt(text)</code> to read the text as a number.",
        "Parsing succeeds: a primitive <code>int</code> 2. Now arithmetic works: 2 × ₹450 = ₹900.",
        "Another user types <b>two</b>. <code>parseInt</code> can't read it and throws <code>NumberFormatException</code>.",
        "The server catches the exception and shows a clear message instead of crashing. (Simplified: real sites also validate in the browser and check limits such as at most 6 passengers.)"])
ANIM2 = A
BLOCKS = {'ANIM': ANIM}

# ---------------- Part 8: tracer ----------------
TRACE = dict(code='''public class Main {
    public static void main(String[] args) {
        int price = 120;
        Integer boxed = Integer.valueOf(price);
        Integer same = Integer.valueOf(120);
        Integer big = Integer.valueOf(500);
        Integer big2 = Integer.valueOf(500);
        System.out.println(boxed == same);
        System.out.println(big == big2);
        System.out.println(big.equals(big2));
        int back = big.intValue();
        System.out.println(back + 1);
    }
}
''', notes={
 3: "Primitive :: A plain int, stored directly in main's frame. No object.",
 4: "Box :: = <code>valueOf(120)</code>: 120 is in the cache range -128..127, so Java hands back a ready-made object, created by the JDK at start-up. <code>boxed</code> = → #2. (The trace numbers objects the first time our code uses them.)",
 5: "Cache hit :: = Asked for 120 again: <code>same</code> = → #2, <b>the same</b> object, not a new one.",
 6: "New object :: 500 is outside the cache, so a fresh Integer is created.",
 7: "New object :: Another call for 500 creates <b>another</b> object, even though the value is the same.",
 8: "Compare :: <code>==</code> compares references. Same object, so <code>true</code>.",
 9: "Compare :: Two different objects, so <code>false</code>.",
 10: "Compare :: <code>equals()</code> compares the values inside: 500 and 500.",
 11: "Unbox :: <code>intValue()</code> copies the number out into a primitive.",
 12: "Print :: Plain int arithmetic."})

# ---------------- Worked examples ----------------
WORKED_INTRO = "Three everyday tasks where wrapper classes do the heavy lifting: reading text, validating characters, and using null for “missing”."
EXAMPLES = [
dict(tag="Education · CSV", title="Average marks from a CSV line",
 problem="<p>A results file stores each student as one line of text: <code>Riya,85,92,78</code>. Write a helper that reads the marks from the line and returns the average.</p>",
 inp='"Riya,85,92,78"',
 approach=["Split the line on commas: the first part is the name, the rest are marks as text.",
           "A helper <code>average(String[] parts)</code> parses each mark with <code>Integer.parseInt</code> and adds it up.",
           "Divide by the count as a <code>double</code> and print."],
 code='''public class Main {
    static double average(String[] parts) {
        int sum = 0;
        for (int i = 1; i < parts.length; i++) {
            sum += Integer.parseInt(parts[i]);
        }
        return (double) sum / (parts.length - 1);
    }

    public static void main(String[] args) {
        String line = "Riya,85,92,78";
        String[] parts = line.split(",");
        double avg = average(parts);
        System.out.println(parts[0] + ": " + avg);
    }
}
''', notes={11: "Input :: The whole line is just text.", 12: "Split :: Four Strings: the name and three marks, still as text.",
            (13, 1): "Call :: ", 5: "Parse :: <code>Integer.parseInt</code> turns the text into an int and adds it.",
            7: "Return :: ", 14: "Print :: "},
 tryit="Press <b>Run</b>. Then change the line to <code>\"Riya,85,AB,78\"</code> (AB = absent) and handle it by skipping marks that aren't numbers."),
dict(tag="Logistics · validation", title="Is this a valid PIN code?",
 problem="<p>A delivery app accepts Indian PIN codes. A valid PIN has exactly 6 characters, all digits, and must not start with 0. Write <code>isValidPin(String pin)</code>.</p>",
 inp='"410210", "41021A", "012345"',
 approach=["Check the length first.", "Reject a leading <code>'0'</code>.", "Loop over the characters and use <code>Character.isDigit</code> on each."],
 code='''public class Main {
    static boolean isValidPin(String pin) {
        if (pin.length() != 6 || pin.charAt(0) == '0') {
            return false;
        }
        for (char c : pin.toCharArray()) {
            if (!Character.isDigit(c)) {
                return false;
            }
        }
        return true;
    }

    public static void main(String[] args) {
        System.out.println(isValidPin("410210"));
        System.out.println(isValidPin("41021A"));
        System.out.println(isValidPin("012345"));
    }
}
''', notes={7: "Check :: <code>Character.isDigit(c)</code>: a static helper of the wrapper class for <code>char</code>."},
 tryit="Press <b>Run</b>. Then add a check that the PIN doesn't contain spaces at the ends: call <code>trim()</code> first."),
dict(tag="HR · attendance", title="Overtime hours with “not entered” days",
 problem="<p>An attendance system stores overtime hours for each day as <code>Integer</code>. A <code>null</code> means the manager hasn't entered that day yet. Total the entered hours and count the missing days.</p>",
 inp="{2, null, 3, null, 1}",
 approach=["Store the week in an <code>Integer[]</code> so a day can be <code>null</code>.",
           "Loop: if the value is null, count it as missing; otherwise unbox and add.",
           "Print the total and the number of missing days."],
 code='''public class Main {
    public static void main(String[] args) {
        Integer[] overtime = {2, null, 3, null, 1};
        int total = 0;
        int missing = 0;
        for (Integer h : overtime) {
            if (h == null) {
                missing++;
            } else {
                total += h.intValue();
            }
        }
        System.out.println("Total overtime: " + total + " h");
        System.out.println("Days not entered: " + missing);
    }
}
''', notes={3: "Array :: An array of Integer references. Two slots hold <code>null</code>: no object at all.",
            7: "Check :: Always test for null before unboxing.", 10: "Unbox :: <code>intValue()</code> copies the number out of the object.",
            13: "Print :: ", 14: "Print :: "},
 tryit="Press <b>Run</b>. Then remove the <code>if (h == null)</code> check and run again: what happens, and why?"),
]

# ---------------- Practice problems ----------------
PRACTICE_INTRO = "Parse text safely, use the wrapper helpers, and avoid the == trap. The last three are business tasks."
PROBLEMS = [
dict(level="easy", title="Sum two numbers typed as text", stmt="<p>Two text boxes contain <code>\"45\"</code> and <code>\"55\"</code>. Print their sum as a number, not <code>4555</code>.</p>", inp='"45", "55"',
 code='''public class Main {
    public static void main(String[] args) {
        String a = "45", b = "55";
        System.out.println(a + b);
        int sum = Integer.parseInt(a) + Integer.parseInt(b);
        System.out.println(sum);
    }
}''', explain="<p><b>How it works:</b> <code>a + b</code> joins two Strings. <code>Integer.parseInt</code> turns each into an int first, so <code>+</code> adds them.</p>"),
dict(level="easy", title="Print the limits of int and long", stmt="<p>Print the largest and smallest values of <code>int</code> and <code>long</code> using wrapper constants.</p>", inp="(none)",
 code='''public class Main {
    public static void main(String[] args) {
        System.out.println("int:  " + Integer.MIN_VALUE + " to " + Integer.MAX_VALUE);
        System.out.println("long: " + Long.MIN_VALUE + " to " + Long.MAX_VALUE);
    }
}''', explain="<p><b>How it works:</b> each numeric wrapper has <code>MIN_VALUE</code> and <code>MAX_VALUE</code> constants. Use them instead of typing the numbers.</p>"),
dict(level="easy", title="Count digits in a mobile number", stmt="<p>Count how many characters in <code>\"+91 98765-43210\"</code> are digits.</p>", inp='"+91 98765-43210"',
 code='''public class Main {
    public static void main(String[] args) {
        String phone = "+91 98765-43210";
        int digits = 0;
        for (char c : phone.toCharArray()) {
            if (Character.isDigit(c)) {
                digits++;
            }
        }
        System.out.println("Digits: " + digits);
    }
}''', explain="<p><b>How it works:</b> <code>Character.isDigit</code> returns true for 0–9. The <code>+</code>, space and dash are skipped.</p>"),
dict(level="medium", title="Fix the == comparison", stmt="<p>This check prints <code>false</code> even though both scores are 250. Fix it so it prints <code>true</code>, and explain why it failed.</p>", inp="Integer s1 = 250, s2 = 250",
 code='''public class Main {
    public static void main(String[] args) {
        Integer s1 = Integer.valueOf(250);
        Integer s2 = Integer.valueOf(250);
        System.out.println("with == : " + (s1 == s2));
        System.out.println("equals  : " + s1.equals(s2));
    }
}''', explain="<p><b>How it works:</b> 250 is outside the Integer cache (-128..127), so two objects exist. <code>==</code> compares references; <code>equals</code> compares the values.</p>"),
dict(level="medium", title="Binary, octal and hex of a number", stmt="<p>Print 45 in binary, octal and hexadecimal, then read <code>\"2d\"</code> back from hex.</p>", inp="45",
 code='''public class Main {
    public static void main(String[] args) {
        int n = 45;
        System.out.println(Integer.toBinaryString(n));
        System.out.println(Integer.toOctalString(n));
        System.out.println(Integer.toHexString(n));
        System.out.println(Integer.parseInt("2d", 16));
    }
}''', explain="<p><b>How it works:</b> the <code>toXxxString</code> methods convert to text in another base; <code>parseInt(text, radix)</code> reads text in that base.</p>"),
dict(level="business", title="Total cart value from text prices", stmt="<p>A shopping cart receives prices as text: <code>\"499.00\"</code>, <code>\"1299.50\"</code>, <code>\"bad\"</code>, <code>\"75\"</code>. Add the valid ones and report how many were rejected.</p>", inp='{"499.00", "1299.50", "bad", "75"}',
 code='''public class Main {
    public static void main(String[] args) {
        String[] prices = {"499.00", "1299.50", "bad", "75"};
        double total = 0;
        int rejected = 0;
        for (String p : prices) {
            try {
                total += Double.parseDouble(p);
            } catch (NumberFormatException e) {
                rejected++;
            }
        }
        System.out.println("Total: " + total);
        System.out.println("Rejected: " + rejected);
    }
}''', explain="<p><b>How it works:</b> <code>Double.parseDouble</code> reads decimal text. Bad entries throw <code>NumberFormatException</code>, which we count instead of crashing. (For real money, use paise as <code>long</code> or <code>BigDecimal</code>.)</p>"),
dict(level="business", title="Strong password check", stmt="<p>A password is strong if it has at least 8 characters, at least one upper-case letter, one digit and one symbol (not a letter or digit). Check <code>\"Riya@2026\"</code> and <code>\"riya2026\"</code>.</p>", inp='"Riya@2026", "riya2026"',
 code='''public class Main {
    static boolean strong(String pw) {
        boolean upper = false, digit = false, symbol = false;
        for (char c : pw.toCharArray()) {
            if (Character.isUpperCase(c)) upper = true;
            else if (Character.isDigit(c)) digit = true;
            else if (!Character.isLetter(c)) symbol = true;
        }
        return pw.length() >= 8 && upper && digit && symbol;
    }

    public static void main(String[] args) {
        System.out.println("Riya@2026 -> " + strong("Riya@2026"));
        System.out.println("riya2026  -> " + strong("riya2026"));
    }
}''', explain="<p><b>How it works:</b> one pass over the characters sets three flags using <code>Character</code> helpers. All four rules must hold.</p>"),
dict(level="business", title="Read settings from a config file", stmt="<p>A config has <code>maxUsers=250</code>, <code>debug=true</code> and <code>timeout=abc</code>. Read each into the right type; use a default of 30 if the timeout is invalid.</p>", inp='{"maxUsers=250", "debug=true", "timeout=abc"}',
 code='''public class Main {
    static int intOr(String text, int fallback) {
        try {
            return Integer.parseInt(text);
        } catch (NumberFormatException e) {
            return fallback;
        }
    }

    public static void main(String[] args) {
        String[] lines = {"maxUsers=250", "debug=true", "timeout=abc"};
        int maxUsers = intOr(lines[0].split("=")[1], 100);
        boolean debug = Boolean.parseBoolean(lines[1].split("=")[1]);
        int timeout = intOr(lines[2].split("=")[1], 30);
        System.out.println("maxUsers=" + maxUsers + ", debug=" + debug + ", timeout=" + timeout);
    }
}''', explain="<p><b>How it works:</b> each line is split at <code>=</code>. A helper parses with a fallback, so one bad setting doesn't stop the application from starting.</p>"),
]
