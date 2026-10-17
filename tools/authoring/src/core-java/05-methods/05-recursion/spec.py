import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../..'))
from mkanim import Anim

ANIM2_HEADING = "Watch it with an example: adding up a folder tree"
ANIM2_INTRO = "The run-the-code program below, as a picture. <code>size()</code> visits each folder, asks each sub-folder the same question, and adds up the answers on the way back."
A = Anim("size(Projects) = 40 + size(Java) + size(Python)", frames=7, h=236, label="recursive folder size")
nodes = {"Projects": (130, 16, "40"), "Java": (40, 92, "10"), "Python": (230, 92, "25"), "Week1": (40, 168, "3")}
for n, (x, y, kb) in nodes.items():
    A.box(x, y, 100, 40, n, sub=f"own files {kb} KB", fill="soft-blue", stroke="blue", bold=True, size=10.5)
A.arrow(160, 56, 100, 90, color="ink", sw=1.5); A.arrow(210, 56, 270, 90, color="ink", sw=1.5); A.arrow(90, 132, 90, 166, color="ink", sw=1.5)
hl = {1: "Projects", 2: "Java", 3: "Week1", 4: "Java", 5: "Python", 6: "Projects", 7: "Projects"}
for f, n in hl.items():
    x, y, _ = nodes[n]
    A.box(x - 3, y - 3, 106, 46, None, fill="none", stroke="track", sw=3, on=str(f))
res = {"Week1": ("3", "3-"), "Java": ("13", "4-"), "Python": ("25", "5-"), "Projects": ("78", "6-")}
for n, (v, on) in res.items():
    x, y, _ = nodes[n]
    A.box(x + 70, y - 10, 44, 20, v + " KB", fill="soft-green", stroke="green", size=9.5, bold=True, on=on, rx=10)
A.box(190, 160, 164, 70, None, fill="board", stroke="board")
A.text(198, 176, "call stack (top first)", size=9, cls="chalk", bold=True)
stk = {1: ["size(Projects)"], 2: ["size(Java)", "size(Projects)"], 3: ["size(Week1)", "size(Java)", "size(Projects)"],
       4: ["size(Java)", "size(Projects)"], 5: ["size(Python)", "size(Projects)"], 6: ["size(Projects)"], 7: ["(empty) → 78 KB"]}
for f, rows in stk.items():
    for i, r in enumerate(rows):
        A.text(198, 193 + i * 13, r, on=str(f), mono=True, size=9.5, cls="kw" if i == 0 else "chalk")
A.caps([
 "<b>Start:</b> <code>size(Projects)</code> begins with its own 40 KB, then loops over its children.",
 "<b>First child:</b> it calls <code>size(Java)</code> and waits. Java starts with its own 10 KB.",
 "<b>Deeper:</b> Java calls <code>size(Week1)</code>. Week1 has no sub-folders, so the loop doesn't run: base case, it returns 3.",
 "<b>Back up:</b> Java adds 10 + 3 = 13 and returns. Its frame is popped.",
 "<b>Second child:</b> Projects now calls <code>size(Python)</code>: no children, returns 25.",
 "<b>Combine:</b> Projects adds 40 + 13 + 25 = 78.",
 "<b>Done:</b> the stack is empty again and the answer is 78 KB. Add a folder at any depth and the same 10-line method still works.",
])
ANIM2 = A

TRACE = dict(code='''public class Main {
    static long power(int base, int exp) {
        if (exp == 0) {
            return 1;
        }
        long smaller = power(base, exp - 1);
        return base * smaller;
    }

    public static void main(String[] args) {
        long result = power(2, 3);
        System.out.println("2^3 = " + result);
    }
}
''', notes={
 (11, 1): "Call :: main calls <code>power(2, 3)</code>.",
 (3, 1): "Check :: exp is 3, not 0: not the base case.",
 (6, 1): "Recurse :: To know 2³ we first need 2². A second <code>power</code> frame is pushed with its own <code>exp</code>.",
 (3, 2): "Check :: exp = 2: still not 0.",
 (6, 2): "Recurse :: A third frame, for 2¹.",
 (3, 3): "Check :: exp = 1.",
 (6, 3): "Recurse :: A fourth frame, for 2⁰. Four power frames are on the stack now: the deepest point.",
 (3, 4): "Base case :: exp is 0!",
 4: "Base case :: Return 1 without any further call. The recursion turns around here.",
 (6, 4): "Unwind :: The frame for exp = 1 receives 1 in <code>smaller</code>.",
 (7, 1): "Unwind :: 2 × 1 = 2 is returned.",
 (6, 5): "Unwind :: The exp = 2 frame receives 2.",
 (7, 2): "Unwind :: 2 × 2 = 4 is returned.",
 (6, 6): "Unwind :: The exp = 3 frame receives 4.",
 (7, 3): "Unwind :: 2 × 4 = 8 is returned to main.",
 (11, 2): "Result :: ",
 12: "Print :: ",
}, end='main returns. At most four power frames existed at the same time, one per exponent value 3, 2, 1, 0.')

WORKED_INTRO = "Three problems where each step is a smaller copy of the whole problem. Step through each one and watch the frames of the same method pile up and unwind."
EXAMPLES = [
dict(tag="Banking · checksums", title="Digit sum of an account number",
 problem="<p>A simple check used by some ID schemes adds up all digits of a number. Write a recursive <code>digitSum(long n)</code>: the last digit (<code>n % 10</code>) plus the digit sum of the rest (<code>n / 10</code>). Print it for 4721.</p>",
 inp="n = 4721", approach=["Base case: <code>n == 0</code> → 0.", "Recursive case: <code>n % 10 + digitSum(n / 10)</code>.", "Each call removes one digit, so the depth equals the number of digits."],
 code='''public class Main {
    static long digitSum(long n) {
        if (n == 0) {
            return 0;
        }
        long rest = digitSum(n / 10);
        return n % 10 + rest;
    }

    public static void main(String[] args) {
        long s = digitSum(4721);
        System.out.println("Digit sum of 4721 = " + s);
    }
}
''', notes={
 (6, 1): "Recurse :: 4721 → drop the last digit → 472.",
 (6, 2): "Recurse :: 472 → 47.",
 (6, 3): "Recurse :: 47 → 4.",
 (6, 4): "Recurse :: 4 → 0.",
 4: "Base case :: n is 0: nothing left to add.",
 (6, 5): "Unwind :: ",
 (7, 1): "Unwind :: Adds 4 (the digit this frame removed).",
 (6, 6): "Unwind :: ", (7, 2): "Unwind :: Adds 7.",
 (6, 7): "Unwind :: ", (7, 3): "Unwind :: Adds 2.",
 (6, 8): "Unwind :: ", (7, 4): "Unwind :: Adds 1: total 14.",
 12: "Print :: "},
 tryit="Press <b>Run</b>. Then try your phone number (add <code>L</code> after it, it's a long)."),
dict(tag="Retail · price search", title="Binary search in sorted prices",
 problem="<p>A shopping app keeps product prices sorted: 99, 149, 249, 399, 599, 799, 999. Find the position of 599 with a recursive binary search that looks at the middle and throws away half each time.</p>",
 inp="prices = {99, 149, 249, 399, 599, 799, 999}, target = 599",
 approach=["Look at the middle index <code>(lo + hi) / 2</code>.", "If it's the target, return the index; if the target is bigger, search the right half, else the left half.", "Base case: <code>lo &gt; hi</code> means not found (−1)."],
 code='''public class Main {
    static int find(int[] a, int target, int lo, int hi) {
        if (lo > hi) {
            return -1;
        }
        int mid = (lo + hi) / 2;
        if (a[mid] == target) {
            return mid;
        }
        if (a[mid] < target) {
            return find(a, target, mid + 1, hi);
        }
        return find(a, target, lo, mid - 1);
    }

    public static void main(String[] args) {
        int[] prices = {99, 149, 249, 399, 599, 799, 999};
        int pos = find(prices, 599, 0, prices.length - 1);
        System.out.println("599 found at index " + pos);
    }
}
''', notes={
 17: "Data :: A sorted array: the key requirement for binary search.",
 (18, 1): "Call :: Search the whole array, indexes 0 to 6.",
 (6, 1): "Middle :: (0 + 6) / 2 = 3. prices[3] is 399.",
 (10, 1): "Compare :: 399 &lt; 599, so 599 must be in the right half.",
 (11, 1): "Recurse :: Search indexes 4 to 6 only. Half the array is ignored.",
 (6, 2): "Middle :: (4 + 6) / 2 = 5. prices[5] is 799.",
 (10, 2): "Compare :: 799 is bigger than 599.",
 13: "Recurse :: Search the left half: indexes 4 to 4.",
 (6, 3): "Middle :: (4 + 4) / 2 = 4. prices[4] is 599!",
 8: "Found :: Base case: return the index 4.",
 (13, 2): "Unwind :: The answer passes back unchanged.",
 (11, 2): "Unwind :: ",
 (18, 2): "Result :: ",
 19: "Print :: "},
 tryit="Press <b>Run</b>. Then search for 300 (not in the list): which base case ends it?"),
dict(tag="HR · org chart", title="Count everyone under a manager",
 problem="<p>An org chart: the CEO (0) manages 1 and 2; 1 manages 3 and 4; 4 manages 5. Write <code>teamSize(person)</code> that returns how many people report to that person, directly or indirectly.</p>",
 inp="reports = {{1, 2}, {3, 4}, {}, {}, {5}, {}}, person = 1",
 approach=["Each direct report counts as 1, plus everyone under them.", "<code>teamSize(p) = sum over each report r of (1 + teamSize(r))</code>.", "Base case: someone with no reports returns 0 (the loop doesn't run)."],
 code='''public class Main {
    static int[][] reports = {{1, 2}, {3, 4}, {}, {}, {5}, {}};

    static int teamSize(int person) {
        int count = 0;
        for (int r : reports[person]) {
            count += 1 + teamSize(r);
        }
        return count;
    }

    public static void main(String[] args) {
        int n = teamSize(1);
        System.out.println("Person 1 leads " + n + " people");
    }
}
''', notes={
 (13, 1): "Call :: How many people are under person 1?",
 (7, 1): "Recurse :: First report of person 1 is person 3: count them and everyone under them.",
 (9, 1): "Base case :: Person 3 has nobody under them: returns 0.",
 (7, 2): "Unwind :: Back in person 1's frame: 1 (person 3) + 0.",
 (7, 3): "Recurse :: Next report: person 4.",
 (7, 4): "Recurse :: Person 4 manages person 5: one level deeper.",
 (9, 2): "Base case :: Person 5 has no reports.",
 (7, 5): "Unwind :: Person 4's count: 1 + 0 = 1.",
 (9, 3): "Unwind :: Person 4 returns 1.",
 (7, 6): "Unwind :: Person 1 adds 1 (person 4) + 1 (person 5).",
 (9, 4): "Unwind :: Person 1's total: 3 people.",
 (13, 2): "Result :: ",
 14: "Print :: "},
 tryit="Press <b>Run</b>. Then change it to <code>teamSize(0)</code> for the CEO. Predict the answer first."),
]

PRACTICE_INTRO = "Practise finding the base case and the smaller problem. Check each answer by tracing a small input by hand before you run it. The last three are business problems."
PROBLEMS = [
dict(level="easy", title="Sum from 1 to n", stmt="<p>Write a recursive <code>sumTo(int n)</code> that returns 1 + 2 + … + n. Print it for n = 10.</p>", inp="n = 10",
 code='''public class Main {
    static int sumTo(int n) {
        if (n == 0) return 0;
        return n + sumTo(n - 1);
    }

    public static void main(String[] args) {
        System.out.println(sumTo(10));
    }
}''', explain="<p><b>How it works:</b> base case n = 0 gives 0; otherwise n plus the sum of the smaller range. Depth is n + 1 frames.</p>"),
dict(level="easy", title="Reverse a word", stmt="<p>Write a recursive <code>reverse(String s)</code>: the last character followed by the reverse of the rest.</p>", inp="\"JAVA\", \"chai\"",
 code='''public class Main {
    static String reverse(String s) {
        if (s.length() <= 1) return s;
        return s.charAt(s.length() - 1) + reverse(s.substring(0, s.length() - 1));
    }

    public static void main(String[] args) {
        System.out.println(reverse("JAVA"));
        System.out.println(reverse("chai"));
    }
}''', explain="<p><b>How it works:</b> a string of length 0 or 1 is its own reverse (base case). Each call removes one character, so the input gets smaller every time. (For real code, <code>new StringBuilder(s).reverse()</code> is simpler.)</p>"),
dict(level="easy", title="Count down and up", stmt="<p>Write <code>countDownUp(int n)</code> that prints n down to 1 and then 1 back up to n, using one recursive call and two print statements.</p>", inp="n = 3",
 code='''public class Main {
    static void countDownUp(int n) {
        if (n == 0) return;
        System.out.print(n + " ");
        countDownUp(n - 1);
        System.out.print(n + " ");
    }

    public static void main(String[] args) {
        countDownUp(3);
        System.out.println();
    }
}''', explain="<p><b>How it works:</b> the first print runs on the way <b>down</b>; the second waits in each frame and runs on the way <b>back up</b>, in reverse order. This is the clearest demonstration of the call stack.</p>"),
dict(level="medium", title="Power in fewer steps", stmt="<p>Compute base<sup>exp</sup> with “fast power”: if exp is even, power(b, e) = half × half where half = power(b, e/2); if odd, multiply by b once more. Count the calls for 2<sup>30</sup>.</p>", inp="power(2, 10), power(3, 5), power(2, 30)",
 code='''public class Main {
    static int calls = 0;

    static long power(long base, int exp) {
        calls++;
        if (exp == 0) return 1;
        long half = power(base, exp / 2);
        if (exp % 2 == 0) return half * half;
        return half * half * base;
    }

    public static void main(String[] args) {
        System.out.println(power(2, 10));
        System.out.println(power(3, 5));
        calls = 0;
        System.out.println(power(2, 30) + " in " + calls + " calls");
    }
}''', explain="<p><b>How it works:</b> halving the exponent each time means only about log₂(exp) + 1 calls: 6 calls for 2³⁰ instead of 31. This divide-and-conquer idea is used in cryptography for huge powers.</p>"),
dict(level="medium", title="Palindrome check", stmt="<p>Write a recursive <code>isPal(String s, int i, int j)</code> that compares the outer characters and moves inwards.</p>", inp="\"MALAYALAM\", \"KERALA\"",
 code='''public class Main {
    static boolean isPal(String s, int i, int j) {
        if (i >= j) return true;
        if (s.charAt(i) != s.charAt(j)) return false;
        return isPal(s, i + 1, j - 1);
    }

    public static void main(String[] args) {
        System.out.println(isPal("MALAYALAM", 0, 8));
        System.out.println(isPal("KERALA", 0, 5));
    }
}''', explain="<p><b>How it works:</b> two base cases: the indexes meet (everything matched → true), or a mismatch is found (→ false, and no further calls are made).</p>"),
dict(level="medium", title="Fibonacci: slow vs remembered", stmt="<p>Compute fib(35) with the naive recursion and with a memo array, and count the calls each one makes.</p>", inp="n = 35",
 code='''public class Main {
    static long naiveCalls = 0, memoCalls = 0;
    static long[] memo = new long[100];

    static long fib(int n) {
        naiveCalls++;
        if (n < 2) return n;
        return fib(n - 1) + fib(n - 2);
    }

    static long fibMemo(int n) {
        memoCalls++;
        if (n < 2) return n;
        if (memo[n] != 0) return memo[n];
        memo[n] = fibMemo(n - 1) + fibMemo(n - 2);
        return memo[n];
    }

    public static void main(String[] args) {
        System.out.println("naive: " + fib(35) + " in " + naiveCalls + " calls");
        System.out.println("memo:  " + fibMemo(35) + " in " + memoCalls + " calls");
    }
}''', explain="<p><b>How it works:</b> the naive version recomputes the same values again and again: almost 3 crore calls. Storing each answer the first time cuts it to 69 calls. This idea (memoization) is the start of dynamic programming.</p>"),
dict(level="business", title="Total value of a nested cart", stmt="<p>A combo pack can contain items and other combo packs. Using arrays, <code>price[i]</code> is the item's own price and <code>contains[i]</code> lists the packs inside it. Find the full price of pack 0.</p>", inp="Festival box (0) = Rs 50 + snacks pack (1) + sweets pack (2); snacks = Rs 120 + chips (3); sweets = Rs 300; chips = Rs 40",
 code='''public class Main {
    static String[] name = {"Festival box", "Snacks pack", "Sweets pack", "Chips"};
    static int[] price = {50, 120, 300, 40};
    static int[][] contains = {{1, 2}, {3}, {}, {}};

    static int fullPrice(int i) {
        int total = price[i];
        for (int inner : contains[i]) {
            total += fullPrice(inner);
        }
        return total;
    }

    public static void main(String[] args) {
        for (int i = 0; i < name.length; i++) {
            System.out.println(name[i] + ": Rs " + fullPrice(i));
        }
    }
}''', explain="<p><b>How it works:</b> exactly the folder-size pattern. Any “thing made of smaller things of the same kind” (bill of materials, combo offers, nested menus) is a natural fit for recursion.</p>"),
dict(level="business", title="EMI-free savings goal: months needed", stmt="<p>Riya saves Rs 3,000 a month and her savings earn 1% per month. Write a recursive <code>months(double saved, double goal)</code> that returns how many months until she reaches Rs 20,000.</p>", inp="start Rs 0, monthly Rs 3000, 1% per month, goal Rs 20000",
 code='''public class Main {
    static int months(double saved, double goal) {
        if (saved >= goal) return 0;
        double next = saved * 1.01 + 3000;
        return 1 + months(next, goal);
    }

    public static void main(String[] args) {
        System.out.println("Months to Rs 20000: " + months(0, 20000));
    }
}''', explain="<p><b>How it works:</b> base case: the goal is reached, 0 more months needed. Otherwise one month passes (interest, then the new deposit) and we ask the same question with the new balance. Because the depth is only a few months, recursion is safe here; for a 30-year plan, a loop would be the safer choice.</p>"),
]
