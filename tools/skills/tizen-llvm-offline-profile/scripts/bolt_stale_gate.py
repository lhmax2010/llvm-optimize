#!/usr/bin/env python3
"""Read complete BOLT rewrite logs and apply the packaging quality gate."""
import argparse
import json
from pathlib import Path
import re

from manifest import file_identity


class GateError(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise GateError(message)


def match_counts(text, argv, successful, trusted_tool):
    require(successful and trusted_tool, 'untrusted tool or incomplete/failed rewrite log')
    require(not any('infer-stale' in str(x) for x in argv), 'infer-stale forbidden')
    nrows = re.findall(r'^BOLT-INFO: (\d+) out of (\d+) functions in the binary .*have non-empty execution profile$', text, re.M)
    srows = re.findall(r'^BOLT-(?:WARNING|ERROR): (\d+) \([^\n]*\) functions? have invalid \(possibly stale\) profile\.', text, re.M)
    urows = re.findall(r'^BOLT-INFO: profile for (\d+) objects was ignored$', text, re.M)
    qrows = re.findall(r'^BOLT-INFO: (\d+) functions? with profile could not be optimized$', text, re.M)
    require('invalid (possibly stale) profile' not in text or bool(srows), 'malformed stale counter')
    require('objects was ignored' not in text or bool(urows), 'malformed unused counter')
    require('with profile could not be optimized' not in text or bool(qrows), 'malformed non-simple counter')
    require(len(nrows) == 1 and len(srows) <= 1 and len(urows) <= 1 and len(qrows) <= 1,
            'missing/duplicate profile counters')
    n, m = map(int, nrows[0]); s = int(srows[0]) if srows else 0
    u = int(urows[0]) if urows else 0; q = int(qrows[0]) if qrows else 0
    require(n > 0 and m >= n and s <= n, 'invalid N/M/S')
    # Absent optional zero-counter lines are allowed only for this authenticated success format.
    require(100 * (s + u) <= 5 * (n + u), 'profile R actual=%s expected=<=0.05; remedy: verify input identity, then retrain the profile or disable BOLT; never raise the threshold' % ((s+u)/(n+u)))
    require(100 * s <= 5 * n, 'profile S/N actual=%s expected=<=0.05; remedy: verify input identity, then retrain the profile or disable BOLT; never raise the threshold' % (s/n))
    return {'N': n, 'M': m, 'S': s, 'U': u, 'Q': q,
            'R': (s + u) / (n + u), 'S_over_N': s / n}


def audit_log(path, argv, successful, trusted_tool):
    text = Path(path).read_text(encoding="utf-8")
    require(text.endswith("\n") and "\x00" not in text, "truncated or invalid log transport")
    thresholds = [arg for arg in argv if arg.lstrip("-").split("=")[0] == "stale-threshold"]
    require(thresholds == ["-stale-threshold=5"], "exactly one -stale-threshold=5 is required")
    # Check the transport separately so an extra malformed line cannot be
    # hidden by a well-formed line for the same optional counter.
    formats = (
        ("have non-empty execution profile", r"^BOLT-INFO: \d+ out of \d+ functions in the binary .*have non-empty execution profile$"),
        ("invalid (possibly stale) profile", r"^BOLT-(?:WARNING|ERROR): \d+ \([^\n]*\) functions? have invalid \(possibly stale\) profile\."),
        ("objects was ignored", r"^BOLT-INFO: profile for \d+ objects was ignored$"),
        ("with profile could not be optimized", r"^BOLT-INFO: \d+ functions? with profile could not be optimized$"),
    )
    for hint, pattern in formats:
        for line in text.splitlines():
            # A stale-sample counter can contain the same phrase.
            if hint == "invalid (possibly stale) profile" and "samples in the binary" in line:
                continue
            if hint in line:
                require(re.match(pattern, line), "malformed profile counter line: " + line)
    return match_counts(text, argv, successful, trusted_tool)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--log", type=Path, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()
    try:
        receipt = json.loads(args.receipt.read_text(encoding="utf-8"))
        require(file_identity(args.log) == receipt["log_identity"], "rewrite log identity mismatch")
        result = audit_log(args.log, receipt["argv"], receipt["exit_code"] == 0,
                           receipt["trusted_tool"] is True)
        print(json.dumps(result, indent=2))
    except (GateError, OSError, KeyError, TypeError, ValueError) as error:
        parser.exit(1, f"STOP: {error}\n")


if __name__ == "__main__":
    main()
