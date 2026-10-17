from mkanim import Anim
HEADING = "Watch it with an example: a bank's month-end interest job speeding up"
INTRO = "A batch job calls <code>addInterest()</code> for every account. Watch the JVM spot the hot method, compile it twice, and briefly step back when a new account type appears."
A = Anim("Hot code gets compiled, and recompiled", frames=6, h=200, label="tiered JIT compilation in a batch job")
A.box(6, 8, 348, 28, None, fill="board", stroke="board")
for f, t in {1: "for (Account a : accounts) a.addInterest();",
             2: "// call 200: addInterest is hot",
             3: "// C1 code runs and profiles",
             4: "// call 5,000: C2 compiles",
             5: "// first FixedDeposit account!",
             6: "// recompiled for both types"}.items():
    A.text(14, 27, t, on=str(f), mono=True, size=10, cls="chalk")
A.text(14, 58, "calls to addInterest:", size=10)
for f, v in {1: "150", 2: "200", 3: "1,800", 4: "5,000", 5: "lakhs", 6: "lakhs"}.items():
    A.text(200, 58, v, on=str(f), size=10, mono=True, bold=True)
A.box(14, 70, 100, 30, "Interpreter", fill="card2", stroke="line", size=9.5, bold=True)
A.box(130, 70, 100, 30, "C1 (tier 3)", fill="soft-blue", stroke="blue", size=9.5, bold=True)
A.box(246, 70, 100, 30, "C2 (tier 4)", fill="soft-green", stroke="green", size=9.5, bold=True)
A.box(14, 70, 100, 30, None, fill="none", stroke="track", sw=3, on="1-2,5")
A.box(130, 70, 100, 30, None, fill="none", stroke="track", sw=3, on="3")
A.box(246, 70, 100, 30, None, fill="none", stroke="track", sw=3, on="4,6")
A.text(180, 116, "queued for C1 on a compiler thread", on="2", size=9.5, cls="blue", anchor="middle")
A.text(180, 116, "profile: receiver is always Savings", on="3", size=9.5, cls="ink2", anchor="middle")
A.text(180, 116, "inlined addInterest + getBalance", on="4", size=9.5, cls="green", anchor="middle", bold=False)
A.text(180, 116, "assumption broken: deoptimise", on="5", size=9.5, cls="red", anchor="middle", bold=True)
A.text(180, 116, "both types inlined behind a type check", on="6", size=9.5, cls="green", anchor="middle")
A.text(14, 148, "speed", size=9.5, cls="ink2")
A.box(60, 138, 284, 14, None, fill="card2", stroke="line", rx=4)
for f, w in {1: 30, 2: 30, 3: 120, 4: 270, 5: 40, 6: 270}.items():
    A.box(60, 138, w, 14, None, fill="soft-acc" if f in (1, 2, 5) else ("soft-blue" if f == 3 else "soft-green"),
          stroke="track" if f in (1, 2, 5) else ("blue" if f == 3 else "green"), rx=4, on=str(f))
A.text(14, 176, "interest credited: same on every account, every tier", on="6", size=9.5, cls="ink2")
A.text(14, 176, "\"made not entrant\" in -XX:+PrintCompilation", on="5", size=9.5, cls="red", mono=False)
A.caps([
 "<b>Batch starts:</b> the job runs in the interpreter, one bytecode at a time. The JVM counts every call to <code>addInterest</code>.",
 "<b>Hot:</b> around 200 calls (the default C1 threshold) the method is queued for compilation. A compiler thread works on it while the job keeps running.",
 "<b>C1:</b> quickly compiled tier 3 code takes over and records a profile: so far every account at this call site is a <code>SavingsAccount</code>.",
 "<b>C2:</b> after thousands of calls, C2 compiles tier 4 code that relies on that profile and inlines <code>addInterest</code> and the getters it uses. The job reaches full speed.",
 "<b>Surprise:</b> the first <code>FixedDeposit</code> account arrives. C2's assumption no longer holds, so that code is thrown away (deoptimised) and execution falls back for a while.",
 "<b>Recompiled:</b> with the new profile, C2 compiles again, this time handling both types. Speed recovers, and the interest credited was correct at every moment: only speed ever changes.",
])
