import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../..'))
from mkanim import Anim

ANIM2_HEADING = "Watch it with an example: a hospital record with layers of access"
ANIM2_INTRO = "A <code>Patient</code> class in package <code>hospital</code>. Different code in the system asks for different parts of it. The compiler lets each one see only what its access level allows."
A = Anim("Who may read a Patient's fields?", frames=6, h=236, label="access levels on a patient record")
A.box(150, 14, 204, 150, None, fill="card", stroke="green")
A.text(160, 32, "class Patient (package hospital)", size=9.5, bold=True, cls="green")
fields = [("public", "String name", "blue"), ("protected", "String ward", "track"), ("default", "int bedNo", "green"), ("private", "String diagnosis", "red")]
for i, (m, f, c) in enumerate(fields):
    y = 40 + i * 30
    A.box(160, y, 184, 24, None, fill="card2", stroke=c)
    A.text(168, y + 16, m, mono=True, size=9.5, bold=True, cls={"blue": "blue", "track": "acc", "green": "green", "red": "red"}[c])
    A.text(232, y + 16, f, mono=True, size=9)
who = {1: ("Visitor kiosk", "other package"), 2: ("NurseStation", "other package, subclass"), 3: ("WardBoard", "same package"), 4: ("Patient itself", "same class"), 5: ("Visitor kiosk", "other package"), 6: ("Doctor app", "uses a public method")}
for f, (n, k) in who.items():
    A.box(6, 50, 130, 50, n, sub=k, on=str(f), fill="soft-blue", stroke="blue", bold=True, size=10)
ok = {1: [0], 2: [0, 1], 3: [0, 1, 2], 4: [0, 1, 2, 3], 5: [0], 6: [3]}
for f, lst in ok.items():
    for i in range(4):
        y = 40 + i * 30
        if i in lst:
            A.text(338, y + 16, "✓", on=str(f), anchor="end", size=12, bold=True, cls="green")
        elif f != 6:
            A.text(338, y + 16, "✗", on=str(f), anchor="end", size=12, bold=True, cls="red")
A.box(6, 120, 130, 40, "p.diagnosis", on="5", fill="soft-acc", stroke="red", mono=True, size=10, cls="red", bold=True)
A.box(6, 120, 130, 40, "p.summaryFor(doc)", on="6", fill="soft-green", stroke="green", mono=True, size=9, bold=True)
notes = {1: "public: everyone can read the name", 2: "protected: + subclasses in other packages", 3: "default: + any class in package hospital",
         4: "private: only Patient's own code", 5: "compile error: diagnosis has private access", 6: "a public method decides what to reveal, and to whom"}
for f, t in notes.items(): A.text(180, 192, t, on=str(f), anchor="middle", size=10.5, bold=True, cls="red" if f == 5 else "ink")
A.text(180, 212, "", size=1)
A.caps([
 "<b>Visitor kiosk</b> (another package, not related): it can use only <code>public</code> members, so it may show the patient's name.",
 "<b>NurseStation</b> is a subclass of Patient in another package: it also gets the <code>protected</code> ward, through inheritance.",
 "<b>WardBoard</b> is in the same package <code>hospital</code>: it gets public, protected and default members, including the bed number.",
 "<b>Patient's own methods</b> can use everything, including the <code>private</code> diagnosis.",
 "<b>The kiosk tries <code>p.diagnosis</code>:</b> javac refuses: <i>diagnosis has private access in Patient</i>. Sensitive data can't leak by accident.",
 "<b>The right way:</b> a public method like <code>summaryFor(doctor)</code>, written inside Patient, checks who is asking and returns only what they may see. The rule lives in one place. (Simplified: real hospital systems also need permission checks at run time.)",
])
ANIM2 = A

TRACE = dict(code='''class Wallet {
    private int balance;

    Wallet(int balance) {
        this.balance = balance;
    }

    public boolean pay(int amount) {
        if (amount > balance) {
            return false;
        }
        balance -= amount;
        return true;
    }

    public int getBalance() {
        return balance;
    }
}

public class Main {
    public static void main(String[] args) {
        Wallet w = new Wallet(500);
        boolean first = w.pay(120);
        boolean second = w.pay(900);
        System.out.println(first + " " + second + " " + w.getBalance());
    }
}
''', notes={
 (23, 1): "Create :: ", 5: "Set :: Inside the class, the private field can be written.",
 (23, 2): "Store :: main holds a reference, but the compiler won't let main touch <code>balance</code> directly.",
 (24, 1): "Call :: The only way to spend: the public method.",
 12: "Change :: Written by Wallet's own code, after the check.",
 (24, 2): "Result :: ", (25, 1): "Call :: ",
 10: "Refuse :: The rule is enforced inside the class: 900 &gt; 380.",
 (25, 2): "Result :: ",
 26: "Print :: The getter reads the private value for main."})

WORKED_INTRO = "Three designs where the right access level does the protecting. Watch the private fields change only inside their own class's methods."
EXAMPLES = [
dict(tag="Banking · PAN", title="Show only the last 4 characters",
 problem="<p>A customer's PAN must never be shown in full on screens. Keep it <code>private</code> and offer only <code>maskedPan()</code>, which returns <code>XXXXXX234F</code>-style text.</p>",
 inp="PAN \"ABCDE1234F\"",
 approach=["Store the PAN in a private final field.", "The public method builds a masked copy; the original never leaves the class.", "main can't read <code>pan</code> even if it wanted to."],
 code='''class Customer {
    private final String pan;

    Customer(String pan) {
        this.pan = pan;
    }

    public String maskedPan() {
        String last4 = pan.substring(pan.length() - 4);
        return "XXXXXX" + last4;
    }
}

public class Main {
    public static void main(String[] args) {
        Customer c = new Customer("ABCDE1234F");
        System.out.println("PAN: " + c.maskedPan());
    }
}
''', notes={(16, 1): "Create :: ", 5: "Set :: ", (16, 2): "Store :: ", (17, 1): "Call :: ", 9: "Mask :: Only Customer's own code reads the full PAN.", 10: "Return :: A new masked String leaves the class, never the original.", 17: "Print :: "},
 tryit="Press <b>Run</b>. Then try <code>System.out.println(c.pan);</code> in main and read the error."),
dict(tag="Education · marks", title="Marks that can only be set within 0–100",
 problem="<p>A results portal stores marks privately. The public setter rejects values outside 0–100, so a typo like 850 can never be saved.</p>",
 inp="set 85, then try 850",
 approach=["<code>private int marks</code>.", "<code>public boolean setMarks(int m)</code> validates before assigning.", "The getter returns the current value."],
 code='''class Result {
    private int marks;

    public boolean setMarks(int m) {
        if (m < 0 || m > 100) {
            return false;
        }
        marks = m;
        return true;
    }

    public int getMarks() {
        return marks;
    }
}

public class Main {
    public static void main(String[] args) {
        Result r = new Result();
        boolean a = r.setMarks(85);
        boolean b = r.setMarks(850);
        System.out.println(a + " " + b + " marks=" + r.getMarks());
    }
}
''', notes={(19, 1): "Create :: The default constructor; marks starts at 0.", (19, 2): "Store :: ", (20, 1): "Call :: ", 8: "Set :: 85 passed the check.", (20, 2): "Result :: ", (21, 1): "Call :: ", 6: "Reject :: 850 is outside 0–100. The field is untouched.", (21, 2): "Result :: ", 22: "Print :: "},
 tryit="Press <b>Run</b>. Then make <code>marks</code> public and set it to 850 directly from main. Nothing stops you: that's the point of private."),
dict(tag="Platform · utilities", title="A utility class nobody can instantiate",
 problem="<p>A <code>Phone</code> utility formats Indian mobile numbers. It has only static methods, so creating objects of it makes no sense: give it a private constructor.</p>",
 inp="\"9876543210\"",
 approach=["<code>private Phone() {}</code> blocks <code>new Phone()</code> outside the class.", "<code>public static String format(String digits)</code> does the work.", "Call it on the class name."],
 code='''class Phone {
    private Phone() {
    }

    public static String format(String digits) {
        String a = digits.substring(0, 5);
        String b = digits.substring(5);
        return "+91 " + a + " " + b;
    }
}

public class Main {
    public static void main(String[] args) {
        String shown = Phone.format("9876543210");
        System.out.println(shown);
    }
}
''', notes={(14, 1): "Call :: A static call on the class; no object is created (and none can be).", 6: "Split :: ", 7: "Split :: ", 8: "Return :: ", (14, 2): "Result :: ", 15: "Print :: "},
 tryit="Press <b>Run</b>. Then add <code>new Phone();</code> in main and read the error."),
]

PRACTICE_INTRO = "Choose the right access level, fix access errors, and design classes with a small public surface. The last three are business tasks."
PROBLEMS = [
dict(level="easy", title="Getter for a private field", stmt="<p>Make <code>temperature</code> private in <code>Sensor</code> and add a public getter. Print the reading from main.</p>", inp="reading 31",
 code='''class Sensor {
    private int temperature = 31;

    public int getTemperature() {
        return temperature;
    }
}

public class Main {
    public static void main(String[] args) {
        Sensor s = new Sensor();
        System.out.println("Temp: " + s.getTemperature() + " C");
    }
}''', explain="<p><b>How it works:</b> other classes can read the value but not change it, because there is no setter.</p>"),
dict(level="easy", title="Validated setter", stmt="<p>A <code>Product</code> has a private price. The setter must ignore negative prices. Set 499, then try −50, and print the price.</p>", inp="499 then -50",
 code='''class Product {
    private int price;

    public void setPrice(int p) {
        if (p >= 0) {
            price = p;
        }
    }

    public int getPrice() {
        return price;
    }
}

public class Main {
    public static void main(String[] args) {
        Product pen = new Product();
        pen.setPrice(499);
        pen.setPrice(-50);
        System.out.println(pen.getPrice());
    }
}''', explain="<p><b>How it works:</b> because <code>price</code> is private, the setter is the only door, and it rejects bad values.</p>"),
dict(level="easy", title="Same package can see default members", stmt="<p>Two classes in one file share a package. Show that a default-level field and method are visible, but a private one isn't used.</p>", inp="branch \"Kharghar\"",
 code='''class Branch {
    String city = "Kharghar";
    private String vaultCode = "7731";

    String label() {
        return "Branch: " + city;
    }
}

public class Main {
    public static void main(String[] args) {
        Branch b = new Branch();
        System.out.println(b.city);
        System.out.println(b.label());
    }
}''', explain="<p><b>How it works:</b> no keyword means package-private: <code>Main</code> is in the same (unnamed) package, so it can use <code>city</code> and <code>label()</code>. Adding <code>b.vaultCode</code> would not compile.</p>"),
dict(level="medium", title="Read-only object", stmt="<p>Design <code>Ticket</code> so its PNR and seat can be read but never changed after creation: private final fields, a constructor, and getters only.</p>", inp="PNR \"8421937750\", seat \"S4-32\"",
 code='''class Ticket {
    private final String pnr;
    private final String seat;

    public Ticket(String pnr, String seat) {
        this.pnr = pnr;
        this.seat = seat;
    }

    public String getPnr() { return pnr; }
    public String getSeat() { return seat; }
}

public class Main {
    public static void main(String[] args) {
        Ticket t = new Ticket("8421937750", "S4-32");
        System.out.println(t.getPnr() + " " + t.getSeat());
    }
}''', explain="<p><b>How it works:</b> private stops outside writes; final stops even the class itself from reassigning after construction. This “immutable object” style is covered in Lesson 7.1.</p>"),
dict(level="medium", title="Hide a helper method", stmt="<p>A <code>Bill</code> computes a total with a private helper <code>round2</code>. Only <code>total()</code> is public.</p>", inp="items 99.999 and 50.004",
 code='''class Bill {
    private double[] items;

    public Bill(double... items) {
        this.items = items;
    }

    public double total() {
        double t = 0;
        for (double i : items) t += i;
        return round2(t);
    }

    private double round2(double x) {
        return Math.round(x * 100) / 100.0;
    }
}

public class Main {
    public static void main(String[] args) {
        System.out.println(new Bill(99.999, 50.004).total());
    }
}''', explain="<p><b>How it works:</b> callers only need <code>total()</code>. The rounding rule is private, so it can change later (for example to banker's rounding) without affecting any other class. (A varargs constructor from Lesson 5.6 accepts any number of items.)</p>"),
dict(level="business", title="OTP that can't be read back", stmt="<p>An <code>Otp</code> object stores a code privately. It offers <code>verify(String typed)</code> but no getter, so no screen can ever display the code.</p>", inp="code \"482913\"; user types \"482931\", then \"482913\"",
 code='''class Otp {
    private final String code;
    private int attemptsLeft = 3;

    public Otp(String code) {
        this.code = code;
    }

    public boolean verify(String typed) {
        if (attemptsLeft == 0) return false;
        attemptsLeft--;
        return code.equals(typed);
    }
}

public class Main {
    public static void main(String[] args) {
        Otp otp = new Otp("482913");
        System.out.println(otp.verify("482931"));
        System.out.println(otp.verify("482913"));
    }
}''', explain="<p><b>How it works:</b> the class exposes behaviour (verify) instead of data (the code). Attempts are private too, so no caller can reset them.</p>"),
dict(level="business", title="Salary visible to HR only", stmt="<p>An <code>Employee</code> keeps salary private. <code>salaryFor(String role)</code> returns the number only if the role is \"HR\", otherwise \"hidden\".</p>", inp="role \"HR\", role \"TEAM\"",
 code='''class Employee {
    private final String name;
    private final int salary;

    public Employee(String name, int salary) {
        this.name = name;
        this.salary = salary;
    }

    public String salaryFor(String role) {
        if (role.equals("HR")) {
            return name + ": Rs " + salary;
        }
        return name + ": hidden";
    }
}

public class Main {
    public static void main(String[] args) {
        Employee e = new Employee("Kavya", 85000);
        System.out.println(e.salaryFor("HR"));
        System.out.println(e.salaryFor("TEAM"));
    }
}''', explain="<p><b>How it works:</b> the rule about who may see the salary lives inside the class, next to the data. (Real systems check the logged-in user's permissions rather than trusting a role string passed in.)</p>"),
dict(level="business", title="Package-style service with an internal adapter", stmt="<p>Model a <code>PaymentService</code> (public) that uses an internal <code>UpiAdapter</code> (default access) and a private fee rule. Pay Rs 1,000 and print the result.</p>", inp="amount 1000, fee 0.5%",
 code='''class UpiAdapter {
    String send(int amount) {
        return "UPI ok: Rs " + amount;
    }
}

public class Main {
    static class PaymentService {
        private final UpiAdapter upi = new UpiAdapter();

        public String pay(int amount) {
            int fee = fee(amount);
            return upi.send(amount + fee) + " (incl. fee Rs " + fee + ")";
        }

        private int fee(int amount) {
            return amount * 5 / 1000;
        }
    }

    public static void main(String[] args) {
        PaymentService ps = new PaymentService();
        System.out.println(ps.pay(1000));
    }
}''', explain="<p><b>How it works:</b> in a real project, <code>UpiAdapter</code> would sit in the <code>payments</code> package with default access, so only <code>PaymentService</code> uses it. The fee rule is private to the service. (Here a static nested class keeps everything in one runnable file; nested classes come in Lesson 10.5.)</p>"),
]

# ---------------------------------------------------------------------------------------------
# MODIFIER LAB: one field, four access levels, five places that use it (all results from real javac/java)
from mkmodlab import modlab, E as _E
ML_FILES = {
'bank/Account.java': '''package bank;

public class Account {
    {MOD}String ifsc = "SBIN0001234";

    public void showOwn() {
        System.out.println("1. Account itself     : " + ifsc);
    }
}
''',
'bank/Branch.java': '''package bank;

public class Branch {
    public void show() {
        Account a = new Account();
        System.out.println("2. Branch (same pkg)  : " + a.ifsc);
    }
}
''',
'shop/Savings.java': '''package shop;

import bank.Account;

public class Savings extends Account {
    public void show() {
        System.out.println("3. Savings (subclass) : " + ifsc);   // its own inherited copy
    }
}
''',
'shop/Kiosk.java': '''package shop;

import bank.Account;

public class Kiosk {
    public void show() {
        Account a = new Account();
        System.out.println("4. Kiosk (other pkg)  : " + a.ifsc);
    }
}
''',
'shop/Loan.java': '''package shop;

import bank.Account;

public class Loan extends Account {
    public void show() {
        Account other = new Account();
        System.out.println("5. Loan (via parent)  : " + other.ifsc);   // someone else's Account
    }
}
''',
}
ML_USERS = [
    dict(n='1', file='bank/Account.java', who='Account itself', where='same class', use='ifsc  // inside showOwn()', call='new Account().showOwn();'),
    dict(n='2', file='bank/Branch.java', who='Branch', where='same package bank, not a subclass', use='a.ifsc', call='new Branch().show();'),
    dict(n='3', file='shop/Savings.java', who='Savings', where='package shop, subclass of Account', use='ifsc  // inherited, same as this.ifsc', call='new Savings().show();'),
    dict(n='4', file='shop/Kiosk.java', who='Kiosk', where='package shop, not related', use='a.ifsc', call='new Kiosk().show();'),
    dict(n='5', file='shop/Loan.java', who='Loan', where='package shop, subclass, but reads a plain Account object', use='other.ifsc', call='new Loan().show();'),
]
ML_WHY = {
 'public': '<b>public: everyone.</b> No checks fail, so all five classes compile and the program prints <b>5 lines</b>. Convenient, but now any code in any package can also <i>change</i> the IFSC (<code>a.ifsc = "FAKE";</code> would compile too).',
 'protected': '<b>protected: package + subclasses.</b> Compared with public, two lines disappear. <b>Kiosk</b> is outside package <code>bank</code> and is not a subclass, so it is refused. <b>Loan</b> is a subclass, but it reads <code>other.ifsc</code> from a plain <code>Account</code> object, not its own inherited field, so it is refused too. <b>Savings</b> still works because it uses its own inherited <code>ifsc</code>. Output drops to <b>3 lines</b>.',
 'default': '<b>default (no keyword): same package only.</b> Now even the subclass <b>Savings</b> fails, because it lives in package <code>shop</code>. Only the two classes inside <code>bank</code> compile. Note the different wording of the error: <i>is not public in Account; cannot be accessed from outside package</i>. Output drops to <b>2 lines</b>.',
 'private': '<b>private: this class only.</b> Even <b>Branch</b>, a neighbour in the same package, is refused. Only <code>showOwn()</code>, written inside <code>Account</code>, may read the field. Output drops to <b>1 line</b>. To let others read it safely, add <code>public String getIfsc() { return ifsc; }</code>: the field stays private and nobody outside can change it.',
}
_lab, _table = modlab('bank/Account.java', ML_FILES, ML_USERS, ML_WHY)
_shown = ML_FILES['bank/Account.java'].replace('{MOD}String ifsc', 'public String ifsc').replace('";\n', '";   // ← the only word we change\n', 1)
_files_html = ''.join(
    f'<div class="code" data-lang="java" data-file="{f}" data-run="skip"><pre><code>{_E((_shown if f == "bank/Account.java" else src).rstrip())}</code></pre></div>\n  '
    for f, src in ML_FILES.items())
BLOCKS = {'MODLAB': f'''<h3 id="four-modifiers">One field, four modifiers: what compiles and what prints</h3>
  <p>The best way to learn the table is to run it. Here is a small project with two packages. Class <code>bank.Account</code> has one field, <code>ifsc</code>. Five classes try to read it from different places. We will change <b>only the modifier</b> on <code>ifsc</code> and see, each time, which classes compile and how the output changes.</p>
  <div class="code" data-lang="bash" data-file="Project folders"><pre><code>src/
├── bank/
│   ├── Account.java    declares ifsc
│   └── Branch.java     same package, not a subclass
├── shop/
│   ├── Savings.java    other package, subclass (uses its inherited ifsc)
│   ├── Kiosk.java      other package, not related
│   └── Loan.java       other package, subclass (reads ifsc of a plain Account object)
└── app/
    └── Main.java       calls show() on each class</code></pre></div>
  <details class="prob__sol"><summary>Show the five classes</summary>
  {_files_html}</details>
  <p>Press a modifier below. Every ✓, ✗, error message and output line was produced by the real <code>javac</code> and <code>java</code>. When a class does not compile, the whole build fails, so we leave that class out of <code>Main</code> and run the rest.</p>
  {_lab}
  <h4>How the output changes: the whole experiment in one table</h4>
  {_table}
  <p>Read the table column by column: every step down from <code>public</code> to <code>private</code> removes one more group of users. That is exactly the access table above, now with real output.</p>
  <warn><b>The protected trap (row 5):</b> a subclass in another package can use a protected member only <b>through its own inheritance</b>: <code>ifsc</code>, <code>this.ifsc</code>, or a reference of its own type (<code>Loan</code>). Reading it from a plain parent object (<code>other.ifsc</code> where <code>other</code> is an <code>Account</code>) is refused. The same rule applies to a protected constructor: the subclass may call <code>super()</code>, but may not write <code>new Account()</code>.</warn>
  <tip><b>Why the online runner can't show this:</b> it runs one file, and all classes in one file are in the same package. There, <code>public</code>, <code>protected</code> and default all behave alike, and only <code>private</code> changes anything. To see the cross-package results yourself, create the folders above on your PC and run <code>javac -d out bank/*.java shop/*.java app/Main.java</code> then <code>java -cp out app.Main</code>.</tip>
  <p>Methods and constructors follow exactly the same rules. Change <code>ifsc</code> to a method <code>getIfsc()</code> and every ✓ and ✗ stays the same.</p>'''}
