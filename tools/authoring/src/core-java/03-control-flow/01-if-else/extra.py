WORKED_INTRO = "Decisions are the heart of business rules. Each program below turns a real rule into <code>if</code> / <code>else if</code> / <code>else</code>. In the trace, watch which lines are skipped: the JVM evaluates a condition and jumps over the branches that don't apply."
EXAMPLES = [
dict(tag="Banking · loans", title="Personal loan pre-approval",
 problem="<p>A bank pre-approves a personal loan if the applicant is 21–58 years old, earns at least Rs 25,000 a month and has a credit score of 700 or more. Otherwise it explains the first reason for rejection.</p>",
 inp="age 35, income 22000, credit score 760",
 approach=["Check each rule in order with <code>if / else if</code>.",
           "The first failing rule gives the reason.",
           "If none fail, approve."],
 code='''public class Main {
    public static void main(String[] args) {
        int age = 35;
        int income = 22000;
        int score = 760;
        if (age < 21 || age > 58) {
            System.out.println("Rejected: age must be 21-58");
        } else if (income < 25000) {
            System.out.println("Rejected: income below Rs 25,000");
        } else if (score < 700) {
            System.out.println("Rejected: credit score below 700");
        } else {
            System.out.println("Pre-approved!");
        }
    }
}
''', notes={6: "Age check :: = 35 is within 21–58, so this condition is false and its block is skipped.",
            8: "Income check :: = 22000 &lt; 25000 is true: this branch runs.",
            9: "Reason :: The remaining else-if and else are skipped entirely: only one branch of the chain ever runs."},
 tryit="Press <b>Run</b>. Then set income to 40000 and run again. (Illustrative rules.)"),
dict(tag="Education · grades", title="Marks to grade",
 problem="<p>A university converts percentage marks into grades: 90+ O, 75–89 A, 60–74 B, 40–59 C, below 40 F. Grade three students.</p>",
 inp="marks 82, 39, 90",
 approach=["Test from the highest band down.",
           "Each <code>else if</code> only runs if all earlier tests failed, so lower limits are enough.",
           "Use a helper method so the same rules grade every student."],
 code='''public class Main {
    static String grade(int marks) {
        if (marks >= 90) {
            return "O";
        } else if (marks >= 75) {
            return "A";
        } else if (marks >= 60) {
            return "B";
        } else if (marks >= 40) {
            return "C";
        } else {
            return "F";
        }
    }

    public static void main(String[] args) {
        System.out.println("82 -> " + grade(82));
        System.out.println("39 -> " + grade(39));
        System.out.println("90 -> " + grade(90));
    }
}
''', notes={(3, 1): "82 ≥ 90? :: = No: move to the next test.",
            (5, 1): "82 ≥ 75? :: = Yes: return \"A\". No upper limit is needed because 90+ was already handled above."},
 tryit="Press <b>Run</b>. Then add a grade \"A+\" for 85–89."),
dict(tag="Utilities · billing", title="Electricity slab billing",
 problem="<p>Electricity is billed in slabs: the first 100 units at Rs 3, the next 200 units (101–300) at Rs 5, and anything above 300 at Rs 8. Compute the bill for 380 units.</p>",
 inp="380 units",
 approach=["If units ≤ 100: units × 3.",
           "Else if ≤ 300: 100 × 3 + (units − 100) × 5.",
           "Else: full first two slabs + (units − 300) × 8."],
 code='''public class Main {
    public static void main(String[] args) {
        int units = 380;
        int bill;
        if (units <= 100) {
            bill = units * 3;
        } else if (units <= 300) {
            bill = 100 * 3 + (units - 100) * 5;
        } else {
            bill = 100 * 3 + 200 * 5 + (units - 300) * 8;
        }
        System.out.println(units + " units: Rs " + bill);
    }
}
''', notes={10: "Top slab :: = 300 + 1000 + 80 × 8 = 1940. <code>bill</code> was declared without a value; the compiler accepts it because every branch assigns it before it's used."},
 tryit="Press <b>Run</b>. Then try 100, 101 and 300 units: the boundaries are where slab bugs hide. (Illustrative tariff.)"),
]
