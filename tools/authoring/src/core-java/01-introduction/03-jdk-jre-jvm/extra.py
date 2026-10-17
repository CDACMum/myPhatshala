WORKED_INTRO = "The JRE ships thousands of ready-made classes (the Java class library). These three programs use some of them for everyday business jobs. Watch the stack: when your code calls a library method, the JVM runs code that came with the JRE, not code you wrote."
EXAMPLES = [
dict(tag="Education · exams", title="Days left until the exam",
 problem="<p>A coaching app shows how many days are left until a student's exam. Use the JRE's <code>java.time</code> classes to count the days between two dates.</p>",
 inp="today 2026-10-15, exam 2026-12-02",
 approach=["Create two <code>LocalDate</code> objects with <code>LocalDate.of</code>.",
           "<code>ChronoUnit.DAYS.between(a, b)</code> counts the days.",
           "Print the date's day of the week too."],
 code='''import java.time.LocalDate;
import java.time.temporal.ChronoUnit;

public class Main {
    public static void main(String[] args) {
        LocalDate today = LocalDate.of(2026, 10, 15);
        LocalDate exam = LocalDate.of(2026, 12, 2);
        long daysLeft = ChronoUnit.DAYS.between(today, exam);
        System.out.println("Exam on: " + exam + " (" + exam.getDayOfWeek() + ")");
        System.out.println("Days left: " + daysLeft);
    }
}
''', notes={6: "Library object :: = <code>LocalDate.of</code> is a JRE method. It creates a LocalDate object on the heap.",
            8: "Count :: = The JRE counts the days between the two dates, handling months of different lengths for you.",
            9: "Day name :: <code>getDayOfWeek()</code> works out the weekday: you didn't write that calendar logic, the JRE did."},
 tryit="Press <b>Run</b>. Then change the exam date to your own birthday."),
dict(tag="Banking · deposits", title="Fixed deposit maturity with Math.pow",
 problem="<p>A bank's fixed deposit grows with compound interest: amount = principal × (1 + rate)<sup>years</sup>. Compute the maturity of Rs 1,00,000 at 7% for 3 years, using <code>Math.pow</code> from the JRE, and round to rupees.</p>",
 inp="principal 100000, rate 7%, 3 years",
 approach=["Store principal, rate (0.07) and years.",
           "<code>Math.pow(1 + rate, years)</code> raises to a power.",
           "<code>Math.round</code> rounds to the nearest rupee."],
 code='''public class Main {
    public static void main(String[] args) {
        double principal = 100000;
        double rate = 0.07;
        int years = 3;
        double maturity = principal * Math.pow(1 + rate, years);
        System.out.println("Maturity amount: Rs " + Math.round(maturity));
        System.out.println("Interest earned: Rs " + Math.round(maturity - principal));
    }
}
''', notes={6: "Math.pow :: = A JRE method computes 1.07³ = 1.225043. Multiplied by 1,00,000 gives 122504.3.",
            7: "Round :: <code>Math.round</code> gives 122504."},
 tryit="Press <b>Run</b>. Then try 5 years at 6.5%. (Real deposits often compound quarterly; this is a simplified yearly version.)"),
dict(tag="CRM · data cleanup", title="Clean up a customer name",
 problem="<p>Names typed at a shop counter often have extra spaces and mixed case. Clean <code>\"   asha VERMA  \"</code> into \"ASHA VERMA\" and print its length before and after, using JRE String methods.</p>",
 inp="\"   asha VERMA  \"",
 approach=["<code>trim()</code> removes spaces at both ends.",
           "<code>toUpperCase()</code> makes every letter capital.",
           "Each method returns a new String; the original stays unchanged."],
 code='''public class Main {
    public static void main(String[] args) {
        String typed = "   asha VERMA  ";
        String clean = typed.trim().toUpperCase();
        System.out.println("[" + typed + "] length " + typed.length());
        System.out.println("[" + clean + "] length " + clean.length());
    }
}
''', notes={4: "Library calls :: = <code>trim()</code> builds a new String without the spaces, then <code>toUpperCase()</code> builds another. Both methods come from the JRE's String class.",
            6: "Result :: 15 characters became 10."},
 tryit="Press <b>Run</b>. Then try <code>toLowerCase()</code> instead."),
]

PRACTICE_INTRO = "Use ready-made classes from the JRE (Math, String, LocalDate) for small tasks. Every output is fixed. The last three are business tasks."
PROBLEMS = [
dict(level="easy", title="Square root", stmt="<p>Print the square root of 144 using <code>Math.sqrt</code>.</p>", inp="144",
 code='''public class Main {
    public static void main(String[] args) {
        System.out.println(Math.sqrt(144));
    }
}''', explain="<p><b>How it works:</b> <code>Math</code> is part of the JRE; <code>sqrt</code> returns a double, so it prints 12.0.</p>"),
dict(level="easy", title="Bigger of two numbers", stmt="<p>Print the larger of 75 and 120 using <code>Math.max</code>.</p>", inp="75, 120",
 code='''public class Main {
    public static void main(String[] args) {
        System.out.println(Math.max(75, 120));
    }
}''', explain="<p><b>How it works:</b> library methods save you from writing common logic yourself.</p>"),
dict(level="easy", title="Upper-case a city", stmt="<p>Print \"mumbai\" in capitals.</p>", inp="mumbai",
 code='''public class Main {
    public static void main(String[] args) {
        System.out.println("mumbai".toUpperCase());
    }
}''', explain="<p><b>How it works:</b> you can call a method directly on a string literal.</p>"),
dict(level="medium", title="Next week's date", stmt="<p>Print the date 7 days after 2026-10-15.</p>", inp="2026-10-15",
 code='''import java.time.LocalDate;

public class Main {
    public static void main(String[] args) {
        LocalDate d = LocalDate.of(2026, 10, 15);
        System.out.println(d.plusDays(7));
    }
}''', explain="<p><b>How it works:</b> <code>plusDays</code> returns a new date; it handles month ends for you.</p>"),
dict(level="medium", title="Round a price", stmt="<p>Round Rs 249.67 to the nearest rupee.</p>", inp="249.67",
 code='''public class Main {
    public static void main(String[] args) {
        System.out.println(Math.round(249.67));
    }
}''', explain="<p><b>How it works:</b> <code>Math.round</code> rounds .5 and above up and returns a long.</p>"),
dict(level="business", title="Delivery date", stmt="<p>An order placed on 2026-10-28 is delivered in 5 days. Print the delivery date and weekday.</p>", inp="2026-10-28, 5 days",
 code='''import java.time.LocalDate;

public class Main {
    public static void main(String[] args) {
        LocalDate delivery = LocalDate.of(2026, 10, 28).plusDays(5);
        System.out.println("Delivery: " + delivery + " (" + delivery.getDayOfWeek() + ")");
    }
}''', explain="<p><b>How it works:</b> the date moves into November correctly without any month logic in your code.</p>"),
dict(level="business", title="Area of a circular stall", stmt="<p>A circular food stall has a radius of 3.5 m. Print its floor area rounded to 2 decimals.</p>", inp="r = 3.5",
 code='''public class Main {
    public static void main(String[] args) {
        double area = Math.PI * 3.5 * 3.5;
        System.out.println("Area: " + Math.round(area * 100) / 100.0 + " sq m");
    }
}''', explain="<p><b>How it works:</b> <code>Math.PI</code> is a constant in the JRE. Multiplying by 100, rounding, and dividing by 100.0 keeps two decimals.</p>"),
dict(level="business", title="Masked phone number", stmt="<p>Show only the last 4 digits of 9876543210, like XXXXXX3210.</p>", inp="9876543210",
 code='''public class Main {
    public static void main(String[] args) {
        String phone = "9876543210";
        System.out.println("XXXXXX" + phone.substring(6));
    }
}''', explain="<p><b>How it works:</b> <code>substring(6)</code> returns the characters from index 6 to the end. Apps mask numbers like this on receipts and screens.</p>"),
]
