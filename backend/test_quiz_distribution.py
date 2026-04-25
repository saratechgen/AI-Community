"""
30-day quiz distribution test.

Simulates the scheduler logic for 30 consecutive days and asserts:
  1. No exact duplicate days (same 5-question set repeated within 30 days)
  2. Max frequency of any single question <= 10 out of 30 days (<=33%)
  3. Day-to-day overlap (questions shared with yesterday) <= 2 per stage on average

SHA-256 seeding with a 35-question pool gives C(35,5)=324,632 combos —
collision probability over 30 days is ~0.13%, so no exclusion window is needed.

Run with: python test_quiz_distribution.py
"""

import sys
from collections import defaultdict
from datetime import date, timedelta

sys.path.insert(0, ".")
from quiz_source import get_questions_for_stage, QUESTION_BANK


def simulate(days: int = 30, stages: list[int] = [1, 2, 3]) -> dict:
    start = date(2026, 4, 1)
    freq: dict[int, dict[str, int]] = {s: defaultdict(int) for s in stages}
    daily_sets: dict[int, list[frozenset]] = {s: [] for s in stages}
    overlaps: dict[int, list[int]] = {s: [] for s in stages}

    for day_n in range(days):
        date_str = (start + timedelta(days=day_n)).isoformat()

        for s in stages:
            qs = get_questions_for_stage(stage=s, n=5, date_str=date_str)
            ids = frozenset(q["id"] for q in qs)

            if daily_sets[s]:
                overlaps[s].append(len(ids & daily_sets[s][-1]))

            for qid in ids:
                freq[s][qid] += 1

            daily_sets[s].append(ids)

    return {"freq": freq, "daily_sets": daily_sets, "overlaps": overlaps}


def run_assertions(result: dict, days: int = 30) -> None:
    freq        = result["freq"]
    daily_sets  = result["daily_sets"]
    overlaps    = result["overlaps"]
    stages      = [1, 2, 3]
    pool_size   = {s: sum(1 for q in QUESTION_BANK if q["stage"] == s) for s in stages}
    failures    = []

    for s in stages:
        max_freq = max(freq[s].values()) if freq[s] else 0
        threshold = days // 3  # 33% ceiling
        if max_freq > threshold:
            worst_id = max(freq[s], key=freq[s].get)
            failures.append(
                f"Stage {s}: question {worst_id} appeared {max_freq}x"
                f" (pool={pool_size[s]}, limit={threshold})"
            )

        # Exact duplicate days
        seen = set()
        for i, s_set in enumerate(daily_sets[s]):
            key = frozenset(s_set)
            if key in seen:
                failures.append(f"Stage {s}: duplicate quiz day at index {i}")
            seen.add(key)

        # Average day-to-day overlap
        if overlaps[s]:
            avg = sum(overlaps[s]) / len(overlaps[s])
            if avg > 2.0:
                failures.append(
                    f"Stage {s}: avg day-to-day overlap = {avg:.2f} (limit 2.0)"
                )

    if failures:
        print("FAIL")
        for f in failures:
            print(f"  FAIL: {f}")
        sys.exit(1)
    else:
        print("PASS")


def print_report(result: dict, days: int = 30) -> None:
    freq       = result["freq"]
    overlaps   = result["overlaps"]
    stages     = [1, 2, 3]
    pool_size  = {s: sum(1 for q in QUESTION_BANK if q["stage"] == s) for s in stages}
    stage_name = {1: "Foundation", 2: "Applied", 3: "Advanced"}

    print(f"\n{'-'*52}")
    print(f"  {days}-Day Distribution Report")
    print(f"{'-'*52}")
    for s in stages:
        counts = sorted(freq[s].values())
        mn, mx = (min(counts), max(counts)) if counts else (0, 0)
        avg_ov = (
            f"{sum(overlaps[s]) / len(overlaps[s]):.2f}"
            if overlaps[s] else "n/a"
        )
        print(
            f"  Stage {s} {stage_name[s]:<12} "
            f"pool={pool_size[s]:>2}  "
            f"freq min={mn} max={mx}  "
            f"avg overlap/day={avg_ov}"
        )
    print(f"{'-'*52}\n")


if __name__ == "__main__":
    DAYS = 30
    result = simulate(days=DAYS)
    print_report(result, days=DAYS)
    run_assertions(result, days=DAYS)
