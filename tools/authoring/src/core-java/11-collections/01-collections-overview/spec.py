import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../..'))
from mkanim import Anim, two_view

# ---------------- Part 5: two-view animation ----------------
CODE = ["Collection<String> c = …;", "List<String> l = new ArrayList<>();", "Set<String> s = new HashSet<>();",
        "Deque<String> q = new ArrayDeque<>();", "Map<String,Integer> m = new HashMap<>();", "Collections.sort(l);"]
CODE = [c.replace('<', '&lt;').replace('>', '&gt;') for c in CODE]
S = Anim("see", frames=6, h=250, label="Declaring different collection types, each with an interface on the left and a class on the right")
S.box(8, 8, 344, 132, None, fill="board", stroke="board")
for i, line in enumerate(CODE):
    y = 30 + i * 20
    S.box(12, y - 14, 336, 19, None, fill="none", stroke="track", sw=2, on=str(i + 1), rx=4)
    S.text(20, y, line, mono=True, size=10, cls="chalk")
S.box(8, 150, 344, 50, None, fill="card2", stroke="line")
notes = {1: "the common root: add, remove, size, contains", 2: "ordered, index, duplicates allowed", 3: "unique elements only",
         4: "work at both ends: queue or stack", 5: "key → value, not a Collection", 6: "a utility class, not the interface"}
for f, t in notes.items():
    S.text(180, 180, t, on=str(f), anchor="middle", size=10.5, bold=True, cls="ink")
S.note({1: "Interface on the left…", 2: "…class on the right.", 3: "A Set promises uniqueness.", 4: "A Deque promises two open ends.",
        5: "A Map stores pairs.", 6: "Collections with an s."}, y=226, size=10.5)
S.caps(["<code>Collection</code> is the root promise shared by lists, sets and queues.",
        "A <code>List</code> variable holding an <code>ArrayList</code> object.",
        "A <code>Set</code> variable holding a <code>HashSet</code>.",
        "A <code>Deque</code> holding an <code>ArrayDeque</code>: usable as a queue or a stack.",
        "A <code>Map</code> holding a <code>HashMap</code>.",
        "<code>Collections.sort</code>: a static helper in the utility class <code>Collections</code>."])
B = Anim("behind", frames=6, h=250, label="The interface hierarchy: Iterable, Collection with List, Set and Queue/Deque, and the separate Map family")
B.box(118, 8, 124, 24, "Iterable", fill="card2", stroke="line", size=10, bold=True, mono=True)
B.box(118, 42, 124, 26, "Collection", fill="soft-blue", stroke="blue", size=10.5, bold=True, mono=True)
B.arrow(180, 42, 180, 32, color="ink", sw=1.5)
B.box(8, 92, 104, 26, "List", fill="card", stroke="line", size=10.5, bold=True, mono=True)
B.box(128, 92, 104, 26, "Set", fill="card", stroke="line", size=10.5, bold=True, mono=True)
B.box(248, 92, 104, 26, "Queue/Deque", fill="card", stroke="line", size=10, bold=True, mono=True)
for x in (60, 180, 300):
    B.arrow(x, 92, 180, 68, color="ink", sw=1.2)
B.box(8, 128, 104, 40, "ArrayList", sub="LinkedList", fill="soft-acc", stroke="track", size=9.5, mono=True, on="2-")
B.box(128, 128, 104, 40, "HashSet", sub="LinkedHashSet, TreeSet", fill="soft-acc", stroke="track", size=9.5, mono=True, on="3-")
B.box(248, 128, 104, 40, "ArrayDeque", sub="PriorityQueue", fill="soft-acc", stroke="track", size=9.5, mono=True, on="4-")
B.box(8, 180, 160, 30, "Map → HashMap, TreeMap", fill="soft-green", stroke="green", size=9.5, bold=True, mono=True, on="5-")
B.box(190, 180, 162, 30, "Collections (utility class)", fill="card2", stroke="track", size=9.5, bold=True, mono=True, on="6")
hl = {1: (118, 42, 124, 26), 2: (8, 92, 104, 26), 3: (128, 92, 104, 26), 4: (248, 92, 104, 26), 5: (8, 180, 160, 30), 6: (190, 180, 162, 30)}
for f, (x, y, w, h) in hl.items():
    B.box(x, y, w, h, None, fill="none", stroke="track", sw=3, on=str(f))
B.note({1: "Collection extends Iterable: for-each works.", 2: "ArrayList keeps the List promise.", 3: "HashSet keeps the Set promise.",
        4: "ArrayDeque keeps the Deque promise.", 5: "Map stands apart from Collection.", 6: "Static helpers for any collection."}, y=232, size=10)
B.caps(["<code>Collection</code> extends <code>Iterable</code>, which is why every list, set and queue works in a for-each loop.",
        "<code>List</code> is a child of <code>Collection</code>; <code>ArrayList</code> and <code>LinkedList</code> are classes that implement it.",
        "<code>Set</code> also extends <code>Collection</code>; HashSet, LinkedHashSet and TreeSet implement it.",
        "<code>Queue</code> and its child <code>Deque</code>: ArrayDeque and PriorityQueue (and LinkedList, which is both a List and a Deque).",
        "<code>Map</code> is <b>not</b> under Collection. It's a separate family of key–value containers.",
        "<code>Collections</code> isn't in the tree at all: it's a class full of static algorithms (sort, max, frequency…) that work on collections."])
ANIM = two_view("Where each collection fits", S, B)
BLOCKS = {'ANIM': ANIM}

# ---------------- Part 6: animated example ----------------
ANIM2_HEADING = "Watch it with an example: a bank's customer-service desk"
ANIM2_INTRO = "One morning at a bank branch, four collections work together: a queue of tokens, a set of customers seen today, a map of account balances, and a list of the day's log."
A = Anim("A morning at the help desk", frames=5, h=226, label="Tokens served from a queue, customers recorded in a set, balances looked up in a map, and events appended to a list")
A.box(8, 12, 166, 62, None, fill="soft-acc", stroke="track")
A.text(16, 28, "Queue: tokens", size=9.5, bold=True, cls="acc")
A.text(16, 50, "T1 T2 T3", on="1", mono=True, size=11, bold=True)
A.text(16, 50, "T2 T3", on="2", mono=True, size=11, bold=True)
A.text(16, 50, "T3", on="3", mono=True, size=11, bold=True)
A.text(16, 50, "(empty)", on="4-5", mono=True, size=11, cls="ink3")
A.box(186, 12, 166, 62, None, fill="soft-green", stroke="green")
A.text(194, 28, "Set: seen today", size=9.5, bold=True, cls="green")
A.text(194, 50, "{}", on="1", mono=True, size=11)
A.text(194, 50, "{Riya}", on="2", mono=True, size=11)
A.text(194, 50, "{Riya, Kabir}", on="3", mono=True, size=11)
A.text(194, 50, "{Riya, Kabir}", on="4-5", mono=True, size=11)
A.text(194, 66, "Riya again: add → false", on="4", size=9, cls="green", bold=True)
A.box(8, 84, 166, 62, None, fill="soft-blue", stroke="blue")
A.text(16, 100, "Map: balance", size=9.5, bold=True, cls="blue")
A.text(16, 120, "Riya → ₹8,200", mono=True, size=10)
A.text(16, 136, "Kabir → ₹1,050", mono=True, size=10)
A.box(8, 108, 166, 18, None, fill="none", stroke="track", sw=2.5, on="2,4")
A.box(8, 124, 166, 18, None, fill="none", stroke="track", sw=2.5, on="3")
A.box(186, 84, 166, 62, None, fill="card", stroke="line")
A.text(194, 100, "List: today's log", size=9.5, bold=True, cls="ink2")
A.text(194, 120, "[]", on="1", mono=True, size=9.5)
A.text(194, 120, "[T1 Riya]", on="2", mono=True, size=9.5)
A.text(194, 120, "[T1 Riya, T2 Kabir]", on="3", mono=True, size=9.5)
A.lines(194, 120, ["[T1 Riya, T2 Kabir,", " T3 Riya]"], on="4-5", mono=True, size=9.5)
A.note({1: "Three customers take tokens.", 2: "Token 1: Riya. Look up her balance.", 3: "Token 2: Kabir.",
        4: "Token 3: Riya again; the set doesn't grow.", 5: "Report: 3 visits, 2 customers."}, y=176, size=11)
A.caps(["Customers take tokens T1, T2, T3. The desk's <code>Queue</code> holds them in arrival order.",
        "<code>poll()</code> serves T1: Riya. Her balance comes from the <code>Map</code> in one lookup, she's added to the <code>Set</code>, and the visit is appended to the <code>List</code>.",
        "T2: Kabir. Same steps: map lookup, set add, list append.",
        "T3 is Riya again. The log grows (it's a List), but <code>set.add(\"Riya\")</code> returns false: she's already counted.",
        "End of the morning: the list says 3 visits, the set says 2 different customers. Each collection answered a different question. (Simplified: real branches use a database, not memory.)"])
ANIM2 = A

# ---------------- Part 8: tracer ----------------
TRACE = dict(code='''import java.util.*;

public class Main {
    public static void main(String[] args) {
        List<String> log = new ArrayList<>();
        Set<String> unique = new HashSet<>();
        Map<String, Integer> count = new HashMap<>();
        String[] visits = {"Riya", "Kabir", "Riya"};
        for (String v : visits) {
            log.add(v);
            unique.add(v);
            count.put(v, count.getOrDefault(v, 0) + 1);
        }
        System.out.println(log + " " + unique.size() + " " + count);
    }
}
''', notes={
 5: "List :: An empty ArrayList. Capacity 0 until the first add.",
 6: "Set :: An empty HashSet (inside, it uses a HashMap).",
 7: "Map :: An empty HashMap.",
 (10, 1): "List add :: The list stores a reference to \"Riya\" at index 0.",
 (11, 1): "Set add :: Added to the set.",
 (12, 1): "Map put :: First time: count 0 + 1.",
 (10, 3): "List add :: The list happily stores \"Riya\" a second time.",
 (11, 3): "Set add :: = Already in the set: <code>add</code> returns false and nothing changes.",
 (12, 3): "Map put :: The same key is updated: Riya → 2.",
 14: "Print :: 3 list entries, 2 unique names, 2 map keys."})

# ---------------- Worked examples ----------------
WORKED_INTRO = "Three everyday problems, each solved by picking the right collection. Watch how differently they grow on the heap."
EXAMPLES = [
dict(tag="Analytics · Set", title="Unique visitors from a page log",
 problem="<p>A website logs one user ID per page view. Count unique visitors and print them in the order they first appeared.</p>",
 inp='["u7", "u3", "u7", "u9", "u3"]',
 approach=["A <code>LinkedHashSet</code> ignores repeats <i>and</i> remembers first-arrival order.",
           "A helper <code>uniqueVisitors(String[] log)</code> adds every ID.",
           "Print the size and the set."],
 code='''import java.util.LinkedHashSet;
import java.util.Set;

public class Main {
    static Set<String> uniqueVisitors(String[] log) {
        Set<String> seen = new LinkedHashSet<>();
        for (String id : log) {
            seen.add(id);
        }
        return seen;
    }

    public static void main(String[] args) {
        String[] log = {"u7", "u3", "u7", "u9", "u3"};
        Set<String> v = uniqueVisitors(log);
        System.out.println(v.size() + " unique: " + v);
    }
}
''', tryit="Press <b>Run</b>. Then switch to <code>TreeSet</code> and see the order change."),
dict(tag="Customer service · Queue", title="Serve support tickets in order",
 problem="<p>Tickets T101, T102, T103 arrive. An agent serves two, then T104 arrives. Print who is served and who is still waiting.</p>",
 inp="T101, T102, T103; serve 2; T104 arrives",
 approach=["Use <code>ArrayDeque</code> as a FIFO queue: <code>offer</code> at the back, <code>poll</code> from the front.",
           "Serve with <code>poll()</code>, which returns and removes the oldest ticket.",
           "Print what remains."],
 code='''import java.util.ArrayDeque;
import java.util.Queue;

public class Main {
    public static void main(String[] args) {
        Queue<String> tickets = new ArrayDeque<>();
        tickets.offer("T101");
        tickets.offer("T102");
        tickets.offer("T103");
        System.out.println("Serving " + tickets.poll());
        System.out.println("Serving " + tickets.poll());
        tickets.offer("T104");
        System.out.println("Waiting: " + tickets);
    }
}
''', tryit="Press <b>Run</b>. Then use <code>peek()</code> to show the next ticket without removing it."),
dict(tag="Retail · Map", title="Stock left after the day's sales",
 problem="<p>A shop starts with pens 10, books 4. Sales today: pen, book, pen. Update stock with a <code>Map</code> and print it.</p>",
 inp="stock {pen=10, book=4}; sales pen, book, pen",
 approach=["A <code>TreeMap</code> so the report prints items alphabetically.",
           "A helper <code>sell(stock, item)</code> reduces the count by one.",
           "Print the map."],
 code='''import java.util.Map;
import java.util.TreeMap;

public class Main {
    static void sell(Map<String, Integer> stock, String item) {
        stock.put(item, stock.get(item) - 1);
    }

    public static void main(String[] args) {
        Map<String, Integer> stock = new TreeMap<>();
        stock.put("pen", 10);
        stock.put("book", 4);
        sell(stock, "pen");
        sell(stock, "book");
        sell(stock, "pen");
        System.out.println(stock);
    }
}
''', tryit="Press <b>Run</b>. Then sell an item that isn't in the map and fix the crash with <code>getOrDefault</code>."),
]

# ---------------- Practice problems ----------------
PRACTICE_INTRO = "Pick the collection whose promise fits the job. The last three are business tasks."
PROBLEMS = [
dict(level="easy", title="Remove duplicate marks", stmt="<p>Marks <code>{78, 91, 78, 64, 91}</code>: print the distinct marks in sorted order.</p>", inp="{78, 91, 78, 64, 91}",
 code='''import java.util.*;

public class Main {
    public static void main(String[] args) {
        Integer[] marks = {78, 91, 78, 64, 91};
        Set<Integer> distinct = new TreeSet<>(Arrays.asList(marks));
        System.out.println(distinct);
    }
}''', explain="<p><b>How it works:</b> a TreeSet drops duplicates and keeps the rest sorted.</p>"),
dict(level="easy", title="Reverse a word with a stack", stmt="<p>Push each character of <code>\"JAVA\"</code> onto an <code>ArrayDeque</code> stack, then pop them to print it reversed.</p>", inp='"JAVA"',
 code='''import java.util.*;

public class Main {
    public static void main(String[] args) {
        Deque<Character> stack = new ArrayDeque<>();
        for (char c : "JAVA".toCharArray()) stack.push(c);
        StringBuilder out = new StringBuilder();
        while (!stack.isEmpty()) out.append(stack.pop());
        System.out.println(out);
    }
}''', explain="<p><b>How it works:</b> a stack is last-in, first-out, so popping returns characters in reverse order.</p>"),
dict(level="easy", title="Collections utility methods", stmt="<p>For the list <code>[5, 2, 9, 2]</code>, print the max, the min, how often 2 appears, and the list sorted.</p>", inp="[5, 2, 9, 2]",
 code='''import java.util.*;

public class Main {
    public static void main(String[] args) {
        List<Integer> nums = new ArrayList<>(List.of(5, 2, 9, 2));
        System.out.println(Collections.max(nums) + " " + Collections.min(nums) + " " + Collections.frequency(nums, 2));
        Collections.sort(nums);
        System.out.println(nums);
    }
}''', explain="<p><b>How it works:</b> <code>Collections</code> (with an s) provides static algorithms. <code>sort</code> needs a modifiable list, hence the copy into an ArrayList.</p>"),
dict(level="medium", title="First repeated order ID", stmt="<p>Find the first order ID that appears twice in <code>[\"A1\", \"B7\", \"C3\", \"B7\", \"A1\"]</code>.</p>", inp='["A1", "B7", "C3", "B7", "A1"]',
 code='''import java.util.*;

public class Main {
    public static void main(String[] args) {
        String[] ids = {"A1", "B7", "C3", "B7", "A1"};
        Set<String> seen = new HashSet<>();
        for (String id : ids) {
            if (!seen.add(id)) {
                System.out.println("First repeat: " + id);
                break;
            }
        }
    }
}''', explain="<p><b>How it works:</b> <code>add</code> returns false when the element is already present, so the first false is the first repeat. O(n) overall.</p>"),
dict(level="medium", title="Most urgent tasks first", stmt="<p>Tasks with priorities 4, 1, 3, 2 arrive. Print them in order of priority using a <code>PriorityQueue</code>.</p>", inp="4, 1, 3, 2",
 code='''import java.util.*;

public class Main {
    public static void main(String[] args) {
        PriorityQueue<Integer> pq = new PriorityQueue<>(List.of(4, 1, 3, 2));
        List<Integer> order = new ArrayList<>();
        while (!pq.isEmpty()) order.add(pq.poll());
        System.out.println(order);
    }
}''', explain="<p><b>How it works:</b> <code>poll</code> always removes the smallest element. Printing the queue directly wouldn't show sorted order; only polling does.</p>"),
dict(level="business", title="Branch lookup by IFSC", stmt="<p>Store three IFSC codes with their branch names in a map, then look up <code>SBIN0001234</code> and an unknown code.</p>", inp='"SBIN0001234", "XXXX0000000"',
 code='''import java.util.*;

public class Main {
    public static void main(String[] args) {
        Map<String, String> branch = new HashMap<>();
        branch.put("SBIN0001234", "SBI Kharghar");
        branch.put("HDFC0000240", "HDFC Vashi");
        branch.put("ICIC0001520", "ICICI Panvel");
        System.out.println(branch.get("SBIN0001234"));
        System.out.println(branch.getOrDefault("XXXX0000000", "Unknown IFSC"));
    }
}''', explain="<p><b>How it works:</b> a HashMap finds the value for a key in constant time on average, no matter how many branches are stored.</p>"),
dict(level="business", title="Daily sales by category, sorted", stmt="<p>Orders: (Books, 450), (Toys, 300), (Books, 200), (Electronics, 1200). Print total per category in alphabetical order.</p>", inp="4 orders",
 code='''import java.util.*;

public class Main {
    public static void main(String[] args) {
        String[] cat = {"Books", "Toys", "Books", "Electronics"};
        int[] amt = {450, 300, 200, 1200};
        Map<String, Integer> totals = new TreeMap<>();
        for (int i = 0; i < cat.length; i++) {
            totals.put(cat[i], totals.getOrDefault(cat[i], 0) + amt[i]);
        }
        System.out.println(totals);
    }
}''', explain="<p><b>How it works:</b> the map aggregates by key; TreeMap keeps keys sorted for the report.</p>"),
dict(level="business", title="Recently viewed products", stmt="<p>A shop shows the last 3 products a user viewed, newest first, without repeats. Views: P1, P2, P3, P2, P4.</p>", inp="P1, P2, P3, P2, P4",
 code='''import java.util.*;

public class Main {
    public static void main(String[] args) {
        Deque<String> recent = new ArrayDeque<>();
        for (String p : new String[]{"P1", "P2", "P3", "P2", "P4"}) {
            recent.remove(p);          // drop an older view of the same product
            recent.addFirst(p);        // newest at the front
            if (recent.size() > 3) recent.removeLast();
        }
        System.out.println(recent);
    }
}''', explain="<p><b>How it works:</b> a Deque lets us add at the front and trim from the back. Removing an existing copy first avoids repeats.</p>"),
]
