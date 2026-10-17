import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../..'))
from mkanim import Anim, two_view

def esc(t): return t.replace('<', '&lt;').replace('>', '&gt;')

# ---------------- Part 5: two-view animation ----------------
CODE = ["LinkedList<String> t = new LinkedList<>();", 't.add("S1");', 't.add("S2");', 't.addFirst("E");', "t.get(2);", "t.removeFirst();"]
S = Anim("see", frames=6, h=250, label="Building a LinkedList: two adds, an addFirst, a get by index and a removeFirst")
S.box(8, 8, 344, 132, None, fill="board", stroke="board")
for i, line in enumerate(CODE):
    y = 30 + i * 20
    S.box(12, y - 14, 336, 19, None, fill="none", stroke="track", sw=2, on=str(i + 1), rx=4)
    S.text(20, y, esc(line), mono=True, size=10, cls="chalk")
S.box(8, 150, 344, 50, None, fill="card2", stroke="line")
S.text(18, 168, "the list", size=9, cls="ink3", bold=True)
for f, t in {1: "[]", 2: "[S1]", 3: "[S1, S2]", 4: "[E, S1, S2]", 5: "[E, S1, S2]   get(2) → S2", 6: "[S1, S2]"}.items():
    S.text(18, 190, t, on=str(f), mono=True, size=11, bold=True)
S.note({1: "Empty.", 2: "One element.", 3: "Two elements.", 4: "Add at the front.", 5: "Read index 2.", 6: "Remove the front."}, y=228, size=10.5)
S.caps(["An empty LinkedList.", "<code>add</code> appends S1.", "<code>add</code> appends S2.",
        "<code>addFirst</code> puts E at the front.", "<code>get(2)</code> returns S2.", "<code>removeFirst</code> removes E."])
B = Anim("behind", frames=6, h=250, label="Node objects with prev and next links; first and last references move; get walks the chain")
B.box(8, 10, 70, 24, "first", fill="soft-blue", stroke="blue", size=9.5, mono=True, bold=True)
B.box(282, 10, 70, 24, "last", fill="soft-blue", stroke="blue", size=9.5, mono=True, bold=True)
B.text(43, 50, "null", on="1", anchor="middle", mono=True, size=9.5, cls="ink3")
B.text(317, 50, "null", on="1", anchor="middle", mono=True, size=9.5, cls="ink3")
# node positions: E at x=14, S1 at x=130, S2 at x=246 (y=80)
def node(x, label, on):
    B.box(x, 80, 100, 50, None, fill="soft-acc", stroke="track", on=on)
    B.text(x + 50, 98, label, on=on, anchor="middle", mono=True, size=11, bold=True)
    B.text(x + 8, 122, "prev", on=on, mono=True, size=8.5, cls="ink2")
    B.text(x + 92, 122, "next", on=on, mono=True, size=8.5, cls="ink2", anchor="end")
node(130, "S1", "2-")
node(246, "S2", "3-")
node(14, "E", "4-5")
B.arrow(230, 96, 246, 96, on="3-", color="blue")
B.arrow(246, 116, 230, 116, on="3-", color="green")
B.arrow(114, 96, 130, 96, on="4-5", color="blue")
B.arrow(130, 116, 114, 116, on="4-5", color="green")
B.arrow(43, 34, 180, 80, on="2-3", color="blue", bend=-10)
B.arrow(43, 34, 64, 80, on="4-5", color="blue")
B.arrow(43, 34, 180, 80, on="6", color="blue", bend=-10)
B.arrow(317, 34, 180, 80, on="2", color="blue", bend=10)
B.arrow(317, 34, 296, 80, on="3-", color="blue")
B.box(14, 80, 100, 50, None, fill="none", stroke="blue", sw=3, on="5")
B.box(130, 80, 100, 50, None, fill="none", stroke="blue", sw=3, on="5")
B.box(246, 80, 100, 50, None, fill="none", stroke="green", sw=3, on="5")
B.text(180, 156, "hop 0 → hop 1 → hop 2: found", on="5", anchor="middle", size=10, bold=True, cls="blue")
B.box(14, 80, 100, 50, "E (garbage)", fill="card2", stroke="line", on="6", size=9.5, mono=True)
B.note({1: "first = last = null, size 0.", 2: "One node: first and last both point to it.", 3: "New node linked after S1; last moves.",
        4: "New node before S1; first moves. Nothing shifts.", 5: "get(2) walks from first: 2 hops.", 6: "first moves to S1; E is unlinked."}, y=190, size=10)
B.caps(["An empty LinkedList has no nodes: <code>first</code> and <code>last</code> are null.",
        "<code>add(\"S1\")</code> creates one Node. Both <code>first</code> and <code>last</code> refer to it.",
        "<code>add(\"S2\")</code> creates a node, links S1.next → S2 and S2.prev → S1, and moves <code>last</code>.",
        "<code>addFirst(\"E\")</code> creates a node whose next is S1, sets S1.prev → E and moves <code>first</code>. S1 and S2 don't move at all.",
        "<code>get(2)</code>: 2 is in the first half, so the walk starts at <code>first</code> and follows <code>next</code> twice. With a million nodes, a get in the middle means half a million hops.",
        "<code>removeFirst()</code> moves <code>first</code> to S1 and clears S1.prev. Nothing points to E any more, so the garbage collector will free it."])
ANIM = two_view("A LinkedList is a chain of nodes", S, B)
BLOCKS = {'ANIM': ANIM}

# ---------------- Part 6: animated example ----------------
ANIM2_HEADING = "Watch it with an example: browser back and forward"
ANIM2_INTRO = "A browser's history behaves like a doubly linked list with a cursor. Watch Back and Forward follow the prev and next links."
A = Anim("History as linked pages", frames=5, h=200, label="Pages linked both ways; a cursor moves back and forward; visiting a new page drops the forward pages")
pages = ["Home", "Menu", "Cart", "Pay"]
for k, p in enumerate(pages):
    x = 10 + k * 88
    A.box(x, 40, 76, 40, p, fill="soft-blue", stroke="blue", size=10.5, bold=True, on="1-3" if p != "Pay" else "1-3")
    if k < 3:
        A.arrow(x + 76, 54, x + 88, 54, on="1-3", color="blue", sw=1.5)
        A.arrow(x + 88, 68, x + 76, 68, on="1-3", color="green", sw=1.5)
for k, p in enumerate(["Home", "Menu", "Offers"]):
    x = 10 + k * 88
    A.box(x, 40, 76, 40, p, fill="soft-blue" if p != "Offers" else "soft-green", stroke="blue" if p != "Offers" else "green", size=10.5, bold=True, on="4-")
    if k < 2:
        A.arrow(x + 76, 54, x + 88, 54, on="4-", color="blue", sw=1.5)
        A.arrow(x + 88, 68, x + 76, 68, on="4-", color="green", sw=1.5)
A.lines(10 + 3 * 88 + 38, 56, ["Cart, Pay", "dropped"], on="4-", anchor="middle", size=9.5, cls="ink3")
cur = {1: 3, 2: 2, 3: 1, 4: 2, 5: 1}
for f, k in cur.items():
    A.text(10 + k * 88 + 38, 100, "▲ you are here", on=str(f), anchor="middle", size=9.5, bold=True, cls="acc")
A.note({1: "Four pages visited.", 2: "Back: follow prev.", 3: "Back again.", 4: "Visit Offers from Menu.", 5: "Back from Offers."}, y=150, size=11)
A.caps(["You visited Home, Menu, Cart and Pay. Each page links to the one before and after.",
        "Back follows the <code>prev</code> link: now on Cart. Forward would follow <code>next</code>.",
        "Back again: Menu.",
        "From Menu you open Offers. The old forward pages (Cart, Pay) are unlinked and dropped; Offers becomes the new next page.",
        "Back from Offers goes to Menu, in O(1), however long the history is. (Simplified: real browsers store more per page.)"])
ANIM2 = A

# ---------------- Part 8: tracer ----------------
TRACE = dict(code='''import java.util.LinkedList;

public class Main {
    public static void main(String[] args) {
        LinkedList<String> train = new LinkedList<>();
        train.add("S1");
        train.add("S2");
        train.addFirst("ENGINE");
        train.addLast("GUARD");
        String gone = train.removeFirst();
        String middle = train.get(1);
        System.out.println(train + " removed " + gone + ", get(1) " + middle);
    }
}
''', notes={
 5: "Create :: An empty LinkedList: first and last are null.",
 6: "Add :: The first node: it is both first and last.",
 7: "Add :: A second node, linked after S1.",
 8: "Front :: A new first node. S1 and S2 stay exactly where they are; only links change.",
 9: "Back :: A new last node, linked after S2.",
 10: "Remove :: <code>first</code> moves to S1; the ENGINE node is unlinked.",
 11: "Walk :: <code>get(1)</code> starts at first and follows one <code>next</code> link.",
 12: "Print :: "})

# ---------------- Worked examples ----------------
WORKED_INTRO = "Three tasks where LinkedList's ends and its List/Deque double life are useful, traced on the real JVM."
EXAMPLES = [
dict(tag="Customer service · deque", title="VIP tickets jump the queue",
 problem="<p>A support desk serves tickets in order, but VIP tickets go to the front. Tickets: T1, T2, VIP1, T3. Print the serving order.</p>",
 inp="T1, T2, VIP1, T3",
 approach=["Use a LinkedList as a Deque.",
           "A helper <code>arrive(desk, id)</code>: VIP tickets with <code>addFirst</code>, others with <code>addLast</code>.",
           "Serve with <code>pollFirst</code> until empty."],
 code='''import java.util.LinkedList;

public class Main {
    static void arrive(LinkedList<String> desk, String id) {
        if (id.startsWith("VIP")) {
            desk.addFirst(id);
        } else {
            desk.addLast(id);
        }
    }

    public static void main(String[] args) {
        LinkedList<String> desk = new LinkedList<>();
        arrive(desk, "T1");
        arrive(desk, "T2");
        arrive(desk, "VIP1");
        arrive(desk, "T3");
        StringBuilder order = new StringBuilder();
        while (!desk.isEmpty()) {
            order.append(desk.pollFirst()).append(" ");
        }
        System.out.println(order.toString().trim());
    }
}
''', tryit="Press <b>Run</b>. Then add a second VIP and see the order: does the newest VIP go first?"),
dict(tag="Text editing · undo", title="Undo the last two edits",
 problem="<p>An editor records edits on a stack. After typing \"Hello\", \" World\" and \"!\", the user presses Undo twice. Print the text left.</p>",
 inp="edits: Hello, ␠World, !; undo × 2",
 approach=["Push each edit with <code>push</code> (adds at the front).",
           "Undo = <code>pop</code>, which removes the most recent edit.",
           "Rebuild the text from the remaining edits, oldest first, using <code>descendingIterator</code>."],
 code='''import java.util.Iterator;
import java.util.LinkedList;

public class Main {
    public static void main(String[] args) {
        LinkedList<String> edits = new LinkedList<>();
        edits.push("Hello");
        edits.push(" World");
        edits.push("!");
        edits.pop();
        edits.pop();
        StringBuilder text = new StringBuilder();
        Iterator<String> it = edits.descendingIterator();
        while (it.hasNext()) {
            text.append(it.next());
        }
        System.out.println("Text: " + text);
    }
}
''', tryit="Press <b>Run</b>. Then undo only once and check the text."),
dict(tag="Logistics · route", title="Add a stop after a given stop",
 problem="<p>A delivery route is <code>[Depot, Kharghar, Vashi, Depot]</code>. Insert \"Belapur\" right after \"Kharghar\" using a <code>ListIterator</code>, without indexes.</p>",
 inp="route, insert Belapur after Kharghar",
 approach=["Walk the route with a ListIterator.",
           "When the current stop is Kharghar, call <code>it.add(\"Belapur\")</code>: an O(1) relink at the cursor.",
           "Stop after inserting and print the route."],
 code='''import java.util.LinkedList;
import java.util.List;
import java.util.ListIterator;

public class Main {
    public static void main(String[] args) {
        LinkedList<String> route = new LinkedList<>(List.of("Depot", "Kharghar", "Vashi", "Depot"));
        ListIterator<String> it = route.listIterator();
        while (it.hasNext()) {
            if (it.next().equals("Kharghar")) {
                it.add("Belapur");
                break;
            }
        }
        System.out.println(route);
    }
}
''', notes={11: "Insert :: = <code>it.add</code> links a new node between Kharghar and Vashi. No other stop moves."},
 tryit="Press <b>Run</b>. Then also remove the second Depot with <code>route.removeLast()</code>."),
]

# ---------------- Practice problems ----------------
PRACTICE_INTRO = "Use LinkedList through its List and Deque methods, and avoid its traps. The last three are business tasks."
PROBLEMS = [
dict(level="easy", title="Both ends", stmt="<p>Start with <code>[2, 3]</code>, add 1 at the front and 4 at the back, then print the first and last elements.</p>", inp="[2, 3]",
 code='''import java.util.LinkedList;
import java.util.List;

public class Main {
    public static void main(String[] args) {
        LinkedList<Integer> l = new LinkedList<>(List.of(2, 3));
        l.addFirst(1);
        l.addLast(4);
        System.out.println(l + " first " + l.getFirst() + " last " + l.getLast());
    }
}''', explain="<p><b>How it works:</b> the list keeps direct references to its first and last nodes, so all four calls are O(1).</p>"),
dict(level="easy", title="Safe peek on an empty list", stmt="<p>Print the next ticket of an empty queue without crashing, then add one and peek again.</p>", inp="empty, then T9",
 code='''import java.util.LinkedList;

public class Main {
    public static void main(String[] args) {
        LinkedList<String> q = new LinkedList<>();
        System.out.println("Next: " + q.peekFirst());
        q.offer("T9");
        System.out.println("Next: " + q.peekFirst());
    }
}''', explain="<p><b>How it works:</b> <code>peekFirst</code> returns null for an empty list; <code>getFirst</code> would throw <code>NoSuchElementException</code>.</p>"),
dict(level="easy", title="Iterate backwards", stmt="<p>Print the stations <code>[Panvel, Kharghar, Belapur, Vashi]</code> in reverse using <code>descendingIterator</code>.</p>", inp="4 stations",
 code='''import java.util.Iterator;
import java.util.LinkedList;
import java.util.List;

public class Main {
    public static void main(String[] args) {
        LinkedList<String> st = new LinkedList<>(List.of("Panvel", "Kharghar", "Belapur", "Vashi"));
        Iterator<String> it = st.descendingIterator();
        while (it.hasNext()) System.out.print(it.next() + " ");
        System.out.println();
    }
}''', explain="<p><b>How it works:</b> the iterator starts at <code>last</code> and follows the <code>prev</code> links, possible because the list is doubly linked.</p>"),
dict(level="medium", title="Rotate a list by one", stmt="<p>Move the first element to the end three times: <code>[A, B, C, D]</code> → ?</p>", inp="[A, B, C, D], 3 rotations",
 code='''import java.util.LinkedList;
import java.util.List;

public class Main {
    public static void main(String[] args) {
        LinkedList<String> l = new LinkedList<>(List.of("A", "B", "C", "D"));
        for (int i = 0; i < 3; i++) {
            l.addLast(l.removeFirst());
        }
        System.out.println(l);
    }
}''', explain="<p><b>How it works:</b> each rotation is two O(1) operations at the ends. On an ArrayList, removing the first element would shift everything.</p>"),
dict(level="medium", title="Remove every other element", stmt="<p>Remove elements at odd positions from <code>[10, 11, 12, 13, 14]</code> with an iterator.</p>", inp="[10, 11, 12, 13, 14]",
 code='''import java.util.Iterator;
import java.util.LinkedList;
import java.util.List;

public class Main {
    public static void main(String[] args) {
        LinkedList<Integer> l = new LinkedList<>(List.of(10, 11, 12, 13, 14));
        Iterator<Integer> it = l.iterator();
        int pos = 0;
        while (it.hasNext()) {
            it.next();
            if (pos % 2 == 1) it.remove();
            pos++;
        }
        System.out.println(l);
    }
}''', explain="<p><b>How it works:</b> <code>it.remove()</code> unlinks the current node in O(1) and keeps the iterator valid. No ConcurrentModificationException.</p>"),
dict(level="business", title="Last 3 notifications", stmt="<p>A phone shows only the 3 most recent notifications, newest first. Add N1…N5 and print what's shown.</p>", inp="N1, N2, N3, N4, N5",
 code='''import java.util.LinkedList;

public class Main {
    public static void main(String[] args) {
        LinkedList<String> shown = new LinkedList<>();
        for (int i = 1; i <= 5; i++) {
            shown.addFirst("N" + i);
            if (shown.size() > 3) shown.removeLast();
        }
        System.out.println(shown);
    }
}''', explain="<p><b>How it works:</b> new items go to the front; the oldest drops off the back. Both ends are O(1).</p>"),
dict(level="business", title="Token desk with no-shows", stmt="<p>Tokens T1–T4 wait. T2 doesn't show up and is skipped (sent to the back once). Print the serving order.</p>", inp="T1, T2(no-show once), T3, T4",
 code='''import java.util.LinkedList;
import java.util.List;

public class Main {
    public static void main(String[] args) {
        LinkedList<String> q = new LinkedList<>(List.of("T1", "T2", "T3", "T4"));
        boolean t2Skipped = false;
        StringBuilder served = new StringBuilder();
        while (!q.isEmpty()) {
            String t = q.pollFirst();
            if (t.equals("T2") && !t2Skipped) {
                t2Skipped = true;
                q.addLast(t);          // try again later
                continue;
            }
            served.append(t).append(" ");
        }
        System.out.println(served.toString().trim());
    }
}''', explain="<p><b>How it works:</b> a skipped token is moved from the front to the back in O(1), and served on its second turn.</p>"),
dict(level="business", title="Merge two sorted delivery lists", stmt="<p>Two drivers have delivery times sorted: <code>[9, 12, 15]</code> and <code>[10, 11, 16]</code>. Merge them into one sorted list.</p>", inp="[9, 12, 15], [10, 11, 16]",
 code='''import java.util.LinkedList;
import java.util.List;

public class Main {
    public static void main(String[] args) {
        LinkedList<Integer> a = new LinkedList<>(List.of(9, 12, 15));
        LinkedList<Integer> b = new LinkedList<>(List.of(10, 11, 16));
        LinkedList<Integer> merged = new LinkedList<>();
        while (!a.isEmpty() && !b.isEmpty()) {
            merged.addLast(a.peekFirst() <= b.peekFirst() ? a.pollFirst() : b.pollFirst());
        }
        merged.addAll(a);
        merged.addAll(b);
        System.out.println(merged);
    }
}''', explain="<p><b>How it works:</b> always take the smaller front element; every step is O(1) at the ends, so the merge is O(n + m).</p>"),
]
