WORKED_INTRO = "Three tiny programs of the kind Java runs every day in shops, banks and phones. Each one uses only what you have seen so far: <code>println</code>, a few variables and arithmetic. Run them, then step through to see each value appear on main's stack."
EXAMPLES = [
dict(tag="Canteen · billing", title="Print a canteen bill",
 problem="<p>A college canteen wants its counter computer to print a simple bill: two items with prices, and the total. Write a Java program that stores the prices in variables, adds them, and prints the bill.</p>",
 inp="Masala dosa Rs 60, Filter coffee Rs 25",
 approach=["Store each price in an <code>int</code> variable.",
           "Add them into a <code>total</code> variable.",
           "Print each line with <code>System.out.println</code>, joining text and numbers with <code>+</code>."],
 code='''public class Main {
    public static void main(String[] args) {
        int dosa = 60;
        int coffee = 25;
        int total = dosa + coffee;
        System.out.println("--- Canteen Bill ---");
        System.out.println("Masala dosa   Rs " + dosa);
        System.out.println("Filter coffee Rs " + coffee);
        System.out.println("Total         Rs " + total);
    }
}
''', notes={3: "Price :: = A variable <code>dosa</code> appears on main's stack with the value 60.",
            5: "Add :: = The JVM adds 60 + 25 and stores 85 in <code>total</code>.",
            9: "Print :: <code>\"Total ... Rs \" + total</code> joins the text and the number into one line."},
 tryit="Press <b>Run</b>. Then add a third item, Vada Rs 30, and update the total."),
dict(tag="Fitness · steps", title="How many steps are left today?",
 problem="<p>A fitness app sets a daily goal of 8,000 steps. The phone has counted 5,340 so far. Print the steps walked, the steps remaining and the percentage completed.</p>",
 inp="goal 8000, walked 5340",
 approach=["Store the goal and the steps walked.",
           "Remaining = goal − walked.",
           "Percentage = walked × 100 / goal (whole-number division)."],
 code='''public class Main {
    public static void main(String[] args) {
        int goal = 8000;
        int walked = 5340;
        int remaining = goal - walked;
        int percent = walked * 100 / goal;
        System.out.println("Walked: " + walked + " steps");
        System.out.println("Remaining: " + remaining + " steps");
        System.out.println("Done: " + percent + "%");
    }
}
''', notes={5: "Subtract :: = 8000 − 5340 = 2660.",
            6: "Percent :: = 5340 × 100 = 534000, divided by 8000 gives 66. Dividing two ints keeps only the whole part (66.75 becomes 66)."},
 tryit="Press <b>Run</b>. Then change <code>walked</code> to 8000 and check the output says 100%."),
dict(tag="Telecom · SMS", title="How many SMS parts will this message need?",
 problem="<p>An SMS can carry 160 characters. A bank wants to know how many characters its OTP message has, and how many 160-character parts it needs.</p>",
 inp="message: \"Your OTP for login is 482913. Do not share it with anyone. Valid for 5 minutes.\"",
 approach=["Store the message in a <code>String</code>.",
           "<code>message.length()</code> gives the number of characters.",
           "Parts = (length + 159) / 160 rounds up using whole-number division."],
 code='''public class Main {
    public static void main(String[] args) {
        String message = "Your OTP for login is 482913. Do not share it with anyone. Valid for 5 minutes.";
        int length = message.length();
        int parts = (length + 159) / 160;
        System.out.println("Characters: " + length);
        System.out.println("SMS parts needed: " + parts);
    }
}
''', notes={3: "Text :: = A String object is created on the heap; the variable <code>message</code> on the stack points to it.",
            4: "Length :: = <code>length()</code> counts the characters.",
            5: "Round up :: = Adding 159 before dividing by 160 rounds up: any message from 1 to 160 characters needs 1 part."},
 tryit="Press <b>Run</b>. Then make the message longer than 160 characters and watch the parts become 2."),
]

PRACTICE_INTRO = "Short programs that use <code>println</code>, variables and arithmetic. Every output is fixed, so you can check yours exactly. The last three are small business tasks."
PROBLEMS = [
dict(level="easy", title="Print your name and city", stmt="<p>Print two lines: your name, then your city.</p>", inp="(none)",
 code='''public class Main {
    public static void main(String[] args) {
        System.out.println("Name: Riya Sharma");
        System.out.println("City: Pune");
    }
}''', explain="<p><b>How it works:</b> each <code>println</code> prints its text and moves to a new line.</p>"),
dict(level="easy", title="Add two numbers", stmt="<p>Store 45 and 30 in two variables and print their sum.</p>", inp="45, 30",
 code='''public class Main {
    public static void main(String[] args) {
        int a = 45;
        int b = 30;
        System.out.println("Sum = " + (a + b));
    }
}''', explain="<p><b>How it works:</b> the brackets make Java add the numbers first. Without them, <code>\"Sum = \" + a + b</code> would print <code>Sum = 4530</code>.</p>"),
dict(level="easy", title="Hours in a week", stmt="<p>Print how many hours there are in a week.</p>", inp="7 days × 24 hours",
 code='''public class Main {
    public static void main(String[] args) {
        int days = 7;
        int hoursPerDay = 24;
        System.out.println("Hours in a week: " + days * hoursPerDay);
    }
}''', explain="<p><b>How it works:</b> <code>*</code> runs before <code>+</code>, so the multiplication happens first.</p>"),
dict(level="medium", title="Minutes to hours and minutes", stmt="<p>A movie is 155 minutes long. Print it as hours and minutes.</p>", inp="155",
 code='''public class Main {
    public static void main(String[] args) {
        int total = 155;
        System.out.println(total / 60 + " h " + total % 60 + " min");
    }
}''', explain="<p><b>How it works:</b> <code>/</code> between ints gives the whole part (2); <code>%</code> gives the remainder (35).</p>"),
dict(level="medium", title="Average of three marks", stmt="<p>Print the average of 78, 85 and 92 with decimals.</p>", inp="78, 85, 92",
 code='''public class Main {
    public static void main(String[] args) {
        int sum = 78 + 85 + 92;
        double avg = sum / 3.0;
        System.out.println("Average: " + avg);
    }
}''', explain="<p><b>How it works:</b> dividing by <code>3.0</code> (a decimal) keeps the fraction; dividing by <code>3</code> would give 85.</p>"),
dict(level="business", title="Auto-rickshaw fare", stmt="<p>Fare is Rs 26 for the first 1.5 km and Rs 17 per km after that. Print the fare for a 6 km ride (4.5 extra km).</p>", inp="6 km",
 code='''public class Main {
    public static void main(String[] args) {
        double extraKm = 6 - 1.5;
        double fare = 26 + extraKm * 17;
        System.out.println("Fare: Rs " + fare);
    }
}''', explain="<p><b>How it works:</b> real fare meters do exactly this: a base fare plus a per-km rate. (Illustrative rates.)</p>"),
dict(level="business", title="Electricity bill", stmt="<p>A home used 240 units at Rs 7 per unit plus a fixed charge of Rs 100. Print the bill.</p>", inp="240 units",
 code='''public class Main {
    public static void main(String[] args) {
        int units = 240;
        int bill = units * 7 + 100;
        System.out.println("Units: " + units);
        System.out.println("Bill: Rs " + bill);
    }
}''', explain="<p><b>How it works:</b> variables make the rule easy to change later when the rate changes. (Illustrative tariff.)</p>"),
dict(level="business", title="Split a dinner bill", stmt="<p>Four friends share a bill of Rs 1,450. Print each person's share and what's left over if each pays a whole number of rupees.</p>", inp="1450, 4 people",
 code='''public class Main {
    public static void main(String[] args) {
        int bill = 1450;
        int people = 4;
        System.out.println("Each pays: Rs " + bill / people);
        System.out.println("Left over: Rs " + bill % people);
    }
}''', explain="<p><b>How it works:</b> 1450 / 4 = 362 (whole part) and 1450 % 4 = 2 rupees remaining, which someone has to cover.</p>"),
]
