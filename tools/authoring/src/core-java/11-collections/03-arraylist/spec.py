import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../..'))
from mkanim import Anim, two_view

def esc(t): return t.replace('<', '&lt;').replace('>', '&gt;')

# ---------------- Part 5: two-view animation ----------------
CODE = ["List<String> w = new ArrayList<>();", 'w.add("W1");', "// … add W2 to W10", 'w.add("W11");', 'w.add(1, "VIP");', 'w.remove("W3");']
S = Anim("see", frames=6, h=250, label="Adding to an ArrayList past ten elements, inserting at index 1 and removing a value")
S.box(8, 8, 344, 132, None, fill="board", stroke="board")
for i, line in enumerate(CODE):
    y = 30 + i * 20
    S.box(12, y - 14, 336, 19, None, fill="none", stroke="track", sw=2, on=str(i + 1), rx=4)
    S.text(20, y, esc(line), mono=True, size=10.2, cls="chalk" if i != 2 else "kw")
S.box(8, 150, 344, 56, None, fill="card2", stroke="line")
S.text(18, 168, "println(w)   size()", size=9, cls="ink3", bold=True)
outs = {1: ("[]", "0"), 2: ("[W1]", "1"), 3: ("[W1 … W10]", "10"), 4: ("[W1 … W10, W11]", "11"),
        5: ("[W1, VIP, W2 … W11]", "12"), 6: ("[W1, VIP, W2, W4 … W11]", "11")}
for f, (a, b) in outs.items():
    S.text(18, 192, a, on=str(f), mono=True, size=10, bold=True)
    S.text(340, 192, b, on=str(f), mono=True, size=11, bold=True, anchor="end", cls="green")
S.note({1: "An empty list.", 2: "One passenger.", 3: "Ten passengers.", 4: "The 11th just works.", 5: "Insert at position 1.",
        6: "Remove by value."}, y=232, size=10.5)
S.caps(["An empty ArrayList: size 0.", "<code>add</code> appends W1: size 1.", "Nine more adds: size 10.",
        "The 11th add works like any other. You can't tell anything special happened.",
        "<code>add(1, \"VIP\")</code> puts VIP second; everyone after moves back one place.",
        "<code>remove(\"W3\")</code> finds W3 and closes the gap. Size goes back to 11."])
B = Anim("behind", frames=6, h=250, label="The internal elementData array: empty, capacity 10, full, copied into capacity 15, shifted right for an insert and left for a removal")
B.text(8, 18, "elementData (internal array)", size=10, bold=True, cls="ink2")
def row(y, n, filled, on, labels=None, hl=None, red=None):
    w = 344 / max(n, 1)
    for k in range(n):
        x = 8 + k * w
        lab = labels[k] if labels and k < len(labels) else ""
        fill = "soft-acc" if k < filled else "card"
        stroke = "track" if k < filled else "line"
        if hl is not None and k in hl: fill, stroke = "soft-green", "green"
        if red is not None and k in red: fill, stroke = "soft-acc", "red"
        B.box(x + 1, y, w - 2, 30, lab, fill=fill, stroke=stroke, on=on, size=7.5, mono=True, rx=3)
B.box(8, 30, 120, 30, "{ } capacity 0", fill="card2", stroke="line", on="1", size=9.5, mono=True)
row(30, 10, 1, "2", ["W1"])
row(30, 10, 10, "3", [f"W{i}" for i in range(1, 11)])
row(30, 10, 10, "4", [f"W{i}" for i in range(1, 11)])
row(80, 15, 11, "4", [f"W{i}" for i in range(1, 12)], hl={10})
B.arrow(180, 62, 180, 78, on="4", color="track")
row(30, 15, 12, "5", ["W1", "VIP"] + [f"W{i}" for i in range(2, 12)], hl={1})
row(30, 15, 11, "6", ["W1", "VIP", "W2"] + [f"W{i}" for i in range(4, 12)], red=None)
B.text(8, 132, "capacity 10, size 1", on="2", mono=True, size=10, bold=True)
B.text(8, 132, "capacity 10, size 10: FULL", on="3", mono=True, size=10, bold=True, cls="red")
B.text(8, 132, "grow: new Object[15], copy 10 refs, store W11", on="4", mono=True, size=9.5, bold=True, cls="acc")
B.text(8, 132, "W2…W11 shifted right by one (O(n))", on="5", mono=True, size=9.5, bold=True, cls="acc")
B.text(8, 132, "W4…W11 shifted left by one (O(n))", on="6", mono=True, size=9.5, bold=True, cls="acc")
B.arrow(60, 160, 300, 160, on="5", color="track")
B.arrow(300, 160, 100, 160, on="6", color="track")
B.note({1: "No array of 10 until it's needed.", 2: "First add: capacity 10.", 3: "Every slot used.", 4: "Bigger array, copy, continue.",
        5: "Inserting shifts the tail right.", 6: "Removing shifts the tail left."}, y=200, size=10.5)
B.caps(["A new ArrayList points to a shared empty array. Nothing is allocated until the first add.",
        "First <code>add</code>: an <code>Object[10]</code> is created. W1's reference goes into slot 0; <code>size</code> = 1.",
        "After ten adds, <code>size</code> equals the capacity. The array is full.",
        "The 11th add calls <code>grow()</code>: capacity 10 + 10/2 = <b>15</b>. A new array is allocated, the 10 references are copied, and W11 goes into slot 10. The old array becomes garbage.",
        "<code>add(1, …)</code> uses <code>System.arraycopy</code> to move W2…W11 one slot right, then writes VIP into slot 1.",
        "<code>remove(\"W3\")</code> searches with <code>equals</code>, then moves W4…W11 one slot left and clears the last slot. Capacity stays 15."])
ANIM = two_view("Inside an ArrayList", S, B)
BLOCKS = {'ANIM': ANIM}

# ---------------- Part 6: animated example ----------------
ANIM2_HEADING = "Watch it with an example: a music app's playlist"
ANIM2_INTRO = "A playlist is an ArrayList of songs. Watch jumping to a song (instant), adding at the end (cheap) and inserting at the top (every song moves)."
A = Anim("Playlist operations and their cost", frames=4, h=214, label="Getting song 3 is instant, appending is cheap, inserting at the front shifts every song")
songs = ["Song A", "Song B", "Song C", "Song D"]
for k, s in enumerate(songs):
    A.box(10 + k * 58, 30, 54, 40, s, fill="soft-acc", stroke="track", size=9, bold=True,
          pos={"1": "0,0", "2": "0,0", "3": "0,0", "4": "58,0"})
A.text(10, 22, "index 0", size=8.5, cls="ink3")
A.box(242, 30, 54, 40, "Song E", fill="soft-green", stroke="green", on="3-", size=9, bold=True, pos={"3": "0,0", "4": "58,0"})
A.box(10, 30, 54, 40, "Intro", fill="soft-green", stroke="green", on="4", size=9, bold=True)
A.box(126, 30, 54, 40, None, fill="none", stroke="blue", sw=3, on="2")
A.text(181, 104, "playlist.get(2) → Song C", on="2", anchor="middle", mono=True, size=11, bold=True, cls="blue")
A.text(181, 124, "one step, whatever the length: O(1)", on="2", anchor="middle", size=10, cls="ink2")
A.text(181, 104, "playlist.add(\"Song E\")", on="3", anchor="middle", mono=True, size=11, bold=True, cls="green")
A.text(181, 124, "a free slot at the end: O(1)", on="3", anchor="middle", size=10, cls="ink2")
A.text(181, 104, "playlist.add(0, \"Intro\")", on="4", anchor="middle", mono=True, size=11, bold=True, cls="acc")
A.text(181, 124, "every song moves one place: O(n)", on="4", anchor="middle", size=10, cls="ink2")
A.text(181, 104, "a list of 4 songs", on="1", anchor="middle", size=11, cls="ink2")
A.note({1: "Songs kept in order.", 2: "Jump to the third song.", 3: "Add to the end.", 4: "Insert at the top."}, y=170, size=11)
A.caps(["The playlist holds songs in order; index 0 is the first song.",
        "Tapping the third song calls <code>get(2)</code>. The list reads <code>elementData[2]</code> directly: instant even with 10,000 songs.",
        "Adding a song at the end usually just fills the next free slot.",
        "Inserting “Intro” at position 0 shifts every existing song one place right. With 10,000 songs that's 10,000 moves. (Simplified: real apps often store huge playlists in a database and load pages.)"])
ANIM2 = A

# ---------------- Part 8: tracer ----------------
TRACE = dict(code='''import java.util.ArrayList;
import java.util.List;

public class Main {
    public static void main(String[] args) {
        List<String> w = new ArrayList<>();
        for (int i = 1; i <= 11; i++) {
            w.add("W" + i);
        }
        w.remove(0);
        System.out.println(w.size() + " waiting, first " + w.get(0));
    }
}
''', notes={
 6: "Create :: Look at the heap: size 0 and capacity 0, no array allocated yet.",
 (8, 1): "First add :: = The first <code>add</code> allocates the default array of 10. Heap: size 1, capacity 10.",
 (8, 10): "Full :: = Ten elements: size 10, capacity 10. The array is full.",
 (8, 11): "Grow :: = The 11th <code>add</code> doesn't fit: ArrayList creates a new array of 10 + 10/2 = <b>15</b> slots, copies the 10 references and adds W11. Heap: size 11, capacity 15.",
 10: "Remove :: = <code>remove(0)</code> deletes W1 and shifts all 10 others one slot left. Size 10; capacity stays 15.",
 11: "Print :: "})

# ---------------- Worked examples ----------------
WORKED_INTRO = "Three ArrayList tasks from real apps. Watch size and capacity on the heap, and the frames of the helper methods."
EXAMPLES = [
dict(tag="Education · list maths", title="Class average and toppers",
 problem="<p>Marks are collected into an <code>ArrayList&lt;Integer&gt;</code>. Compute the average and list the positions (1-based) of students who scored the highest mark.</p>",
 inp="[78, 91, 64, 91]",
 approach=["A helper <code>average(List&lt;Integer&gt; m)</code> loops by index with <code>get(i)</code>.",
           "<code>Collections.max</code> gives the top mark.",
           "Loop again and collect positions with that mark into a new list."],
 code='''import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class Main {
    static double average(List<Integer> m) {
        int sum = 0;
        for (int i = 0; i < m.size(); i++) {
            sum += m.get(i);
        }
        return (double) sum / m.size();
    }

    public static void main(String[] args) {
        List<Integer> marks = new ArrayList<>(List.of(78, 91, 64, 91));
        int top = Collections.max(marks);
        List<Integer> toppers = new ArrayList<>();
        for (int i = 0; i < marks.size(); i++) {
            if (marks.get(i) == top) toppers.add(i + 1);
        }
        System.out.println("Average " + average(marks) + ", top " + top + " by " + toppers);
    }
}
''', tryit="Press <b>Run</b>. Then add a third 91 and check the output. (<code>marks.get(i) == top</code> compares values here because <code>top</code> is an <code>int</code>, so the Integer is unboxed.)"),
dict(tag="Retail · cleanup", title="Remove expired items safely",
 problem="<p>A grocery list stores days-to-expiry for each item. Remove every item with 0 days left, without a <code>ConcurrentModificationException</code>.</p>",
 inp="[3, 0, 5, 0, 1]",
 approach=["Loop <b>backwards</b> by index, so removing an element doesn't skip the next one.",
           "Use <code>remove(int)</code>, passing the index.",
           "Print the list that's left."],
 code='''import java.util.ArrayList;
import java.util.List;

public class Main {
    public static void main(String[] args) {
        List<Integer> daysLeft = new ArrayList<>(List.of(3, 0, 5, 0, 1));
        for (int i = daysLeft.size() - 1; i >= 0; i--) {
            if (daysLeft.get(i) == 0) {
                daysLeft.remove(i);
            }
        }
        System.out.println(daysLeft);
    }
}
''', notes={(9, 1): "Remove :: = <code>remove(i)</code> with an int index (i = 3). Going backwards, the elements still to check (indexes 0–2) don't move."},
 tryit="Press <b>Run</b>. Then rewrite it with <code>daysLeft.removeIf(d -&gt; d == 0);</code>."),
dict(tag="Travel · insert in order", title="Keep stops sorted by time",
 problem="<p>A bus route keeps stop times (minutes after start) sorted. Insert a new stop at 25 minutes into <code>[10, 20, 40]</code> at the right position.</p>",
 inp="stops [10, 20, 40], new stop 25",
 approach=["A helper <code>insertSorted(list, t)</code> finds the first index whose time is greater than t.",
           "<code>add(index, t)</code> inserts there; later stops shift right.",
           "Print the route."],
 code='''import java.util.ArrayList;
import java.util.List;

public class Main {
    static void insertSorted(List<Integer> stops, int t) {
        int i = 0;
        while (i < stops.size() && stops.get(i) < t) {
            i++;
        }
        stops.add(i, t);
    }

    public static void main(String[] args) {
        List<Integer> stops = new ArrayList<>(List.of(10, 20, 40));
        insertSorted(stops, 25);
        System.out.println(stops);
    }
}
''', notes={10: "Insert :: = <code>add(2, 25)</code>: 40 shifts one slot right and 25 goes into index 2."},
 tryit="Press <b>Run</b>. Then insert 5 and 50 as well."),
]

# ---------------- Practice problems ----------------
PRACTICE_INTRO = "Everyday ArrayList work: add, read, search, remove safely and reason about cost. The last three are business tasks."
PROBLEMS = [
dict(level="easy", title="Build and print a list", stmt="<p>Add five city names to an ArrayList, print the list, its size, and the third city.</p>", inp="Mumbai, Pune, Nashik, Thane, Panvel",
 code='''import java.util.ArrayList;
import java.util.List;

public class Main {
    public static void main(String[] args) {
        List<String> cities = new ArrayList<>();
        cities.add("Mumbai");
        cities.add("Pune");
        cities.add("Nashik");
        cities.add("Thane");
        cities.add("Panvel");
        System.out.println(cities + " " + cities.size() + " " + cities.get(2));
    }
}''', explain="<p><b>How it works:</b> indexes start at 0, so the third city is <code>get(2)</code>.</p>"),
dict(level="easy", title="Sum with for-each", stmt="<p>Sum the prices <code>[120, 45, 60]</code> stored in an <code>ArrayList&lt;Integer&gt;</code>.</p>", inp="[120, 45, 60]",
 code='''import java.util.ArrayList;
import java.util.List;

public class Main {
    public static void main(String[] args) {
        List<Integer> prices = new ArrayList<>(List.of(120, 45, 60));
        int total = 0;
        for (int p : prices) total += p;
        System.out.println("Total ₹" + total);
    }
}''', explain="<p><b>How it works:</b> the for-each loop reads each Integer and unboxes it into <code>p</code>.</p>"),
dict(level="easy", title="Replace with set", stmt="<p>In <code>[\"chai\", \"coffee\", \"lassi\"]</code>, replace \"coffee\" with \"filter coffee\" using <code>indexOf</code> and <code>set</code>.</p>", inp='["chai", "coffee", "lassi"]',
 code='''import java.util.ArrayList;
import java.util.List;

public class Main {
    public static void main(String[] args) {
        List<String> drinks = new ArrayList<>(List.of("chai", "coffee", "lassi"));
        int i = drinks.indexOf("coffee");
        if (i != -1) drinks.set(i, "filter coffee");
        System.out.println(drinks);
    }
}''', explain="<p><b>How it works:</b> <code>set</code> replaces in place, O(1), without shifting anything.</p>"),
dict(level="medium", title="Remove duplicates, keep order", stmt="<p>From <code>[3, 1, 3, 2, 1]</code> build a new list with each value once, in first-seen order, using only ArrayList methods.</p>", inp="[3, 1, 3, 2, 1]",
 code='''import java.util.ArrayList;
import java.util.List;

public class Main {
    public static void main(String[] args) {
        List<Integer> in = List.of(3, 1, 3, 2, 1);
        List<Integer> out = new ArrayList<>();
        for (Integer x : in) {
            if (!out.contains(x)) out.add(x);
        }
        System.out.println(out);
    }
}''', explain="<p><b>How it works:</b> <code>contains</code> is O(n), so this is O(n²): fine for small lists. For large ones, a LinkedHashSet does it in O(n).</p>"),
dict(level="medium", title="Reverse in place", stmt="<p>Reverse <code>[1, 2, 3, 4, 5]</code> in place by swapping from both ends with <code>get</code>/<code>set</code>.</p>", inp="[1, 2, 3, 4, 5]",
 code='''import java.util.ArrayList;
import java.util.List;

public class Main {
    public static void main(String[] args) {
        List<Integer> a = new ArrayList<>(List.of(1, 2, 3, 4, 5));
        for (int i = 0, j = a.size() - 1; i < j; i++, j--) {
            Integer t = a.get(i);
            a.set(i, a.get(j));
            a.set(j, t);
        }
        System.out.println(a);
    }
}''', explain="<p><b>How it works:</b> random access makes each swap O(1), so the whole reversal is O(n). <code>Collections.reverse</code> does the same.</p>"),
dict(level="business", title="Top 3 sellers", stmt="<p>Daily sales per product are in a list. Sort a copy in descending order and print the top 3 values.</p>", inp="[340, 120, 990, 560, 75]",
 code='''import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class Main {
    public static void main(String[] args) {
        List<Integer> sales = List.of(340, 120, 990, 560, 75);
        List<Integer> sorted = new ArrayList<>(sales);
        sorted.sort(Collections.reverseOrder());
        System.out.println("Top 3: " + sorted.subList(0, 3));
    }
}''', explain="<p><b>How it works:</b> we sort a copy (the original is immutable) in reverse order, then take a view of the first three with <code>subList</code>.</p>"),
dict(level="business", title="Split orders into batches", stmt="<p>A courier sends orders in batches of 3. Split <code>[O1 … O7]</code> into batches and print each.</p>", inp="O1..O7, batch size 3",
 code='''import java.util.ArrayList;
import java.util.List;

public class Main {
    public static void main(String[] args) {
        List<String> orders = new ArrayList<>();
        for (int i = 1; i <= 7; i++) orders.add("O" + i);
        for (int start = 0; start < orders.size(); start += 3) {
            int end = Math.min(start + 3, orders.size());
            System.out.println("Batch: " + orders.subList(start, end));
        }
    }
}''', explain="<p><b>How it works:</b> <code>subList(from, to)</code> gives a window of the list; <code>Math.min</code> handles the shorter last batch.</p>"),
dict(level="business", title="Pre-sized list for a big import", stmt="<p>An import job knows it will load 100,000 rows. Create the list with that capacity, add the rows, and print the size.</p>", inp="100,000 rows",
 code='''import java.util.ArrayList;
import java.util.List;

public class Main {
    public static void main(String[] args) {
        int rows = 100_000;
        List<Integer> ids = new ArrayList<>(rows);   // no resizing needed
        for (int i = 0; i < rows; i++) ids.add(i);
        System.out.println("Loaded " + ids.size() + " rows, last id " + ids.get(ids.size() - 1));
    }
}''', explain="<p><b>How it works:</b> with the right initial capacity, the list never has to grow and copy. Without it, there would be about 23 grow-and-copy rounds.</p>"),
]
