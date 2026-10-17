import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from mkanim import Anim, two_view
from m13 import code, snippet, runner, quiz

def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

# ---------------- Part 5: two-view animation ----------------
S = Anim("see", frames=6, h=250, label="The text Hi₹ is 3 characters but 5 bytes; a byte stream sees bytes, a character stream sees characters")
S.box(8, 8, 344, 40, None, fill="board", stroke="board")
codes = {1: 'String note = "Hi₹";', 2: 'out.write(bytes);   // OutputStream', 3: 'out.write(bytes);   // OutputStream',
         4: '// note.txt on disk', 5: 'reader.read()      // Reader', 6: 'in.read()          // InputStream'}
for f, c in codes.items():
    S.text(18, 33, esc(c), on=str(f), mono=True, size=9.6, cls="chalk")
chars = [("H", 30), ("i", 80), ("₹", 130)]
for ch, x in chars:
    S.box(x, 62, 44, 34, ch, fill="soft-green", stroke="green", size=14, bold=True, on="1-3,5")
S.text(190, 84, "3 characters", size=10, bold=True, cls="green", on="1")
S.text(190, 84, "3 chars again", size=10, bold=True, cls="green", on="5")
bytes_ = ["72", "105", "226", "130", "185"]
for i, b in enumerate(bytes_):
    on = "2-" if i < 2 else "3-"
    S.box(14 + i * 66, 120, 58, 34, b, fill="soft-acc" if i >= 2 else "soft-blue", stroke="track" if i >= 2 else "blue",
          size=11, bold=True, mono=True, on=on)
S.text(14, 172, "H and i: 1 byte each", size=9.5, cls="blue", on="2")
S.text(14, 172, "₹ needs 3 bytes in UTF-8", size=9.5, cls="acc", bold=True, on="3")
S.text(14, 172, "the file only stores these 5 numbers", size=9.5, cls="ink2", on="4")
S.text(14, 172, "a Reader decodes 3 bytes back into ₹", size=9.5, cls="green", on="5")
S.text(14, 172, "an InputStream hands you 226, then 130…", size=9.5, cls="red", on="6")
S.arrow(152, 96, 220, 118, on="3", color="track")
S.note({1: "Text: 3 characters.", 2: "Written as bytes…", 3: "…₹ becomes 3 bytes.", 4: "The file: 5 bytes.",
        5: "Character stream: 3 chars.", 6: "Byte stream: 5 numbers."}, y=234, size=10.5)
S.caps(["A Java <code>String</code> holds <b>characters</b>. <code>\"Hi₹\"</code> has 3.",
        "Files, networks and keyboards only move <b>bytes</b> (numbers 0–255). <code>H</code> is 72 and <code>i</code> is 105.",
        "In the UTF-8 encoding, <code>₹</code> doesn't fit in one byte: it becomes three bytes, 226 130 185.",
        "The file note.txt contains just these 5 bytes. It doesn't “know” they were text.",
        "A <b>character stream</b> (<code>Reader</code>) decodes the bytes with a charset and gives you back 3 characters.",
        "A <b>byte stream</b> (<code>InputStream</code>) gives you the raw bytes one at a time. Perfect for images and PDFs, wrong for text."])

B = Anim("behind", frames=6, h=250, label="The layers between your program and the disk: Writer, encoder, OutputStream, operating system, file")
layers = [("your code", "write(\"Hi₹\")", "card2", "line"), ("Writer", "OutputStreamWriter", "soft-green", "green"),
          ("encoder", "UTF-8: chars → bytes", "soft-acc", "track"), ("OutputStream", "FileOutputStream", "soft-blue", "blue"),
          ("operating system", "file descriptor", "card", "line"), ("disk", "note.txt: 5 bytes", "board", "board")]
for i, (t, sub, fill, stroke) in enumerate(layers):
    y = 6 + i * 36
    B.box(10, y, 230, 30, None, fill=fill, stroke=stroke)
    B.text(20, y + 19, t, size=9.6, bold=True, cls="chalk" if fill == "board" else "ink")
    B.text(120, y + 19, esc(sub), size=8.8, mono=True, cls="chalk" if fill == "board" else "ink2")
    B.box(8, y - 2, 234, 34, None, fill="none", stroke="red", on=str(i + 1), sw=2.2, rx=7)
side = {1: "characters", 2: "still characters", 3: "chars → bytes", 4: "bytes", 5: "system call", 6: "stored bytes"}
for f, t in side.items():
    B.text(254, 22 + (f - 1) * 36, t, on=str(f), size=9.6, bold=True, cls="acc")
B.arrow(250, 30, 250, 210, color="line", sw=1.2)
B.note({1: "Your program has text.", 2: "A Writer accepts chars.", 3: "The charset encodes them.",
        4: "An OutputStream moves bytes.", 5: "The OS does the real write.", 6: "Bytes land on disk."}, y=236, size=10.5)
B.caps(["Your program calls <code>writer.write(\"Hi₹\")</code> with characters.",
        "A <code>Writer</code> is a <b>character stream</b>. <code>OutputStreamWriter</code> is the bridge from characters to bytes.",
        "Inside the bridge, a <b>charset encoder</b> (here UTF-8) turns each character into one or more bytes.",
        "The bytes go to a <b>byte stream</b>, <code>FileOutputStream</code>, which knows nothing about text.",
        "The JVM asks the operating system to write the bytes through a file handle. This is slow compared with memory, which is why buffering matters (Lesson 13.3).",
        "The disk holds 5 bytes. Reading goes back up the same layers: <code>FileInputStream</code> → <code>InputStreamReader</code> (decoder) → your <code>String</code>."])
ANIM = two_view("Bytes vs characters, both views", S, B)

# ---------------- Part 6: animated example ----------------
ANIM2_HEADING = "Watch it with an example: why ₹ turned into “â‚¹” in a bank statement"
ANIM2_INTRO = "A bank exports statements as CSV files written in UTF-8. A customer opens one in an old spreadsheet program that assumes the Windows-1252 charset."
A = Anim("The same bytes, two charsets", frames=5, h=230, label="UTF-8 bytes of ₹500 decoded with the wrong charset show â‚¹500; with UTF-8 they show ₹500")
A.box(10, 14, 120, 40, None, fill="soft-green", stroke="green")
A.text(70, 40, "₹500", size=15, bold=True, anchor="middle")
A.text(70, 70, "in the bank app", size=9, anchor="middle", cls="ink3")
bts = ["E2", "82", "B9", "35", "30", "30"]
for i, b in enumerate(bts):
    A.box(150 + i * 33, 18, 29, 30, b, fill="soft-acc" if i < 3 else "soft-blue", stroke="track" if i < 3 else "blue",
          size=9.5, bold=True, mono=True, on="2-")
A.text(150, 70, "UTF-8 bytes (hex)", size=9, cls="ink3", on="2-")
A.box(150, 86, 196, 30, "statement.csv", fill="card2", stroke="line", size=10, mono=True, on="3-")
A.box(10, 140, 160, 50, None, fill="card", stroke="red", on="4-")
A.text(20, 158, "read as Windows-1252", size=9, cls="red", bold=True, on="4-")
A.text(20, 180, "â‚¹500", size=13, bold=True, mono=True, on="4-")
A.box(186, 140, 160, 50, None, fill="card", stroke="green", on="5")
A.text(196, 158, "read as UTF-8", size=9, cls="green", bold=True, on="5")
A.text(196, 180, "₹500", size=13, bold=True, mono=True, on="5")
A.arrow(248, 116, 100, 138, on="4-", color="red")
A.arrow(248, 116, 266, 138, on="5", color="green")
A.note({1: "The amount as text.", 2: "Encoded to 6 bytes.", 3: "Saved to a file.", 4: "Wrong charset: garbage.", 5: "Right charset: ₹500."}, y=206, size=10.5)
A.caps(["The statement line shows ₹500: four characters.",
        "Writing with UTF-8 gives six bytes: three for ₹ (E2 82 B9) and one each for 5, 0, 0.",
        "The file stores only those bytes; nothing in a plain CSV says which charset was used.",
        "The spreadsheet decodes each byte as one Windows-1252 character: E2 → â, 82 → ‚, B9 → ¹. The customer sees “â‚¹500” and calls the bank.",
        "Decoded with UTF-8, the same bytes give ₹500 again. The rule: <b>always name the charset</b> when you turn bytes into text or text into bytes."])
ANIM2 = A

# ---------------- Part 8: tracer ----------------
TRACE = dict(code='''import java.io.*;
import java.nio.charset.StandardCharsets;

public class Main {
    public static void main(String[] args) throws IOException {
        String note = "Hi\\u20B9";
        byte[] data = note.getBytes(StandardCharsets.UTF_8);
        InputStream bytesIn = new ByteArrayInputStream(data);
        int first = bytesIn.read();
        int third = bytesIn.skip(1) == 1 ? bytesIn.read() : -1;
        Reader charsIn = new InputStreamReader(new ByteArrayInputStream(data), StandardCharsets.UTF_8);
        int chars = 0;
        while (charsIn.read() != -1) {
            chars++;
        }
        System.out.println(note.length() + " chars, " + data.length + " bytes; first byte " + first + ", third byte " + third + "; reader saw " + chars + " chars");
    }
}
''', notes={
 6: "Text :: <code>\\u20B9</code> is the rupee sign ₹. The String holds 3 characters.",
 7: "Encode :: = <code>getBytes(UTF_8)</code> turns the 3 characters into a <code>byte[]</code> of 5 bytes. Java bytes are signed, so 226 shows as −30.",
 8: "Byte stream :: = A ByteArrayInputStream reads from that array in memory, exactly as a FileInputStream would read from a file.",
 9: "read() :: = <code>read()</code> returns the next byte as an int from 0 to 255: 72 for <code>H</code>.",
 10: "Skip, read :: = Skip <code>i</code>, then read the first byte of ₹: 226. On its own it's not a character.",
 11: "Character stream :: = <code>InputStreamReader</code> wraps a fresh byte stream and decodes UTF-8.",
 13: "Read chars :: The reader returns one character per call and −1 at the end.",
 16: "Result :: Same data: 5 bytes to a byte stream, 3 characters to a reader."})

# ---------------- Worked examples ----------------
WORKED_INTRO = "Three everyday jobs: copying a file byte by byte, reading text with a character stream, and fixing a charset bug. The programs create their own small files, so you can run them as they are."
EXAMPLES = [
dict(tag="Office · backups", title="Back up an invoice file byte by byte",
 problem="<p>An office app saves invoices as files. Before overwriting one, it must make a backup copy. Write the invoice with a <code>FileOutputStream</code>, copy it to <code>invoice.bak</code> with a byte-stream loop, and confirm both files are the same size.</p>",
 inp="invoice text: INV-7 Rs 236",
 approach=["Write the bytes of the text to invoice.txt.",
           "Open a <code>FileInputStream</code> on it and a <code>FileOutputStream</code> on the backup, both in try-with-resources.",
           "Loop: <code>read()</code> one byte, <code>write()</code> it, until <code>read()</code> returns −1. Count the bytes."],
 code='''import java.io.*;
import java.nio.charset.StandardCharsets;

public class Main {
    public static void main(String[] args) throws IOException {
        try (FileOutputStream out = new FileOutputStream("invoice.txt")) {
            out.write("INV-7 Rs 236".getBytes(StandardCharsets.UTF_8));
        }
        int copied = 0;
        try (FileInputStream in = new FileInputStream("invoice.txt");
             FileOutputStream bak = new FileOutputStream("invoice.bak")) {
            int b;
            while ((b = in.read()) != -1) {
                bak.write(b);
                copied++;
            }
        }
        File a = new File("invoice.txt"), c = new File("invoice.bak");
        System.out.println("copied " + copied + " bytes; sizes " + a.length() + " and " + c.length());
    }
}
''', notes={6: "Open for writing :: = A FileOutputStream creates invoice.txt (or empties it if it exists).",
            7: "Write bytes :: = The text is encoded to 12 bytes and written.",
            8: "Closed :: = Leaving the try block closes the stream, so the bytes are really in the file.",
            10: "Two streams :: = One stream reads the original, the other writes the backup.",
            (13, 1): "First byte :: = <code>read()</code> returns 73, the code for <code>I</code>.",
            (13, 13): "End :: = <code>read()</code> returns −1: no more bytes. The loop stops.",
            18: "Check :: Two File objects describe the paths; <code>length()</code> asks the OS for each size.",
            19: "Report :: 12 bytes copied; both files are 12 bytes."},
 tryit="Press <b>Run</b>. Then change the text and check that the counts still match. Byte copying works for any file: images, PDFs, zip files."),
dict(tag="Restaurant · menu", title="Read a menu with a character stream",
 problem="<p>A restaurant keeps its menu in menu.txt, one dish per line, including Hindi names. Read it with a <code>Reader</code>, one character at a time, and count the characters and lines.</p>",
 inp="menu.txt: Dosa / Idli / पनीर टिक्का",
 approach=["Write the file with a <code>FileWriter</code>, naming UTF-8.",
           "Read it back with a <code>FileReader</code> (UTF-8) one character at a time.",
           "Count characters, and count <code>'\\n'</code> as line ends."],
 code='''import java.io.*;
import java.nio.charset.StandardCharsets;

public class Main {
    public static void main(String[] args) throws IOException {
        try (Writer w = new FileWriter("menu.txt", StandardCharsets.UTF_8)) {
            w.write("Dosa\\nIdli\\n\\u092A\\u0928\\u0940\\u0930\\n");
        }
        int chars = 0, lines = 0;
        try (Reader r = new FileReader("menu.txt", StandardCharsets.UTF_8)) {
            int c;
            while ((c = r.read()) != -1) {
                chars++;
                if (c == '\\n') lines++;
            }
        }
        long bytes = new File("menu.txt").length();
        System.out.println(lines + " lines, " + chars + " chars, " + bytes + " bytes on disk");
    }
}
''', notes={6: "Writer :: = A FileWriter that encodes with UTF-8.",
            7: "Write text :: = Two English dishes and the Hindi word पनीर (4 characters, 3 bytes each in UTF-8).",
            10: "Reader :: = A FileReader decoding UTF-8.",
            (12, 1): "First char :: = <code>read()</code> returns the character <code>D</code> (as an int).",
            17: "Bytes :: The file has more bytes than characters, because each Hindi letter takes 3 bytes.",
            18: "Report :: 3 lines, 15 characters, 23 bytes."},
 tryit="Press <b>Run</b>. Then add another dish. Compare chars and bytes: English letters are 1 byte each, Hindi letters 3."),
dict(tag="Banking · exports", title="Find and fix a charset bug",
 problem="<p>A statement line <code>Paid ₹500</code> is saved in UTF-8. A legacy tool reads it as Windows-1252 and shows garbage. Reproduce the bug, then read it correctly. Print through a UTF-8 <code>PrintStream</code> so the console shows ₹ properly.</p>",
 inp="Paid ₹500",
 approach=["Write the text to statement.csv with UTF-8.",
           "Read all bytes, then decode them twice: once with windows-1252, once with UTF-8.",
           "Print both through <code>new PrintStream(System.out, true, UTF_8)</code>."],
 code='''import java.io.*;
import java.nio.charset.*;

public class Main {
    public static void main(String[] args) throws IOException {
        PrintStream out = new PrintStream(System.out, true, StandardCharsets.UTF_8);
        try (Writer w = new OutputStreamWriter(new FileOutputStream("statement.csv"), StandardCharsets.UTF_8)) {
            w.write("Paid \\u20B9500");
        }
        byte[] raw;
        try (InputStream in = new FileInputStream("statement.csv")) {
            raw = in.readAllBytes();
        }
        String wrong = new String(raw, Charset.forName("windows-1252"));
        String right = new String(raw, StandardCharsets.UTF_8);
        out.println("bytes: " + raw.length);
        out.println("as windows-1252: " + wrong);
        out.println("as UTF-8:        " + right);
    }
}
''', notes={6: "Console stream :: = A PrintStream that encodes what you print as UTF-8, so the console can show ₹.",
            7: "Writer :: = An OutputStreamWriter (UTF-8) on top of a FileOutputStream.",
            8: "Write :: = 9 characters become 11 bytes.",
            12: "Read bytes :: = <code>readAllBytes()</code> returns the whole file as a byte array.",
            14: "Wrong decode :: = Each byte becomes one Windows-1252 character, so ₹ turns into three characters.",
            15: "Right decode :: = UTF-8 turns the three bytes back into one ₹.",
            17: "Bug :: The garbled text customers would see.",
            18: "Fixed :: The correct text."},
 tryit="Press <b>Run</b>. Then try <code>StandardCharsets.ISO_8859_1</code> for the wrong decode: the garbage looks different, because each charset maps bytes differently."),
]

# ---------------- Practice problems ----------------
PRACTICE_INTRO = "Work with byte streams and character streams, in memory and on files, and always close what you open. Each program makes its own files, so the output is the same every run. The last three are business tasks."
PROBLEMS = [
dict(level="easy", title="Bytes of a word", stmt="<p>Print the UTF-8 byte values (0–255) of <code>Java</code> using a <code>ByteArrayInputStream</code> and <code>read()</code>.</p>", inp="Java",
 code='''import java.io.*;
import java.nio.charset.StandardCharsets;

public class Main {
    public static void main(String[] args) throws IOException {
        InputStream in = new ByteArrayInputStream("Java".getBytes(StandardCharsets.UTF_8));
        int b;
        while ((b = in.read()) != -1) {
            System.out.print(b + " ");
        }
        System.out.println();
    }
}''', explain="<p><b>How it works:</b> <code>read()</code> returns the next byte as an int 0–255, or −1 at the end. Using an <code>int</code> (not a <code>byte</code>) is what lets −1 mean “end” without clashing with any real byte value.</p>"),
dict(level="easy", title="Write and read a file", stmt="<p>Write <code>Hello file</code> to greet.txt with a <code>FileWriter</code>, then read it back character by character with a <code>FileReader</code> and print it.</p>", inp="Hello file",
 code='''import java.io.*;

public class Main {
    public static void main(String[] args) throws IOException {
        try (FileWriter w = new FileWriter("greet.txt")) {
            w.write("Hello file");
        }
        StringBuilder sb = new StringBuilder();
        try (FileReader r = new FileReader("greet.txt")) {
            int c;
            while ((c = r.read()) != -1) sb.append((char) c);
        }
        System.out.println(sb);
    }
}''', explain="<p><b>How it works:</b> the int from <code>read()</code> is cast back to <code>char</code>. Since Java 18 FileWriter and FileReader use UTF-8 by default; naming the charset is still clearer.</p>"),
dict(level="easy", title="Characters vs bytes", stmt="<p>For the word <code>नमस्ते</code>, print its length in characters and in UTF-8 bytes.</p>", inp="नमस्ते",
 code='''import java.nio.charset.StandardCharsets;

public class Main {
    public static void main(String[] args) {
        String word = "\\u0928\\u092E\\u0938\\u094D\\u0924\\u0947";
        System.out.println(word.length() + " chars, " + word.getBytes(StandardCharsets.UTF_8).length + " bytes");
    }
}''', explain="<p><b>How it works:</b> each Devanagari code point here takes 3 bytes in UTF-8, so 6 characters become 18 bytes. Limits like “max 160 bytes” in SMS or database columns are about bytes, not characters.</p>"),
dict(level="medium", title="Count lines in a file", stmt="<p>Write three lines to log.txt and count the line breaks by reading characters.</p>", inp="three log lines",
 code='''import java.io.*;

public class Main {
    public static void main(String[] args) throws IOException {
        try (Writer w = new FileWriter("log.txt")) {
            w.write("login ok\\npayment ok\\nlogout\\n");
        }
        int lines = 0;
        try (Reader r = new FileReader("log.txt")) {
            int c;
            while ((c = r.read()) != -1) if (c == '\\n') lines++;
        }
        System.out.println("lines: " + lines);
    }
}''', explain="<p><b>How it works:</b> a text file is just characters; lines are separated by <code>'\\n'</code>. Lesson 13.3's <code>BufferedReader.readLine()</code> does this for you, much faster.</p>"),
dict(level="medium", title="Append instead of overwrite", stmt="<p>Write <code>A</code> to audit.txt, then open it again in <b>append</b> mode and add <code>B</code>. Print the file's contents.</p>", inp="A then B",
 code='''import java.io.*;
import java.nio.charset.StandardCharsets;

public class Main {
    public static void main(String[] args) throws IOException {
        try (FileOutputStream f = new FileOutputStream("audit.txt")) {
            f.write('A');
        }
        try (FileOutputStream f = new FileOutputStream("audit.txt", true)) {
            f.write('B');
        }
        try (FileInputStream in = new FileInputStream("audit.txt")) {
            System.out.println(new String(in.readAllBytes(), StandardCharsets.UTF_8));
        }
    }
}''', explain="<p><b>How it works:</b> by default a FileOutputStream starts the file empty. The second constructor argument <code>true</code> means append. Forgetting it is a classic way to lose a log file.</p>"),
dict(level="medium", title="Handle a missing file", stmt="<p>Try to open orders.csv, which doesn't exist. Catch the exception and print a friendly message with its type.</p>", inp="(no file)",
 code='''import java.io.*;

public class Main {
    public static void main(String[] args) {
        try (FileInputStream in = new FileInputStream("orders.csv")) {
            System.out.println("first byte: " + in.read());
        } catch (FileNotFoundException e) {
            System.out.println("No orders file yet (" + e.getClass().getSimpleName() + ")");
        } catch (IOException e) {
            System.out.println("Could not read orders: " + e.getMessage());
        }
    }
}''', explain="<p><b>How it works:</b> <code>FileNotFoundException</code> is a subclass of <code>IOException</code>, so it must be caught first. Every I/O method can throw IOException because disks and networks can fail.</p>"),
dict(level="business", title="Receipt size check for a printer", stmt="<p>A thermal printer accepts at most 32 bytes per line. Check each receipt line's UTF-8 size and mark lines that are too long.</p>", inp="3 receipt lines",
 code='''import java.nio.charset.StandardCharsets;

public class Main {
    public static void main(String[] args) {
        String[] lines = {"Masala Dosa x2   Rs 180", "Filter Coffee x3 Rs 90", "Paneer Butter Masala Family Pack Rs 520"};
        for (String l : lines) {
            int size = l.getBytes(StandardCharsets.UTF_8).length;
            System.out.println((size <= 32 ? "OK   " : "LONG ") + size + " bytes: " + l);
        }
    }
}''', explain="<p><b>How it works:</b> devices and protocols limit bytes, not characters. Measuring with the same charset the printer uses avoids cut-off lines.</p>"),
dict(level="business", title="Save a binary price table", stmt="<p>Save three prices (in paise) as raw bytes using <code>DataOutputStream</code>, then read them back with <code>DataInputStream</code> and print the total in rupees.</p>", inp="prices 1999, 4950, 120 (paise)",
 code='''import java.io.*;

public class Main {
    public static void main(String[] args) throws IOException {
        int[] paise = {1999, 4950, 120};
        try (DataOutputStream out = new DataOutputStream(new FileOutputStream("prices.bin"))) {
            for (int p : paise) out.writeInt(p);
        }
        int total = 0;
        try (DataInputStream in = new DataInputStream(new FileInputStream("prices.bin"))) {
            for (int i = 0; i < paise.length; i++) total += in.readInt();
        }
        System.out.println("file size " + new File("prices.bin").length() + " bytes, total Rs " + total / 100 + "." + total % 100);
    }
}''', explain="<p><b>How it works:</b> <code>DataOutputStream</code> is a filter on a byte stream that writes each int as exactly 4 bytes, so 3 prices take 12 bytes. Binary formats are compact, but you need the same program logic to read them back.</p>"),
dict(level="business", title="Copy a file with a buffer array", stmt="<p>Copying one byte per call is slow. Copy a 10,000-byte file using a 1,024-byte array with <code>read(byte[])</code>, and count how many read calls were needed.</p>", inp="10,000-byte file",
 code='''import java.io.*;

public class Main {
    public static void main(String[] args) throws IOException {
        try (FileOutputStream f = new FileOutputStream("scan.dat")) {
            f.write(new byte[10_000]);
        }
        int calls = 0;
        long copied = 0;
        try (InputStream in = new FileInputStream("scan.dat");
             OutputStream out = new FileOutputStream("scan-copy.dat")) {
            byte[] buf = new byte[1024];
            int n;
            while ((n = in.read(buf)) != -1) {
                out.write(buf, 0, n);
                copied += n;
                calls++;
            }
        }
        System.out.println("copied " + copied + " bytes in " + calls + " reads");
    }
}''', explain="<p><b>How it works:</b> <code>read(buf)</code> fills up to 1,024 bytes and returns how many it actually read; the last chunk is shorter, so always write <code>n</code> bytes, not the whole array. 10 reads instead of 10,000 (for a local file; a stream may return fewer bytes per call). Java 9+ also has <code>in.transferTo(out)</code>.</p>"),
]

# ---------------- Extra blocks ----------------
BLOCKS = {
'ANIM': ANIM,
'CODE_STD': code('''public class Main {
    public static void main(String[] args) {
        System.out.println("System.in  is a " + System.in.getClass().getSimpleName() + " (bytes from the keyboard)");
        System.out.println("System.out is a " + System.out.getClass().getSimpleName() + " (bytes to the console)");
        System.err.println("System.err is for error messages");
    }
}'''),
'CODE_TREE': snippet('''               BYTE streams                         CHARACTER streams
        InputStream     OutputStream              Reader            Writer
          FileInputStream   FileOutputStream        FileReader        FileWriter
          ByteArrayInputStream ...                  InputStreamReader OutputStreamWriter   (bridges)
          BufferedInputStream BufferedOutputStream  BufferedReader    BufferedWriter
          DataInputStream  DataOutputStream          StringReader      PrintWriter
          ObjectInputStream ObjectOutputStream (13.4)''', lang='text', file='java.io'),
'CODE_RUN': code('''import java.io.*;
import java.nio.charset.StandardCharsets;

public class Main {
    public static void main(String[] args) throws IOException {
        String note = "Order #77: 2 x Vada Pav";
        try (OutputStream out = new FileOutputStream("note.txt")) {
            out.write(note.getBytes(StandardCharsets.UTF_8));
        }
        try (InputStream in = new FileInputStream("note.txt")) {
            int first = in.read();
            System.out.println("first byte: " + first + " = '" + (char) first + "'");
        }
        try (Reader r = new FileReader("note.txt", StandardCharsets.UTF_8)) {
            char[] buf = new char[100];
            int n = r.read(buf);
            System.out.println("read " + n + " chars: " + new String(buf, 0, n));
        }
    }
}'''),
'RUNNER': runner([
 dict(label="1 · Write, then read two ways", hint="Press <b>Run</b>. Then change the note and run again: the byte count and the character count stay equal while the text is plain English.",
      code='''import java.io.*;
import java.nio.charset.StandardCharsets;

public class Main {
    public static void main(String[] args) throws IOException {
        String note = "Order #77: 2 x Vada Pav";
        try (OutputStream out = new FileOutputStream("note.txt")) {
            out.write(note.getBytes(StandardCharsets.UTF_8));
        }
        try (InputStream in = new FileInputStream("note.txt")) {
            System.out.println("bytes in file: " + in.readAllBytes().length);
        }
        try (Reader r = new FileReader("note.txt", StandardCharsets.UTF_8)) {
            int chars = 0;
            while (r.read() != -1) chars++;
            System.out.println("chars read:    " + chars);
        }
    }
}'''),
 dict(label="2 · Predict: a byte cast to char", hint="<b>Predict first:</b> the text has a ₹. What does casting each <i>byte</i> to a char print? (The console may show odd symbols; that's the point.)",
      code='''import java.io.*;
import java.nio.charset.StandardCharsets;

public class Main {
    public static void main(String[] args) throws IOException {
        InputStream in = new ByteArrayInputStream("Rs\\u20B9".getBytes(StandardCharsets.UTF_8));
        int b, count = 0;
        while ((b = in.read()) != -1) {
            count++;
            System.out.println("byte " + count + " = " + b);
        }
        System.out.println(count + " bytes for 3 characters");
    }
}'''),
 dict(label="3 · Predict: forgot to append", hint="<b>Predict first:</b> what's in the file after two writes? Then pass <code>true</code> as the second argument of the second FileWriter.",
      code='''import java.io.*;

public class Main {
    public static void main(String[] args) throws IOException {
        try (FileWriter w = new FileWriter("visits.log")) { w.write("visit 1\\n"); }
        try (FileWriter w = new FileWriter("visits.log")) { w.write("visit 2\\n"); }
        try (FileReader r = new FileReader("visits.log")) {
            int c;
            while ((c = r.read()) != -1) System.out.print((char) c);
        }
    }
}'''),
 dict(label="4 · Crash: file not found", hint="The file doesn't exist. Read the exception, then either create the file first or catch <code>FileNotFoundException</code>.",
      code='''import java.io.*;

public class Main {
    public static void main(String[] args) throws IOException {
        FileReader r = new FileReader("customers.csv");
        System.out.println((char) r.read());
        r.close();
    }
}''', _expect="exception"),
 dict(label="5 · Spot the error", hint="Almost every I/O method throws the checked <code>IOException</code>. Add <code>throws IOException</code> to main, or use try/catch.",
      code='''import java.io.*;

public class Main {
    public static void main(String[] args) {
        FileWriter w = new FileWriter("hello.txt");
        w.write("hello");
        w.close();
    }
}''', _expect="compile-error"),
]),
'QUIZ': quiz([
 {"q": "Which are the base classes of character streams?", "options": ["InputStream and OutputStream", "Reader and Writer", "File and Path", "Scanner and PrintStream"], "answer": 1, "why": "Byte streams: InputStream/OutputStream. Character streams: Reader/Writer."},
 {"q": "What does InputStream.read() return at the end of the stream?", "options": ["0", "null", "-1", "It throws EOFException"], "answer": 2, "why": "read() returns 0–255 for a byte and −1 at end of stream; that's why it returns int."},
 {"q": "Which stream should you use to copy a JPG photo?", "options": ["FileReader", "FileInputStream", "BufferedReader", "Scanner"], "answer": 1, "why": "Images are binary: use byte streams. Character streams would try to decode them as text."},
 {"q": "In UTF-8, how many bytes does ₹ take?", "options": ["1", "2", "3", "4"], "answer": 2, "why": "U+20B9 is encoded as E2 82 B9."},
 {"q": "InputStreamReader is…", "options": ["a byte stream", "a bridge that decodes bytes into characters using a charset", "a buffered reader", "a file"], "answer": 1, "why": "It wraps an InputStream and decodes with the charset you give it."},
 {"q": "Why should streams be opened in try-with-resources?", "options": ["It's faster", "They are closed automatically, even if an exception occurs", "It's required by the compiler", "To make them buffered"], "answer": 1, "why": "Unclosed streams leak file handles and may lose unwritten data."},
 {"q": "new FileOutputStream(\"a.txt\") on an existing file…", "options": ["appends", "empties it first", "throws", "makes a backup"], "answer": 1, "why": "Pass true as the second argument to append."},
 {"q": "System.out is a…", "options": ["Writer", "PrintStream (a byte stream with print methods)", "Reader", "File"], "answer": 1, "why": "PrintStream extends OutputStream and encodes text to bytes for the console."},
]),
}
