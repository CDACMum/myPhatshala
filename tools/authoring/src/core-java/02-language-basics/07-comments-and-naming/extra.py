WORKED_INTRO = "Good names and comments don't change what the program does; they change how fast the next person understands it. Each example is a real calculation written the way professional teams write it: clear names, constants in CAPITALS, and comments that explain <i>why</i>."
EXAMPLES = [
dict(tag="Payroll · readability", title="From x, y, z to names that explain themselves",
 problem="<p>A payroll snippet was written as <code>double z = x * 1.4 - x * 0.12;</code>. Rewrite it with meaningful names, constants and a short comment, and show it gives the same answer for a basic salary of Rs 30,000.</p>",
 inp="basic salary 30000",
 approach=["Name every value: <code>basicSalary</code>, <code>HRA_RATE</code>, <code>PF_RATE</code>.",
           "Use camelCase for variables and UPPER_SNAKE_CASE for constants.",
           "Comment the business rule, not the obvious syntax."],
 code='''public class Main {
    // Company policy 2026: HRA is 40% of basic; employee PF is 12% of basic.
    static final double HRA_RATE = 0.40;
    static final double PF_RATE = 0.12;

    public static void main(String[] args) {
        double x = 30000;
        double z = x * 1.4 - x * 0.12;            // unreadable version

        double basicSalary = 30000;
        double hra = basicSalary * HRA_RATE;
        double providentFund = basicSalary * PF_RATE;
        double takeHome = basicSalary + hra - providentFund;

        System.out.println("old: " + z);
        System.out.println("new: " + takeHome);
    }
}
''', notes={8: "Hard to read :: = Same maths, but what are x, 1.4 and 0.12? A reader must guess.",
            11: "Named :: = <code>hra</code> says what it is, and <code>HRA_RATE</code> says where 0.40 comes from.",
            13: "Readable :: = The line reads like the policy itself: basic + HRA − PF."},
 tryit="Press <b>Run</b>. Then change the HRA rate in one place and see only the new version follow the policy."),
dict(tag="E-commerce · delivery", title="Constants and a Javadoc comment",
 problem="<p>An app's delivery fee is Rs 40, waived for orders of Rs 499 or more. Write a method with a Javadoc comment (<code>/** … */</code>) describing it, using named constants instead of magic numbers.</p>",
 inp="orders of Rs 350 and Rs 620",
 approach=["Constants <code>DELIVERY_FEE</code> and <code>FREE_DELIVERY_FROM</code>.",
           "A Javadoc comment above the method: what it returns and why.",
           "Call it for two order values."],
 code='''public class Main {
    static final int DELIVERY_FEE = 40;
    static final int FREE_DELIVERY_FROM = 499;

    /**
     * Returns the delivery fee for an order.
     * Orders at or above FREE_DELIVERY_FROM ship free (marketing rule, Oct 2026).
     */
    static int deliveryFee(int orderValue) {
        return orderValue >= FREE_DELIVERY_FROM ? 0 : DELIVERY_FEE;
    }

    public static void main(String[] args) {
        System.out.println("Rs 350 order: fee Rs " + deliveryFee(350));
        System.out.println("Rs 620 order: fee Rs " + deliveryFee(620));
    }
}
''', notes={(14, 1): "Call :: = The comments never run; the JVM ignores them. They exist only for people (and for javadoc, which turns /** */ comments into documentation pages).",
            (10, 1): "Rule :: = 350 is below 499, so the fee is DELIVERY_FEE (40).",
            (10, 2): "Free :: = 620 ≥ 499, so 0."},
 tryit="Press <b>Run</b>. Then change FREE_DELIVERY_FROM to 699 and run again."),
dict(tag="Utilities · billing", title="Comments that explain why, not what",
 problem="<p>An electricity bill adds a minimum charge. Write it with two kinds of comments: a bad one that repeats the code and a good one that explains the business reason. Compute bills for 30 and 180 units.</p>",
 inp="30 units, 180 units; Rs 6/unit; minimum Rs 250",
 approach=["Name the constants.",
           "Use <code>Math.max</code> to apply the minimum.",
           "Compare a useless comment with a useful one."],
 code='''public class Main {
    static final int RATE_PER_UNIT = 6;
    static final int MINIMUM_BILL = 250;

    public static void main(String[] args) {
        int units = 30;
        // multiply units by rate   <- bad: repeats what the code already says
        int energyCharge = units * RATE_PER_UNIT;
        // Every connection pays at least the minimum, which covers meter reading and maintenance.
        int bill = Math.max(energyCharge, MINIMUM_BILL);
        System.out.println(units + " units: Rs " + bill);

        units = 180;
        bill = Math.max(units * RATE_PER_UNIT, MINIMUM_BILL);
        System.out.println(units + " units: Rs " + bill);
    }
}
''', notes={10: "Minimum :: = 30 × 6 = 180 is below 250, so the bill is 250. The comment above tells a new developer <i>why</i> that rule exists.",
            14: "Above minimum :: = 180 × 6 = 1080, which is more than 250."},
 tryit="Press <b>Run</b>. Then add a comment above the second calculation that explains something a reader couldn't guess. (Illustrative tariff.)"),
]

PRACTICE_INTRO = "Rewrite and write code with clear names, constants and helpful comments. The output stays the same; the code gets easier to read. The last three are business tasks."
PROBLEMS = [
dict(level="easy", title="Single-line and multi-line comments", stmt="<p>Write a program with a // comment and a /* */ comment that prints \"Comments are ignored\".</p>", inp="(none)",
 code='''public class Main {
    public static void main(String[] args) {
        // this line is a single-line comment
        /* this is a
           multi-line comment */
        System.out.println("Comments are ignored");
    }
}''', explain="<p><b>How it works:</b> the compiler skips comments completely; they don't exist in the bytecode.</p>"),
dict(level="easy", title="camelCase names", stmt="<p>Store the number of students in a class (42) in a well-named variable and print it.</p>", inp="42",
 code='''public class Main {
    public static void main(String[] args) {
        int studentsInClass = 42;
        System.out.println("Students: " + studentsInClass);
    }
}''', explain="<p><b>How it works:</b> variables use camelCase: first word lowercase, later words capitalised.</p>"),
dict(level="easy", title="A named constant", stmt="<p>Replace the magic number 0.05 with a constant SERVICE_CHARGE and print the charge on Rs 800.</p>", inp="800",
 code='''public class Main {
    static final double SERVICE_CHARGE = 0.05;

    public static void main(String[] args) {
        System.out.println("Service charge: Rs " + 800 * SERVICE_CHARGE);
    }
}''', explain="<p><b>How it works:</b> constants use UPPER_SNAKE_CASE and say what the number means.</p>"),
dict(level="medium", title="Rename for clarity", stmt="<p>Rewrite <code>int a = 60, b = 45; int c = a * b;</code> (minutes per class × classes) with clear names and print the total minutes.</p>", inp="60, 45",
 code='''public class Main {
    public static void main(String[] args) {
        int minutesPerClass = 60;
        int classesPerTerm = 45;
        int totalMinutes = minutesPerClass * classesPerTerm;
        System.out.println("Total teaching minutes: " + totalMinutes);
    }
}''', explain="<p><b>How it works:</b> the same calculation, but now it explains itself.</p>"),
dict(level="medium", title="Method name as a verb", stmt="<p>Write a method <code>calculateArea(double radius)</code> and print the area for radius 2.</p>", inp="2",
 code='''public class Main {
    static double calculateArea(double radius) {
        return Math.PI * radius * radius;
    }

    public static void main(String[] args) {
        System.out.println(calculateArea(2));
    }
}''', explain="<p><b>How it works:</b> methods are named with verbs (calculate, print, find) in camelCase.</p>"),
dict(level="business", title="Clear invoice calculation", stmt="<p>Compute an invoice: unit price 250, quantity 6, discount 5%, GST 18%, with clear names and constants.</p>", inp="250, 6",
 code='''public class Main {
    static final double DISCOUNT_RATE = 0.05;
    static final double GST_RATE = 0.18;

    public static void main(String[] args) {
        double unitPrice = 250;
        int quantity = 6;
        double subtotal = unitPrice * quantity;
        double afterDiscount = subtotal * (1 - DISCOUNT_RATE);
        double invoiceTotal = afterDiscount * (1 + GST_RATE);
        System.out.println("Invoice total: Rs " + Math.round(invoiceTotal));
    }
}''', explain="<p><b>How it works:</b> 1500 → 1425 → 1681.5 → rounded to 1682. Each step has a name you could show an accountant.</p>"),
dict(level="business", title="Document a rule", stmt="<p>Add a comment explaining why late fees are capped, and compute the fee: Rs 10/day, at most Rs 100, for 14 days late.</p>", inp="14 days",
 code='''public class Main {
    static final int FEE_PER_DAY = 10;
    // Library rule: late fees are capped so students aren't charged more than a book's typical cost.
    static final int MAX_LATE_FEE = 100;

    public static void main(String[] args) {
        int daysLate = 14;
        int fee = Math.min(daysLate * FEE_PER_DAY, MAX_LATE_FEE);
        System.out.println("Late fee: Rs " + fee);
    }
}''', explain="<p><b>How it works:</b> Math.min applies the cap; the comment records the reason, which code alone can't show.</p>"),
dict(level="business", title="Class and constant names", stmt="<p>Create a class-level constant COMPANY_NAME and print it with a monthly target stored as monthlySalesTarget.</p>", inp="(none)",
 code='''public class Main {
    static final String COMPANY_NAME = "Shree Traders";

    public static void main(String[] args) {
        int monthlySalesTarget = 500000;
        System.out.println(COMPANY_NAME + " target: Rs " + monthlySalesTarget);
    }
}''', explain="<p><b>How it works:</b> classes use PascalCase (Main), constants UPPER_SNAKE_CASE, variables camelCase.</p>"),
]
