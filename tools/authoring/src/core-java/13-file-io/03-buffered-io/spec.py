import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from mkanim import Anim, two_view
from m13 import code, snippet, runner, quiz

def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

# ---------------- Part 5: two-view animation ----------------
S = Anim("see", frames=6, h=250, label="Without a buffer every small write goes to the disk; with a buffer writes collect in memory and go to disk in one large chunk")
S.box(8, 8, 344, 36, None, fill="board", stroke="board")
codes = {1: 'out.write(b);  // FileOutputStream, x5', 2: 'out.write(b);  // FileOutputStream, x5',
         3: 'bw.write(line); // BufferedWriter', 4: 'bw.write(line); // more lines', 5: '// buffer full, or flush()/close()',
         6: 'bw.close();     // flushes, then closes'}
for f, c in codes.items():
    S.text(16, 31, esc(c), on=str(f), mono=True, size=9.4, cls="chalk")
S.box(10, 60, 90, 120, None, fill="card2", stroke="line")
S.text(55, 78, "program", size=9.5, bold=True, anchor="middle")
S.box(262, 60, 90, 120, None, fill="card", stroke="line")
S.text(307, 78, "disk", size=9.5, bold=True, anchor="middle")
for i in range(5):
    S.arrow(100, 92 + i * 16, 260, 92 + i * 16, on="1-2", color="red", sw=1.4)
S.text(180, 196, "5 trips to the disk", on="2", size=10.5, bold=True, anchor="middle", cls="red")
S.box(120, 70, 122, 96, None, fill="soft-acc", stroke="track", on="3-")
S.text(181, 88, "buffer (8 KB)", size=9, bold=True, anchor="middle", cls="acc", on="3-")
fill = {3: 1, 4: 4, 5: 6}
for f, n in fill.items():
    for k in range(n):
        S.box(128 + k * 18, 104, 14, 40, None, fill="soft-blue", stroke="blue", on=str(f), rx=2)
S.arrow(100, 116, 120, 116, on="3-4", color="ink")
S.arrow(242, 124, 260, 124, on="5-6", color="green", sw=2.4)
S.text(180, 196, "1 trip carries everything", on="5", size=10.5, bold=True, anchor="middle", cls="green")
S.text(180, 196, "close() = flush + release the file", on="6", size=10.5, bold=True, anchor="middle", cls="ink2")
S.text(181, 158, "empty again", size=9, anchor="middle", cls="ink3", on="6")
S.note({1: "No buffer: each write hits the disk.", 2: "Many small trips: slow.", 3: "With a buffer: writes go to memory.",
        4: "The buffer fills up.", 5: "One big write to disk.", 6: "close() flushes the rest."}, y=234, size=10.5)
S.caps(["A plain <code>FileOutputStream</code> passes every <code>write</code> straight to the operating system.",
        "Each call is a <b>system call</b>: the program switches to the OS kernel and back. Doing that thousands of times for tiny pieces is slow.",
        "A <code>BufferedWriter</code> keeps an array (8,192 characters) in memory. <code>write</code> just copies into it: no OS call.",
        "More writes, still in memory. This is extremely fast.",
        "When the buffer is full, or when you call <code>flush()</code>, the whole chunk goes down in <b>one</b> call.",
        "<code>close()</code> flushes whatever is left, then closes the file. Forget it and the last part of your data never reaches the disk."])

B = Anim("behind", frames=6, h=250, label="A BufferedReader wraps a FileReader: it reads a big block into its char array once and then serves lines from memory")
B.box(6, 6, 348, 120, None, fill="soft-blue", stroke="blue")
B.text(16, 24, "HEAP", size=10, bold=True, cls="blue")
B.box(16, 34, 150, 82, None, fill="card", stroke="line")
B.text(24, 52, "#1 BufferedReader", size=9.2, bold=True, mono=True)
B.text(24, 70, "in  → #2", size=9, mono=True, cls="ink2")
B.text(24, 88, "cb  → char[8192]", size=9, mono=True, cls="ink2")
B.text(24, 106, "pos", size=9, mono=True, cls="ink2")
pos = {1: "0", 2: "0", 3: "12", 4: "24", 5: "36", 6: "—"}
for f, v in pos.items():
    B.text(56, 106, v, on=str(f), size=9, mono=True, cls="acc", bold=True)
B.box(186, 34, 160, 34, None, fill="card", stroke="line")
B.text(194, 55, "#2 FileReader (orders.txt)", size=8.8, bold=True, mono=True)
B.box(186, 76, 160, 40, None, fill="soft-acc", stroke="track", on="2-5")
B.text(194, 92, "char[] holds lines 1–3", size=8.8, mono=True, cls="acc", on="2-5")
B.text(194, 108, "(whole small file)", size=8.4, cls="ink3", on="2-5")
B.box(6, 136, 348, 72, None, fill="card2", stroke="line")
B.text(16, 154, "main stack", size=9.5, bold=True, cls="ink2")
lines = {3: "line = \"101,dosa,80\"", 4: "line = \"102,idli,40\"", 5: "line = \"103,vada,30\"", 6: "line = null  (end)"}
for f, l in lines.items():
    B.text(16, 178, l, on=str(f), size=10, mono=True, cls="red" if f == 6 else "ink")
B.text(16, 200, "1 read from the file, 3 lines served", size=9.2, cls="green", on="5")
B.text(16, 200, "readLine() returns null at the end", size=9.2, cls="red", on="6")
B.arrow(186, 51, 168, 51, on="1-", color="ink")
B.arrow(266, 68, 266, 76, on="2", color="track")
B.note({1: "A reader wrapped in a buffered reader.", 2: "First readLine: one big read.", 3: "Line 1 from memory.",
        4: "Line 2 from memory.", 5: "Line 3 from memory.", 6: "No more lines: null."}, y=236, size=10.5)
B.caps(["<code>new BufferedReader(new FileReader(\"orders.txt\"))</code>: two objects. The BufferedReader holds a reference to the FileReader and an empty <code>char[8192]</code>.",
        "The first <code>readLine()</code> asks the FileReader for up to 8,192 characters at once. This small file fits completely.",
        "<code>readLine()</code> finds the first line break in the array, returns the characters before it as a new String, and moves <code>pos</code> forward.",
        "The second line comes from the same array: no disk access at all.",
        "Same for the third. One read from the file served three lines.",
        "At the end of the data, <code>readLine()</code> returns <code>null</code>. That's the loop condition: <code>while ((line = br.readLine()) != null)</code>."])
ANIM = two_view("Why buffering is fast, both views", S, B)

# ---------------- Part 6: animated example ----------------
ANIM2_HEADING = "Watch it with an example: a bank's nightly statement file"
ANIM2_INTRO = "A bank writes 2 lakh transaction lines every night. Without a buffer, each line is a separate trip to the disk; with one, lines are sent in big blocks."
A = Anim("2,00,000 lines, buffered vs unbuffered", frames=5, h=230, label="Comparing the number of disk writes for a large statement file with and without a buffer")
A.box(10, 14, 160, 120, None, fill="card", stroke="red")
A.text(20, 34, "unbuffered", size=10, bold=True, cls="red")
A.box(190, 14, 160, 120, None, fill="card", stroke="green")
A.text(200, 34, "BufferedWriter", size=10, bold=True, cls="green")
A.text(20, 60, "writes to OS:", size=9, cls="ink2", on="2-")
A.text(200, 60, "writes to OS:", size=9, cls="ink2", on="2-")
un = {2: "50,000", 3: "1,20,000", 4: "2,00,000", 5: "2,00,000"}
bu = {2: "~150", 3: "~350", 4: "~600", 5: "~600"}
for f, v in un.items():
    A.text(20, 88, v, on=str(f), size=16, bold=True, mono=True, cls="red")
for f, v in bu.items():
    A.text(200, 88, v, on=str(f), size=16, bold=True, mono=True, cls="green")
A.text(20, 118, "one per line", size=9, cls="ink3", on="2-")
A.text(200, 118, "one per 8 KB block", size=9, cls="ink3", on="2-")
A.box(10, 146, 340, 40, None, fill="board", stroke="board", on="5")
A.text(20, 170, "Same file, far fewer OS calls: the job finishes much sooner", size=9.8, cls="chalk", bold=True, on="5")
A.text(10, 160, "writing 2,00,000 lines of about 25 characters…", size=9.5, cls="ink2", on="1-4")
A.note({1: "The nightly job starts.", 2: "A quarter of the way.", 3: "Over half done.", 4: "Finished.", 5: "Why buffering wins."}, y=206, size=10.5)
A.caps(["Each night the bank writes one line per transaction: date, account, amount. About 2 lakh lines, 5 MB.",
        "Written straight to a <code>FileOutputStream</code> with no buffer, every line is its own write call to the OS. Buffered, lines collect in an 8 KB array, so one call carries about 300 lines.",
        "The unbuffered job keeps switching into the OS kernel; the buffered one is mostly copying characters in memory.",
        "The file contents are identical. Only the number of trips differs: 2 lakh vs about 600. (Counts are approximate; the exact number depends on line lengths.)",
        "That's why production code always wraps file streams in buffers, or uses <code>Files.newBufferedWriter</code>, which does it for you."])
ANIM2 = A

# ---------------- Part 8: tracer ----------------
TRACE = dict(code='''import java.io.*;
import java.nio.file.*;

public class Main {
    public static void main(String[] args) throws IOException {
        Files.writeString(Path.of("orders.txt"), "101,dosa,80\\n102,idli,40\\n103,vada,30\\n");
        int total = 0, count = 0;
        try (BufferedReader br = new BufferedReader(new FileReader("orders.txt"))) {
            String line;
            while ((line = br.readLine()) != null) {
                total += Integer.parseInt(line.substring(line.lastIndexOf(',') + 1));
                count++;
            }
        }
        System.out.println(count + " orders, Rs " + total);
    }
}
''', notes={
 6: "Test file :: = Three order lines are written so the program has something to read.",
 7: "Counters :: Two running values on main's stack.",
 8: "Wrap :: = A FileReader opens the file; a BufferedReader wraps it with an 8 KB char buffer. try-with-resources will close both.",
 (10, 1): "First line :: = The first <code>readLine()</code> fills the buffer from the file (one read), then returns \"101,dosa,80\".",
 (11, 1): "Amount :: = The text after the last comma is parsed: 80.",
 (10, 2): "From memory :: = The second line comes from the buffer: no file access.",
 (10, 4): "End :: = <code>readLine()</code> returns null: the loop stops.",
 15: "Result :: 3 orders, Rs 150. The reader was closed when the try block ended."})

# ---------------- Worked examples ----------------
WORKED_INTRO = "Three real uses: proving how many OS calls a buffer saves, writing a report with <code>BufferedWriter</code>, and filtering a large log line by line. Watch the stack: only one line is held at a time."
EXAMPLES = [
dict(tag="Performance · proof", title="Count the trips to the OS",
 problem="<p>Prove that buffering reduces system calls. Write 20 bytes one at a time, first straight to a <code>FileOutputStream</code>, then through a <code>BufferedOutputStream</code> with a tiny 8-byte buffer (so the trace stays short; the real default is 8,192). Count the calls that reach the file stream with a small counting wrapper.</p>",
 inp="20 single-byte writes, buffer of 8 bytes",
 approach=["A <code>Counting</code> class extends <code>FilterOutputStream</code> and counts every write that reaches it.",
           "Put it directly under the loop, then under a BufferedOutputStream.",
           "Compare the counts. Each call into a FileOutputStream is one OS call."],
 code='''import java.io.*;

public class Main {
    static class Counting extends FilterOutputStream {
        int calls = 0;
        Counting(OutputStream out) { super(out); }
        @Override public void write(int b) throws IOException { calls++; out.write(b); }
        @Override public void write(byte[] b, int off, int len) throws IOException { calls++; out.write(b, off, len); }
    }

    public static void main(String[] args) throws IOException {
        Counting direct = new Counting(new FileOutputStream("a.dat"));
        try (direct) {
            for (int i = 0; i < 20; i++) direct.write('x');
        }
        Counting under = new Counting(new FileOutputStream("b.dat"));
        try (OutputStream out = new BufferedOutputStream(under, 8)) {
            for (int i = 0; i < 20; i++) out.write('x');
        }
        System.out.println("unbuffered: " + direct.calls + " calls to the file");
        System.out.println("buffered:   " + under.calls + " calls to the file");
    }
}
''', notes={12: "Direct :: = The counting wrapper sits right on the FileOutputStream.",
            13: "try (direct) :: An existing variable can be used in try-with-resources (Java 9+).",
            14: "20 writes :: = Every single byte goes straight to the file stream: 20 OS calls.",
            16: "Buffered :: = This time a BufferedOutputStream with an 8-byte buffer sits above the counter.",
            18: "Buffered writes :: = Bytes collect in memory; the counter sees one call each time 8 bytes are full (twice), and one more at close for the last 4.",
            20: "Result :: 20 calls vs 3. With real sizes the gap is huge: 10,000 single-byte writes need 10,000 calls unbuffered, but only 2 with the default 8 KB buffer."},
 tryit="Press <b>Run</b>. Then change the buffer size from 8 to 4, then to 64. How many calls now?"),
dict(tag="Payroll · reports", title="Write a salary-slip summary with BufferedWriter",
 problem="<p>Payroll must write one summary line per employee to payroll.txt, then read the file back with <code>BufferedReader</code> to confirm the line count and the total payout.</p>",
 inp="Asha 52000, Ravi 47500, Meena 61000, Imran 39000",
 approach=["<code>Files.newBufferedWriter</code> gives a BufferedWriter with UTF-8.",
           "Write each line with <code>write</code> + <code>newLine()</code>.",
           "Read back with <code>Files.newBufferedReader</code> and <code>readLine()</code>."],
 code='''import java.io.*;
import java.nio.file.*;

public class Main {
    public static void main(String[] args) throws IOException {
        String[] names = {"Asha", "Ravi", "Meena", "Imran"};
        int[] pay = {52000, 47500, 61000, 39000};
        Path file = Path.of("payroll.txt");
        try (BufferedWriter w = Files.newBufferedWriter(file)) {
            for (int i = 0; i < names.length; i++) {
                w.write(names[i] + "," + pay[i]);
                w.newLine();
            }
        }
        int lines = 0;
        long total = 0;
        try (BufferedReader r = Files.newBufferedReader(file)) {
            String line;
            while ((line = r.readLine()) != null) {
                lines++;
                total += Long.parseLong(line.split(",")[1]);
            }
        }
        System.out.println(lines + " slips, total payout Rs " + total);
    }
}
''', notes={9: "Writer :: = A BufferedWriter over the file, UTF-8, created or replaced.",
            (11, 1): "Into the buffer :: = \"Asha,52000\" is copied into memory, not yet written to disk.",
            (12, 4): "Last line :: = All four lines are in the buffer.",
            14: "Closed :: = Leaving the try block flushes the buffer to the file in one write and closes it.",
            17: "Reader :: = A BufferedReader over the same file.",
            (19, 1): "Line 1 :: = \"Asha,52000\".",
            24: "Report :: 4 slips, Rs 1,99,500."},
 tryit="Press <b>Run</b>. Then move the reading code <i>inside</i> the first try block (before it closes): the reader finds an empty file, because nothing was flushed yet."),
dict(tag="Operations · logs", title="Pull the errors out of a big log",
 problem="<p>A server log has thousands of lines. Support needs only the ERROR lines, saved to errors.txt. Read line by line (never the whole file at once), write matching lines, and report counts.</p>",
 inp="a generated log of 12 lines, every 4th an ERROR (real logs have millions)",
 approach=["Generate a test log with a BufferedWriter.",
           "Open a BufferedReader on the log and a BufferedWriter on errors.txt in one try.",
           "For each line containing \"ERROR\", write it out. Only one line is in memory at a time."],
 code='''import java.io.*;
import java.nio.file.*;

public class Main {
    public static void main(String[] args) throws IOException {
        try (BufferedWriter w = Files.newBufferedWriter(Path.of("server.log"))) {
            for (int i = 1; i <= 12; i++) {
                w.write(i % 4 == 0 ? "ERROR payment timeout #" + i : "INFO request ok #" + i);
                w.newLine();
            }
        }
        int read = 0, errors = 0;
        try (BufferedReader in = Files.newBufferedReader(Path.of("server.log"));
             BufferedWriter out = Files.newBufferedWriter(Path.of("errors.txt"))) {
            String line;
            while ((line = in.readLine()) != null) {
                read++;
                if (line.startsWith("ERROR")) {
                    out.write(line);
                    out.newLine();
                    errors++;
                }
            }
        }
        System.out.println("read " + read + " lines, saved " + errors + " errors");
        System.out.println("first error: " + Files.readAllLines(Path.of("errors.txt")).get(0));
    }
}
''', notes={6: "Make a log :: = The test log is written through a buffer.",
            7: "12 lines :: = The loop runs 12 times; every 4th line is an ERROR.",
            12: "Counters :: Lines read and errors found.",
            13: "Two streams :: = A reader for the log and a writer for the errors, both buffered and both closed automatically.",
            25: "Report :: Both files were closed at the end of the try, so errors.txt is complete: 12 read, 3 errors saved. The same code handles a 5 GB log, because it never holds more than one line.",
            26: "Check :: The first saved line."},
 tryit="Press <b>Run</b>. Then change the filter to keep lines that end with \"#6\"."),
]

# ---------------- Practice problems ----------------
PRACTICE_INTRO = "Read with <code>BufferedReader.readLine()</code>, write with <code>BufferedWriter</code>, and never forget to flush or close. Each program creates its own files. The last three are business tasks."
PROBLEMS = [
dict(level="easy", title="Read every line", stmt="<p>Write three city names to cities.txt, then print each line with its number using <code>BufferedReader</code>.</p>", inp="Pune, Nagpur, Nashik",
 code='''import java.io.*;
import java.nio.file.*;

public class Main {
    public static void main(String[] args) throws IOException {
        Files.writeString(Path.of("cities.txt"), "Pune\\nNagpur\\nNashik\\n");
        try (BufferedReader br = new BufferedReader(new FileReader("cities.txt"))) {
            String line;
            int n = 1;
            while ((line = br.readLine()) != null) {
                System.out.println(n++ + ": " + line);
            }
        }
    }
}''', explain="<p><b>How it works:</b> the assignment inside the condition reads a line and checks it for null in one go. This loop shape is worth memorising.</p>"),
dict(level="easy", title="Write lines with newLine()", stmt="<p>Write three lines with a <code>BufferedWriter</code> and <code>newLine()</code>, then print how many lines the file has.</p>", inp="(none)",
 code='''import java.io.*;
import java.nio.file.*;

public class Main {
    public static void main(String[] args) throws IOException {
        try (BufferedWriter bw = new BufferedWriter(new FileWriter("todo.txt"))) {
            bw.write("pay electricity bill");
            bw.newLine();
            bw.write("book train ticket");
            bw.newLine();
            bw.write("call bank");
            bw.newLine();
        }
        System.out.println(Files.readAllLines(Path.of("todo.txt")).size() + " tasks saved");
    }
}''', explain="<p><b>How it works:</b> <code>newLine()</code> writes the platform's line separator (\\n on Linux and macOS, \\r\\n on Windows).</p>"),
dict(level="easy", title="flush() before reading", stmt="<p>Write <code>hello</code> with a BufferedWriter but don't close it. Print the file size, then call <code>flush()</code> and print it again.</p>", inp="(none)",
 code='''import java.io.*;
import java.nio.file.*;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedWriter bw = new BufferedWriter(new FileWriter("draft.txt"));
        bw.write("hello");
        System.out.println("before flush: " + Files.size(Path.of("draft.txt")) + " bytes");
        bw.flush();
        System.out.println("after flush:  " + Files.size(Path.of("draft.txt")) + " bytes");
        bw.close();
    }
}''', explain="<p><b>How it works:</b> until the buffer is flushed, the data exists only in your program's memory. If the program crashed before <code>flush()</code> or <code>close()</code>, those 5 bytes would be lost.</p>"),
dict(level="medium", title="Longest line", stmt="<p>Find the longest line in a file of product names and print it with its length.</p>", inp="4 product names",
 code='''import java.io.*;
import java.nio.file.*;
import java.util.List;

public class Main {
    public static void main(String[] args) throws IOException {
        Files.write(Path.of("products.txt"), List.of("Tea", "Basmati Rice 5kg", "Sugar", "Sunflower Oil 1L"));
        String longest = "";
        try (BufferedReader br = Files.newBufferedReader(Path.of("products.txt"))) {
            String line;
            while ((line = br.readLine()) != null) {
                if (line.length() > longest.length()) longest = line;
            }
        }
        System.out.println(longest + " (" + longest.length() + " chars)");
    }
}''', explain="<p><b>How it works:</b> only the current line and the best so far are kept, so this works for files of any size.</p>"),
dict(level="medium", title="Count lines with lines()", stmt="<p>Use <code>BufferedReader.lines()</code> to count non-empty lines in a file that has some blank lines.</p>", inp="5 lines, 2 blank",
 code='''import java.io.*;
import java.nio.file.*;

public class Main {
    public static void main(String[] args) throws IOException {
        Files.writeString(Path.of("notes.txt"), "buy milk\\n\\ncall Ravi\\n\\nsubmit GST\\n");
        try (BufferedReader br = Files.newBufferedReader(Path.of("notes.txt"))) {
            long filled = br.lines().filter(l -> !l.isBlank()).count();
            System.out.println("non-empty lines: " + filled);
        }
    }
}''', explain="<p><b>How it works:</b> <code>lines()</code> turns the reader into a lazy Stream of lines (Lesson 14.3), reading as it goes.</p>"),
dict(level="medium", title="Copy a text file line by line", stmt="<p>Copy menu.txt to menu-copy.txt using a BufferedReader and BufferedWriter, converting each line to upper case.</p>", inp="3 dishes",
 code='''import java.io.*;
import java.nio.file.*;
import java.util.List;

public class Main {
    public static void main(String[] args) throws IOException {
        Files.write(Path.of("menu.txt"), List.of("masala dosa", "idli sambar", "filter coffee"));
        try (BufferedReader in = Files.newBufferedReader(Path.of("menu.txt"));
             BufferedWriter out = Files.newBufferedWriter(Path.of("menu-copy.txt"))) {
            String line;
            while ((line = in.readLine()) != null) {
                out.write(line.toUpperCase());
                out.newLine();
            }
        }
        System.out.println(Files.readAllLines(Path.of("menu-copy.txt")));
    }
}''', explain="<p><b>How it works:</b> resources in one try are closed in reverse order: the writer first (flushing it), then the reader.</p>"),
dict(level="business", title="Bank statement summary", stmt="<p>statement.csv has <code>date,type,amount</code> lines with type CR or DR. Read it with BufferedReader and print total credits, total debits and the closing balance from an opening balance of 10,000.</p>", inp="5 transactions",
 code='''import java.io.*;
import java.nio.file.*;
import java.util.List;

public class Main {
    public static void main(String[] args) throws IOException {
        Files.write(Path.of("statement.csv"), List.of(
            "01-10,CR,25000", "03-10,DR,1200", "07-10,DR,8500", "15-10,CR,3000", "20-10,DR,450"));
        long cr = 0, dr = 0;
        try (BufferedReader br = Files.newBufferedReader(Path.of("statement.csv"))) {
            String line;
            while ((line = br.readLine()) != null) {
                String[] f = line.split(",");
                long amt = Long.parseLong(f[2]);
                if (f[1].equals("CR")) cr += amt; else dr += amt;
            }
        }
        System.out.println("credits " + cr + ", debits " + dr + ", closing " + (10000 + cr - dr));
    }
}''', explain="<p><b>How it works:</b> streaming through the statement keeps memory use constant whether it has 5 lines or 5 million.</p>"),
dict(level="business", title="Split a big order file by city", stmt="<p>orders.csv has <code>id,city,amount</code>. Write Pune orders to pune.csv and all others to others.csv, then print the line counts.</p>", inp="6 orders",
 code='''import java.io.*;
import java.nio.file.*;
import java.util.List;

public class Main {
    public static void main(String[] args) throws IOException {
        Files.write(Path.of("orders.csv"), List.of("1,Pune,450", "2,Mumbai,900", "3,Pune,120", "4,Nagpur,300", "5,Pune,75", "6,Mumbai,640"));
        try (BufferedReader in = Files.newBufferedReader(Path.of("orders.csv"));
             BufferedWriter pune = Files.newBufferedWriter(Path.of("pune.csv"));
             BufferedWriter rest = Files.newBufferedWriter(Path.of("others.csv"))) {
            String line;
            while ((line = in.readLine()) != null) {
                BufferedWriter target = line.split(",")[1].equals("Pune") ? pune : rest;
                target.write(line);
                target.newLine();
            }
        }
        System.out.println("pune.csv: " + Files.readAllLines(Path.of("pune.csv")).size()
                + ", others.csv: " + Files.readAllLines(Path.of("others.csv")).size());
    }
}''', explain="<p><b>How it works:</b> one pass over the input feeds two buffered outputs. Each writer is flushed and closed when the try ends.</p>"),
dict(level="business", title="Resume-safe batch: flush every 100 lines", stmt="<p>A job writes 250 receipt lines. To limit loss on a crash, it calls <code>flush()</code> every 100 lines. Count the flushes, including the final close.</p>", inp="250 receipts",
 code='''import java.io.*;
import java.nio.file.*;

public class Main {
    public static void main(String[] args) throws IOException {
        int flushes = 0;
        try (BufferedWriter w = Files.newBufferedWriter(Path.of("receipts.txt"))) {
            for (int i = 1; i <= 250; i++) {
                w.write("RCPT-" + i);
                w.newLine();
                if (i % 100 == 0) {
                    w.flush();
                    flushes++;
                }
            }
        }
        flushes++;
        System.out.println(Files.readAllLines(Path.of("receipts.txt")).size() + " receipts, " + flushes + " flushes");
    }
}''', explain="<p><b>How it works:</b> flushing too often removes the benefit of buffering; never flushing risks losing everything since the start. Periodic flushes (or checkpoints) are the usual compromise in batch jobs.</p>"),
]

# ---------------- Extra blocks ----------------
BLOCKS = {
'ANIM': ANIM,
'CODE_WRAP': snippet('''// classic: wrap a file stream in a buffer
BufferedReader br = new BufferedReader(new FileReader("in.txt", StandardCharsets.UTF_8));
BufferedWriter bw = new BufferedWriter(new FileWriter("out.txt", StandardCharsets.UTF_8));
// for bytes
InputStream in = new BufferedInputStream(new FileInputStream("photo.jpg"));
// modern shortcut (UTF-8, already buffered)
BufferedReader r = Files.newBufferedReader(Path.of("in.txt"));
BufferedWriter w = Files.newBufferedWriter(Path.of("out.txt"));'''),
'CODE_LOST': code('''import java.io.*;
import java.nio.file.*;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedWriter w = new BufferedWriter(new FileWriter("invoice.txt"));
        w.write("INV-501 Rs 2360");
        System.out.println("on disk now: " + Files.size(Path.of("invoice.txt")) + " bytes");
        w.close();
        System.out.println("after close: " + Files.size(Path.of("invoice.txt")) + " bytes");
    }
}'''),
'CODE_RUN': code('''import java.io.*;
import java.nio.file.*;

public class Main {
    public static void main(String[] args) throws IOException {
        try (BufferedWriter w = Files.newBufferedWriter(Path.of("menu.txt"))) {
            w.write("Masala Dosa,80");
            w.newLine();
            w.write("Idli Sambar,50");
            w.newLine();
            w.write("Filter Coffee,25");
            w.newLine();
        }
        try (BufferedReader r = Files.newBufferedReader(Path.of("menu.txt"))) {
            String line;
            while ((line = r.readLine()) != null) {
                String[] f = line.split(",");
                System.out.printf("%-14s Rs %3s%n", f[0], f[1]);
            }
        }
    }
}'''),
'RUNNER': runner([
 dict(label="1 · Write a menu, read it back", hint="Press <b>Run</b>. Then add a dish. Notice there's no <code>flush()</code>: try-with-resources closes, and closing flushes.",
      code='''import java.io.*;
import java.nio.file.*;

public class Main {
    public static void main(String[] args) throws IOException {
        try (BufferedWriter w = Files.newBufferedWriter(Path.of("menu.txt"))) {
            w.write("Masala Dosa,80");
            w.newLine();
            w.write("Idli Sambar,50");
            w.newLine();
        }
        try (BufferedReader r = Files.newBufferedReader(Path.of("menu.txt"))) {
            String line;
            while ((line = r.readLine()) != null) {
                System.out.println(line.replace(",", "  Rs "));
            }
        }
    }
}'''),
 dict(label="2 · Predict: the forgotten close", hint="<b>Predict first:</b> how many lines does the reader find? Then add <code>w.close();</code> before reading.",
      code='''import java.io.*;
import java.nio.file.*;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedWriter w = new BufferedWriter(new FileWriter("orders.txt"));
        for (int i = 1; i <= 3; i++) {
            w.write("order " + i);
            w.newLine();
        }
        System.out.println("lines on disk: " + Files.readAllLines(Path.of("orders.txt")).size());
    }
}'''),
 dict(label="3 · Predict: how much time?", hint="<b>Predict first:</b> which loop is faster? Run it a few times (timings vary). Each unbuffered <code>write</code> is a call into the operating system.",
      code='''import java.io.*;

public class Main {
    public static void main(String[] args) throws IOException {
        long t0 = System.nanoTime();
        try (OutputStream out = new FileOutputStream("slow.dat")) {
            for (int i = 0; i < 200_000; i++) out.write('x');
        }
        long t1 = System.nanoTime();
        try (OutputStream out = new BufferedOutputStream(new FileOutputStream("fast.dat"))) {
            for (int i = 0; i < 200_000; i++) out.write('x');
        }
        long t2 = System.nanoTime();
        System.out.println("unbuffered: " + (t1 - t0) / 1_000_000 + " ms");
        System.out.println("buffered:   " + (t2 - t1) / 1_000_000 + " ms");
    }
}'''),
 dict(label="4 · Crash: reading after close", hint="A closed reader can't be used. Do all the reading inside the try block.",
      code='''import java.io.*;
import java.nio.file.*;

public class Main {
    public static void main(String[] args) throws IOException {
        Files.writeString(Path.of("a.txt"), "line 1\\nline 2\\n");
        BufferedReader br = new BufferedReader(new FileReader("a.txt"));
        System.out.println(br.readLine());
        br.close();
        System.out.println(br.readLine());
    }
}''', _expect="exception"),
 dict(label="5 · Spot the error", hint="<code>readLine()</code> belongs to <code>BufferedReader</code>, not <code>FileReader</code>. Wrap it: <code>new BufferedReader(new FileReader(...))</code>.",
      code='''import java.io.*;

public class Main {
    public static void main(String[] args) throws IOException {
        try (FileReader r = new FileReader("a.txt")) {
            String first = r.readLine();
            System.out.println(first);
        }
    }
}''', _expect="compile-error"),
]),
'QUIZ': quiz([
 {"q": "Why is buffered I/O faster?", "options": ["It compresses data", "It groups many small reads/writes into few large OS calls", "It uses more threads", "It skips encoding"], "answer": 1, "why": "System calls are expensive; a buffer turns thousands of tiny ones into a few big ones."},
 {"q": "What is the default buffer size of BufferedReader/BufferedWriter?", "options": ["512", "1024", "8192 characters", "64 KB"], "answer": 2, "why": "8,192 chars by default; you can pass another size to the constructor."},
 {"q": "What does readLine() return at the end of the file?", "options": ["\"\"", "-1", "null", "\"EOF\""], "answer": 2, "why": "An empty line returns \"\"; only end of stream returns null."},
 {"q": "Does readLine() include the line break?", "options": ["Yes, always", "No", "Only on Windows", "Only the last line"], "answer": 1, "why": "It returns the text without \\n or \\r\\n."},
 {"q": "You write with a BufferedWriter and the program ends without close() or flush(). The file…", "options": ["has all the data", "may be missing the data still in the buffer", "is deleted", "is corrupted with random bytes"], "answer": 1, "why": "Buffered data only reaches the file on flush or close."},
 {"q": "Which statement is true about close()?", "options": ["It does not flush", "It flushes the buffer and closes the underlying stream", "It only closes the outer wrapper", "It deletes the file"], "answer": 1, "why": "Closing the outer stream closes the whole chain."},
 {"q": "BufferedReader wrapping FileReader is an example of…", "options": ["inheritance", "the decorator (wrapper) pattern", "singleton", "recursion"], "answer": 1, "why": "Each wrapper adds behaviour around another stream with the same interface."},
 {"q": "Files.newBufferedWriter(path) gives you…", "options": ["an unbuffered writer", "a BufferedWriter using UTF-8", "a PrintStream", "a byte stream"], "answer": 1, "why": "It's the modern shortcut for a buffered, UTF-8 writer."},
]),
}
