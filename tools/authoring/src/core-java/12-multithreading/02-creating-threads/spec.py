import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from mkanim import Anim, two_view
from m12 import code, snippet, runner, quiz

def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

# ---------------- Part 5: two-view animation ----------------
S = Anim("see", frames=6, h=250, label="Two ways to give a thread its work: extend Thread, or pass a Runnable")
S.box(8, 8, 344, 96, None, fill="board", stroke="board")
lines_a = ["class Sender extends Thread {", "  public void run() { send(); }", "}", "new Sender().start();"]
lines_b = ["Runnable job = () -> send();", "Thread t = new Thread(job);", "t.start();", ""]
for i, l in enumerate(lines_a):
    S.text(18, 28 + i * 20, esc(l), on="1-3", mono=True, size=9.6, cls="chalk")
for i, l in enumerate(lines_b):
    if l:
        S.text(18, 28 + i * 20, esc(l), on="4-", mono=True, size=9.6, cls="chalk")
S.text(10, 128, "Way 1: extend Thread", on="1-3", size=10.5, bold=True, cls="acc")
S.text(10, 128, "Way 2: implement Runnable (a lambda)", on="4-", size=10.5, bold=True, cls="green")
S.box(10, 140, 150, 40, "Sender IS a thread", on="1-3", fill="soft-acc", stroke="track", size=10, bold=True)
S.box(10, 140, 110, 40, "job: the work", on="4-", fill="soft-green", stroke="green", size=10, bold=True)
S.box(200, 140, 120, 40, "t: the worker", on="5-", fill="soft-blue", stroke="blue", size=10, bold=True)
S.arrow(122, 160, 198, 160, on="5-", color="green")
S.text(10, 204, "run() was called by the new thread", on="3", size=10, cls="ink2")
S.text(10, 204, "same job can be given to any worker or a pool", on="6", size=10, cls="green")
S.note({1: "Way 1: a subclass of Thread.", 2: "The work goes in run().", 3: "start() runs it on a new thread.",
        4: "Way 2: the work is a separate Runnable.", 5: "A Thread object carries it out.", 6: "Job and worker stay separate."}, y=234, size=10.5)
S.caps(["<b>Way 1:</b> write a class that <code>extends Thread</code>.",
        "Override <code>run()</code>: whatever is inside it is the thread's work.",
        "<code>start()</code> creates the new thread, and that thread calls <code>run()</code>. You never call <code>run()</code> yourself.",
        "<b>Way 2:</b> put the work in a <code>Runnable</code>, an interface with one method <code>run()</code>. A lambda is the shortest way to write one.",
        "Hand the Runnable to <code>new Thread(job)</code>. The Thread is the worker; the Runnable is the job.",
        "Separating job and worker is the preferred style: your class stays free to extend something else, and the same job can later go to a thread pool (Lesson 12.6)."])

B = Anim("behind", frames=6, h=250, label="On the heap a Thread object points to its Runnable target; start creates a new stack whose first frame calls the target's run")
B.box(6, 6, 200, 200, None, fill="soft-blue", stroke="blue")
B.text(16, 24, "HEAP", size=10, bold=True, cls="blue")
B.box(16, 36, 180, 44, None, fill="card", stroke="line", on="1-")
B.text(26, 54, "#1 Runnable (lambda)", size=9.5, bold=True, mono=True, on="1-")
B.text(26, 70, "run() → send()", size=9, mono=True, cls="ink2", on="1-")
B.box(16, 110, 180, 60, None, fill="card", stroke="line", on="2-")
B.text(26, 128, "#2 Thread \"Thread-0\"", size=9.5, bold=True, mono=True, on="2-")
B.text(26, 144, "target = #1", size=9, mono=True, on="2-", cls="acc")
B.text(26, 160, "state NEW", size=9, mono=True, on="2", cls="ink2")
B.text(26, 160, "state RUNNABLE", size=9, mono=True, on="3-5", cls="green")
B.text(26, 160, "state TERMINATED", size=9, mono=True, on="6", cls="ink3")
B.arrow(120, 110, 120, 82, on="2-", color="track")
B.box(222, 6, 132, 96, None, fill="card2", stroke="line")
B.text(232, 24, "main stack", size=9.5, bold=True, cls="ink2")
B.box(232, 32, 112, 24, "main()", fill="card", stroke="line", size=9, mono=True)
B.text(232, 76, "t.start()", on="3", mono=True, size=9, cls="acc")
B.text(232, 76, "t.join()", on="4-5", mono=True, size=9, cls="ink2")
B.box(222, 112, 132, 94, None, fill="soft-green", stroke="green", on="3-5")
B.text(232, 130, "Thread-0 stack", size=9.5, bold=True, cls="green", on="3-5")
B.box(232, 172, 112, 24, "Thread.run()", fill="card", stroke="line", size=9, mono=True, on="3-5")
B.box(232, 144, 112, 24, "#1.run() → send()", fill="card", stroke="green", size=8.6, mono=True, on="4-5")
B.text(232, 160, "stack freed", on="6", size=10, cls="ink3")
B.note({1: "new: the job object.", 2: "new Thread(job): it stores the target.", 3: "start(): a brand-new stack.",
        4: "Thread.run() calls target.run().", 5: "Both threads run at once.", 6: "run() returned: thread ends."}, y=234, size=10.5)
B.caps(["The lambda becomes a <b>Runnable object</b> (#1) on the heap.",
        "<code>new Thread(job)</code> creates a Thread object (#2). It stores a reference to the job in its <b>target</b> field. State: NEW.",
        "<code>start()</code> creates a new thread with its <b>own stack</b>. The first frame on that stack is <code>Thread.run()</code>.",
        "<code>Thread.run()</code> checks its target and calls <code>target.run()</code>, which calls <code>send()</code>. (If you extend Thread, your overriding <code>run()</code> is called instead.)",
        "Meanwhile <code>main</code> carries on with its own stack, here waiting in <code>join()</code>.",
        "When <code>run()</code> returns, the thread ends: its stack is freed and the Thread object's state becomes TERMINATED. The objects stay on the heap until no longer referenced."])
ANIM = two_view("Creating a thread, both views", S, B)

# ---------------- Part 6: animated example ----------------
ANIM2_HEADING = "Watch it with an example: OTP messages for three customers"
ANIM2_INTRO = "A payments app must send one-time passwords to three customers at once. Each message is a Runnable job; each job gets its own Thread."
A = Anim("Three OTP jobs, three threads", frames=5, h=230, label="Three Runnable jobs are each wrapped in a Thread and started; all three send at the same time")
for i, (ph, y) in enumerate([("98xxx-101", 18), ("97xxx-202", 74), ("99xxx-303", 130)]):
    A.box(10, y, 130, 44, None, fill="soft-acc", stroke="track", on="1-")
    A.text(20, y + 18, f"OtpJob #{i + 1}", size=9.5, bold=True, mono=True, on="1-")
    A.text(20, y + 34, ph, size=9, mono=True, cls="ink2", on="1-")
    A.box(176, y, 104, 44, None, fill="soft-blue", stroke="blue", on="2-")
    A.text(186, y + 18, f"Thread otp-{i + 1}", size=9.2, bold=True, mono=True, on="2-")
    A.text(186, y + 34, "NEW", size=9, mono=True, cls="ink2", on="2")
    A.text(186, y + 34, "RUNNABLE", size=9, mono=True, cls="green", on="3-4")
    A.text(186, y + 34, "TERMINATED", size=9, mono=True, cls="ink3", on="5")
    A.arrow(176, y + 22, 142, y + 22, on="2-", color="track")
    A.text(292, y + 26, "sending…", size=9.5, cls="acc", on="3")
    A.text(292, y + 26, "sent ✓", size=10, bold=True, cls="green", on="4-")
A.note({1: "Three jobs (Runnables).", 2: "Each wrapped in a Thread.", 3: "start() on all three.",
        4: "Messages go out together.", 5: "Threads end; main reports."}, y=204, size=10.5)
A.caps(["For each customer the app creates an <code>OtpJob</code>, a class that <code>implements Runnable</code> and stores the phone number.",
        "Each job is handed to its own <code>new Thread(job, \"otp-1\")</code>. The arrows show each Thread's <b>target</b>.",
        "<code>start()</code> is called on each Thread. The loop doesn't wait: all three are running within microseconds.",
        "The SMS gateway calls overlap, so three messages take about as long as one. (Illustrative.)",
        "After <code>join()</code> on each, <code>main</code> knows all three are sent and can show “OTPs sent” to the operator."])
ANIM2 = A

# ---------------- Part 8: tracer ----------------
TRACE = dict(code='''class Greeter implements Runnable {
    String name;
    String reply;

    Greeter(String name) {
        this.name = name;
    }

    public void run() {
        reply = "Welcome, " + name;
    }
}

public class Main {
    public static void main(String[] args) throws InterruptedException {
        Greeter job = new Greeter("Asha");
        Thread t = new Thread(job, "greeter");
        t.start();
        t.join();
        System.out.println(job.reply + " (from " + t.getName() + ")");
    }
}
''', notes={
 16: "The job :: = A Greeter object is created on the heap. It is only a Runnable: it holds the data and the <code>run()</code> code, but it is not a thread.",
 17: "The worker :: = <code>new Thread(job, \"greeter\")</code> creates a Thread object (state NEW) that keeps a reference to the job as its target.",
 18: "Start :: = <code>start()</code> creates a new thread. That thread calls <code>Thread.run()</code>, which calls <code>job.run()</code>. This trace follows main, so those lines run on the other stack and don't appear here.",
 19: "Join :: = main waits. When <code>join()</code> returns, the greeter thread is TERMINATED and <code>job.reply</code> has been filled in by the other thread.",
 20: "Print :: main reads the field the worker wrote: the job object is shared through the heap."})

# ---------------- Worked examples ----------------
WORKED_INTRO = "Three styles you'll see in real code: a subclass of Thread, a Runnable class that carries its own data, and a method reference. Each trace follows main: watch the job objects and Thread objects on the heap."
EXAMPLES = [
dict(tag="Cinema · tickets", title="A ticket-printer thread by extending Thread",
 problem="<p>A cinema kiosk prints tickets on a printer thread so the touch screen stays free. Write a <code>PrinterThread</code> class that extends <code>Thread</code>, holds the seat numbers, and prints one ticket line per seat. Count how many were printed.</p>",
 inp="seats: A4, A5, A6",
 approach=["Make <code>PrinterThread extends Thread</code> with a field for the seats and a counter.",
           "Override <code>run()</code> with the printing loop. Call <code>super(name)</code> to name the thread.",
           "Create it, <code>start()</code> it, <code>join()</code> it, then read the counter from main."],
 code='''class PrinterThread extends Thread {
    String[] seats;
    int printed = 0;

    PrinterThread(String[] seats) {
        super("printer");
        this.seats = seats;
    }

    @Override
    public void run() {
        for (String s : seats) {
            System.out.println(getName() + ": ticket for seat " + s);
            printed++;
        }
    }
}

public class Main {
    public static void main(String[] args) throws InterruptedException {
        PrinterThread p = new PrinterThread(new String[]{"A4", "A5", "A6"});
        p.start();
        p.join();
        System.out.println("Printed " + p.printed + " tickets");
    }
}
''', notes={21: "Create :: The PrinterThread object is created. Because it extends Thread, it IS the thread object (state NEW) and also holds the seats.",
            22: "Start :: = The new thread calls the overridden <code>run()</code> and prints the three tickets on its own stack.",
            23: "Join :: = main waits for the printer. Now <code>printed</code> is 3 and the thread is TERMINATED.",
            24: "Report :: main reads a field of the same object the printer thread updated."},
 tryit="Press <b>Run</b>. Then change <code>p.start()</code> to <code>p.run()</code>: the output looks the same, but now <code>getName()</code> still says printer while the work really ran on main. Print <code>Thread.currentThread().getName()</code> inside the loop to prove it."),
dict(tag="E-commerce · emails", title="Order-confirmation emails as Runnable jobs",
 problem="<p>After a sale, a shop must send confirmation emails to three customers. Write an <code>EmailJob implements Runnable</code> that stores the address and order id, and records a status after “sending”. Run each job on its own thread and print all statuses in order.</p>",
 inp="(asha@mail.in, 501), (ravi@mail.in, 502), (meena@mail.in, 503)",
 approach=["Each <code>EmailJob</code> holds its own data and its own <code>status</code> field, so no two threads share a field.",
           "Create a Thread for each job and start it.",
           "Join all threads, then print the statuses from the job objects."],
 code='''class EmailJob implements Runnable {
    String to;
    int orderId;
    String status = "pending";

    EmailJob(String to, int orderId) {
        this.to = to;
        this.orderId = orderId;
    }

    public void run() {
        status = "sent #" + orderId + " to " + to;
    }
}

public class Main {
    public static void main(String[] args) throws InterruptedException {
        EmailJob[] jobs = {
            new EmailJob("asha@mail.in", 501),
            new EmailJob("ravi@mail.in", 502),
            new EmailJob("meena@mail.in", 503)
        };
        Thread[] workers = new Thread[jobs.length];
        for (int i = 0; i < jobs.length; i++) {
            workers[i] = new Thread(jobs[i], "mail-" + i);
            workers[i].start();
        }
        for (Thread w : workers) w.join();
        for (EmailJob j : jobs) System.out.println(j.status);
    }
}
''', notes={18: "Jobs :: Three EmailJob objects on the heap, each with status \"pending\".",
            23: "Workers array :: An empty array for three Thread objects.",
            (25, 1): "Thread for job 0 :: A Thread whose target is the first EmailJob.",
            (26, 3): "All started :: = Three threads are running (or already done). Each one writes only its own job's <code>status</code>.",
            28: "Wait :: = After the joins every status says \"sent\".",
            29: "Print :: Reading the results in array order gives the same output every run, whichever thread finished first."},
 tryit="Press <b>Run</b>. Then add a 4th customer to the array: no other code needs to change, because the loop and the job class are separate."),
dict(tag="Banking · month end", title="Two reports with method references",
 problem="<p>At month end a bank builds an interest report and a fee report. The methods already exist in <code>Main</code>. Run each method on its own thread using a <b>method reference</b> instead of writing a Runnable class.</p>",
 inp="balances 10000, 25000, 4000; interest 4% p.a. for one month; fee Rs 50 if balance below 5000",
 approach=["<code>Main::interestReport</code> fits <code>Runnable</code>: no parameters, returns nothing.",
           "Each report method writes its result into a static field.",
           "Start both threads, join both, print both results."],
 code='''public class Main {
    static int[] balances = {10000, 25000, 4000};
    static double interest;
    static int fees;

    static void interestReport() {
        for (int b : balances) interest += b * 0.04 / 12;
    }

    static void feeReport() {
        for (int b : balances) if (b < 5000) fees += 50;
    }

    public static void main(String[] args) throws InterruptedException {
        Thread a = new Thread(Main::interestReport, "interest");
        Thread b = new Thread(Main::feeReport, "fees");
        a.start();
        b.start();
        a.join();
        b.join();
        System.out.printf("Interest Rs %.2f, fees Rs %d%n", interest, fees);
    }
}
''', notes={15: "Method reference :: <code>Main::interestReport</code> becomes a Runnable object whose <code>run()</code> calls that static method.",
            16: "Second job :: Another Runnable, this time for <code>feeReport</code>.",
            17: "Start interest :: = The interest thread starts adding to <code>Main.interest</code>.",
            18: "Start fees :: = The fee thread starts, possibly at the same time. They write different static fields, so they don't clash.",
            20: "Both done :: = Both static fields now hold the final results.",
            21: "Print :: printf formats the interest to two decimal places."},
 tryit="Press <b>Run</b>. Then add a third report method (say, count accounts above Rs 20,000) and run it on a third thread."),
]

# ---------------- Practice problems ----------------
PRACTICE_INTRO = "Create threads in all three styles: extending Thread, implementing Runnable, and lambdas or method references. Each solution joins before printing, so its output is fixed. The last three are business tasks."
PROBLEMS = [
dict(level="easy", title="Extend Thread", stmt="<p>Write a class <code>Hello extends Thread</code> whose <code>run()</code> prints <code>Hello from</code> followed by its thread name. Start one named \"t1\" and wait for it.</p>", inp="(none)",
 code='''class Hello extends Thread {
    Hello(String name) {
        super(name);
    }

    public void run() {
        System.out.println("Hello from " + getName());
    }
}

public class Main {
    public static void main(String[] args) throws InterruptedException {
        Hello h = new Hello("t1");
        h.start();
        h.join();
    }
}''', explain="<p><b>How it works:</b> <code>super(name)</code> passes the name to the Thread constructor. Inside <code>run()</code>, <code>getName()</code> is the inherited Thread method.</p>"),
dict(level="easy", title="Implement Runnable", stmt="<p>Write <code>Counter implements Runnable</code> that prints 1 to 3 on one line. Run it on a thread.</p>", inp="(none)",
 code='''class Counter implements Runnable {
    public void run() {
        for (int i = 1; i <= 3; i++) System.out.print(i + " ");
        System.out.println();
    }
}

public class Main {
    public static void main(String[] args) throws InterruptedException {
        Thread t = new Thread(new Counter());
        t.start();
        t.join();
    }
}''', explain="<p><b>How it works:</b> the Runnable is the job; <code>new Thread(job)</code> is the worker. <code>Counter</code> could still extend another class if it needed to.</p>"),
dict(level="easy", title="Lambda Runnable with a name", stmt="<p>Create a thread with a lambda and the name \"beeper\". The lambda prints <code>beep on</code> and the current thread's name.</p>", inp="(none)",
 code='''public class Main {
    public static void main(String[] args) throws InterruptedException {
        Runnable beep = () -> System.out.println("beep on " + Thread.currentThread().getName());
        Thread t = new Thread(beep, "beeper");
        t.start();
        t.join();
    }
}''', explain="<p><b>How it works:</b> inside a lambda there is no <code>getName()</code> (it's not a Thread subclass), so use <code>Thread.currentThread()</code>.</p>"),
dict(level="medium", title="One job class, three threads", stmt="<p>Write <code>Square implements Runnable</code> that stores a number and computes its square into a field. Run it for 4, 7 and 9 on three threads and print the results in input order.</p>", inp="4, 7, 9",
 code='''class Square implements Runnable {
    int n;
    int result;

    Square(int n) {
        this.n = n;
    }

    public void run() {
        result = n * n;
    }
}

public class Main {
    public static void main(String[] args) throws InterruptedException {
        Square[] jobs = {new Square(4), new Square(7), new Square(9)};
        Thread[] ts = new Thread[3];
        for (int i = 0; i < 3; i++) {
            ts[i] = new Thread(jobs[i]);
            ts[i].start();
        }
        for (Thread t : ts) t.join();
        for (Square s : jobs) System.out.println(s.n + "^2 = " + s.result);
    }
}''', explain="<p><b>How it works:</b> each job object carries its own input and output, so the threads never share a field. Printing from the jobs array keeps the input order.</p>"),
dict(level="medium", title="run() vs start(): who ran it?", stmt="<p>Store the name of the thread that executed a Runnable. Call it once with <code>run()</code> and once through <code>start()</code>, and print both names.</p>", inp="(none)",
 code='''public class Main {
    static String ranOn;

    public static void main(String[] args) throws InterruptedException {
        Thread t = new Thread(() -> ranOn = Thread.currentThread().getName(), "worker");
        t.run();
        System.out.println("run():   " + ranOn);
        t.start();
        t.join();
        System.out.println("start(): " + ranOn);
    }
}''', explain="<p><b>How it works:</b> <code>t.run()</code> is an ordinary method call, so it runs on main. Only <code>start()</code> creates the new thread named worker. (Calling <code>run()</code> first doesn't count as starting, so <code>start()</code> is still allowed.)</p>"),
dict(level="medium", title="Method reference to an instance method", stmt="<p>A <code>Cart</code> object has a method <code>total()</code> that adds its prices into a field. Run <code>cart::total</code> on a thread and print the total.</p>", inp="prices 199, 349, 50",
 code='''class Cart {
    int[] prices = {199, 349, 50};
    int sum;

    void total() {
        for (int p : prices) sum += p;
    }
}

public class Main {
    public static void main(String[] args) throws InterruptedException {
        Cart cart = new Cart();
        Thread t = new Thread(cart::total);
        t.start();
        t.join();
        System.out.println("Cart total: Rs " + cart.sum);
    }
}''', explain="<p><b>How it works:</b> <code>cart::total</code> is bound to that particular cart object. The Runnable created from it calls <code>cart.total()</code> on the new thread.</p>"),
dict(level="business", title="Parallel price check across three sellers", stmt="<p>A comparison site asks three sellers for the price of a phone. Each <code>Quote</code> job looks up its seller's price (from a fixed table) on its own thread. Print each price and the cheapest seller.</p>", inp="Shopkart 18999, BuyNow 18499, MegaMart 19250",
 code='''class Quote implements Runnable {
    String seller;
    int price;

    Quote(String seller) {
        this.seller = seller;
    }

    public void run() {
        price = switch (seller) {
            case "Shopkart" -> 18999;
            case "BuyNow" -> 18499;
            default -> 19250;
        };
    }
}

public class Main {
    public static void main(String[] args) throws InterruptedException {
        Quote[] qs = {new Quote("Shopkart"), new Quote("BuyNow"), new Quote("MegaMart")};
        Thread[] ts = new Thread[qs.length];
        for (int i = 0; i < qs.length; i++) {
            ts[i] = new Thread(qs[i], qs[i].seller);
            ts[i].start();
        }
        for (Thread t : ts) t.join();
        Quote best = qs[0];
        for (Quote q : qs) {
            System.out.println(q.seller + ": Rs " + q.price);
            if (q.price < best.price) best = q;
        }
        System.out.println("Cheapest: " + best.seller);
    }
}''', explain="<p><b>How it works:</b> in a real site each lookup is a slow network call, so running them on separate threads makes the page about as fast as the slowest seller. The comparison happens on main after all joins.</p>"),
dict(level="business", title="Invoice and SMS after a payment", stmt="<p>After a payment of Rs 1,250 succeeds, two independent tasks must run: generate the invoice number and prepare the SMS text. Run each as a lambda on its own thread, then print both.</p>", inp="payment id 7781, amount 1250",
 code='''public class Main {
    static String invoice;
    static String sms;

    public static void main(String[] args) throws InterruptedException {
        int paymentId = 7781;
        int amount = 1250;
        Thread inv = new Thread(() -> invoice = "INV-2026-" + paymentId, "invoice");
        Thread msg = new Thread(() -> sms = "Paid Rs " + amount + ". Ref " + paymentId, "sms");
        inv.start();
        msg.start();
        inv.join();
        msg.join();
        System.out.println(invoice);
        System.out.println(sms);
    }
}''', explain="<p><b>How it works:</b> the lambdas capture <code>paymentId</code> and <code>amount</code>, which are effectively final. Independent tasks after an event are a classic use of threads.</p>"),
dict(level="business", title="Reusable job, different workers", stmt="<p>A <code>StockCheck</code> job counts items below 10 units. Run the <i>same</i> job object twice, on two different threads one after the other, and show it ran on each.</p>", inp="stock 4, 25, 8, 13, 2",
 code='''class StockCheck implements Runnable {
    int[] stock = {4, 25, 8, 13, 2};

    public void run() {
        int low = 0;
        for (int s : stock) if (s < 10) low++;
        System.out.println(Thread.currentThread().getName() + ": " + low + " items low");
    }
}

public class Main {
    public static void main(String[] args) throws InterruptedException {
        StockCheck job = new StockCheck();
        Thread morning = new Thread(job, "morning-check");
        morning.start();
        morning.join();
        Thread evening = new Thread(job, "evening-check");
        evening.start();
        evening.join();
    }
}''', explain="<p><b>How it works:</b> a Thread can be started only once, but a Runnable job can be given to as many workers as you like. <code>low</code> is a local variable, so each run has its own copy on its own stack.</p>"),
]

# ---------------- Extra blocks ----------------
BLOCKS = {
'ANIM': ANIM,
'CODE_WAYS': code('''class Packer extends Thread {
    public void run() {
        System.out.println("1. subclass of Thread");
    }
}

class Labeller implements Runnable {
    public void run() {
        System.out.println("2. Runnable class");
    }
}

public class Main {
    static void ship() {
        System.out.println("4. method reference");
    }

    public static void main(String[] args) throws InterruptedException {
        Thread[] ts = {
            new Packer(),
            new Thread(new Labeller()),
            new Thread(() -> System.out.println("3. lambda")),
            new Thread(Main::ship)
        };
        for (Thread t : ts) {
            t.start();
            t.join();
        }
    }
}'''),
'CODE_CTOR': snippet('''new Thread(Runnable task)                 // default name Thread-N
new Thread(Runnable task, String name)    // recommended: a meaningful name
new Thread(String name)                   // for subclasses that override run()
Thread.ofPlatform().name("worker").start(task)   // Java 21 builder style'''),
'CODE_RUN': code('''public class Main {
    static String[] orders = {"#101 pizza", "#102 dosa", "#103 biryani"};

    static void prepare(String order) {
        System.out.println(Thread.currentThread().getName() + " prepares " + order);
    }

    public static void main(String[] args) throws InterruptedException {
        Thread[] cooks = new Thread[orders.length];
        for (int i = 0; i < orders.length; i++) {
            String order = orders[i];
            cooks[i] = new Thread(() -> prepare(order), "cook-" + (i + 1));
            cooks[i].start();
        }
        for (Thread c : cooks) {
            c.join();
        }
        System.out.println("All " + cooks.length + " orders ready");
    }
}''', skip=True),
'RUNNER': runner([
 dict(label="1 · Kitchen threads", hint="Press <b>Run</b> a few times; the order of the “prepares” lines may change. Then add a fourth order to the array.",
      code='''public class Main {
    static String[] orders = {"#101 pizza", "#102 dosa", "#103 biryani"};

    static void prepare(String order) {
        System.out.println(Thread.currentThread().getName() + " prepares " + order);
    }

    public static void main(String[] args) throws InterruptedException {
        Thread[] cooks = new Thread[orders.length];
        for (int i = 0; i < orders.length; i++) {
            String order = orders[i];
            cooks[i] = new Thread(() -> prepare(order), "cook-" + (i + 1));
            cooks[i].start();
        }
        for (Thread c : cooks) {
            c.join();
        }
        System.out.println("All " + cooks.length + " orders ready");
    }
}'''),
 dict(label="2 · Predict: forgot to override", hint="<b>Predict first:</b> what does this print? The class spells the method <code>Run</code>. Add <code>@Override</code> above it and compile again: the compiler now catches the mistake.",
      code='''class Backup extends Thread {
    public void Run() {
        System.out.println("backing up files");
    }
}

public class Main {
    public static void main(String[] args) throws InterruptedException {
        Backup b = new Backup();
        b.start();
        b.join();
        System.out.println("main done");
    }
}'''),
 dict(label="3 · Predict: run() on a subclass", hint="<b>Predict first:</b> which thread name is printed? Then change <code>run()</code> to <code>start()</code> and add <code>join()</code>.",
      code='''class Report extends Thread {
    Report() {
        super("report-thread");
    }

    public void run() {
        System.out.println("built on " + Thread.currentThread().getName());
    }
}

public class Main {
    public static void main(String[] args) {
        new Report().run();
    }
}'''),
 dict(label="4 · Crash: daemon too late", hint="<code>setDaemon</code> must be called <b>before</b> <code>start()</code>. Move the line up and run again.",
      code='''public class Main {
    public static void main(String[] args) {
        Thread sync = new Thread(() -> {
            try { Thread.sleep(300); } catch (InterruptedException e) { }
        }, "sync");
        sync.start();
        sync.setDaemon(true);
        System.out.println("sync is a daemon");
    }
}''', _expect="exception"),
 dict(label="5 · Spot the error", hint="<code>Runnable.run()</code> declares no checked exceptions, so a lambda used as a Runnable can't throw <code>InterruptedException</code>. Wrap the sleep in try/catch inside the lambda.",
      code='''public class Main {
    public static void main(String[] args) throws InterruptedException {
        Runnable reminder = () -> {
            Thread.sleep(200);
            System.out.println("Your EMI is due tomorrow");
        };
        Thread t = new Thread(reminder);
        t.start();
        t.join();
    }
}''', _expect="compile-error"),
]),
'QUIZ': quiz([
 {"q": "Which method must you override when you extend Thread?", "options": ["start()", "run()", "main()", "execute()"], "answer": 1, "why": "run() holds the thread's work. start() is inherited and must not be overridden."},
 {"q": "Runnable is…", "options": ["a class with start()", "a functional interface with one method run()", "a subclass of Thread", "a keyword"], "answer": 1, "why": "Runnable has exactly one abstract method, void run(), so a lambda can implement it."},
 {"q": "Why is implementing Runnable usually preferred over extending Thread?", "options": ["It's faster", "Your class can still extend another class, and the job is separate from the worker", "Thread is deprecated", "Runnable threads never crash"], "answer": 1, "why": "Java allows one superclass. Keeping the job separate also lets you send it to a thread pool later."},
 {"q": "What does new Thread(job) do?", "options": ["Starts job immediately", "Creates a Thread object in state NEW whose target is job", "Calls job.run()", "Nothing"], "answer": 1, "why": "Nothing runs until start() is called."},
 {"q": "A class extends Thread but names its method Run() by mistake. What happens on start()?", "options": ["Compile error", "Run() is called", "Thread's own empty run() is called, so nothing happens", "Exception"], "answer": 2, "why": "Run is a different method. Use @Override so the compiler catches such mistakes."},
 {"q": "Can a lambda used as a Runnable call Thread.sleep() without try/catch?", "options": ["Yes", "No: run() doesn't declare InterruptedException", "Only in main", "Only if the thread is a daemon"], "answer": 1, "why": "A checked exception must be caught inside run() (Lesson 9.3)."},
 {"q": "Which of these is a valid Runnable?", "options": ["Main::ship where ship() is static void and takes no parameters", "Main::ship where ship(int x)", "Main::ship where ship() returns int and takes a String", "\"ship\""], "answer": 0, "why": "A method reference fits Runnable if it takes no arguments (the return value, if any, is ignored)."},
 {"q": "Can the same Runnable object be given to two different Thread objects?", "options": ["No, never", "Yes", "Only if it's a lambda", "Only after the first thread is NEW"], "answer": 1, "why": "A Thread can be started only once, but the job can be reused. Just be careful if the job has fields both threads change."},
]),
}
