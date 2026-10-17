WORKED_INTRO = "Your .java file is compiled to bytecode once, and the JVM runs it statement by statement. In these three programs, watch the order: each line runs only after the one before it, and every method call gets its own frame on the stack."
EXAMPLES = [
dict(tag="Tea stall · sales", title="A tea stall's daily income",
 problem="<p>A tea stall sells 140 cups of chai at Rs 12 and 60 samosas at Rs 15. Its daily cost is Rs 1,100. Print the income, the cost and the profit.</p>",
 inp="140 chai × 12, 60 samosa × 15, cost 1100",
 approach=["Compute the income from each item.",
           "Add them and subtract the cost.",
           "Each statement uses values computed by the lines above it: order matters."],
 code='''public class Main {
    public static void main(String[] args) {
        int chaiIncome = 140 * 12;
        int samosaIncome = 60 * 15;
        int income = chaiIncome + samosaIncome;
        int cost = 1100;
        int profit = income - cost;
        System.out.println("Income: Rs " + income);
        System.out.println("Profit: Rs " + profit);
    }
}
''', notes={5: "Uses earlier lines :: = <code>income</code> can only be computed now, because the two lines above have already run.",
            7: "Profit :: = 2580 − 1100 = 1480."},
 tryit="Press <b>Run</b>. Then move the <code>profit</code> line above the <code>cost</code> line and read the compile error: the compiler checks order before anything runs."),
dict(tag="Retail · GST", title="A method call gets its own stack frame",
 problem="<p>A shop needs the price including 18% GST for two items. Put the calculation in a method <code>withGst</code> and call it twice. Watch a new frame appear on the stack for each call.</p>",
 inp="prices 500 and 1200",
 approach=["Write <code>static int withGst(int price)</code> that returns price × 118 / 100.",
           "Call it from main for each price.",
           "The method's frame is pushed when called and popped when it returns."],
 code='''public class Main {
    static int withGst(int price) {
        int total = price * 118 / 100;
        return total;
    }

    public static void main(String[] args) {
        int bag = withGst(500);
        int shoes = withGst(1200);
        System.out.println("Bag: Rs " + bag);
        System.out.println("Shoes: Rs " + shoes);
    }
}
''', notes={(8, 1): "Call :: = main calls <code>withGst(500)</code>. The JVM pushes a new frame for it, with its own <code>price</code>.",
            (3, 1): "Inside the method :: = 500 × 118 / 100 = 590, stored in the method's local <code>total</code>.",
            (4, 1): "Return :: = The method returns 590; its frame is popped and <code>bag</code> gets the value.",
            (9, 1): "Again :: = A fresh frame for the second call; nothing is left over from the first."},
 tryit="Press <b>Run</b>. Then call <code>withGst</code> for a third price."),
dict(tag="Weather · conversion", title="Celsius to Fahrenheit, step by step",
 problem="<p>A weather display stores temperatures in Celsius but must also show Fahrenheit: F = C × 9 / 5 + 32. Convert 37.5 °C and print both.</p>",
 inp="37.5 °C",
 approach=["Store the Celsius value as a <code>double</code>.",
           "Apply the formula; Java follows the usual order: × and / before +.",
           "Print both values."],
 code='''public class Main {
    public static void main(String[] args) {
        double celsius = 37.5;
        double fahrenheit = celsius * 9 / 5 + 32;
        System.out.println(celsius + " C = " + fahrenheit + " F");
    }
}
''', notes={4: "Order of operations :: = 37.5 × 9 = 337.5, ÷ 5 = 67.5, + 32 = 99.5."},
 tryit="Press <b>Run</b>. Then convert 100 °C."),
]

PRACTICE_INTRO = "Programs whose results depend on the order statements run in. Trace each one in your head before running it. The last three are business tasks."
PROBLEMS = [
dict(level="easy", title="Swap the order", stmt="<p>Print \"Step 1\", \"Step 2\", \"Step 3\" on separate lines.</p>", inp="(none)",
 code='''public class Main {
    public static void main(String[] args) {
        System.out.println("Step 1");
        System.out.println("Step 2");
        System.out.println("Step 3");
    }
}''', explain="<p><b>How it works:</b> statements in main run from top to bottom, one at a time.</p>"),
dict(level="easy", title="Update a variable", stmt="<p>Start with 10 points, add 5, then double it, then print.</p>", inp="10",
 code='''public class Main {
    public static void main(String[] args) {
        int points = 10;
        points = points + 5;
        points = points * 2;
        System.out.println(points);
    }
}''', explain="<p><b>How it works:</b> each line uses the value left by the line before: 10 → 15 → 30.</p>"),
dict(level="easy", title="Rectangle area", stmt="<p>Print the area of a 12 × 8 room.</p>", inp="12, 8",
 code='''public class Main {
    public static void main(String[] args) {
        int length = 12;
        int width = 8;
        System.out.println("Area: " + length * width + " sq ft");
    }
}''', explain="<p><b>How it works:</b> multiplication happens before joining with text.</p>"),
dict(level="medium", title="Call a method twice", stmt="<p>Write <code>static int square(int n)</code> and print the squares of 6 and 9.</p>", inp="6, 9",
 code='''public class Main {
    static int square(int n) {
        return n * n;
    }

    public static void main(String[] args) {
        System.out.println(square(6));
        System.out.println(square(9));
    }
}''', explain="<p><b>How it works:</b> each call gets its own frame with its own <code>n</code>.</p>"),
dict(level="medium", title="Precedence puzzle", stmt="<p>Print the values of <code>2 + 3 * 4</code> and <code>(2 + 3) * 4</code>.</p>", inp="(none)",
 code='''public class Main {
    public static void main(String[] args) {
        System.out.println(2 + 3 * 4);
        System.out.println((2 + 3) * 4);
    }
}''', explain="<p><b>How it works:</b> * runs before +, unless brackets say otherwise.</p>"),
dict(level="business", title="Petrol cost of a trip", stmt="<p>A car gives 15 km per litre. Petrol costs Rs 105. Print the cost of a 360 km trip.</p>", inp="360 km, 15 km/l, Rs 105/l",
 code='''public class Main {
    public static void main(String[] args) {
        double litres = 360 / 15.0;
        double cost = litres * 105;
        System.out.println("Litres: " + litres);
        System.out.println("Cost: Rs " + cost);
    }
}''', explain="<p><b>How it works:</b> dividing by 15.0 keeps decimals. (Illustrative price.)</p>"),
dict(level="business", title="Simple interest", stmt="<p>Print the simple interest on Rs 25,000 at 8% for 2 years (P × R × T / 100).</p>", inp="25000, 8, 2",
 code='''public class Main {
    public static void main(String[] args) {
        int p = 25000, r = 8, t = 2;
        System.out.println("Interest: Rs " + p * r * t / 100);
    }
}''', explain="<p><b>How it works:</b> several variables of the same type can be declared on one line.</p>"),
dict(level="business", title="Cost per student", stmt="<p>A college trip costs Rs 48,600 for a bus and Rs 350 per student for food. Print the total for 54 students and the cost per student.</p>", inp="54 students",
 code='''public class Main {
    static int total(int students) {
        return 48600 + students * 350;
    }

    public static void main(String[] args) {
        int t = total(54);
        System.out.println("Total: Rs " + t);
        System.out.println("Per student: Rs " + t / 54);
    }
}''', explain="<p><b>How it works:</b> 48600 + 18900 = 67500; 67500 / 54 = 1250.</p>"),
]
