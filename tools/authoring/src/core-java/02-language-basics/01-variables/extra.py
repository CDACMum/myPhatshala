WORKED_INTRO = "Variables are named boxes on the stack. In these three programs, watch each box appear when it's declared, change when it's assigned, and disappear when its block ends."
EXAMPLES = [
dict(tag="Wallet · payments", title="A digital wallet's balance through the day",
 problem="<p>A student's wallet starts with Rs 500. She pays Rs 120 for lunch, gets Rs 200 cashback, then pays Rs 45 for a bus ticket. Track the balance in one variable and print it after each step.</p>",
 inp="start 500; −120, +200, −45",
 approach=["Declare <code>balance</code> once with the starting amount.",
           "Reassign it after each transaction.",
           "Print the running balance."],
 code='''public class Main {
    public static void main(String[] args) {
        int balance = 500;
        balance = balance - 120;
        System.out.println("After lunch: Rs " + balance);
        balance = balance + 200;
        System.out.println("After cashback: Rs " + balance);
        balance = balance - 45;
        System.out.println("After bus ticket: Rs " + balance);
    }
}
''', notes={3: "Declare :: = A new box <code>balance</code> appears on main's stack holding 500.",
            4: "Reassign :: = The right side is computed first (500 − 120), then the result replaces the old value.",
            6: "Same box :: = No new variable is created; the same box now holds 580."},
 tryit="Press <b>Run</b>. Then add a recharge of Rs 99 at the end."),
dict(tag="Retail · constants", title="A GST rate that must never change by accident",
 problem="<p>A billing program uses the 18% GST rate in several places. Store it in a <code>final</code> variable so nobody can change it by mistake, and compute the GST on two bills.</p>",
 inp="bills 1200 and 350",
 approach=["<code>final double GST = 0.18;</code>: assigned once, then locked.",
           "Use it in two calculations.",
           "Any later <code>GST = ...</code> would be a compile error."],
 code='''public class Main {
    public static void main(String[] args) {
        final double GST = 0.18;
        double bill1 = 1200;
        double bill2 = 350;
        System.out.println("GST on bill 1: Rs " + bill1 * GST);
        System.out.println("GST on bill 2: Rs " + bill2 * GST);
    }
}
''', notes={3: "final :: = The variable gets its value once. The compiler will reject any second assignment.",
            6: "Use :: = 1200 × 0.18 = 216.0."},
 tryit="Press <b>Run</b>. Then add <code>GST = 0.12;</code> on the next line and read the compile error."),
dict(tag="Logistics · swap", title="Swap two delivery slots",
 problem="<p>A delivery app shows two slots, 10 AM and 4 PM. The customer wants them swapped. Swap the values of two variables using a temporary variable inside a block, and show that <code>temp</code> disappears after the block.</p>",
 inp="first = 10, second = 16",
 approach=["Copy the first value into <code>temp</code>.",
           "Copy second into first, then temp into second.",
           "<code>temp</code> is declared inside <code>{ }</code>, so it exists only there."],
 code='''public class Main {
    public static void main(String[] args) {
        int first = 10;
        int second = 16;
        {
            int temp = first;
            first = second;
            second = temp;
        }
        System.out.println("First slot: " + first + ":00");
        System.out.println("Second slot: " + second + ":00");
    }
}
''', notes={6: "Temporary :: = <code>temp</code> appears on the stack, holding a copy of 10.",
            7: "Overwrite :: = first becomes 16. Without temp, the 10 would now be lost.",
            8: "Restore :: = second gets the saved 10.",
            10: "Block ended :: <code>temp</code> is gone from the stack: its scope was the block."},
 tryit="Press <b>Run</b>. Then try to print <code>temp</code> after the block and read the error."),
]

PRACTICE_INTRO = "Declare, assign and update variables, and use <code>final</code> for values that must not change. Every output is fixed. The last three are business tasks."
PROBLEMS = [
dict(level="easy", title="Declare and print", stmt="<p>Store your age (19) and city (Nagpur) in variables and print them.</p>", inp="19, Nagpur",
 code='''public class Main {
    public static void main(String[] args) {
        int age = 19;
        String city = "Nagpur";
        System.out.println(age + " years, from " + city);
    }
}''', explain="<p><b>How it works:</b> each variable has a type, a name and a value.</p>"),
dict(level="easy", title="Update a score", stmt="<p>A quiz score starts at 0. Add 10 three times and print it.</p>", inp="(none)",
 code='''public class Main {
    public static void main(String[] args) {
        int score = 0;
        score = score + 10;
        score = score + 10;
        score = score + 10;
        System.out.println("Score: " + score);
    }
}''', explain="<p><b>How it works:</b> a variable can be reassigned as often as you like (unless it's final).</p>"),
dict(level="easy", title="Use a constant", stmt="<p>Declare <code>final int DAYS_IN_WEEK = 7;</code> and print the number of days in 6 weeks.</p>", inp="6 weeks",
 code='''public class Main {
    public static void main(String[] args) {
        final int DAYS_IN_WEEK = 7;
        System.out.println(6 * DAYS_IN_WEEK);
    }
}''', explain="<p><b>How it works:</b> constants make code self-explaining: 6 * DAYS_IN_WEEK reads better than 6 * 7.</p>"),
dict(level="medium", title="Swap without temp (arithmetic)", stmt="<p>Swap a = 5 and b = 9 using only + and −.</p>", inp="5, 9",
 code='''public class Main {
    public static void main(String[] args) {
        int a = 5, b = 9;
        a = a + b;
        b = a - b;
        a = a - b;
        System.out.println("a = " + a + ", b = " + b);
    }
}''', explain="<p><b>How it works:</b> a becomes 14, then b = 14 − 9 = 5, then a = 14 − 5 = 9. A temp variable is clearer in real code.</p>"),
dict(level="medium", title="Scope of a block", stmt="<p>Declare <code>total</code> outside a block and <code>tip</code> inside it; add the tip to the total inside the block and print total afterwards.</p>", inp="total 400, tip 40",
 code='''public class Main {
    public static void main(String[] args) {
        int total = 400;
        {
            int tip = 40;
            total = total + tip;
        }
        System.out.println("Total with tip: " + total);
    }
}''', explain="<p><b>How it works:</b> code inside a block can use variables from outside it; variables declared inside vanish when it ends.</p>"),
dict(level="business", title="Stock after sales", stmt="<p>A shop has 50 units. It sells 12, receives 30, sells 25. Print the stock after each step.</p>", inp="50; −12, +30, −25",
 code='''public class Main {
    public static void main(String[] args) {
        int stock = 50;
        stock = stock - 12;
        System.out.println("After sale: " + stock);
        stock = stock + 30;
        System.out.println("After delivery: " + stock);
        stock = stock - 25;
        System.out.println("After sale: " + stock);
    }
}''', explain="<p><b>How it works:</b> one variable tracks a running value, the basis of inventory systems.</p>"),
dict(level="business", title="Discount with a constant", stmt="<p>A store gives a fixed 15% member discount. Print the price after discount for items costing Rs 2,000 and Rs 640.</p>", inp="2000, 640",
 code='''public class Main {
    public static void main(String[] args) {
        final double MEMBER_DISCOUNT = 0.15;
        System.out.println("Rs " + 2000 * (1 - MEMBER_DISCOUNT));
        System.out.println("Rs " + 640 * (1 - MEMBER_DISCOUNT));
    }
}''', explain="<p><b>How it works:</b> changing the discount later needs one edit.</p>"),
dict(level="business", title="Monthly savings", stmt="<p>Salary Rs 32,000; rent Rs 9,500; food Rs 6,000; travel Rs 2,500. Print savings.</p>", inp="as given",
 code='''public class Main {
    public static void main(String[] args) {
        int salary = 32000;
        int rent = 9500, food = 6000, travel = 2500;
        int savings = salary - rent - food - travel;
        System.out.println("Savings: Rs " + savings);
    }
}''', explain="<p><b>How it works:</b> well-named variables make the calculation read like the sentence it comes from.</p>"),
]
