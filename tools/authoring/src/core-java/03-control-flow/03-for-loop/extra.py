WORKED_INTRO = "A <code>for</code> loop repeats work a known number of times. Each program below is a real job done with one loop. In the trace, watch the loop variable change, the condition being checked, and the running total grow on each pass."
EXAMPLES = [
dict(tag="Retail · daily sales", title="Total and best day of the week",
 problem="<p>A shop records sales for 5 days. Find the total, the average and the best day using one for loop over the array.</p>",
 inp="sales {4200, 3800, 5100, 2900, 6100}",
 approach=["Start <code>total = 0</code> and <code>best = 0</code>.",
           "Loop over indexes 0 to length − 1, adding and comparing.",
           "Day numbers are index + 1."],
 code='''public class Main {
    public static void main(String[] args) {
        int[] sales = {4200, 3800, 5100, 2900, 6100};
        int total = 0;
        int best = 0;
        for (int i = 0; i < sales.length; i++) {
            total += sales[i];
            if (sales[i] > sales[best]) {
                best = i;
            }
        }
        System.out.println("Total: Rs " + total + ", average: Rs " + total / sales.length);
        System.out.println("Best day: " + (best + 1) + " (Rs " + sales[best] + ")");
    }
}
''', notes={(6, 1): "Start :: = <code>i = 0</code>; 0 &lt; 5, so the body runs.",
            (7, 1): "Accumulate :: = total = 0 + 4200.",
            (9, 1): "New best :: = 5100 &gt; 4200, so index 2 (day 3) becomes the best so far.",
            12: "Loop done :: <code>i</code> reached 5, the condition failed, and <code>i</code> left the stack (it was declared in the for)."},
 tryit="Press <b>Run</b>. Then add a sixth day and check that nothing else needs changing."),
dict(tag="Banking · deposits", title="A recurring deposit year by year",
 problem="<p>A customer deposits Rs 10,000 at the start of each year for 4 years. The balance earns 7% interest at the end of each year. Print the balance after each year.</p>",
 inp="Rs 10,000 per year, 7%, 4 years",
 approach=["Loop <code>year</code> from 1 to 4.",
           "Add the deposit, then multiply by 1.07.",
           "Round when printing."],
 code='''public class Main {
    public static void main(String[] args) {
        double balance = 0;
        for (int year = 1; year <= 4; year++) {
            balance += 10000;
            balance *= 1.07;
            System.out.println("Year " + year + ": Rs " + Math.round(balance));
        }
    }
}
''', notes={(5, 1): "Deposit :: = Year 1: balance becomes 10000.",
            (6, 1): "Interest :: = × 1.07 = 10700.",
            (6, 2): "Compounding :: = Interest is now earned on last year's interest too."},
 tryit="Press <b>Run</b>. Then change it to 10 years. (Simplified: real deposits compound quarterly.)"),
dict(tag="Data · validation", title="Count digits and letters in a vehicle number",
 problem="<p>A parking app checks the number plate \"MH12AB4521\". Count how many characters are letters and how many are digits with a for loop over the String.</p>",
 inp="\"MH12AB4521\"",
 approach=["Loop over indexes of the String.",
           "<code>charAt(i)</code> gets each character.",
           "<code>Character.isDigit</code> / <code>isLetter</code> classify it."],
 code='''public class Main {
    public static void main(String[] args) {
        String plate = "MH12AB4521";
        int letters = 0, digits = 0;
        for (int i = 0; i < plate.length(); i++) {
            char c = plate.charAt(i);
            if (Character.isDigit(c)) {
                digits++;
            } else if (Character.isLetter(c)) {
                letters++;
            }
        }
        System.out.println(letters + " letters, " + digits + " digits");
    }
}
''', notes={(6, 1): "First char :: = <code>c</code> = 'M', a letter.",
            13: "Result :: 4 letters, 6 digits: a valid shape for an Indian plate."},
 tryit="Press <b>Run</b>. Then try a plate with a space in it and see it counted as neither."),
]
