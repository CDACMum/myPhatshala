import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from mkanim import Anim, two_view
from m12 import code, snippet, runner, quiz

# ---------------- Part 5: two-view animation ----------------
S = Anim("see", frames=6, h=250, label="One thread does three downloads one after another; three threads do them at the same time")
S.box(8, 8, 344, 40, None, fill="board", stroke="board")
for f, t in {1: "download(a); download(b); download(c);", 2: "download(a); download(b); download(c);",
             3: "download(a); download(b); download(c);", 4: "new Thread(() -> download(a)).start(); …",
             5: "t1.join(); t2.join(); t3.join();", 6: "// all three done"}.items():
    S.text(18, 33, t.replace('<', '&lt;').replace('>', '&gt;'), on=str(f), mono=True, size=9.6, cls="chalk")
S.text(10, 72, "time →", size=9.5, cls="ink3")
S.arrow(50, 68, 346, 68, color="line", sw=1.2)
# sequential bars
S.text(10, 98, "main", size=9.5, bold=True, cls="ink2", )
S.box(50, 84, 90, 22, "a", fill="soft-acc", stroke="track", on="1-3", size=10, bold=True)
S.box(142, 84, 90, 22, "b", fill="soft-acc", stroke="track", on="2-3", size=10, bold=True)
S.box(234, 84, 90, 22, "c", fill="soft-acc", stroke="track", on="3", size=10, bold=True)
S.text(330, 100, "3 s", on="3", size=10, bold=True, cls="red")
# parallel bars
for i, (n, y) in enumerate([("t1", 124), ("t2", 152), ("t3", 180)]):
    S.text(10, y + 15, n, size=9.5, bold=True, cls="ink2", on="4-")
    S.box(50, y, 90, 22, "abc"[i], fill="soft-green", stroke="green", on="4-", size=10, bold=True)
S.text(148, 168, "≈ 1 s", on="5-", size=11, bold=True, cls="green")
S.note({1: "One thread, first download…", 2: "…then the second…", 3: "…then the third: 3 seconds.",
        4: "Three threads start together.", 5: "main waits for all three.", 6: "Same work, about a third of the time."}, y=232, size=10.5)
S.caps(["One thread does one thing at a time: <code>download(a)</code> must finish before <code>download(b)</code> starts.",
        "The second download waits for the first. The app feels stuck.",
        "Three one-second downloads take three seconds in a row.",
        "With three <b>threads</b>, the three downloads run at the same time.",
        "<code>join()</code> makes <code>main</code> wait until each thread has finished.",
        "When the work is mostly waiting (network, disk), threads finish in about the time of the slowest one. (Times are illustrative.)"])

B = Anim("behind", frames=6, h=250, label="Inside one process: a shared heap, one stack per thread, and the CPU cores running them")
B.box(6, 6, 348, 200, None, fill="card", stroke="line")
B.text(16, 24, "one JVM process (its own memory)", size=10, bold=True, cls="ink2")
B.box(16, 34, 150, 60, None, fill="soft-blue", stroke="blue")
B.text(26, 52, "HEAP (shared)", size=9.5, bold=True, cls="blue")
B.text(26, 70, "#1 images[3]", mono=True, size=9.5, on="1-")
B.text(26, 86, "{a, b, c}", mono=True, size=9.5, on="5-", cls="green")
stacks = [("main", 186, "1-"), ("t1", 230, "4-"), ("t2", 274, "4-"), ("t3", 318, "4-")]
for n, x, on in stacks:
    B.box(x - 18, 34, 38, 60, None, fill="card2", stroke="line", on=on)
    B.text(x + 1, 50, n, size=9, bold=True, anchor="middle", on=on)
    B.text(x + 1, 66, "stack", size=8, anchor="middle", cls="ink3", on=on)
for n, x, on in stacks[1:]:
    B.arrow(x, 94, 120, 92, on="5", color="green", sw=1.3)
B.text(16, 120, "CPU cores", size=10, bold=True, cls="ink2")
for i in range(2):
    B.box(16 + i * 82, 128, 74, 34, f"core {i + 1}", fill="soft-acc", stroke="track", size=9.5, bold=True)
B.text(186, 140, "main", on="1-3", size=10, mono=True)
B.text(186, 140, "t1, t2", on="4-5", size=10, mono=True, cls="green")
B.text(186, 156, "t3 waits its turn", on="4", size=9.5, cls="ink2")
B.text(186, 156, "scheduler swaps them", on="5", size=9.5, cls="ink2")
B.text(186, 140, "t1–t3 finished", on="6", size=10, mono=True, cls="green")
B.note({1: "A process with its heap and one thread.", 2: "main runs on one core.", 3: "The other core sits idle.",
        4: "Each new thread gets its own stack.", 5: "All threads write to the same heap.", 6: "Threads end; their stacks go."}, y=228, size=10.5)
B.caps(["Your program runs as one <b>process</b>: it has its own memory. Inside, the <code>main</code> thread has its own <b>stack</b>; objects live on the shared <b>heap</b>.",
        "With one thread, only one core works on your code at any moment.",
        "On a multi-core machine, the other cores sit idle for this program.",
        "<code>new Thread(…).start()</code> creates threads with their <b>own stacks</b> in the <b>same process</b>. Creating a thread is much cheaper than starting a new process.",
        "All threads see the same heap, so they can fill the same array. The OS scheduler shares the cores between threads, switching between them many times a second.",
        "When a thread's work ends, its stack is freed. The results stay on the heap for <code>main</code> to read."])
ANIM = two_view("One thread vs several threads", S, B)

# ---------------- Part 6: animated example ----------------
ANIM2_HEADING = "Watch it with an example: a banking app that never freezes"
ANIM2_INTRO = "A customer taps “Download statement”. Creating the PDF takes a few seconds. Watch what happens with and without a background thread."
A = Anim("Statement download in the background", frames=5, h=220, label="The screen thread hands the slow PDF job to a background thread and stays responsive")
A.box(10, 14, 120, 150, None, fill="card2", stroke="line")
A.text(70, 32, "phone screen", size=9.5, anchor="middle", cls="ink3")
A.box(22, 44, 96, 26, "Download", fill="soft-blue", stroke="blue", size=10, bold=True)
A.box(22, 80, 96, 26, "Balance", fill="card", stroke="line", size=10)
A.text(70, 130, "frozen…", on="2", size=11, bold=True, cls="red", anchor="middle")
A.text(70, 130, "responsive ✓", on="4-", size=10.5, bold=True, cls="green", anchor="middle")
A.text(70, 148, "₹ 24,500", on="4-", size=10.5, mono=True, anchor="middle")
A.box(160, 14, 190, 46, None, fill="board", stroke="board")
A.text(170, 32, "UI thread", size=9.5, bold=True, cls="chalk")
A.text(170, 50, "makePdf();   // 4 s", on="2", mono=True, size=9.5, cls="chalk")
A.text(170, 50, "new Thread(makePdf).start();", on="3-", mono=True, size=9.2, cls="chalk")
A.box(160, 72, 190, 40, None, fill="soft-green", stroke="green", on="3-")
A.text(170, 90, "background thread", on="3-", size=9.5, bold=True, cls="green")
A.text(170, 104, "building PDF…", on="3-4", size=9.5, mono=True)
A.text(170, 104, "statement.pdf ready", on="5", size=9.5, mono=True, cls="green", bold=True)
A.arrow(190, 60, 190, 72, on="3", color="green")
A.note({1: "A tap on Download.", 2: "Done on the UI thread: the app freezes.", 3: "Hand the job to a new thread.",
        4: "The screen keeps responding.", 5: "The PDF is ready; tell the user."}, y=196, size=10.5)
A.caps(["The customer taps <b>Download statement</b>.",
        "If the UI thread builds the PDF itself, it can't redraw the screen or react to taps for 4 seconds: the app looks hung.",
        "Instead, the UI thread starts a <b>background thread</b> for the slow job and returns at once.",
        "While the PDF is being built, the customer can still check the balance: two threads, one app.",
        "When the background thread finishes, the app shows “statement ready”. Mobile and desktop apps work this way. (Simplified: real apps use thread pools and UI-safe callbacks, Lesson 12.6.)"])
ANIM2 = A

# ---------------- Part 8: tracer ----------------
TRACE = dict(code='''public class Main {
    static int[] result = new int[1];

    public static void main(String[] args) throws InterruptedException {
        String me = Thread.currentThread().getName();
        Thread worker = new Thread(() -> result[0] = 6 * 7, "worker");
        worker.start();
        worker.join();
        System.out.println(me + " read " + result[0] + " from " + worker.getName());
    }
}
''', notes={
 5: "Who am I? :: <code>Thread.currentThread()</code> returns the thread running this line: the JVM's <b>main</b> thread.",
 6: "Create :: A Thread object named \"worker\" is created on the heap. It is only an object so far: state <b>NEW</b>, no stack, nothing running.",
 7: "Start :: = <code>start()</code> asks the JVM to create a real thread with its own stack and let the scheduler run it. Its state becomes RUNNABLE (or already TERMINATED if it was quick). This trace follows the main thread only, so the worker's own line doesn't appear here.",
 8: "Join :: = <code>join()</code> makes main wait until the worker has finished. Now the worker is TERMINATED and <code>result[0]</code> on the shared heap holds 42.",
 9: "Print :: main reads the value the other thread wrote: both threads share the same heap."})

# ---------------- Worked examples ----------------
WORKED_INTRO = "Three small programs in the style of real apps. The traces follow the main thread: watch Thread objects appear on the heap, change state, and leave their results in shared objects."
EXAMPLES = [
dict(tag="Food delivery · images", title="Prepare three menu photos at once",
 problem="<p>A food app must resize three dish photos before showing the menu. Do each one in its own thread, wait for all three, then print the new sizes. (Resizing is simulated by halving a number.)</p>",
 inp="photo sizes in KB: 840, 620, 980",
 approach=["Store the inputs and the results in two arrays on the heap.",
           "Create one thread per photo; each thread writes only its own result slot, so they never touch the same element.",
           "Start all threads, then <code>join()</code> each one before reading the results."],
 code='''public class Main {
    static int[] sizes = {840, 620, 980};
    static int[] resized = new int[3];

    public static void main(String[] args) throws InterruptedException {
        Thread[] workers = new Thread[3];
        for (int i = 0; i < 3; i++) {
            int k = i;
            workers[i] = new Thread(() -> resized[k] = sizes[k] / 2, "photo-" + k);
            workers[i].start();
        }
        for (Thread t : workers) {
            t.join();
        }
        System.out.println(resized[0] + " " + resized[1] + " " + resized[2] + " KB");
    }
}
''', notes={6: "Array of threads :: An array to hold the three Thread objects.",
            (8, 1): "Copy the index :: <code>k</code> is a fresh, effectively final copy of <code>i</code> that the lambda can capture.",
            (10, 1): "Start photo-0 :: = The first worker starts. It may finish before main reaches the next line: the scheduler decides.",
            (10, 3): "Start photo-2 :: = All three workers have been started. Each wrote, or will write, its own slot of <code>resized</code>.",
            (13, 3): "Last join :: = After the last <code>join()</code> returns, every worker is TERMINATED and all three results are on the heap.",
            15: "Print :: main reads the three results the workers stored."},
 tryit="Press <b>Run</b>. Then remove the second loop (the joins). Run it several times: sometimes you'll see 0s, because main printed before the workers finished."),
dict(tag="Banking · reports", title="Two threads fill one report object",
 problem="<p>A month-end report has two sections: total deposits and total withdrawals. Compute each section in a separate thread that writes into the same <code>Report</code> object, then print the report.</p>",
 inp="deposits 5000, 12000, 800; withdrawals 2000, 450",
 approach=["Create one <code>Report</code> object on the heap; both threads get a reference to it.",
           "Thread A sums deposits into <code>report.in</code>; thread B sums withdrawals into <code>report.out</code>. Different fields, so no clash.",
           "Join both threads, then print. The report object shows both threads' work."],
 code='''class Report {
    int in;
    int out;
}

public class Main {
    public static void main(String[] args) throws InterruptedException {
        Report report = new Report();
        int[] deposits = {5000, 12000, 800};
        int[] withdrawals = {2000, 450};
        Thread a = new Thread(() -> {
            for (int d : deposits) report.in += d;
        }, "deposits");
        Thread b = new Thread(() -> {
            for (int w : withdrawals) report.out += w;
        }, "withdrawals");
        a.start();
        b.start();
        a.join();
        b.join();
        System.out.println("In " + report.in + ", out " + report.out + ", net " + (report.in - report.out));
    }
}
''', notes={8: "Shared object :: One Report object (#n) on the heap. Both lambdas will capture this same reference.",
            11: "Thread A :: The deposits thread is created, still NEW.",
            14: "Thread B :: The withdrawals thread is created.",
            17: "Start A :: = Thread A starts summing deposits into <code>report.in</code>.",
            18: "Start B :: = Thread B starts summing withdrawals into <code>report.out</code>, possibly at the same moment on another core.",
            20: "Both done :: = After both joins, the Report object holds 17800 in and 2450 out.",
            21: "Print :: main prints the combined report."},
 tryit="Press <b>Run</b>. Then make both threads add into the <i>same</i> field and think about whether that is safe. (It isn't: Lesson 12.4.)"),
dict(tag="Notes app · autosave", title="A daemon autosave thread doesn't keep the app alive",
 problem="<p>A notes app runs an autosave helper in the background forever. When the user closes the app, the program must end without waiting for the helper. Mark the helper as a <b>daemon</b> thread and show that the program still ends.</p>",
 inp="(no input)",
 approach=["Create the autosave thread with an endless loop that sleeps between saves.",
           "Call <code>setDaemon(true)</code> before <code>start()</code>.",
           "When main ends, only daemon threads are left, so the JVM exits."],
 code='''public class Main {
    public static void main(String[] args) {
        Thread autosave = new Thread(() -> {
            while (true) {
                try {
                    Thread.sleep(60_000);
                } catch (InterruptedException e) {
                    return;
                }
            }
        }, "autosave");
        autosave.setDaemon(true);
        autosave.start();
        System.out.println("autosave daemon? " + autosave.isDaemon());
        System.out.println("main is done; the JVM exits now");
    }
}
''', notes={3: "Create :: The autosave thread object is created (NEW). Its loop would run forever.",
            12: "Daemon :: <code>setDaemon(true)</code> marks it as a helper thread. This must happen before <code>start()</code>.",
            13: "Start :: = The helper starts and soon goes to sleep for 60 seconds.",
            15: "Last line :: After this line main ends. The only thread left is a daemon, so the JVM stops it and exits."},
 tryit="Press <b>Run</b>: it finishes at once. Then delete the <code>setDaemon(true)</code> line: the program keeps running (the online runner will time out), because a normal thread is still alive."),
]

# ---------------- Practice problems ----------------
PRACTICE_INTRO = "Start, name and join threads, and let them share results through the heap. Every solution waits with <code>join()</code> before printing, so the output is always the same. The last three are business tasks."
PROBLEMS = [
dict(level="easy", title="Name of the current thread", stmt="<p>Print the name of the thread that runs <code>main</code>.</p>", inp="(none)",
 code='''public class Main {
    public static void main(String[] args) {
        System.out.println("Running on: " + Thread.currentThread().getName());
    }
}''', explain="<p><b>How it works:</b> the JVM runs <code>main</code> on a thread called \"main\". <code>Thread.currentThread()</code> returns the thread executing the current line.</p>"),
dict(level="easy", title="Start a named thread and wait for it", stmt="<p>Create a thread named \"greeter\" that prints <code>Hello from greeter</code>. Start it, wait for it, then print <code>main ends</code>.</p>", inp="(none)",
 code='''public class Main {
    public static void main(String[] args) throws InterruptedException {
        Thread g = new Thread(() -> System.out.println("Hello from " + Thread.currentThread().getName()), "greeter");
        g.start();
        g.join();
        System.out.println("main ends");
    }
}''', explain="<p><b>How it works:</b> the second argument of the constructor names the thread. <code>join()</code> guarantees the greeting is printed before \"main ends\".</p>"),
dict(level="easy", title="Default thread names", stmt="<p>Create two threads without names and print their default names and states.</p>", inp="(none)",
 code='''public class Main {
    public static void main(String[] args) {
        Thread a = new Thread(() -> {});
        Thread b = new Thread(() -> {});
        System.out.println(a.getName() + " " + a.getState());
        System.out.println(b.getName() + " " + b.getState());
    }
}''', explain="<p><b>How it works:</b> unnamed threads get names Thread-0, Thread-1 … in creation order. Before <code>start()</code> they are in state NEW. Name your threads: it makes logs readable.</p>"),
dict(level="medium", title="Sum 1 to 1000 in two halves", stmt="<p>Use two threads: one sums 1–500, the other 501–1000. Each stores its part in a shared array. Print both parts and the total.</p>", inp="1..1000",
 code='''public class Main {
    static long[] part = new long[2];

    public static void main(String[] args) throws InterruptedException {
        Thread low = new Thread(() -> { for (int i = 1; i <= 500; i++) part[0] += i; });
        Thread high = new Thread(() -> { for (int i = 501; i <= 1000; i++) part[1] += i; });
        low.start();
        high.start();
        low.join();
        high.join();
        System.out.println(part[0] + " + " + part[1] + " = " + (part[0] + part[1]));
    }
}''', explain="<p><b>How it works:</b> each thread writes a different array slot, so they never write the same memory. After both joins, main can safely read the results. Splitting work into independent pieces is the basic idea of parallel processing.</p>"),
dict(level="medium", title="Largest value, split across threads", stmt="<p>Find the largest value in an array of 8 numbers by giving each half to a different thread, then comparing the two answers.</p>", inp="[14, 92, 33, 7, 61, 88, 45, 19]",
 code='''public class Main {
    static int[] data = {14, 92, 33, 7, 61, 88, 45, 19};
    static int[] best = new int[2];

    static void maxOf(int slot, int from, int to) {
        int m = data[from];
        for (int i = from + 1; i < to; i++) m = Math.max(m, data[i]);
        best[slot] = m;
    }

    public static void main(String[] args) throws InterruptedException {
        Thread a = new Thread(() -> maxOf(0, 0, 4));
        Thread b = new Thread(() -> maxOf(1, 4, 8));
        a.start();
        b.start();
        a.join();
        b.join();
        System.out.println("Halves: " + best[0] + ", " + best[1] + "; max " + Math.max(best[0], best[1]));
    }
}''', explain="<p><b>How it works:</b> a normal method does the work; each thread just calls it with different ranges. Each thread has its own stack, so the local <code>m</code> in one thread can't interfere with the other's.</p>"),
dict(level="business", title="Store totals in parallel", stmt="<p>A chain has 3 stores. Each store's daily bills are in an array. Compute each store's total in its own thread and print a summary.</p>", inp="Pune {450, 1200, 300}; Nagpur {800, 150}; Nashik {990, 60, 75, 300}",
 code='''public class Main {
    static String[] stores = {"Pune", "Nagpur", "Nashik"};
    static int[][] bills = {{450, 1200, 300}, {800, 150}, {990, 60, 75, 300}};
    static int[] totals = new int[3];

    public static void main(String[] args) throws InterruptedException {
        Thread[] t = new Thread[3];
        for (int s = 0; s < 3; s++) {
            int k = s;
            t[s] = new Thread(() -> { for (int b : bills[k]) totals[k] += b; }, stores[s]);
            t[s].start();
        }
        for (Thread x : t) x.join();
        for (int s = 0; s < 3; s++) System.out.println(stores[s] + ": Rs " + totals[s]);
    }
}''', explain="<p><b>How it works:</b> one thread per store, each writing only its own slot. Naming each thread after its store makes logs and thread dumps easy to read in production.</p>"),
dict(level="business", title="GST for two halves of an order list", stmt="<p>Compute 18% GST on 6 order amounts, using one thread for the first three and another for the last three. Print the GST per order in the original order.</p>", inp="[1000, 250, 4999, 120, 760, 3300]",
 code='''public class Main {
    static double[] amount = {1000, 250, 4999, 120, 760, 3300};
    static double[] gst = new double[6];

    static void tax(int from, int to) {
        for (int i = from; i < to; i++) gst[i] = Math.round(amount[i] * 18) / 100.0;
    }

    public static void main(String[] args) throws InterruptedException {
        Thread a = new Thread(() -> tax(0, 3));
        Thread b = new Thread(() -> tax(3, 6));
        a.start();
        b.start();
        a.join();
        b.join();
        for (int i = 0; i < 6; i++) System.out.println("Order " + (i + 1) + ": GST " + gst[i]);
    }
}''', explain="<p><b>How it works:</b> results are stored by index, so the printing order doesn't depend on which thread finished first. <code>Math.round(x * 18) / 100.0</code> rounds the tax to paise.</p>"),
dict(level="business", title="Background audit logger that doesn't block shutdown", stmt="<p>Start a daemon thread named \"audit\" that would write logs forever, record two transactions on main, and end the program cleanly.</p>", inp="two transactions",
 code='''public class Main {
    public static void main(String[] args) {
        Thread audit = new Thread(() -> {
            while (true) {
                try { Thread.sleep(10_000); } catch (InterruptedException e) { return; }
            }
        }, "audit");
        audit.setDaemon(true);
        audit.start();
        System.out.println("TXN-1 Rs 500 recorded");
        System.out.println("TXN-2 Rs 120 recorded");
        System.out.println(audit.getName() + " is daemon: " + audit.isDaemon());
    }
}''', explain="<p><b>How it works:</b> the JVM exits when all non-daemon threads have ended. A daemon thread is a helper that never keeps the program alive. Never use daemons for work that must finish (like saving data): they are stopped abruptly.</p>"),
]

# ---------------- Extra blocks ----------------
BLOCKS = {
'ANIM': ANIM,
'CODE_NAMES': code('''public class Main {
    public static void main(String[] args) {
        Thread me = Thread.currentThread();
        System.out.println("main runs on: " + me.getName());

        Thread helper = new Thread(() -> {});
        System.out.println(helper.getName() + ", state " + helper.getState()
                + ", daemon " + helper.isDaemon() + ", priority " + helper.getPriority());
    }
}'''),
'CODE_CORES': code('''public class Main {
    public static void main(String[] args) {
        System.out.println("CPU cores Java can use: " + Runtime.getRuntime().availableProcessors());
    }
}''', skip=True),
'CODE_RUN': code('''public class Main {
    static String[] files = {"menu.json", "offers.json", "photo.jpg"};
    static int[] bytes = new int[3];

    static void download(int i) {
        bytes[i] = files[i].length() * 100;   // pretend work: size depends on the name
        System.out.println(Thread.currentThread().getName() + " downloaded " + files[i]);
    }

    public static void main(String[] args) throws InterruptedException {
        Thread[] workers = new Thread[3];
        for (int i = 0; i < 3; i++) {
            int k = i;
            workers[i] = new Thread(() -> download(k), "dl-" + k);
            workers[i].start();
        }
        for (Thread t : workers) {
            t.join();
        }
        System.out.println("All done: " + bytes[0] + " + " + bytes[1] + " + " + bytes[2] + " bytes");
    }
}''', skip=True),
'RUNNER': runner([
 dict(label="1 · Three downloads", hint="Press <b>Run</b> a few times. The order of the “downloaded” lines can change between runs; the last line never does. Why?",
      code='''public class Main {
    static String[] files = {"menu.json", "offers.json", "photo.jpg"};
    static int[] bytes = new int[3];

    static void download(int i) {
        bytes[i] = files[i].length() * 100;
        System.out.println(Thread.currentThread().getName() + " downloaded " + files[i]);
    }

    public static void main(String[] args) throws InterruptedException {
        Thread[] workers = new Thread[3];
        for (int i = 0; i < 3; i++) {
            int k = i;
            workers[i] = new Thread(() -> download(k), "dl-" + k);
            workers[i].start();
        }
        for (Thread t : workers) {
            t.join();
        }
        System.out.println("All done: " + bytes[0] + " + " + bytes[1] + " + " + bytes[2] + " bytes");
    }
}'''),
 dict(label="2 · Predict: which thread?", hint="<b>Predict first:</b> what names are printed? Then change <code>t.run()</code> to <code>t.start()</code> and run again (and add <code>t.join()</code>).",
      code='''public class Main {
    public static void main(String[] args) {
        Thread t = new Thread(() -> System.out.println("Working on " + Thread.currentThread().getName()), "report-builder");
        t.run();
        System.out.println("main continues on " + Thread.currentThread().getName());
    }
}'''),
 dict(label="3 · Predict: without join", hint="<b>Predict first:</b> can the total be printed before the worker has finished? Run it several times, then add <code>worker.join();</code> before the print (and <code>throws InterruptedException</code>).",
      code='''public class Main {
    static int total = 0;

    public static void main(String[] args) {
        Thread worker = new Thread(() -> {
            for (int i = 1; i <= 100000; i++) total += 1;
        });
        worker.start();
        System.out.println("total = " + total);
    }
}'''),
 dict(label="4 · Crash: start twice", hint="A thread can be started only once. Read the exception, then create a new Thread object for the second run.",
      code='''public class Main {
    public static void main(String[] args) throws InterruptedException {
        Thread t = new Thread(() -> System.out.println("sending OTP"));
        t.start();
        t.join();
        t.start();
    }
}''', _expect="exception"),
 dict(label="5 · Spot the error", hint="<code>Thread.sleep</code> can throw the checked <code>InterruptedException</code> (Lesson 9.3). Add <code>throws InterruptedException</code> to main, or wrap it in try/catch.",
      code='''public class Main {
    public static void main(String[] args) {
        System.out.println("Refreshing in 1 second...");
        Thread.sleep(1000);
        System.out.println("Refreshed");
    }
}''', _expect="compile-error"),
]),
'QUIZ': quiz([
 {"q": "What does a thread have that it does NOT share with other threads of the same process?", "options": ["The heap", "Its own stack", "Static fields", "Loaded classes"], "answer": 1, "why": "Each thread has its own stack of method frames and local variables. The heap, static fields and classes are shared."},
 {"q": "What is the name of the thread that runs main()?", "options": ["Thread-0", "main", "primary", "jvm"], "answer": 1, "why": "The JVM starts your program on a thread named \"main\"."},
 {"q": "Which call actually starts a new thread of execution?", "options": ["t.run()", "t.start()", "new Thread()", "t.join()"], "answer": 1, "why": "start() asks the JVM to create the thread; run() just calls the method on the current thread."},
 {"q": "What does t.join() do?", "options": ["Starts t", "Makes the calling thread wait until t finishes", "Merges two threads", "Stops t"], "answer": 1, "why": "join() blocks the caller until t has terminated."},
 {"q": "Two threads of the same process…", "options": ["have separate heaps", "can read and write the same objects", "cannot communicate", "must run on different computers"], "answer": 1, "why": "Threads share the heap, which is what makes them useful, and also what makes them risky (Lesson 12.4)."},
 {"q": "On a computer with 1 core, multithreading gives…", "options": ["No benefit ever", "Concurrency (taking turns), not true parallelism", "Parallelism", "A compile error"], "answer": 1, "why": "One core runs one thread at a time but switches between them, which still helps when threads wait for I/O."},
 {"q": "When does the JVM exit?", "options": ["When main ends", "When all non-daemon threads have ended", "When all threads including daemons end", "Never"], "answer": 1, "why": "Daemon threads don't keep the JVM alive; normal (user) threads do."},
 {"q": "Compared with starting a new process, starting a thread is…", "options": ["more expensive", "cheaper, because it shares the process's memory", "the same", "impossible in Java"], "answer": 1, "why": "A process needs its own memory and resources; a thread only needs a stack and scheduling information."},
]),
}
