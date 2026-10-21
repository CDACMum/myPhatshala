"""India-scale numbers turned into per-second rates, and a Tatkal-style
virtual waiting room that admits users at a safe rate."""
import random

published = {
    # figure, unit, source (see the lesson's Sources list)
    "UPI, September 2026": (24.07e9, "transactions in the month"),
    "IRCTC, peak minute (16 Aug 2025)": (37_410, "tickets in one minute"),
    "Live cricket, 2023 World Cup final": (5.9e7, "concurrent viewers"),
}

upi_per_s = 24.07e9 / (30 * 86_400)
irctc_per_s = 37_410 / 60
viewers = 5.9e7
bitrate_mbps = 2.5                       # assumption: an average mobile stream
print(f"UPI average           : {upi_per_s:,.0f} transactions per second")
print(f"IRCTC peak            : {irctc_per_s:,.0f} tickets per second")
print(f"Live final, bandwidth : {viewers * bitrate_mbps / 1e6:,.0f} Tbps if every viewer streams {bitrate_mbps} Mbps")

# ---- a virtual waiting room for a 10:00 am rush
random.seed(3)
arrivals = sorted(random.uniform(0, 60) for _ in range(30_000))   # 30,000 users in the first minute
ADMIT_PER_SECOND = 250                                            # what the booking system can safely take
admitted_at = []
next_slot = 0.0
for t in arrivals:
    start = max(t, next_slot)
    admitted_at.append(start)
    next_slot = start + 1 / ADMIT_PER_SECOND
waits = [a - t for a, t in zip(admitted_at, arrivals)]
print(f"\nWaiting room: {len(arrivals):,} users arrive in 60 s, admitted at {ADMIT_PER_SECOND}/s")
print(f"  last user admitted after {admitted_at[-1]:.0f} s")
print(f"  median wait {sorted(waits)[len(waits) // 2]:.0f} s, worst wait {max(waits):.0f} s")
print("  the booking servers never see more than 250 users per second")
