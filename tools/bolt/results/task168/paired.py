"""Pair compiler CPU times by run, round and translation unit."""
from fractions import Fraction
from itertools import groupby
import json
import math
from pathlib import Path
import random
import statistics
import sys

A = Path(__file__).resolve().parent
W = A.parents[1]
B = W.with_name(W.name + "-bolt")
OLD = B / "tools/bolt/results/task167"
PAIRS = (("V3", "V1"), ("V3", "V2"), ("V2", "V1"), ("V1", "V0"), ("V2", "V0"), ("V3", "V0"))
GROUPS = (("all", None), ("small", "size_band"), ("medium", "size_band"), ("large", "size_band"),
          ("c", "language"), ("c++", "language"))
DRAWS = 10_000
SEED = 168


def read(path):
    return json.loads(path.read_text())


def save(path, obj):
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, allow_nan=False) + "\n")


def wilcoxon(ratios):
    """Two-sided conditional sign randomization, with average tied ranks."""
    factors = sorted((max(x, 1/x), x > 1) for x in ratios if x != 1)
    n = len(factors)
    if not n:
        return {"nonzero_tus": n, "W": 0, "p": 1.0}
    width_bytes = (n + 8) // 8
    bit_width = 8 * width_bytes
    polynomial, cumulative, positive = 1, 0, 0
    for _, items in groupby(factors, key=lambda x: x[0]):
        tied = list(items)
        rank2 = 2*cumulative + len(tied) + 1
        for _, sign in tied:
            polynomial += polynomial << (rank2*bit_width)
            if sign:
                positive += rank2
        cumulative += len(tied)
    total = n*(n+1)
    tail = min(positive, total-positive)
    # Each coefficient has more bits than 2**n, so additions never carry
    # between coefficients of the polynomial.
    raw = polynomial.to_bytes((total+1)*width_bytes, "little")
    lower = sum(int.from_bytes(raw[i:i+width_bytes], "little")
                for i in range(0, (tail+1)*width_bytes, width_bytes))
    return {"nonzero_tus": n, "W": tail/2, "p": min(1.0, lower/(1 << (n-1)))}


def metrics(values):
    if not values:
        return {"tus": 0, "ratio": None, "ci": None, "p": None}
    logs = [math.log(float(x)) for x in values]
    count = len(logs)
    rng = random.Random(SEED)
    simulations = sorted(math.exp(sum(rng.choices(logs, k=count))/count) for _ in range(DRAWS))
    return {"tus": count, "ratio": math.exp(statistics.mean(logs)),
            "ci": [simulations[int(p*(DRAWS-1))] for p in (0.025, 0.975)], **wilcoxon(values)}


def stored_time(row, mode):
    if row["status"] != "PASS":
        return None
    if mode == "167":
        return 2 * (round(row["user_seconds"]*100) + round(row["sys_seconds"]*100))
    return row["cpu_usec"]


def analyze(rounds, inputs, mode):
    timing = [{name: {r["tu"]: stored_time(r, mode) for r in variant["measurements"]}
               for name, variant in row["variants"].items()} for row in rounds]
    result = {}
    for candidate, reference in PAIRS:
        by_id = {}
        for tu in inputs:
            ratios, at_floor, available, dropped = [], [], 0, 0
            ident = tu["id"]
            for row in timing:
                new, old = row[candidate][ident], row[reference][ident]
                if new is None or old is None:
                    continue
                available += 1
                if new and old:
                    ratios.append(Fraction(new, old))
                else:
                    dropped += 1
                if mode == "167":
                    # Units above are 5ms; substitute the midpoint of the
                    # zero timing bin for the all-TU sensitivity analysis.
                    at_floor.append(Fraction(new or 1, old or 1))
            by_id[ident] = {"median": statistics.median(ratios) if ratios else None,
                            "midpoint": statistics.median(at_floor) if at_floor else None,
                            "positive_round_pairs": len(ratios), "zero_round_pairs": dropped,
                            "unavailable_round_pairs": len(rounds)-available}
        groups = {}
        for group, key in GROUPS:
            selected = [by_id[tu["id"]] for tu in inputs if key is None or tu[key] == group]
            stat = metrics([v["median"] for v in selected if v["median"] is not None])
            stat.update(available_tus=len(selected),
                        all_rounds_positive=sum(v["positive_round_pairs"] == len(rounds) for v in selected),
                        zero_round_pairs=sum(v["zero_round_pairs"] for v in selected),
                        unavailable_round_pairs=sum(v["unavailable_round_pairs"] for v in selected),
                        positive_round_pairs=sum(v["positive_round_pairs"] for v in selected))
            if mode == "167":
                stat["zero_bin_midpoint"] = metrics([v["midpoint"] for v in selected if v["midpoint"] is not None])
            groups[group] = stat
        per_tu = {ident: {field: str(value) if isinstance(value, Fraction) else value
                          for field, value in values.items()} for ident, values in by_id.items()}
        result[candidate+"/"+reference] = {"groups": groups, "per_tu": per_tu}
    return {"rounds": len(rounds), "observed_time_resolution_seconds": 0.01 if mode == "167" else 0.000001,
            "bootstrap_draws": DRAWS, "bootstrap_seed": SEED, "pairs": result}


def rounds_in(path):
    return [read(p) for p in sorted(path.glob("round-*.json"))]


def row_text(stat):
    if stat["ratio"] is None:
        return "—", "—"
    lo, hi = stat["ci"]
    return f"{stat['ratio']:.4f} [{lo:.4f}, {hi:.4f}]", f"{stat['p']:.4g}"


if __name__ == "__main__":
    rows = rounds_in(OLD)
    assert len(rows) == 5 and wilcoxon([Fraction(2), Fraction(2), Fraction(2)])["p"] == 0.25
    data = analyze(rows, read(OLD/"manifest.json")["inputs"], "167")
    save(A/"A-paired.json", data)
    for pair, item in data["pairs"].items():
        s = item["groups"]["all"]
        print(pair, s["tus"], *row_text(s), "midpoint", *row_text(s["zero_bin_midpoint"]), flush=True)
