WORKED_INTRO = "Use <code>while</code> when you don't know in advance how many times to repeat: until a goal is reached, until a valid input arrives, until a number runs out of digits. In the traces, watch the condition being re-checked before (while) or after (do-while) each pass."
EXAMPLES = [
dict(tag="Personal finance · goals", title="How many months to save for a laptop?",
 problem="<p>A student saves Rs 3,500 a month and also earns 1% interest per month on what's saved. How many months until she has Rs 15,000 for a laptop?</p>",
 inp="goal 15000, saves 3500/month, 1% per month",
 approach=["Start with balance 0 and months 0.",
           "While the balance is below the goal: add interest, add the saving, count a month.",
           "The loop stops as soon as the goal is reached."],
 code='''public class Main {
    public static void main(String[] args) {
        double balance = 0;
        int months = 0;
        while (balance < 15000) {
            balance = balance * 1.01 + 3500;
            months++;
        }
        System.out.println("Months needed: " + months);
        System.out.println("Balance then: Rs " + Math.round(balance));
    }
}
''', notes={(5, 1): "Check first :: = 0 &lt; 15000 is true, so the body runs.",
            (6, 1): "Month 1 :: = 0 × 1.01 + 3500 = 3500.",
            9: "Done :: After 5 months the balance passed 15000; the condition became false and the loop ended."},
 tryit="Press <b>Run</b>. Then raise the goal to 50,000. (Simplified interest.)"),
dict(tag="Banking · ATM", title="Three PIN attempts with do-while",
 problem="<p>An ATM allows up to 3 PIN attempts. The customer's attempts are in an array (simulating key presses). Use a do-while: the first attempt always happens, then repeat while the PIN is wrong and attempts remain.</p>",
 inp="correct PIN 4821; attempts 1234, 4812, 4821",
 approach=["<code>do { … } while (…)</code> runs the body at least once.",
           "Each pass reads the next attempt and counts it.",
           "After the loop, decide: unlocked or card blocked."],
 code='''public class Main {
    public static void main(String[] args) {
        int correctPin = 4821;
        int[] typed = {1234, 4812, 4821};
        int attempt = 0;
        boolean ok;
        do {
            ok = typed[attempt] == correctPin;
            System.out.println("Attempt " + (attempt + 1) + ": " + (ok ? "correct" : "wrong"));
            attempt++;
        } while (!ok && attempt < 3);
        System.out.println(ok ? "Card unlocked" : "Card blocked");
    }
}
''', notes={(8, 1): "First attempt :: = The body runs before any check: 1234 ≠ 4821.",
            (11, 1): "Check after :: = Wrong and attempts left: go round again.",
            (11, 3): "Stop :: = The third attempt was correct, so <code>!ok</code> is false and the loop ends."},
 tryit="Press <b>Run</b>. Then make the third attempt wrong as well and see the card blocked."),
dict(tag="Data · checks", title="Digit sum of an account number",
 problem="<p>Some systems use a digit sum as a quick check on account numbers. Add up the digits of 40021876 by repeatedly taking the last digit with <code>% 10</code> and removing it with <code>/ 10</code>.</p>",
 inp="40021876",
 approach=["While the number is greater than 0:",
           "add <code>n % 10</code> (last digit) to the sum, then <code>n /= 10</code>.",
           "Count the digits too."],
 code='''public class Main {
    public static void main(String[] args) {
        int n = 40021876;
        int sum = 0, digits = 0;
        while (n > 0) {
            sum += n % 10;
            n /= 10;
            digits++;
        }
        System.out.println(digits + " digits, digit sum " + sum);
    }
}
''', notes={(6, 1): "Last digit :: = 40021876 % 10 = 6.",
            (7, 1): "Remove it :: = 40021876 / 10 = 4002187 (integer division drops the last digit).",
            10: "Result :: 8 digits, sum 28."},
 tryit="Press <b>Run</b>. Then try your own phone number's last 8 digits."),
]
