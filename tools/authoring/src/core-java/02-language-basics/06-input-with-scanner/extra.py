WORKED_INTRO = "Real programs read input. Each program below reads from the keyboard with <code>Scanner</code>; the trace and the runner feed it the sample input shown. Watch each <code>next…()</code> call take the next piece of input and store it in a variable."
EXAMPLES = [
dict(tag="Grocery · billing", title="Read an item, quantity and price",
 problem="<p>A grocery counter types the item name, quantity and unit price. Print a bill line with the amount.</p>",
 inp="Basmati Rice\n3\n92.50",
 stdin="Basmati Rice\n3\n92.50\n",
 approach=["<code>nextLine()</code> reads the whole first line (names can have spaces).",
           "<code>nextInt()</code> and <code>nextDouble()</code> read numbers.",
           "Multiply and print."],
 code='''import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String item = sc.nextLine();
        int qty = sc.nextInt();
        double price = sc.nextDouble();
        double amount = qty * price;
        System.out.println(item + " x" + qty + " = Rs " + amount);
        sc.close();
    }
}
''', notes={5: "Scanner :: = A Scanner object wraps <code>System.in</code> (the keyboard).",
            6: "Line :: = <code>nextLine()</code> reads up to the end of the line, spaces included: \"Basmati Rice\".",
            7: "Number :: = <code>nextInt()</code> reads the next whole number: 3.",
            8: "Decimal :: = <code>nextDouble()</code> reads 92.5."},
 tryit="Press <b>Run</b> (the sample input is filled in). Then change the input to your own item."),
dict(tag="Education · marks", title="Average of three subjects",
 problem="<p>A teacher enters a student's name and three marks on one line. Print the total and the average with one decimal.</p>",
 inp="Ravi 78 85 91",
 stdin="Ravi 78 85 91\n",
 approach=["<code>next()</code> reads one word.",
           "Three <code>nextInt()</code> calls read the marks from the same line.",
           "<code>printf(\"%.1f\")</code> shows one decimal."],
 code='''import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String name = sc.next();
        int m1 = sc.nextInt();
        int m2 = sc.nextInt();
        int m3 = sc.nextInt();
        int total = m1 + m2 + m3;
        System.out.printf("%s: total %d, average %.1f%n", name, total, total / 3.0);
        sc.close();
    }
}
''', notes={6: "Word :: = <code>next()</code> stops at the first space: \"Ravi\".",
            9: "Same line :: = Tokens are separated by spaces, so all three marks can be on one line.",
            11: "printf :: = <code>%.1f</code> prints 84.666… as 84.7."},
 tryit="Press <b>Run</b>. Then put each mark on its own line in the input: the program still works."),
dict(tag="Banking · forms", title="The nextInt + nextLine trap",
 problem="<p>A bank form reads an account number (a number) and then the holder's full name (a line). Read naively, the name comes out empty, because <code>nextInt()</code> leaves the Enter key in the input. Show the fix: an extra <code>nextLine()</code>.</p>",
 inp="40021876\nAsha Kumari Verma",
 stdin="40021876\nAsha Kumari Verma\n",
 approach=["<code>nextInt()</code> reads 40021876 but not the line break after it.",
           "One <code>nextLine()</code> consumes that leftover line break.",
           "The next <code>nextLine()</code> reads the real name."],
 code='''import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int account = sc.nextInt();
        String leftover = sc.nextLine();
        String name = sc.nextLine();
        System.out.println("Account: " + account);
        System.out.println("Leftover was [" + leftover + "]");
        System.out.println("Holder: " + name);
        sc.close();
    }
}
''', notes={6: "Number :: = Reads 40021876. The line break after it is still waiting in the input.",
            7: "The trap :: = This <code>nextLine()</code> reads only that leftover line break, so <code>leftover</code> is an empty string. Without this line, <code>name</code> would be empty.",
            8: "Real line :: = Now the name is read correctly."},
 tryit="Press <b>Run</b>. Then delete the <code>leftover</code> line (and its println) and see the name come out empty."),
]

PRACTICE_INTRO = "Read input with Scanner and compute something with it. Each problem's sample input is used when you run it. The last three are business tasks."
PROBLEMS = [
dict(level="easy", title="Greet by name", stmt="<p>Read a name and print \"Hello, NAME!\".</p>", inp="Meena", stdin="Meena\n",
 code='''import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String name = sc.nextLine();
        System.out.println("Hello, " + name + "!");
    }
}''', explain="<p><b>How it works:</b> nextLine reads the whole line typed.</p>"),
dict(level="easy", title="Sum of two numbers", stmt="<p>Read two integers and print their sum.</p>", inp="25 17", stdin="25 17\n",
 code='''import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int a = sc.nextInt(), b = sc.nextInt();
        System.out.println(a + b);
    }
}''', explain="<p><b>How it works:</b> nextInt skips spaces and reads one number at a time.</p>"),
dict(level="easy", title="Square of a decimal", stmt="<p>Read a decimal number and print its square.</p>", inp="2.5", stdin="2.5\n",
 code='''import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        double x = sc.nextDouble();
        System.out.println(x * x);
    }
}''', explain="<p><b>How it works:</b> nextDouble reads numbers with decimals.</p>"),
dict(level="medium", title="Rectangle from input", stmt="<p>Read length and width, print area and perimeter.</p>", inp="12 7", stdin="12 7\n",
 code='''import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int l = sc.nextInt(), w = sc.nextInt();
        System.out.println("Area " + l * w + ", perimeter " + 2 * (l + w));
    }
}''', explain="<p><b>How it works:</b> read once, use many times.</p>"),
dict(level="medium", title="Number then sentence", stmt="<p>Read a roll number, then a full name on the next line, and print both.</p>", inp="17\nKiran Rao", stdin="17\nKiran Rao\n",
 code='''import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int roll = sc.nextInt();
        sc.nextLine();
        String name = sc.nextLine();
        System.out.println(roll + ": " + name);
    }
}''', explain="<p><b>How it works:</b> the extra nextLine() eats the line break left by nextInt.</p>"),
dict(level="business", title="Bill with GST from input", stmt="<p>Read an amount and print the GST (18%) and total.</p>", inp="1250", stdin="1250\n",
 code='''import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        double amount = sc.nextDouble();
        double gst = amount * 0.18;
        System.out.println("GST: Rs " + gst + ", total: Rs " + (amount + gst));
    }
}''', explain="<p><b>How it works:</b> the same program now works for any amount typed in.</p>"),
dict(level="business", title="Fuel bill", stmt="<p>Read litres and price per litre; print the bill rounded to the rupee.</p>", inp="23.5 104.7", stdin="23.5 104.7\n",
 code='''import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        double litres = sc.nextDouble(), rate = sc.nextDouble();
        System.out.println("Pay Rs " + Math.round(litres * rate));
    }
}''', explain="<p><b>How it works:</b> 23.5 × 104.7 = 2460.45, rounded to 2460.</p>"),
dict(level="business", title="Customer details card", stmt="<p>Read a customer's name (line), age and city, then print a one-line card.</p>", inp="Asha Verma\n29 Pune", stdin="Asha Verma\n29 Pune\n",
 code='''import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String name = sc.nextLine();
        int age = sc.nextInt();
        String city = sc.next();
        System.out.println(name + " (" + age + "), " + city);
    }
}''', explain="<p><b>How it works:</b> nextLine for the full name first avoids the leftover-line-break problem.</p>"),
]
