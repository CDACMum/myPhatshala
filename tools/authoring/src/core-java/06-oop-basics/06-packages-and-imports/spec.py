import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../..'))
from mkanim import Anim

ANIM2_HEADING = "Watch it with an example: the class loader finds App by its address"
ANIM2_INTRO = "You type <code>java -cp out in.myphatshala.app.App</code>. Watch the JVM turn the package name into folders, find each class file, and load <code>FeeCalc</code> from another package only when <code>main</code> first needs it."
A = Anim("From a full class name to a .class file", frames=6, h=240, label="classpath lookup by package folders")
A.box(6, 14, 348, 28, "java -cp out in.myphatshala.app.App", fill="board", stroke="board", cls="chalk", mono=True, size=10.5)
tree = [("📁 out", 0, "1-"), ("📁 in", 1, "2-"), ("📁 myphatshala", 2, "2-"), ("📁 app", 3, "2-"), ("App.class", 4, "2-"), ("📁 fees", 3, "5-"), ("FeeCalc.class", 4, "5-")]
for i, (n, d, on) in enumerate(tree):
    y = 64 + i * 22
    A.text(14 + d * 16, y, n, size=10.5, mono=n.endswith(".class"), bold=n.endswith(".class"), on=on, cls="acc" if n.endswith(".class") else "ink")
A.box(72, 139, 74, 18, None, fill="none", stroke="green", sw=2.5, on="3", rx=4)
A.box(72, 183, 100, 18, None, fill="none", stroke="green", sw=2.5, on="5", rx=4)
A.box(196, 56, 158, 150, None, fill="soft-green", stroke="green")
A.text(206, 74, "JVM: loaded classes", size=10, bold=True, cls="green")
A.text(206, 96, "in.myphatshala.app.App", mono=True, size=9, on="3-")
A.text(206, 114, "main() running", mono=True, size=9, on="4-", cls="acc", bold=True)
A.text(206, 132, "in.myphatshala.fees.FeeCalc", mono=True, size=8.6, on="5-")
A.text(206, 154, "prints 5000", mono=True, size=10, on="6", bold=True, cls="green")
notes = {1: "start at the classpath root: out", 2: "dots become folders: in/myphatshala/app", 3: "App.class found and loaded",
         4: "main calls FeeCalc.monthly(60000)", 5: "FeeCalc's package → in/myphatshala/fees", 6: "two packages, one program"}
for f, t in notes.items(): A.text(180, 228, t, on=str(f), anchor="middle", size=10.5, bold=True)
A.caps([
 "<b>-cp out</b> tells the JVM where to start looking. The rest of the command is the class's full name.",
 "<b>Package to path:</b> the class loader replaces dots with folder separators: <code>in/myphatshala/app/App.class</code>.",
 "<b>Loaded:</b> it reads the file, checks that the class inside really is <code>in.myphatshala.app.App</code>, and loads it.",
 "<b>main runs</b> and reaches <code>FeeCalc.monthly(60000)</code>. The class file of App stores the full name <code>in/myphatshala/fees/FeeCalc</code>, thanks to the import.",
 "<b>Second lookup:</b> the same rule finds <code>out/in/myphatshala/fees/FeeCalc.class</code>. Classes are loaded on first use (Lesson 8.4).",
 "<b>Output:</b> 60000 / 12 = 5000. If any folder name didn't match its package, you'd get <code>ClassNotFoundException</code> or <code>NoClassDefFoundError</code> instead.",
])
ANIM2 = A

TRACE = dict(code='''import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;

public class Main {
    public static void main(String[] args) {
        LocalDate due = LocalDate.of(2025, 7, 15);
        List<String> items = new ArrayList<>();
        items.add("Tuition");
        items.add("Hostel");
        System.out.println(items + " due " + due);
    }
}
''', notes={7: "Object :: A <code>java.time.LocalDate</code> object. In the bytecode, the call names the class in full: <code>java/time/LocalDate.of</code>.",
 8: "Object :: <code>List</code> (java.util) is the variable's type; the object is a <code>java.util.ArrayList</code>.",
 9: "Add :: ", 10: "Add :: ", 11: "Print :: "}, end='main returns. The imports did their job at compile time; at run time only full class names were used.')

WORKED_INTRO = "Three small programs that use classes from several JDK packages. Each one needs the right imports, and one shows how to handle two classes with the same name."
EXAMPLES = [
dict(tag="College · attendance", title="Days until the exam",
 problem="<p>Show how many days are left until an exam, using classes from <code>java.time</code> and <code>java.time.temporal</code> (two separate packages).</p>",
 inp="today 2025-03-01, exam 2025-03-20",
 approach=["Import <code>java.time.LocalDate</code> for the dates.", "Import <code>java.time.temporal.ChronoUnit</code> for counting days.", "<code>ChronoUnit.DAYS.between(a, b)</code> returns a long."],
 code='''import java.time.LocalDate;
import java.time.temporal.ChronoUnit;

public class Main {
    public static void main(String[] args) {
        LocalDate today = LocalDate.of(2025, 3, 1);
        LocalDate exam = LocalDate.of(2025, 3, 20);
        long left = ChronoUnit.DAYS.between(today, exam);
        System.out.println("Exam on " + exam + ": " + left + " days left");
    }
}
''', notes={6: "Object :: ", 7: "Object :: ", 8: "Compute :: ", 9: "Print :: "},
 tryit="Press <b>Run</b>. Then delete the ChronoUnit import and read the error: the wildcard-free code can't find it."),
dict(tag="Banking · money", title="Exact money with BigDecimal, no import",
 problem="<p>Add Rs 0.10 and Rs 0.20 exactly. Use <code>java.math.BigDecimal</code> written by its full name, without any import line.</p>",
 inp="0.10 + 0.20",
 approach=["A fully qualified name works without an import.", "Create BigDecimals from Strings so the values are exact.", "Compare with <code>double</code> to see why this matters (Lesson 2.2)."],
 code='''public class Main {
    public static void main(String[] args) {
        java.math.BigDecimal a = new java.math.BigDecimal("0.10");
        java.math.BigDecimal b = new java.math.BigDecimal("0.20");
        java.math.BigDecimal sum = a.add(b);
        System.out.println("BigDecimal: " + sum);
        System.out.println("double:     " + (0.10 + 0.20));
    }
}
''', notes={3: "Object :: ", 4: "Object :: ", 5: "Add :: A new BigDecimal is created: these objects never change (like String).", 6: "Print :: ", 7: "Print :: "},
 tryit="Press <b>Run</b>. Then add <code>import java.math.BigDecimal;</code> and shorten the three lines."),
dict(tag="Data · reports", title="Two Date classes in one program",
 problem="<p>A report reads a <code>java.sql.Date</code> from a database row and also needs <code>java.util.Date</code>. Import one and write the other in full, then print both kinds.</p>",
 inp="DB date 2025-01-26",
 approach=["<code>import java.util.Date;</code> makes <code>Date</code> mean java.util.Date.", "Write <code>java.sql.Date</code> in full for the database value.", "<code>java.sql.Date.valueOf(\"2025-01-26\")</code> creates one from text."],
 code='''import java.util.Date;

public class Main {
    public static void main(String[] args) {
        java.sql.Date dbDate = java.sql.Date.valueOf("2025-01-26");
        Date utilDate = new Date(dbDate.getTime());
        System.out.println("from DB: " + dbDate);
        System.out.println("same instant as java.util.Date: " + (utilDate.getTime() == dbDate.getTime()));
    }
}
''', notes={5: "Object :: Full name: no import needed and no clash.", 6: "Object :: Here <code>Date</code> means java.util.Date, because of the import.", 7: "Print :: java.sql.Date prints just the date.", 8: "Print :: "},
 tryit="Press <b>Run</b>. Then add <code>import java.sql.Date;</code> as well and read the compile error."),
]

PRACTICE_INTRO = "Fix missing and clashing imports, and practise using classes from several packages. The last three are business tasks."
PROBLEMS = [
dict(level="easy", title="Add the missing import", stmt="<p>This program uses <code>ArrayList</code> without an import. Add a single-type import and print the list.</p>", inp="items Tea, Vada",
 code='''import java.util.ArrayList;

public class Main {
    public static void main(String[] args) {
        ArrayList<String> menu = new ArrayList<>();
        menu.add("Tea");
        menu.add("Vada");
        System.out.println(menu);
    }
}''', explain="<p><b>How it works:</b> without the import, javac reports <i>cannot find symbol: class ArrayList</i>. One line tells it the full name.</p>"),
dict(level="easy", title="Full name instead of import", stmt="<p>Print today's date pattern for a fixed date using <code>java.time.LocalDate</code> written in full, with no import line.</p>", inp="2025-08-15",
 code='''public class Main {
    public static void main(String[] args) {
        java.time.LocalDate d = java.time.LocalDate.of(2025, 8, 15);
        System.out.println(d + " is a " + d.getDayOfWeek());
    }
}''', explain="<p><b>How it works:</b> a fully qualified name always works. It's handy for one-off uses or when two classes share a simple name.</p>"),
dict(level="easy", title="Static import of a constant", stmt="<p>Use <code>import static java.lang.Math.PI;</code> to compute the area of a circular stage of radius 7 m.</p>", inp="r = 7",
 code='''import static java.lang.Math.PI;

public class Main {
    public static void main(String[] args) {
        double r = 7;
        double area = PI * r * r;
        System.out.println(Math.round(area) + " sq m");
    }
}''', explain="<p><b>How it works:</b> the static import lets you write <code>PI</code> instead of <code>Math.PI</code>. <code>Math.round</code> is still written with the class name, which is fine.</p>"),
dict(level="medium", title="Fix the ambiguous List", stmt="<p>A file has <code>import java.util.*;</code> and <code>import java.awt.*;</code>, both of which have a <code>List</code>. Fix it so <code>List</code> means <code>java.util.List</code>.</p>", inp="names Riya, Kabir",
 code='''import java.util.*;
import java.util.List;

public class Main {
    public static void main(String[] args) {
        List<String> names = new ArrayList<>();
        names.add("Riya");
        names.add("Kabir");
        System.out.println(names);
    }
}''', explain="<p><b>How it works:</b> a single-type import beats wildcards, so <code>List</code> now clearly means <code>java.util.List</code>, even if another wildcard (like <code>java.awt.*</code>) also offers one. Here the AWT import was simply removed because it wasn't needed.</p>"),
dict(level="medium", title="Classes from three packages", stmt="<p>Use <code>java.util.Scanner</code> to read a name and amount from a String, <code>java.math.BigDecimal</code> for the amount and <code>java.time.LocalDate</code> for the receipt date.</p>", inp="text \"Asha 249.50\", date 2025-02-14",
 code='''import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner("Asha 249.50");
        String name = sc.next();
        BigDecimal amount = new BigDecimal(sc.next());
        LocalDate date = LocalDate.of(2025, 2, 14);
        System.out.println(date + " | " + name + " paid Rs " + amount);
    }
}''', explain="<p><b>How it works:</b> three packages, three single-type imports. A <code>Scanner</code> can read from a String as well as from the keyboard.</p>"),
dict(level="business", title="Due-date checker for invoices", stmt="<p>Mark each invoice as \"OVERDUE\" or \"OK\" by comparing its due date with today's date (fixed here so the output is repeatable).</p>", inp="today 2025-04-10; due dates 2025-04-05, 2025-04-20",
 code='''import java.time.LocalDate;

public class Main {
    public static void main(String[] args) {
        LocalDate today = LocalDate.of(2025, 4, 10);
        String[] ids = {"INV-101", "INV-102"};
        LocalDate[] due = {LocalDate.of(2025, 4, 5), LocalDate.of(2025, 4, 20)};
        for (int i = 0; i < ids.length; i++) {
            String status = due[i].isBefore(today) ? "OVERDUE" : "OK";
            System.out.println(ids[i] + " due " + due[i] + ": " + status);
        }
    }
}''', explain="<p><b>How it works:</b> <code>LocalDate.isBefore</code> compares dates correctly, including month and year boundaries. In production you'd use <code>LocalDate.now()</code>.</p>"),
dict(level="business", title="Unique order IDs with java.util.UUID", stmt="<p>Generate an order ID with <code>java.util.UUID</code> and show that two generated IDs are different. (UUIDs are random, so print only their length and whether they differ.)</p>", inp="two orders",
 code='''import java.util.UUID;

public class Main {
    public static void main(String[] args) {
        String a = UUID.randomUUID().toString();
        String b = UUID.randomUUID().toString();
        System.out.println("ID length: " + a.length());
        System.out.println("Different: " + !a.equals(b));
    }
}''', explain="<p><b>How it works:</b> a UUID is a 36-character random identifier, practically unique even across many servers. That's why distributed systems use it instead of a static counter (Lesson 6.4).</p>"),
dict(level="business", title="Price list with currency formatting", stmt="<p>Format prices in Indian style (lakhs and crores) using <code>java.text.NumberFormat</code> and <code>java.util.Locale</code>.</p>", inp="prices 1250, 125000, 12500000",
 code='''import java.text.NumberFormat;
import java.util.Locale;

public class Main {
    public static void main(String[] args) {
        NumberFormat f = NumberFormat.getNumberInstance(Locale.forLanguageTag("en-IN"));
        long[] prices = {1250, 125000, 12500000};
        for (long p : prices) {
            System.out.println("Rs " + f.format(p));
        }
    }
}''', explain="<p><b>How it works:</b> the Indian locale groups digits as 1,25,00,000. Formatting classes live in <code>java.text</code>; locales in <code>java.util</code>.</p>"),
]
