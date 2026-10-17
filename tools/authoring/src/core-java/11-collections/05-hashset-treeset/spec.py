import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../..'))
from mkanim import Anim, two_view

def esc(t): return t.replace('<', '&lt;').replace('>', '&gt;')

# ---------------- Part 5: two-view animation ----------------
CODE = ["add(30)", "add(10)", "add(40)", "add(20)", "add(30)   // again", "println(hash); println(tree);"]
S = Anim("see", frames=6, h=250, label="The same numbers added to a HashSet and a TreeSet, including a duplicate, then both printed")
S.box(8, 8, 344, 24, None, fill="soft-blue", stroke="blue")
S.text(16, 25, esc("Set<Integer> hash = new HashSet<>();  tree = new TreeSet<>();"), mono=True, size=8.6, cls="ink")
S.box(8, 40, 344, 132, None, fill="board", stroke="board")
for i, line in enumerate(CODE):
    y = 62 + i * 20
    S.box(12, y - 14, 336, 19, None, fill="none", stroke="track", sw=2, on=str(i + 1), rx=4)
    S.text(20, y, ("both." if i < 5 else "") + line, mono=True, size=10, cls="chalk" if i != 4 else "kw")
S.box(8, 180, 344, 40, None, fill="card2", stroke="line")
S.text(18, 205, "true true", on="1-4", mono=True, size=11, cls="green", bold=True)
S.text(18, 205, "false false   (duplicate)", on="5", mono=True, size=11, cls="red", bold=True)
S.text(18, 205, "[20, 40, 10, 30]   [10, 20, 30, 40]", on="6", mono=True, size=10.5, cls="green", bold=True)
S.note({1: "30 goes into both sets.", 2: "10 goes into both.", 3: "40 goes into both.", 4: "20 goes into both.", 5: "30 again: refused by both.",
        6: "Same elements, different order."}, y=240, size=10.5)
S.caps(["<code>add(30)</code> on both sets returns true.", "<code>add(10)</code>: true.", "<code>add(40)</code>: true.", "<code>add(20)</code>: true.",
        "<code>add(30)</code> again: both return <b>false</b>. A set holds each element once.",
        "Both contain 10, 20, 30, 40, but the HashSet prints them in bucket order and the TreeSet in sorted order."])
B = Anim("behind", frames=6, h=250, label="Left: HashSet buckets chosen by hash code; right: TreeSet's binary search tree")
B.text(80, 16, "HashSet: 16 buckets", anchor="middle", size=9.5, bold=True, cls="blue")
B.text(268, 16, "TreeSet: sorted tree", anchor="middle", size=9.5, bold=True, cls="acc")
for k, b in enumerate([4, 8, 10, 14]):
    y = 26 + k * 34
    B.box(8, y, 150, 28, None, fill="card", stroke="line", rx=5)
    B.text(16, y + 18, f"[{b}]", mono=True, size=9.5, cls="ink3")
hb = {30: (3, "1-"), 10: (2, "2-"), 40: (1, "3-"), 20: (0, "4-")}
for v, (k, on) in hb.items():
    B.box(60, 29 + k * 34, 50, 22, str(v), fill="soft-blue", stroke="blue", on=on, size=10, bold=True, mono=True)
B.box(60, 29 + 3 * 34, 50, 22, None, fill="none", stroke="red", sw=3, on="5")
B.text(114, 44 + 3 * 34, "equal!", on="5", size=9, cls="red", bold=True)
B.text(83, 178, "index = hash & 15", anchor="middle", mono=True, size=9, cls="ink2")
# tree
B.circle(268, 44, 16, label="30", on="1-")
B.circle(222, 94, 16, label="10", on="2-", fill="soft-acc", stroke="track")
B.circle(314, 94, 16, label="40", on="3-", fill="soft-acc", stroke="track")
B.circle(252, 144, 16, label="20", on="4-", fill="soft-green", stroke="green")
B.arrow(256, 56, 232, 80, on="2-", color="ink", sw=1.4, head=False)
B.arrow(280, 56, 304, 80, on="3-", color="ink", sw=1.4, head=False)
B.arrow(230, 108, 246, 130, on="4-", color="ink", sw=1.4, head=False)
B.circle(268, 44, 19, fill="none", stroke="red", on="5")
B.text(268, 178, "20: < 30 left, > 10 right", on="4", anchor="middle", size=9, cls="green", bold=True)
B.text(268, 178, "30 vs 30: compareTo = 0", on="5", anchor="middle", size=9, cls="red", bold=True)
B.text(268, 178, "in-order walk: 10 20 30 40", on="6", anchor="middle", size=9, cls="acc", bold=True)
B.text(83, 196, "walk buckets: 20 40 10 30", on="6", anchor="middle", size=9, cls="blue", bold=True)
B.note({1: "30: bucket 14 | root of the tree.", 2: "10: bucket 10 | left of 30.", 3: "40: bucket 8 | right of 30.",
        4: "20: bucket 4 | left of 30, right of 10.", 5: "Duplicate: equals in the bucket | compareTo 0.",
        6: "Bucket order vs sorted order."}, y=226, size=10)
B.caps(["HashSet: Integer 30's hash code is 30; with 16 buckets the index is 30 &amp; 15 = 14. TreeSet: 30 becomes the root.",
        "10 → bucket 10. In the tree, 10 &lt; 30, so it goes left.",
        "40 → bucket 40 &amp; 15 = 8. In the tree, 40 &gt; 30: right.",
        "20 → bucket 4. In the tree: 20 &lt; 30 (go left), 20 &gt; 10 (go right of 10). The red-black tree also recolours nodes to stay balanced.",
        "30 again: the HashSet looks in bucket 14 and <code>equals</code> finds 30; the TreeSet's <code>compareTo</code> returns 0 at the root. Both refuse.",
        "Printing walks the structure: the HashSet goes bucket by bucket (20, 40, 10, 30); the TreeSet walks the tree in order (10, 20, 30, 40)."])
ANIM = two_view("Same elements, two structures", S, B)
BLOCKS = {'ANIM': ANIM}

# ---------------- Part 6: animated example ----------------
ANIM2_HEADING = "Watch it with an example: booking a turf slot"
ANIM2_INTRO = "A turf-cricket ground keeps its free evening slots in a TreeSet. Watch it answer “next slot after 6:10” and update itself as slots are booked."
A = Anim("Free slots in a TreeSet", frames=5, h=210, label="A TreeSet of free slots answers ceiling queries and shrinks as slots are booked")
slots = ["17:00", "18:00", "19:00", "20:00", "21:00"]
for k, s in enumerate(slots):
    x = 10 + k * 70
    A.box(x, 40, 62, 36, s, fill="soft-green", stroke="green", size=10, bold=True, mono=True, on="1-" if s != "19:00" else "1-2")
A.box(150, 40, 62, 36, "booked", fill="card2", stroke="line", size=9.5, on="3-", mono=True)
A.box(220, 40, 62, 36, None, fill="none", stroke="blue", sw=3, on="2")
A.box(220, 40, 62, 36, None, fill="none", stroke="blue", sw=3, on="4")
A.box(80, 40, 62, 36, None, fill="none", stroke="blue", sw=3, on="5")
A.text(181, 106, "free.ceiling(18:10) → 19:00", on="2", anchor="middle", mono=True, size=11, bold=True, cls="blue")
A.text(181, 106, "free.remove(19:00): booked for Kabir's team", on="3", anchor="middle", size=10.5, bold=True, cls="ink")
A.text(181, 106, "free.ceiling(18:10) → 20:00 now", on="4", anchor="middle", mono=True, size=11, bold=True, cls="blue")
A.text(181, 106, "free.floor(18:50) → 18:00", on="5", anchor="middle", mono=True, size=11, bold=True, cls="blue")
A.text(181, 106, "sorted automatically, each slot once", on="1", anchor="middle", size=10.5, cls="ink2")
A.note({1: "Free slots, always sorted.", 2: "Next slot at or after 18:10.", 3: "Book it.", 4: "Ask again.", 5: "Latest slot at or before 18:50."}, y=160, size=11)
A.caps(["The ground's free evening slots sit in a <code>TreeSet</code>, sorted by time.",
        "Riya asks for the first slot at or after 18:10: <code>ceiling</code> finds 19:00 in O(log n).",
        "Kabir's team books 19:00, so it's removed from the free set.",
        "The same question now gives 20:00.",
        "<code>floor(18:50)</code> finds the latest slot not after 18:50: 18:00. (Simplified: real booking systems lock slots in a database so two teams can't book the same one.)"])
ANIM2 = A

# ---------------- Part 8: tracer ----------------
TRACE = dict(code='''import java.util.*;

public class Main {
    public static void main(String[] args) {
        Set<String> hash = new HashSet<>();
        Set<String> linked = new LinkedHashSet<>();
        Set<String> tree = new TreeSet<>();
        String[] scans = {"Riya", "Kabir", "Om", "Riya"};
        for (String s : scans) {
            hash.add(s);
            linked.add(s);
            tree.add(s);
        }
        System.out.println(hash + " " + linked + " " + tree);
    }
}
''', notes={
 (10, 1): "HashSet :: \"Riya\" goes into the bucket its hash code chooses.",
 (11, 1): "LinkedHashSet :: Stored and remembered as first.",
 (12, 1): "TreeSet :: The first element becomes the root of the tree.",
 (12, 2): "TreeSet :: \"Kabir\" &lt; \"Riya\": it goes before Riya in sorted order.",
 (12, 3): "TreeSet :: \"Om\" sorts between Kabir and Riya.",
 (10, 4): "Duplicate :: = \"Riya\" again: same hash, same bucket, <code>equals</code> true. Nothing changes.",
 (11, 4): "Duplicate :: = Refused by the LinkedHashSet too.",
 (12, 4): "Duplicate :: = <code>compareTo</code> returns 0 at Riya's node. The TreeSet is unchanged.",
 14: "Print :: Bucket order, arrival order, sorted order."})

# ---------------- Worked examples ----------------
WORKED_INTRO = "Three problems, each solved by the set whose order fits the job."
EXAMPLES = [
dict(tag="Payments · HashSet", title="Flag duplicate transaction IDs",
 problem="<p>A payment batch has transaction IDs. List the IDs that appear more than once, each reported once.</p>",
 inp='["T1", "T2", "T1", "T3", "T2", "T1"]',
 approach=["<code>seen</code>: a HashSet of IDs met so far.",
           "If <code>seen.add(id)</code> returns false, it's a repeat: add it to a <code>dups</code> set (so it's reported once).",
           "Print <code>dups</code> using a LinkedHashSet to keep first-detection order."],
 code='''import java.util.HashSet;
import java.util.LinkedHashSet;
import java.util.Set;

public class Main {
    static Set<String> duplicates(String[] ids) {
        Set<String> seen = new HashSet<>();
        Set<String> dups = new LinkedHashSet<>();
        for (String id : ids) {
            if (!seen.add(id)) {
                dups.add(id);
            }
        }
        return dups;
    }

    public static void main(String[] args) {
        String[] batch = {"T1", "T2", "T1", "T3", "T2", "T1"};
        System.out.println("Duplicates: " + duplicates(batch));
    }
}
''', tryit="Press <b>Run</b>. Then also print how many unique IDs there were (<code>seen.size()</code>)."),
dict(tag="Clinic · TreeSet", title="Next free appointment",
 problem="<p>Free slots (minutes after 10:00) are 0, 20, 40, 90. Patients ask for 15 and then 25. Give each the first slot at or after the time asked, and remove it once booked.</p>",
 inp="free {0, 20, 40, 90}; requests 15, 25",
 approach=["Keep free slots in a TreeSet.",
           "A helper <code>book(free, want)</code> uses <code>ceiling</code> and removes the slot.",
           "Print each booking and what's left."],
 code='''import java.util.List;
import java.util.TreeSet;

public class Main {
    static Integer book(TreeSet<Integer> free, int want) {
        Integer slot = free.ceiling(want);
        if (slot != null) {
            free.remove(slot);
        }
        return slot;
    }

    public static void main(String[] args) {
        TreeSet<Integer> free = new TreeSet<>(List.of(0, 20, 40, 90));
        System.out.println("15 → " + book(free, 15));
        System.out.println("25 → " + book(free, 25));
        System.out.println("Still free: " + free);
    }
}
''', tryit="Press <b>Run</b>. Then request 100: what does <code>ceiling</code> return?"),
dict(tag="Search · LinkedHashSet", title="Recent searches, newest last, no repeats",
 problem="<p>A food app shows recent searches without repeats. If a search is repeated, it moves to the end. Searches: dosa, chai, vada, dosa.</p>",
 inp="dosa, chai, vada, dosa",
 approach=["A LinkedHashSet keeps insertion order.",
           "To move a repeat to the end, <code>remove</code> it first, then <code>add</code> it again.",
           "Print the set."],
 code='''import java.util.LinkedHashSet;
import java.util.Set;

public class Main {
    public static void main(String[] args) {
        Set<String> recent = new LinkedHashSet<>();
        for (String q : new String[]{"dosa", "chai", "vada", "dosa"}) {
            recent.remove(q);
            recent.add(q);
        }
        System.out.println(recent);
    }
}
''', tryit="Press <b>Run</b>. Then keep only the last 3 searches by removing the first element when the size goes above 3."),
]

# ---------------- Practice problems ----------------
PRACTICE_INTRO = "Pick the right set for each job and use the set operations. The last three are business tasks."
PROBLEMS = [
dict(level="easy", title="Count distinct words", stmt="<p>How many different words are in <code>\"to be or not to be\"</code>?</p>", inp='"to be or not to be"',
 code='''import java.util.*;

public class Main {
    public static void main(String[] args) {
        Set<String> words = new HashSet<>(Arrays.asList("to be or not to be".split(" ")));
        System.out.println(words.size());
    }
}''', explain="<p><b>How it works:</b> six words go in; the HashSet keeps the four distinct ones.</p>"),
dict(level="easy", title="Sorted distinct values", stmt="<p>Print the distinct marks of <code>{72, 85, 72, 91, 85}</code> from highest to lowest.</p>", inp="{72, 85, 72, 91, 85}",
 code='''import java.util.*;

public class Main {
    public static void main(String[] args) {
        TreeSet<Integer> m = new TreeSet<>(List.of(72, 85, 72, 91, 85));
        System.out.println(m.descendingSet());
    }
}''', explain="<p><b>How it works:</b> the TreeSet removes repeats and sorts; <code>descendingSet</code> is a reversed view.</p>"),
dict(level="easy", title="Is every required skill present?", stmt="<p>A job needs {java, sql}. A candidate has {java, git, sql}. Check with <code>containsAll</code>.</p>", inp="required {java, sql}",
 code='''import java.util.*;

public class Main {
    public static void main(String[] args) {
        Set<String> need = Set.of("java", "sql");
        Set<String> has = Set.of("java", "git", "sql");
        System.out.println(has.containsAll(need));
    }
}''', explain="<p><b>How it works:</b> <code>containsAll</code> is the subset test.</p>"),
dict(level="medium", title="Common and unique subjects", stmt="<p>Riya takes {Maths, Physics, CS}; Kabir takes {CS, Biology, Maths}. Print subjects both take and subjects only one of them takes.</p>", inp="two subject sets",
 code='''import java.util.*;

public class Main {
    public static void main(String[] args) {
        Set<String> r = Set.of("Maths", "Physics", "CS");
        Set<String> k = Set.of("CS", "Biology", "Maths");
        Set<String> both = new TreeSet<>(r); both.retainAll(k);
        Set<String> either = new TreeSet<>(r); either.addAll(k);
        Set<String> onlyOne = new TreeSet<>(either); onlyOne.removeAll(both);
        System.out.println("Both: " + both + ", only one: " + onlyOne);
    }
}''', explain="<p><b>How it works:</b> symmetric difference = union minus intersection.</p>"),
dict(level="medium", title="Closest price", stmt="<p>Prices available: {99, 149, 199, 299}. A customer's budget is 180. Find the best price within budget and the cheapest above it.</p>", inp="budget 180",
 code='''import java.util.*;

public class Main {
    public static void main(String[] args) {
        TreeSet<Integer> prices = new TreeSet<>(List.of(99, 149, 199, 299));
        System.out.println("Within budget: " + prices.floor(180));
        System.out.println("Just above: " + prices.higher(180));
    }
}''', explain="<p><b>How it works:</b> <code>floor</code> = largest ≤ 180; <code>higher</code> = smallest &gt; 180. Both O(log n).</p>"),
dict(level="business", title="Unique pin codes served", stmt="<p>Deliveries went to pin codes 410210, 400703, 410210, 400614, 400703. Print the distinct pin codes in sorted order and their count.</p>", inp="5 deliveries",
 code='''import java.util.*;

public class Main {
    public static void main(String[] args) {
        int[] pins = {410210, 400703, 410210, 400614, 400703};
        Set<Integer> served = new TreeSet<>();
        for (int p : pins) served.add(p);
        System.out.println(served.size() + " areas: " + served);
    }
}''', explain="<p><b>How it works:</b> a TreeSet gives distinct and sorted in one structure.</p>"),
dict(level="business", title="Customers who stopped buying", stmt="<p>Customers last month: {C1, C2, C3, C4}. This month: {C2, C4, C5}. Find churned customers (last month but not this month) and new ones.</p>", inp="two months",
 code='''import java.util.*;

public class Main {
    public static void main(String[] args) {
        Set<String> last = Set.of("C1", "C2", "C3", "C4");
        Set<String> now = Set.of("C2", "C4", "C5");
        Set<String> churned = new TreeSet<>(last); churned.removeAll(now);
        Set<String> fresh = new TreeSet<>(now); fresh.removeAll(last);
        System.out.println("Churned: " + churned + ", new: " + fresh);
    }
}''', explain="<p><b>How it works:</b> two set differences answer two business questions; HashSet-backed <code>removeAll</code> is fast even for large sets.</p>"),
dict(level="business", title="Leaderboard without ties lost", stmt="<p>Players with scores: (Riya 92), (Om 85), (Kabir 92). Keep a sorted set by score (highest first) without losing either 92.</p>", inp="3 players",
 code='''import java.util.*;

public class Main {
    record Player(String name, int score) {}

    public static void main(String[] args) {
        Comparator<Player> byScoreThenName =
            Comparator.comparingInt(Player::score).reversed().thenComparing(Player::name);
        TreeSet<Player> board = new TreeSet<>(byScoreThenName);
        board.add(new Player("Riya", 92));
        board.add(new Player("Om", 85));
        board.add(new Player("Kabir", 92));
        for (Player p : board) System.out.println(p.name() + " " + p.score());
    }
}''', explain="<p><b>How it works:</b> the name tie-breaker makes the comparator return 0 only for truly identical players, so both 92s stay. (Records and method references are covered in Lessons 14.5 and 14.1; comparators in 11.8.)</p>"),
]
