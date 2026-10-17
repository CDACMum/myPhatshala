import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from mkanim import Anim, two_view
from m13 import code, snippet, runner, quiz

def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

# ---------------- Part 5: two-view animation ----------------
S = Anim("see", frames=6, h=250, label="A Customer object is serialized to bytes in a file and later deserialized into a new, equal object; the transient OTP is not saved")
S.box(8, 8, 344, 36, None, fill="board", stroke="board")
codes = {1: 'Customer c = new Customer("Asha", 120);', 2: 'out.writeObject(c);   // ObjectOutputStream',
         3: '// customer.ser on disk', 4: '// the program ends: c is gone',
         5: 'Customer back = (Customer) in.readObject();', 6: 'back == c ?   // false: a new object'}
for f, c in codes.items():
    S.text(16, 31, esc(c), on=str(f), mono=True, size=9.2, cls="chalk")
S.box(10, 60, 150, 96, None, fill="soft-green", stroke="green", on="1-3")
S.text(20, 78, "Customer c", size=9.5, bold=True, cls="green", on="1-3")
for i, t in enumerate(["name   \"Asha\"", "points 120", "otp    \"4821\" (transient)"]):
    S.text(20, 100 + i * 18, t, size=9, mono=True, on="1-3", cls="red" if i == 2 else "ink")
S.text(20, 110, "(object gone)", size=10, cls="ink3", on="4")
S.box(186, 60, 166, 96, None, fill="soft-acc", stroke="track", on="2-")
S.text(196, 78, "customer.ser (bytes)", size=9.2, bold=True, cls="acc", on="2-")
S.text(196, 100, "AC ED 00 05 73 72 …", size=9, mono=True, on="2-")
S.text(196, 118, "class name, fields:", size=8.8, cls="ink2", on="2-")
S.text(196, 136, "\"Asha\", 120 (no otp)", size=8.8, mono=True, on="2-")
S.arrow(160, 108, 184, 108, on="2", color="track")
S.box(10, 166, 150, 60, None, fill="soft-blue", stroke="blue", on="5-")
S.text(20, 184, "Customer back", size=9.5, bold=True, cls="blue", on="5-")
S.text(20, 202, "\"Asha\", 120", size=9, mono=True, on="5-")
S.text(20, 218, "otp = null", size=9, mono=True, cls="red", on="5-")
S.arrow(268, 156, 162, 190, on="5", color="blue")
S.text(186, 196, "a new object with the", size=9.5, cls="ink2", on="6")
S.text(186, 212, "same state; not c itself", size=9.5, cls="ink2", on="6")
S.note({1: "An object in memory.", 2: "Serialize: object → bytes.", 3: "Bytes saved in a file.",
        4: "Program ends; memory is gone.", 5: "Deserialize: bytes → object.", 6: "Same data, new object."}, y=240, size=10.5)
S.caps(["A <code>Customer</code> object lives on the heap with a name, loyalty points and a one-time password. Objects disappear when the program ends.",
        "<code>ObjectOutputStream.writeObject(c)</code> <b>serializes</b> it: turns the object's state into a sequence of bytes.",
        "The bytes go into customer.ser. They start with the magic number AC ED, then the class name and field values. The OTP field is <code>transient</code>, so it's skipped.",
        "The program can now end. Only the file remains.",
        "Later (even in another program), <code>ObjectInputStream.readObject()</code> <b>deserializes</b> the bytes into a brand-new Customer. No constructor of Customer runs.",
        "The new object has the saved name and points; the transient OTP comes back as its default value, <code>null</code>. It is a different object from the original: <code>back == c</code> would be false."])

B = Anim("behind", frames=6, h=250, label="Serialization walks the object graph: a Customer referencing an Address that is shared by two fields is written once and restored as one object")
B.box(6, 6, 170, 200, None, fill="soft-blue", stroke="blue")
B.text(16, 24, "HEAP (before)", size=10, bold=True, cls="blue")
B.box(16, 34, 150, 70, None, fill="card", stroke="line")
B.text(24, 52, "#1 Customer", size=9.5, bold=True, mono=True)
B.text(24, 70, "home → #2", size=9, mono=True)
B.text(24, 88, "work → #2", size=9, mono=True)
B.box(16, 130, 150, 44, None, fill="card", stroke="line")
B.text(24, 148, "#2 Address", size=9.5, bold=True, mono=True)
B.text(24, 164, "city \"Pune\"", size=9, mono=True)
B.arrow(90, 104, 90, 128, color="ink")
B.box(186, 6, 168, 200, None, fill="card2", stroke="line")
B.text(196, 24, "stream / file", size=10, bold=True, cls="ink2")
steps = [(2, "Customer: class + fields"), (3, "Address #2: \"Pune\""), (4, "home again: handle → #2"), (5, "read back…")]
for f, t in steps[:3]:
    B.text(196, 48 + (f - 2) * 20, t, size=8.8, mono=True, on=f"{f}-")
B.box(16, 34, 150, 70, None, fill="none", stroke="red", on="2", sw=2.2)
B.box(16, 130, 150, 44, None, fill="none", stroke="red", on="3", sw=2.2)
B.box(196, 116, 150, 80, None, fill="soft-green", stroke="green", on="5-")
B.text(204, 134, "HEAP (after read)", size=9, bold=True, cls="green", on="5-")
B.text(204, 152, "#3 Customer", size=9, mono=True, on="5-")
B.text(204, 168, "home, work → #4", size=9, mono=True, on="5-")
B.text(204, 186, "#4 Address \"Pune\"", size=9, mono=True, on="5-")
B.text(16, 196, "static fields: not saved", size=8.8, cls="ink3", on="6")
B.note({1: "An object graph.", 2: "Write the Customer.", 3: "Follow its reference: Address.", 4: "Seen before: just a handle.",
        5: "Read: new objects, same shape.", 6: "Shared stays shared."}, y=236, size=10.5)
B.caps(["Objects usually point to other objects. Here both <code>home</code> and <code>work</code> refer to the same Address #2.",
        "<code>writeObject</code> writes the Customer's class description and its non-transient, non-static fields.",
        "A reference field means the referenced object must be written too, so it follows <code>home</code> to Address #2. Every object reached this way must be <code>Serializable</code>.",
        "<code>work</code> points to an object already written, so only a short back-reference (a <b>handle</b>) is stored. Each object is written once.",
        "<code>readObject</code> recreates the whole graph as new objects: Customer #3 and Address #4.",
        "Because of the handle, both fields of #3 point to the same #4, just as before. Static fields belong to the class, not the object, so they are never part of the bytes."])
ANIM = two_view("Serialization, both views", S, B)

# ---------------- Part 6: animated example ----------------
ANIM2_HEADING = "Watch it with an example: a shopping cart that survives an app restart"
ANIM2_INTRO = "A shopping app saves the customer's cart when the app is closed and restores it when it opens again."
A = Anim("Save the cart, restore the cart", frames=5, h=230, label="A Cart object is serialized when the app closes and deserialized when it starts again")
A.box(10, 14, 150, 110, None, fill="soft-green", stroke="green", on="1-2")
A.text(20, 32, "Cart (in memory)", size=9.5, bold=True, cls="green", on="1-2")
for i, t in enumerate(["phone cover  Rs 299", "charger      Rs 799", "earphones    Rs 1499"]):
    A.text(20, 56 + i * 20, t, size=9, mono=True, on="1-2")
A.text(20, 70, "app closed", size=11, bold=True, cls="ink3", on="3")
A.box(196, 40, 156, 50, None, fill="soft-acc", stroke="track", on="2-")
A.text(206, 60, "cart.ser", size=10, bold=True, mono=True, cls="acc", on="2-")
A.text(206, 78, "412 bytes", size=9, cls="ink3", on="2-")
A.arrow(160, 64, 194, 64, on="2", color="track")
A.box(10, 118, 150, 70, None, fill="soft-blue", stroke="blue", on="4-")
A.text(20, 136, "Cart (restored)", size=9.5, bold=True, cls="blue", on="4-")
A.text(20, 156, "3 items, Rs 2597", size=9.5, mono=True, on="4-")
A.text(20, 176, "coupon: re-checked", size=9, cls="ink2", on="5")
A.arrow(270, 90, 162, 140, on="4", color="blue")
A.note({1: "Cart with 3 items.", 2: "App closing: writeObject.", 3: "App closed.", 4: "App opens: readObject.", 5: "Restored and validated."}, y=206, size=10.5)
A.caps(["While shopping, the cart is an object with a list of items.",
        "When the app closes, it writes the cart with <code>writeObject</code> to cart.ser in the app's private storage. (Illustrative size.)",
        "The app process ends; only the file remains.",
        "Next launch, <code>readObject</code> rebuilds the cart: same items, same prices as when it was saved.",
        "Saved prices may be old, so the app re-checks prices and coupons with the server. Many real apps save such state as JSON instead of Java serialization, for reasons you'll see in Part 3."])
ANIM2 = A

# ---------------- Part 8: tracer ----------------
TRACE = dict(code='''import java.io.*;

class Customer implements Serializable {
    private static final long serialVersionUID = 1L;
    String name;
    int points;
    transient String otp;

    Customer(String name, int points, String otp) {
        this.name = name;
        this.points = points;
        this.otp = otp;
    }
}

public class Main {
    public static void main(String[] args) throws IOException, ClassNotFoundException {
        Customer c = new Customer("Asha", 120, "4821");
        try (ObjectOutputStream out = new ObjectOutputStream(new FileOutputStream("customer.ser"))) {
            out.writeObject(c);
        }
        Customer back;
        try (ObjectInputStream in = new ObjectInputStream(new FileInputStream("customer.ser"))) {
            back = (Customer) in.readObject();
        }
        System.out.println(back.name + ", " + back.points + " points, otp=" + back.otp + ", same object? " + (back == c));
    }
}
''', notes={
 18: "Original :: = A Customer object (#n) with name, points and a transient OTP.",
 19: "Output :: = An ObjectOutputStream over a FileOutputStream. It immediately writes the stream header (AC ED 00 05).",
 20: "Serialize :: = The class description and the fields name and points are written. otp is transient, so it's skipped.",
 21: "Closed :: = The file is complete.",
 23: "Input :: = An ObjectInputStream reads and checks the header.",
 24: "Deserialize :: = <code>readObject</code> creates a brand-new Customer without calling its constructor and fills in the saved fields. It returns Object, so we cast.",
 26: "Compare :: Same name and points; otp is null; and it's a different object from <code>c</code>."})

# ---------------- Worked examples ----------------
WORKED_INTRO = "Three cases you'll meet: saving game progress, protecting a secret with <code>transient</code>, and saving a whole list of objects in one call. Watch new objects appear on the heap when they are read back."
EXAMPLES = [
dict(tag="Gaming · progress", title="Save and load game progress",
 problem="<p>A quiz game must save the player's progress (name, level, score, list of badges) when they quit and restore it next time. Make the class serializable, save it, load it, and show the restored progress.</p>",
 inp="Ravi, level 7, score 4350, badges: Speed, Streak",
 approach=["<code>Progress implements Serializable</code>, with a <code>serialVersionUID</code>.",
           "Fields include an <code>ArrayList&lt;String&gt;</code>, which is itself serializable.",
           "Write with ObjectOutputStream, read with ObjectInputStream, cast the result."],
 code='''import java.io.*;
import java.util.*;

class Progress implements Serializable {
    private static final long serialVersionUID = 1L;
    String player;
    int level;
    int score;
    List<String> badges = new ArrayList<>();
}

public class Main {
    public static void main(String[] args) throws IOException, ClassNotFoundException {
        Progress p = new Progress();
        p.player = "Ravi";
        p.level = 7;
        p.score = 4350;
        p.badges.add("Speed");
        p.badges.add("Streak");
        try (ObjectOutputStream out = new ObjectOutputStream(new FileOutputStream("save.dat"))) {
            out.writeObject(p);
        }
        Progress loaded;
        try (ObjectInputStream in = new ObjectInputStream(new FileInputStream("save.dat"))) {
            loaded = (Progress) in.readObject();
        }
        System.out.println(loaded.player + " is on level " + loaded.level + " with " + loaded.score + " points");
        System.out.println("badges: " + loaded.badges);
    }
}
''', notes={14: "Progress :: = A Progress object with an empty badges list.",
            19: "Badges :: The list now holds two strings.",
            21: "Save :: = The Progress object, its ArrayList and both Strings are written: the whole graph.",
            25: "Load :: = A new Progress, a new ArrayList and new Strings are created from the bytes.",
            27: "Restored :: Ravi, level 7, 4350 points.",
            28: "List too :: The badges list came back with both items."},
 tryit="Press <b>Run</b>. Then add a field <code>transient int livesLeft = 3;</code> and print it after loading: it comes back as 0."),
dict(tag="Banking · security", title="Never save the PIN: transient",
 problem="<p>A banking app caches a <code>Session</code> object to disk so a user doesn't have to re-select their account. The session holds the account number, the last screen and the user's PIN. The PIN must never be written to disk.</p>",
 inp="account XX4521, screen statements, PIN 7391",
 approach=["Mark <code>pin</code> as <code>transient</code>.",
           "Serialize, then look inside the raw bytes for the PIN text to prove it's absent.",
           "Deserialize and show the PIN came back as null."],
 code='''import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;

class Session implements Serializable {
    private static final long serialVersionUID = 1L;
    String account = "XX4521";
    String lastScreen = "statements";
    transient String pin = "7391";
}

public class Main {
    public static void main(String[] args) throws IOException, ClassNotFoundException {
        try (ObjectOutputStream out = new ObjectOutputStream(new FileOutputStream("session.ser"))) {
            out.writeObject(new Session());
        }
        String raw = new String(Files.readAllBytes(Path.of("session.ser")), StandardCharsets.ISO_8859_1);
        System.out.println("file mentions account? " + raw.contains("XX4521"));
        System.out.println("file mentions PIN?     " + raw.contains("7391"));
        Session s;
        try (ObjectInputStream in = new ObjectInputStream(new FileInputStream("session.ser"))) {
            s = (Session) in.readObject();
        }
        System.out.println("restored: " + s.account + ", " + s.lastScreen + ", pin=" + s.pin);
    }
}
''', notes={14: "Stream :: = An ObjectOutputStream on session.ser.",
            15: "Write :: = A new Session is serialized: account and lastScreen are written, pin is skipped.",
            17: "Inspect :: = The raw bytes are read as Latin-1 text so we can search them.",
            18: "Account :: The account string is visible in the file: serialized data is not encrypted.",
            19: "PIN :: The PIN does not appear anywhere.",
            22: "Read :: = A new Session is built from the bytes. Field initializers don't run either, so pin stays null.",
            24: "Result :: pin=null."},
 tryit="Press <b>Run</b>. Then remove <code>transient</code> and run again: the PIN is now readable inside the file. That's why secrets must never be serialized."),
dict(tag="E-commerce · catalogue", title="Save a whole product list in one call",
 problem="<p>A shop caches its product catalogue (a list of Product objects) to a file so it can start quickly without waiting for the server. Save the list with one <code>writeObject</code> call, reload it, and print the cheapest product.</p>",
 inp="Rice 5kg Rs 450, Oil 1L Rs 165, Sugar 1kg Rs 48",
 approach=["<code>Product implements Serializable</code>.",
           "<code>ArrayList</code> is serializable, so writing the list writes every product in it.",
           "Read it back and cast to <code>List&lt;Product&gt;</code> (an unchecked cast, so add <code>@SuppressWarnings</code>)."],
 code='''import java.io.*;
import java.util.*;

class Product implements Serializable {
    private static final long serialVersionUID = 1L;
    String name;
    int price;

    Product(String name, int price) {
        this.name = name;
        this.price = price;
    }
}

public class Main {
    @SuppressWarnings("unchecked")
    public static void main(String[] args) throws IOException, ClassNotFoundException {
        List<Product> catalogue = new ArrayList<>();
        catalogue.add(new Product("Rice 5kg", 450));
        catalogue.add(new Product("Oil 1L", 165));
        catalogue.add(new Product("Sugar 1kg", 48));
        try (ObjectOutputStream out = new ObjectOutputStream(new FileOutputStream("catalogue.ser"))) {
            out.writeObject(catalogue);
        }
        List<Product> cached;
        try (ObjectInputStream in = new ObjectInputStream(new FileInputStream("catalogue.ser"))) {
            cached = (List<Product>) in.readObject();
        }
        Product cheapest = cached.get(0);
        for (Product p : cached) if (p.price < cheapest.price) cheapest = p;
        System.out.println(cached.size() + " products loaded; cheapest: " + cheapest.name + " Rs " + cheapest.price);
    }
}
''', notes={18: "List :: = An empty ArrayList.",
            21: "Filled :: Three Product objects in the list.",
            23: "One call :: = Writing the list writes its size and then each Product: the whole graph.",
            27: "Read :: = A new list with three new Products.",
            29: "Search :: Start with the first product as the cheapest so far.",
            30: "Loop :: Compare each product's price.",
            31: "Result :: 3 products; Sugar 1kg is cheapest."},
 tryit="Press <b>Run</b>. Then remove <code>implements Serializable</code> from Product: writing fails with <code>NotSerializableException: Product</code>, because every object in the graph must be serializable."),
]

# ---------------- Practice problems ----------------
PRACTICE_INTRO = "Serialize objects, control what's saved with <code>transient</code>, and handle the exceptions. Each program writes and reads its own file. The last three are business tasks."
PROBLEMS = [
dict(level="easy", title="Save and load one object", stmt="<p>Make a serializable <code>Book</code> (title, price). Save one and load it back.</p>", inp="Java Basics, 399",
 code='''import java.io.*;

class Book implements Serializable {
    private static final long serialVersionUID = 1L;
    String title;
    int price;
}

public class Main {
    public static void main(String[] args) throws Exception {
        Book b = new Book();
        b.title = "Java Basics";
        b.price = 399;
        try (ObjectOutputStream out = new ObjectOutputStream(new FileOutputStream("book.ser"))) {
            out.writeObject(b);
        }
        try (ObjectInputStream in = new ObjectInputStream(new FileInputStream("book.ser"))) {
            Book copy = (Book) in.readObject();
            System.out.println(copy.title + " Rs " + copy.price);
        }
    }
}''', explain="<p><b>How it works:</b> <code>Serializable</code> is a marker interface: no methods, it just gives permission. <code>readObject</code> returns Object, so cast it.</p>"),
dict(level="easy", title="transient fields come back empty", stmt="<p>Serialize a <code>Login</code> with a username and a transient password and print both after loading.</p>", inp="asha / secret123",
 code='''import java.io.*;

class Login implements Serializable {
    private static final long serialVersionUID = 1L;
    String user = "asha";
    transient String password = "secret123";
}

public class Main {
    public static void main(String[] args) throws Exception {
        try (ObjectOutputStream out = new ObjectOutputStream(new FileOutputStream("login.ser"))) {
            out.writeObject(new Login());
        }
        try (ObjectInputStream in = new ObjectInputStream(new FileInputStream("login.ser"))) {
            Login l = (Login) in.readObject();
            System.out.println("user=" + l.user + ", password=" + l.password);
        }
    }
}''', explain="<p><b>How it works:</b> transient fields get default values after deserialization (null, 0, false). Initializers like <code>= \"secret123\"</code> don't run for a deserialized object.</p>"),
dict(level="easy", title="The magic number", stmt="<p>Serialize a String and print the first four bytes of the file in hex.</p>", inp="\"hello\"",
 code='''import java.io.*;
import java.nio.file.*;

public class Main {
    public static void main(String[] args) throws IOException {
        try (ObjectOutputStream out = new ObjectOutputStream(new FileOutputStream("s.ser"))) {
            out.writeObject("hello");
        }
        byte[] b = Files.readAllBytes(Path.of("s.ser"));
        System.out.printf("%02X %02X %02X %02X (%d bytes)%n", b[0], b[1], b[2], b[3], b.length);
    }
}''', explain="<p><b>How it works:</b> every Java serialization stream starts with the magic number <code>AC ED</code> and version <code>00 05</code>. Security tools look for these bytes in network traffic.</p>"),
dict(level="medium", title="Constructors don't run", stmt="<p>Show that deserialization does not call the class's constructor: count constructor calls in a static counter.</p>", inp="(none)",
 code='''import java.io.*;

class Ticket implements Serializable {
    private static final long serialVersionUID = 1L;
    static int made = 0;
    int seat;
    Ticket(int seat) { this.seat = seat; made++; }
}

public class Main {
    public static void main(String[] args) throws Exception {
        try (ObjectOutputStream out = new ObjectOutputStream(new FileOutputStream("t.ser"))) {
            out.writeObject(new Ticket(14));
        }
        try (ObjectInputStream in = new ObjectInputStream(new FileInputStream("t.ser"))) {
            Ticket t = (Ticket) in.readObject();
            System.out.println("seat " + t.seat + ", constructor calls: " + Ticket.made);
        }
    }
}''', explain="<p><b>How it works:</b> the JVM creates the object without running Ticket's constructor and then fills in the fields from the stream. So any validation in your constructor is skipped; that's one reason deserializing untrusted data is risky.</p>"),
dict(level="medium", title="Static fields aren't saved", stmt="<p>Serialize an object, change a static field, deserialize, and show the static value is the current one, not the saved one.</p>", inp="(none)",
 code='''import java.io.*;

class Config implements Serializable {
    private static final long serialVersionUID = 1L;
    static String theme = "light";
    String user = "meena";
}

public class Main {
    public static void main(String[] args) throws Exception {
        try (ObjectOutputStream out = new ObjectOutputStream(new FileOutputStream("cfg.ser"))) {
            out.writeObject(new Config());
        }
        Config.theme = "dark";
        try (ObjectInputStream in = new ObjectInputStream(new FileInputStream("cfg.ser"))) {
            Config c = (Config) in.readObject();
            System.out.println("user=" + c.user + ", theme=" + Config.theme);
        }
    }
}''', explain="<p><b>How it works:</b> serialization saves an object's state; static fields belong to the class, so they're not part of it.</p>"),
dict(level="medium", title="Catch NotSerializableException", stmt="<p>A serializable <code>Order</code> has a field of a non-serializable type <code>Printer</code>. Catch the exception and print which class caused it.</p>", inp="(none)",
 code='''import java.io.*;

class Printer {
    String model = "TP-80";
}

class Order implements Serializable {
    private static final long serialVersionUID = 1L;
    int id = 501;
    Printer printer = new Printer();
}

public class Main {
    public static void main(String[] args) throws IOException {
        try (ObjectOutputStream out = new ObjectOutputStream(new FileOutputStream("o.ser"))) {
            out.writeObject(new Order());
        } catch (NotSerializableException e) {
            System.out.println("cannot save: " + e.getMessage() + " is not Serializable");
        }
    }
}''', explain="<p><b>How it works:</b> the whole object graph must be serializable. Fix it by making Printer serializable, or by marking the field <code>transient</code> and recreating it after loading.</p>"),
dict(level="business", title="Persist a customer list", stmt="<p>Save three customers (name, city, loyalty points) as one list, reload it, and print the total points.</p>", inp="3 customers",
 code='''import java.io.*;
import java.util.*;

class Customer implements Serializable {
    private static final long serialVersionUID = 1L;
    String name, city;
    int points;
    Customer(String n, String c, int p) { name = n; city = c; points = p; }
}

public class Main {
    @SuppressWarnings("unchecked")
    public static void main(String[] args) throws Exception {
        List<Customer> list = new ArrayList<>(List.of(
            new Customer("Asha", "Pune", 120), new Customer("Ravi", "Nagpur", 300), new Customer("Imran", "Pune", 75)));
        try (ObjectOutputStream out = new ObjectOutputStream(new FileOutputStream("customers.ser"))) {
            out.writeObject(list);
        }
        try (ObjectInputStream in = new ObjectInputStream(new FileInputStream("customers.ser"))) {
            List<Customer> loaded = (List<Customer>) in.readObject();
            int total = 0;
            for (Customer c : loaded) total += c.points;
            System.out.println(loaded.size() + " customers, " + total + " points in total");
        }
    }
}''', explain="<p><b>How it works:</b> collections serialize their elements, so one call saves everything. Remember the cast from Object is unchecked: the file could contain anything.</p>"),
dict(level="business", title="Shared address saved once", stmt="<p>Two employees share one office Address object. Serialize both in one stream and show they still share the same Address after loading.</p>", inp="2 employees, 1 office",
 code='''import java.io.*;

class Address implements Serializable {
    private static final long serialVersionUID = 1L;
    String city = "Mumbai";
}

class Employee implements Serializable {
    private static final long serialVersionUID = 1L;
    String name;
    Address office;
    Employee(String n, Address a) { name = n; office = a; }
}

public class Main {
    public static void main(String[] args) throws Exception {
        Address hq = new Address();
        try (ObjectOutputStream out = new ObjectOutputStream(new FileOutputStream("staff.ser"))) {
            out.writeObject(new Employee("Asha", hq));
            out.writeObject(new Employee("Ravi", hq));
        }
        try (ObjectInputStream in = new ObjectInputStream(new FileInputStream("staff.ser"))) {
            Employee a = (Employee) in.readObject();
            Employee r = (Employee) in.readObject();
            System.out.println("same office object? " + (a.office == r.office) + ", city " + r.office.city);
        }
    }
}''', explain="<p><b>How it works:</b> within one stream, an object that was already written is stored as a back-reference, so sharing is preserved. Objects must be read in the same order they were written.</p>"),
dict(level="business", title="Version check with serialVersionUID", stmt="<p>Print the serialVersionUID that Java uses for a class, so a team can fix it explicitly before shipping.</p>", inp="class Invoice",
 code='''import java.io.*;

class Invoice implements Serializable {
    private static final long serialVersionUID = 2026_10L;
    String number;
    double amount;
}

public class Main {
    public static void main(String[] args) {
        ObjectStreamClass desc = ObjectStreamClass.lookup(Invoice.class);
        System.out.println(desc.getName() + " serialVersionUID = " + desc.getSerialVersionUID());
        System.out.println("fields saved: " + desc.getFields().length);
    }
}''', explain="<p><b>How it works:</b> the UID is stored in every serialized stream. When reading, Java compares it with the current class; if they differ you get <code>InvalidClassException</code>. Declaring it yourself keeps compatible changes (like adding a field) from breaking old files.</p>"),
]

# ---------------- Extra blocks ----------------
BLOCKS = {
'ANIM': ANIM,
'CODE_RULES': snippet('''class Customer implements Serializable {          // 1. opt in (marker interface)
    private static final long serialVersionUID = 1L; // 2. version number of the format
    String name;                                     //    saved
    int points;                                      //    saved
    Address home;                                    // 3. must be Serializable too
    transient String otp;                            // 4. skipped, comes back null
    static int count;                                // 5. class data, never saved
}'''),
'CODE_UID': snippet('''java.io.InvalidClassException: Customer; local class incompatible:
    stream classdesc serialVersionUID = 1, local class serialVersionUID = 2''', lang='text', file='console'),
'CODE_RUN': code('''import java.io.*;

class Customer implements Serializable {
    private static final long serialVersionUID = 1L;
    String name;
    int points;
    transient String otp;

    Customer(String name, int points, String otp) {
        this.name = name;
        this.points = points;
        this.otp = otp;
    }
}

public class Main {
    public static void main(String[] args) throws IOException, ClassNotFoundException {
        Customer c = new Customer("Asha", 120, "4821");
        try (ObjectOutputStream out = new ObjectOutputStream(new FileOutputStream("customer.ser"))) {
            out.writeObject(c);
        }
        System.out.println("saved " + new File("customer.ser").length() + " bytes");
        try (ObjectInputStream in = new ObjectInputStream(new FileInputStream("customer.ser"))) {
            Customer back = (Customer) in.readObject();
            System.out.println(back.name + ", " + back.points + " points, otp=" + back.otp);
            System.out.println("same object? " + (back == c));
        }
    }
}'''),
'RUNNER': runner([
 dict(label="1 · Save and restore a customer", hint="Press <b>Run</b>. Then remove <code>transient</code> from <code>otp</code> and compare the file size and the restored OTP.",
      code='''import java.io.*;

class Customer implements Serializable {
    private static final long serialVersionUID = 1L;
    String name;
    int points;
    transient String otp;

    Customer(String name, int points, String otp) {
        this.name = name;
        this.points = points;
        this.otp = otp;
    }
}

public class Main {
    public static void main(String[] args) throws IOException, ClassNotFoundException {
        Customer c = new Customer("Asha", 120, "4821");
        try (ObjectOutputStream out = new ObjectOutputStream(new FileOutputStream("customer.ser"))) {
            out.writeObject(c);
        }
        System.out.println("saved " + new File("customer.ser").length() + " bytes");
        try (ObjectInputStream in = new ObjectInputStream(new FileInputStream("customer.ser"))) {
            Customer back = (Customer) in.readObject();
            System.out.println(back.name + ", " + back.points + " points, otp=" + back.otp);
        }
    }
}'''),
 dict(label="2 · Predict: does the constructor print?", hint="<b>Predict first:</b> how many times is “constructor called” printed? Deserialization builds the object differently.",
      code='''import java.io.*;

class Pass implements Serializable {
    private static final long serialVersionUID = 1L;
    String holder;
    Pass(String h) {
        holder = h;
        System.out.println("constructor called for " + h);
    }
}

public class Main {
    public static void main(String[] args) throws Exception {
        try (ObjectOutputStream out = new ObjectOutputStream(new FileOutputStream("pass.ser"))) {
            out.writeObject(new Pass("Meena"));
        }
        try (ObjectInputStream in = new ObjectInputStream(new FileInputStream("pass.ser"))) {
            Pass p = (Pass) in.readObject();
            System.out.println("loaded pass for " + p.holder);
        }
    }
}'''),
 dict(label="3 · Predict: two references, one object?", hint="<b>Predict first:</b> after reading, is <code>a == b</code>? Then write the same object twice and read twice.",
      code='''import java.io.*;
import java.util.*;

public class Main {
    @SuppressWarnings("unchecked")
    public static void main(String[] args) throws Exception {
        List<String> shared = new ArrayList<>(List.of("tea", "coffee"));
        List<List<String>> menus = List.of(shared, shared);
        try (ObjectOutputStream out = new ObjectOutputStream(new FileOutputStream("m.ser"))) {
            out.writeObject(new ArrayList<>(menus));
        }
        try (ObjectInputStream in = new ObjectInputStream(new FileInputStream("m.ser"))) {
            List<List<String>> back = (List<List<String>>) in.readObject();
            System.out.println("same inner list? " + (back.get(0) == back.get(1)));
        }
    }
}'''),
 dict(label="4 · Crash: not serializable", hint="<code>Wallet</code> doesn't implement <code>Serializable</code>. Read the exception, then add <code>implements Serializable</code>.",
      code='''import java.io.*;

class Wallet {
    int balance = 500;
}

public class Main {
    public static void main(String[] args) throws IOException {
        try (ObjectOutputStream out = new ObjectOutputStream(new FileOutputStream("w.ser"))) {
            out.writeObject(new Wallet());
        }
        System.out.println("saved");
    }
}''', _expect="exception"),
 dict(label="5 · Spot the error", hint="<code>readObject()</code> returns <code>Object</code>. Cast it: <code>(String) in.readObject()</code>. It also throws <code>ClassNotFoundException</code>, which main must declare.",
      code='''import java.io.*;

public class Main {
    public static void main(String[] args) throws Exception {
        try (ObjectOutputStream out = new ObjectOutputStream(new FileOutputStream("n.ser"))) {
            out.writeObject("Asha");
        }
        try (ObjectInputStream in = new ObjectInputStream(new FileInputStream("n.ser"))) {
            String name = in.readObject();
            System.out.println(name);
        }
    }
}''', _expect="compile-error"),
]),
'QUIZ': quiz([
 {"q": "What is serialization?", "options": ["Sorting objects", "Converting an object's state into a byte stream", "Encrypting a file", "Running threads in order"], "answer": 1, "why": "Deserialization is the reverse: bytes back into an object."},
 {"q": "Serializable has how many methods?", "options": ["0 (it's a marker interface)", "1", "2", "3"], "answer": 0, "why": "It just marks the class as allowed to be serialized."},
 {"q": "A transient field after deserialization holds…", "options": ["its saved value", "its type's default value (null, 0, false)", "a random value", "it throws"], "answer": 1, "why": "transient fields are skipped when writing."},
 {"q": "Are static fields serialized?", "options": ["Yes", "No", "Only if final", "Only primitives"], "answer": 1, "why": "They belong to the class, not to the object's state."},
 {"q": "Writing an object whose field refers to a non-serializable class throws…", "options": ["ClassCastException", "NotSerializableException", "InvalidClassException", "Nothing"], "answer": 1, "why": "Every object in the graph must be serializable (or the field transient)."},
 {"q": "What is serialVersionUID for?", "options": ["Encrypting the stream", "Checking that the class used to read is compatible with the one that wrote", "Counting objects", "Thread safety"], "answer": 1, "why": "A mismatch causes InvalidClassException."},
 {"q": "Does deserialization run the constructor of a Serializable class?", "options": ["Yes, always", "No", "Only the default constructor", "Only if public"], "answer": 1, "why": "The object is created without it (only the first non-serializable superclass's no-arg constructor runs)."},
 {"q": "Why should you never deserialize data from untrusted sources?", "options": ["It's slow", "Crafted byte streams can trigger dangerous code in classes on the classpath", "It's deprecated", "It loses transient fields"], "answer": 1, "why": "Deserialization attacks have caused major security incidents; prefer JSON with validation, or use deserialization filters."},
]),
}
