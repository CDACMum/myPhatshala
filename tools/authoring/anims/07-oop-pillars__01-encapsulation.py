from mkanim import Anim
HEADING = "Watch it with an example: a wallet that protects its balance"
INTRO = "The balance field is <code>private</code>. Outside code can't touch it directly; it must go through <code>withdraw()</code>, which checks the rules first."
A = Anim("private balance, public withdraw()", frames=6, h=224, label="encapsulation guarding a private field")
A.box(6, 14, 348, 30, None, fill="board", stroke="board")
for f, t in {1: "Wallet w = new Wallet(500);", 2: "w.balance = 1000000;", 3: "w.withdraw(200);", 4: "w.withdraw(200);", 5: "w.withdraw(900);", 6: "w.getBalance();"}.items():
    A.text(14, 34, t, on=str(f), mono=True, size=10.5, cls="chalk")
A.box(150, 56, 204, 130, None, fill="soft-green", stroke="green")
A.text(160, 74, "#1 Wallet", mono=True, bold=True, size=10)
A.box(164, 84, 176, 40, None, fill="board", stroke="board")
A.text(174, 100, "private int balance", mono=True, size=9.5, cls="kw")
for f, v in {1: "500", 2: "500", 3: "500", 4: "300", 5: "300", 6: "300"}.items():
    A.text(330, 116, v, on=str(f), mono=True, size=12, bold=True, cls="chalk", anchor="end")
A.box(164, 134, 176, 40, None, fill="card2", stroke="green")
A.text(174, 150, "public withdraw(amt)", mono=True, size=9.5, bold=True)
A.text(174, 166, "if (amt &gt; balance) throw …", mono=True, size=8.8, cls="ink2")
A.box(10, 70, 120, 34, "outside code", fill="soft-blue", stroke="blue", size=10.5, bold=True)
A.arrow(130, 98, 162, 104, on="2", color="red")
A.text(10, 128, "✗ compile error:", on="2", size=10, cls="red", bold=True)
A.text(10, 144, "balance has private", on="2", size=10, cls="red")
A.text(10, 158, "access in Wallet", on="2", size=10, cls="red")
A.arrow(130, 92, 162, 150, on="3-5", color="blue")
A.text(10, 128, "200 ≤ 500 ✓", on="3-4", size=10.5, cls="green", bold=True)
A.text(10, 146, "balance 500 → 300", on="4", size=10.5, mono=True)
A.text(10, 128, "900 &gt; 300 ✗", on="5", size=10.5, cls="red", bold=True)
A.text(10, 146, "IllegalArgument…", on="5", size=10, mono=True, cls="red")
A.text(10, 164, "balance unchanged", on="5", size=10, cls="ink2")
A.text(10, 128, "read-only access", on="6", size=10.5, bold=True)
A.text(10, 146, "returns 300", on="6", size=10.5, mono=True, cls="green")
A.text(180, 212, "Only the class's own methods can change balance.", anchor="middle", on="6", size=10, cls="ink2")
A.caps([
 "<b>The object:</b> a Wallet with 500 in a <code>private</code> field. Private means only code inside the Wallet class can read or write it.",
 "<b>Direct access:</b> <code>w.balance = 1000000</code> from another class doesn't even compile. Nobody can give themselves free money.",
 "<b>The safe door:</b> outside code calls the <code>public</code> method <code>withdraw(200)</code>. The method checks the rule first: 200 is not more than 500.",
 "<b>Changed safely:</b> the method itself updates balance to 300.",
 "<b>Rule enforced:</b> <code>withdraw(900)</code> fails the check and throws an exception. The balance can never go negative.",
 "<b>Read access:</b> a getter returns the value without exposing the field. Banking and wallet apps rely on this: every change goes through methods that validate and log it.",
])
