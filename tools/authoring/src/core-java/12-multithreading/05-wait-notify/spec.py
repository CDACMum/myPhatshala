import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from mkanim import Anim, two_view
from m12 import code, snippet, runner, quiz

def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

# ---------------- Part 5: two-view animation ----------------
S = Anim("see", frames=6, h=250, label="A chef and a waiter share a one-dish counter; each waits when it can't proceed and notifies the other")
S.box(120, 60, 120, 60, None, fill="soft-blue", stroke="blue")
S.text(180, 78, "counter (1 slot)", size=9, anchor="middle", bold=True, cls="blue")
dish = {2: "dosa", 3: "dosa", 4: "idli", 6: "vada"}
for f, d in dish.items():
    S.text(180, 104, d, on=str(f), size=12, bold=True, anchor="middle", mono=True)
S.text(180, 104, "empty", on="1", size=10.5, anchor="middle", cls="ink3")
S.text(180, 104, "empty", on="5", size=10.5, anchor="middle", cls="ink3")
S.box(8, 60, 96, 60, None, fill="card2", stroke="line")
S.text(18, 78, "chef", size=10.5, bold=True)
S.box(256, 60, 96, 60, None, fill="card2", stroke="line")
S.text(266, 78, "waiter", size=10.5, bold=True)
S.text(266, 100, "empty → wait()", size=8.8, mono=True, cls="blue", on="1")
S.text(266, 114, "WAITING", size=9, mono=True, cls="blue", bold=True, on="1")
S.text(266, 100, "WAITING", size=9, mono=True, cls="blue", bold=True, on="2")
S.text(18, 100, "put dosa", size=9, mono=True, on="2")
S.text(18, 114, "notify()", size=9, mono=True, cls="green", on="2")
S.arrow(104, 118, 256, 118, on="2", color="green", bend=30)
S.text(266, 100, "took dosa", size=9, mono=True, cls="green", on="3")
S.text(18, 100, "full → wait()", size=8.8, mono=True, cls="blue", on="4")
S.text(18, 114, "WAITING", size=9, mono=True, cls="blue", bold=True, on="4")
S.text(266, 100, "took idli", size=9, mono=True, cls="green", on="5")
S.text(266, 114, "notify()", size=9, mono=True, cls="green", on="5")
S.arrow(256, 118, 104, 118, on="5", color="green", bend=-30)
S.text(18, 100, "put vada", size=9, mono=True, on="6")
S.box(8, 150, 344, 56, None, fill="board", stroke="board")
rules = {1: "while (counter empty) wait();", 2: "counter = dish; notify();", 3: "dish = counter; counter = null;",
         4: "while (counter full) wait();", 5: "take; notify();  // wake the chef", 6: "chef wakes, re-checks, puts"}
for f, r in rules.items():
    S.text(18, 182, esc(r), on=str(f), mono=True, size=9.6, cls="chalk")
S.note({1: "Nothing to serve: the waiter waits.", 2: "Chef puts a dish and notifies.", 3: "Waiter wakes and takes it.",
        4: "Counter full: the chef waits.", 5: "Waiter takes it and notifies.", 6: "Chef continues."}, y=236, size=10.5)
S.caps(["The waiter thread finds the counter empty. Instead of checking again and again, it calls <code>wait()</code> and sleeps: state <b>WAITING</b>, no CPU used.",
        "The chef thread puts a dosa on the counter and calls <code>notify()</code> to wake one waiting thread.",
        "The waiter wakes up, re-checks the condition (the counter now has food) and takes the dosa.",
        "Later the chef has an idli ready but the counter is still full, so now the <b>chef</b> waits.",
        "The waiter takes the idli and calls <code>notify()</code>, waking the chef.",
        "The chef re-checks: the counter is free, so it puts the vada. Each side waits only when it can't continue. This is the <b>producer–consumer</b> pattern."])

B = Anim("behind", frames=6, h=250, label="Inside the counter object's monitor: the owner, the entry set of blocked threads and the wait set of waiting threads")
B.box(6, 6, 348, 200, None, fill="card", stroke="line")
B.text(16, 24, "monitor of the counter object", size=10, bold=True, cls="ink2")
B.box(16, 36, 100, 70, None, fill="soft-green", stroke="green")
B.text(26, 54, "owner", size=9.5, bold=True, cls="green")
own = {1: "waiter", 2: "chef", 3: "waiter", 4: "chef", 5: "waiter", 6: "chef"}
for f, o in own.items():
    B.text(26, 80, o, on=str(f), mono=True, size=11, bold=True)
B.box(130, 36, 100, 70, None, fill="soft-acc", stroke="track")
B.text(140, 54, "entry set", size=9.5, bold=True, cls="acc")
B.text(140, 72, "(BLOCKED)", size=8.4, cls="ink3")
B.text(140, 92, "waiter", on="2", mono=True, size=10)
B.text(140, 92, "chef", on="5", mono=True, size=10)
B.box(244, 36, 100, 70, None, fill="soft-blue", stroke="blue")
B.text(254, 54, "wait set", size=9.5, bold=True, cls="blue")
B.text(254, 72, "(WAITING)", size=8.4, cls="ink3")
B.text(254, 92, "waiter", on="1", mono=True, size=10)
B.text(254, 92, "chef", on="4", mono=True, size=10)
B.arrow(244, 96, 222, 96, on="2", color="green")
B.arrow(244, 96, 222, 96, on="5", color="green")
expl = {1: "wait(): give up the lock, join the wait set", 2: "notify(): move one waiter to the entry set",
        3: "lock free: waiter re-acquires it, returns from wait()", 4: "chef calls wait(): releases the lock",
        5: "notify(): chef moves to the entry set", 6: "chef gets the lock back, loop re-checks"}
for f, e in expl.items():
    B.text(16, 136, e, on=str(f), size=9.6, cls="ink")
B.text(16, 162, "wait/notify must be called while owning", size=9.2, cls="ink2")
B.text(16, 178, "this monitor (inside synchronized)", size=9.2, cls="ink2")
B.note({1: "Waiter parks in the wait set.", 2: "Chef notifies: waiter must re-lock.", 3: "Waiter owns the lock again.",
        4: "Chef parks in the wait set.", 5: "Waiter notifies the chef.", 6: "Chef owns the lock again."}, y=236, size=10.5)
B.caps(["Every object's monitor has an owner, an <b>entry set</b> (threads BLOCKED trying to get the lock) and a <b>wait set</b> (threads that called <code>wait()</code>). Calling <code>wait()</code> <b>releases the lock</b> and puts the waiter in the wait set.",
        "Because the lock was released, the chef can enter and own it. <code>notify()</code> moves one thread from the wait set to the entry set. It doesn't run yet: the chef still owns the lock.",
        "When the chef leaves the synchronized method, the waiter re-acquires the lock and only then returns from <code>wait()</code>.",
        "Same mechanism the other way: the chef can't continue, so it waits and releases the lock.",
        "The waiter takes the dish and notifies; the chef moves to the entry set.",
        "The chef gets the lock back and, because the call sits in a <code>while</code> loop, re-checks the condition before acting. Always wait in a loop: a thread can wake up when the condition is still false."])
ANIM = two_view("wait() and notify(), both views", S, B)

# ---------------- Part 6: animated example ----------------
ANIM2_HEADING = "Watch it with an example: restaurant orders and delivery riders"
ANIM2_INTRO = "A food app's restaurant thread produces orders into a queue that holds at most 2. A rider thread takes them. BlockingQueue does all the waiting and notifying for you."
A = Anim("Orders through a BlockingQueue (capacity 2)", frames=6, h=230, label="A producer puts orders into a bounded queue and blocks when it is full; a consumer takes them and blocks when it is empty")
A.box(8, 40, 96, 70, None, fill="soft-acc", stroke="track")
A.text(18, 58, "restaurant", size=10, bold=True)
A.text(18, 76, "put()", size=9.5, mono=True)
A.box(256, 40, 96, 70, None, fill="soft-green", stroke="green")
A.text(266, 58, "rider", size=10, bold=True)
A.text(266, 76, "take()", size=9.5, mono=True)
A.box(118, 40, 124, 70, None, fill="card2", stroke="line")
A.text(180, 34, "queue (max 2)", size=9, anchor="middle", cls="ink2")
slots = {1: ["#1"], 2: ["#1", "#2"], 3: ["#1", "#2"], 4: ["#2", "#3"], 5: ["#3"], 6: []}
for f, items in slots.items():
    for i, it in enumerate(items):
        A.box(128 + i * 56, 56, 48, 38, it, on=str(f), fill="soft-blue", stroke="blue", size=11, bold=True, mono=True)
A.text(18, 98, "WAITING", on="3", size=9, mono=True, cls="red", bold=True)
A.text(266, 98, "WAITING", on="6", size=9, mono=True, cls="red", bold=True)
A.text(266, 98, "got #1", on="4", size=9, mono=True, cls="green")
A.text(266, 98, "got #2", on="5", size=9, mono=True, cls="green")
A.text(180, 140, "queue full: put() blocks", on="3", size=10.5, bold=True, anchor="middle", cls="red")
A.text(180, 140, "space freed: #3 goes in", on="4", size=10.5, bold=True, anchor="middle", cls="green")
A.text(180, 140, "queue empty: take() blocks", on="6", size=10.5, bold=True, anchor="middle", cls="red")
A.note({1: "Order #1 queued.", 2: "Order #2 queued: full.", 3: "#3 must wait for space.", 4: "Rider takes #1; #3 goes in.",
        5: "Rider takes #2.", 6: "Rider takes #3; next take waits."}, y=204, size=10.5)
A.caps(["The restaurant thread calls <code>queue.put(order1)</code>.",
        "Order #2 goes in too. The queue's capacity is 2, so it is now full.",
        "<code>put(order3)</code> can't proceed: the restaurant thread waits inside <code>put()</code> (no busy loop, no CPU). This <b>back-pressure</b> stops a fast producer from flooding memory.",
        "The rider calls <code>take()</code>, gets #1, and the queue signals the waiting producer, which adds #3.",
        "The rider takes #2.",
        "After #3 the queue is empty, so the rider's next <code>take()</code> waits until a new order arrives. Inside, BlockingQueue uses a lock and conditions: the same idea as wait/notify, already written and tested."])
ANIM2 = A

# ---------------- Part 8: tracer ----------------
TRACE = dict(code='''class Counter {
    private String dish;

    synchronized void put(String d) {
        dish = d;
        notify();
    }

    synchronized String take() throws InterruptedException {
        while (dish == null) {
            wait();
        }
        String d = dish;
        dish = null;
        return d;
    }
}

public class Main {
    public static void main(String[] args) throws InterruptedException {
        Counter counter = new Counter();
        Thread chef = new Thread(() -> {
            try { Thread.sleep(500); } catch (InterruptedException e) { return; }
            counter.put("masala dosa");
        }, "chef");
        chef.start();
        String served = counter.take();
        chef.join();
        System.out.println("waiter (main) served " + served);
    }
}
''', notes={
 21: "Shared counter :: = One Counter object on the heap, <code>dish = null</code>. Its monitor will coordinate the two threads.",
 22: "The chef :: A thread that cooks for half a second, then puts the dish.",
 26: "Start :: = The chef starts and goes to sleep (cooking).",
 27: "Take :: main (acting as the waiter) calls <code>take()</code> and takes the counter's lock.",
 10: "Check :: = The dish is still null: nothing to serve yet.",
 11: "wait() :: = main releases the lock and waits. The chef wakes after 500 ms, enters <code>put</code>, stores the dish and calls <code>notify()</code>. main re-acquires the lock and returns from <code>wait()</code>.",
 13: "Take it :: The loop checked again: the dish is there.",
 14: "Clear :: The counter is empty again, ready for the next dish.",
 28: "Join :: = The chef thread has finished.",
 29: "Served :: main got the value the chef produced."})

# ---------------- Worked examples ----------------
WORKED_INTRO = "Three coordination problems from real apps: a one-slot hand-off, waiting for a confirmation, and a message queue. Notice that every <code>wait()</code> sits inside a <code>while</code> loop and a synchronized method."
EXAMPLES = [
dict(tag="Restaurant · kitchen", title="Chef and waiter with a one-dish counter",
 problem="<p>A chef cooks 3 dishes and a waiter serves them through a counter that holds one dish. The chef must wait if the counter is full; the waiter must wait if it's empty. Print each put and take.</p>",
 inp="dishes: dosa, idli, vada",
 approach=["A <code>Counter</code> class with synchronized <code>put</code> and <code>take</code>.",
           "<code>put</code> waits while full; <code>take</code> waits while empty. Each calls <code>notifyAll()</code> after changing the counter.",
           "Print inside the synchronized methods so the order of lines is always put, take, put, take…"],
 code='''class Counter {
    private String dish;

    synchronized void put(String d) throws InterruptedException {
        while (dish != null) wait();
        dish = d;
        System.out.println("chef put " + d);
        notifyAll();
    }

    synchronized String take() throws InterruptedException {
        while (dish == null) wait();
        String d = dish;
        dish = null;
        System.out.println("waiter took " + d);
        notifyAll();
        return d;
    }
}

public class Main {
    public static void main(String[] args) throws InterruptedException {
        Counter counter = new Counter();
        String[] menu = {"dosa", "idli", "vada"};
        Thread chef = new Thread(() -> {
            try {
                for (String d : menu) counter.put(d);
            } catch (InterruptedException e) { }
        }, "chef");
        Thread waiter = new Thread(() -> {
            try {
                for (int i = 0; i < menu.length; i++) counter.take();
            } catch (InterruptedException e) { }
        }, "waiter");
        chef.start();
        waiter.start();
        chef.join();
        waiter.join();
        System.out.println("all dishes served");
    }
}
''', notes={23: "Shared counter :: One Counter object; both threads will use its monitor.",
            25: "Chef :: The producer thread: three <code>put</code> calls.",
            30: "Waiter :: The consumer thread: three <code>take</code> calls.",
            35: "Start chef :: = The chef puts dosa. Its next put finds the counter full and waits.",
            36: "Start waiter :: = The waiter takes dosa and notifies the chef, and so on: put and take strictly alternate.",
            38: "Both done :: = Three puts and three takes have happened.",
            39: "Finish :: Same six lines, same order, every run."},
 tryit="Press <b>Run</b>. Then change both <code>while</code> to <code>if</code>; with one chef and one waiter it still works, but add a second waiter thread and it can break. That's why the rule is “always wait in a loop”."),
dict(tag="Payments · confirmation", title="Wait until the gateway confirms",
 problem="<p>After a customer pays, the order thread must not ship until the payment gateway confirms. The gateway runs on its own thread and confirms after a short delay. Use a lock object, a flag, <code>wait()</code> and <code>notifyAll()</code>.</p>",
 inp="payment id PAY-551; gateway answers after 100 ms",
 approach=["A small <code>Payment</code> class with a <code>confirmed</code> flag.",
           "<code>awaitConfirmation()</code> waits in a loop while the flag is false.",
           "<code>confirm()</code> sets the flag and calls <code>notifyAll()</code>."],
 code='''class Payment {
    private boolean confirmed = false;

    synchronized void confirm() {
        confirmed = true;
        notifyAll();
    }

    synchronized void awaitConfirmation() throws InterruptedException {
        while (!confirmed) {
            wait();
        }
    }
}

public class Main {
    public static void main(String[] args) throws InterruptedException {
        Payment pay = new Payment();
        Thread gateway = new Thread(() -> {
            try { Thread.sleep(100); } catch (InterruptedException e) { return; }
            System.out.println("gateway: PAY-551 confirmed");
            pay.confirm();
        }, "gateway");
        gateway.start();
        System.out.println("order: waiting for payment");
        pay.awaitConfirmation();
        System.out.println("order: shipping now");
        gateway.join();
    }
}
''', notes={18: "Payment object :: <code>confirmed</code> starts false.",
            19: "Gateway :: A thread that answers after 100 ms.",
            24: "Start :: = The gateway is busy (sleeping) for now.",
            25: "Message :: main announces it's waiting.",
            26: "Wait :: = main waits inside <code>awaitConfirmation()</code>, releasing the lock. The gateway confirms and notifies; main re-checks the flag and returns.",
            27: "Ship :: This line can only run after the confirmation.",
            28: "Tidy up :: Wait for the gateway thread to end."},
 tryit="Press <b>Run</b>. Then change <code>wait()</code> to <code>wait(50)</code>: the loop wakes every 50 ms, re-checks, and keeps waiting, so the result is the same. Timed waits are useful as a safety net."),
dict(tag="Messaging · SMS", title="An SMS dispatcher with a BlockingQueue",
 problem="<p>A notification service queues SMS messages; a dispatcher thread sends them one by one. To shut down, the producer puts a special <b>STOP</b> message (a “poison pill”). Use <code>ArrayBlockingQueue</code> instead of writing wait/notify yourself.</p>",
 inp="messages: OTP 4821, Order shipped, Refund done, then STOP",
 approach=["Create an <code>ArrayBlockingQueue&lt;String&gt;</code> with capacity 2.",
           "The dispatcher loops on <code>take()</code> and stops when it receives STOP.",
           "main <code>put</code>s the messages and then STOP, and joins the dispatcher."],
 code='''import java.util.concurrent.*;

public class Main {
    public static void main(String[] args) throws InterruptedException {
        BlockingQueue<String> outbox = new ArrayBlockingQueue<>(2);
        Thread dispatcher = new Thread(() -> {
            try {
                while (true) {
                    String sms = outbox.take();
                    if (sms.equals("STOP")) break;
                    System.out.println("sent: " + sms);
                }
            } catch (InterruptedException e) { }
            System.out.println("dispatcher stopped");
        }, "dispatcher");
        dispatcher.start();
        outbox.put("OTP 4821");
        outbox.put("Order shipped");
        outbox.put("Refund done");
        outbox.put("STOP");
        dispatcher.join();
    }
}
''', notes={5: "Queue :: = An ArrayBlockingQueue with room for 2 messages. It has its own internal lock and two conditions (not empty, not full).",
            6: "Dispatcher :: The consumer thread.",
            16: "Start :: = The dispatcher calls <code>take()</code> on an empty queue and waits.",
            17: "Put 1 :: = The OTP goes in; the dispatcher wakes and sends it.",
            19: "Put 3 :: = If the queue is full at this moment, <code>put</code> makes main wait until there's room.",
            20: "Poison pill :: = STOP tells the dispatcher to leave its loop.",
            21: "Join :: = All three messages are sent and the dispatcher has stopped."},
 tryit="Press <b>Run</b>. Then add five more messages before STOP: with capacity 2, main regularly waits inside <code>put</code>, yet nothing is lost and the order is kept."),
]

# ---------------- Practice problems ----------------
PRACTICE_INTRO = "Coordinate threads with <code>wait</code>/<code>notifyAll</code>, then with the ready-made tools in <code>java.util.concurrent</code>. Outputs are fixed because every print happens in a guaranteed order. The last three are business tasks."
PROBLEMS = [
dict(level="easy", title="wait() outside synchronized", stmt="<p>Call <code>wait()</code> on an object without holding its lock, catch the exception and print it.</p>", inp="(none)",
 code='''public class Main {
    public static void main(String[] args) throws InterruptedException {
        Object lock = new Object();
        try {
            lock.wait();
        } catch (IllegalMonitorStateException e) {
            System.out.println("error: " + e.getMessage());
        }
    }
}''', explain="<p><b>How it works:</b> <code>wait</code>, <code>notify</code> and <code>notifyAll</code> must be called by the thread that owns the object's monitor, i.e. inside <code>synchronized (lock)</code>. Otherwise the JVM throws <code>IllegalMonitorStateException</code>.</p>"),
dict(level="easy", title="Wake a waiting thread", stmt="<p>A thread waits until <code>ready</code> becomes true. main sets it and calls <code>notifyAll()</code>. The thread then prints <code>got the signal</code>.</p>", inp="(none)",
 code='''public class Main {
    static boolean ready = false;
    static final Object LOCK = new Object();

    public static void main(String[] args) throws InterruptedException {
        Thread t = new Thread(() -> {
            synchronized (LOCK) {
                while (!ready) {
                    try { LOCK.wait(); } catch (InterruptedException e) { return; }
                }
                System.out.println("got the signal");
            }
        });
        t.start();
        synchronized (LOCK) {
            ready = true;
            LOCK.notifyAll();
        }
        t.join();
    }
}''', explain="<p><b>How it works:</b> the flag makes it safe even if main signals <i>before</i> the thread starts waiting: the thread checks <code>ready</code> first and doesn't wait at all. A notify with no flag would be lost.</p>"),
dict(level="easy", title="A bounded queue refuses extras", stmt="<p>Create an <code>ArrayBlockingQueue</code> of capacity 2, <code>offer</code> three items, and print the results and the queue.</p>", inp="a, b, c",
 code='''import java.util.concurrent.ArrayBlockingQueue;

public class Main {
    public static void main(String[] args) {
        ArrayBlockingQueue<String> q = new ArrayBlockingQueue<>(2);
        System.out.println(q.offer("a") + " " + q.offer("b") + " " + q.offer("c"));
        System.out.println(q);
    }
}''', explain="<p><b>How it works:</b> <code>offer</code> returns false at once when full; <code>put</code> would wait instead; <code>add</code> would throw. Pick the method that matches what should happen when the system is overloaded.</p>"),
dict(level="medium", title="Ping-pong in turns", stmt="<p>Two threads print <code>ping</code> and <code>pong</code> alternately, 3 times each, starting with ping. Use a shared turn flag with wait/notifyAll.</p>", inp="(none)",
 code='''public class Main {
    static boolean pingTurn = true;
    static final Object LOCK = new Object();

    static void play(String word, boolean mine, int times) {
        for (int i = 0; i < times; i++) {
            synchronized (LOCK) {
                while (pingTurn != mine) {
                    try { LOCK.wait(); } catch (InterruptedException e) { return; }
                }
                System.out.println(word);
                pingTurn = !pingTurn;
                LOCK.notifyAll();
            }
        }
    }

    public static void main(String[] args) throws InterruptedException {
        Thread ping = new Thread(() -> play("ping", true, 3));
        Thread pong = new Thread(() -> play("pong", false, 3));
        pong.start();
        ping.start();
        ping.join();
        pong.join();
    }
}''', explain="<p><b>How it works:</b> each thread waits until it's its turn, prints, flips the flag and wakes the other. Even though pong starts first, it waits for ping.</p>"),
dict(level="medium", title="notifyAll wakes everyone", stmt="<p>Three threads wait for a <code>gateOpen</code> flag. main opens the gate with one <code>notifyAll()</code>. Count how many threads passed.</p>", inp="3 waiting threads",
 code='''import java.util.concurrent.atomic.AtomicInteger;

public class Main {
    static boolean gateOpen = false;
    static final Object GATE = new Object();

    public static void main(String[] args) throws InterruptedException {
        AtomicInteger passed = new AtomicInteger();
        Thread[] fans = new Thread[3];
        for (int i = 0; i < 3; i++) {
            fans[i] = new Thread(() -> {
                synchronized (GATE) {
                    while (!gateOpen) {
                        try { GATE.wait(); } catch (InterruptedException e) { return; }
                    }
                }
                passed.incrementAndGet();
            });
            fans[i].start();
        }
        synchronized (GATE) {
            gateOpen = true;
            GATE.notifyAll();
        }
        for (Thread f : fans) f.join();
        System.out.println("fans through the gate: " + passed.get());
    }
}''', explain="<p><b>How it works:</b> <code>notify()</code> wakes only one waiting thread; <code>notifyAll()</code> wakes all, and each re-checks the condition. When several threads may be waiting, notifyAll is the safe default.</p>"),
dict(level="medium", title="Wait for three services with CountDownLatch", stmt="<p>An app starts only when the database, cache and payment services are ready. Each starts on its own thread and counts down a latch. main waits on the latch.</p>", inp="3 services",
 code='''import java.util.concurrent.CountDownLatch;

public class Main {
    public static void main(String[] args) throws InterruptedException {
        String[] services = {"database", "cache", "payments"};
        CountDownLatch ready = new CountDownLatch(services.length);
        for (String s : services) {
            new Thread(() -> ready.countDown(), s).start();
        }
        ready.await();
        System.out.println("all " + services.length + " services ready, latch = " + ready.getCount());
    }
}''', explain="<p><b>How it works:</b> <code>await()</code> waits until the count reaches 0. It's a ready-made “wait until N things have happened”, built on the same waiting machinery as wait/notify.</p>"),
dict(level="business", title="Odd and even invoice numbers", stmt="<p>Two printers share the invoice numbers 1–10: one prints odd numbers, the other even, strictly in order. Use wait/notifyAll on a shared counter.</p>", inp="1..10",
 code='''public class Main {
    static int next = 1;
    static final Object LOCK = new Object();

    static void printer(String name, int parity) {
        while (true) {
            synchronized (LOCK) {
                while (next <= 10 && next % 2 != parity) {
                    try { LOCK.wait(); } catch (InterruptedException e) { return; }
                }
                if (next > 10) {
                    LOCK.notifyAll();
                    return;
                }
                System.out.println(name + ": INV-" + next);
                next++;
                LOCK.notifyAll();
            }
        }
    }

    public static void main(String[] args) throws InterruptedException {
        Thread odd = new Thread(() -> printer("printer-A", 1));
        Thread even = new Thread(() -> printer("printer-B", 0));
        odd.start();
        even.start();
        odd.join();
        even.join();
    }
}''', explain="<p><b>How it works:</b> each printer waits until the next number has its parity. The <code>next &gt; 10</code> check lets both threads finish; without the final notifyAll one of them could wait forever.</p>"),
dict(level="business", title="Order pipeline with a BlockingQueue", stmt="<p>A restaurant thread produces 5 orders with ids 101–105 into a queue of capacity 2. A rider thread takes exactly 5 orders and adds up their bill amounts (id × 2). Print the total.</p>", inp="orders 101..105",
 code='''import java.util.concurrent.*;

public class Main {
    public static void main(String[] args) throws InterruptedException {
        BlockingQueue<Integer> orders = new ArrayBlockingQueue<>(2);
        int[] total = {0};
        Thread restaurant = new Thread(() -> {
            try {
                for (int id = 101; id <= 105; id++) orders.put(id);
            } catch (InterruptedException e) { }
        });
        Thread rider = new Thread(() -> {
            try {
                for (int i = 0; i < 5; i++) total[0] += orders.take() * 2;
            } catch (InterruptedException e) { }
        });
        restaurant.start();
        rider.start();
        restaurant.join();
        rider.join();
        System.out.println("delivered 5 orders, bills total Rs " + total[0]);
    }
}''', explain="<p><b>How it works:</b> the queue's capacity limits how far the restaurant can get ahead of the rider. <code>total</code> is written only by the rider and read after <code>join()</code>, so no lock is needed for it.</p>"),
dict(level="business", title="Seat hold that expires", stmt="<p>A cinema holds a seat while the customer pays, but for at most 200 ms. The payment never arrives. Use <code>wait(timeout)</code> in a loop with a deadline, then release the seat.</p>", inp="hold 200 ms, no payment",
 code='''public class Main {
    static boolean paid = false;
    static final Object LOCK = new Object();

    public static void main(String[] args) throws InterruptedException {
        long deadline = System.currentTimeMillis() + 200;
        synchronized (LOCK) {
            long left;
            while (!paid && (left = deadline - System.currentTimeMillis()) > 0) {
                LOCK.wait(left);
            }
            System.out.println(paid ? "seat confirmed" : "hold expired, seat released");
        }
    }
}''', explain="<p><b>How it works:</b> <code>wait(ms)</code> returns on notify, on timeout, or spuriously, so the loop recomputes the time left and re-checks the flag. This is the correct pattern for “wait for a condition, but not forever”.</p>"),
]

# ---------------- Extra blocks ----------------
KITCHEN = '''class Counter {
    private String dish;

    synchronized void put(String d) throws InterruptedException {
        while (dish != null) wait();
        dish = d;
        System.out.println("chef put " + d);
        notifyAll();
    }

    synchronized String take() throws InterruptedException {
        while (dish == null) wait();
        String d = dish;
        dish = null;
        System.out.println("waiter took " + d);
        notifyAll();
        return d;
    }
}

public class Main {
    public static void main(String[] args) throws InterruptedException {
        Counter counter = new Counter();
        Thread chef = new Thread(() -> {
            try {
                for (String d : new String[]{"dosa", "idli", "vada", "upma"}) counter.put(d);
            } catch (InterruptedException e) { }
        });
        Thread waiter = new Thread(() -> {
            try {
                for (int i = 0; i < 4; i++) counter.take();
            } catch (InterruptedException e) { }
        });
        chef.start();
        waiter.start();
        chef.join();
        waiter.join();
    }
}'''
BLOCKS = {
'ANIM': ANIM,
'CODE_PATTERN': snippet('''synchronized (lock) {
    while (!condition) {      // ALWAYS a loop, never just "if"
        lock.wait();          // releases lock, waits, re-acquires before returning
    }
    // condition is true and we hold the lock: act on it
}

synchronized (lock) {
    changeTheCondition();
    lock.notifyAll();         // wake the waiters so they re-check
}'''),
'CODE_IMSE': code('''public class Main {
    public static void main(String[] args) {
        Object lock = new Object();
        try {
            lock.notify();
        } catch (IllegalMonitorStateException e) {
            System.out.println(e);
        }
    }
}'''),
'CODE_RUN': code(KITCHEN),
'RUNNER': runner([
 dict(label="1 · Chef and waiter", hint="Press <b>Run</b>: put and take always alternate. Then remove both <code>notifyAll()</code> calls and run again: both threads wait forever (the runner will time out).",
      code=KITCHEN),
 dict(label="2 · Predict: does wait() release the lock?", hint="<b>Predict first:</b> the helper waits <i>inside</i> a synchronized block. Can main enter a block on the same lock while it waits?",
      code='''public class Main {
    static final Object LOCK = new Object();

    public static void main(String[] args) throws InterruptedException {
        Thread helper = new Thread(() -> {
            synchronized (LOCK) {
                try { LOCK.wait(); } catch (InterruptedException e) { }
                System.out.println("helper: woken up");
            }
        });
        helper.start();
        while (helper.getState() != Thread.State.WAITING) Thread.onSpinWait();
        synchronized (LOCK) {
            System.out.println("main: I got the lock while helper waits");
            LOCK.notifyAll();
        }
        helper.join();
    }
}'''),
 dict(label="3 · Predict: a notify nobody heard", hint="<b>Predict first:</b> main notifies <i>before</i> the helper waits. How long does the helper wait? Then fix it with a boolean flag checked in a while loop.",
      code='''public class Main {
    static final Object LOCK = new Object();

    public static void main(String[] args) throws InterruptedException {
        synchronized (LOCK) {
            LOCK.notifyAll();
            System.out.println("main: signal sent");
        }
        Thread helper = new Thread(() -> {
            long t0 = System.currentTimeMillis();
            synchronized (LOCK) {
                try { LOCK.wait(1000); } catch (InterruptedException e) { }
            }
            System.out.println("helper waited about " + (System.currentTimeMillis() - t0) / 100 * 100 + " ms");
        });
        helper.start();
        helper.join();
    }
}'''),
 dict(label="4 · Crash: notify without the lock", hint="<code>notifyAll()</code> must be called while holding the lock. Wrap it in <code>synchronized (LOCK) { … }</code>.",
      code='''public class Main {
    static final Object LOCK = new Object();
    static boolean ready = false;

    public static void main(String[] args) {
        ready = true;
        LOCK.notifyAll();
        System.out.println("signalled");
    }
}''', _expect="exception"),
 dict(label="5 · Spot the error", hint="<code>wait()</code> throws the checked <code>InterruptedException</code>. Declare it with <code>throws</code> or catch it.",
      code='''public class Main {
    static final Object LOCK = new Object();

    public static void main(String[] args) {
        synchronized (LOCK) {
            LOCK.wait(100);
        }
        System.out.println("done waiting");
    }
}''', _expect="compile-error"),
]),
'QUIZ': quiz([
 {"q": "wait(), notify() and notifyAll() are methods of…", "options": ["Thread", "Object", "Runnable", "System"], "answer": 1, "why": "Every object has a monitor, so the methods are in Object."},
 {"q": "What happens to the lock when a thread calls wait()?", "options": ["It keeps it", "It releases it, and re-acquires it before wait() returns", "It's destroyed", "It passes to main"], "answer": 1, "why": "That's the key difference from sleep(), which keeps any locks."},
 {"q": "Calling notify() without holding the object's lock throws…", "options": ["InterruptedException", "IllegalMonitorStateException", "NullPointerException", "Nothing"], "answer": 1, "why": "The calling thread must own the monitor."},
 {"q": "Why must wait() be called in a while loop?", "options": ["Style only", "The thread may wake when the condition is still false (spurious wakeup or another thread got there first)", "It's faster", "Java requires it at compile time"], "answer": 1, "why": "Always re-check the condition after waking."},
 {"q": "notify() vs notifyAll()?", "options": ["Same thing", "notify wakes one waiting thread; notifyAll wakes all of them", "notifyAll is deprecated", "notify wakes all"], "answer": 1, "why": "With several waiters for different conditions, notifyAll is safer."},
 {"q": "After notify(), when does the woken thread continue?", "options": ["Immediately", "After the notifying thread releases the lock and the woken thread re-acquires it", "Never", "After 1 second"], "answer": 1, "why": "It moves to the entry set and must win the lock first."},
 {"q": "A thread inside wait() (no timeout) is in state…", "options": ["BLOCKED", "WAITING", "TIMED_WAITING", "RUNNABLE"], "answer": 1, "why": "Untimed wait = WAITING; wait(ms) = TIMED_WAITING."},
 {"q": "Which class gives producer–consumer without writing wait/notify?", "options": ["ArrayList", "ArrayBlockingQueue", "HashMap", "StringBuilder"], "answer": 1, "why": "put() waits when full and take() waits when empty."},
]),
}
