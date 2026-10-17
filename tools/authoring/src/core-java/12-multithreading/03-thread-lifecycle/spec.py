import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from mkanim import Anim, two_view
from m12 import code, snippet, runner, quiz

def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

# ---------------- Part 5: two-view animation ----------------
CODE = ["Thread t = new Thread(task);", "t.start();", "Thread.sleep(500);      // in task",
        "synchronized (lock) {…}  // lock busy", "other.join();           // in task", "// run() returns"]
STATE = ["NEW", "RUNNABLE", "TIMED_WAITING", "BLOCKED", "WAITING", "TERMINATED"]
S = Anim("see", frames=6, h=250, label="The code a thread runs and the state it is in at each moment")
S.box(8, 8, 344, 136, None, fill="board", stroke="board")
for i, l in enumerate(CODE):
    S.text(18, 30 + i * 21, esc(l), mono=True, size=9.4, cls="chalk")
    S.box(12, 16 + i * 21, 336, 20, None, fill="none", stroke="track", on=str(i + 1), rx=4)
S.text(10, 172, "state of t:", size=10.5, bold=True, cls="ink2")
cls = ["ink2", "green", "acc", "red", "blue", "ink3"]
for i, st in enumerate(STATE):
    S.text(96, 173, st, on=str(i + 1), mono=True, size=13, bold=True, cls=cls[i])
S.text(10, 200, "t.getState() returns this value", size=9.5, cls="ink3")
S.note({1: "Created, not started.", 2: "Running or ready to run.", 3: "Sleeping for a set time.",
        4: "Waiting to enter a lock.", 5: "Waiting with no time limit.", 6: "Finished for good."}, y=234, size=10.5)
S.caps(["<code>new Thread(task)</code> gives a thread in state <b>NEW</b>: an object, not yet running.",
        "After <code>start()</code> it is <b>RUNNABLE</b>: either running on a core, or ready and waiting for the scheduler to give it one. Java uses one state for both.",
        "<code>Thread.sleep(500)</code> puts it in <b>TIMED_WAITING</b>: it uses no CPU and wakes up by itself after the time is up (or when interrupted).",
        "If it reaches a <code>synchronized</code> block whose lock another thread holds, it is <b>BLOCKED</b> until the lock is free (Lesson 12.4).",
        "<code>join()</code> or <code>wait()</code> without a time limit puts it in <b>WAITING</b>: it needs another thread to finish or to notify it (Lesson 12.5).",
        "When <code>run()</code> returns or throws, the thread is <b>TERMINATED</b>. It can never run again."])

B = Anim("behind", frames=6, h=250, label="The six states of java.lang.Thread.State and the transitions between them")
pos = {"NEW": (8, 40, 70), "RUNNABLE": (122, 40, 112), "TERMINATED": (270, 40, 84),
       "TIMED_WAITING": (8, 150, 112), "BLOCKED": (128, 150, 96), "WAITING": (232, 150, 90)}
for k, (x, y, w) in pos.items():
    B.box(x, y, w, 32, k, fill="card", stroke="line", size=8.8, mono=True, bold=True)
for i, st in enumerate(STATE):
    x, y, w = pos[st]
    B.box(x, y, w, 32, st, fill="soft-green", stroke="green", size=8.8, mono=True, bold=True, on=str(i + 1), sw=2.2)
B.arrow(80, 56, 120, 56, color="ink", on="2-")
B.text(84, 48, "start()", size=8, cls="ink3", on="2-")
B.arrow(236, 56, 268, 56, color="ink", on="6")
B.arrow(150, 74, 70, 148, color="acc", on="3", sw=1.6)
B.arrow(178, 74, 178, 148, color="red", on="4", sw=1.6)
B.arrow(206, 74, 270, 148, color="blue", on="5", sw=1.6)
B.text(12, 112, "sleep(ms), join(ms)", size=8.5, cls="acc", on="3")
B.text(186, 112, "lock busy", size=8.5, cls="red", on="4")
B.text(232, 112, "join(), wait()", size=8.5, cls="blue", on="5")
B.text(8, 212, "time up / interrupt → back to RUNNABLE", size=9, cls="ink2", on="3")
B.text(8, 212, "lock released → back to RUNNABLE", size=9, cls="ink2", on="4")
B.text(8, 212, "other thread ends / notify → RUNNABLE", size=9, cls="ink2", on="5")
B.text(8, 212, "no way back from TERMINATED", size=9, cls="ink2", on="6")
B.text(8, 20, "enum Thread.State", size=10, bold=True, cls="ink2")
B.note({1: "Only an object.", 2: "In the scheduler's hands.", 3: "Parked with a timer.",
        4: "Queued for a lock.", 5: "Parked until someone acts.", 6: "Done."}, y=236, size=10.5)
B.caps(["The six values of the enum <code>Thread.State</code>. A brand-new Thread is <b>NEW</b>.",
        "<code>start()</code> is the only way out of NEW. RUNNABLE means the OS may run it whenever a core is free.",
        "Timed waits (<code>sleep</code>, <code>join(ms)</code>, <code>wait(ms)</code>) go to TIMED_WAITING and come back on their own.",
        "Trying to enter a <code>synchronized</code> block held by another thread: BLOCKED. It returns when the lock is released.",
        "Untimed waits (<code>join()</code>, <code>wait()</code>) go to WAITING and need another thread to act.",
        "From RUNNABLE, a finished <code>run()</code> leads to TERMINATED. There is no arrow back: calling <code>start()</code> again throws <code>IllegalThreadStateException</code>."])
ANIM = two_view("The life of a thread", S, B)

# ---------------- Part 6: animated example ----------------
ANIM2_HEADING = "Watch it with an example: a payment-status poller the user can cancel"
ANIM2_INTRO = "After a UPI payment, the app checks the bank every 2 seconds until the status is final. If the user taps Cancel, main interrupts the poller."
A = Anim("Payment poller: sleep, wake, interrupt", frames=6, h=230, label="A poller thread alternates between RUNNABLE and TIMED_WAITING and ends when interrupted")
A.box(10, 14, 150, 66, None, fill="soft-blue", stroke="blue")
A.text(20, 32, "Thread \"poller\"", size=9.5, bold=True, mono=True)
st = {1: ("NEW", "ink2"), 2: ("RUNNABLE", "green"), 3: ("TIMED_WAITING", "acc"), 4: ("RUNNABLE", "green"),
      5: ("TIMED_WAITING", "acc"), 6: ("TERMINATED", "ink3")}
for f, (s, c) in st.items():
    A.text(20, 54, s, on=str(f), mono=True, size=11, bold=True, cls=c)
A.text(20, 72, "woken by interrupt", on="6", size=9, cls="red")
A.box(170, 14, 184, 120, None, fill="board", stroke="board")
for i, l in enumerate(["while (true) {", "  check(bank);", "  Thread.sleep(2000);", "}", "catch (InterruptedException e)", "  stop polling"]):
    A.text(178, 32 + i * 18, esc(l), mono=True, size=8.4, cls="chalk")
hl = {2: 1, 3: 2, 4: 1, 5: 2, 6: 5}
for f, r in hl.items():
    A.box(173, 18 + r * 18, 178, 18, None, fill="none", stroke="track", on=str(f), rx=3)
A.text(10, 108, "bank says:", size=9.5, cls="ink2", on="2-")
A.text(80, 108, "PENDING", size=10, bold=True, mono=True, cls="acc", on="2-5")
A.text(10, 128, "user taps Cancel →", size=9.5, bold=True, cls="red", on="5-")
A.text(10, 146, "main: poller.interrupt()", size=9.5, mono=True, cls="red", on="5-")
A.text(10, 164, "poller woke up early and stopped", size=9.5, cls="green", on="6")
A.note({1: "Poller created.", 2: "Asks the bank: pending.", 3: "Sleeps 2 s, no CPU used.", 4: "Wakes, asks again.",
        5: "User cancels: interrupt.", 6: "sleep throws; thread ends."}, y=204, size=10.5)
A.caps(["main creates the poller thread: <b>NEW</b>.",
        "After <code>start()</code> it is RUNNABLE and calls the bank: still PENDING.",
        "<code>Thread.sleep(2000)</code>: <b>TIMED_WAITING</b>. The thread uses no CPU while sleeping.",
        "Time's up: back to RUNNABLE, and it asks again.",
        "The user taps Cancel. main calls <code>poller.interrupt()</code>, which sets the poller's interrupted flag.",
        "A sleeping thread that is interrupted wakes at once with <code>InterruptedException</code>. The catch block stops the loop, <code>run()</code> returns, and the poller is TERMINATED. Interrupt is a polite request, not a kill switch."])
ANIM2 = A

# ---------------- Part 8: tracer ----------------
TRACE = dict(code='''public class Main {
    public static void main(String[] args) throws InterruptedException {
        Thread poller = new Thread(() -> {
            try {
                Thread.sleep(60_000);
            } catch (InterruptedException e) {
                System.out.println("poller: woke early, stopping");
            }
        }, "poller");
        Thread.State before = poller.getState();
        poller.start();
        poller.interrupt();
        poller.join();
        System.out.println(before + " -> " + poller.getState() + ", alive " + poller.isAlive());
    }
}
''', notes={
 3: "Create :: = A Thread object named \"poller\" is created. Its task would sleep for a whole minute.",
 10: "NEW :: = <code>getState()</code> returns the enum value NEW: the thread exists only as an object.",
 11: "Start :: = The poller thread starts. Its state becomes RUNNABLE, then TIMED_WAITING once it reaches <code>sleep</code>.",
 12: "Interrupt :: = <code>interrupt()</code> sets the poller's interrupted flag. If it is already asleep it wakes up at once; if it hasn't reached <code>sleep</code> yet, <code>sleep</code> will throw immediately. Either way it doesn't sleep a minute.",
 13: "Join :: = main waits (state WAITING) until the poller has printed its message and ended. Now it is TERMINATED.",
 14: "Print :: Before start it was NEW; now it is TERMINATED and <code>isAlive()</code> is false."})

# ---------------- Worked examples ----------------
WORKED_INTRO = "Three lifecycle tools you'll use constantly: <code>sleep</code> for pauses, <code>interrupt</code> for cancelling, and <code>join(ms)</code> for waiting with a time limit. The traces follow main and show the worker's state on the heap."
EXAMPLES = [
dict(tag="Food delivery · tracking", title="Order status ticks with sleep()",
 problem="<p>A delivery tracker moves an order through three statuses, pausing between updates. Run the updates on a <code>tracker</code> thread with <code>Thread.sleep(50)</code> between them. Main waits and then confirms the tracker has ended.</p>",
 inp="statuses: PLACED, COOKING, OUT FOR DELIVERY",
 approach=["The tracker loops over the statuses, printing each and sleeping in between.",
           "<code>sleep</code> throws a checked exception, so catch it inside the lambda.",
           "main joins, then checks <code>getState()</code> and <code>isAlive()</code>."],
 code='''public class Main {
    public static void main(String[] args) throws InterruptedException {
        String[] steps = {"PLACED", "COOKING", "OUT FOR DELIVERY"};
        Thread tracker = new Thread(() -> {
            for (String s : steps) {
                System.out.println("Order #88: " + s);
                try {
                    Thread.sleep(50);
                } catch (InterruptedException e) {
                    return;
                }
            }
        }, "tracker");
        tracker.start();
        tracker.join();
        System.out.println("tracker " + tracker.getState() + ", alive " + tracker.isAlive());
    }
}
''', notes={3: "Statuses :: The array the tracker will walk through.",
            4: "Create :: The tracker Thread object, state NEW.",
            14: "Start :: = The tracker starts. For the next 150 ms it alternates between RUNNABLE (printing) and TIMED_WAITING (sleeping).",
            15: "Join :: = main is WAITING until the tracker's <code>run()</code> returns.",
            16: "Check :: The tracker is TERMINATED and no longer alive."},
 tryit="Press <b>Run</b>. Then change the sleep to 500 ms and watch the updates appear slowly, one by one."),
dict(tag="Analytics · reports", title="Cancel a slow report with interrupt()",
 problem="<p>A report job processes rows, pausing after each one (simulating slow disk reads). The user cancels right away. The job must notice the interrupt, stop cleanly, and say how many rows it finished.</p>",
 inp="rows 1..5, cancel immediately",
 approach=["The worker processes a row, then sleeps 1 second.",
           "main calls <code>interrupt()</code> straight after <code>start()</code>.",
           "The sleep throws <code>InterruptedException</code>; the catch reports progress and returns."],
 code='''public class Main {
    static int done = 0;

    public static void main(String[] args) throws InterruptedException {
        Thread report = new Thread(() -> {
            for (int row = 1; row <= 5; row++) {
                done++;
                try {
                    Thread.sleep(1000);
                } catch (InterruptedException e) {
                    System.out.println("cancelled after " + done + " row(s)");
                    return;
                }
            }
            System.out.println("report finished");
        }, "report");
        report.start();
        report.interrupt();
        report.join();
        System.out.println("report state: " + report.getState());
    }
}
''', notes={5: "Create :: The report thread, NEW.",
            17: "Start :: = The report thread starts and processes row 1.",
            18: "Interrupt :: = main sets the report thread's interrupted flag. The first <code>sleep</code> sees it and throws at once, whether it was already sleeping or not.",
            19: "Join :: = main waits. The worker printed the cancel message and returned.",
            20: "Done :: The report thread is TERMINATED, after one row instead of five seconds of work."},
 tryit="Press <b>Run</b>. Then remove the <code>report.interrupt()</code> line: the job takes about five seconds and prints “report finished”."),
dict(tag="Banking · timeouts", title="Wait at most 100 ms for a slow bank API",
 problem="<p>A balance check calls a bank API that sometimes hangs. main waits for it with <code>join(100)</code>. If it hasn't finished by then, main reports a timeout, cancels the call with <code>interrupt()</code>, and shows a cached balance.</p>",
 inp="cached balance Rs 12,400; the API hangs",
 approach=["The API thread sleeps 60 s to simulate a hung call.",
           "<code>join(100)</code> returns after at most 100 ms, finished or not.",
           "Check <code>isAlive()</code>: if still alive, interrupt it and use the cached value."],
 code='''public class Main {
    public static void main(String[] args) throws InterruptedException {
        Thread api = new Thread(() -> {
            try {
                Thread.sleep(60_000);
            } catch (InterruptedException e) {
                System.out.println("api call cancelled");
            }
        }, "bank-api");
        api.start();
        api.join(100);
        if (api.isAlive()) {
            System.out.println("timeout: bank-api is " + api.getState());
            api.interrupt();
            api.join();
            System.out.println("showing cached balance Rs 12,400");
        }
    }
}
''', notes={3: "Create :: A thread that simulates a call that hangs for a minute.",
            10: "Start :: = The API thread starts and soon sleeps (TIMED_WAITING).",
            11: "Timed join :: = main waits at most 100 ms. The API thread is still sleeping, so <code>join</code> simply returns.",
            12: "Still alive? :: <code>isAlive()</code> is true: the call hasn't finished.",
            13: "Report :: The API thread is TIMED_WAITING (inside its long sleep).",
            14: "Cancel :: = main interrupts it; the sleep throws and the thread prints its message.",
            15: "Wait to end :: = A plain <code>join()</code> waits for the cancelled thread to finish cleanly.",
            16: "Fallback :: The app shows the cached balance instead of hanging."},
 tryit="Press <b>Run</b>. Then make the API sleep only 20 ms: <code>join(100)</code> returns early, <code>isAlive()</code> is false, and nothing is printed by main."),
]

# ---------------- Practice problems ----------------
PRACTICE_INTRO = "Observe states, pause with <code>sleep</code>, wait with <code>join</code>, and cancel with <code>interrupt</code>. Every output is fixed. The last three are business tasks."
PROBLEMS = [
dict(level="easy", title="State before and after", stmt="<p>Print a thread's state before <code>start()</code> and after <code>join()</code>.</p>", inp="(none)",
 code='''public class Main {
    public static void main(String[] args) throws InterruptedException {
        Thread t = new Thread(() -> {});
        System.out.println("before: " + t.getState());
        t.start();
        t.join();
        System.out.println("after: " + t.getState());
    }
}''', explain="<p><b>How it works:</b> NEW until <code>start()</code>; after <code>join()</code> returns the thread is certainly TERMINATED. Any state in between depends on timing.</p>"),
dict(level="easy", title="isAlive()", stmt="<p>Print <code>isAlive()</code> before starting a thread and after it has finished.</p>", inp="(none)",
 code='''public class Main {
    public static void main(String[] args) throws InterruptedException {
        Thread t = new Thread(() -> System.out.println("working"));
        System.out.println("alive before start: " + t.isAlive());
        t.start();
        t.join();
        System.out.println("alive after join: " + t.isAlive());
    }
}''', explain="<p><b>How it works:</b> a thread is alive from <code>start()</code> until it terminates. NEW and TERMINATED threads are not alive.</p>"),
dict(level="easy", title="Countdown with sleep", stmt="<p>Print 3, 2, 1, Go! with a 100 ms pause between numbers, on the main thread.</p>", inp="(none)",
 code='''public class Main {
    public static void main(String[] args) throws InterruptedException {
        for (int i = 3; i >= 1; i--) {
            System.out.println(i);
            Thread.sleep(100);
        }
        System.out.println("Go!");
    }
}''', explain="<p><b>How it works:</b> <code>Thread.sleep</code> is static: it always pauses the <i>current</i> thread (here, main). main declares <code>throws InterruptedException</code>.</p>"),
dict(level="medium", title="Interrupt a sleeping thread", stmt="<p>Start a thread that sleeps 10 seconds. Interrupt it at once and print the exception message it catches.</p>", inp="(none)",
 code='''public class Main {
    public static void main(String[] args) throws InterruptedException {
        Thread t = new Thread(() -> {
            try {
                Thread.sleep(10_000);
            } catch (InterruptedException e) {
                System.out.println("caught: " + e.getMessage());
            }
        });
        t.start();
        t.interrupt();
        t.join();
    }
}''', explain="<p><b>How it works:</b> <code>interrupt()</code> makes <code>sleep</code> throw <code>InterruptedException</code> (message \"sleep interrupted\"), so the program ends in milliseconds, not 10 seconds.</p>"),
dict(level="medium", title="The flag is cleared", stmt="<p>Interrupt the current thread, then call <code>sleep</code>. Print the interrupted flag after catching the exception.</p>", inp="(none)",
 code='''public class Main {
    public static void main(String[] args) {
        Thread.currentThread().interrupt();
        System.out.println("flag set: " + Thread.currentThread().isInterrupted());
        try {
            Thread.sleep(1000);
        } catch (InterruptedException e) {
            System.out.println("sleep threw at once");
        }
        System.out.println("flag now: " + Thread.currentThread().isInterrupted());
    }
}''', explain="<p><b>How it works:</b> when <code>sleep</code> throws <code>InterruptedException</code> it also <b>clears</b> the flag. If you can't handle the interrupt, restore it with <code>Thread.currentThread().interrupt()</code> so callers still see it.</p>"),
dict(level="medium", title="Join in a chain", stmt="<p>Thread B must print only after thread A has finished. Make B call <code>a.join()</code> before printing. main joins B.</p>", inp="(none)",
 code='''public class Main {
    public static void main(String[] args) throws InterruptedException {
        Thread a = new Thread(() -> System.out.println("A: data downloaded"));
        Thread b = new Thread(() -> {
            try {
                a.join();
            } catch (InterruptedException e) {
                return;
            }
            System.out.println("B: data processed");
        });
        a.start();
        b.start();
        b.join();
        System.out.println("main: all done");
    }
}''', explain="<p><b>How it works:</b> any thread can join any other. B is WAITING inside <code>a.join()</code> until A terminates, so B's line always comes second, whichever thread the scheduler runs first. (Careful: if B called <code>a.join()</code> before A was started, join would return at once, because a NEW thread isn't alive.)</p>"),
dict(level="business", title="OTP expiry timer", stmt="<p>An OTP is valid for 3 ticks. A timer thread prints the remaining ticks with 50 ms sleeps and then marks the OTP expired. main waits and prints the final status.</p>", inp="OTP 482913, 3 ticks",
 code='''public class Main {
    static String status = "VALID";

    public static void main(String[] args) throws InterruptedException {
        Thread timer = new Thread(() -> {
            try {
                for (int left = 3; left > 0; left--) {
                    System.out.println("OTP 482913 valid for " + left + " more tick(s)");
                    Thread.sleep(50);
                }
                status = "EXPIRED";
            } catch (InterruptedException e) {
                status = "CANCELLED";
            }
        }, "otp-timer");
        timer.start();
        timer.join();
        System.out.println("OTP status: " + status);
    }
}''', explain="<p><b>How it works:</b> the timer is mostly TIMED_WAITING. If the user verified the OTP early, main could <code>interrupt()</code> the timer and the status would become CANCELLED.</p>"),
dict(level="business", title="Cancel a bulk SMS run", stmt="<p>A marketing job sends 1,000 SMS, one per 500 ms. Operations cancels it right after start. The job must check for the interrupt, stop, and report how many were sent.</p>", inp="1,000 messages, cancelled immediately",
 code='''public class Main {
    public static void main(String[] args) throws InterruptedException {
        int[] sent = {0};
        Thread job = new Thread(() -> {
            for (int i = 1; i <= 1000; i++) {
                sent[0]++;
                try {
                    Thread.sleep(500);
                } catch (InterruptedException e) {
                    System.out.println("campaign stopped by operator");
                    return;
                }
            }
        }, "sms-campaign");
        job.start();
        job.interrupt();
        job.join();
        System.out.println("messages sent: " + sent[0] + " of 1000");
    }
}''', explain="<p><b>How it works:</b> the job checks for cancellation at every sleep. A thread that never sleeps or checks <code>isInterrupted()</code> can't be cancelled politely; that's why long loops should check the flag.</p>"),
dict(level="business", title="Pipeline with join timeouts", stmt="<p>A nightly pipeline has a fast step (sleeps 10 ms) and a stuck step (sleeps 60 s). Give each <code>join(200)</code>. Print which steps completed and cancel the stuck one.</p>", inp="steps: export (fast), upload (stuck)",
 code='''public class Main {
    static Thread step(String name, long ms) {
        return new Thread(() -> {
            try {
                Thread.sleep(ms);
            } catch (InterruptedException e) {
                System.out.println(name + " cancelled");
            }
        }, name);
    }

    public static void main(String[] args) throws InterruptedException {
        Thread[] steps = {step("export", 10), step("upload", 60_000)};
        for (Thread s : steps) s.start();
        for (Thread s : steps) {
            s.join(200);
            if (s.isAlive()) {
                System.out.println(s.getName() + ": TIMEOUT");
                s.interrupt();
                s.join();
            } else {
                System.out.println(s.getName() + ": OK");
            }
        }
    }
}''', explain="<p><b>How it works:</b> <code>join(ms)</code> never blocks longer than the limit. Combining it with <code>isAlive()</code> and <code>interrupt()</code> is the classic timeout pattern for raw threads (executors give you <code>Future.get(timeout)</code>, Lesson 12.6).</p>"),
]

# ---------------- Extra blocks ----------------
BLOCKS = {
'ANIM': ANIM,
'CODE_STATES': code('''public class Main {
    public static void main(String[] args) throws InterruptedException {
        Object lock = new Object();
        Thread sleeper = new Thread(() -> {
            try { Thread.sleep(60_000); } catch (InterruptedException e) { }
        }, "sleeper");
        Thread waiter = new Thread(() -> {
            try { sleeper.join(); } catch (InterruptedException e) { }
        }, "waiter");
        Thread blocked = new Thread(() -> {
            synchronized (lock) { }
        }, "blocked");

        System.out.println("sleeper: " + sleeper.getState());
        sleeper.start();
        waiter.start();
        synchronized (lock) {                 // main holds the lock...
            blocked.start();                  // ...so this thread can't get in
            while (blocked.getState() != Thread.State.BLOCKED
                    || sleeper.getState() != Thread.State.TIMED_WAITING
                    || waiter.getState() != Thread.State.WAITING) {
                Thread.onSpinWait();          // wait until all three have settled
            }
            System.out.println("sleeper: " + sleeper.getState());
            System.out.println("waiter:  " + waiter.getState());
            System.out.println("blocked: " + blocked.getState());
        }
        sleeper.interrupt();
        sleeper.join();
        waiter.join();
        blocked.join();
        System.out.println("sleeper: " + sleeper.getState());
    }
}'''),
'CODE_METHODS': snippet('''Thread.sleep(500);            // pause the CURRENT thread 500 ms  -> TIMED_WAITING
t.join();                     // wait until t ends                 -> WAITING
t.join(200);                  // ...but at most 200 ms             -> TIMED_WAITING
t.interrupt();                // politely ask t to stop
Thread.currentThread().isInterrupted();   // check the flag
t.getState();  t.isAlive();   // inspect
Thread.yield();               // hint: let another thread run (rarely needed)'''),
'CODE_RUN': code('''public class Main {
    public static void main(String[] args) throws InterruptedException {
        Thread download = new Thread(() -> {
            for (int pct = 25; pct <= 100; pct += 25) {
                System.out.println("download " + pct + "%");
                try {
                    Thread.sleep(40);
                } catch (InterruptedException e) {
                    System.out.println("download cancelled");
                    return;
                }
            }
        }, "download");

        System.out.println("1. " + download.getState());
        download.start();
        download.join();
        System.out.println("2. " + download.getState() + ", alive " + download.isAlive());
    }
}'''),
'RUNNER': runner([
 dict(label="1 · Progress with sleep", hint="Press <b>Run</b>. Then add <code>download.interrupt();</code> right after <code>start()</code> and run again: what changes?",
      code='''public class Main {
    public static void main(String[] args) throws InterruptedException {
        Thread download = new Thread(() -> {
            for (int pct = 25; pct <= 100; pct += 25) {
                System.out.println("download " + pct + "%");
                try {
                    Thread.sleep(40);
                } catch (InterruptedException e) {
                    System.out.println("download cancelled");
                    return;
                }
            }
        }, "download");

        System.out.println("1. " + download.getState());
        download.start();
        download.join();
        System.out.println("2. " + download.getState() + ", alive " + download.isAlive());
    }
}'''),
 dict(label="2 · Predict: state right after start", hint="<b>Predict first:</b> which state is printed? Run it several times. Why can't you be sure? (The thread may still be RUNNABLE or already asleep.)",
      code='''public class Main {
    public static void main(String[] args) throws InterruptedException {
        Thread t = new Thread(() -> {
            try { Thread.sleep(200); } catch (InterruptedException e) { }
        });
        t.start();
        System.out.println("right after start: " + t.getState());
        Thread.sleep(50);
        System.out.println("50 ms later: " + t.getState());
        t.join();
    }
}'''),
 dict(label="3 · Predict: interrupt yourself", hint="<b>Predict first:</b> does the sleep last 2 seconds? Then delete the first line and compare.",
      code='''public class Main {
    public static void main(String[] args) {
        Thread.currentThread().interrupt();
        long start = System.currentTimeMillis();
        try {
            Thread.sleep(2000);
        } catch (InterruptedException e) {
            System.out.println("sleep ended early: " + e.getMessage());
        }
        System.out.println("slept about " + (System.currentTimeMillis() - start) / 1000 + " s");
    }
}'''),
 dict(label="4 · Crash: negative timeout", hint="A timeout can't be negative. Read the exception, then use <code>join(500)</code>.",
      code='''public class Main {
    public static void main(String[] args) throws InterruptedException {
        Thread sync = new Thread(() -> System.out.println("syncing contacts"));
        sync.start();
        long waitMs = 500 - 1000;
        sync.join(waitMs);
        System.out.println("done");
    }
}''', _expect="exception"),
 dict(label="5 · Spot the error", hint="<code>getState()</code> returns an enum <code>Thread.State</code>, not a String. Compare with <code>Thread.State.NEW</code>.",
      code='''public class Main {
    public static void main(String[] args) {
        Thread t = new Thread(() -> {});
        if (t.getState() == "NEW") {
            System.out.println("not started yet");
        }
    }
}''', _expect="compile-error"),
]),
'QUIZ': quiz([
 {"q": "How many values does Thread.State have?", "options": ["4", "5", "6", "7"], "answer": 2, "why": "NEW, RUNNABLE, BLOCKED, WAITING, TIMED_WAITING, TERMINATED."},
 {"q": "A thread is inside Thread.sleep(1000). Its state is…", "options": ["WAITING", "BLOCKED", "TIMED_WAITING", "RUNNABLE"], "answer": 2, "why": "Waits with a time limit are TIMED_WAITING."},
 {"q": "A thread tries to enter a synchronized block whose lock another thread holds. Its state is…", "options": ["WAITING", "BLOCKED", "TIMED_WAITING", "NEW"], "answer": 1, "why": "BLOCKED means waiting to acquire a monitor lock."},
 {"q": "Java has no separate 'RUNNING' state because…", "options": ["threads never run", "RUNNABLE covers both running and ready-to-run", "it's called ACTIVE", "it's TIMED_WAITING"], "answer": 1, "why": "Whether a RUNNABLE thread is on a core right now is up to the OS scheduler."},
 {"q": "What does t.interrupt() do?", "options": ["Kills t immediately", "Sets t's interrupted flag; blocking calls like sleep then throw InterruptedException", "Pauses t", "Restarts t"], "answer": 1, "why": "Interruption is cooperative: the thread must notice and stop itself."},
 {"q": "Which statement pauses the thread that executes it?", "options": ["t.sleep(100) always pauses t", "Thread.sleep(100)", "t.join()", "t.yield()"], "answer": 1, "why": "sleep is static and always pauses the current thread, whatever reference you call it through."},
 {"q": "After join() returns normally, the joined thread is…", "options": ["NEW", "RUNNABLE", "TERMINATED", "WAITING"], "answer": 2, "why": "join() waits until the thread has terminated."},
 {"q": "Which call can bring a TERMINATED thread back to life?", "options": ["start()", "run()", "interrupt()", "None: create a new Thread"], "answer": 3, "why": "TERMINATED is final. start() on it throws IllegalThreadStateException."},
]),
}
