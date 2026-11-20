"""Shared memory admission and parallelism for profile stages."""
import os

GIB = 2**30
PAGE = os.sysconf("SC_PAGE_SIZE")
RESERVE = 4 * GIB
WATCHDOG_MEMORY = 3 * GIB
WATCHDOG_DISK = 15 * GIB
FULL_CAP = 24 * GIB
PEAKS = {
    "instrumented-build": 7227248640,
    "ir-train": 1481818112,
    "merge-profdata": 1824751616,
    "bolt-match": 8712601600,
    "write-manifest": 21703991296,
}
BUILD_STAGES = {"full-build", "instrumented-build", "pgo-build", "bolt-tools-relink"}
BOLT_INSTRUMENT = "bolt-instrument-train-merge"


def peak_budget(stage):
    return (PEAKS[stage] * 6 + 5 * PAGE - 1) // (5 * PAGE) * PAGE


def budget(stage):
    if stage == "archive-replay":
        return 12 * GIB, 11222745088
    if stage in ("full-build", "pgo-build"):
        return FULL_CAP, 10 * GIB
    if stage == "bolt-tools-relink":
        return FULL_CAP, 15 * GIB
    if stage == "instrumented-build":
        return FULL_CAP, peak_budget(stage)
    if stage == BOLT_INSTRUMENT:
        return FULL_CAP, 18 * GIB
    cap = min(FULL_CAP, peak_budget(stage))
    return cap, GIB if stage == "write-manifest" else cap


def parallelism(stage, memory_max):
    if stage in BUILD_STAGES:
        jobs = 6 if memory_max >= 20 * GIB else 4 if memory_max >= 14 * GIB else 2
        return {"jobs": jobs, "thinlto_jobs": jobs, "link_jobs": 1}
    return {"jobs": 2 if stage == "archive-replay" else 1,
            "thinlto_jobs": None, "link_jobs": None}


def admission(stage, available):
    cap, floor = budget(stage)
    memory_max = max(0, min(available - RESERVE, cap)) // PAGE * PAGE
    return {"stage": stage, "memory_max": memory_max, "standard_cap": cap, "floor": floor,
            **parallelism(stage, memory_max), "admitted": memory_max >= floor}
