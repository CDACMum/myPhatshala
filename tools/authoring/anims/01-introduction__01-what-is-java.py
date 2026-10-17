from mkanim import Anim
HEADING = "Watch it with an example: one UPI payment"
INTRO = "You pay Rs 60 at the college canteen. Follow the payment and see where Java code is doing the work."
A = Anim("Rs 60 from Riya to the canteen", frames=6, h=226)
A.box(6, 36, 74, 62, "Riya's", fill="soft-blue", stroke="blue", bold=True, sub="phone", size=11)
A.box(96, 14, 168, 172, None, fill="card", stroke="line")
A.text(180, 33, "Bank server", anchor="middle", bold=True, size=11)
A.text(180, 47, "Java program on a JVM", anchor="middle", size=9.5, cls="ink2")
A.box(280, 36, 74, 62, "Canteen", fill="soft-green", stroke="green", bold=True, sub="phone", size=11)
A.box(104, 62, 112, 30, "check PIN, limit", fill="soft-acc", stroke="track", on="2-", size=10)
A.box(104, 100, 112, 30, "Riya 500→440", fill="soft-acc", stroke="track", on="3-", size=10, mono=True)
A.box(104, 138, 112, 30, "Canteen +60", fill="soft-acc", stroke="track", on="4-", size=10, mono=True)
A.arrow(82, 70, 94, 70, on="1-")
A.arrow(262, 150, 300, 100, on="4-", color="green")
A.token(56, 12, 40, 22, "₹60", pos={1: "0,0", 2: "164,53", 3: "164,91", 4: "164,129", 5: "240,-2"}, size=10)
A.text(317, 118, "Paid ✓", on="5-", anchor="middle", cls="green", bold=True, size=11)
A.text(43, 116, "Sent ✓", on="6", anchor="middle", cls="green", bold=True, size=11)
A.caps([
 "<b>Tap Pay:</b> the UPI app on Riya's phone sends a payment request (who pays, who gets it, how much) over the internet to the bank.",
 "<b>Check:</b> on the bank's server a Java program checks the UPI PIN and the daily limit. If anything is wrong, it stops here and sends back an error.",
 "<b>Debit:</b> Java code reduces Riya's balance from 500 to 440. Banks write this kind of code very carefully, because money must never be lost or created.",
 "<b>Credit:</b> the same program adds 60 to the canteen's account.",
 "<b>Confirm:</b> the canteen's phone shows “Paid”. The JVM ran this Java program on the bank's server, not on either phone.",
 "<b>Done:</b> Riya's app shows “Sent”. Many banking and payment back-ends are written in Java because it is fast, safe and runs on any server. (Simplified: real UPI also passes through NPCI and both banks.)",
])
