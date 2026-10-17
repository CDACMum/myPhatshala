import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../..'))
from mkanim import Anim, two_view

# ---------------- Part 5: two-view animation ----------------
S = Anim("see", frames=6, h=250, label="Adding the same student twice to a HashSet, first without hashCode, then with it")
S.box(8, 8, 344, 26, None, fill="soft-acc", stroke="red", on="1-3", rx=6)
S.text(180, 26, "Student overrides equals() only", on="1-3", anchor="middle", size=10.5, bold=True, cls="red")
S.box(8, 8, 344, 26, None, fill="soft-green", stroke="green", on="4-6", rx=6)
S.text(180, 26, "Student overrides equals() and hashCode()", on="4-6", anchor="middle", size=10.5, bold=True, cls="green")
S.box(8, 42, 344, 92, None, fill="board", stroke="board")
lines = ['set.add(new Student("21CS07"));', 'set.add(new Student("21CS07"));', "println(set.size());"]
for i, l in enumerate(lines):
    y = 66 + i * 24
    S.box(12, y - 15, 336, 21, None, fill="none", stroke="track", sw=2, on=f"{i + 1},{i + 4}", rx=4)
    S.text(20, y, l, mono=True, size=10.5, cls="chalk")
S.box(8, 144, 344, 58, None, fill="card2", stroke="line")
S.text(18, 162, "Returned / printed", size=9, cls="ink3", bold=True)
S.text(18, 188, "add → true", on="1,4", mono=True, size=11, cls="green", bold=True)
S.text(18, 188, "add → true   (duplicate accepted!)", on="2", mono=True, size=11, cls="red", bold=True)
S.text(18, 188, "size() = 2  ✗", on="3", mono=True, size=12, cls="red", bold=True)
S.text(18, 188, "add → false  (already there)", on="5", mono=True, size=11, cls="green", bold=True)
S.text(18, 188, "size() = 1  ✓", on="6", mono=True, size=12, cls="green", bold=True)
S.note({1: "First scan of Riya's card.", 2: "Second scan, same roll number.", 3: "The set counts Riya twice.",
        4: "Same code, hashCode() added.", 5: "The second scan is rejected.", 6: "One Riya, counted once."}, y=228, size=10.5)
S.caps(["Without <code>hashCode()</code>: the first Student is added. <code>add</code> returns true.",
        "The second Student has the same roll, and <code>equals</code> would say they're equal, yet <code>add</code> returns <b>true</b> again.",
        "<code>size()</code> is 2. The duplicate got in.",
        "Now <code>Student</code> also overrides <code>hashCode()</code> using the roll number. The first add works as before.",
        "The second add returns <b>false</b>: the set recognised the duplicate.",
        "<code>size()</code> is 1. Same main code; the only change was one method in Student."])
B = Anim("behind", frames=6, h=250, label="Inside the HashSet: hash codes choose buckets; equals is only checked inside the chosen bucket")
B.text(16, 22, "hashCode()", size=10, bold=True, cls="ink2")
B.text(16, 40, "identity: 0x1b6d…", on="1", mono=True, size=10, cls="ink")
B.text(16, 40, "identity: 0x4e25…", on="2-3", mono=True, size=10, cls="ink")
B.text(16, 40, "Objects.hash(roll) = 1478787413", on="4-6", mono=True, size=10, cls="green", bold=True)
B.text(16, 58, "→ bucket 3", on="1", mono=True, size=10, cls="blue", bold=True)
B.text(16, 58, "→ bucket 12 (different!)", on="2", mono=True, size=10, cls="red", bold=True)
B.text(16, 58, "→ bucket 1", on="4", mono=True, size=10, cls="blue", bold=True)
B.text(16, 58, "→ bucket 1 (same) → equals() → true", on="5", mono=True, size=10, cls="green", bold=True)
B.text(16, 58, "equals() never called", on="3", mono=True, size=10, cls="red", bold=True)
B.text(16, 58, "one entry per student", on="6", mono=True, size=10, cls="green", bold=True)
for k, b in enumerate([1, 3, 12]):
    y = 74 + k * 36
    B.box(14, y, 332, 30, None, fill="card", stroke="line", rx=5)
    B.text(24, y + 20, f"[{b}]", mono=True, size=10, cls="ink3")
B.box(70, 113, 120, 24, "Riya #1", fill="soft-acc", stroke="track", on="1-3", size=10, bold=True)
B.box(70, 149, 120, 24, "Riya #2", fill="soft-acc", stroke="red", on="2-3", size=10, bold=True)
B.box(70, 77, 120, 24, "Riya #1", fill="soft-acc", stroke="track", on="4-6", size=10, bold=True)
B.box(200, 77, 120, 24, "Riya #2 ?", fill="card2", stroke="green", on="5", size=10, bold=True)
B.text(204, 200, "equals: true → not added", on="5", size=9.5, bold=True, cls="green")
B.note({1: "Default hashCode is based on identity.", 2: "Another object, another number.", 3: "Two buckets, so no comparison happens.",
        4: "Hash now depends only on the roll.", 5: "Same bucket, so equals() runs and says equal.", 6: "Equal objects share one bucket."}, y=228, size=10)
B.caps(["Object's default <code>hashCode()</code> is an identity number, unrelated to the roll. It sends Riya #1 to bucket 3.",
        "Riya #2 is a different object, so its identity hash is different: bucket 12. The set only compares objects <b>inside</b> the chosen bucket, and bucket 12 is empty.",
        "<code>equals()</code> was never even called. Both objects stay: size 2.",
        "With <code>hashCode()</code> returning <code>Objects.hash(roll)</code>, the hash depends only on the roll number. Riya #1 goes to bucket 1.",
        "Riya #2 has the same roll, so the same hash and the same bucket 1. Now the set calls <code>equals()</code>, gets true, and refuses to add.",
        "That's the contract at work: equal objects must have equal hash codes, so they meet in the same bucket."])
ANIM = two_view("Why HashSet needs hashCode()", S, B)
BLOCKS = {'ANIM': ANIM}

# ---------------- Part 6: animated example ----------------
ANIM2_HEADING = "Watch it with an example: a train seat lookup"
ANIM2_INTRO = "A booking system stores who sits where in a <code>HashMap&lt;Seat, String&gt;</code>. The ticket checker creates a new Seat object from the printed ticket and looks it up."
A = Anim("Finding a booking by seat", frames=5, h=226, label="A HashMap get with a new but equal Seat key: hashCode finds the bucket, equals confirms the key")
A.box(10, 14, 130, 50, 'Seat("S4", 32)', sub="key used to book", fill="soft-blue", stroke="blue", size=10, mono=True, bold=True)
A.box(10, 84, 130, 50, 'Seat("S4", 32)', sub="new object from ticket", fill="soft-acc", stroke="track", on="2-", size=10, mono=True, bold=True)
A.box(170, 14, 182, 150, None, fill="card", stroke="line")
A.text(180, 32, "HashMap&lt;Seat, String&gt;", mono=True, size=9.5, bold=True, cls="ink2")
for k, b in enumerate(["[2]", "[9]", "[14]"]):
    A.box(180, 42 + k * 38, 162, 30, None, fill="card2", stroke="line", rx=5)
    A.text(188, 62 + k * 38, b, mono=True, size=9.5, cls="ink3")
A.box(214, 84, 122, 22, "S4-32 → Riya", fill="soft-green", stroke="green", size=9.5, mono=True, bold=True)
A.arrow(140, 39, 214, 92, on="1", color="blue", bend=-10)
A.arrow(140, 109, 214, 98, on="3-4", color="track")
A.box(214, 84, 122, 22, None, fill="none", stroke="track", sw=3, on="3-4")
A.text(181, 186, "hashCode(): coach + number → bucket [9]", on="3", anchor="middle", size=10.5, bold=True, cls="ink")
A.text(181, 186, "equals(): S4 = S4, 32 = 32 → same seat", on="4", anchor="middle", size=10.5, bold=True, cls="green")
A.box(10, 196, 342, 26, "get → \"Riya\"", fill="soft-green", stroke="green", on="5", size=11, bold=True, mono=True)
A.text(181, 186, "At booking: put(seat, \"Riya\") into bucket [9]", on="1", anchor="middle", size=10.5, cls="ink")
A.text(181, 186, "A different object, but the same seat", on="2", anchor="middle", size=10.5, cls="ink")
A.caps(["At booking time, <code>put(new Seat(\"S4\", 32), \"Riya\")</code> stores the entry in the bucket chosen by the seat's <code>hashCode()</code>.",
        "Later, the checker's app builds a <b>new</b> <code>Seat</code> object from the ticket. It is not the same object as the one used to book.",
        "<code>get</code> calls the new key's <code>hashCode()</code>. Because it's computed from coach and number, it picks the same bucket [9].",
        "Inside that bucket, <code>equals()</code> compares coach and number: equal. The key matches.",
        "The map returns “Riya”. Without the two overrides, <code>get</code> would return <code>null</code>. (Simplified: real systems also store date and train number in the key.)"])
ANIM2 = A

# ---------------- Part 8: tracer ----------------
TRACE = dict(code='''import java.util.HashSet;
import java.util.Objects;

class Student {
    String roll;

    Student(String roll) {
        this.roll = roll;
    }

    @Override
    public boolean equals(Object o) {
        if (!(o instanceof Student)) {
            return false;
        }
        Student other = (Student) o;
        return roll.equals(other.roll);
    }

    @Override
    public int hashCode() {
        int h = Objects.hash(roll);
        return h;
    }
}

public class Main {
    public static void main(String[] args) {
        HashSet<Student> present = new HashSet<>();
        boolean first = present.add(new Student("21CS07"));
        boolean again = present.add(new Student("21CS07"));
        System.out.println(first + " " + again + " " + present.size());
    }
}
''', notes={
 29: "Create :: An empty set. Its bucket table is created on the first add.",
 (30, 2): "add() calls you :: = Inside <code>add</code>, the HashSet calls <b>your</b> <code>hashCode()</code> on the new student #3: a frame is pushed.",
 (22, 1): "Hash :: Computed only from the roll number, so any Student with roll 21CS07 gets this same number.",
 (23, 1): "Bucket :: = <code>hashCode()</code> returns 1478787413. The set turns it into bucket 1, finds it empty and stores #3 there.",
 (30, 3): "Result :: <code>add</code> returned true: the student was added.",
 (31, 2): "add() calls you :: = The set asks the second student (#5) for its hash code.",
 (22, 2): "Hash :: = Same roll, same number: 1478787413. The set looks in the same bucket and finds #3 there.",
 (23, 2): "equals() :: = The hashes match, so the set calls <code>equals()</code> on #5 with <code>o</code> = #3, the student already in the bucket. A new frame is pushed.",
 13: "Check :: ",
 16: "Cast :: ",
 17: "Compare :: = Both rolls are \"21CS07\": <code>equals</code> returns true, its frame is popped, and the set refuses to add #5.",
 (31, 3): "Result :: <code>add</code> returned false. #5 is not stored anywhere.",
 32: "Print :: "})

# ---------------- Worked examples ----------------
WORKED_INTRO = "Three business classes that need the right Object methods. Watch the JVM call your <code>toString</code>, <code>hashCode</code> and <code>equals</code> from inside Java's own code."
EXAMPLES = [
dict(tag="E-commerce · receipts", title="A receipt line that prints itself",
 problem="<p>An order line has an item name, quantity and unit price in paise. Printing it should give <code>2 x Notebook @ ₹45.00 = ₹90.00</code>. Override <code>toString()</code>.</p>",
 inp='Line("Notebook", 2, 4500)',
 approach=["Store money in paise as <code>long</code>, so there are no rounding errors.",
           "A helper <code>rupees(long paise)</code> formats paise as ₹ with two decimals.",
           "<code>toString()</code> builds the line; <code>println</code> calls it automatically."],
 code='''class Line {
    String item;
    int qty;
    long paise;

    Line(String item, int qty, long paise) {
        this.item = item;
        this.qty = qty;
        this.paise = paise;
    }

    static String rupees(long p) {
        return String.format("₹%d.%02d", p / 100, p % 100);
    }

    @Override
    public String toString() {
        String text = qty + " x " + item + " @ " + rupees(paise);
        return text + " = " + rupees(qty * paise);
    }
}

public class Main {
    public static void main(String[] args) {
        Line l = new Line("Notebook", 2, 4500);
        System.out.println(l);
    }
}
''', notes={26: "Print :: = <code>println(l)</code> calls <code>String.valueOf(l)</code>, which calls <b>your</b> <code>toString()</code>: watch the frame appear."},
 tryit="Press <b>Run</b>. Then remove <code>toString()</code> and see the default <code>Line@…</code> output."),
dict(tag="Railways · lookup", title="Find a booking by seat",
 problem="<p>Bookings are stored in a <code>HashMap&lt;Seat, String&gt;</code>. The checker builds a new <code>Seat(\"S4\", 32)</code> from a ticket and must find the passenger. Override <code>equals</code> and <code>hashCode</code> on coach and number.</p>",
 inp='put(Seat("S4", 32), "Riya"); get(Seat("S4", 32))',
 approach=["Both methods use the same two fields: <code>coach</code> and <code>number</code>.",
           "<code>put</code> calls <code>hashCode</code> to choose a bucket.",
           "<code>get</code> with a new, equal Seat finds the same bucket, then <code>equals</code> confirms the key."],
 code='''import java.util.HashMap;
import java.util.Objects;

class Seat {
    String coach;
    int number;

    Seat(String coach, int number) {
        this.coach = coach;
        this.number = number;
    }

    @Override
    public boolean equals(Object o) {
        if (!(o instanceof Seat)) return false;
        Seat s = (Seat) o;
        return number == s.number && coach.equals(s.coach);
    }

    @Override
    public int hashCode() {
        return Objects.hash(coach, number);
    }
}

public class Main {
    public static void main(String[] args) {
        HashMap<Seat, String> booked = new HashMap<>();
        booked.put(new Seat("S4", 32), "Riya");
        String who = booked.get(new Seat("S4", 32));
        System.out.println("S4-32: " + who);
    }
}
''', notes={(29, 2): "put() calls you :: = Inside <code>put</code>, the HashMap calls <b>your</b> <code>hashCode()</code> on the key #3.",
            (22, 1): "Bucket :: = <code>hashCode()</code> returns a number made from \"S4\" and 32. The map stores the entry #3 → \"Riya\" in bucket 1.",
            (29, 3): "Done :: <code>put</code> has finished.",
            (30, 2): "get() calls you :: = Inside <code>get</code>, the map asks the <b>new</b> Seat #6 for its hash code.",
            (22, 2): "equals() :: = Same coach and number, so the same hash and the same bucket. The map finds key #3 there and calls your <code>equals()</code> with <code>this</code> = #6, <code>o</code> = #3.",
            15: "Check :: <code>o</code> is a Seat.", 16: "Cast :: ",
            17: "Compare :: = 32 == 32 and \"S4\" equals \"S4\": true. The frame is popped and <code>get</code> returns the value stored with #3.",
            (30, 3): "Result :: ", 31: "Print :: "},
 tryit="Press <b>Run</b>. Then delete <code>hashCode()</code> and run again: <code>get</code> returns <code>null</code>."),
dict(tag="Fintech · money", title="Is this refund already in the list?",
 problem="<p>A refund list holds <code>Money</code> values (paise + currency). Before adding a refund, check whether an equal amount is already pending. <code>ArrayList.contains</code> uses only <code>equals</code>.</p>",
 inp="pending: ₹250 INR, $5 USD; check ₹250 INR",
 approach=["<code>equals</code> compares both <code>paise</code> and <code>currency</code>.",
           "<code>contains</code> walks the list and calls <code>equals</code> on each element until one matches.",
           "<code>hashCode</code> is still overridden, as the contract requires, even though a list doesn't use it."],
 code='''import java.util.ArrayList;
import java.util.Objects;

class Money {
    long paise;
    String currency;

    Money(long paise, String currency) {
        this.paise = paise;
        this.currency = currency;
    }

    @Override
    public boolean equals(Object o) {
        if (!(o instanceof Money)) return false;
        Money m = (Money) o;
        return paise == m.paise && currency.equals(m.currency);
    }

    @Override
    public int hashCode() {
        return Objects.hash(paise, currency);
    }
}

public class Main {
    public static void main(String[] args) {
        ArrayList<Money> pending = new ArrayList<>();
        pending.add(new Money(25000, "INR"));
        pending.add(new Money(500, "USD"));
        boolean dup = pending.contains(new Money(25000, "INR"));
        System.out.println("Already pending: " + dup);
    }
}
''', notes={(31, 2): "contains() calls you :: = <code>ArrayList.contains</code> calls your <code>equals()</code> on the Money being searched (#7), with <code>o</code> = the first element #3. A list never uses hashCode.",
            15: "Check :: <code>o</code> is a Money.", 16: "Cast :: ",
            17: "Compare :: = 25000 == 25000 and \"INR\" equals \"INR\": true. <code>contains</code> stops at the first match.",
            (31, 3): "Result :: ", 32: "Print :: "},
 tryit="Press <b>Run</b>. Then search for <code>new Money(25000, \"USD\")</code>: same number, different currency."),
]

# ---------------- Practice problems ----------------
PRACTICE_INTRO = "Override the three methods correctly and see collections behave. The last three are business tasks."
PROBLEMS = [
dict(level="easy", title="toString for a Product", stmt="<p>Give <code>Product</code> a <code>toString()</code> that prints <code>Pen (₹10)</code>.</p>", inp='Product("Pen", 10)',
 code='''class Product {
    String name;
    int price;
    Product(String name, int price) { this.name = name; this.price = price; }

    @Override
    public String toString() {
        return name + " (₹" + price + ")";
    }
}

public class Main {
    public static void main(String[] args) {
        System.out.println(new Product("Pen", 10));
    }
}''', explain="<p><b>How it works:</b> <code>println(Object)</code> calls <code>toString()</code>; our override replaces the default <code>Product@…</code>.</p>"),
dict(level="easy", title="Every class is an Object", stmt="<p>Store a String, an Integer and an int array in <code>Object</code> variables and print each one's class name with <code>getClass().getSimpleName()</code>.</p>", inp='"UPI", 42, new int[3]',
 code='''public class Main {
    public static void main(String[] args) {
        Object[] things = {"UPI", 42, new int[3]};
        for (Object o : things) {
            System.out.println(o.getClass().getSimpleName());
        }
    }
}''', explain="<p><b>How it works:</b> every object, even an array, is an <code>Object</code>. <code>getClass()</code> reports the real run-time class.</p>"),
dict(level="easy", title="Hash collision", stmt="<p>Show that two different Strings can have the same hash code: print the hash codes of <code>\"Aa\"</code> and <code>\"BB\"</code> and whether they're equal.</p>", inp='"Aa", "BB"',
 code='''public class Main {
    public static void main(String[] args) {
        System.out.println("Aa".hashCode() + " " + "BB".hashCode());
        System.out.println("Aa".equals("BB"));
    }
}''', explain="<p><b>How it works:</b> equal hash codes don't imply equal objects. That's a collision; the contract allows it, and hash tables handle it with equals.</p>"),
dict(level="medium", title="Point equality", stmt="<p>Override <code>equals</code> and <code>hashCode</code> in <code>Point(x, y)</code> so that a <code>HashSet</code> stores <code>(1,2)</code> only once.</p>", inp="(1,2), (1,2), (3,4)",
 code='''import java.util.HashSet;
import java.util.Objects;

class Point {
    final int x, y;
    Point(int x, int y) { this.x = x; this.y = y; }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof Point)) return false;
        Point p = (Point) o;
        return x == p.x && y == p.y;
    }

    @Override
    public int hashCode() { return Objects.hash(x, y); }

    @Override
    public String toString() { return "(" + x + "," + y + ")"; }
}

public class Main {
    public static void main(String[] args) {
        HashSet<Point> pts = new HashSet<>();
        pts.add(new Point(1, 2));
        pts.add(new Point(1, 2));
        pts.add(new Point(3, 4));
        System.out.println(pts.size());
    }
}''', explain="<p><b>How it works:</b> both methods use x and y. Equal points get equal hashes, meet in one bucket, and equals rejects the duplicate.</p>"),
dict(level="medium", title="getClass() vs instanceof", stmt="<p><code>Employee</code> and its subclass <code>Manager</code> share an <code>id</code>. Show how <code>instanceof</code> and <code>getClass()</code> give different answers when comparing an Employee with a Manager.</p>", inp="Employee(7) vs Manager(7)",
 code='''class Employee {
    int id;
    Employee(int id) { this.id = id; }

    boolean equalsByInstanceof(Object o) {
        return o instanceof Employee && ((Employee) o).id == id;
    }

    boolean equalsByClass(Object o) {
        return o != null && getClass() == o.getClass() && ((Employee) o).id == id;
    }
}

class Manager extends Employee {
    Manager(int id) { super(id); }
}

public class Main {
    public static void main(String[] args) {
        Employee e = new Employee(7);
        Manager m = new Manager(7);
        System.out.println(e.equalsByInstanceof(m));
        System.out.println(e.equalsByClass(m));
    }
}''', explain="<p><b>How it works:</b> a Manager <i>is an</i> Employee, so <code>instanceof</code> accepts it. <code>getClass()</code> requires exactly the same class. Pick one rule and use it consistently so equals stays symmetric.</p>"),
dict(level="business", title="De-duplicate customers by PAN", stmt="<p>Three sign-ups arrive: <code>abcde1234f</code>, <code>ABCDE1234F </code> (with a space) and <code>PQRSX9876L</code>. Normalise the PAN in the constructor and count unique customers with a HashSet.</p>", inp='"abcde1234f", "ABCDE1234F ", "PQRSX9876L"',
 code='''import java.util.HashSet;
import java.util.Objects;

class Customer {
    private final String pan;

    Customer(String pan) {
        this.pan = pan.trim().toUpperCase();
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof Customer)) return false;
        return pan.equals(((Customer) o).pan);
    }

    @Override
    public int hashCode() { return Objects.hash(pan); }
}

public class Main {
    public static void main(String[] args) {
        HashSet<Customer> unique = new HashSet<>();
        unique.add(new Customer("abcde1234f"));
        unique.add(new Customer("ABCDE1234F "));
        unique.add(new Customer("PQRSX9876L"));
        System.out.println("Unique customers: " + unique.size());
    }
}''', explain="<p><b>How it works:</b> normalising in the constructor means equal PANs are stored identically, so equals and hashCode agree. The final field also keeps the hash stable.</p>"),
dict(level="business", title="Masked toString for a card", stmt="<p>A <code>Card</code> holds a 16-digit number. Its <code>toString()</code> must show only the last 4 digits, so logs never contain the full number.</p>", inp='"4111222233334421"',
 code='''class Card {
    private final String number;
    private final String holder;

    Card(String number, String holder) {
        this.number = number;
        this.holder = holder;
    }

    @Override
    public String toString() {
        return "Card[" + holder + ", XXXX-XXXX-XXXX-" + number.substring(12) + "]";
    }
}

public class Main {
    public static void main(String[] args) {
        Card c = new Card("4111222233334421", "Riya");
        System.out.println("Payment failed for " + c);
    }
}''', explain="<p><b>How it works:</b> string concatenation calls <code>toString()</code>. Masking there protects every log line that ever prints a Card.</p>"),
dict(level="business", title="Count orders per customer object", stmt="<p>Use <code>Customer</code> objects (equal by phone number) as keys in a <code>HashMap</code> to count orders: Riya orders twice (two separate objects), Kabir once.</p>", inp="Riya 98xxx, Kabir 97xxx, Riya 98xxx",
 code='''import java.util.LinkedHashMap;
import java.util.Map;
import java.util.Objects;

class Customer {
    final String phone, name;
    Customer(String phone, String name) { this.phone = phone; this.name = name; }

    @Override
    public boolean equals(Object o) {
        return o instanceof Customer && phone.equals(((Customer) o).phone);
    }

    @Override
    public int hashCode() { return Objects.hash(phone); }

    @Override
    public String toString() { return name; }
}

public class Main {
    public static void main(String[] args) {
        Map<Customer, Integer> orders = new LinkedHashMap<>();
        Customer[] seen = {
            new Customer("9876500001", "Riya"),
            new Customer("9876500002", "Kabir"),
            new Customer("9876500001", "Riya")
        };
        for (Customer c : seen) {
            orders.put(c, orders.getOrDefault(c, 0) + 1);
        }
        System.out.println(orders);
    }
}''', explain="<p><b>How it works:</b> the third object is a different instance, but equals/hashCode on the phone number make it the same key, so Riya's count becomes 2. <code>toString</code> keeps the printed map readable.</p>"),
]
