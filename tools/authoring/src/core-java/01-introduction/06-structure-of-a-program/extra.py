WORKED_INTRO = "Every Java program has the same skeleton: imports, a class, fields, methods and <code>main</code>. These three programs use each part for a real job. In the trace, watch <code>static</code> fields appear once for the class while each method call gets its own frame."
EXAMPLES = [
dict(tag="Restaurant · tokens", title="Token slips from a helper method",
 problem="<p>A restaurant prints a token slip for each order. The restaurant name is the same for every slip, so store it once in a <code>static</code> field. Put the printing in a method and call it for tokens 101 and 102.</p>",
 inp="tokens 101, 102",
 approach=["A <code>static String</code> field holds the name: one copy for the whole class.",
           "<code>printSlip(int token)</code> prints one slip.",
           "main calls it twice."],
 code='''public class Main {
    static String restaurant = "Udupi Corner";

    static void printSlip(int token) {
        System.out.println(restaurant + " | Token #" + token);
    }

    public static void main(String[] args) {
        printSlip(101);
        printSlip(102);
        System.out.println("Slips printed: 2");
    }
}
''', notes={(9, 1): "Call :: = main calls <code>printSlip(101)</code>; a new frame with <code>token = 101</code> is pushed.",
            (5, 1): "Static field :: = The method reads the class's single <code>restaurant</code> field, shown under statics.",
            (10, 1): "Second call :: = A new frame, <code>token = 102</code>; the field is shared, not copied."},
 tryit="Press <b>Run</b>. Then change the restaurant name once and see both slips change."),
dict(tag="Library · due dates", title="Using an import: a library book's due date",
 problem="<p>A college library lends books for 14 days. Print the issue date and the due date. <code>LocalDate</code> lives in package <code>java.time</code>, so it must be imported at the top of the file.</p>",
 inp="issued 2026-10-15, 14 days",
 approach=["<code>import java.time.LocalDate;</code> before the class.",
           "Create the issue date, then <code>plusDays(14)</code>.",
           "Print both."],
 code='''import java.time.LocalDate;

public class Main {
    static final int LOAN_DAYS = 14;

    public static void main(String[] args) {
        LocalDate issued = LocalDate.of(2026, 10, 15);
        LocalDate due = issued.plusDays(LOAN_DAYS);
        System.out.println("Issued: " + issued);
        System.out.println("Due:    " + due);
    }
}
''', notes={7: "Imported class :: = Because of the import, we can write <code>LocalDate</code> instead of <code>java.time.LocalDate</code>.",
            8: "Constant :: = <code>LOAN_DAYS</code> is a <code>static final</code> constant: one value for the class that can never change."},
 tryit="Press <b>Run</b>. Then delete the import line and read the compile error."),
dict(tag="Shop · pricing", title="Two methods working together",
 problem="<p>A shop computes a bill in two steps: apply a 10% discount, then add 5% tax. Write one method for each step and combine them in main.</p>",
 inp="price 800",
 approach=["<code>discount(double p)</code> returns 90% of p.",
           "<code>addTax(double p)</code> returns 105% of p.",
           "main passes the result of one method into the other."],
 code='''public class Main {
    static double discount(double price) {
        return price * 0.90;
    }

    static double addTax(double price) {
        return price * 1.05;
    }

    public static void main(String[] args) {
        double price = 800;
        double afterDiscount = discount(price);
        double finalPrice = addTax(afterDiscount);
        System.out.println("After discount: Rs " + afterDiscount);
        System.out.println("Final price:    Rs " + finalPrice);
    }
}
''', notes={12: "First method :: = <code>discount</code> gets its own frame and returns 720.0.",
            13: "Second method :: = The result is passed into <code>addTax</code>: 720 × 1.05 = 756.0."},
 tryit="Press <b>Run</b>. Then write it in one line: <code>addTax(discount(price))</code>."),
]

PRACTICE_INTRO = "Use the parts of a Java program: class, main, static fields, constants, imports and methods. Every output is fixed. The last three are business tasks."
PROBLEMS = [
dict(level="easy", title="A greeting method", stmt="<p>Write <code>static void greet()</code> that prints \"Welcome!\" and call it from main twice.</p>", inp="(none)",
 code='''public class Main {
    static void greet() {
        System.out.println("Welcome!");
    }

    public static void main(String[] args) {
        greet();
        greet();
    }
}''', explain="<p><b>How it works:</b> a method is defined once and can be called many times.</p>"),
dict(level="easy", title="A constant", stmt="<p>Declare <code>static final double GST = 0.18;</code> and print the GST on Rs 1,000.</p>", inp="1000",
 code='''public class Main {
    static final double GST = 0.18;

    public static void main(String[] args) {
        System.out.println("GST: Rs " + 1000 * GST);
    }
}''', explain="<p><b>How it works:</b> <code>final</code> means it can't be changed; constants are written in capitals by convention.</p>"),
dict(level="easy", title="Method with a parameter", stmt="<p>Write <code>static int doubleIt(int n)</code> and print doubleIt(21).</p>", inp="21",
 code='''public class Main {
    static int doubleIt(int n) {
        return n * 2;
    }

    public static void main(String[] args) {
        System.out.println(doubleIt(21));
    }
}''', explain="<p><b>How it works:</b> <code>return</code> sends a value back to the caller.</p>"),
dict(level="medium", title="Import and use", stmt="<p>Import <code>java.time.LocalDate</code> and print the weekday of 2026-08-15.</p>", inp="2026-08-15",
 code='''import java.time.LocalDate;

public class Main {
    public static void main(String[] args) {
        System.out.println(LocalDate.of(2026, 8, 15).getDayOfWeek());
    }
}''', explain="<p><b>How it works:</b> imports go before the class and let you use the short class name.</p>"),
dict(level="medium", title="Shared counter", stmt="<p>A static field <code>visits</code> starts at 0. A method <code>visit()</code> adds 1. Call it three times and print visits.</p>", inp="(none)",
 code='''public class Main {
    static int visits = 0;

    static void visit() {
        visits = visits + 1;
    }

    public static void main(String[] args) {
        visit();
        visit();
        visit();
        System.out.println("Visits: " + visits);
    }
}''', explain="<p><b>How it works:</b> a static field lives as long as the class, so every call updates the same value.</p>"),
dict(level="business", title="Delivery charge method", stmt="<p>Write <code>static int delivery(int km)</code>: Rs 20 base + Rs 8 per km. Print charges for 3 km and 7 km.</p>", inp="3, 7",
 code='''public class Main {
    static int delivery(int km) {
        return 20 + 8 * km;
    }

    public static void main(String[] args) {
        System.out.println("3 km: Rs " + delivery(3));
        System.out.println("7 km: Rs " + delivery(7));
    }
}''', explain="<p><b>How it works:</b> putting the rule in one method means a price change is made in one place. (Illustrative rates.)</p>"),
dict(level="business", title="Shop details in constants", stmt="<p>Store the shop name and GSTIN as constants and print a receipt header.</p>", inp="(none)",
 code='''public class Main {
    static final String SHOP = "Patil Electronics";
    static final String GSTIN = "27ABCDE1234F1Z5";

    public static void main(String[] args) {
        System.out.println(SHOP);
        System.out.println("GSTIN: " + GSTIN);
    }
}''', explain="<p><b>How it works:</b> constants for fixed business details avoid typos repeated across a program. (Made-up GSTIN.)</p>"),
dict(level="business", title="Two-step salary calculation", stmt="<p>Write <code>gross(basic)</code> = basic + 40% HRA and <code>net(gross)</code> = gross − 12% PF. Print net for basic Rs 30,000.</p>", inp="30000",
 code='''public class Main {
    static double gross(double basic) {
        return basic * 1.40;
    }

    static double net(double gross) {
        return gross * 0.88;
    }

    public static void main(String[] args) {
        System.out.println("Net: Rs " + net(gross(30000)));
    }
}''', explain="<p><b>How it works:</b> the inner call runs first (42000.0), its result feeds the outer call (36960.0). (Simplified salary rules.)</p>"),
]
