import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../..'))
from mkanim import Anim, two_view

def esc(t): return t.replace('<', '&lt;').replace('>', '&gt;')

# ---------------- Part 5: two-view animation ----------------
CODE = ["it = marks.iterator();", "it.next();   // 78", "it.next();   // 32", "it.remove();", "it.next();   // 91", "marks.remove(0); it.next();"]
S = Anim("see", frames=6, h=250, label="An iterator over marks: two next calls, a safe remove, another next, then a direct list change that breaks the iterator")
S.box(8, 8, 344, 132, None, fill="board", stroke="board")
for i, line in enumerate(CODE):
    y = 30 + i * 20
    S.box(12, y - 14, 336, 19, None, fill="none", stroke="track" if i < 5 else "red", sw=2, on=str(i + 1), rx=4)
    S.text(20, y, line, mono=True, size=10.5, cls="chalk" if i < 5 else "kw")
S.box(8, 150, 344, 50, None, fill="card2", stroke="line")
S.text(18, 168, "marks", size=9, cls="ink3", bold=True)
for f, t in {1: "[78, 32, 91, 28]", 2: "[78, 32, 91, 28]  → 78", 3: "[78, 32, 91, 28]  → 32", 4: "[78, 91, 28]",
             5: "[78, 91, 28]  → 91"}.items():
    S.text(18, 190, t, on=str(f), mono=True, size=11, bold=True)
S.text(18, 190, "ConcurrentModificationException", on="6", mono=True, size=11, bold=True, cls="red")
S.note({1: "Get an iterator.", 2: "First element.", 3: "Second element.", 4: "Remove 32 through the iterator.", 5: "Carry on: 91.",
        6: "Change the list directly…"}, y=226, size=10.5)
S.caps(["Ask the list for an iterator.", "<code>next()</code> returns 78.", "<code>next()</code> returns 32.",
        "<code>it.remove()</code> removes 32, the element just returned.", "<code>next()</code> continues correctly with 91: nothing skipped.",
        "Removing through the list itself and then calling <code>next()</code> throws <code>ConcurrentModificationException</code>."])
B = Anim("behind", frames=6, h=250, label="The iterator's cursor, lastRet and expectedModCount compared with the list's array and modCount")
vals4 = ["78", "32", "91", "28"]
vals3 = ["78", "91", "28"]
vals2 = ["91", "28"]
for k, v in enumerate(vals4):
    B.box(8 + k * 60, 24, 54, 30, v, fill="soft-acc", stroke="track", on="1-3", size=11, mono=True, bold=True)
for k, v in enumerate(vals3):
    B.box(8 + k * 60, 24, 54, 30, v, fill="soft-acc", stroke="track", on="4-5", size=11, mono=True, bold=True)
for k, v in enumerate(vals2):
    B.box(8 + k * 60, 24, 54, 30, v, fill="soft-acc", stroke="track", on="6", size=11, mono=True, bold=True)
for k in range(5):
    B.text(8 + k * 60 - 3, 70, str(k), size=8.5, mono=True, cls="ink3")
cur = {1: 0, 2: 1, 3: 2, 4: 1, 5: 2, 6: 2}
for f, c in cur.items():
    B.text(8 + c * 60 - 3, 86, "▲ cursor", on=str(f), size=9.5, bold=True, cls="blue")
B.text(8, 16, "list elementData", size=9, bold=True, cls="ink2")
B.box(254, 18, 98, 40, None, fill="card2", stroke="line")
B.text(262, 34, "modCount", size=9, cls="ink2")
for f, m in {1: "0", 2: "0", 3: "0", 4: "1", 5: "1", 6: "2"}.items():
    B.text(262, 52, m, on=str(f), mono=True, size=12, bold=True, cls="ink" if f < 6 else "red")
B.box(8, 104, 344, 70, None, fill="soft-blue", stroke="blue")
B.text(16, 122, "Itr object", size=10, bold=True, cls="blue")
rows = {1: ("0", "-1", "0"), 2: ("1", "0", "0"), 3: ("2", "1", "0"), 4: ("1", "-1", "1"), 5: ("2", "1", "1"), 6: ("2", "1", "1")}
for f, (c, l, e) in rows.items():
    B.text(16, 144, f"cursor = {c}   lastRet = {l}", on=str(f), mono=True, size=10.5)
    B.text(16, 164, f"expectedModCount = {e}", on=str(f), mono=True, size=10.5, cls="red" if f == 6 else "ink")
B.text(250, 164, "2 ≠ 1 → throw", on="6", mono=True, size=10, bold=True, cls="red")
B.note({1: "Cursor before index 0; counts match.", 2: "Return [0], cursor → 1.", 3: "Return [1], cursor → 2.",
        4: "Remove [lastRet]; cursor back to 1; counts re-synced.", 5: "Return [1] = 91.", 6: "Direct change: counts disagree."}, y=196, size=10)
B.caps(["A new <code>ArrayList.Itr</code>: <code>cursor = 0</code>, <code>lastRet = -1</code>, and it copies the list's <code>modCount</code> (0) into <code>expectedModCount</code>.",
        "<code>next()</code> checks the counts (equal), returns <code>elementData[0]</code> = 78, sets <code>lastRet = 0</code>, <code>cursor = 1</code>.",
        "Again: returns 32, <code>lastRet = 1</code>, <code>cursor = 2</code>.",
        "<code>it.remove()</code> removes index <code>lastRet</code> (32); later elements shift left. The list's <code>modCount</code> becomes 1, and the iterator <b>updates its own copy</b> to 1, moves <code>cursor</code> back to 1 and sets <code>lastRet = -1</code>.",
        "<code>next()</code>: counts equal, returns <code>elementData[1]</code> = 91. Nothing was skipped.",
        "<code>marks.remove(0)</code> bypasses the iterator: <code>modCount</code> becomes 2 but the iterator still expects 1. The next <code>next()</code> notices and throws <code>ConcurrentModificationException</code>."])
ANIM = two_view("How an iterator stays safe", S, B)
BLOCKS = {'ANIM': ANIM}

# ---------------- Part 6: animated example ----------------
ANIM2_HEADING = "Watch it with an example: clearing expired OTPs"
ANIM2_INTRO = "A login service keeps one-time passwords in a map with their expiry. A cleanup job walks the entries with an iterator and removes expired ones in place."
A = Anim("Removing expired entries with an iterator", frames=5, h=210, label="An iterator walks map entries and removes expired ones; valid ones remain")
entries = [("riya", "valid"), ("kabir", "expired"), ("om", "valid"), ("zoya", "expired")]
for k, (u, st) in enumerate(entries):
    y = 14 + k * 34
    gone = {"kabir": "3-", "zoya": "5"}.get(u)
    A.box(10, y, 200, 28, f"{u} → OTP ({st})", fill="soft-green" if st == "valid" else "soft-acc",
          stroke="green" if st == "valid" else "red", size=10, mono=True, on=("1-" if not gone else ("1-2" if u == "kabir" else "1-4")))
    if gone:
        A.box(10, y, 200, 28, f"{u}: removed", fill="card2", stroke="line", size=10, mono=True, on=gone)
for f, k in {1: 0, 2: 1, 3: 1, 4: 2, 5: 3}.items():
    A.text(222, 32 + k * 34, "◀ it", on=str(f), size=11, bold=True, cls="blue")
A.text(260, 40, "it.next()", on="1-2,4", mono=True, size=10, cls="ink")
A.text(260, 58, "valid: keep", on="1,4", size=10, cls="green", bold=True)
A.text(260, 58, "expired!", on="2", size=10, cls="red", bold=True)
A.text(260, 40, "it.remove()", on="3,5", mono=True, size=10, cls="red", bold=True)
A.text(260, 58, "safe, in place", on="3,5", size=10, cls="ink2")
A.note({1: "Riya's OTP is still valid.", 2: "Kabir's has expired.", 3: "Remove it through the iterator.", 4: "Om's is valid.", 5: "Zoya's expired: removed."}, y=170, size=11)
A.caps(["The job calls <code>map.entrySet().iterator()</code> and checks the first entry: still valid, so it stays.",
        "Kabir's OTP is older than 5 minutes.",
        "<code>it.remove()</code> deletes that entry from the map itself. No copy, no exception.",
        "Om's OTP is valid.",
        "Zoya's has expired and is removed too. The map now holds only valid OTPs. (Simplified: real services use ConcurrentHashMap or a store with built-in expiry, since logins happen on many threads.)"])
ANIM2 = A

# ---------------- Part 8: tracer ----------------
TRACE = dict(code='''import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

public class Main {
    public static void main(String[] args) {
        List<Integer> marks = new ArrayList<>(List.of(78, 32, 91));
        Iterator<Integer> it = marks.iterator();
        while (it.hasNext()) {
            int m = it.next();
            if (m < 35) {
                it.remove();
            }
        }
        System.out.println(marks);
    }
}
''', notes={
 8: "Iterator :: = <code>it</code> = → an <code>ArrayList.Itr</code> object: <code>cursor=0</code>, <code>lastRet=-1</code>. It belongs to the list (an inner class, Lesson 10.5).",
 (10, 1): "next() :: Returns 78; cursor moves to 1, lastRet = 0.",
 (10, 2): "next() :: Returns 32; cursor 2, lastRet 1.",
 12: "remove() :: = Removes index <code>lastRet</code> (32) from the list. The iterator moves <code>cursor</code> back to 1 and sets <code>lastRet=-1</code>, so 91 won't be skipped.",
 (10, 3): "next() :: = Returns 91 from index 1. Nothing was skipped.",
 15: "Print :: "})

# ---------------- Worked examples ----------------
WORKED_INTRO = "Three iterator jobs from real apps: safe removal, editing at the cursor and a custom iterable."
EXAMPLES = [
dict(tag="Login · map cleanup", title="Remove expired OTPs from a map",
 problem="<p>OTPs are stored as user → expiry minute. At minute 10, remove every entry whose expiry is before 10, while iterating.</p>",
 inp="{riya=12, kabir=8, om=15, zoya=9}, now = 10",
 approach=["Iterate over <code>entrySet().iterator()</code>.",
           "If an entry's value is less than <code>now</code>, call <code>it.remove()</code>.",
           "Print what remains."],
 code='''import java.util.Iterator;
import java.util.LinkedHashMap;
import java.util.Map;

public class Main {
    public static void main(String[] args) {
        Map<String, Integer> otpExpiry = new LinkedHashMap<>();
        otpExpiry.put("riya", 12);
        otpExpiry.put("kabir", 8);
        otpExpiry.put("om", 15);
        int now = 10;
        Iterator<Map.Entry<String, Integer>> it = otpExpiry.entrySet().iterator();
        while (it.hasNext()) {
            Map.Entry<String, Integer> e = it.next();
            if (e.getValue() < now) {
                it.remove();
            }
        }
        System.out.println(otpExpiry);
    }
}
''', tryit="Press <b>Run</b>. Then rewrite the loop as <code>otpExpiry.values().removeIf(v -&gt; v &lt; now);</code>."),
dict(tag="Exams · ListIterator", title="Apply grace marks in place",
 problem="<p>Students who scored 33 or 34 get grace marks up to 35. Update the list in place with a ListIterator's <code>set</code>, and count how many were changed.</p>",
 inp="[33, 72, 34, 20]",
 approach=["Walk with <code>listIterator()</code>.",
           "If a mark is 33 or 34, <code>set(35)</code> replaces it where the cursor just passed.",
           "Count the changes."],
 code='''import java.util.ArrayList;
import java.util.List;
import java.util.ListIterator;

public class Main {
    public static void main(String[] args) {
        List<Integer> marks = new ArrayList<>(List.of(33, 72, 34, 20));
        int changed = 0;
        ListIterator<Integer> li = marks.listIterator();
        while (li.hasNext()) {
            int m = li.next();
            if (m == 33 || m == 34) {
                li.set(35);
                changed++;
            }
        }
        System.out.println(marks + ", grace given to " + changed);
    }
}
''', tryit="Press <b>Run</b>. Then also <i>insert</i> a note “*” after each changed mark using <code>li.add</code> (change the list to <code>List&lt;Object&gt;</code>)."),
dict(tag="Fitness · custom Iterable", title="Iterate over a workout plan's days",
 problem="<p>A <code>Plan</code> stores exercises per day. Make it <code>Iterable&lt;String&gt;</code> so a for-each prints each day's line.</p>",
 inp='Plan with "Push", "Pull", "Legs"',
 approach=["<code>Plan</code> keeps a private String array.",
           "<code>iterator()</code> returns an anonymous Iterator with an index.",
           "main uses for-each; Plan's storage stays hidden."],
 code='''import java.util.Iterator;

class Plan implements Iterable<String> {
    private final String[] days;

    Plan(String... days) {
        this.days = days;
    }

    public Iterator<String> iterator() {
        return new Iterator<>() {
            int i = 0;
            public boolean hasNext() {
                return i < days.length;
            }
            public String next() {
                return "Day " + (i + 1) + ": " + days[i++];
            }
        };
    }
}

public class Main {
    public static void main(String[] args) {
        for (String line : new Plan("Push", "Pull", "Legs")) {
            System.out.println(line);
        }
    }
}
''', notes={(25, 2): "for-each :: = The for-each calls <code>iterator()</code> on the Plan.",
            (11, 1): "Iterator object :: = An object of the anonymous class (shown as Plan.1) is created with <code>i=0</code>.",
            (11, 2): "Outer link :: = Its hidden <code>this$0</code> now points to the Plan, which is how <code>next()</code> can read the private <code>days</code> array (Lesson 10.5).",
            (25, 3): "hasNext :: = The loop asks <code>hasNext()</code>: is 0 &lt; 3?",
            (25, 4): "next :: = Then <code>next()</code>, which builds \"Day 1: Push\" and increases <code>i</code>."},
 tryit="Press <b>Run</b>. Then add a rest day after every three days inside <code>next()</code>."),
]

# ---------------- Practice problems ----------------
PRACTICE_INTRO = "Iterate, remove and edit safely. The last three are business tasks."
PROBLEMS = [
dict(level="easy", title="Walk with an explicit iterator", stmt="<p>Print the elements of <code>[\"UPI\", \"Card\", \"Cash\"]</code> using <code>hasNext</code>/<code>next</code>.</p>", inp='["UPI", "Card", "Cash"]',
 code='''import java.util.*;

public class Main {
    public static void main(String[] args) {
        Iterator<String> it = List.of("UPI", "Card", "Cash").iterator();
        while (it.hasNext()) System.out.println(it.next());
    }
}''', explain="<p><b>How it works:</b> exactly what a for-each compiles to.</p>"),
dict(level="easy", title="Remove empty strings", stmt="<p>Remove all empty strings from <code>[\"a\", \"\", \"b\", \"\"]</code> using an iterator.</p>", inp='["a", "", "b", ""]',
 code='''import java.util.*;

public class Main {
    public static void main(String[] args) {
        List<String> l = new ArrayList<>(List.of("a", "", "b", ""));
        Iterator<String> it = l.iterator();
        while (it.hasNext()) if (it.next().isEmpty()) it.remove();
        System.out.println(l);
    }
}''', explain="<p><b>How it works:</b> <code>it.remove()</code> keeps the iterator consistent, so adjacent empty strings aren't skipped.</p>"),
dict(level="easy", title="Print a list backwards", stmt="<p>Print <code>[1, 2, 3, 4]</code> in reverse using a ListIterator started at the end.</p>", inp="[1, 2, 3, 4]",
 code='''import java.util.*;

public class Main {
    public static void main(String[] args) {
        List<Integer> l = List.of(1, 2, 3, 4);
        ListIterator<Integer> li = l.listIterator(l.size());
        while (li.hasPrevious()) System.out.print(li.previous() + " ");
        System.out.println();
    }
}''', explain="<p><b>How it works:</b> <code>listIterator(size)</code> starts the cursor after the last element; <code>previous()</code> walks back.</p>"),
dict(level="medium", title="Double every even number in place", stmt="<p>In <code>[1, 2, 3, 4]</code> replace each even number with double its value; remove odd numbers.</p>", inp="[1, 2, 3, 4]",
 code='''import java.util.*;

public class Main {
    public static void main(String[] args) {
        List<Integer> l = new ArrayList<>(List.of(1, 2, 3, 4));
        ListIterator<Integer> li = l.listIterator();
        while (li.hasNext()) {
            int v = li.next();
            if (v % 2 == 0) li.set(v * 2);
            else li.remove();
        }
        System.out.println(l);
    }
}''', explain="<p><b>How it works:</b> <code>set</code> and <code>remove</code> both act on the element last returned by <code>next()</code>.</p>"),
dict(level="medium", title="Interleave a separator", stmt="<p>Insert \"|\" between every pair of items in <code>[A, B, C]</code> using <code>ListIterator.add</code>.</p>", inp="[A, B, C]",
 code='''import java.util.*;

public class Main {
    public static void main(String[] args) {
        List<String> l = new ArrayList<>(List.of("A", "B", "C"));
        ListIterator<String> li = l.listIterator();
        while (li.hasNext()) {
            li.next();
            if (li.hasNext()) li.add("|");
        }
        System.out.println(l);
    }
}''', explain="<p><b>How it works:</b> <code>add</code> inserts at the cursor, before the next element, and the loop continues with that next element, so separators aren't revisited.</p>"),
dict(level="business", title="Drop out-of-stock products", stmt="<p>Products as \"name:stock\": [Pen:4, Ink:0, Book:2, Clip:0]. Remove those with 0 stock and print the rest.</p>", inp="4 products",
 code='''import java.util.*;

public class Main {
    public static void main(String[] args) {
        List<String> products = new ArrayList<>(List.of("Pen:4", "Ink:0", "Book:2", "Clip:0"));
        Iterator<String> it = products.iterator();
        while (it.hasNext()) {
            String p = it.next();
            if (p.endsWith(":0")) it.remove();
        }
        System.out.println(products);
    }
}''', explain="<p><b>How it works:</b> safe in-place filtering in one pass.</p>"),
dict(level="business", title="Mask phone numbers in a list", stmt="<p>Replace each phone number in a contact list with a masked form (last 4 digits visible) using <code>set</code>.</p>", inp='["9876543210", "9123456789"]',
 code='''import java.util.*;

public class Main {
    public static void main(String[] args) {
        List<String> phones = new ArrayList<>(List.of("9876543210", "9123456789"));
        ListIterator<String> li = phones.listIterator();
        while (li.hasNext()) {
            String p = li.next();
            li.set("XXXXXX" + p.substring(6));
        }
        System.out.println(phones);
    }
}''', explain="<p><b>How it works:</b> <code>set</code> replaces in place without changing the list's size, so it's not a structural change.</p>"),
dict(level="business", title="Pages of results as an Iterable", stmt="<p>Write <code>Pages</code> that iterates over a list in pages of size 2, so a for-each gets one page (a sub-list) at a time.</p>", inp="[O1..O5], page size 2",
 code='''import java.util.*;

class Pages implements Iterable<List<String>> {
    private final List<String> all;
    private final int size;

    Pages(List<String> all, int size) { this.all = all; this.size = size; }

    public Iterator<List<String>> iterator() {
        return new Iterator<>() {
            int from = 0;
            public boolean hasNext() { return from < all.size(); }
            public List<String> next() {
                List<String> page = all.subList(from, Math.min(from + size, all.size()));
                from += size;
                return page;
            }
        };
    }
}

public class Main {
    public static void main(String[] args) {
        for (List<String> page : new Pages(List.of("O1", "O2", "O3", "O4", "O5"), 2)) {
            System.out.println(page);
        }
    }
}''', explain="<p><b>How it works:</b> callers just loop over pages; the paging logic lives inside the iterator.</p>"),
]
