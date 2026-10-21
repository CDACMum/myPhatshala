import random, time

random.seed(27)
OUTCOMES = [0, 0, 1, 1, 1, 2, 4, 6, "W"]


def ball_stream(overs=3):
    """An endless-looking stream of balls, one every 0.3 s (sped up)."""
    for over in range(1, overs + 1):
        for ball in range(1, 7):
            time.sleep(0.3)
            yield over, ball, random.choice(OUTCOMES)


# STREAM processing: update the answer the moment each ball arrives
total, wickets, over_runs, per_over = 0, 0, 0, []
start = time.time()
for over, ball, result in ball_stream():
    if result == "W":
        wickets += 1
    else:
        total += result
        over_runs += result
    print(f"{time.time() - start:4.1f}s  ball {over - 1}.{ball}  {str(result):>2}   score {total}/{wickets}")
    if ball == 6:                       # the "over" window closes
        print(f"        --- over {over}: {over_runs} runs ---")
        per_over.append(over_runs)
        over_runs = 0

# BATCH processing: after the match, compute from the complete data
print("Batch summary after the match:", per_over, "| run rate", round(total / len(per_over), 2))
