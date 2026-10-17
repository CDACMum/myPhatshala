import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../..'))
from mkanim import Anim, two_view

def esc(t): return t.replace('<', '&lt;').replace('>', '&gt;')

# ---------------- Part 5: two-view animation ----------------
CODE = ['put("chai", 15)', 'put("idli", 30)', 'put("samosa", 20)', 'put("chai", 20)', 'get("samosa")', "// … 13th entry added"]
S = Anim("see", frames=6, h=250, label="HashMap calls: three puts, an update, a get, and a thirteenth entry that triggers a resize")
S.box(8, 8, 344, 132, None, fill="board", stroke="board")
for i, line in enumerate(CODE):
    y = 30 + i * 20
    S.box(12, y - 14, 336, 19, None, fill="none", stroke="track", sw=2, on=str(i + 1), rx=4)
    S.text(20, y, ("price." if i < 5 else "") + line, mono=True, size=10.5, cls="chalk" if i < 5 else "kw")
S.box(8, 150, 344, 50, None, fill="card2", stroke="line")
S.text(18, 168, "returns", size=9, cls="ink3", bold=True)
for f, t in {1: "null", 2: "null", 3: "null", 4: "15   (old value)", 5: "20", 6: "map still works, just faster"}.items():
    S.text(18, 190, t, on=str(f), mono=True, size=11, bold=True, cls="green" if f >= 4 else "ink")
S.note({1: "Add chai.", 2: "Add idli.", 3: "Add samosa.", 4: "Update chai's price.", 5: "Look up samosa.", 6: "The map grows."}, y=226, size=10.5)
S.caps(["<code>put</code> a new key returns <code>null</code>: there was no old value.",
        "Another new key.",
        "And another. Nothing on screen hints that anything special happened.",
        "<code>put</code> on an existing key replaces the value and returns the old one, 15. Size stays 3.",
        "<code>get(\"samosa\")</code> returns 20.",
        "Many dishes later, the 13th entry is added. Your code doesn't change; the map reorganises itself."])
B = Anim("behind", frames=6, h=250, label="The bucket table: chai in bucket 3, idli and samosa chained in bucket 9, an update in place, a get walking the chain, and a resize splitting the chain")
B.text(8, 16, "table (16 buckets)", on="1-5", size=10, bold=True, cls="ink2")
B.text(8, 16, "table (32 buckets) after resize", on="6", size=10, bold=True, cls="acc")
for k, b in enumerate([3, 9]):
    y = 28 + k * 44
    B.box(8, y, 344, 34, None, fill="card", stroke="line", on="1-5", rx=5)
    B.text(16, y + 22, f"[{b}]", on="1-5", mono=True, size=10, cls="ink3")
B.box(48, 32, 110, 26, 'chai = 15', fill="soft-blue", stroke="blue", on="1-3", size=10, mono=True, bold=True)
B.box(48, 32, 110, 26, 'chai = 20', fill="soft-green", stroke="green", on="4-5", size=10, mono=True, bold=True)
B.box(48, 76, 110, 26, 'idli = 30', fill="soft-blue", stroke="blue", on="2-5", size=10, mono=True, bold=True)
B.arrow(158, 89, 186, 89, on="3-5", color="track")
B.box(188, 76, 130, 26, 'samosa = 20', fill="soft-acc", stroke="track", on="3-5", size=10, mono=True, bold=True)
B.box(48, 76, 110, 26, None, fill="none", stroke="red", sw=3, on="5")
B.box(188, 76, 130, 26, None, fill="none", stroke="green", sw=3, on="5")
# resized table
for k, (b, lab) in enumerate([(3, "chai = 20"), (9, "idli = 30"), (25, "samosa = 20")]):
    y = 28 + k * 40
    B.box(8, y, 344, 32, None, fill="card", stroke="line", on="6", rx=5)
    B.text(16, y + 21, f"[{b}]", on="6", mono=True, size=10, cls="ink3")
    B.box(56, y + 4, 130, 24, lab, fill="soft-blue" if b != 25 else "soft-acc", stroke="blue" if b != 25 else "track", on="6", size=10, mono=True, bold=True)
B.text(196, 133, "moved 9 → 9 + 16", on="6", size=9.5, cls="acc", bold=True)
notes = {1: 'hash("chai") → index 3: empty → new node', 2: 'hash("idli") → index 9: empty → new node',
         3: 'hash("samosa") → index 9: idli ≠ samosa → chain', 4: 'index 3: equals("chai") → replace value',
         5: 'index 9: idli? no → samosa? yes → 20', 6: '13 > 16 × 0.75 → double: 9 stays, samosa → 25'}
for f, t in notes.items():
    B.text(180, 182, t, on=str(f), anchor="middle", size=9.6, bold=True, mono=True)
B.note({1: "One computed jump, no search.", 2: "Different key, different bucket.", 3: "A collision: both live in bucket 9.",
        4: "Same key: the node is updated in place.", 5: "Hash finds the bucket; equals finds the key.", 6: "Resize splits the chain using one more hash bit."}, y=222, size=10)
B.caps(["<code>hash(\"chai\")</code> mixes the hash code's bits; <code>(16 − 1) &amp; hash</code> = 3. Bucket 3 is empty, so a new node goes there.",
        "\"idli\" lands in bucket 9.",
        "\"samosa\" also lands in bucket 9: a collision. The map compares with idli (hash, then <code>equals</code>): different key, so the new node is linked after idli.",
        "\"chai\" again: bucket 3, the existing node's key <code>equals</code> \"chai\", so only the value changes (15 → 20). The old value is returned.",
        "<code>get(\"samosa\")</code> computes the same index 9, checks idli (not equal), moves to the next node, finds samosa and returns 20.",
        "When the 13th entry pushes size past the threshold 12, the table doubles to 32. Each node moves to the same index or index + 16, decided by one extra hash bit: idli stays at 9, samosa goes to 25. The chain is gone."])
ANIM = two_view("Inside a HashMap", S, B)
BLOCKS = {'ANIM': ANIM}

# ---------------- Part 6: animated example ----------------
ANIM2_HEADING = "Watch it with an example: an IFSC lookup at a bank"
ANIM2_INTRO = "A payments service maps IFSC codes to branch details. Watch one lookup: no scanning of thousands of branches, just a computed jump and one or two equals checks."
A = Anim("Looking up an IFSC code", frames=4, h=210, label="An IFSC code is hashed to a bucket; equals confirms the matching entry in a short chain")
A.box(10, 14, 150, 34, '"SBIN0001234"', fill="soft-blue", stroke="blue", size=10.5, mono=True, bold=True)
A.arrow(160, 31, 196, 31, on="2-", color="track")
A.text(178, 24, "hash", on="2-", anchor="middle", size=8.5, cls="acc", bold=True)
A.box(200, 14, 152, 34, "bucket 1,847 of 4,096", fill="soft-acc", stroke="track", on="2-", size=9.5, bold=True)
A.box(10, 70, 342, 40, None, fill="card", stroke="line", on="3-")
A.box(18, 78, 150, 24, "HDFC0000240 ✗", fill="card2", stroke="line", on="3-", size=9.5, mono=True)
A.arrow(168, 90, 184, 90, on="3-", color="ink", sw=1.4)
A.box(186, 78, 158, 24, "SBIN0001234 ✓", fill="soft-green", stroke="green", on="3-", size=9.5, mono=True, bold=True)
A.box(10, 126, 342, 34, "SBI · Kharghar · Navi Mumbai", fill="soft-green", stroke="green", on="4", size=11, bold=True)
A.note({1: "A key arrives.", 2: "Its hash picks one bucket out of thousands.", 3: "A short chain: equals finds the match.", 4: "The value comes back."}, y=184, size=11)
A.caps(["A transfer request carries the IFSC code <code>SBIN0001234</code>.",
        "The code's <code>hashCode()</code> is spread and masked into a bucket index. The other 4,095 buckets are never touched.",
        "That bucket happens to hold two entries. One <code>equals</code> check fails, the next succeeds.",
        "The branch details come back in a few steps, whether the map holds 100 or 1,50,000 branches. (Simplified: real systems also validate the code format and cache results.)"])
ANIM2 = A

# ---------------- Part 8: tracer ----------------
TRACE = dict(code='''import java.util.HashMap;
import java.util.Map;

public class Main {
    public static void main(String[] args) {
        Map<String, Integer> price = new HashMap<>();
        price.put("chai", 15);
        price.put("idli", 30);
        price.put("samosa", 20);
        Integer old = price.put("chai", 20);
        int p = price.get("samosa");
        System.out.println(old + " " + p + " " + price.size());
    }
}
''', notes={
 6: "Create :: No bucket table yet: it's allocated on the first put (16 buckets).",
 7: "Put :: = \"chai\" hashes to bucket 3. The heap now shows a 16-bucket table with one entry.",
 8: "Put :: \"idli\" lands in bucket 9.",
 9: "Collision :: = \"samosa\" also maps to bucket 9. Look at the heap: <code>[9] \"idli\"=30 → \"samosa\"=20</code>, a chain of two nodes.",
 10: "Update :: = Same key \"chai\": the existing node's value changes to 20, and <code>put</code> returns the old value 15. Size stays 3.",
 11: "Get :: = <code>get(\"samosa\")</code>: bucket 9, skip idli (not equal), match samosa → 20, unboxed into <code>p</code>.",
 12: "Print :: "})

# ---------------- Worked examples ----------------
WORKED_INTRO = "Three classic HashMap tasks, traced on the real JVM. The first one shows a resize happening."
EXAMPLES = [
dict(tag="Internals · resize", title="Watch the table double at the 13th entry",
 problem="<p>Add 13 menu items to a HashMap and observe, on the heap, the table growing from 16 to 32 buckets and the idli/samosa chain splitting.</p>",
 inp="13 dishes",
 approach=["Put the dishes in a loop.",
           "Watch the heap line: “16 buckets” until size 12, then “32 buckets”.",
           "Notice samosa moving from bucket 9 to bucket 25."],
 code='''import java.util.HashMap;
import java.util.Map;

public class Main {
    public static void main(String[] args) {
        String[] dishes = {"idli", "samosa", "chai", "dosa", "vada", "poha",
                           "upma", "dal", "puri", "naan", "kheer", "lassi", "pav"};
        Map<String, Integer> menu = new HashMap<>();
        for (int i = 0; i < dishes.length; i++) {
            menu.put(dishes[i], 10 + i);
        }
        System.out.println(menu.size() + " dishes");
    }
}
''', notes={(10, 2): "Collision :: = \"samosa\" joins \"idli\" in bucket 9.",
            (10, 12): "Threshold :: = 12 entries: exactly at the threshold (16 × 0.75). One more triggers a resize.",
            (10, 13): "Resize :: = The 13th put makes size 13 &gt; 12: the table doubles to <b>32 buckets</b>. Look for idli in [9] and samosa now in [25]."},
 tryit="Press <b>Run</b>. Then create the map with <code>new HashMap&lt;&gt;(32)</code>: no resize is needed for 13 entries."),
dict(tag="Logistics · grouping", title="Group parcels by city",
 problem="<p>Parcels arrive as \"id:city\". Group parcel IDs by city with <code>computeIfAbsent</code> and print the groups in city order.</p>",
 inp='["P1:Pune", "P2:Mumbai", "P3:Pune", "P4:Thane"]',
 approach=["A <code>TreeMap&lt;String, List&lt;String&gt;&gt;</code> so cities print sorted.",
           "For each parcel, <code>computeIfAbsent(city, k -&gt; new ArrayList&lt;&gt;())</code> returns the city's list, creating it the first time.",
           "Add the ID to that list."],
 code='''import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.TreeMap;

public class Main {
    public static void main(String[] args) {
        String[] parcels = {"P1:Pune", "P2:Mumbai", "P3:Pune", "P4:Thane"};
        Map<String, List<String>> byCity = new TreeMap<>();
        for (String p : parcels) {
            String[] part = p.split(":");
            byCity.computeIfAbsent(part[1], k -> new ArrayList<>()).add(part[0]);
        }
        System.out.println(byCity);
    }
}
''', tryit="Press <b>Run</b>. Then print how many parcels go to each city using <code>byCity.get(city).size()</code>."),
dict(tag="Retail · two-sum", title="Two items that use a gift card exactly",
 problem="<p>A customer has a ₹500 gift card. From prices [120, 260, 380, 240], find two different items whose prices add up to exactly 500, in one pass.</p>",
 inp="prices [120, 260, 380, 240], target 500",
 approach=["Keep a map from price → index of items seen so far.",
           "For each price p, check whether <code>500 − p</code> is already in the map.",
           "If yes, report the pair; otherwise store p. O(n) instead of checking every pair."],
 code='''import java.util.HashMap;
import java.util.Map;

public class Main {
    static int[] pair(int[] prices, int target) {
        Map<Integer, Integer> seen = new HashMap<>();
        for (int i = 0; i < prices.length; i++) {
            int need = target - prices[i];
            Integer j = seen.get(need);
            if (j != null) {
                return new int[]{j, i};
            }
            seen.put(prices[i], i);
        }
        return null;
    }

    public static void main(String[] args) {
        int[] prices = {120, 260, 380, 240};
        int[] r = pair(prices, 500);
        System.out.println("Items " + r[0] + " and " + r[1] + ": ₹" + prices[r[0]] + " + ₹" + prices[r[1]]);
    }
}
''', tryit="Press <b>Run</b>. Then try a target of 1000 and handle the <code>null</code> result."),
]

# ---------------- Practice problems ----------------
PRACTICE_INTRO = "Use HashMap fluently and reason about its internals. The last three are business tasks."
PROBLEMS = [
dict(level="easy", title="Character frequency", stmt="<p>Count how many times each character appears in <code>\"banana\"</code>, printed in alphabetical order.</p>", inp='"banana"',
 code='''import java.util.*;

public class Main {
    public static void main(String[] args) {
        Map<Character, Integer> freq = new TreeMap<>();
        for (char c : "banana".toCharArray()) freq.merge(c, 1, Integer::sum);
        System.out.println(freq);
    }
}''', explain="<p><b>How it works:</b> <code>merge</code> inserts 1 for a new key or adds 1 to the existing count.</p>"),
dict(level="easy", title="Iterate entries", stmt="<p>Print each state with its capital from a map of three states, one per line, in insertion order.</p>", inp="Maharashtra, Karnataka, Gujarat",
 code='''import java.util.*;

public class Main {
    public static void main(String[] args) {
        Map<String, String> cap = new LinkedHashMap<>();
        cap.put("Maharashtra", "Mumbai");
        cap.put("Karnataka", "Bengaluru");
        cap.put("Gujarat", "Gandhinagar");
        for (Map.Entry<String, String> e : cap.entrySet()) {
            System.out.println(e.getKey() + " → " + e.getValue());
        }
    }
}''', explain="<p><b>How it works:</b> <code>entrySet()</code> gives key and value together; LinkedHashMap keeps insertion order.</p>"),
dict(level="easy", title="Compute the bucket index", stmt="<p>Write the HashMap index formula and print the 16-bucket index of \"Aa\", \"BB\" and \"chai\".</p>", inp='"Aa", "BB", "chai"',
 code='''public class Main {
    static int index(Object key, int n) {
        int h = key.hashCode();
        return (n - 1) & (h ^ (h >>> 16));
    }

    public static void main(String[] args) {
        for (String k : new String[]{"Aa", "BB", "chai"}) System.out.print(k + "→" + index(k, 16) + " ");
        System.out.println();
    }
}''', explain="<p><b>How it works:</b> \"Aa\" and \"BB\" have the same hash code (2112), so they always collide.</p>"),
dict(level="medium", title="First non-repeating character", stmt="<p>Find the first character in <code>\"swiss\"</code> that appears only once.</p>", inp='"swiss"',
 code='''import java.util.*;

public class Main {
    public static void main(String[] args) {
        String s = "swiss";
        Map<Character, Integer> count = new LinkedHashMap<>();
        for (char c : s.toCharArray()) count.merge(c, 1, Integer::sum);
        for (Map.Entry<Character, Integer> e : count.entrySet()) {
            if (e.getValue() == 1) { System.out.println(e.getKey()); break; }
        }
    }
}''', explain="<p><b>How it works:</b> a LinkedHashMap counts in one pass and remembers first-seen order for the second pass. O(n).</p>"),
dict(level="medium", title="Invert a map", stmt="<p>Invert {chai=15, vada=25, poha=15} into price → list of dishes, sorted by price.</p>", inp="{chai=15, vada=25, poha=15}",
 code='''import java.util.*;

public class Main {
    public static void main(String[] args) {
        Map<String, Integer> price = new LinkedHashMap<>();
        price.put("chai", 15); price.put("vada", 25); price.put("poha", 15);
        Map<Integer, List<String>> byPrice = new TreeMap<>();
        for (Map.Entry<String, Integer> e : price.entrySet()) {
            byPrice.computeIfAbsent(e.getValue(), k -> new ArrayList<>()).add(e.getKey());
        }
        System.out.println(byPrice);
    }
}''', explain="<p><b>How it works:</b> values may repeat, so the inverted map's values are lists.</p>"),
dict(level="business", title="Stock after orders", stmt="<p>Stock: pen 10, book 4. Orders: pen 3, book 5, pen 2. Fulfil an order only if enough stock exists; print rejected orders and final stock.</p>", inp="3 orders",
 code='''import java.util.*;

public class Main {
    public static void main(String[] args) {
        Map<String, Integer> stock = new TreeMap<>(Map.of("pen", 10, "book", 4));
        String[] item = {"pen", "book", "pen"};
        int[] qty = {3, 5, 2};
        for (int i = 0; i < item.length; i++) {
            int have = stock.getOrDefault(item[i], 0);
            if (have >= qty[i]) stock.put(item[i], have - qty[i]);
            else System.out.println("Rejected: " + item[i] + " x" + qty[i]);
        }
        System.out.println(stock);
    }
}''', explain="<p><b>How it works:</b> each order is one O(1) lookup and one update.</p>"),
dict(level="business", title="Join orders with customers", stmt="<p>Customers: (1, Riya), (2, Kabir). Orders: (101, cust 2), (102, cust 1), (103, cust 2). Print each order with the customer name, using a map instead of a nested loop.</p>", inp="2 customers, 3 orders",
 code='''import java.util.*;

public class Main {
    public static void main(String[] args) {
        Map<Integer, String> customer = new HashMap<>();
        customer.put(1, "Riya");
        customer.put(2, "Kabir");
        int[][] orders = {{101, 2}, {102, 1}, {103, 2}};
        for (int[] o : orders) {
            System.out.println("Order " + o[0] + " → " + customer.get(o[1]));
        }
    }
}''', explain="<p><b>How it works:</b> building the map is O(c) and each lookup O(1), so the join is O(c + o) instead of O(c × o).</p>"),
dict(level="business", title="Rate-limit API keys", stmt="<p>Each API key may make at most 3 calls. Process calls K1, K2, K1, K1, K1, K2 and print which are allowed.</p>", inp="K1, K2, K1, K1, K1, K2",
 code='''import java.util.*;

public class Main {
    public static void main(String[] args) {
        Map<String, Integer> used = new HashMap<>();
        for (String key : new String[]{"K1", "K2", "K1", "K1", "K1", "K2"}) {
            int n = used.merge(key, 1, Integer::sum);
            System.out.println(key + (n <= 3 ? " allowed (" + n + ")" : " BLOCKED"));
        }
    }
}''', explain="<p><b>How it works:</b> <code>merge</code> returns the new count, so the check and update are one call. (A real limiter also resets counts per time window and uses ConcurrentHashMap.)</p>"),
]
