from mkanim import Anim
HEADING = "Watch it with an example: opening a bank account (KYC)"
INTRO = "A bank won't open an account without a name and PAN. The constructor makes these details compulsory, and constructor chaining fills in sensible defaults."
A = Anim("new Account(\"Riya\", \"ABCDE1234F\")", frames=6, h=226, label="constructor and chaining")
A.box(6, 14, 348, 30, None, fill="board", stroke="board")
for f, t in {1: "Account a = new Account(\"Riya\", \"ABCDE1234F\");", 2: "// JVM: memory with default values", 3: "Account(String n, String p) { this(n, p, 1000); }", 4: "Account(String n, String p, int min) { name = n; … }", 5: "// constructor done → reference stored in a", 6: "new Account();  // compile error"}.items():
    A.text(14, 34, t, on=str(f), mono=True, size=9.5, cls="chalk")
A.box(150, 60, 204, 92, None, fill="soft-green", stroke="green", on="2-5")
A.text(160, 78, "#1 Account", mono=True, bold=True, size=10, on="2-5")
for i, (n, d, v) in enumerate([("name", "null", "\"Riya\""), ("pan", "null", "\"ABCDE1234F\""), ("balance", "0", "1000")]):
    A.text(160, 98 + i * 18, f"{n} = {d}", mono=True, size=10, on="2-3", cls="ink3")
    A.text(160, 98 + i * 18, f"{n} = {v}", mono=True, size=10, on="4-5", bold=True)
A.text(10, 70, "STACK", bold=True, size=9.5, cls="ink2")
A.box(10, 78, 120, 30, "Account(n, p)", fill="soft-acc", stroke="track", mono=True, size=9.5, on="3-4")
A.box(10, 112, 120, 30, "Account(n, p, min)", fill="soft-acc", stroke="track", mono=True, size=9, on="4")
A.box(10, 150, 120, 30, "a → #1", fill="soft-blue", stroke="blue", mono=True, size=10, on="5", bold=True)
A.arrow(130, 165, 150, 120, on="5", color="blue")
A.box(10, 168, 344, 40, "constructor Account() is undefined: KYC can't be skipped", fill="soft-acc", stroke="red", cls="red", size=10, bold=True, on="6")
A.caps([
 "<b>Opening:</b> <code>new Account(\"Riya\", \"ABCDE1234F\")</code>. The constructor's parameters are exactly what the bank requires.",
 "<b>Memory first:</b> the JVM creates object #1 with default values: <code>null</code> for references, 0 for numbers.",
 "<b>Chaining:</b> the 2-argument constructor calls <code>this(n, p, 1000)</code>, passing a default minimum balance. <code>this(…)</code> must be the first line.",
 "<b>Main constructor:</b> sets name, PAN and balance. All the real work is in one place.",
 "<b>Ready:</b> only now is the reference stored in <code>a</code>. Nobody can ever see a half-built account.",
 "<b>Safety:</b> because the class defines constructors with parameters, Java gives no default no-arg constructor. <code>new Account()</code> doesn't compile, so required details can't be skipped.",
])
