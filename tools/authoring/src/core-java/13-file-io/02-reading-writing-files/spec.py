import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from mkanim import Anim, two_view
from m13 import code, snippet, runner, quiz

def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

# ---------------- Part 5: two-view animation ----------------
CODE = {1: 'Path p = Path.of("data", "orders.csv");', 2: 'Files.createDirectories(p.getParent());',
        3: 'Files.writeString(p, "101,dosa,80\\n");', 4: 'Files.writeString(p, "102,idli,40\\n", APPEND);',
        5: 'List<String> lines = Files.readAllLines(p);', 6: 'Files.delete(p);'}
S = Anim("see", frames=6, h=250, label="A Path names a file; Files methods create the folder, write, append, read and delete the file")
S.box(8, 8, 344, 36, None, fill="board", stroke="board")
for f, c in CODE.items():
    S.text(16, 31, esc(c), on=str(f), mono=True, size=9.2, cls="chalk")
S.box(10, 58, 160, 150, None, fill="card2", stroke="line")
S.text(20, 76, "app/  (working directory)", size=9.5, bold=True)
S.text(34, 98, "data/", size=9.5, on="2-", bold=True, cls="blue")
S.text(48, 120, "orders.csv", size=9.5, on="3-5", mono=True)
S.text(20, 98, "(no data folder yet)", size=9, on="1", cls="ink3")
S.text(48, 120, "(deleted)", size=9, on="6", cls="red")
S.box(186, 58, 166, 92, None, fill="soft-acc", stroke="track", on="3-5")
S.text(196, 76, "orders.csv contents", size=9, bold=True, cls="acc", on="3-5")
S.text(196, 98, "101,dosa,80", mono=True, size=9.6, on="3-5")
S.text(196, 118, "102,idli,40", mono=True, size=9.6, on="4-5", cls="green")
S.text(196, 140, "12 bytes", size=9, cls="ink3", on="3")
S.text(196, 140, "24 bytes", size=9, cls="ink3", on="4-5")
S.box(186, 160, 166, 48, None, fill="soft-green", stroke="green", on="5")
S.text(196, 178, "lines (a List in memory)", size=8.8, bold=True, cls="green", on="5")
S.text(196, 196, "[101,dosa,80, 102,idli,40]", mono=True, size=8.2, on="5")
S.text(186, 186, "a Path names a file;", size=9.2, cls="ink2", on="1")
S.text(186, 202, "it doesn't create one", size=9.2, cls="ink2", on="1")
S.note({1: "Just a name, nothing on disk.", 2: "The folder is created.", 3: "File created and written.",
        4: "A second line appended.", 5: "Whole file read into a List.", 6: "File deleted."}, y=234, size=10.5)
S.caps(["<code>Path.of(\"data\", \"orders.csv\")</code> builds a <b>path</b>: the file's name and location. Nothing on disk changes.",
        "<code>Files.createDirectories</code> makes the folder (and any missing parents). No error if it already exists.",
        "<code>Files.writeString</code> creates the file, writes the text in UTF-8 and closes it, all in one call. An existing file would be replaced.",
        "With <code>StandardOpenOption.APPEND</code>, the new text goes at the end instead.",
        "<code>Files.readAllLines</code> reads the whole file and returns a <code>List&lt;String&gt;</code>, one element per line, without the line breaks.",
        "<code>Files.delete</code> removes the file. Your <code>Path</code> object still exists: it is only a name."])

B = Anim("behind", frames=6, h=250, label="On the heap: a Path object and later a List of lines; outside the JVM: the operating system's file with its size")
B.box(6, 6, 170, 200, None, fill="soft-blue", stroke="blue")
B.text(16, 24, "JVM HEAP", size=10, bold=True, cls="blue")
B.box(16, 34, 150, 44, None, fill="card", stroke="line")
B.text(24, 52, "#1 Path", size=9.5, bold=True, mono=True)
B.text(24, 70, "\"data/orders.csv\"", size=9, mono=True, cls="ink2")
B.box(16, 120, 150, 76, None, fill="card", stroke="green", on="5")
B.text(24, 138, "#2 ArrayList (2)", size=9.5, bold=True, mono=True, on="5")
B.text(24, 158, "#3 \"101,dosa,80\"", size=8.8, mono=True, on="5")
B.text(24, 176, "#4 \"102,idli,40\"", size=8.8, mono=True, on="5")
B.box(190, 6, 164, 200, None, fill="card2", stroke="line")
B.text(200, 24, "OPERATING SYSTEM", size=10, bold=True, cls="ink2")
B.text(200, 46, "working dir: /home/riya/app", size=8.4, mono=True, cls="ink3")
B.text(200, 70, "data/  —", size=9.5, mono=True, on="1", cls="ink3")
B.text(200, 70, "data/  folder", size=9.5, mono=True, on="2-")
B.text(200, 92, "orders.csv  —", size=9.5, mono=True, on="1-2", cls="ink3")
B.text(200, 92, "orders.csv  12 B", size=9.5, mono=True, on="3", cls="acc")
B.text(200, 92, "orders.csv  24 B", size=9.5, mono=True, on="4-5", cls="acc")
B.text(200, 92, "orders.csv  —", size=9.5, mono=True, on="6", cls="red")
B.box(196, 114, 152, 82, None, fill="board", stroke="board", on="3-5")
B.text(206, 132, "inside writeString:", size=8.6, cls="chalk", on="3-4")
B.text(206, 150, "open → encode → write", size=8.6, mono=True, cls="chalk", on="3-4")
B.text(206, 168, "→ close", size=8.6, mono=True, cls="chalk", on="3-4")
B.text(206, 132, "inside readAllLines:", size=8.6, cls="chalk", on="5")
B.text(206, 150, "open → read → decode", size=8.6, mono=True, cls="chalk", on="5")
B.text(206, 168, "→ split lines → close", size=8.6, mono=True, cls="chalk", on="5")
B.arrow(166, 56, 196, 92, on="3-6", color="track")
B.note({1: "A Path object, no file.", 2: "OS creates the folder.", 3: "Stream opened and closed for you.",
        4: "Appended: 24 bytes.", 5: "New List + Strings on the heap.", 6: "OS removes the file."}, y=236, size=10.5)
B.caps(["The Path is a small object on the heap holding a <b>relative</b> path. Relative paths are resolved against the program's <b>working directory</b>, here /home/riya/app.",
        "The OS creates the <code>data</code> folder. The JVM itself stores nothing about it.",
        "<code>writeString</code> opens a stream, encodes the text as UTF-8, writes 12 bytes and closes the stream: the stream code from Lesson 13.1, already written for you.",
        "Appending adds 12 more bytes; the file is now 24 bytes long.",
        "<code>readAllLines</code> reads all bytes, decodes them and splits on line breaks. Each line becomes a String in a new ArrayList. For a huge file this would fill memory, so you'd read it line by line instead (Lesson 13.3).",
        "After <code>delete</code>, the OS no longer has the file. The Path object is unchanged; <code>Files.exists(p)</code> would now return false."])
ANIM = two_view("Paths and files, both views", S, B)

# ---------------- Part 6: animated example ----------------
ANIM2_HEADING = "Watch it with an example: a canteen's daily sales file"
ANIM2_INTRO = "Every order is appended to one CSV file per day. At closing time the owner's report reads the file and adds up the sales."
A = Anim("Append all day, read at night", frames=5, h=230, label="Orders are appended as CSV lines during the day; at night all lines are read and the amounts totalled")
A.box(10, 14, 200, 130, None, fill="card2", stroke="line")
A.text(20, 32, "sales-2026-10-16.csv", size=9.5, bold=True, mono=True)
rows = ["09:10,dosa,80", "12:45,thali,120", "16:30,chai,15"]
for i, r in enumerate(rows):
    A.text(20, 56 + i * 22, r, mono=True, size=10, on=f"{i + 1}-")
A.box(226, 14, 126, 40, None, fill="soft-acc", stroke="track", on="1-3")
A.text(236, 38, "APPEND", size=10, bold=True, mono=True, cls="acc", on="1-3")
A.arrow(226, 34, 212, 34 + 0, on="1-3", color="track")
A.box(226, 70, 126, 74, None, fill="soft-green", stroke="green", on="4-")
A.text(236, 88, "readAllLines()", size=9.2, bold=True, mono=True, cls="green", on="4-")
A.text(236, 108, "split(\",\")[2]", size=9, mono=True, on="4-")
A.text(236, 128, "80+120+15", size=9, mono=True, on="4-")
A.box(10, 156, 342, 36, None, fill="board", stroke="board", on="5")
A.text(20, 179, "Today's sales: 3 orders, Rs 215", size=11, bold=True, cls="chalk", on="5")
A.note({1: "Morning: first order appended.", 2: "Lunch: another line.", 3: "Evening: another line.",
        4: "Night: read every line.", 5: "Report the total."}, y=206, size=10.5)
A.caps(["At 9:10 a dosa is sold. The app appends one line, <code>time,item,amount</code>, to today's file.",
        "Each new order adds one line at the end. Earlier lines are never rewritten, so a crash can't lose the morning's orders.",
        "By evening the file has three lines. Opening it in a spreadsheet already works: CSV is just text.",
        "At closing, the report reads all lines and takes the third field of each, the amount.",
        "It prints the day's total. One file per day keeps files small and easy to archive. (Real shops would also keep this in a database.)"])
ANIM2 = A

# ---------------- Part 8: tracer ----------------
TRACE = dict(code='''import java.io.IOException;
import java.nio.file.*;
import java.util.List;

public class Main {
    public static void main(String[] args) throws IOException {
        Path file = Path.of("orders.csv");
        Files.writeString(file, "101,dosa,80\\n102,idli,40\\n");
        Files.writeString(file, "103,vada,30\\n", StandardOpenOption.APPEND);
        List<String> lines = Files.readAllLines(file);
        int total = 0;
        for (String line : lines) {
            total += Integer.parseInt(line.split(",")[2]);
        }
        System.out.println(lines.size() + " orders, Rs " + total + ", file " + Files.size(file) + " bytes");
    }
}
''', notes={
 7: "Path :: = A Path object for orders.csv, relative to the working directory. No file exists yet.",
 8: "Write :: = <code>writeString</code> creates the file and writes two lines (24 bytes), then closes it.",
 9: "Append :: = The APPEND option adds a third line at the end instead of replacing the file.",
 10: "Read :: = <code>readAllLines</code> returns a List with one String per line, line breaks removed.",
 11: "Total :: A running sum on main's stack.",
 (13, 1): "Parse :: = <code>split(\",\")</code> gives [\"101\", \"dosa\", \"80\"]; element 2 is the amount.",
 15: "Report :: 3 orders, Rs 150, and the file is 36 bytes."})

# ---------------- Worked examples ----------------
WORKED_INTRO = "Three file tasks from small businesses: saving a list, totalling a CSV, and archiving reports into folders. Each program creates the files it needs, so it runs anywhere."
EXAMPLES = [
dict(tag="Grocery · lists", title="Save and reload a shopping list",
 problem="<p>A grocery app saves the customer's list when the app closes and loads it on the next start. Save a <code>List&lt;String&gt;</code> with <code>Files.write</code>, read it back with <code>Files.readAllLines</code>, and show it numbered.</p>",
 inp="milk, bread, eggs, curd",
 approach=["<code>Files.write(path, list)</code> writes each element as one line (UTF-8).",
           "<code>Files.readAllLines(path)</code> gives the list back.",
           "Print with a counter."],
 code='''import java.io.IOException;
import java.nio.file.*;
import java.util.List;

public class Main {
    public static void main(String[] args) throws IOException {
        Path saved = Path.of("cart.txt");
        List<String> cart = List.of("milk", "bread", "eggs", "curd");
        Files.write(saved, cart);
        List<String> loaded = Files.readAllLines(saved);
        for (int i = 0; i < loaded.size(); i++) {
            System.out.println((i + 1) + ". " + loaded.get(i));
        }
        System.out.println("same list? " + cart.equals(loaded));
    }
}
''', notes={7: "Path :: = Where the list is saved.",
            8: "List :: = An immutable list of 4 items.",
            9: "Save :: = Four lines are written: milk, bread, eggs, curd.",
            10: "Load :: = A brand-new ArrayList with 4 new Strings, read from disk.",
            (12, 1): "Print :: The first item.",
            14: "Compare :: Different objects, equal contents: <code>equals</code> is true."},
 tryit="Press <b>Run</b>. Then add an item with an Indian-language name; Files uses UTF-8 by default, so it survives the round trip."),
dict(tag="Canteen · sales", title="Total a day's sales from a CSV",
 problem="<p>Orders are appended to sales.csv as <code>time,item,amount</code>. At closing, read the file, skip the header line, and print the number of orders, the total and the best-selling amount.</p>",
 inp="header + 4 orders",
 approach=["Write the header once, then append each order line.",
           "Read all lines; start the loop at index 1 to skip the header.",
           "Split each line on commas and parse the amount."],
 code='''import java.io.IOException;
import java.nio.file.*;
import java.util.List;

public class Main {
    public static void main(String[] args) throws IOException {
        Path sales = Path.of("sales.csv");
        Files.writeString(sales, "time,item,amount\\n");
        String[] orders = {"09:10,dosa,80", "12:45,thali,120", "13:05,thali,120", "16:30,chai,15"};
        for (String o : orders) {
            Files.writeString(sales, o + "\\n", StandardOpenOption.APPEND);
        }
        List<String> lines = Files.readAllLines(sales);
        int total = 0, biggest = 0;
        for (int i = 1; i < lines.size(); i++) {
            int amount = Integer.parseInt(lines.get(i).split(",")[2]);
            total += amount;
            biggest = Math.max(biggest, amount);
        }
        System.out.println((lines.size() - 1) + " orders, total Rs " + total + ", biggest Rs " + biggest);
    }
}
''', notes={8: "Header :: = A new file with only the header row.",
            (11, 1): "Append :: = The first order goes to the end of the file.",
            (11, 4): "Last order :: = All four orders appended: the file has 5 lines.",
            13: "Read :: = All 5 lines in a List.",
            (16, 1): "Parse :: = Index 1 is the first real order; field 2 is 80.",
            20: "Report :: 4 orders, Rs 335, biggest Rs 120."},
 tryit="Press <b>Run</b>. Then add a line with a bad amount like <code>\"17:00,lassi,abc\"</code>: <code>parseInt</code> throws NumberFormatException. Wrap the parse in try/catch to skip bad rows."),
dict(tag="Office · archiving", title="Archive last month's reports",
 problem="<p>An office keeps reports in a <code>reports</code> folder. At month end, create <code>archive/2026-09</code>, move every report whose name starts with <code>2026-09</code> into it, and list both folders.</p>",
 inp="reports: 2026-09-gst.txt, 2026-09-sales.txt, 2026-10-sales.txt",
 approach=["Create the folders with <code>Files.createDirectories</code>.",
           "List the reports folder with <code>Files.list</code> (a stream; close it with try-with-resources).",
           "<code>Files.move</code> each matching file into the archive folder, keeping its name."],
 code='''import java.io.IOException;
import java.nio.file.*;
import java.util.*;
import java.util.stream.Stream;

public class Main {
    static List<String> names(Path dir) throws IOException {
        try (Stream<Path> s = Files.list(dir)) {
            return s.map(p -> p.getFileName().toString()).sorted().toList();
        }
    }

    public static void main(String[] args) throws IOException {
        Path reports = Files.createDirectories(Path.of("reports"));
        Path archive = Files.createDirectories(Path.of("archive", "2026-09"));
        for (String n : List.of("2026-09-gst.txt", "2026-09-sales.txt", "2026-10-sales.txt")) {
            Files.writeString(reports.resolve(n), "report " + n);
        }
        for (String n : names(reports)) {
            if (n.startsWith("2026-09")) {
                Files.move(reports.resolve(n), archive.resolve(n));
            }
        }
        System.out.println("reports: " + names(reports));
        System.out.println("archive/2026-09: " + names(archive));
    }
}
''', notes={14: "Folder :: = <code>createDirectories</code> returns the Path it created (or that already existed).",
            15: "Nested :: = archive and archive/2026-09 are created in one call.",
            (17, 1): "resolve :: = <code>reports.resolve(n)</code> builds reports/2026-09-gst.txt.",
            19: "List :: = The three file names, sorted.",
            (21, 1): "Move :: = The GST report moves to the archive. A move inside one disk is just a rename: no bytes are copied.",
            24: "Left :: Only October's report remains.",
            25: "Archived :: Both September reports are in the archive."},
 tryit="Press <b>Run</b>. Then run the move twice in a row: the second time there's nothing to move, because the files are already gone from <code>reports</code>."),
]

# ---------------- Practice problems ----------------
PRACTICE_INTRO = "Use <code>Path</code> and <code>Files</code> for everyday file work, plus <code>Scanner</code> and <code>PrintWriter</code>. Every program creates its own files, so the output is fixed. The last three are business tasks."
PROBLEMS = [
dict(level="easy", title="Write and read a string", stmt="<p>Write <code>Welcome to MyPhatshala</code> to welcome.txt with <code>Files.writeString</code> and print it back with <code>Files.readString</code>.</p>", inp="(none)",
 code='''import java.io.IOException;
import java.nio.file.*;

public class Main {
    public static void main(String[] args) throws IOException {
        Path p = Path.of("welcome.txt");
        Files.writeString(p, "Welcome to MyPhatshala");
        System.out.println(Files.readString(p));
    }
}''', explain="<p><b>How it works:</b> both methods open, use and close the file for you, with UTF-8. Ideal for small text files.</p>"),
dict(level="easy", title="Exists and size", stmt="<p>Check whether notes.txt exists before and after creating it with 5 bytes, and print its size.</p>", inp="(none)",
 code='''import java.io.IOException;
import java.nio.file.*;

public class Main {
    public static void main(String[] args) throws IOException {
        Path p = Path.of("notes.txt");
        System.out.println("before: " + Files.exists(p));
        Files.writeString(p, "hello");
        System.out.println("after: " + Files.exists(p) + ", " + Files.size(p) + " bytes");
    }
}''', explain="<p><b>How it works:</b> <code>Files.exists</code> asks the OS; <code>Files.size</code> returns the length in bytes. The program creates notes.txt fresh in its own folder, so “before” is false.</p>"),
dict(level="easy", title="Parts of a path", stmt="<p>For the path <code>bills/2026/oct/bill-17.pdf</code>, print the file name, the parent folder and the number of name parts.</p>", inp="bills/2026/oct/bill-17.pdf",
 code='''import java.nio.file.Path;

public class Main {
    public static void main(String[] args) {
        Path p = Path.of("bills", "2026", "oct", "bill-17.pdf");
        System.out.println("file:   " + p.getFileName());
        System.out.println("parent: " + p.getParent());
        System.out.println("parts:  " + p.getNameCount());
    }
}''', explain="<p><b>How it works:</b> a Path is just a name, so this works even though the file doesn't exist. <code>Path.of</code> joins the parts with the right separator for the OS (<code>/</code> on Linux, <code>\\</code> on Windows).</p>"),
dict(level="medium", title="Count words in a file", stmt="<p>Write a two-line review to review.txt, then count its lines and words.</p>", inp="two lines of text",
 code='''import java.io.IOException;
import java.nio.file.*;
import java.util.List;

public class Main {
    public static void main(String[] args) throws IOException {
        Path p = Path.of("review.txt");
        Files.writeString(p, "Great dosa and fast service\\nWill come again\\n");
        List<String> lines = Files.readAllLines(p);
        int words = 0;
        for (String line : lines) {
            words += line.trim().split("\\\\s+").length;
        }
        System.out.println(lines.size() + " lines, " + words + " words");
    }
}''', explain="<p><b>How it works:</b> <code>split(\"\\\\s+\")</code> splits on any run of spaces. This is the basis of text analytics: read lines, split, count.</p>"),
dict(level="medium", title="Sum numbers with Scanner", stmt="<p>Write the numbers 120 45 300 15 to amounts.txt, then read them with <code>new Scanner(file)</code> and print the sum.</p>", inp="120 45 300 15",
 code='''import java.io.*;
import java.nio.file.*;
import java.util.Scanner;

public class Main {
    public static void main(String[] args) throws IOException {
        Files.writeString(Path.of("amounts.txt"), "120 45\\n300 15\\n");
        int sum = 0;
        try (Scanner sc = new Scanner(new File("amounts.txt"))) {
            while (sc.hasNextInt()) {
                sum += sc.nextInt();
            }
        }
        System.out.println("sum = " + sum);
    }
}''', explain="<p><b>How it works:</b> a Scanner on a File reads tokens (here ints) across lines, exactly like reading from the keyboard. Close it, as it holds the file open.</p>"),
dict(level="medium", title="Formatted report with PrintWriter", stmt="<p>Write a small aligned price table to menu.txt with <code>PrintWriter.printf</code>, then print the file.</p>", inp="dosa 80, thali 120, chai 15",
 code='''import java.io.*;
import java.nio.file.*;

public class Main {
    public static void main(String[] args) throws IOException {
        String[] items = {"dosa", "thali", "chai"};
        int[] prices = {80, 120, 15};
        try (PrintWriter pw = new PrintWriter("menu.txt")) {
            for (int i = 0; i < items.length; i++) {
                pw.printf("%-8s Rs %4d%n", items[i], prices[i]);
            }
        }
        System.out.print(Files.readString(Path.of("menu.txt")));
    }
}''', explain="<p><b>How it works:</b> PrintWriter gives you <code>println</code> and <code>printf</code> on a file. <code>%-8s</code> left-aligns in 8 columns; <code>%4d</code> right-aligns numbers. PrintWriter never throws IOException on write; call <code>checkError()</code> if you need to know.</p>"),
dict(level="business", title="Attendance from a CSV", stmt="<p>attendance.csv has <code>name,status</code> lines (P or A). Count present and absent students and list the absentees.</p>", inp="5 students",
 code='''import java.io.IOException;
import java.nio.file.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws IOException {
        Path p = Path.of("attendance.csv");
        Files.write(p, List.of("Asha,P", "Ravi,A", "Meena,P", "Imran,P", "Joseph,A"));
        int present = 0;
        List<String> absent = new ArrayList<>();
        for (String line : Files.readAllLines(p)) {
            String[] f = line.split(",");
            if (f[1].equals("P")) present++;
            else absent.add(f[0]);
        }
        System.out.println("present " + present + ", absent " + absent.size() + ": " + absent);
    }
}''', explain="<p><b>How it works:</b> CSV is the most common data-exchange format in offices. Reading lines and splitting on commas is enough for simple files; real CSVs with quoted commas need a CSV library.</p>"),
dict(level="business", title="Low-stock alert", stmt="<p>inventory.csv has <code>item,qty</code>. Write a new file reorder.txt listing items with quantity below 10, then print it.</p>", inp="rice 40, oil 6, sugar 9, salt 25",
 code='''import java.io.IOException;
import java.nio.file.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws IOException {
        Files.write(Path.of("inventory.csv"), List.of("rice,40", "oil,6", "sugar,9", "salt,25"));
        List<String> reorder = new ArrayList<>();
        for (String line : Files.readAllLines(Path.of("inventory.csv"))) {
            String[] f = line.split(",");
            if (Integer.parseInt(f[1]) < 10) reorder.add(f[0] + " (only " + f[1] + " left)");
        }
        Files.write(Path.of("reorder.txt"), reorder);
        System.out.print(Files.readString(Path.of("reorder.txt")));
    }
}''', explain="<p><b>How it works:</b> read one file, filter, write another: the shape of most batch jobs. The output file can be emailed to the supplier or loaded by another system.</p>"),
dict(level="business", title="Daily backup that may already exist", stmt="<p>Copy ledger.txt to ledger-backup.txt. Copying again fails because the backup exists; catch that, then copy with <code>REPLACE_EXISTING</code>.</p>", inp="ledger.txt",
 code='''import java.io.IOException;
import java.nio.file.*;

public class Main {
    public static void main(String[] args) throws IOException {
        Path ledger = Path.of("ledger.txt"), backup = Path.of("ledger-backup.txt");
        Files.writeString(ledger, "opening balance 50000\\n");
        Files.copy(ledger, backup);
        Files.writeString(ledger, "sale 1200\\n", StandardOpenOption.APPEND);
        try {
            Files.copy(ledger, backup);
        } catch (FileAlreadyExistsException e) {
            System.out.println("backup exists: " + e.getFile());
        }
        Files.copy(ledger, backup, StandardCopyOption.REPLACE_EXISTING);
        System.out.println("backup now " + Files.size(backup) + " bytes, ledger " + Files.size(ledger) + " bytes");
    }
}''', explain="<p><b>How it works:</b> NIO refuses to overwrite by accident: <code>Files.copy</code> throws <code>FileAlreadyExistsException</code> unless you pass <code>REPLACE_EXISTING</code>. Making overwrites explicit prevents losing data.</p>"),
]

# ---------------- Extra blocks ----------------
BLOCKS = {
'ANIM': ANIM,
'CODE_FILES': snippet('''Path p = Path.of("data", "orders.csv");          // just a name
Files.exists(p)    Files.size(p)    Files.isDirectory(p)
Files.writeString(p, text)                        // create or replace
Files.writeString(p, text, StandardOpenOption.APPEND)
Files.write(p, listOfLines)
String all = Files.readString(p);
List<String> lines = Files.readAllLines(p);
Files.createDirectories(p.getParent());
Files.copy(a, b)   Files.move(a, b)   Files.delete(p)   Files.deleteIfExists(p)'''),
'CODE_OLD': code('''import java.io.*;

public class Main {
    public static void main(String[] args) throws IOException {
        File f = new File("legacy.txt");
        try (FileWriter w = new FileWriter(f)) {
            w.write("written with java.io.File");
        }
        System.out.println(f.getName() + " exists=" + f.exists() + " size=" + f.length());
        System.out.println("deleted: " + f.delete() + ", deleted again: " + f.delete());
    }
}'''),
'CODE_RUN': code('''import java.io.IOException;
import java.nio.file.*;
import java.util.List;

public class Main {
    public static void main(String[] args) throws IOException {
        Path file = Path.of("data", "orders.csv");
        Files.createDirectories(file.getParent());
        Files.writeString(file, "101,dosa,80\\n");
        Files.writeString(file, "102,idli,40\\n", StandardOpenOption.APPEND);
        List<String> lines = Files.readAllLines(file);
        System.out.println(lines.size() + " lines: " + lines);
        System.out.println("size " + Files.size(file) + " bytes");
        Files.delete(file);
        System.out.println("exists after delete: " + Files.exists(file));
    }
}'''),
'RUNNER': runner([
 dict(label="1 · Create, append, read, delete", hint="Press <b>Run</b>. Then remove the APPEND option and run again: how many lines now?",
      code='''import java.io.IOException;
import java.nio.file.*;
import java.util.List;

public class Main {
    public static void main(String[] args) throws IOException {
        Path file = Path.of("data", "orders.csv");
        Files.createDirectories(file.getParent());
        Files.writeString(file, "101,dosa,80\\n");
        Files.writeString(file, "102,idli,40\\n", StandardOpenOption.APPEND);
        List<String> lines = Files.readAllLines(file);
        System.out.println(lines.size() + " lines: " + lines);
        System.out.println("size " + Files.size(file) + " bytes");
        Files.delete(file);
        System.out.println("exists after delete: " + Files.exists(file));
    }
}'''),
 dict(label="2 · Predict: where is the file?", hint="<b>Predict first:</b> a relative path is resolved against the working directory. What does <code>toAbsolutePath()</code> print here? (On your computer it would be your project folder.)",
      code='''import java.nio.file.*;

public class Main {
    public static void main(String[] args) {
        Path p = Path.of("report.txt");
        System.out.println("relative: " + p + "  absolute? " + p.isAbsolute());
        System.out.println("resolved: " + p.toAbsolutePath());
        System.out.println("working dir: " + System.getProperty("user.dir"));
    }
}'''),
 dict(label="3 · Predict: a Path to nothing", hint="<b>Predict first:</b> does creating a Path for a file that doesn't exist throw? When would an error happen?",
      code='''import java.nio.file.*;

public class Main {
    public static void main(String[] args) {
        Path ghost = Path.of("does-not-exist.csv");
        System.out.println("Path made: " + ghost);
        System.out.println("exists: " + Files.exists(ghost));
        System.out.println("no exception yet: a Path is only a name");
    }
}'''),
 dict(label="4 · Crash: reading a missing file", hint="The file was never created. Read the exception name, then create it with <code>Files.writeString</code> first, or check <code>Files.exists</code>.",
      code='''import java.io.IOException;
import java.nio.file.*;

public class Main {
    public static void main(String[] args) throws IOException {
        String prices = Files.readString(Path.of("prices.csv"));
        System.out.println(prices);
    }
}''', _expect="exception"),
 dict(label="5 · Spot the error", hint="<code>Files.readString</code> throws the checked <code>IOException</code>. Declare it on main or catch it.",
      code='''import java.nio.file.*;

public class Main {
    public static void main(String[] args) {
        Files.writeString(Path.of("a.txt"), "hello");
        System.out.println(Files.readString(Path.of("a.txt")));
    }
}''', _expect="compile-error"),
]),
'QUIZ': quiz([
 {"q": "What does Path.of(\"a.txt\") do on disk?", "options": ["Creates a.txt", "Nothing: it only builds a path object", "Opens a.txt", "Deletes a.txt"], "answer": 1, "why": "A Path is just a name; Files methods do the actual work."},
 {"q": "Files.writeString(p, text) on an existing file…", "options": ["appends", "replaces its contents", "throws FileAlreadyExistsException", "does nothing"], "answer": 1, "why": "Default options are CREATE, TRUNCATE_EXISTING, WRITE. Use APPEND to add."},
 {"q": "Files.readAllLines returns…", "options": ["a String", "a List<String> without line breaks", "a byte[]", "a Stream"], "answer": 1, "why": "One element per line."},
 {"q": "Reading a missing file with Files.readString throws…", "options": ["FileNotFoundException", "NoSuchFileException", "NullPointerException", "EOFException"], "answer": 1, "why": "NIO uses NoSuchFileException; old java.io uses FileNotFoundException. Both are IOExceptions."},
 {"q": "A relative path like \"data/x.csv\" is resolved against…", "options": ["the Java installation folder", "the working directory (user.dir)", "the user's home folder", "the folder of the .java file"], "answer": 1, "why": "It's wherever the program was started from, which may surprise you in IDEs and servers."},
 {"q": "Files.copy(a, b) when b already exists…", "options": ["overwrites b", "throws FileAlreadyExistsException", "appends to b", "renames b"], "answer": 1, "why": "Pass StandardCopyOption.REPLACE_EXISTING to overwrite deliberately."},
 {"q": "Which is the better choice for reading a 5 GB log file?", "options": ["Files.readAllLines", "Reading line by line (BufferedReader or Files.lines)", "Files.readString", "Scanner.nextInt"], "answer": 1, "why": "readAllLines loads everything into memory at once."},
 {"q": "File.delete() on a file that doesn't exist…", "options": ["throws", "returns false", "creates it", "returns true"], "answer": 1, "why": "Old java.io.File reports failure with a boolean; Files.delete throws NoSuchFileException instead."},
]),
}
