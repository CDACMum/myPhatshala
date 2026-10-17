import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from mkanim import Anim, two_view
from m12 import code, snippet, runner, quiz

def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

# ---------------- Part 5: two-view animation ----------------
S = Anim("see", frames=6, h=250, label="Tasks are submitted to a pool of two worker threads; each submit returns a Future that later holds the result")
S.box(8, 8, 344, 74, None, fill="board", stroke="board")
lines = {1: ["ExecutorService pool =", "    Executors.newFixedThreadPool(2);"],
         2: ["Future<Integer> f1 = pool.submit(task1);", "Future<Integer> f2 = pool.submit(task2);"],
         3: ["Future<Integer> f3 = pool.submit(task3);", "// only 2 workers: task3 waits"],
         4: ["// a worker finished task1", "// and picks up task3"],
         5: ["int total = f1.get() + f2.get()", "          + f3.get();   // waits if needed"],
         6: ["pool.shutdown();", "// workers end after the queue is empty"]}
for f, ls in lines.items():
    for i, l in enumerate(ls):
        S.text(18, 32 + i * 22, esc(l), on=str(f), mono=True, size=9.4, cls="chalk")
S.text(10, 104, "your code (main)", size=9.5, bold=True, cls="ink2")
fut = {"f1": (10, "2-"), "f2": (100, "2-"), "f3": (190, "3-")}
for n, (x, on) in fut.items():
    S.box(x, 112, 82, 36, None, fill="card2", stroke="line", on=on)
    S.text(x + 8, 128, n, size=9.5, bold=True, mono=True, on=on)
S.text(18, 143, "pending", size=8.6, mono=True, cls="acc", on="2-3")
S.text(18, 143, "done: 10", size=8.6, mono=True, cls="green", on="4-")
S.text(108, 143, "pending", size=8.6, mono=True, cls="acc", on="2-4")
S.text(108, 143, "done: 20", size=8.6, mono=True, cls="green", on="5-")
S.text(198, 143, "pending", size=8.6, mono=True, cls="acc", on="3-4")
S.text(198, 143, "done: 30", size=8.6, mono=True, cls="green", on="5-")
S.text(10, 180, "total = 60", on="5-", size=12, bold=True, mono=True, cls="green")
S.text(10, 204, "no new Thread() written anywhere", on="1-2", size=9.5, cls="ink3")
S.text(10, 204, "pool threads stop; JVM can exit", on="6", size=9.5, cls="ink2")
S.note({1: "Create a pool of 2 workers.", 2: "Submit two tasks: two Futures.", 3: "A third task queues.",
        4: "task1 done; worker takes task3.", 5: "get() collects the results.", 6: "Shut the pool down."}, y=234, size=10.5)
S.caps(["<code>Executors.newFixedThreadPool(2)</code> creates an <b>ExecutorService</b> with 2 worker threads that will be reused for every task.",
        "<code>submit(task)</code> hands over the job and returns immediately with a <b>Future</b>: a receipt for a result that isn't ready yet.",
        "A third task arrives while both workers are busy. It waits in the pool's queue; no extra thread is created.",
        "When a worker finishes task1, its Future becomes <b>done</b>, and the same worker immediately takes task3 from the queue.",
        "<code>future.get()</code> returns the result, waiting if the task hasn't finished. main never touches a Thread object.",
        "<code>shutdown()</code> stops accepting new tasks; the workers finish what's queued and then end. Without it, the pool's threads keep the JVM alive."])

B = Anim("behind", frames=6, h=250, label="Inside the ThreadPoolExecutor: a task queue and two reusable worker threads")
B.box(6, 6, 348, 200, None, fill="card", stroke="line")
B.text(16, 24, "ThreadPoolExecutor (core size 2)", size=10, bold=True, cls="ink2")
B.box(16, 36, 150, 50, None, fill="soft-acc", stroke="track")
B.text(26, 52, "task queue", size=9.5, bold=True, cls="acc")
B.text(26, 74, "task3", on="3", mono=True, size=10, bold=True)
B.text(26, 74, "(empty)", on="1-2,4-", size=9, cls="ink3")
for i, (y, n) in enumerate([(36, "pool-1-thread-1"), (100, "pool-1-thread-2")]):
    B.box(186, y, 160, 54, None, fill="soft-blue", stroke="blue")
    B.text(196, y + 18, n, size=9, bold=True, mono=True, cls="blue")
w1 = {1: ("idle (waits on queue)", "ink3"), 2: ("running task1", "ink"), 3: ("running task1", "ink"), 4: ("running task3", "ink"),
      5: ("idle", "ink3"), 6: ("TERMINATED", "ink3")}
w2 = {1: ("idle (waits on queue)", "ink3"), 2: ("running task2", "ink"), 3: ("running task2", "ink"), 4: ("running task2", "ink"),
      5: ("idle", "ink3"), 6: ("TERMINATED", "ink3")}
for f, (t, c) in w1.items():
    B.text(196, 76, t, on=str(f), mono=True, size=9, cls=c)
for f, (t, c) in w2.items():
    B.text(196, 140, t, on=str(f), mono=True, size=9, cls=c)
B.arrow(166, 62, 184, 62, on="4", color="green")
B.text(16, 116, "Futures on the heap", size=9.5, bold=True, cls="ink2")
B.text(16, 134, "f1: NEW → COMPLETED", size=9, mono=True, on="4-", cls="green")
B.text(16, 150, "f2, f3: COMPLETED", size=9, mono=True, on="5-", cls="green")
B.text(16, 134, "f1, f2: NEW (not done)", size=9, mono=True, on="2-3", cls="acc")
B.text(16, 180, "threads created once, reused for every task", size=9.2, cls="ink2", on="1-5")
B.text(16, 180, "shutdown(): queue drained, workers exit", size=9.2, cls="ink2", on="6")
B.note({1: "Two workers, empty queue.", 2: "Each worker runs one task.", 3: "Extra task waits in the queue.",
        4: "A freed worker takes the next task.", 5: "Results stored in Futures.", 6: "Workers end after shutdown."}, y=236, size=10.5)
B.caps(["Inside, the pool keeps a <b>task queue</b> and up to 2 worker threads named <code>pool-1-thread-1</code> and <code>-2</code>. Idle workers wait on the queue (like a consumer, Lesson 12.5).",
        "Submitted tasks are wrapped in <code>FutureTask</code> objects. Each worker takes one and runs its <code>call()</code>.",
        "With both workers busy, task3 sits in the queue. This is how a pool limits how many threads exist, however many tasks arrive.",
        "Worker 1 finishes task1, stores the result in f1's FutureTask, and loops back to take task3. No thread was created or destroyed.",
        "All results are stored. <code>get()</code> on a completed Future returns at once.",
        "After <code>shutdown()</code>, the workers find the queue empty and closed, so they exit and become TERMINATED."])
ANIM = two_view("A thread pool at work", S, B)

# ---------------- Part 6: animated example ----------------
ANIM2_HEADING = "Watch it with an example: a travel site searching three airlines"
ANIM2_INTRO = "A flight search asks three airline APIs for prices at the same time, using a pool and Futures, and shows the cheapest. One airline is slow, so the search uses a timeout."
A = Anim("Fare search with Futures", frames=5, h=230, label="Three Callable tasks run on a pool; two return prices, one times out; the cheapest available fare is shown")
air = [("IndiAir", "₹4,850", 18), ("SkyJet", "₹4,420", 70), ("BlueWing", "slow…", 122)]
for name, price, y in air:
    A.box(10, y, 110, 42, None, fill="card2", stroke="line")
    A.text(20, y + 26, name, size=10, bold=True)
    A.box(150, y, 90, 42, None, fill="soft-blue", stroke="blue", on="2-")
    A.text(160, y + 18, "Future", size=9, bold=True, mono=True, cls="blue", on="2-")
    A.arrow(120, y + 21, 148, y + 21, on="2-", color="ink")
A.text(160, 54, "pending", size=9, mono=True, cls="acc", on="2")
A.text(160, 106, "pending", size=9, mono=True, cls="acc", on="2")
A.text(160, 158, "pending", size=9, mono=True, cls="acc", on="2-3")
A.text(160, 54, "₹4,850", size=9.5, mono=True, cls="green", bold=True, on="3-")
A.text(160, 106, "₹4,420", size=9.5, mono=True, cls="green", bold=True, on="3-")
A.text(160, 158, "timeout ✗", size=9.5, mono=True, cls="red", bold=True, on="4-")
A.box(256, 60, 96, 70, None, fill="soft-green", stroke="green", on="5")
A.text(304, 84, "cheapest", size=9.5, anchor="middle", cls="green", bold=True, on="5")
A.text(304, 104, "SkyJet", size=11, anchor="middle", bold=True, on="5")
A.text(304, 120, "₹4,420", size=10.5, anchor="middle", mono=True, on="5")
A.text(256, 30, "get(800 ms)", size=9.5, mono=True, on="3-4", cls="ink2")
A.note({1: "Search for Pune → Delhi.", 2: "Three tasks submitted at once.", 3: "Two answers arrive.",
        4: "BlueWing misses the deadline.", 5: "Show the best answer we have."}, y=204, size=10.5)
A.caps(["The user searches Pune → Delhi. The site must ask three airline APIs; each call takes a few hundred milliseconds.",
        "Each call is a <code>Callable&lt;Integer&gt;</code> submitted to a pool. Three Futures come back at once, all pending.",
        "IndiAir and SkyJet answer; their Futures complete. Because the calls overlapped, the wait was about as long as the slowest of them, not the sum.",
        "<code>get(800, MILLISECONDS)</code> on BlueWing's Future throws <code>TimeoutException</code>. The site cancels that task instead of making the user wait.",
        "The cheapest fare among the answers is shown. This is how comparison sites stay fast even when one partner is slow. (Illustrative times and prices.)"])
ANIM2 = A

# ---------------- Part 8: tracer ----------------
TRACE = dict(code='''import java.util.concurrent.*;

public class Main {
    static int priceOf(String item) {
        return item.length() * 100;
    }

    public static void main(String[] args) throws Exception {
        ExecutorService pool = Executors.newFixedThreadPool(2);
        Callable<Integer> mouse = () -> priceOf("mouse");
        Callable<Integer> keyboard = () -> priceOf("keyboard");
        Future<Integer> f1 = pool.submit(mouse);
        Future<Integer> f2 = pool.submit(keyboard);
        int total = f1.get() + f2.get();
        pool.shutdown();
        System.out.println("cart total: Rs " + total + ", done " + f1.isDone());
    }
}
''', notes={
 9: "Pool :: = An ExecutorService with up to 2 worker threads. They are created lazily, when tasks arrive.",
 10: "Task 1 :: A Callable: like a Runnable, but <code>call()</code> returns a value (an Integer here).",
 11: "Task 2 :: A second Callable object.",
 12: "Submit :: = <code>submit</code> wraps the task in a FutureTask, gives it to a worker, and returns that Future at once. The price is computed on the worker thread.",
 13: "Submit :: = The second task goes to the second worker. Both may already be finished by the next line, or not: the Futures handle that.",
 14: "Collect :: = <code>get()</code> returns each result, waiting if necessary: 500 + 800.",
 15: "Shut down :: = No more tasks. The two worker threads end once idle, so the JVM can exit.",
 16: "Print :: The Future reports it is done."})

# ---------------- Worked examples ----------------
WORKED_INTRO = "Three common executor patterns: a pool processing many small jobs, Callables with Futures collected by <code>invokeAll</code>, and a Future with a timeout. Results are always read in submission order, so the output never changes."
EXAMPLES = [
dict(tag="E-commerce · invoices", title="Ten invoices on a pool of three workers",
 problem="<p>At closing time a shop generates 10 invoices. Creating a thread for each is wasteful; use a fixed pool of 3. Count the invoices with an <code>AtomicInteger</code>, shut down properly, and print the total.</p>",
 inp="invoice ids 1..10",
 approach=["Create <code>Executors.newFixedThreadPool(3)</code>.",
           "Submit 10 Runnables; each increments a shared AtomicInteger.",
           "<code>shutdown()</code>, then <code>awaitTermination</code> to wait until all tasks have finished."],
 code='''import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicInteger;

public class Main {
    public static void main(String[] args) throws InterruptedException {
        ExecutorService pool = Executors.newFixedThreadPool(3);
        AtomicInteger made = new AtomicInteger();
        for (int id = 1; id <= 10; id++) {
            int invoice = id;
            pool.submit(() -> {
                String pdf = "INV-" + invoice + ".pdf";
                made.incrementAndGet();
            });
        }
        pool.shutdown();
        boolean finished = pool.awaitTermination(5, TimeUnit.SECONDS);
        System.out.println("finished: " + finished + ", invoices made: " + made.get());
    }
}
''', notes={6: "Pool :: = A pool of 3 reusable workers.",
            7: "Counter :: A thread-safe counter shared by all tasks.",
            (10, 1): "First task :: = Submitted; a worker starts it straight away.",
            (10, 10): "Tenth task :: = All 10 submitted. At most 3 run at once; the rest wait in the queue.",
            15: "Shutdown :: = No new tasks accepted; queued ones still run.",
            16: "Wait :: = Blocks until every task has finished (or 5 seconds pass). Returns true here.",
            17: "Report :: 10 invoices, made by only 3 threads."},
 tryit="Press <b>Run</b>. Then print <code>Thread.currentThread().getName()</code> inside the task: you'll see only pool-1-thread-1 to -3 doing all ten jobs (in some order)."),
dict(tag="Analytics · dashboard", title="Three dashboard numbers with invokeAll",
 problem="<p>A sales dashboard needs today's orders, revenue and new customers. Each is a separate query (a <code>Callable&lt;Integer&gt;</code>). Run all three at once with <code>invokeAll</code> and print them in a fixed order.</p>",
 inp="orders = 3 bills; revenue = 1200 + 850 + 400; new customers = 2",
 approach=["Write three Callables in a <code>List</code>.",
           "<code>invokeAll</code> runs them and returns a list of Futures in the <b>same order</b>, once all are done.",
           "Read each Future with <code>get()</code>."],
 code='''import java.util.*;
import java.util.concurrent.*;

public class Main {
    public static void main(String[] args) throws Exception {
        int[] bills = {1200, 850, 400};
        List<Callable<Integer>> queries = List.of(
            () -> bills.length,
            () -> Arrays.stream(bills).sum(),
            () -> 2
        );
        ExecutorService pool = Executors.newFixedThreadPool(3);
        List<Future<Integer>> answers = pool.invokeAll(queries);
        pool.shutdown();
        String[] labels = {"orders", "revenue", "new customers"};
        for (int i = 0; i < labels.length; i++) {
            System.out.println(labels[i] + ": " + answers.get(i).get());
        }
    }
}
''', notes={6: "Data :: Today's three bills.",
            7: "Queries :: = An immutable list of three Callable objects.",
            12: "Pool :: = Three workers, one per query.",
            13: "invokeAll :: = Runs all three in parallel and waits until all are done. The Futures come back in the order of the list.",
            14: "Shutdown :: = Done with the pool.",
            (17, 1): "Read :: = <code>get()</code> on a finished Future returns at once."},
 tryit="Press <b>Run</b>. Then add a fourth query (average bill) and a fourth label."),
dict(tag="Banking · timeouts", title="A credit-score check with a deadline",
 problem="<p>A loan app asks a credit bureau for a score. The bureau sometimes takes too long. Wait at most 200 ms with <code>get(timeout)</code>; on timeout, cancel the task and send the application for manual review.</p>",
 inp="the bureau call takes 5 s (too slow)",
 approach=["Submit a Callable that sleeps 5 s, then returns 742.",
           "<code>get(200, TimeUnit.MILLISECONDS)</code> throws <code>TimeoutException</code>.",
           "In the catch: <code>cancel(true)</code> interrupts the worker; then <code>shutdown()</code>."],
 code='''import java.util.concurrent.*;

public class Main {
    public static void main(String[] args) throws Exception {
        ExecutorService pool = Executors.newSingleThreadExecutor();
        Future<Integer> score = pool.submit(() -> {
            Thread.sleep(5000);
            return 742;
        });
        try {
            System.out.println("score: " + score.get(200, TimeUnit.MILLISECONDS));
        } catch (TimeoutException e) {
            boolean stopped = score.cancel(true);
            System.out.println("bureau too slow, cancelled: " + stopped + " -> manual review");
        }
        pool.shutdown();
    }
}
''', notes={5: "Pool :: = A pool with exactly one worker thread.",
            6: "Submit :: = The bureau call starts on the worker and sleeps (simulating a slow network).",
            11: "Timed get :: = main waits at most 200 ms. The result isn't ready, so <code>get</code> throws TimeoutException.",
            13: "Cancel :: = <code>cancel(true)</code> interrupts the worker: its sleep throws and the task ends early.",
            14: "Fallback :: The application continues without the score.",
            16: "Shutdown :: = The worker is idle again and exits."},
 tryit="Press <b>Run</b>. Then change the sleep to 50 ms: <code>get</code> returns 742 in time."),
]

# ---------------- Practice problems ----------------
PRACTICE_INTRO = "Use pools, Callables and Futures instead of raw threads. Results are read from Futures in a fixed order, so every output is the same each run. The last three are business tasks."
PROBLEMS = [
dict(level="easy", title="Submit a Callable", stmt="<p>Submit a Callable that returns 6 × 7 to a single-thread pool and print the result.</p>", inp="(none)",
 code='''import java.util.concurrent.*;

public class Main {
    public static void main(String[] args) throws Exception {
        ExecutorService pool = Executors.newSingleThreadExecutor();
        Future<Integer> f = pool.submit(() -> 6 * 7);
        System.out.println("answer: " + f.get());
        pool.shutdown();
    }
}''', explain="<p><b>How it works:</b> a lambda that returns a value is treated as a <code>Callable</code>. <code>get()</code> waits for the result.</p>"),
dict(level="easy", title="Shutdown and awaitTermination", stmt="<p>Submit 5 Runnables that each add their number to an AtomicInteger, shut down, wait, and print the sum.</p>", inp="1..5",
 code='''import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicInteger;

public class Main {
    public static void main(String[] args) throws InterruptedException {
        ExecutorService pool = Executors.newFixedThreadPool(2);
        AtomicInteger sum = new AtomicInteger();
        for (int i = 1; i <= 5; i++) {
            int n = i;
            pool.submit(() -> sum.addAndGet(n));
        }
        pool.shutdown();
        pool.awaitTermination(1, TimeUnit.SECONDS);
        System.out.println("sum = " + sum.get());
    }
}''', explain="<p><b>How it works:</b> <code>shutdown()</code> alone doesn't wait. <code>awaitTermination</code> blocks until the queued tasks are finished (or the timeout passes).</p>"),
dict(level="easy", title="Runnable Future returns null", stmt="<p>Submit a Runnable and print what its Future's <code>get()</code> returns, and whether it's done.</p>", inp="(none)",
 code='''import java.util.concurrent.*;

public class Main {
    public static void main(String[] args) throws Exception {
        ExecutorService pool = Executors.newSingleThreadExecutor();
        Future<?> f = pool.submit(() -> System.out.println("cleaning cache"));
        System.out.println("get() = " + f.get() + ", done = " + f.isDone());
        pool.shutdown();
    }
}''', explain="<p><b>How it works:</b> a Runnable has no result, so <code>get()</code> returns null. It's still useful: it waits for completion and rethrows failures.</p>"),
dict(level="medium", title="Exceptions come back through get()", stmt="<p>A task divides by zero. Catch the <code>ExecutionException</code> from <code>get()</code> and print its cause.</p>", inp="(none)",
 code='''import java.util.concurrent.*;

public class Main {
    public static void main(String[] args) throws InterruptedException {
        ExecutorService pool = Executors.newSingleThreadExecutor();
        Future<Integer> f = pool.submit(() -> 100 / 0);
        try {
            f.get();
        } catch (ExecutionException e) {
            System.out.println("task failed: " + e.getCause());
        }
        pool.shutdown();
    }
}''', explain="<p><b>How it works:</b> the exception happened on a worker thread. The pool catches it and stores it in the Future; <code>get()</code> rethrows it wrapped in <code>ExecutionException</code>. If you never call <code>get()</code>, the failure is silently lost.</p>"),
dict(level="medium", title="Squares with invokeAll", stmt="<p>Build Callables that square 2, 3, 4 and 5, run them with <code>invokeAll</code>, and print the results in order.</p>", inp="2, 3, 4, 5",
 code='''import java.util.*;
import java.util.concurrent.*;

public class Main {
    public static void main(String[] args) throws Exception {
        List<Callable<Integer>> jobs = new ArrayList<>();
        for (int n = 2; n <= 5; n++) {
            int x = n;
            jobs.add(() -> x * x);
        }
        ExecutorService pool = Executors.newFixedThreadPool(2);
        for (Future<Integer> f : pool.invokeAll(jobs)) {
            System.out.print(f.get() + " ");
        }
        System.out.println();
        pool.shutdown();
    }
}''', explain="<p><b>How it works:</b> invokeAll returns Futures in the same order as the tasks, however the workers scheduled them.</p>"),
dict(level="medium", title="CompletableFuture pipeline", stmt="<p>Compute a price of 400 asynchronously, add 18% GST with <code>thenApply</code>, and format it with another <code>thenApply</code>. Print with <code>join()</code>.</p>", inp="price 400",
 code='''import java.util.concurrent.CompletableFuture;

public class Main {
    public static void main(String[] args) {
        String bill = CompletableFuture.supplyAsync(() -> 400)
                .thenApply(p -> p * 118 / 100)
                .thenApply(t -> "Total with GST: Rs " + t)
                .join();
        System.out.println(bill);
    }
}''', explain="<p><b>How it works:</b> <code>CompletableFuture</code> lets you chain steps that run when the previous one completes, without blocking in between. By default it uses the shared ForkJoinPool. <code>join()</code> is like <code>get()</code> but throws an unchecked exception.</p>"),
dict(level="business", title="Parallel GST for store branches", stmt="<p>Three branches have daily sales of 25000, 18000 and 32000. Compute each branch's 18% GST in a Callable on a pool, then print each and the total GST.</p>", inp="25000, 18000, 32000",
 code='''import java.util.*;
import java.util.concurrent.*;

public class Main {
    public static void main(String[] args) throws Exception {
        String[] branch = {"Pune", "Nagpur", "Nashik"};
        int[] sales = {25000, 18000, 32000};
        ExecutorService pool = Executors.newFixedThreadPool(3);
        List<Future<Integer>> gst = new ArrayList<>();
        for (int s : sales) gst.add(pool.submit(() -> s * 18 / 100));
        int total = 0;
        for (int i = 0; i < branch.length; i++) {
            int g = gst.get(i).get();
            total += g;
            System.out.println(branch[i] + ": GST Rs " + g);
        }
        System.out.println("total GST: Rs " + total);
        pool.shutdown();
    }
}''', explain="<p><b>How it works:</b> results are summed on main from the Futures, so no shared variable or lock is needed. Collecting results through Futures is usually simpler than sharing state between tasks.</p>"),
dict(level="business", title="Email batch with a bounded pool", stmt="<p>Send 8 promotional emails using a pool of 2 workers. Each task returns <code>true</code> if the address contains \"@\". Count successes and failures.</p>", inp="8 addresses, 2 invalid",
 code='''import java.util.*;
import java.util.concurrent.*;

public class Main {
    public static void main(String[] args) throws Exception {
        String[] to = {"a@x.in", "b@x.in", "bad-address", "c@x.in", "d@x.in", "e@x.in", "oops", "f@x.in"};
        ExecutorService pool = Executors.newFixedThreadPool(2);
        List<Callable<Boolean>> sends = new ArrayList<>();
        for (String addr : to) sends.add(() -> addr.contains("@"));
        int ok = 0;
        for (Future<Boolean> f : pool.invokeAll(sends)) if (f.get()) ok++;
        pool.shutdown();
        System.out.println("sent " + ok + ", failed " + (to.length - ok));
    }
}''', explain="<p><b>How it works:</b> the pool size caps how many emails are sent at once, protecting the mail server, however many addresses there are. This is why pools are preferred over one thread per task.</p>"),
dict(level="business", title="Seat confirmation with timeout fallback", stmt="<p>A train-booking app asks two seat servers. The first answers at once (seat \"B4-32\"), the second hangs. Wait up to 150 ms for each; print the answer or \"no reply\", and cancel the hanging task.</p>", inp="server 1 fast, server 2 hangs",
 code='''import java.util.concurrent.*;

public class Main {
    public static void main(String[] args) throws Exception {
        ExecutorService pool = Executors.newFixedThreadPool(2);
        Future<String> s1 = pool.submit(() -> "B4-32");
        Future<String> s2 = pool.submit(() -> {
            Thread.sleep(10_000);
            return "S2-11";
        });
        for (Future<String> f : java.util.List.of(s1, s2)) {
            try {
                System.out.println("seat: " + f.get(150, TimeUnit.MILLISECONDS));
            } catch (TimeoutException e) {
                f.cancel(true);
                System.out.println("no reply, cancelled");
            }
        }
        pool.shutdown();
    }
}''', explain="<p><b>How it works:</b> each server gets its own deadline. <code>cancel(true)</code> interrupts the stuck task so the worker is freed and <code>shutdown()</code> can finish.</p>"),
]

# ---------------- Extra blocks ----------------
BLOCKS = {
'ANIM': ANIM,
'CODE_POOL_NAMES': code('''import java.util.concurrent.*;

public class Main {
    public static void main(String[] args) throws InterruptedException {
        ExecutorService pool = Executors.newFixedThreadPool(2);
        for (int i = 1; i <= 5; i++) {
            int job = i;
            pool.submit(() -> System.out.println("job " + job + " on " + Thread.currentThread().getName()));
        }
        pool.shutdown();
        pool.awaitTermination(5, TimeUnit.SECONDS);
    }
}''', skip=True),
'CODE_FACTORIES': snippet('''Executors.newFixedThreadPool(n)          // n workers, unbounded queue: steady CPU/IO work
Executors.newCachedThreadPool()          // grows as needed, idle threads die: short bursts
Executors.newSingleThreadExecutor()      // one worker: tasks run strictly in order
Executors.newScheduledThreadPool(n)      // delays and repeats: schedule(task, 5, SECONDS)
Executors.newVirtualThreadPerTaskExecutor()  // Java 21: a cheap virtual thread per task'''),
'CODE_RUN': code('''import java.util.*;
import java.util.concurrent.*;

public class Main {
    static int fetchPrice(String shop) throws InterruptedException {
        Thread.sleep(100);                    // pretend network call
        return switch (shop) {
            case "Shopkart" -> 18999;
            case "BuyNow" -> 18499;
            default -> 19250;
        };
    }

    public static void main(String[] args) throws Exception {
        List<String> shops = List.of("Shopkart", "BuyNow", "MegaMart");
        ExecutorService pool = Executors.newFixedThreadPool(3);
        List<Future<Integer>> prices = new ArrayList<>();
        for (String s : shops) {
            prices.add(pool.submit(() -> fetchPrice(s)));
        }
        for (int i = 0; i < shops.size(); i++) {
            System.out.println(shops.get(i) + ": Rs " + prices.get(i).get());
        }
        pool.shutdown();
    }
}'''),
'RUNNER': runner([
 dict(label="1 · Price check on a pool", hint="Press <b>Run</b>. The three 100 ms calls overlap, so it takes about 0.1 s, not 0.3 s. Then change the pool size to 1 and compare.",
      code='''import java.util.*;
import java.util.concurrent.*;

public class Main {
    static int fetchPrice(String shop) throws InterruptedException {
        Thread.sleep(100);
        return switch (shop) {
            case "Shopkart" -> 18999;
            case "BuyNow" -> 18499;
            default -> 19250;
        };
    }

    public static void main(String[] args) throws Exception {
        long t0 = System.currentTimeMillis();
        List<String> shops = List.of("Shopkart", "BuyNow", "MegaMart");
        ExecutorService pool = Executors.newFixedThreadPool(3);
        List<Future<Integer>> prices = new ArrayList<>();
        for (String s : shops) prices.add(pool.submit(() -> fetchPrice(s)));
        for (int i = 0; i < shops.size(); i++) {
            System.out.println(shops.get(i) + ": Rs " + prices.get(i).get());
        }
        pool.shutdown();
        System.out.println("took about " + (System.currentTimeMillis() - t0) / 100 * 100 + " ms");
    }
}'''),
 dict(label="2 · Predict: which threads?", hint="<b>Predict first:</b> 6 jobs, pool of 2. How many different thread names appear?",
      code='''import java.util.*;
import java.util.concurrent.*;

public class Main {
    public static void main(String[] args) throws InterruptedException {
        ExecutorService pool = Executors.newFixedThreadPool(2);
        Set<String> names = ConcurrentHashMap.newKeySet();
        for (int i = 0; i < 6; i++) {
            pool.submit(() -> names.add(Thread.currentThread().getName()));
        }
        pool.shutdown();
        pool.awaitTermination(1, TimeUnit.SECONDS);
        System.out.println(names.size() + " worker(s): " + new TreeSet<>(names));
    }
}'''),
 dict(label="3 · Predict: a failure nobody saw", hint="<b>Predict first:</b> does anything get printed about the division by zero? Then add <code>f.get()</code> inside a try/catch for <code>ExecutionException</code>.",
      code='''import java.util.concurrent.*;

public class Main {
    public static void main(String[] args) throws InterruptedException {
        ExecutorService pool = Executors.newSingleThreadExecutor();
        Future<Integer> f = pool.submit(() -> 500 / 0);
        pool.shutdown();
        pool.awaitTermination(1, TimeUnit.SECONDS);
        System.out.println("pool finished, done = " + f.isDone());
    }
}'''),
 dict(label="4 · Crash: submit after shutdown", hint="A pool that has been shut down rejects new work. Submit all tasks before calling <code>shutdown()</code>.",
      code='''import java.util.concurrent.*;

public class Main {
    public static void main(String[] args) {
        ExecutorService pool = Executors.newFixedThreadPool(2);
        pool.submit(() -> System.out.println("order 1 packed"));
        pool.shutdown();
        pool.submit(() -> System.out.println("order 2 packed"));
    }
}''', _expect="exception"),
 dict(label="5 · Spot the error", hint="<code>Future.get()</code> throws the checked <code>InterruptedException</code> and <code>ExecutionException</code>. Add <code>throws Exception</code> to main, or catch them.",
      code='''import java.util.concurrent.*;

public class Main {
    public static void main(String[] args) {
        ExecutorService pool = Executors.newFixedThreadPool(1);
        Future<Integer> f = pool.submit(() -> 21 * 2);
        int answer = f.get();
        System.out.println(answer);
        pool.shutdown();
    }
}''', _expect="compile-error"),
]),
'QUIZ': quiz([
 {"q": "What is the main benefit of a thread pool?", "options": ["Threads never fail", "Threads are created once and reused, and their number is limited", "No need for locks", "Tasks run in order"], "answer": 1, "why": "Reuse avoids creation cost; a limit protects memory and CPU."},
 {"q": "Callable differs from Runnable because…", "options": ["it can't be a lambda", "call() returns a value and may throw checked exceptions", "it runs faster", "it needs Thread"], "answer": 1, "why": "Runnable.run() returns void and can't throw checked exceptions."},
 {"q": "What does submit() return?", "options": ["The result", "A Future", "A Thread", "void"], "answer": 1, "why": "A Future represents the pending result."},
 {"q": "future.get() on a task that's still running…", "options": ["returns null", "waits until it finishes", "throws immediately", "cancels it"], "answer": 1, "why": "Use get(timeout, unit) to limit the wait."},
 {"q": "A task throws an exception. What does get() do?", "options": ["Returns null", "Throws ExecutionException with the original as the cause", "Kills the pool", "Nothing"], "answer": 1, "why": "Failures are stored in the Future and rethrown wrapped."},
 {"q": "After shutdown(), what happens to tasks already in the queue?", "options": ["They are dropped", "They still run", "They throw", "They wait forever"], "answer": 1, "why": "shutdown() stops new submissions; shutdownNow() tries to stop everything and returns queued tasks."},
 {"q": "What happens if you forget shutdown() on a fixed pool?", "options": ["Nothing", "Its worker threads stay alive and the JVM may never exit", "A compile error", "Tasks are lost"], "answer": 1, "why": "Pool threads are non-daemon by default."},
 {"q": "Results of invokeAll(list) come back…", "options": ["in completion order", "in the same order as the list", "randomly", "only the first"], "answer": 1, "why": "invokeAll waits for all and returns Futures in task order."},
]),
}
