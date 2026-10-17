import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../..'))
from mkanim import Anim

ANIM2_HEADING = "Watch it with an example: token numbers at a clinic"
ANIM2_INTRO = "Every patient gets a <code>Token</code> object with its own number, but one <code>static</code> counter at the reception hands out the numbers, so no two patients get the same one."
A = Anim("static int next shared by every Token", frames=5, h=226, label="static counter issuing token numbers")
A.box(6, 14, 140, 90, None, fill="board", stroke="board")
A.text(16, 34, "class Token", size=10.5, bold=True, cls="chalk")
A.text(16, 50, "(one copy)", size=9, cls="chalk")
for f, v in {1: "101", 2: "102", 3: "103", 4: "104", 5: "101"}.items():
    A.text(16, 80, "static next = " + v, on=str(f), mono=True, size=11, cls="kw", bold=True)
pts = [("Asha", "101"), ("Ravi", "102"), ("Meena", "103")]
for i, (n, t) in enumerate(pts):
    y = 14 + i * 62
    with A.g(on=f"{i+2}-"):
        A.box(200, y, 154, 52, None, fill="soft-green", stroke="green")
        A.text(210, y + 20, f"#{i+1} Token", mono=True, size=10, bold=True)
        A.text(210, y + 40, f"patient={n}  number={t}", mono=True, size=9.3)
    A.arrow(148, 70, 198, y + 26, on=str(i + 2), color="track")
A.box(6, 120, 140, 64, None, fill="soft-acc", stroke="track", on="5")
A.text(16, 140, "Token.next = 101;", mono=True, size=9.5, on="5", cls="red", bold=True)
A.text(16, 156, "(a reset by mistake)", size=9, on="5", cls="red")
A.text(16, 172, "next token: 101 again!", size=9, on="5", cls="red")
A.text(180, 214, "1 counter, 3 objects, 3 different numbers", anchor="middle", size=10.5, bold=True, cls="green", on="4")
A.caps([
 "<b>Before anyone arrives:</b> the class has one static field <code>next = 101</code>. No Token object exists yet.",
 "<b>Asha:</b> <code>new Token(\"Asha\")</code> creates object #1. The constructor copies <code>next</code> into the object's own <code>number</code> field, then increments the shared counter to 102.",
 "<b>Ravi:</b> object #2 gets 102; the same counter moves to 103.",
 "<b>Meena:</b> object #3 gets 103. Each token keeps its own number; the counter is shared.",
 "<b>The risk:</b> static state can be changed from anywhere. If some code resets <code>Token.next</code>, numbers repeat. That's why real systems keep counters private and, with many threads, use <code>AtomicInteger</code> (Module 12).",
])
ANIM2 = A

TRACE = dict(code='''class Token {
    static int next = 101;
    int number;

    Token() {
        number = next;
        next++;
    }
}

public class Main {
    public static void main(String[] args) {
        Token a = new Token();
        Token b = new Token();
        System.out.println(a.number + " " + b.number);
        System.out.println("next free: " + Token.next);
    }
}
''', notes={
 (13, 1): "Class init :: ",
 (13, 2): "Create :: Now <code>new Token()</code> runs the constructor for the first object.",
 (6, 1): "Copy :: The object's own field <code>number</code> takes the current shared value.",
 (7, 1): "Shared ++ :: Only the class's single copy of <code>next</code> changes.",
 (13, 3): "Store :: ",
 (14, 1): "Create :: A second object. The class is already initialised, so <code>next</code> is <b>not</b> reset to 101.",
 (6, 2): "Copy :: The second object gets 102.",
 (7, 2): "Shared ++ :: ",
 (14, 2): "Store :: ",
 15: "Print :: Each object kept its own number.",
 16: "Print :: Read the static field through the class name."}, end='main returns. There were two Token objects but only ever one <code>next</code>.')

WORKED_INTRO = "Three common, correct uses of static: a utility method, a constant with a counter, and a shared setting. In each trace, static fields appear at the top of the heap list."
EXAMPLES = [
dict(tag="Retail · GST", title="A static GST helper",
 problem="<p>A billing system needs GST for many prices. The calculation depends only on the price and the rate, not on any object, so write it as a static method in a utility class <code>Gst</code> and call it for two items.</p>",
 inp="price 1200 at 18%, price 450 at 5%",
 approach=["Put the logic in <code>static int amount(int price, int rate)</code>.", "Call it through the class name: <code>Gst.amount(…)</code>.", "No <code>Gst</code> object is ever created."],
 code='''class Gst {
    static int amount(int price, int rate) {
        return price * rate / 100;
    }
}

public class Main {
    public static void main(String[] args) {
        int phone = Gst.amount(1200, 18);
        int book = Gst.amount(450, 5);
        System.out.println("GST on cover: Rs " + phone);
        System.out.println("GST on book: Rs " + book);
    }
}
''', notes={(9, 1): "Call :: A static method is called on the class. Note that the frame has no <code>this</code>.",
 3: "Compute :: Only the parameters are needed.", (9, 2): "Store :: ", (10, 1): "Call :: ", (10, 2): "Store :: ", 11: "Print :: ", 12: "Print :: "},
 tryit="Press <b>Run</b>. Then try <code>new Gst().amount(100, 18)</code>: it compiles, but why is the class name better?"),
dict(tag="Travel · bookings", title="Booking IDs with a fixed prefix",
 problem="<p>Each booking gets an ID like <code>MP-1001</code>. The prefix is a constant for the whole class and the number comes from a shared counter. Create three bookings and print their IDs.</p>",
 inp="passengers Asha, Ravi, Meena",
 approach=["<code>static final String PREFIX = \"MP-\"</code> is a constant (final statics aren't shown in the trace: they never change).", "<code>static int counter = 1000</code> is shared and incremented in the constructor.", "Each object stores its own <code>id</code> String."],
 code='''class Booking {
    static final String PREFIX = "MP-";
    static int counter = 1000;
    String id;
    String passenger;

    Booking(String passenger) {
        counter++;
        this.id = PREFIX + counter;
        this.passenger = passenger;
    }
}

public class Main {
    public static void main(String[] args) {
        Booking b1 = new Booking("Asha");
        Booking b2 = new Booking("Ravi");
        System.out.println(b1.id + " " + b1.passenger);
        System.out.println(b2.id + " " + b2.passenger);
        System.out.println("Bookings made: " + (Booking.counter - 1000));
    }
}
''', notes={(16, 1): "Class init :: ", (16, 2): "Create :: The constructor runs for the first booking.",
 (8, 1): "Shared ++ :: ", (9, 1): "ID :: The constant prefix plus the new counter value.",
 (16, 3): "Store :: ", (17, 1): "Create :: ", (8, 2): "Shared ++ :: The same counter, now 1002.", (17, 2): "Store :: ",
 18: "Print :: ", 19: "Print :: ", 20: "Print :: "},
 tryit="Press <b>Run</b>. Then add a third booking and check the last line."),
dict(tag="Banking · settings", title="Changing a shared minimum balance",
 problem="<p>A bank's minimum balance applies to every account. Accounts below it pay a fee. Store the minimum as a static field, check two accounts, change the rule once, and check again.</p>",
 inp="minimum 1000, then 3000; balances 2500 and 800",
 approach=["<code>static int minBalance</code> is shared by all accounts.", "An instance method compares this account's balance with the shared minimum.", "<code>Account.minBalance = 3000</code> changes the rule for everyone at once."],
 code='''class Account {
    static int minBalance = 1000;
    int balance;

    Account(int balance) {
        this.balance = balance;
    }

    boolean paysFee() {
        return balance < minBalance;
    }
}

public class Main {
    public static void main(String[] args) {
        Account a = new Account(2500);
        Account b = new Account(800);
        System.out.println("a pays fee: " + a.paysFee() + ", b pays fee: " + b.paysFee());
        Account.minBalance = 3000;
        System.out.println("a pays fee: " + a.paysFee() + ", b pays fee: " + b.paysFee());
    }
}
''', notes={(16, 1): "Class init :: ", (16, 2): "Create :: ", (17, 1): "Create :: ", (10, 1): "Check :: 2500 &lt; 1000? false.", (10, 2): "Check :: 800 &lt; 1000? true.",
 18: "Print :: ", 19: "Rule change :: One assignment changes the rule for every account.",
 (10, 3): "Check :: 2500 &lt; 3000? Now true.", (10, 4): "Check :: ", 20: "Print :: "},
 tryit="Press <b>Run</b>. Then remove <code>static</code> from minBalance: what does the compiler say about <code>Account.minBalance</code>?"),
]

PRACTICE_INTRO = "Decide what should be static and what shouldn't, and practise static methods, blocks and counters. The last three are real business tasks."
PROBLEMS = [
dict(level="easy", title="Count objects created", stmt="<p>Write a class <code>Student</code> with a static counter that increases in the constructor. Create three students and print the count.</p>", inp="Riya, Kabir, Asha",
 code='''class Student {
    static int count = 0;
    String name;

    Student(String name) {
        this.name = name;
        count++;
    }
}

public class Main {
    public static void main(String[] args) {
        new Student("Riya");
        new Student("Kabir");
        new Student("Asha");
        System.out.println("Students: " + Student.count);
    }
}''', explain="<p><b>How it works:</b> each constructor call increments the same field. The objects aren't even stored in variables, yet the count is right.</p>"),
dict(level="easy", title="A static utility method", stmt="<p>Write <code>MathUtil.isEven(int n)</code> and <code>MathUtil.square(int n)</code> as static methods and call them without creating an object.</p>", inp="isEven(7), square(12)",
 code='''class MathUtil {
    static boolean isEven(int n) {
        return n % 2 == 0;
    }

    static int square(int n) {
        return n * n;
    }
}

public class Main {
    public static void main(String[] args) {
        System.out.println(MathUtil.isEven(7));
        System.out.println(MathUtil.square(12));
    }
}''', explain="<p><b>How it works:</b> these methods use only their parameters, so there is no reason to require an object. That's the pattern of <code>Math</code>, <code>Arrays</code> and <code>Collections</code>.</p>"),
dict(level="easy", title="Fix the static context error", stmt="<p>This doesn't compile: <code>main</code> uses the instance field <code>shop</code> directly. Fix it by creating an object.</p>", inp="shop = \"Chai Point\"",
 code='''public class Main {
    String shop = "Chai Point";

    void welcome() {
        System.out.println("Welcome to " + shop);
    }

    public static void main(String[] args) {
        Main m = new Main();
        System.out.println(m.shop);
        m.welcome();
    }
}''', explain="<p><b>How it works:</b> instance members need an object. Inside the static <code>main</code> we create one and use it through the reference <code>m</code>.</p>"),
dict(level="medium", title="Static block for a lookup table", stmt="<p>Fill a static array of state codes in a static block, then look up a code by index.</p>", inp="codes: MH, KA, TN, DL; look up index 2",
 code='''class States {
    static String[] codes = new String[4];

    static {
        codes[0] = "MH";
        codes[1] = "KA";
        codes[2] = "TN";
        codes[3] = "DL";
        System.out.println("State table ready");
    }

    static String at(int i) {
        return codes[i];
    }
}

public class Main {
    public static void main(String[] args) {
        System.out.println("Looking up...");
        System.out.println(States.at(2));
        System.out.println(States.at(0));
    }
}''', explain="<p><b>How it works:</b> the static block runs once, when <code>States</code> is first used, which is after “Looking up...” has printed. The second lookup does not run it again.</p>"),
dict(level="medium", title="Instance or static? Mixed counters", stmt="<p>A video has its own view count, and the platform has a total view count across all videos. Model both and play two videos a few times.</p>", inp="video A played 3 times, video B played 2 times",
 code='''class Video {
    static int totalViews = 0;
    String title;
    int views = 0;

    Video(String title) {
        this.title = title;
    }

    void play() {
        views++;
        totalViews++;
    }
}

public class Main {
    public static void main(String[] args) {
        Video a = new Video("Java in 10 min");
        Video b = new Video("UPI explained");
        a.play(); a.play(); a.play();
        b.play(); b.play();
        System.out.println(a.title + ": " + a.views);
        System.out.println(b.title + ": " + b.views);
        System.out.println("Platform total: " + Video.totalViews);
    }
}''', explain="<p><b>How it works:</b> one <code>play()</code> updates both: the video's own counter and the class-wide total. Asking “does this differ per object?” decides static or not.</p>"),
dict(level="business", title="Currency converter with a shared rate", stmt="<p>A travel app converts rupees to dollars. The exchange rate is the same for every conversion and changes during the day. Write a static rate and a static <code>toUsd</code> method, convert, update the rate, convert again.</p>", inp="rate 83.0 then 83.5; convert Rs 8300 and Rs 16700",
 code='''class Fx {
    static double inrPerUsd = 83.0;

    static double toUsd(double inr) {
        return Math.round(inr / inrPerUsd * 100) / 100.0;
    }
}

public class Main {
    public static void main(String[] args) {
        System.out.println("$" + Fx.toUsd(8300));
        System.out.println("$" + Fx.toUsd(16700));
        Fx.inrPerUsd = 83.5;
        System.out.println("$" + Fx.toUsd(8300));
    }
}''', explain="<p><b>How it works:</b> the rate is shared by every conversion, so it's static, and the method uses nothing else. Rounding to cents uses the trick from Lesson 2.4. (Real apps fetch the rate from a service and keep it in a config object.)</p>"),
dict(level="business", title="Seat limit for an event", stmt="<p>An event has 3 seats. A static counter tracks seats booked across all <code>Ticket</code> objects; booking fails once the limit is reached.</p>", inp="booking requests: Asha, Ravi, Meena, Kabir",
 code='''class Ticket {
    static final int CAPACITY = 3;
    static int booked = 0;

    static boolean book(String name) {
        if (booked >= CAPACITY) {
            System.out.println(name + ": sold out");
            return false;
        }
        booked++;
        System.out.println(name + ": seat " + booked);
        return true;
    }
}

public class Main {
    public static void main(String[] args) {
        String[] people = {"Asha", "Ravi", "Meena", "Kabir"};
        for (String p : people) {
            Ticket.book(p);
        }
        System.out.println("Booked " + Ticket.booked + " of " + Ticket.CAPACITY);
    }
}''', explain="<p><b>How it works:</b> the capacity is a constant and the booked count is shared state. Both belong to the event, not to one ticket. (With many simultaneous users, the check-and-increment must be synchronized, Lesson 12.4.)</p>"),
dict(level="business", title="Unique invoice numbers per financial year", stmt="<p>Invoices are numbered like <code>FY25-0001</code>. Use a static constant for the year prefix and a static counter, and format the number with 4 digits.</p>", inp="three invoices",
 code='''class Invoice {
    static final String FY = "FY25";
    static int last = 0;
    String no;

    Invoice() {
        last++;
        no = FY + "-" + String.format("%04d", last);
    }
}

public class Main {
    public static void main(String[] args) {
        for (int i = 0; i < 3; i++) {
            System.out.println(new Invoice().no);
        }
    }
}''', explain="<p><b>How it works:</b> <code>%04d</code> pads the number to 4 digits with zeros (Lesson 5.6's <code>String.format</code>). The counter is shared, so numbers never repeat within a run; a real system would store the last number in a database.</p>"),
]
