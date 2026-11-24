from pathlib import Path
import gzip
import json
import os
import sys
import tempfile

import buildsteps

work = Path("/home/linhao/Toolchain/development/llvm-optimize")
archive = work / "archive/task149-run/resume"
step = archive / "N2"
evidence = work.with_name("llvm-optimize-bolt")
sys.path.insert(0, str(evidence / "tools/skills/tizen-llvm-offline-profile/scripts"))
from build_jobs import require_rpm_log


def test_logs():
    with tempfile.TemporaryDirectory(dir=archive, prefix="n2-log-test-") as workspace:
        base = Path(workspace)
        for variant in ("chroot", "plain", "gzip", "missing", "ambiguous"):
            path = base / variant
            logs = path / "gbs-driver/local/repos/x86_64/logs/success/llvm"
            logs.mkdir(parents=True)
            scratch = path / "scratch"
            scratch.mkdir()
            content = b"[   1s] LLVM_BUILD_JOBS phase=configure compile=4 thinlto=4 link=1\n[   1s] + ninja -j 4\n"
            if variant == "chroot":
                (scratch / ".build.log").write_bytes(content)
            if variant in ("plain", "ambiguous"):
                (logs / "log.txt").write_bytes(content)
            if variant in ("gzip", "ambiguous"):
                (logs / "log.txt.gz").write_bytes(gzip.compress(content))
            if variant in ("missing", "ambiguous"):
                try:
                    buildsteps.archive_rpm_log(path, scratch)
                except RuntimeError as exc:
                    assert "expected one full RPM build log" in str(exc), str(exc)
                else:
                    raise AssertionError(f"{variant} RPM log unexpectedly accepted")
            else:
                archived = buildsteps.archive_rpm_log(path, scratch)
                assert archived.read_bytes() == content
                assert buildsteps.archive_rpm_log(path) == archived
                require_rpm_log(archived, (4, 4, 1))
            print(f"RPM log {variant}: PASS", flush=True)


def audit():
    counts = (4, 4, 1)
    log = buildsteps.archive_rpm_log(step)
    require_rpm_log(log, counts)
    rpms = sorted(step.joinpath("gbs-driver/local/repos").rglob("*.rpm"))
    assert len(rpms) == 23, f"expected 23 finished build RPMs, found {len(rpms)}"
    buildsteps.save(step / "rpm-identities.json", [buildsteps.receipt(rpm) for rpm in rpms])
    print(f"RPM inventory: {len(rpms)} files with SHA-256", flush=True)
    checks = buildsteps.n2_checks(work, step, rpms)
    dry_run = buildsteps.read(step / "dry-run.json")
    assert all(dry_run["checks"].values())
    actual = buildsteps.checked(buildsteps.GIT, "-C", step / "source", "rev-parse", "HEAD", "HEAD^{tree}").decode().splitlines()
    assert actual[0] == buildsteps.PS5, actual
    out = {
        "commit": actual[0],
        "source_tree": actual[1],
        "dry_run": dry_run,
        "parallelism": list(counts),
        "rpm_log": buildsteps.receipt(log),
        "validation": checks,
    }
    buildsteps.save(step / "validation.json", out)
    print(json.dumps(out, indent=2, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    test_logs()
    if sys.argv[1:] != ["--tests-only"]:
        audit()
