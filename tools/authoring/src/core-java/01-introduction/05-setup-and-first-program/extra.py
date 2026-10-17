WORKED_INTRO = "Your first programs mostly print. These three show the printing tools you'll use for years: <code>println</code> vs <code>print</code>, escape sequences like <code>\\t</code> and <code>\\n</code>, and the <code>args</code> array that receives command-line input."
EXAMPLES = [
dict(tag="Railways · tickets", title="Print a train ticket with tabs and new lines",
 problem="<p>Print a small train ticket with labels lined up in columns. Use <code>\\t</code> (tab) to align and <code>\\n</code> to start new lines inside one string.</p>",
 inp="PNR 4521789630, train 12123 Deccan Queen, coach C2 seat 34",
 approach=["<code>\\t</code> moves to the next tab stop; <code>\\n</code> starts a new line.",
           "Build the ticket with a few <code>println</code> calls.",
           "Use <code>\\\"</code> to print double quotes inside a string."],
 code='''public class Main {
    public static void main(String[] args) {
        System.out.println("==== E-TICKET ====");
        System.out.println("PNR:\\t4521789630");
        System.out.println("Train:\\t12123 \\"Deccan Queen\\"");
        System.out.println("Coach:\\tC2\\nSeat:\\t34");
        System.out.println("==================");
    }
}
''', notes={4: "Tab :: = <code>\\t</code> prints a tab character, so the value starts at the next tab stop.",
            5: "Quotes :: = <code>\\\"</code> puts a double quote inside a string without ending it.",
            6: "Two lines :: = <code>\\n</code> inside the string starts a new line, so one println prints two lines."},
 tryit="Press <b>Run</b>. Then add a line for the date of journey."),
dict(tag="Shop · receipts", title="print vs println on one receipt line",
 problem="<p>A shop prints each item, its quantity and price on one line, building it piece by piece. Use <code>print</code> (stays on the same line) and finish each line with <code>println</code>.</p>",
 inp="Pen × 3 Rs 30, Notebook × 2 Rs 90",
 approach=["<code>System.out.print</code> prints without a line break.",
           "<code>System.out.println()</code> ends the line.",
           "Print a total at the end."],
 code='''public class Main {
    public static void main(String[] args) {
        System.out.print("Pen");
        System.out.print(" x3 ");
        System.out.println("Rs 30");
        System.out.print("Notebook");
        System.out.print(" x2 ");
        System.out.println("Rs 90");
        System.out.println("Total Rs " + (30 + 90));
    }
}
''', notes={3: "print :: = Prints \"Pen\" and stays on the same line.",
            5: "println :: = Prints \"Rs 30\" and then moves to a new line."},
 tryit="Press <b>Run</b>. Then change one <code>println</code> to <code>print</code> and see the lines join."),
dict(tag="Command line · args", title="How many arguments did the program get?",
 problem="<p>When you run <code>java Main</code> from a terminal, extra words after it arrive in the <code>args</code> array. This run has none. Print how many arguments arrived and what <code>args</code> is.</p>",
 inp="run as: java Main (no extra words)",
 approach=["<code>args</code> is a <code>String[]</code> created by the JVM before main starts.",
           "<code>args.length</code> is the number of words passed.",
           "With no words, it's an empty array (length 0), not null."],
 code='''public class Main {
    public static void main(String[] args) {
        System.out.println("Arguments received: " + args.length);
        System.out.println("Is args null? " + (args == null));
        System.out.println("Try: java Main Asha 3");
    }
}
''', notes={3: "Count :: = The JVM always passes an array. Run without words, it has 0 elements.",
            4: "Not null :: = An empty array is still an object, so <code>args == null</code> is false."},
 tryit="Press <b>Run</b>. On your own computer, run <code>java Main Asha 3</code> and print <code>args[0]</code>."),
]

PRACTICE_INTRO = "Practise printing exactly what you want: lines, tabs, quotes and numbers. Every output is fixed. The last three are business tasks."
PROBLEMS = [
dict(level="easy", title="Hello on three lines", stmt="<p>Print Hello, Namaste and Vanakkam on three lines with one println.</p>", inp="(none)",
 code='''public class Main {
    public static void main(String[] args) {
        System.out.println("Hello\\nNamaste\\nVanakkam");
    }
}''', explain="<p><b>How it works:</b> each <code>\\n</code> starts a new line.</p>"),
dict(level="easy", title="Print quotes", stmt="<p>Print: She said \"Java is easy\".</p>", inp="(none)",
 code='''public class Main {
    public static void main(String[] args) {
        System.out.println("She said \\"Java is easy\\".");
    }
}''', explain="<p><b>How it works:</b> <code>\\\"</code> is the escape for a double quote.</p>"),
dict(level="easy", title="print on one line", stmt="<p>Print 1 2 3 on one line using three <code>print</code> calls, then end the line.</p>", inp="(none)",
 code='''public class Main {
    public static void main(String[] args) {
        System.out.print("1 ");
        System.out.print("2 ");
        System.out.print("3");
        System.out.println();
    }
}''', explain="<p><b>How it works:</b> <code>println()</code> with no argument just ends the line.</p>"),
dict(level="medium", title="A tabbed table", stmt="<p>Print a 2-row table with columns Item and Price, separated by tabs.</p>", inp="Tea 15, Coffee 25",
 code='''public class Main {
    public static void main(String[] args) {
        System.out.println("Item\\tPrice");
        System.out.println("Tea\\t15");
        System.out.println("Coffee\\t25");
    }
}''', explain="<p><b>How it works:</b> tabs line up short columns; for perfect alignment you'll later use <code>printf</code>.</p>"),
dict(level="medium", title="Print a backslash", stmt="<p>Print the Windows path C:\\Java\\bin.</p>", inp="(none)",
 code='''public class Main {
    public static void main(String[] args) {
        System.out.println("C:\\\\Java\\\\bin");
    }
}''', explain="<p><b>How it works:</b> a single backslash starts an escape, so a real backslash is written <code>\\\\</code>.</p>"),
dict(level="business", title="Shop banner", stmt="<p>Print a 3-line banner for \"Sharma General Store\" with a line of = signs above and below.</p>", inp="(none)",
 code='''public class Main {
    public static void main(String[] args) {
        System.out.println("========================");
        System.out.println("  Sharma General Store");
        System.out.println("========================");
    }
}''', explain="<p><b>How it works:</b> small banners like this are common in receipts and console tools.</p>"),
dict(level="business", title="Bill with print and println", stmt="<p>Print \"Total: Rs 450\" by printing the label, then the amount, then ending the line.</p>", inp="450",
 code='''public class Main {
    public static void main(String[] args) {
        int total = 450;
        System.out.print("Total: Rs ");
        System.out.println(total);
    }
}''', explain="<p><b>How it works:</b> print and println accept numbers as well as text.</p>"),
dict(level="business", title="Argument count check", stmt="<p>A billing tool expects 2 arguments (customer and amount). Print how many it got and how many are missing.</p>", inp="run with no arguments",
 code='''public class Main {
    public static void main(String[] args) {
        System.out.println("Got " + args.length + " of 2 arguments");
        System.out.println("Missing: " + (2 - args.length));
    }
}''', explain="<p><b>How it works:</b> real command-line tools check <code>args.length</code> first and print usage help if something is missing.</p>"),
]
