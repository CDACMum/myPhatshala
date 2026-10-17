import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../..'))
from mkanim import Anim, two_view

def esc(t): return t.replace('<', '&lt;').replace('>', '&gt;')

# ---------------- Part 5: two-view animation ----------------
CODE = ["List<String> names = new ArrayList<>();", 'names.add("Riya");', "names.add(21007);",
        "String s = names.get(0);", "// javac writes the class file", "// the program runs"]
S = Anim("see", frames=6, h=250, label="Generic list code: a correct add, a rejected add, a read without a cast, then compilation and running")
S.box(8, 8, 344, 132, None, fill="board", stroke="board")
for i, line in enumerate(CODE):
    y = 30 + i * 20
    S.box(12, y - 14, 336, 19, None, fill="none", stroke="track" if i != 2 else "red", sw=2, on=str(i + 1), rx=4)
    S.text(20, y, esc(line), mono=True, size=10, cls="chalk" if i < 4 else "kw")
S.box(8, 150, 344, 50, None, fill="card2", stroke="line")
S.text(18, 168, "javac / console", size=9, cls="ink3", bold=True)
S.text(18, 188, "✗ int cannot be converted to String", on="3", mono=True, size=10, cls="red", bold=True)
S.text(18, 188, "✓ compiles (after removing the bad line)", on="5", mono=True, size=10, cls="green", bold=True)
S.text(18, 188, "RIYA", on="6", mono=True, size=11, cls="green", bold=True)
S.note({1: "A list labelled: Strings only.", 2: "A String goes in.", 3: "A number is refused.", 4: "Reading needs no cast.",
        5: "Compile.", 6: "Run."}, y=226, size=10.5)
S.caps(["The variable is declared <code>List&lt;String&gt;</code>; the diamond on the right is filled in by javac.",
        "Adding a String is fine.",
        "Adding <code>21007</code> is a <b>compile error</b>. The bug is caught where it's written.",
        "<code>names.get(0)</code> is used as a String directly. No <code>(String)</code> cast in your code.",
        "With the bad line removed, javac produces the class file.",
        "The program runs and prints the name in capitals."])
B = Anim("behind", frames=6, h=250, label="javac substitutes E = String to check calls, then erases the type and inserts a checkcast")
B.box(8, 8, 344, 30, None, fill="soft-blue", stroke="blue")
B.text(18, 28, esc("interface List<E> { boolean add(E e); E get(int i); }"), mono=True, size=9.2, cls="ink")
B.box(8, 48, 344, 88, None, fill="card", stroke="line")
B.text(18, 66, "javac check", on="1-4", size=10, bold=True, cls="ink2")
B.text(18, 88, "E = String (diamond → ArrayList<String>)".replace('<', '&lt;').replace('>', '&gt;'), on="1-4", mono=True, size=9.5)
B.text(18, 108, "add(E) = add(String) ← \"Riya\" ✓", on="2", mono=True, size=9.5, cls="green", bold=True)
B.text(18, 108, "add(String) ← int 21007 ✗ stop", on="3", mono=True, size=9.5, cls="red", bold=True)
B.text(18, 108, "get(int) returns E = String ✓", on="4", mono=True, size=9.5, cls="green", bold=True)
B.text(18, 66, "class file (after erasure)", on="5", size=10, bold=True, cls="ink2")
B.lines(18, 88, ["List.add(Object)", "List.get(int) → Object", "checkcast String   ← inserted"], on="5", mono=True, size=9.5, gap=16)
B.text(18, 66, "heap at run time", on="6", size=10, bold=True, cls="ink2")
B.box(18, 76, 200, 50, None, fill="soft-acc", stroke="track", on="6")
B.lines(26, 94, ["ArrayList", 'elementData: Object[] {"Riya"}'], on="6", mono=True, size=9.2, gap=16)
B.text(230, 98, "no <String>".replace('<', '&lt;').replace('>', '&gt;'), on="6", mono=True, size=9.5, cls="acc", bold=True)
B.text(230, 114, "anywhere", on="6", mono=True, size=9.5, cls="acc", bold=True)
B.note({1: "E is replaced by String for checking.", 2: "The argument matches add(String).", 3: "int doesn't fit add(String).",
        4: "The result type is known: String.", 5: "Types erased; a cast is added.", 6: "One ArrayList class for all types."}, y=180, size=10.5)
B.caps(["javac reads <code>List&lt;String&gt;</code> and substitutes <code>E = String</code> into every method of <code>List</code> for checking.",
        "<code>add(E)</code> is checked as <code>add(String)</code>: \"Riya\" fits.",
        "An <code>int</code> doesn't fit <code>add(String)</code>, and it can't be boxed to String either. javac stops with an error.",
        "<code>get</code> returns <code>E</code>, which is String, so assigning it to a String needs no cast in your code.",
        "Erasure: the class file calls <code>add(Object)</code> and <code>get</code> returning Object, plus a <code>checkcast String</code> javac inserted. It can't fail, because only Strings could get in.",
        "At run time the list is a plain <code>ArrayList</code> with an <code>Object[]</code> inside. <code>ArrayList&lt;Integer&gt;</code> would be exactly the same class."])
ANIM = two_view("Generics: checked, then erased", S, B)
BLOCKS = {'ANIM': ANIM}

# ---------------- Part 6: animated example ----------------
ANIM2_HEADING = "Watch it with an example: one response class for a whole app"
ANIM2_INTRO = "A food-delivery backend sends every reply in a generic <code>ApiResponse&lt;T&gt;</code>. Watch the same class carry an order, a list of restaurants and an error."
A = Anim("One generic class, many payloads", frames=4, h=210, label="ApiResponse of T used with an Order, a list of restaurants and an error")
A.box(10, 12, 342, 40, None, fill="board", stroke="board")
A.text(20, 30, esc("class ApiResponse<T> {"), mono=True, size=10, cls="chalk")
A.text(20, 45, "  boolean ok;  T data;  String error; }", mono=True, size=10, cls="chalk")
A.box(10, 66, 160, 30, esc("ApiResponse<Order>"), fill="soft-acc", stroke="track", on="2", size=9.5, mono=True, bold=True)
A.box(10, 66, 160, 30, esc("ApiResponse<List<Shop>>"), fill="soft-acc", stroke="track", on="3", size=9, mono=True, bold=True)
A.box(10, 66, 160, 30, esc("ApiResponse<Order>"), fill="soft-acc", stroke="red", on="4", size=9.5, mono=True, bold=True)
A.text(90, 84, "T = ?", on="1", anchor="middle", mono=True, size=11, cls="ink3", bold=True)
A.box(190, 66, 162, 96, None, fill="card", stroke="line")
A.text(198, 84, "JSON sent to the app", size=9, bold=True, cls="ink2")
A.lines(198, 104, ['ok: true', 'data: {id: 9912,', '  total: 349}'], on="2", mono=True, size=9.2, gap=15)
A.lines(198, 104, ['ok: true', 'data: [Chai Point,', '  Dosa Hut]'], on="3", mono=True, size=9.2, gap=15)
A.lines(198, 104, ['ok: false', 'data: null', 'error: "Restaurant closed"'], on="4", mono=True, size=9, gap=15)
A.text(90, 130, "compiler-checked", on="2-", anchor="middle", size=9.5, cls="green", bold=True)
A.text(90, 146, "no casts in callers", on="2-", anchor="middle", size=9.5, cls="green", bold=True)
A.note({1: "One class, written once.", 2: "T = Order for the order screen.", 3: "T = a list of shops for the home screen.", 4: "Errors use the same shape."}, y=186, size=11)
A.caps(["The team writes one class with a type parameter <code>T</code> for the payload.",
        "The order endpoint returns <code>ApiResponse&lt;Order&gt;</code>: <code>data</code> is an Order, checked by javac.",
        "The home screen gets <code>ApiResponse&lt;List&lt;Shop&gt;&gt;</code>. Same class, different type argument.",
        "When something fails, <code>ok</code> is false and <code>error</code> explains why. Every endpoint answers in one predictable shape. (Simplified: real APIs also send status codes and request IDs.)"])
ANIM2 = A

# ---------------- Part 8: tracer ----------------
TRACE = dict(code='''class Box<T> {
    private T item;

    void put(T item) {
        this.item = item;
    }

    T get() {
        return item;
    }
}

public class Main {
    public static void main(String[] args) {
        Box<String> parcel = new Box<>();
        Box<Integer> locker = new Box<>();
        parcel.put("Laptop");
        locker.put(42);
        String what = parcel.get();
        int n = locker.get() + 1;
        System.out.println(what + " " + n + " " + (parcel.getClass() == locker.getClass()));
    }
}
''', notes={
 (15, 1): "Generic object :: A <code>Box&lt;String&gt;</code> is created. On the heap it's just a Box: the type argument isn't stored anywhere.",
 (15, 2): "Store :: ",
 (16, 1): "Generic object :: A <code>Box&lt;Integer&gt;</code>: the same class, Box.",
 (16, 2): "Store :: ",
 (17, 1): "Call :: javac already checked that \"Laptop\" is a String. Look at the frame name: <code>put(Object item)</code>. After erasure, T became Object.",
 (5, 1): "Store :: The field <code>item</code> is really of type Object after erasure; it now refers to the String.",
 (18, 1): "Call :: 42 is autoboxed to an Integer before the call (a cached object).",
 (19, 1): "Call :: ",
 (19, 2): "Cast :: = <code>get()</code> returned an Object; javac's inserted cast to String succeeded. <code>what</code> = → \"Laptop\".",
 (20, 2): "Cast + unbox :: = Cast to Integer, unboxed, plus 1: <code>n</code> = 43.",
 21: "Print :: <code>getClass()</code> is the same Box class for both: erasure."})

# ---------------- Worked examples ----------------
WORKED_INTRO = "Three reusable pieces of code made type-safe with generics: a bounded generic method, a wildcard method and a two-parameter generic class."
EXAMPLES = [
dict(tag="Sports · bounded generic method", title="Top score from any comparable list",
 problem="<p>Write one method that returns the largest element of a list, and use it for runs (Integers) and for player names (Strings, alphabetically last).</p>",
 inp="[34, 71, 12] and [\"Om\", \"Riya\", \"Kabir\"]",
 approach=["Declare <code>&lt;T extends Comparable&lt;T&gt;&gt; T best(List&lt;T&gt; xs)</code>: the bound allows <code>compareTo</code>.",
           "Loop and keep the larger element.",
           "Call it twice: javac infers T = Integer, then T = String."],
 code='''import java.util.List;

public class Main {
    static <T extends Comparable<T>> T best(List<T> xs) {
        T top = xs.get(0);
        for (T x : xs) {
            if (x.compareTo(top) > 0) {
                top = x;
            }
        }
        return top;
    }

    public static void main(String[] args) {
        Integer runs = best(List.of(34, 71, 12));
        String name = best(List.of("Om", "Riya", "Kabir"));
        System.out.println(runs + " " + name);
    }
}
''', tryit="Press <b>Run</b>. Then try <code>best(List.of(new Object()))</code> and read the compile error: Object isn't Comparable."),
dict(tag="Finance · wildcard", title="Total of mixed amount lists",
 problem="<p>Bills come as <code>List&lt;Integer&gt;</code> (whole rupees) and refunds as <code>List&lt;Double&gt;</code>. Write one method that totals either.</p>",
 inp="bills [499, 250], refunds [99.5]",
 approach=["Parameter type <code>List&lt;? extends Number&gt;</code>: a producer of Numbers.",
           "Read each element as a Number and add <code>doubleValue()</code>.",
           "Call it with both lists."],
 code='''import java.util.List;

public class Main {
    static double total(List<? extends Number> amounts) {
        double sum = 0;
        for (Number n : amounts) {
            sum += n.doubleValue();
        }
        return sum;
    }

    public static void main(String[] args) {
        List<Integer> bills = List.of(499, 250);
        List<Double> refunds = List.of(99.5);
        System.out.println("Bills " + total(bills) + ", refunds " + total(refunds));
    }
}
''', tryit="Press <b>Run</b>. Then change the parameter to <code>List&lt;Number&gt;</code> and read the error."),
dict(tag="Education · generic class", title="Pairs of student and grade",
 problem="<p>A results screen shows pairs like (Riya, A). Write a generic <code>Pair&lt;K, V&gt;</code> and use it for (String, Character) and (String, Integer).</p>",
 inp="(Riya, 'A'), (Kabir, 78)",
 approach=["<code>class Pair&lt;K, V&gt;</code> with two final fields and a <code>toString</code>.",
           "Create <code>Pair&lt;String, Character&gt;</code> and <code>Pair&lt;String, Integer&gt;</code>.",
           "Read <code>value</code> back without casts."],
 code='''class Pair<K, V> {
    final K key;
    final V value;

    Pair(K key, V value) {
        this.key = key;
        this.value = value;
    }

    @Override
    public String toString() {
        return key + "=" + value;
    }
}

public class Main {
    public static void main(String[] args) {
        Pair<String, Character> grade = new Pair<>("Riya", 'A');
        Pair<String, Integer> marks = new Pair<>("Kabir", 78);
        char g = grade.value;
        int m = marks.value + 2;
        System.out.println(grade + " " + marks + " " + g + " " + m);
    }
}
''', tryit="Press <b>Run</b>. Then add a generic method <code>static &lt;K, V&gt; Pair&lt;V, K&gt; swap(Pair&lt;K, V&gt; p)</code>."),
]

# ---------------- Practice problems ----------------
PRACTICE_INTRO = "Write and use generic classes and methods, and choose the right wildcard. The last three are business tasks."
PROBLEMS = [
dict(level="easy", title="A generic Box", stmt="<p>Write <code>Box&lt;T&gt;</code> with <code>put</code> and <code>get</code>. Store a <code>Double</code> price and print it with 18% GST added.</p>", inp="price 100.0",
 code='''class Box<T> {
    private T item;
    void put(T item) { this.item = item; }
    T get() { return item; }
}

public class Main {
    public static void main(String[] args) {
        Box<Double> price = new Box<>();
        price.put(100.0);
        System.out.println(price.get() * 1.18);
    }
}''', explain="<p><b>How it works:</b> <code>get()</code> returns a Double (no cast); it's unboxed for the multiplication.</p>"),
dict(level="easy", title="Generic method: first element", stmt="<p>Write <code>&lt;T&gt; T first(List&lt;T&gt; xs)</code> and use it on a list of names and a list of numbers.</p>", inp='["Riya", "Om"], [7, 3]',
 code='''import java.util.List;

public class Main {
    static <T> T first(List<T> xs) {
        return xs.get(0);
    }

    public static void main(String[] args) {
        String n = first(List.of("Riya", "Om"));
        Integer x = first(List.of(7, 3));
        System.out.println(n + " " + x);
    }
}''', explain="<p><b>How it works:</b> the method's own type parameter is inferred at each call: String, then Integer.</p>"),
dict(level="easy", title="Count elements of any list", stmt="<p>Write <code>static int count(List&lt;?&gt; xs)</code> that works for any list, and call it with a list of Strings and a list of Doubles.</p>", inp='["a", "b"], [1.5]',
 code='''import java.util.List;

public class Main {
    static int count(List<?> xs) {
        return xs.size();
    }

    public static void main(String[] args) {
        System.out.println(count(List.of("a", "b")) + " " + count(List.of(1.5)));
    }
}''', explain="<p><b>How it works:</b> the unbounded wildcard <code>?</code> accepts a list of any element type. We only call methods that don't depend on the type.</p>"),
dict(level="medium", title="Bounded average", stmt="<p>Write <code>&lt;T extends Number&gt; double avg(List&lt;T&gt; xs)</code> and test it with Integers and Doubles.</p>", inp="[80, 90, 70], [2.5, 3.5]",
 code='''import java.util.List;

public class Main {
    static <T extends Number> double avg(List<T> xs) {
        double s = 0;
        for (T x : xs) s += x.doubleValue();
        return s / xs.size();
    }

    public static void main(String[] args) {
        System.out.println(avg(List.of(80, 90, 70)) + " " + avg(List.of(2.5, 3.5)));
    }
}''', explain="<p><b>How it works:</b> the bound <code>T extends Number</code> lets us call <code>doubleValue()</code> on T.</p>"),
dict(level="medium", title="Fill a list with ? super", stmt="<p>Write <code>addRange(List&lt;? super Integer&gt; dest, int from, int to)</code> and use it to fill a <code>List&lt;Number&gt;</code> and a <code>List&lt;Object&gt;</code>.</p>", inp="1..3",
 code='''import java.util.ArrayList;
import java.util.List;

public class Main {
    static void addRange(List<? super Integer> dest, int from, int to) {
        for (int i = from; i <= to; i++) dest.add(i);
    }

    public static void main(String[] args) {
        List<Number> nums = new ArrayList<>();
        List<Object> objs = new ArrayList<>();
        addRange(nums, 1, 3);
        addRange(objs, 1, 3);
        System.out.println(nums + " " + objs);
    }
}''', explain="<p><b>How it works:</b> consumer super: any list whose element type is Integer or a supertype can safely receive Integers.</p>"),
dict(level="business", title="Generic paginated results", stmt="<p>An app shows 2 items per page. Write <code>&lt;T&gt; List&lt;T&gt; page(List&lt;T&gt; all, int pageNo, int size)</code> and print page 2 of five products.</p>", inp="[P1..P5], page 2, size 2",
 code='''import java.util.List;

public class Main {
    static <T> List<T> page(List<T> all, int pageNo, int size) {
        int from = (pageNo - 1) * size;
        int to = Math.min(from + size, all.size());
        return from >= all.size() ? List.of() : all.subList(from, to);
    }

    public static void main(String[] args) {
        List<String> products = List.of("P1", "P2", "P3", "P4", "P5");
        System.out.println(page(products, 2, 2));
        System.out.println(page(products, 3, 2));
    }
}''', explain="<p><b>How it works:</b> one generic method pages products, orders or users alike. <code>subList</code> returns a view of the range.</p>"),
dict(level="business", title="Typed cache with a size limit", stmt="<p>Write <code>Cache&lt;K, V&gt;</code> that keeps at most 2 entries, evicting the oldest. Store three exchange rates and print the cache.</p>", inp="USD 83.2, EUR 90.1, GBP 105.4",
 code='''import java.util.LinkedHashMap;
import java.util.Map;

class Cache<K, V> {
    private final int max;
    private final LinkedHashMap<K, V> map = new LinkedHashMap<>();

    Cache(int max) { this.max = max; }

    void put(K key, V value) {
        map.put(key, value);
        if (map.size() > max) {
            K oldest = map.keySet().iterator().next();
            map.remove(oldest);
        }
    }

    V get(K key) { return map.get(key); }

    @Override
    public String toString() { return map.toString(); }
}

public class Main {
    public static void main(String[] args) {
        Cache<String, Double> rates = new Cache<>(2);
        rates.put("USD", 83.2);
        rates.put("EUR", 90.1);
        rates.put("GBP", 105.4);
        System.out.println(rates + " USD=" + rates.get("USD"));
    }
}''', explain="<p><b>How it works:</b> K and V are fixed per cache instance; LinkedHashMap keeps insertion order so the first key is the oldest.</p>"),
dict(level="business", title="Validation result for any form", stmt="<p>Write <code>Validated&lt;T&gt;</code> holding either a value or an error. Validate an age (\"25\" → 25) and a bad age (\"abc\").</p>", inp='"25", "abc"',
 code='''class Validated<T> {
    final T value;
    final String error;

    private Validated(T value, String error) { this.value = value; this.error = error; }

    static <T> Validated<T> ok(T v) { return new Validated<>(v, null); }
    static <T> Validated<T> bad(String e) { return new Validated<>(null, e); }

    @Override
    public String toString() { return error == null ? "OK " + value : "ERROR " + error; }
}

public class Main {
    static Validated<Integer> age(String text) {
        try {
            int a = Integer.parseInt(text);
            return a > 0 && a < 120 ? Validated.ok(a) : Validated.bad("out of range");
        } catch (NumberFormatException e) {
            return Validated.bad("not a number: " + text);
        }
    }

    public static void main(String[] args) {
        System.out.println(age("25"));
        System.out.println(age("abc"));
    }
}''', explain="<p><b>How it works:</b> the generic result type works for ages, emails or dates, and callers get a typed value with no casts.</p>"),
]
