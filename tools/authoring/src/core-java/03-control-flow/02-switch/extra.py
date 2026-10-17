WORKED_INTRO = "A <code>switch</code> picks one path from many fixed values: days, menu choices, status codes. These programs use both the classic form and the modern arrow form (Java 14+). In the trace, watch the JVM jump straight to the matching case."
EXAMPLES = [
dict(tag="Restaurant · offers", title="Today's offer by weekday",
 problem="<p>A restaurant runs a different offer each day. Given the day name, print the offer. Weekends share one offer. Use the arrow form, which never falls through.</p>",
 inp="day \"SAT\"",
 approach=["<code>switch (day)</code> on a String.",
           "<code>case \"SAT\", \"SUN\" -&gt;</code> groups two labels.",
           "<code>default</code> handles anything unexpected."],
 code='''public class Main {
    public static void main(String[] args) {
        String day = "SAT";
        String offer = switch (day) {
            case "MON" -> "Free dessert";
            case "WED" -> "2 for 1 on coffee";
            case "FRI" -> "20% off thalis";
            case "SAT", "SUN" -> "Family combo at Rs 799";
            default -> "No offer today";
        };
        System.out.println(day + ": " + offer);
    }
}
''', notes={4: "Switch expression :: = The JVM compares <code>day</code> with the case labels and jumps to the match. The result of the chosen case becomes the value of <code>offer</code>.",
            11: "Result :: Saturday matched the grouped weekend case."},
 tryit="Press <b>Run</b>. Then try \"TUE\" to reach the default."),
dict(tag="Banking · IVR", title="Phone-banking menu",
 problem="<p>A bank's phone menu: press 1 for balance, 2 for mini statement, 3 to block a card, 0 for an agent. Handle the key pressed with a classic switch and break.</p>",
 inp="key 3",
 approach=["<code>switch (key)</code> on an int.",
           "Each case ends with <code>break</code> so execution doesn't fall into the next case.",
           "<code>default</code> for invalid keys."],
 code='''public class Main {
    public static void main(String[] args) {
        int key = 3;
        switch (key) {
            case 1:
                System.out.println("Your balance is Rs 12,480");
                break;
            case 2:
                System.out.println("Sending mini statement by SMS");
                break;
            case 3:
                System.out.println("Card blocked. A new card will be sent.");
                break;
            case 0:
                System.out.println("Connecting to an agent...");
                break;
            default:
                System.out.println("Invalid option");
        }
        System.out.println("Thank you for banking with us");
    }
}
''', notes={4: "Jump :: = Key 3: the JVM jumps directly to <code>case 3</code>, skipping cases 1 and 2 without testing each one in turn.",
            13: "break :: = Leaves the switch. Without it, execution would fall through into case 0 and connect an agent too."},
 tryit="Press <b>Run</b>. Then delete the <code>break</code> after case 3 and see the fall-through."),
dict(tag="Payroll · calendar", title="Days in a month with grouped cases",
 problem="<p>A payroll system pays daily wages, so it needs the number of days in each month. Group months with the same length. February depends on whether it's a leap year.</p>",
 inp="month 2, year 2028; month 9",
 approach=["Arrow cases with several labels: <code>case 4, 6, 9, 11 -&gt; 30</code>.",
           "A block with <code>yield</code> for February's leap-year rule.",
           "Compute wages for February 2028 at Rs 650/day."],
 code='''public class Main {
    static int daysIn(int month, int year) {
        return switch (month) {
            case 4, 6, 9, 11 -> 30;
            case 2 -> {
                boolean leap = (year % 4 == 0 && year % 100 != 0) || year % 400 == 0;
                yield leap ? 29 : 28;
            }
            default -> 31;
        };
    }

    public static void main(String[] args) {
        int feb = daysIn(2, 2028);
        System.out.println("Feb 2028: " + feb + " days, wages Rs " + feb * 650);
        System.out.println("Sep: " + daysIn(9, 2028) + " days");
    }
}
''', notes={(6, 1): "February :: = 2028 is divisible by 4 and not by 100: a leap year.",
            (7, 1): "yield :: = In a block inside a switch expression, <code>yield</code> gives the case's value: 29."},
 tryit="Press <b>Run</b>. Then try February 2100 (not a leap year)."),
]
