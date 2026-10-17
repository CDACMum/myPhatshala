WORKED_INTRO = "Choosing the right primitive type is a real design decision: too small and numbers overflow, decimals in <code>double</code> aren't exact, and <code>char</code> is secretly a number. Each program below shows one of these in action."
EXAMPLES = [
dict(tag="E-commerce · product", title="Pick a type for every field of a product",
 problem="<p>An online store keeps, for each product: number in stock, total units ever sold, price, rating, size letter and whether it's in stock. Pick the most suitable primitive type for each and print a product summary.</p>",
 inp="stock 42, sold 3,200,000,000 (all time), price 1499.00, rating 4.3, size 'M', in stock",
 approach=["<code>int</code> for small counts; <code>long</code> for counts beyond 2.1 billion.",
           "<code>double</code> for price and rating (decimals).",
           "<code>char</code> for one letter, <code>boolean</code> for yes/no."],
 code='''public class Main {
    public static void main(String[] args) {
        int stock = 42;
        long totalSold = 3_200_000_000L;
        double price = 1499.00;
        float rating = 4.3f;
        char size = 'M';
        boolean available = stock > 0;
        System.out.println("Stock " + stock + ", sold " + totalSold);
        System.out.println("Price " + price + ", rating " + rating + ", size " + size + ", available " + available);
    }
}
''', notes={4: "long :: = 3.2 billion is above the int limit (about 2.1 billion), so it needs <code>long</code> and the <code>L</code> suffix. Underscores just make the number readable.",
            6: "float :: = A float needs the <code>f</code> suffix; plain 4.3 is a double.",
            8: "boolean :: = <code>stock &gt; 0</code> is a comparison, and its true/false result goes into a boolean."},
 tryit="Press <b>Run</b>. Then remove the <code>L</code> after 3_200_000_000 and read the compile error."),
dict(tag="Banking · interest", title="Why money shouldn't be stored in double",
 problem="<p>A banking app adds 10 paise (0.10) to a balance three times and expects 0.30. With <code>double</code> it gets something slightly different, because binary fractions can't hold 0.1 exactly. Show the problem and the usual fix: count in paise with <code>long</code>.</p>",
 inp="0.10 added three times",
 approach=["Add 0.10 to a double three times and print it.",
           "Do the same in paise with a long.",
           "Compare both to the expected value."],
 code='''public class Main {
    public static void main(String[] args) {
        double rupees = 0.0;
        rupees = rupees + 0.10;
        rupees = rupees + 0.10;
        rupees = rupees + 0.10;
        long paise = 0;
        paise = paise + 10;
        paise = paise + 10;
        paise = paise + 10;
        System.out.println("double: " + rupees + " (equals 0.3? " + (rupees == 0.3) + ")");
        System.out.println("paise:  " + paise + " = Rs 0." + paise);
    }
}
''', notes={6: "Tiny error :: = 0.1 has no exact binary form, so the sum becomes 0.30000000000000004.",
            10: "Exact :: = Whole numbers of paise are exact.",
            11: "Compare :: = <code>rupees == 0.3</code> is false. That's why banks count money in the smallest unit or use BigDecimal."},
 tryit="Press <b>Run</b>. Then try adding 0.25 three times: 0.25 is exact in binary, so this one works."),
dict(tag="Ticketing · seats", title="char is a number: the next seat letter",
 problem="<p>A theatre names rows A, B, C… A customer is in row 'C' and wants the row 2 behind. Since <code>char</code> stores a character code, you can add to it. Print the code and the new row.</p>",
 inp="row 'C', move 2 rows back",
 approach=["Store the row as a <code>char</code>.",
           "Its numeric code: <code>(int) row</code>.",
           "Add 2 and cast back to <code>char</code>."],
 code='''public class Main {
    public static void main(String[] args) {
        char row = 'C';
        int code = row;
        char newRow = (char) (row + 2);
        System.out.println("Row " + row + " has code " + code);
        System.out.println("Two rows back: " + newRow);
    }
}
''', notes={4: "Widening :: = A char fits into an int automatically: 'C' is 67.",
            5: "Back to char :: = 67 + 2 = 69, and casting 69 to char gives 'E'."},
 tryit="Press <b>Run</b>. Then start from 'Y' and add 2. What comes after 'Z'?"),
]

PRACTICE_INTRO = "Pick the right primitive type, and see each type's limits and quirks. Every output is fixed. The last three are business tasks."
PROBLEMS = [
dict(level="easy", title="All eight types", stmt="<p>Declare one variable of each primitive type and print them on one line.</p>", inp="(none)",
 code='''public class Main {
    public static void main(String[] args) {
        byte b = 10; short s = 300; int i = 70000; long l = 9000000000L;
        float f = 2.5f; double d = 3.14159; char c = 'J'; boolean ok = true;
        System.out.println(b + " " + s + " " + i + " " + l + " " + f + " " + d + " " + c + " " + ok);
    }
}''', explain="<p><b>How it works:</b> byte, short, int, long hold whole numbers of increasing size; float and double hold decimals; char one character; boolean true/false.</p>"),
dict(level="easy", title="Type limits", stmt="<p>Print the smallest and largest <code>byte</code>.</p>", inp="(none)",
 code='''public class Main {
    public static void main(String[] args) {
        System.out.println(Byte.MIN_VALUE + " to " + Byte.MAX_VALUE);
    }
}''', explain="<p><b>How it works:</b> a byte is 8 bits, so it holds −128 to 127.</p>"),
dict(level="easy", title="Character code", stmt="<p>Print the numeric code of 'A' and of 'a'.</p>", inp="'A', 'a'",
 code='''public class Main {
    public static void main(String[] args) {
        System.out.println((int) 'A' + " " + (int) 'a');
    }
}''', explain="<p><b>How it works:</b> lowercase letters come 32 codes after uppercase ones.</p>"),
dict(level="medium", title="Integer division vs double division", stmt="<p>Print 7 / 2 and 7 / 2.0.</p>", inp="7, 2",
 code='''public class Main {
    public static void main(String[] args) {
        System.out.println(7 / 2);
        System.out.println(7 / 2.0);
    }
}''', explain="<p><b>How it works:</b> if both operands are ints, the result is an int (the fraction is dropped).</p>"),
dict(level="medium", title="byte overflow", stmt="<p>Store 127 in a byte, add 1 with <code>++</code>, and print it.</p>", inp="127",
 code='''public class Main {
    public static void main(String[] args) {
        byte level = 127;
        level++;
        System.out.println(level);
    }
}''', explain="<p><b>How it works:</b> the value wraps around from 127 to −128.</p>"),
dict(level="business", title="Price in paise", stmt="<p>Store a price of Rs 249.50 as paise in a long and print it back in rupees and paise.</p>", inp="249.50",
 code='''public class Main {
    public static void main(String[] args) {
        long paise = 24950;
        System.out.println("Rs " + paise / 100 + "." + paise % 100);
    }
}''', explain="<p><b>How it works:</b> money in the smallest unit is exact; divide and take the remainder to display it.</p>"),
dict(level="business", title="In-stock flag", stmt="<p>A product has 0 units. Store <code>inStock</code> as a boolean and print it, then print it for 15 units.</p>", inp="0, 15",
 code='''public class Main {
    public static void main(String[] args) {
        int units = 0;
        boolean inStock = units > 0;
        System.out.println("In stock: " + inStock);
        units = 15;
        inStock = units > 0;
        System.out.println("In stock: " + inStock);
    }
}''', explain="<p><b>How it works:</b> a comparison produces a boolean you can store and print.</p>"),
dict(level="business", title="Daily visitors over a year", stmt="<p>A website gets 80 lakh visits a day. Print the yearly total using long.</p>", inp="8000000 × 365",
 code='''public class Main {
    public static void main(String[] args) {
        long daily = 8_000_000;
        System.out.println("Yearly visits: " + daily * 365);
    }
}''', explain="<p><b>How it works:</b> 2,920,000,000 is larger than an int can hold; long has room.</p>"),
]
