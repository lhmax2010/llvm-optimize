"""Read the task 158 corpus handoff before launching a full build."""
import json

TERMINAL = {"PASS", "PARTIAL", "SKIPPED", "FAIL", "BUDGET_EXPIRED"}


def corpus_terminal(marker):
    try:
        status = json.loads(marker.read_text())
    except (OSError, ValueError):
        return None, "waiting for the task 158 corpus handoff"
    if status.get("status") not in TERMINAL or status.get("package_build_active") is not False:
        return None, "task 158 corpus work or its package build has not finished"
    return status, ""
