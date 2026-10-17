WORKED_INTRO = "Three programs that show Java's famous features at work: <b>robust</b> (errors are caught, not crashes), <b>strongly typed</b> (sizes of numbers are fixed on every machine) and <b>automatic memory management</b> (unused objects are cleaned up for you)."
EXAMPLES = [
dict(tag="Cinema · bookings", title="A wrong seat number doesn't crash the kiosk",
 problem="<p>A cinema kiosk stores the prices of 3 seat classes in an array. A customer asks for class number 5, which doesn't exist. The kiosk must show a friendly message instead of crashing. Java's exception handling makes this possible.</p>",
 inp="prices {150, 220, 350}; customer asks for class index 5",
 approach=["Store the prices in an array.",
           "Read the requested price inside <code>try</code>.",
           "If the index is outside the array, Java throws <code>ArrayIndexOutOfBoundsException</code>; <code>catch</code> it and print a message."],
 code='''public class Main {
    public static void main(String[] args) {
        int[] prices = {150, 220, 350};
        int wanted = 5;
        try {
            System.out.println("Price: Rs " + prices[wanted]);
        } catch (ArrayIndexOutOfBoundsException e) {
            System.out.println("Sorry, seat class " + wanted + " does not exist.");
        }
        System.out.println("Kiosk still running. Classes available: " + prices.length);
    }
}
''', notes={3: "Array :: = An array of 3 ints is created on the heap; <code>prices</code> points to it.",
            6: "Check :: = Java checks every array index at run time. Index 5 is outside 0–2, so an exception is thrown instead of reading random memory.",
            8: "Catch :: The catch block runs; the program does not crash.",
            10: "Carry on :: The kiosk keeps working. In C, a bad index could silently read garbage; Java's check is part of what makes it robust."},
 tryit="Press <b>Run</b>. Then set <code>wanted</code> to 2 and see the real price printed."),
dict(tag="Retail · revenue", title="Yearly revenue that's too big for an int",
 problem="<p>A retail chain earns about Rs 9,50,00,000 a day. Compute the yearly revenue. An <code>int</code> is exactly 32 bits on every computer (a Java feature), so its limit is the same everywhere: it overflows. Use <code>long</code>.</p>",
 inp="daily revenue 95000000, 365 days",
 approach=["Multiply with <code>int</code> and see the wrong (overflowed) answer.",
           "Multiply with <code>long</code> (64 bits) for the right answer.",
           "Print <code>Integer.MAX_VALUE</code> to see the limit."],
 code='''public class Main {
    public static void main(String[] args) {
        int daily = 95000000;
        int wrongYearly = daily * 365;
        long rightYearly = (long) daily * 365;
        System.out.println("int result:  " + wrongYearly);
        System.out.println("long result: " + rightYearly);
        System.out.println("int limit:   " + Integer.MAX_VALUE);
    }
}
''', notes={4: "Overflow :: = The true answer (34,67,50,00,000) is bigger than an int can hold, so it wraps around to a wrong number.",
            5: "long :: = Converting to long first makes Java multiply with 64 bits: correct.",
            8: "Limit :: An int's maximum is 2,147,483,647 on every machine, because Java fixes the size of each type."},
 tryit="Press <b>Run</b>. Then change <code>daily</code> to 5000000 and check whether the int result is right now."),
dict(tag="Memory · garbage collection", title="Old messages are cleaned up automatically",
 problem="<p>A notice board app keeps one current message in a variable. Each time the message changes, the old String is no longer used. Java's garbage collector frees such objects automatically; you never call free() or delete.</p>",
 inp="three notices in a row",
 approach=["Assign a first notice to <code>notice</code>.",
           "Assign a new String twice; the older objects lose their reference.",
           "Watch the heap: unreachable objects are eligible for garbage collection."],
 code='''public class Main {
    public static void main(String[] args) {
        String notice = "Canteen opens at 8";
        System.out.println(notice);
        notice = "Canteen opens at 9 today";
        System.out.println(notice);
        notice = null;
        System.out.println("No notice. Is it null? " + (notice == null));
    }
}
''', notes={3: "First object :: = <code>notice</code> points to a String object on the heap.",
            5: "New object :: = <code>notice</code> now points to a new String. The first one has no reference left: the garbage collector may free it whenever it runs.",
            7: "null :: = <code>notice</code> points to nothing. The second String is unreachable too.",
            8: "Check :: <code>== null</code> tests whether a reference points to nothing."},
 tryit="Press <b>Run</b>. Then add another notice after the null line."),
]

PRACTICE_INTRO = "Small programs that touch Java's features: safe error handling, fixed-size types and strings. Every output is fixed. The last three are business tasks."
PROBLEMS = [
dict(level="easy", title="Java's age", stmt="<p>Java was released in 1995. Print how old Java is in 2026.</p>", inp="1995, 2026",
 code='''public class Main {
    public static void main(String[] args) {
        int born = 1995;
        int now = 2026;
        System.out.println("Java is " + (now - born) + " years old");
    }
}''', explain="<p><b>How it works:</b> brackets make the subtraction happen before joining with text.</p>"),
dict(level="easy", title="Limits of int and long", stmt="<p>Print the largest values an <code>int</code> and a <code>long</code> can hold.</p>", inp="(none)",
 code='''public class Main {
    public static void main(String[] args) {
        System.out.println("int max:  " + Integer.MAX_VALUE);
        System.out.println("long max: " + Long.MAX_VALUE);
    }
}''', explain="<p><b>How it works:</b> these limits are the same on every computer, which is part of Java's portability.</p>"),
dict(level="easy", title="Catch a division by zero", stmt="<p>Divide 100 by 0 inside try/catch and print a friendly message.</p>", inp="100 / 0",
 code='''public class Main {
    public static void main(String[] args) {
        try {
            System.out.println(100 / 0);
        } catch (ArithmeticException e) {
            System.out.println("Cannot divide by zero");
        }
    }
}''', explain="<p><b>How it works:</b> Java turns the error into an exception object you can catch, instead of crashing the whole program.</p>"),
dict(level="medium", title="Overflow you can see", stmt="<p>Add 1 to <code>Integer.MAX_VALUE</code> and print the result.</p>", inp="2147483647 + 1",
 code='''public class Main {
    public static void main(String[] args) {
        int big = Integer.MAX_VALUE;
        big = big + 1;
        System.out.println(big);
    }
}''', explain="<p><b>How it works:</b> an int wraps around to its minimum value. Use long when values can get this large.</p>"),
dict(level="medium", title="Length of a message", stmt="<p>Print the number of characters in \"Write once, run anywhere\".</p>", inp="the slogan",
 code='''public class Main {
    public static void main(String[] args) {
        String slogan = "Write once, run anywhere";
        System.out.println(slogan.length());
    }
}''', explain="<p><b>How it works:</b> spaces and commas count as characters.</p>"),
dict(level="business", title="Safe price lookup", stmt="<p>Prices of 4 products are in an array. Look up product 2, then product 9 safely.</p>", inp="{99, 149, 249, 399}; indexes 2 and 9",
 code='''public class Main {
    public static void main(String[] args) {
        int[] prices = {99, 149, 249, 399};
        try {
            System.out.println("Product 2: Rs " + prices[2]);
            System.out.println("Product 9: Rs " + prices[9]);
        } catch (ArrayIndexOutOfBoundsException e) {
            System.out.println("Product not found");
        }
    }
}''', explain="<p><b>How it works:</b> the first line prints; the second throws, so the rest of the try is skipped and the catch runs.</p>"),
dict(level="business", title="Population in long", stmt="<p>India's population is about 1,45,00,00,000. Store it and print it divided across 28 states (whole number).</p>", inp="1450000000, 28",
 code='''public class Main {
    public static void main(String[] args) {
        long population = 1450000000L;
        System.out.println("Average per state: " + population / 28);
    }
}''', explain="<p><b>How it works:</b> 1,450,000,000 fits in an int, but just barely; using long with the <code>L</code> suffix leaves room for growth. (Approximate figure.)</p>"),
dict(level="business", title="Monthly salary bill", stmt="<p>A company has 1,200 employees with an average salary of Rs 45,000. Print the monthly and yearly salary bill using long.</p>", inp="1200, 45000",
 code='''public class Main {
    public static void main(String[] args) {
        long monthly = 1200L * 45000;
        long yearly = monthly * 12;
        System.out.println("Monthly: Rs " + monthly);
        System.out.println("Yearly:  Rs " + yearly);
    }
}''', explain="<p><b>How it works:</b> the yearly total, 64,80,00,000, still fits in an int, but bigger companies would overflow. Payroll code always uses long (or BigDecimal) for money totals.</p>"),
]
