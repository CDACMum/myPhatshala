WORKED_INTRO = "<code>break</code> leaves a loop early; <code>continue</code> skips to the next pass. Both are about not doing unnecessary work. In the traces, watch the JVM jump straight out of the loop, or straight back to its top."
EXAMPLES = [
dict(tag="Inventory · stock", title="Find the first out-of-stock item",
 problem="<p>A shop's app checks the stock of 6 items in order and must alert on the <b>first</b> item with zero stock. No need to look further once it's found: use <code>break</code>.</p>",
 inp="items Rice, Oil, Sugar, Salt, Tea, Dal; stock 40, 12, 0, 25, 0, 8",
 approach=["Loop over the items.",
           "When stock is 0, remember the item and <code>break</code>.",
           "After the loop, report what was found (or that all are in stock)."],
 code='''public class Main {
    public static void main(String[] args) {
        String[] items = {"Rice", "Oil", "Sugar", "Salt", "Tea", "Dal"};
        int[] stock = {40, 12, 0, 25, 0, 8};
        String firstEmpty = "none";
        int checked = 0;
        for (int i = 0; i < items.length; i++) {
            checked++;
            if (stock[i] == 0) {
                firstEmpty = items[i];
                break;
            }
        }
        System.out.println("First out of stock: " + firstEmpty + " (checked " + checked + " items)");
    }
}
''', notes={(11, 1): "break :: = Sugar has 0 stock. <code>break</code> jumps out of the loop immediately: Salt, Tea and Dal are never checked.",
            14: "Result :: Only 3 of 6 items were checked."},
 tryit="Press <b>Run</b>. Then remove <code>break</code>: which item is reported now, and how many were checked?"),
dict(tag="E-commerce · orders", title="Total only the delivered orders",
 problem="<p>Today's orders have statuses. Cancelled orders must be skipped when totalling revenue. Use <code>continue</code> to skip them.</p>",
 inp="amounts 450, 1200, 300, 800; statuses OK, CANCELLED, OK, OK",
 approach=["Loop over the orders.",
           "If cancelled, <code>continue</code>: go straight to the next order.",
           "Otherwise add the amount."],
 code='''public class Main {
    public static void main(String[] args) {
        int[] amounts = {450, 1200, 300, 800};
        String[] status = {"OK", "CANCELLED", "OK", "OK"};
        int revenue = 0;
        for (int i = 0; i < amounts.length; i++) {
            if (status[i].equals("CANCELLED")) {
                continue;
            }
            revenue += amounts[i];
        }
        System.out.println("Revenue: Rs " + revenue);
    }
}
''', notes={(8, 1): "continue :: = Order 2 is cancelled: the rest of the body is skipped and the loop moves to i = 2.",
            12: "Result :: 450 + 300 + 800 = 1550."},
 tryit="Press <b>Run</b>. Then cancel the last order too."),
dict(tag="Cinema · seats", title="Find a free seat with a labeled break",
 problem="<p>A small hall has 3 rows of 4 seats (1 = booked, 0 = free). Find the first free seat, searching row by row. A plain <code>break</code> would only leave the inner loop, so use a <b>labeled break</b> to leave both.</p>",
 inp="rows {1,1,1,1}, {1,1,0,1}, {0,0,0,0}",
 approach=["Label the outer loop <code>search:</code>.",
           "When a free seat is found, record it and <code>break search;</code>.",
           "Print the seat as row letter + number."],
 code='''public class Main {
    public static void main(String[] args) {
        int[][] hall = {{1, 1, 1, 1}, {1, 1, 0, 1}, {0, 0, 0, 0}};
        int foundRow = -1, foundSeat = -1;
        search:
        for (int r = 0; r < hall.length; r++) {
            for (int s = 0; s < hall[r].length; s++) {
                if (hall[r][s] == 0) {
                    foundRow = r;
                    foundSeat = s;
                    break search;
                }
            }
        }
        System.out.println("First free seat: " + (char) ('A' + foundRow) + (foundSeat + 1));
    }
}
''', notes={(11, 1): "Labeled break :: = Row B, seat 3 is free. <code>break search</code> leaves both loops at once; row C is never examined.",
            15: "Result :: Seat B3."},
 tryit="Press <b>Run</b>. Then change <code>break search;</code> to <code>break;</code>: the outer loop keeps going and finds a seat in row C, overwriting the answer."),
]
