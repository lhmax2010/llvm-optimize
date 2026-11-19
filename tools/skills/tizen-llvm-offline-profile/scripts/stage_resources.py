"""Shared memory admission and parallelism for the profile stages."""
import os

GIB = 2**30
PAGE = os.sysconf("SC_PAGE_SIZE")
RESERVE = 6 * GIB
LINK_FLOOR = 15 * GIB
FULL_CAP = 24 * GIB
PEAKS = {
    "instrumented-build": 7227248640,
    "ir-train": 1481818112,
    "merge-profdata": 1824751616,
    "pgo-build": 21703991296,
    "bolt-tools-relink": None,
    "bolt-instrument-train-merge": 17074352128,
    "bolt-match": 8712601600,
    "write-manifest": None,
}
BUILD_STAGES = {"full-build", "instrumented-build", "pgo-build", "bolt-tools-relink"}


def budget(stage):
    if stage == "full-build":
        return FULL_CAP, LINK_FLOOR
    if stage == "archive-replay":
        return 12 * GIB, 11222745088
    peak = PEAKS[stage]
    cap = ((peak if peak is not None else PEAKS["pgo-build"]) * 6 + 4) // 5
    # Round the historical cap up to the kernel's MemoryMax granularity.
    cap = (cap + PAGE - 1) // PAGE * PAGE
    if stage in ("pgo-build", "bolt-tools-relink"):
        return cap, LINK_FLOOR
    if stage == "write-manifest":
        return cap, GIB
    return cap, cap


def admission(stage, available):
    cap, floor = budget(stage)
    memory_max = max(0, min(available - RESERVE, cap))
    if stage in BUILD_STAGES:
        jobs = max(2, 6 * memory_max // FULL_CAP)
    elif stage == "archive-replay":
        jobs = 2
    else:
        jobs = 1
    return {"stage": stage, "memory_max": memory_max, "standard_cap": cap,
            "floor": floor, "jobs": jobs, "admitted": memory_max >= floor}
