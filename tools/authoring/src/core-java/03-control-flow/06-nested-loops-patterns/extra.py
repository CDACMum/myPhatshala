WORKED_INTRO = "A loop inside a loop handles anything with rows and columns: seating charts, tables, calendars and printed patterns. In the traces, notice that the inner loop runs completely for every single pass of the outer loop."
EXAMPLES = [
dict(tag="Events · seating", title="Print a seating chart",
 problem="<p>A seminar hall has 3 rows (A–C) of 4 seats. Print the chart with seat labels like A1 A2 …, one row per line.</p>",
 inp="3 rows, 4 seats",
 approach=["Outer loop over rows, inner loop over seats.",
           "Row letter: <code>(char) ('A' + r)</code>.",
           "<code>print</code> inside, <code>println</code> after each row."],
 code='''public class Main {
    public static void main(String[] args) {
        int rows = 3, seats = 4;
        for (int r = 0; r < rows; r++) {
            for (int s = 1; s <= seats; s++) {
                System.out.print((char) ('A' + r) + "" + s + " ");
            }
            System.out.println();
        }
    }
}
''', notes={(5, 1): "Inner loop starts :: = For row A, s goes 1, 2, 3, 4.",
            (8, 1): "Row done :: = After 4 seats the inner loop ends; println moves to the next line.",
            (4, 2): "Next row :: = r becomes 1 (row B) and the inner loop starts again from s = 1."},
 tryit="Press <b>Run</b>. Then make it 5 rows of 6 seats."),
dict(tag="Retail · weekly report", title="Weekly sales per store",
 problem="<p>Two stores record sales for 3 days in a 2D array. Print each store's total and the overall total.</p>",
 inp="Pune {1200, 950, 1800}; Nashik {700, 1100, 640}",
 approach=["Outer loop over stores, inner loop over days.",
           "Reset <code>storeTotal</code> for each store.",
           "Add each store's total into the grand total."],
 code='''public class Main {
    public static void main(String[] args) {
        String[] stores = {"Pune", "Nashik"};
        int[][] sales = {{1200, 950, 1800}, {700, 1100, 640}};
        int grand = 0;
        for (int st = 0; st < sales.length; st++) {
            int storeTotal = 0;
            for (int d = 0; d < sales[st].length; d++) {
                storeTotal += sales[st][d];
            }
            System.out.println(stores[st] + ": Rs " + storeTotal);
            grand += storeTotal;
        }
        System.out.println("All stores: Rs " + grand);
    }
}
''', notes={(7, 1): "Reset :: = A fresh <code>storeTotal</code> for Pune.",
            (11, 1): "Store done :: = Pune's three days added: 3950.",
            (7, 2): "Reset again :: = The variable is created anew for Nashik, starting at 0."},
 tryit="Press <b>Run</b>. Then add a third store row."),
dict(tag="Printing · patterns", title="A right-angled number triangle",
 problem="<p>A token display board shows a staircase of numbers. Print 4 rows where row <i>i</i> has the numbers 1 to <i>i</i>. The inner loop's limit depends on the outer loop variable.</p>",
 inp="4 rows",
 approach=["Outer loop <code>i</code> from 1 to 4.",
           "Inner loop <code>j</code> from 1 to <code>i</code>.",
           "So row 1 prints once, row 4 prints four times."],
 code='''public class Main {
    public static void main(String[] args) {
        for (int i = 1; i <= 4; i++) {
            for (int j = 1; j <= i; j++) {
                System.out.print(j + " ");
            }
            System.out.println();
        }
    }
}
''', notes={(4, 1): "Short row :: = i = 1, so j runs only once.",
            (3, 4): "Longer row :: = i = 4: the inner loop will now run four times."},
 tryit="Press <b>Run</b>. Then print <code>i</code> instead of <code>j</code> and see the pattern change."),
]
