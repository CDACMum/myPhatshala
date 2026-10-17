from mkanim import Anim
HEADING = "Watch it with an example: a bank's loan products"
INTRO = "Every loan uses the same EMI formula, but each loan type has its own interest rate. An abstract <code>Loan</code> class holds the formula and leaves the rate to its children."
A = Anim("abstract Loan, concrete loan types", frames=6, h=232, label="abstract class with a shared EMI formula and an abstract rate")
A.box(6, 14, 348, 30, None, fill="board", stroke="board")
code = {1: "Loan l = new Loan(500000, 36);", 2: "class GoldLoan extends Loan { }",
        3: "Loan l = new HomeLoan(3000000, 240);", 4: "l.emi();   // final, in Loan",
        5: "l = new CarLoan(600000, 60);", 6: "for (Loan x : loans) x.emi();"}
for f, t in code.items():
    A.text(14, 34, t, on=str(f), mono=True, size=10.5, cls="chalk")
A.box(170, 56, 182, 62, None, fill="soft-blue", stroke="blue")
A.text(180, 72, "abstract class Loan", mono=True, size=9.8, bold=True, cls="blue")
A.text(180, 88, "abstract double rate();", mono=True, size=9, cls="ink2")
A.text(180, 104, "final double emi() {…}", mono=True, size=9, cls="ink2")
A.box(170, 56, 182, 62, None, fill="none", stroke="green", on="4", sw=2.5)
A.box(170, 140, 84, 40, None, fill="soft-acc", stroke="track", on="3-")
A.text(178, 156, "HomeLoan", mono=True, size=9.5, bold=True, cls="acc", on="3-")
A.text(178, 172, "rate() 8.5", mono=True, size=9, cls="ink2", on="3-")
A.box(268, 140, 84, 40, None, fill="soft-acc", stroke="track", on="5-")
A.text(276, 156, "CarLoan", mono=True, size=9.5, bold=True, cls="acc", on="5-")
A.text(276, 172, "rate() 9.5", mono=True, size=9, cls="ink2", on="5-")
A.box(170, 140, 84, 40, None, fill="none", stroke="green", on="4", sw=2.5)
A.box(268, 140, 84, 40, None, fill="none", stroke="green", on="5", sw=2.5)
A.arrow(212, 140, 230, 118, on="3-", color="track")
A.arrow(310, 140, 292, 118, on="5-", color="track")
A.box(170, 140, 100, 40, None, fill="card2", stroke="red", on="2")
A.text(178, 156, "GoldLoan", mono=True, size=9.5, bold=True, cls="red", on="2")
A.text(178, 172, "rate() missing", mono=True, size=9, cls="red", on="2")
A.lines(10, 68, ["error: Loan is", "abstract; cannot", "be instantiated"], on="1", size=9.5, mono=True, cls="red")
A.lines(10, 68, ["error: GoldLoan is", "not abstract and", "does not override", "abstract method", "rate() in Loan"], on="2", size=9.5, mono=True, cls="red")
A.lines(10, 68, ["Loan's constructor", "runs first (super)", "principal 30,00,000", "240 months"], on="3", size=9.5, cls="ink")
A.lines(10, 68, ["emi() calls rate()", "→ HomeLoan: 8.5%", "EMI Rs 26,035"], on="4", size=10, cls="ink")
A.text(10, 126, "Rs 26,035", on="4", size=13, bold=True, mono=True, cls="green")
A.lines(10, 68, ["same emi() code", "→ CarLoan: 9.5%", "EMI Rs 12,601"], on="5", size=10, cls="ink")
A.text(10, 126, "Rs 12,601", on="5", size=13, bold=True, mono=True, cls="green")
A.lines(10, 68, ["Home Rs 26,035", "Car  Rs 12,601", "one formula,", "many rates"], on="6", size=10, mono=True, cls="green", bold=True)
A.note({1: "An abstract class can't be created on its own.", 2: "Forgetting the abstract method is a compile error.",
        3: "A concrete loan; the abstract parent's part is built first.", 4: "Shared final formula, child-supplied rate.",
        5: "Same formula, different rate: a different EMI.", 6: "New loan type = one class with one rate()."}, y=214, size=10)
A.caps([
 "<b>No plain loans:</b> <code>Loan</code> is abstract. A loan with no rate makes no sense, so <code>new Loan(...)</code> doesn't compile.",
 "<b>Contract enforced:</b> a new <code>GoldLoan</code> that forgets <code>rate()</code> is rejected by javac, so it can never reach customers with a missing rate.",
 "<b>Concrete child:</b> <code>new HomeLoan(...)</code> works. Its constructor calls <code>super(...)</code>, so Loan's constructor stores the principal and tenure.",
 "<b>Shared formula:</b> <code>emi()</code> is written once in Loan (and is final). It calls the abstract <code>rate()</code>, which dispatches to HomeLoan's 8.5%: EMI ≈ Rs 26,035 for Rs 30 lakh over 20 years.",
 "<b>Same code, different child:</b> for a CarLoan at 9.5%, Rs 6 lakh over 5 years, the same formula gives ≈ Rs 12,601.",
 "<b>The payoff:</b> the bank's EMI calculator loops over <code>Loan</code> objects. Each product supplies only its rate. (Teaching figures, not real offers.)",
])
