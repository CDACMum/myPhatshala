import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from mkanim import Anim, two_view
from m12 import code, snippet, runner, quiz

def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

# ---------------- Part 5: two-view animation ----------------
S = Anim("see", frames=6, h=250, label="Two threads do count++ at the same time and one update is lost; with synchronized they take turns")
S.box(130, 10, 100, 44, None, fill="soft-blue", stroke="blue")
S.text(180, 28, "count", size=9.5, anchor="middle", bold=True, cls="blue")
vals = {1: "5", 2: "5", 3: "5", 4: "6", 5: "6", 6: "7"}
for f, v in vals.items():
    S.text(180, 47, v, on=str(f), size=14, bold=True, mono=True, anchor="middle", cls="red" if f == 4 else "ink")
for x, n in [(10, "T1"), (250, "T2")]:
    S.box(x, 74, 100, 96, None, fill="card2", stroke="line")
    S.text(x + 10, 92, n, size=10.5, bold=True)
S.text(20, 114, "count++", mono=True, size=9.5, on="1")
S.text(260, 114, "count++", mono=True, size=9.5, on="1")
S.text(20, 114, "read 5", mono=True, size=9.5, on="2-4", cls="acc")
S.text(260, 114, "read 5", mono=True, size=9.5, on="3-4", cls="acc")
S.text(20, 134, "write 6", mono=True, size=9.5, on="4", cls="red")
S.text(260, 134, "write 6", mono=True, size=9.5, on="4", cls="red")
S.arrow(110, 104, 140, 54, on="2", color="acc")
S.arrow(250, 104, 220, 54, on="3", color="acc")
S.text(180, 196, "2 increments, count went up by 1", size=10, bold=True, anchor="middle", cls="red", on="4")
S.box(118, 60, 124, 24, "synchronized", fill="soft-green", stroke="green", on="5-", size=9, bold=True)
S.text(20, 114, "has lock: 5→6", mono=True, size=9, on="5", cls="green")
S.text(260, 114, "BLOCKED", mono=True, size=9.5, on="5", cls="red", bold=True)
S.text(20, 114, "done", mono=True, size=9.5, on="6", cls="ink3")
S.text(260, 114, "has lock: 6→7", mono=True, size=9, on="6", cls="green")
S.text(180, 196, "they take turns: no update lost", size=10, bold=True, anchor="middle", cls="green", on="6")
S.note({1: "Two threads, one shared count.", 2: "T1 reads 5…", 3: "…T2 also reads 5.",
        4: "Both write 6: one update lost.", 5: "With synchronized, T2 must wait.", 6: "T2 then sees 6 and writes 7."}, y=234, size=10.5)
S.caps(["<code>count</code> is a shared field on the heap, value 5. Two threads both run <code>count++</code>.",
        "<code>count++</code> is not one step. T1 first <b>reads</b> 5 into its own working space…",
        "…and before T1 writes back, the scheduler lets T2 run. T2 also reads 5.",
        "Both add 1 and both write 6. Two increments, but count only went up by 1: a <b>lost update</b>. This is a <b>race condition</b>.",
        "Now <code>count++</code> is inside a <code>synchronized</code> block. T1 takes the lock first; T2 arrives, finds the lock taken, and is <b>BLOCKED</b>.",
        "T1 writes 6 and releases the lock. T2 gets the lock, reads 6, writes 7. The result is always correct."])

B = Anim("behind", frames=6, h=250, label="count++ compiles to four bytecode steps; a monitor lock lets only one thread run them at a time")
B.box(6, 6, 150, 112, None, fill="board", stroke="board")
B.text(16, 24, "count++ in bytecode", size=9, bold=True, cls="chalk")
bc = ["getstatic count", "iconst_1", "iadd", "putstatic count"]
for i, l in enumerate(bc):
    B.text(16, 44 + i * 18, l, mono=True, size=9.2, cls="chalk")
B.box(10, 30, 142, 20, None, fill="none", stroke="track", on="2-3", rx=3)
B.box(10, 84, 142, 20, None, fill="none", stroke="red", on="4", rx=3)
for x, n in [(170, "T1 operand stack"), (266, "T2 operand stack")]:
    B.box(x, 6, 88, 62, None, fill="card2", stroke="line")
    B.text(x + 6, 22, n, size=8, bold=True, cls="ink2")
B.text(190, 48, "5", mono=True, size=13, bold=True, on="2-3", cls="acc")
B.text(190, 48, "6", mono=True, size=13, bold=True, on="4", cls="red")
B.text(286, 48, "5", mono=True, size=13, bold=True, on="3", cls="acc")
B.text(286, 48, "6", mono=True, size=13, bold=True, on="4", cls="red")
B.text(178, 92, "a switch can happen between", size=8.8, cls="ink2", on="2-4")
B.text(178, 106, "any two of these steps", size=8.8, cls="ink2", on="2-4")
B.box(170, 80, 184, 96, None, fill="soft-green", stroke="green", on="5-")
B.text(180, 98, "monitor of the lock object", size=9, bold=True, cls="green", on="5-")
B.text(180, 118, "owner: T1", mono=True, size=9.5, on="5")
B.text(180, 118, "owner: T2", mono=True, size=9.5, on="6")
B.text(180, 136, "entry set: T2 (BLOCKED)", mono=True, size=9, cls="red", on="5")
B.text(180, 136, "entry set: (empty)", mono=True, size=9, cls="ink3", on="6")
B.text(180, 156, "monitorenter … monitorexit", mono=True, size=8.6, cls="ink2", on="5-")
B.text(10, 146, "count on the heap:", size=9.5, cls="ink2")
for f, v in vals.items():
    B.text(116, 147, v, on=str(f), mono=True, size=12, bold=True, cls="red" if f == 4 else "ink")
B.note({1: "One line of Java…", 2: "…is four bytecode steps.", 3: "T2 interleaves after T1's read.",
        4: "Two writes of 6.", 5: "The lock has one owner at a time.", 6: "Ownership passes to T2."}, y=236, size=10.5)
B.caps(["<code>count++</code> looks like one action, but the compiler turns it into several bytecode instructions.",
        "<code>getstatic</code> copies the current value (5) onto T1's own <b>operand stack</b>. The shared field isn't changed yet.",
        "The scheduler can switch threads between any two instructions. T2 also copies 5 onto its own stack.",
        "Each thread adds 1 and <code>putstatic</code> writes 6. The second write overwrites the first.",
        "<code>synchronized</code> compiles to <code>monitorenter</code> / <code>monitorexit</code>. Every object has a <b>monitor</b>: one owner at a time, and other threads wait in its entry set (BLOCKED).",
        "When T1 leaves the block, the lock is released and T2 becomes the owner. Leaving the block also makes T1's write <b>visible</b> to the next thread that takes the lock."])
ANIM = two_view("A race condition and its fix", S, B)

# ---------------- Part 6: animated example ----------------
ANIM2_HEADING = "Watch it with an example: two ATMs, one joint account"
ANIM2_INTRO = "A joint account has ₹1,000. Two holders withdraw ₹800 at two ATMs at the same moment. Without a lock, both succeed."
A = Anim("Two ATMs, one balance", frames=6, h=230, label="Without synchronization both withdrawals pass the balance check; with a synchronized withdraw the second is refused")
A.box(130, 14, 100, 50, None, fill="soft-blue", stroke="blue")
A.text(180, 32, "balance", size=9.5, anchor="middle", bold=True, cls="blue")
bal = {1: "₹1000", 2: "₹1000", 3: "₹200", 4: "₹-600", 5: "₹200", 6: "₹200"}
for f, v in bal.items():
    A.text(180, 54, v, on=str(f), size=13, bold=True, mono=True, anchor="middle", cls="red" if f == 4 else "ink")
for x, n in [(10, "ATM 1"), (250, "ATM 2")]:
    A.box(x, 84, 100, 86, None, fill="card2", stroke="line")
    A.text(x + 10, 102, n, size=10, bold=True)
A.text(20, 124, "1000 ≥ 800 ✓", size=9, mono=True, on="2-4", cls="green")
A.text(260, 124, "1000 ≥ 800 ✓", size=9, mono=True, on="2-4", cls="green")
A.text(20, 144, "pay ₹800", size=9.5, on="3-4", bold=True)
A.text(260, 144, "pay ₹800", size=9.5, on="4", bold=True)
A.text(180, 188, "overdrawn by ₹600!", size=11, bold=True, anchor="middle", cls="red", on="4")
A.box(118, 66, 124, 18, "synchronized withdraw", fill="soft-green", stroke="green", on="5-", size=8.6, bold=True)
A.text(20, 124, "1000 ≥ 800 ✓", size=9, mono=True, on="5-", cls="green")
A.text(20, 144, "paid ₹800", size=9.5, on="5-", bold=True)
A.text(260, 124, "waits…", size=9.5, on="5", cls="red", bold=True)
A.text(260, 124, "200 ≥ 800 ✗", size=9, mono=True, on="6", cls="red")
A.text(260, 144, "refused", size=9.5, on="6", bold=True, cls="red")
A.text(180, 188, "balance never goes negative", size=11, bold=True, anchor="middle", cls="green", on="6")
A.note({1: "₹1000 in the account.", 2: "Both ATMs check the balance.", 3: "ATM 1 pays out.", 4: "ATM 2 pays out too.",
        5: "With a lock: ATM 2 waits.", 6: "Then it sees ₹200 and refuses."}, y=206, size=10.5)
A.caps(["A shared <code>Account</code> object with balance ₹1,000. Two threads (two ATMs) call <code>withdraw(800)</code>.",
        "Both run <code>if (balance &gt;= amount)</code> before either subtracts. Both checks pass.",
        "ATM 1 subtracts: ₹200 left.",
        "ATM 2 already passed its check, so it subtracts too: ₹−600. The bank paid ₹1,600 from ₹1,000. This is a <b>check-then-act</b> race.",
        "Make <code>withdraw</code> <code>synchronized</code>: the check and the subtraction become one indivisible step. ATM 2 is BLOCKED until ATM 1 is done.",
        "ATM 2 now checks against ₹200 and refuses. Real banks protect balances the same way, usually with database locks or transactions."])
ANIM2 = A

# ---------------- Part 8: tracer ----------------
TRACE = dict(code='''class Counter {
    private int value;

    synchronized void add() {
        value++;
    }

    synchronized int get() {
        return value;
    }
}

public class Main {
    public static void main(String[] args) throws InterruptedException {
        Counter likes = new Counter();
        Runnable tap = () -> {
            for (int i = 0; i < 1000; i++) likes.add();
        };
        Thread a = new Thread(tap, "phone-A");
        Thread b = new Thread(tap, "phone-B");
        a.start();
        b.start();
        a.join();
        b.join();
        System.out.println("likes = " + likes.get());
    }
}
''', notes={
 15: "Shared object :: = One Counter object (#n) on the heap. Its monitor is the lock that <code>synchronized</code> methods use.",
 16: "The job :: Both threads will run this same lambda, so both call <code>add()</code> on the same Counter.",
 19: "Thread A :: The first Thread object (NEW).",
 20: "Thread B :: The second Thread object (NEW), with the same job.",
 21: "Start A :: = Phone A starts tapping. Each <code>add()</code> takes the Counter's lock, does <code>value++</code>, and releases it.",
 22: "Start B :: = Phone B starts. When it calls <code>add()</code> while A holds the lock, it is BLOCKED for a moment, then continues.",
 24: "Both done :: = After both joins, all 2000 increments have happened; none were lost.",
 25: "Read :: = <code>get()</code> is synchronized too, so main reads the latest value: 2000 every run. Remove both <code>synchronized</code> keywords and you'll often get less."})

# ---------------- Worked examples ----------------
WORKED_INTRO = "Three ways to make shared data safe: a synchronized method, an atomic class, and a volatile flag. Each trace follows main; the other threads' work shows up in the shared objects on the heap."
EXAMPLES = [
dict(tag="Ticketing · last seat", title="Only one person gets the last seat",
 problem="<p>A concert has 1 seat left. Two customers press Book at the same moment, each on their own thread. Exactly one booking must succeed. Make <code>book()</code> safe and print how many bookings succeeded and how many seats are left.</p>",
 inp="seats left: 1; two booking threads",
 approach=["The check (<code>left &gt; 0</code>) and the update (<code>left--</code>) must happen as one step, so put both inside a <code>synchronized</code> method.",
           "Each thread stores whether it succeeded in its own array slot.",
           "After joining, count the successes. The winner's name may vary; the counts never do."],
 code='''class Show {
    private int left = 1;

    synchronized boolean book() {
        if (left > 0) {
            left--;
            return true;
        }
        return false;
    }

    synchronized int seatsLeft() {
        return left;
    }
}

public class Main {
    public static void main(String[] args) throws InterruptedException {
        Show show = new Show();
        boolean[] ok = new boolean[2];
        Thread asha = new Thread(() -> ok[0] = show.book(), "asha");
        Thread ravi = new Thread(() -> ok[1] = show.book(), "ravi");
        asha.start();
        ravi.start();
        asha.join();
        ravi.join();
        int wins = (ok[0] ? 1 : 0) + (ok[1] ? 1 : 0);
        System.out.println("successful bookings: " + wins + ", seats left: " + show.seatsLeft());
    }
}
''', notes={19: "Shared show :: One Show object with <code>left = 1</code>. Its monitor guards <code>book()</code>.",
            20: "Results :: Each thread writes its own slot, so this array needs no lock.",
            23: "Start :: = Asha's thread tries to book.",
            24: "Start :: = Ravi's thread tries at the same time. Whoever gets the lock second finds <code>left == 0</code>.",
            26: "Both done :: = Exactly one of the two slots is true.",
            27: "Count :: One win, zero seats left, on every run."},
 tryit="Press <b>Run</b>. Then remove <code>synchronized</code> from <code>book()</code> and set <code>left</code> to 1 with 50 threads: sometimes more than one booking succeeds and <code>left</code> goes negative."),
dict(tag="Payments · cashback", title="Cashback counter with AtomicInteger",
 problem="<p>Four payment servers each credit ₹1 cashback 1,000 times to the same wallet total. Use <code>AtomicInteger</code> so no credit is lost, without writing <code>synchronized</code>.</p>",
 inp="4 threads × 1,000 credits of ₹1",
 approach=["<code>AtomicInteger.incrementAndGet()</code> performs read-add-write as one indivisible hardware operation (compare-and-swap).",
           "All four threads share one AtomicInteger.",
           "Join all, then print the total: always 4000."],
 code='''import java.util.concurrent.atomic.AtomicInteger;

public class Main {
    public static void main(String[] args) throws InterruptedException {
        AtomicInteger cashback = new AtomicInteger();
        Thread[] servers = new Thread[4];
        for (int s = 0; s < 4; s++) {
            servers[s] = new Thread(() -> {
                for (int i = 0; i < 1000; i++) cashback.incrementAndGet();
            }, "server-" + s);
            servers[s].start();
        }
        for (Thread t : servers) t.join();
        System.out.println("total cashback: Rs " + cashback.get());
    }
}
''', notes={5: "Atomic :: = An AtomicInteger object on the heap, value 0. Its methods are safe to call from many threads at once.",
            6: "Array :: Room for four server threads.",
            (11, 1): "Start server-0 :: = The first server starts crediting.",
            (11, 4): "All started :: = Four threads are incrementing the same AtomicInteger.",
            13: "Join :: = Wait for all four.",
            14: "Total :: 4 × 1000 = 4000, every run, with no lock in sight."},
 tryit="Press <b>Run</b>. Then replace the AtomicInteger with a plain <code>static int</code> and <code>count++</code>: the total usually comes out below 4000."),
dict(tag="Streaming · shutdown", title="Stop a worker with a volatile flag",
 problem="<p>A video-encoding worker keeps processing chunks while a flag <code>running</code> is true. main lets it work for a moment, then sets the flag to false. Without <code>volatile</code>, the worker might never see the change. Make the stop reliable.</p>",
 inp="(no input)",
 approach=["Declare <code>static volatile boolean running = true;</code>.",
           "The worker loops <code>while (running)</code>.",
           "main sleeps briefly, sets <code>running = false</code>, joins the worker, and reports."],
 code='''public class Main {
    static volatile boolean running = true;
    static long chunks = 0;

    public static void main(String[] args) throws InterruptedException {
        Thread encoder = new Thread(() -> {
            while (running) {
                chunks++;
            }
            System.out.println("encoder: saw running = false, stopping");
        }, "encoder");
        encoder.start();
        Thread.sleep(50);
        running = false;
        encoder.join();
        System.out.println("encoded some chunks: " + (chunks > 0));
    }
}
''', notes={6: "Create :: The encoder thread object.",
            12: "Start :: = The encoder spins, counting chunks, re-reading <code>running</code> each time.",
            13: "Let it work :: = main pauses 50 ms while the encoder runs.",
            14: "Signal :: = main writes false. Because <code>running</code> is <code>volatile</code>, the write is published to all threads at once and the encoder's next read sees it.",
            15: "Join :: = The encoder leaves its loop, prints, and ends.",
            16: "Report :: <code>chunks</code> is only read after <code>join()</code>, which guarantees we see the encoder's final value."},
 tryit="Press <b>Run</b>. Then remove <code>volatile</code>: on many JVMs the program may never end, because the JIT compiler can hoist the read of <code>running</code> out of the loop. (The online runner would time out.)"),
]

# ---------------- Practice problems ----------------
PRACTICE_INTRO = "Find the shared data, then protect it with <code>synchronized</code>, an atomic class, or <code>volatile</code>. Every solution prints the same result on every run. The last three are business tasks."
PROBLEMS = [
dict(level="easy", title="Synchronized counter", stmt="<p>Two threads each call <code>inc()</code> 50,000 times on one counter. Make the total always 100000.</p>", inp="2 × 50,000",
 code='''class Counter {
    private int n;
    synchronized void inc() { n++; }
    synchronized int get() { return n; }
}

public class Main {
    public static void main(String[] args) throws InterruptedException {
        Counter c = new Counter();
        Runnable job = () -> { for (int i = 0; i < 50_000; i++) c.inc(); };
        Thread a = new Thread(job), b = new Thread(job);
        a.start(); b.start();
        a.join(); b.join();
        System.out.println(c.get());
    }
}''', explain="<p><b>How it works:</b> a synchronized instance method locks <code>this</code>. Both threads use the same Counter, so they take turns inside <code>inc()</code>.</p>"),
dict(level="easy", title="Synchronized block on a lock object", stmt="<p>Do the same with a static <code>int</code> and a <code>synchronized (LOCK)</code> block around <code>count++</code> only.</p>", inp="2 × 50,000",
 code='''public class Main {
    static int count = 0;
    static final Object LOCK = new Object();

    public static void main(String[] args) throws InterruptedException {
        Runnable job = () -> {
            for (int i = 0; i < 50_000; i++) {
                synchronized (LOCK) {
                    count++;
                }
            }
        };
        Thread a = new Thread(job), b = new Thread(job);
        a.start(); b.start();
        a.join(); b.join();
        System.out.println(count);
    }
}''', explain="<p><b>How it works:</b> a block lets you lock only the lines that touch shared data. Make the lock object <code>final</code> so it can never be replaced.</p>"),
dict(level="easy", title="AtomicInteger", stmt="<p>Three threads each add 10 to an <code>AtomicInteger</code> 100 times using <code>addAndGet</code>. Print the result.</p>", inp="3 × 100 × 10",
 code='''import java.util.concurrent.atomic.AtomicInteger;

public class Main {
    public static void main(String[] args) throws InterruptedException {
        AtomicInteger total = new AtomicInteger();
        Thread[] ts = new Thread[3];
        for (int i = 0; i < 3; i++) {
            ts[i] = new Thread(() -> { for (int k = 0; k < 100; k++) total.addAndGet(10); });
            ts[i].start();
        }
        for (Thread t : ts) t.join();
        System.out.println(total.get());
    }
}''', explain="<p><b>How it works:</b> atomic classes use a CPU compare-and-swap instruction, retrying if another thread got there first. No thread is ever BLOCKED.</p>"),
dict(level="medium", title="Static synchronized across objects", stmt="<p>Each thread uses its <b>own</b> <code>Visit</code> object, but all visits must be counted in one static total. Use a <code>static synchronized</code> method.</p>", inp="4 threads × 2,500 visits",
 code='''class Visit {
    private static int total = 0;

    static synchronized void record() { total++; }
    static synchronized int total() { return total; }
}

public class Main {
    public static void main(String[] args) throws InterruptedException {
        Thread[] ts = new Thread[4];
        for (int i = 0; i < 4; i++) {
            ts[i] = new Thread(() -> { for (int k = 0; k < 2500; k++) Visit.record(); });
            ts[i].start();
        }
        for (Thread t : ts) t.join();
        System.out.println("visits: " + Visit.total());
    }
}''', explain="<p><b>How it works:</b> a static synchronized method locks the <b>class object</b> <code>Visit.class</code>, one lock for the whole class, which is right for a static field. An instance lock (<code>this</code>) would not protect it if the threads used different objects.</p>"),
dict(level="medium", title="Thread-safe list", stmt="<p>Two threads each add 1,000 items to a shared list. A plain ArrayList can lose items or crash. Use <code>Collections.synchronizedList</code> and print the size.</p>", inp="2 × 1,000 items",
 code='''import java.util.*;

public class Main {
    public static void main(String[] args) throws InterruptedException {
        List<Integer> orders = Collections.synchronizedList(new ArrayList<>());
        Runnable job = () -> { for (int i = 0; i < 1000; i++) orders.add(i); };
        Thread a = new Thread(job), b = new Thread(job);
        a.start(); b.start();
        a.join(); b.join();
        System.out.println("orders: " + orders.size());
    }
}''', explain="<p><b>How it works:</b> the wrapper makes each method synchronized. ArrayList's <code>add</code> does several steps (check capacity, store, size++), so unsynchronized adds can be lost. For heavy use, prefer <code>java.util.concurrent</code> collections such as <code>CopyOnWriteArrayList</code> or <code>ConcurrentHashMap</code>.</p>"),
dict(level="medium", title="Check-then-act fixed", stmt="<p>A coupon can be used at most 3 times. Ten threads try to redeem it. Make <code>redeem()</code> safe and print how many succeeded.</p>", inp="limit 3, 10 attempts",
 code='''class Coupon {
    private int uses = 0;

    synchronized boolean redeem() {
        if (uses < 3) {
            uses++;
            return true;
        }
        return false;
    }
}

public class Main {
    public static void main(String[] args) throws InterruptedException {
        Coupon c = new Coupon();
        boolean[] ok = new boolean[10];
        Thread[] ts = new Thread[10];
        for (int i = 0; i < 10; i++) {
            int k = i;
            ts[i] = new Thread(() -> ok[k] = c.redeem());
            ts[i].start();
        }
        int wins = 0;
        for (int i = 0; i < 10; i++) {
            ts[i].join();
            if (ok[i]) wins++;
        }
        System.out.println("redeemed " + wins + " times");
    }
}''', explain="<p><b>How it works:</b> the comparison and the increment must be in the same synchronized method. Synchronizing them separately would still allow two threads to pass the check before either increments.</p>"),
dict(level="business", title="Flash-sale stock reservation", stmt="<p>A phone has 5 units in stock. Eight shoppers' threads each try to reserve one. Print reserved and sold-out counts and the final stock.</p>", inp="stock 5, 8 shoppers",
 code='''class Stock {
    private int units = 5;

    synchronized boolean reserve() {
        if (units == 0) return false;
        units--;
        return true;
    }

    synchronized int units() { return units; }
}

public class Main {
    public static void main(String[] args) throws InterruptedException {
        Stock phone = new Stock();
        boolean[] got = new boolean[8];
        Thread[] shoppers = new Thread[8];
        for (int i = 0; i < 8; i++) {
            int k = i;
            shoppers[i] = new Thread(() -> got[k] = phone.reserve(), "shopper-" + i);
            shoppers[i].start();
        }
        int reserved = 0;
        for (int i = 0; i < 8; i++) {
            shoppers[i].join();
            if (got[i]) reserved++;
        }
        System.out.println("reserved: " + reserved + ", sold out for: " + (8 - reserved) + ", stock now: " + phone.units());
    }
}''', explain="<p><b>How it works:</b> this is the classic overselling bug in flash sales. Real systems use the same idea one level down: a database row lock or an atomic <code>UPDATE … WHERE units &gt; 0</code>.</p>"),
dict(level="business", title="Transfers without deadlock", stmt="<p>Two threads run transfers at once: ten of A→B ₹100 and ten of B→A ₹50. Each must lock both accounts. Always lock the account with the smaller id first, so the threads can't deadlock. Print the final balances.</p>", inp="A (id 1) ₹500, B (id 2) ₹300",
 code='''class Account {
    final int id;
    int balance;

    Account(int id, int balance) {
        this.id = id;
        this.balance = balance;
    }
}

public class Main {
    static void transfer(Account from, Account to, int amt) {
        Account first = from.id < to.id ? from : to;
        Account second = first == from ? to : from;
        synchronized (first) {
            synchronized (second) {
                from.balance -= amt;
                to.balance += amt;
            }
        }
    }

    public static void main(String[] args) throws InterruptedException {
        Account a = new Account(1, 500), b = new Account(2, 300);
        Thread t1 = new Thread(() -> { for (int i = 0; i < 10; i++) transfer(a, b, 100); });
        Thread t2 = new Thread(() -> { for (int i = 0; i < 10; i++) transfer(b, a, 50); });
        t1.start(); t2.start();
        t1.join(); t2.join();
        System.out.println("A: " + a.balance + ", B: " + b.balance + ", total: " + (a.balance + b.balance));
    }
}''', explain="<p><b>How it works:</b> if t1 locked A then waited for B while t2 locked B then waited for A, both would wait forever: a <b>deadlock</b>. A fixed global lock order makes that cycle impossible. The total stays ₹800. (No balance checks here, so balances may go negative; it's only a locking demo.)</p>"),
dict(level="business", title="Page-view counter for a news site", stmt="<p>Six web threads each record 5,000 page views. Use <code>LongAdder</code>, which is faster than AtomicLong when many threads update often, and print the total.</p>", inp="6 × 5,000",
 code='''import java.util.concurrent.atomic.LongAdder;

public class Main {
    public static void main(String[] args) throws InterruptedException {
        LongAdder views = new LongAdder();
        Thread[] web = new Thread[6];
        for (int i = 0; i < 6; i++) {
            web[i] = new Thread(() -> { for (int k = 0; k < 5000; k++) views.increment(); });
            web[i].start();
        }
        for (Thread t : web) t.join();
        System.out.println("page views: " + views.sum());
    }
}''', explain="<p><b>How it works:</b> LongAdder keeps several internal cells so threads rarely compete for the same one, and <code>sum()</code> adds them up. It's the usual choice for high-traffic counters and metrics.</p>"),
]

RACE = '''public class Main {
    static int count = 0;

    public static void main(String[] args) throws InterruptedException {
        Runnable job = () -> {
            for (int i = 0; i < 100_000; i++) {
                count++;
            }
        };
        Thread a = new Thread(job);
        Thread b = new Thread(job);
        a.start();
        b.start();
        a.join();
        b.join();
        System.out.println("expected 200000, got " + count);
    }
}'''

# ---------------- Extra blocks ----------------
BLOCKS = {
'ANIM': ANIM,
'CODE_RACE': code(RACE, skip=True),
'CODE_FIXED': code('''public class Main {
    static int count = 0;

    static synchronized void increment() {
        count++;
    }

    public static void main(String[] args) throws InterruptedException {
        Runnable job = () -> {
            for (int i = 0; i < 100_000; i++) {
                increment();
            }
        };
        Thread a = new Thread(job);
        Thread b = new Thread(job);
        a.start();
        b.start();
        a.join();
        b.join();
        System.out.println("expected 200000, got " + count);
    }
}'''),
'CODE_FORMS': snippet('''synchronized void deposit(int amt) { … }        // locks this
static synchronized void log(String s) { … }    // locks the class object (Bank.class)
synchronized (lock) { … }                       // locks the object you choose

volatile boolean running;                       // visibility only, no locking
AtomicInteger hits = new AtomicInteger();       // lock-free atomic updates
hits.incrementAndGet();'''),
'CODE_DEADLOCK': snippet('''// Thread 1                       // Thread 2
synchronized (accountA) {          synchronized (accountB) {
    synchronized (accountB) {          synchronized (accountA) {   // each waits for the
        …                                  …                       // other's lock: forever
    }                                  }
}                                  }'''),
'CODE_RUN': code(RACE.replace('count++;', 'synchronized (Main.class) {\n                    count++;\n                }').replace('expected 200000, got', 'synchronized result:'), out=None),
'RUNNER': runner([
 dict(label="1 · See the race", hint="Press <b>Run</b> several times. The total changes, and is almost never 200000. Then fix it by adding <code>synchronized (Main.class) { … }</code> around <code>count++</code>.",
      code=RACE),
 dict(label="2 · Predict: two different locks", hint="<b>Predict first:</b> is the result always 200000? Each thread locks its <i>own</i> object, so they never wait for each other. Fix: make both use one shared lock.",
      code='''public class Main {
    static int count = 0;

    public static void main(String[] args) throws InterruptedException {
        Thread a = new Thread(new Adder());
        Thread b = new Thread(new Adder());
        a.start(); b.start();
        a.join(); b.join();
        System.out.println("got " + count);
    }
}

class Adder implements Runnable {
    public void run() {
        for (int i = 0; i < 100_000; i++) {
            synchronized (this) {
                Main.count++;
            }
        }
    }
}'''),
 dict(label="3 · Predict: is ++ on volatile safe?", hint="<b>Predict first:</b> <code>volatile</code> gives visibility, but is <code>count++</code> now atomic? Run it a few times, then switch to <code>AtomicInteger</code>.",
      code='''public class Main {
    static volatile int count = 0;

    public static void main(String[] args) throws InterruptedException {
        Runnable job = () -> { for (int i = 0; i < 100_000; i++) count++; };
        Thread a = new Thread(job), b = new Thread(job);
        a.start(); b.start();
        a.join(); b.join();
        System.out.println("got " + count);
    }
}'''),
 dict(label="4 · Crash: lock is null", hint="You can't lock a <code>null</code> reference. Initialise the lock: <code>static final Object lock = new Object();</code>",
      code='''public class Main {
    static Object lock;
    static int stock = 10;

    public static void main(String[] args) {
        synchronized (lock) {
            stock--;
        }
        System.out.println("stock " + stock);
    }
}''', _expect="exception"),
 dict(label="5 · Spot the error", hint="Only objects have locks. <code>synchronized</code> needs a reference, not an <code>int</code>. Lock a dedicated object instead.",
      code='''public class Main {
    static int count = 0;

    public static void main(String[] args) {
        synchronized (count) {
            count++;
        }
        System.out.println(count);
    }
}''', _expect="compile-error"),
]),
'QUIZ': quiz([
 {"q": "Why can count++ lose updates when two threads run it?", "options": ["Java ints are 16-bit", "It is read, add, write: another thread can interleave between the steps", "The JVM skips it", "Only on one-core machines"], "answer": 1, "why": "count++ is not atomic; two threads can read the same old value."},
 {"q": "A synchronized instance method locks…", "options": ["the class", "this object", "all objects", "nothing"], "answer": 1, "why": "Instance methods use this object's monitor; static synchronized methods use the Class object."},
 {"q": "Two threads call synchronized methods on two DIFFERENT objects of the same class. They…", "options": ["block each other", "don't block each other", "deadlock", "throw an exception"], "answer": 1, "why": "Each object has its own lock."},
 {"q": "What does volatile guarantee?", "options": ["Atomic ++", "Visibility: every thread sees the latest written value", "Mutual exclusion", "Faster code"], "answer": 1, "why": "volatile is about visibility and ordering, not atomicity of compound actions."},
 {"q": "Which is lock-free and safe for a shared counter?", "options": ["int", "volatile int", "AtomicInteger", "Integer"], "answer": 2, "why": "AtomicInteger uses compare-and-swap for atomic read-modify-write."},
 {"q": "A thread waiting to enter a synchronized block held by another thread is in state…", "options": ["WAITING", "BLOCKED", "TIMED_WAITING", "NEW"], "answer": 1, "why": "BLOCKED = waiting to acquire a monitor."},
 {"q": "Thread 1 holds lock A and wants B; thread 2 holds B and wants A. This is…", "options": ["a race condition", "a deadlock", "starvation", "fine"], "answer": 1, "why": "Each waits for the other forever. Prevent it with a consistent lock order."},
 {"q": "Is a synchronized lock re-entrant (can the owner enter another block on the same lock)?", "options": ["Yes", "No, it deadlocks itself", "Only for static methods", "Only once"], "answer": 0, "why": "Java monitors are re-entrant: the owning thread can re-acquire the lock it already holds."},
]),
}
