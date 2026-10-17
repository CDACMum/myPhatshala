WORKED_INTRO = "Casting changes a value from one type to another. Widening (int → double) is automatic and safe; narrowing (double → int, long → int) needs an explicit cast and can lose data. These programs show both, with real business numbers."
EXAMPLES = [
dict(tag="Reviews · ratings", title="Average rating: integer division vs casting",
 problem="<p>A restaurant has 3 reviews with total stars 13. Compute the average rating. Dividing two ints gives 4, not 4.33. Cast to <code>double</code> first to keep the fraction, then show the rating as whole stars by casting back to <code>int</code>.</p>",
 inp="total stars 13, reviews 3",
 approach=["<code>13 / 3</code> is integer division: 4.",
           "<code>(double) 13 / 3</code> widens first: 4.333….",
           "<code>(int) avg</code> narrows: the fraction is cut off (not rounded)."],
 code='''public class Main {
    public static void main(String[] args) {
        int totalStars = 13;
        int reviews = 3;
        int wrong = totalStars / reviews;
        double avg = (double) totalStars / reviews;
        int wholeStars = (int) avg;
        System.out.println("int division: " + wrong);
        System.out.println("average: " + avg);
        System.out.println("whole stars shown: " + wholeStars);
    }
}
''', notes={5: "Integer division :: = Both are ints, so the result is an int: 4. The .333 is thrown away.",
            6: "Cast first :: = <code>(double)</code> applies to <code>totalStars</code> only; then double ÷ int is done in double: 4.333333333333333.",
            7: "Narrowing :: = <code>(int)</code> truncates toward zero: 4. Use <code>Math.round</code> to round instead."},
 tryit="Press <b>Run</b>. Then move the cast: <code>(double) (totalStars / reviews)</code>. Why is it 4.0?"),
dict(tag="Payments · conversion", title="Squeezing a long into an int loses data",
 problem="<p>An old reporting system stores amounts in <code>int</code>. A large transfer of Rs 3,000,000,000 (in a <code>long</code>) is cast to int. Show the corrupted value and how to detect the problem with <code>Math.toIntExact</code>.</p>",
 inp="amount 3000000000",
 approach=["Cast <code>(int) amount</code>: the extra bits are dropped silently.",
           "<code>Math.toIntExact(amount)</code> throws instead of losing data.",
           "Catch it and report the problem."],
 code='''public class Main {
    public static void main(String[] args) {
        long amount = 3_000_000_000L;
        int squeezed = (int) amount;
        System.out.println("long: " + amount + ", cast to int: " + squeezed);
        try {
            int safe = Math.toIntExact(amount);
            System.out.println("safe: " + safe);
        } catch (ArithmeticException e) {
            System.out.println("refused: " + e.getMessage());
        }
    }
}
''', notes={4: "Silent loss :: = Only the lowest 32 bits are kept, and the number becomes negative: −1294967296.",
            7: "Checked :: = <code>Math.toIntExact</code> notices the value doesn't fit and throws ArithmeticException.",
            10: "Safe failure :: An error you can see is far better than a wrong amount in a report."},
 tryit="Press <b>Run</b>. Then set the amount to 2_000_000_000L and see both methods agree."),
dict(tag="Ticketing · seats", title="From seat letter to row number and back",
 problem="<p>A bus booking app labels rows 'A' to 'L' but stores them as numbers 1–12. Convert 'H' to its row number and convert row 3 back to a letter, using char ↔ int casts.</p>",
 inp="seat row 'H'; row number 3",
 approach=["<code>row - 'A' + 1</code>: char arithmetic gives an int.",
           "<code>(char) ('A' + n - 1)</code> turns a number back into a letter.",
           "Print both conversions."],
 code='''public class Main {
    public static void main(String[] args) {
        char seatRow = 'H';
        int rowNumber = seatRow - 'A' + 1;
        int n = 3;
        char letter = (char) ('A' + n - 1);
        System.out.println("Row " + seatRow + " is number " + rowNumber);
        System.out.println("Number " + n + " is row " + letter);
    }
}
''', notes={4: "char math :: = Chars are promoted to int in arithmetic: 72 − 65 + 1 = 8.",
            6: "Back to char :: = 65 + 3 − 1 = 67, and <code>(char) 67</code> is 'C'. The cast is required because int → char is narrowing."},
 tryit="Press <b>Run</b>. Then convert row 12 to its letter."),
]

PRACTICE_INTRO = "Widen automatically, narrow with care. Predict each output before running. The last three are business tasks."
PROBLEMS = [
dict(level="easy", title="Automatic widening", stmt="<p>Assign an int 50 to a double and print it.</p>", inp="50",
 code='''public class Main {
    public static void main(String[] args) {
        int i = 50;
        double d = i;
        System.out.println(d);
    }
}''', explain="<p><b>How it works:</b> int fits into double without loss, so no cast is needed; it prints 50.0.</p>"),
dict(level="easy", title="Truncation", stmt="<p>Cast 9.99 to int and print it.</p>", inp="9.99",
 code='''public class Main {
    public static void main(String[] args) {
        System.out.println((int) 9.99);
    }
}''', explain="<p><b>How it works:</b> casting to int drops the fraction; it does not round.</p>"),
dict(level="easy", title="char to int", stmt="<p>Print the int value of '0' and of '9'.</p>", inp="'0', '9'",
 code='''public class Main {
    public static void main(String[] args) {
        System.out.println((int) '0' + " " + (int) '9');
    }
}''', explain="<p><b>How it works:</b> digit characters have codes 48 to 57, not 0 to 9.</p>"),
dict(level="medium", title="Digit character to number", stmt="<p>Convert the character '7' to the number 7 and add 1.</p>", inp="'7'",
 code='''public class Main {
    public static void main(String[] args) {
        char c = '7';
        int digit = c - '0';
        System.out.println(digit + 1);
    }
}''', explain="<p><b>How it works:</b> subtracting '0' (48) turns a digit character into its value.</p>"),
dict(level="medium", title="Rounding vs casting", stmt="<p>For 7.6, print the cast to int and Math.round.</p>", inp="7.6",
 code='''public class Main {
    public static void main(String[] args) {
        double x = 7.6;
        System.out.println((int) x + " " + Math.round(x));
    }
}''', explain="<p><b>How it works:</b> casting cuts to 7; rounding gives 8.</p>"),
dict(level="business", title="Percentage of target", stmt="<p>Sales were 37 out of a target of 40. Print the percentage with decimals.</p>", inp="37, 40",
 code='''public class Main {
    public static void main(String[] args) {
        int sold = 37, target = 40;
        double pct = (double) sold / target * 100;
        System.out.println("Achieved " + pct + "%");
    }
}''', explain="<p><b>How it works:</b> without the cast, 37 / 40 would be 0 and the answer 0.0%.</p>"),
dict(level="business", title="Whole cartons needed", stmt="<p>A shop must ship 250 bottles, 24 per carton. Print cartons needed (round up).</p>", inp="250, 24",
 code='''public class Main {
    public static void main(String[] args) {
        int cartons = (int) Math.ceil(250 / 24.0);
        System.out.println("Cartons: " + cartons);
    }
}''', explain="<p><b>How it works:</b> Math.ceil rounds up (10.41 → 11.0); the cast turns the double into an int.</p>"),
dict(level="business", title="Price to paise", stmt="<p>Convert Rs 129.95 to paise as a long, once with a plain cast and once with rounding.</p>", inp="129.95",
 code='''public class Main {
    public static void main(String[] args) {
        double rupees = 129.95;
        long cast = (long) (rupees * 100);
        long rounded = Math.round(rupees * 100);
        System.out.println("cast: " + cast + " paise, rounded: " + rounded + " paise");
    }
}''', explain="<p><b>How it works:</b> 129.95 × 100 is 12994.999999999998 in binary floating point, so the cast cuts it to 12994, one paisa short. Rounding gives the correct 12995. Always round when converting money.</p>"),
]
