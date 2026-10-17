from mkanim import Anim
HEADING = "Watch it with an example: a code review on a fee program"
INTRO = "The code works but nobody can read it. Watch a reviewer fix one problem per step using Java's naming conventions."
A = Anim("Same code, readable names", frames=6, h=210)
A.box(6, 14, 348, 140, None, fill="board", stroke="board")
L = [
 {1: " ", 6: "package in.college.fees;"},
 {1: "class fee {", 2: "class FeeCalculator {"},
 {1: "  static final int m = 3;", 3: "  static final int MAX_INSTALMENTS = 3;"},
 {1: "  int a(int x) {", 4: "  int monthlyFee(int annualFee) {"},
 {1: "    return x / 12;", 4: "    return annualFee / 12;"},
 {1: "  }", 5: "  }   // fee is split into 12 equal parts"},
 {1: "}"},
]
def spans(d):
    ks = sorted(d); out = []
    for i, k in enumerate(ks):
        end = ks[i + 1] - 1 if i + 1 < len(ks) else 6
        out.append((f"{k}-{end}" if end > k else str(k), d[k], i > 0))
    return out
for r, d in enumerate(L):
    for on, t, changed in spans(d):
        changed = changed or (r == 0)
        A.text(16, 32 + r * 18, t, on=on, mono=True, size=10, cls="str" if changed else "chalk", bold=changed)
tips = {1: "Works, but what are fee, m, a and x?", 2: "Classes: PascalCase nouns", 3: "Constants: UPPER_SNAKE_CASE",
        4: "Methods and variables: camelCase", 5: "Comments explain why, not what", 6: "Packages: lowercase, reversed domain"}
for f, t in tips.items():
    A.box(6, 164, 348, 32, t, on=str(f), fill="soft-acc" if f == 1 else "soft-green", stroke="track" if f == 1 else "green", bold=True, size=10.5)
A.caps([
 "<b>Before:</b> this compiles and gives the right answer, but a teammate has to guess what <code>fee</code>, <code>m</code>, <code>a</code> and <code>x</code> mean.",
 "<b>Class name:</b> class names start with a capital letter and are nouns: <code>FeeCalculator</code>.",
 "<b>Constant:</b> <code>static final</code> values use capitals with underscores: <code>MAX_INSTALMENTS</code>.",
 "<b>Method and parameter:</b> camelCase, and say what they are: <code>monthlyFee(int annualFee)</code>.",
 "<b>Comment:</b> say <i>why</i> the code does something. The compiler throws comments away; they are only for humans.",
 "<b>Package:</b> lowercase, often a reversed domain such as <code>in.college.fees</code>, so names never clash with other teams' classes. Tools like Checkstyle check these rules automatically in code review.",
])
