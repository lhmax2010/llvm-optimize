#!/usr/bin/env python3
"""Resource-bounded, fail-closed GBS build of the workspace LLVM spec."""
import argparse
import configparser
import datetime as dt
import gzip
import hashlib
import json
import os
from pathlib import Path
import re
import shlex
import shutil
import signal
import subprocess as sp
import sys
import threading
import time
import urllib.parse
import urllib.request
import uuid
import xml.etree.ElementTree as ET

GIB = 1024 ** 3
MAX_BUILD_MEMORY_GIB = 18
BASELINE_PROFILE = Path(__file__).with_name('llvm_baseline_capacity.json')
HYBRID_PROFILE = Path(__file__).with_name('llvm_hybrid_trial_fingerprint.json')
ARCHIVE_PROFILE = Path(__file__).with_name('llvm_archive_fix_trial_fingerprint.json')
CONFIG_GATE_SECONDS = 900
WORKSPACE = Path(__file__).resolve().parents[1]
SPEC = Path("packaging/llvm.spec")
EXPECTED_HEAD = "f111162e94aa48ed367c9d2c039456c70e7160ae"
CONCURRENCY = {
    "ninja": r"(?m)^(%\{!\?mlgo_build_jobs: %define mlgo_build_jobs )\d+(\})$",
    "compile": r"(?m)^(\s*-DLLVM_PARALLEL_COMPILE_JOBS=)\d+(\s*\\)$",
    "link": r"(?m)^(\s*-DLLVM_PARALLEL_LINK_JOBS=)\d+(\s*\\)$",
}


def stamp():
    return dt.datetime.now().astimezone().isoformat(timespec="seconds")


def mem_available():
    for line in Path("/proc/meminfo").read_text().splitlines():
        if line.startswith("MemAvailable:"):
            return int(line.split()[1]) * 1024
    raise RuntimeError("MemAvailable is missing")


def normalized_spec(text):
    for pattern in CONCURRENCY.values():
        text = re.sub(pattern, lambda m: m[1] + "JOBS" + m[2], text)
    return text


def configuration_identity(head, spec, config, buildconf, *, repository_metadata=None, debuginfo_jobs=4):
    """Fingerprint actual recipe inputs; this is not a caller's 'baseline' label.

    The pinned recipe, source and repository macros determine CMake arguments.
    The cache contract is checked separately when configure actually runs.
    """
    jobs = {}
    for key, pattern in CONCURRENCY.items():
        match = re.search(pattern, spec)
        if match is None:
            raise RuntimeError('missing concurrency setting: ' + key)
        jobs[key+'_jobs'] = int(match[0][len(match[1]):-len(match[2])])
    return dict(source_head=head,
                normalized_spec_sha256=hashlib.sha256(normalized_spec(spec).encode()).hexdigest(),
                gbs_config_sha256=hashlib.sha256(config).hexdigest(),
                buildconf_sha256=hashlib.sha256(buildconf).hexdigest(),
                repository_metadata=repository_metadata or {},
                arch='x86_64', gbs_threads=1, debuginfo_jobs=debuginfo_jobs, **jobs)


def validate_resources(available, free_disk, cpus):
    if available < 16 * GIB:
        raise RuntimeError(f"MemAvailable {available / GIB:.3f} GiB < 16 GiB")
    if free_disk < 60 * GIB:
        raise RuntimeError(f"disk free {free_disk / GIB:.3f} GiB < 60 GiB")
    if cpus < 1:
        raise RuntimeError('nproc must be positive')


def resource_plan(available, free_disk, cpus, configuration, profile=None, *, certify_fingerprint=None):
    if certify_fingerprint is not None:
        profiles = {'hybrid-trial': HYBRID_PROFILE, 'archive-fix-trial': ARCHIVE_PROFILE}
        if certify_fingerprint not in profiles or profile is not None:
            raise RuntimeError('only explicitly pinned trial certifications are allowed')
        profile = json.loads(profiles[certify_fingerprint].read_text())
    else:
        profile = profile or json.loads(BASELINE_PROFILE.read_text())
    validate_resources(available, free_disk, cpus)
    expected = profile['configuration']
    differences = [key for key in sorted(set(expected) | set(configuration))
                   if configuration.get(key) != expected.get(key)]
    if differences:
        raise RuntimeError('capacity evidence does not cover this configuration: '+', '.join(differences)+
                           '; PGO/instrumentation and other unmeasured variants remain refused')
    # These phases succeeded under this cap. Their independent peaks are not additive.
    # Admission avoids an unsupported rebuild; the cgroup still protects the host if it fails.
    return dict(available_bytes=available, disk_free_bytes=free_disk, nproc=cpus,
                memory_max_gib=MAX_BUILD_MEMORY_GIB, gbs_threads=1, ninja_jobs=4,
                compile_jobs=4, link_jobs=1, debuginfo_jobs=4,
                admission=('CERTIFICATION_'+certify_fingerprint.upper().replace('-', '_'))
                          if certify_fingerprint else 'MEASURED_BASELINE',
                certify_fingerprint=certify_fingerprint, configuration=configuration,
                cmake_parameters=profile['cmake_parameters'], evidence=profile['evidence'])


def archive_trial_source_identity(source):
    """Accept only the certified spec/Source bytes in the dedicated worktree."""
    profile = json.loads(ARCHIVE_PROFILE.read_text())
    expected = profile['configuration']
    if source.resolve() != (WORKSPACE/'temp/llvm-archivefix-trial').resolve():
        raise RuntimeError('archive trial requires the isolated registered worktree')
    def git(*args):
        return sp.check_output(['git', '-C', str(source), *args])
    if git('rev-parse', 'HEAD').decode().strip() != expected['source_head']:
        raise RuntimeError('archive trial HEAD mismatch')
    branch = git('branch', '--show-current').decode().strip()
    if branch != 'archive-fix-trial':
        raise RuntimeError('archive trial branch mismatch')
    status = git('status', '--porcelain', '--untracked-files=all').decode().splitlines()
    required = {' M packaging/llvm.spec', ' A packaging/llvm-static-archives-native.py'}
    if set(status) != required:
        raise RuntimeError('archive trial changed/untracked inventory mismatch')
    files = {name: hashlib.sha256((source/name).read_bytes()).hexdigest() for name in expected['source_files']}
    diff = git('diff', '--no-ext-diff', '--binary', 'HEAD')
    patch = Path(profile['evidence']['patch_path']).read_bytes()
    if (files != expected['source_files'] or hashlib.sha256(diff).hexdigest() != expected['source_diff_sha256'] or
            hashlib.sha256(patch).hexdigest() != expected['packaging_patch_sha256']):
        raise RuntimeError('archive trial spec/Source/diff/patch differs from certified bytes')
    return {k: expected[k] for k in ('trial','source_branch','source_files','source_diff_sha256','packaging_patch_sha256')}


def archive_trial_root(root, session):
    """The sole allowed existing root contains only this session's live lock."""
    if root.resolve() != (WORKSPACE/'temp/gbs-root-x86_64-archivefix').resolve():
        raise RuntimeError('archive trial requires the registered fresh buildroot')
    lock = root/'.llvm-optimize-exclusive.lock'
    if not session or not root.is_dir() or set(root.iterdir()) != {lock}:
        raise RuntimeError('archive trial root must contain only the exclusive session lock')
    record = json.loads(lock.read_text())
    if record.get('session') != session or record.get('root') != str(root.resolve()):
        raise RuntimeError('archive trial exclusive lock ownership mismatch')
    try:
        os.kill(int(record['pid']), 0)
    except (ValueError, KeyError, OSError) as error:
        raise RuntimeError('archive trial lock holder is not alive') from error
    return record


def trial_source_identity(source, trial='hybrid-trial'):
    """Bind the trial to the exact approved seven-file diff; no general bypass."""
    if trial == 'archive-fix-trial':
        return archive_trial_source_identity(source)
    if trial != 'hybrid-trial':
        raise RuntimeError('unknown source certification')
    expected = json.loads(HYBRID_PROFILE.read_text())['configuration']
    if source.resolve() != (WORKSPACE/'temp/llvm-hybrid-trial').resolve():
        raise RuntimeError('hybrid trial requires the isolated temp/llvm-hybrid-trial worktree')
    def git(*args):
        return sp.check_output(['git', '-C', str(source), *args])
    branch = git('branch', '--show-current').decode().strip()
    if branch != 'hybrid-link-trial':
        raise RuntimeError('hybrid trial source branch mismatch')
    status = git('status', '--porcelain', '--untracked-files=all').decode().splitlines()
    if any(line[:3] != ' M ' for line in status) or {line[3:] for line in status} != set(expected['source_files']):
        raise RuntimeError('hybrid trial changed/untracked source inventory mismatch')
    files = {name: hashlib.sha256((source/name).read_bytes()).hexdigest() for name in expected['source_files']}
    diff = git('diff', '--no-ext-diff', '--binary', 'HEAD')
    if files != expected['source_files'] or hashlib.sha256(diff).hexdigest() != expected['source_diff_sha256']:
        raise RuntimeError('hybrid trial source differs from approved patch')
    return dict(trial='hybrid-trial', source_branch=branch, source_files=files,
                source_diff_sha256=hashlib.sha256(diff).hexdigest(),
                approved_design_commit=expected['approved_design_commit'])


def changed_concurrency(original, plan):
    result = original
    for key, value in (("ninja", plan["ninja_jobs"]),
                       ("compile", plan["compile_jobs"]), ("link", plan["link_jobs"])):
        result, count = re.subn(CONCURRENCY[key], lambda m: m[1] + str(value) + m[2], result)
        if count != 1:
            raise RuntimeError(f"expected exactly one concurrency setting: {key}, got {count}")
    return result


def only_concurrency_changed(original, modified):
    return normalized_spec(original) == normalized_spec(modified)


def validate_cache(text, expected_parameters=None, *, certify_fingerprint=None):
    if certify_fingerprint not in (None, 'hybrid-trial', 'archive-fix-trial'):
        raise ValueError('unknown CMake certification contract')
    values = {}
    for line in text.splitlines():
        match = re.match(r"([^/#][^:]*):[^=]+=(.*)$", line)
        if match:
            values[match[1]] = match[2]
    errors = []
    expected = dict(CMAKE_BUILD_TYPE="Release", LLVM_ENABLE_LTO="Thin", LLVM_USE_LINKER="lld")
    for key, value in expected.items():
        if values.get(key) != value:
            errors.append(f"{key}: expected {value}, found {values.get(key, 'MISSING')}")
    off_keys = ["LLVM_ENABLE_ASSERTIONS"]
    if certify_fingerprint == 'hybrid-trial':
        expected.update(LLVM_LINK_LLVM_DYLIB='ON', CLANG_LINK_CLANG_DYLIB='ON', TIZEN_HYBRID_LINK='ON')
        off_keys += ['LLVM_TOOL_LLVM_DRIVER_BUILD', 'BUILD_SHARED_LIBS']
        for key, value in expected.items():
            if values.get(key) != value:
                errors.append(f'{key}: expected {value}, found {values.get(key, "MISSING")}')
    else:
        off_keys += ["LLVM_LINK_LLVM_DYLIB", "CLANG_LINK_CLANG_DYLIB"]
    for key in off_keys:
        if values.get(key, "MISSING").upper() not in ("OFF", "NO", "FALSE", "0"):
            errors.append(f"{key}: expected OFF, found {values.get(key, 'MISSING')}")
    flags = shlex.split(values.get("CMAKE_CXX_FLAGS", ""))
    if "-O3" not in flags or "-Os" in flags:
        errors.append(f"CMAKE_CXX_FLAGS must contain -O3 and exclude -Os: {flags}")
    targets = set(values.get("LLVM_TARGETS_TO_BUILD", "").split(";"))
    if not {"X86", "ARM"} <= targets:
        errors.append(f"LLVM_TARGETS_TO_BUILD lacks X86/ARM: {sorted(targets)}")
    if expected_parameters is not None:
        for key, expected in expected_parameters.items():
            actual = values.get(key)
            # Both representations occurred in the original and resumed CMake caches.
            if key in ('CMAKE_C_COMPILER', 'CMAKE_CXX_COMPILER') and actual in (
                    '/bin/'+expected, '/usr/bin/'+expected):
                actual = expected
            if actual != expected:
                errors.append(f'baseline contract {key}: expected {expected!r}, found {actual!r}')
        # This option was absent in the baseline; an injected BOLT build is not covered.
        if values.get('LLVM_ENABLE_BOLT', 'OFF').upper() not in ('OFF', 'NO', 'FALSE', '0', ''):
            errors.append('baseline contract LLVM_ENABLE_BOLT must be absent/OFF')
    return values, errors


class Audit:
    def __init__(self, directory):
        self.directory = directory
        directory.mkdir(parents=True, exist_ok=False)
        self.stream = (directory / "commands.log").open("w", buffering=1)
        self.lock = threading.Lock()

    def log(self, text):
        with self.lock:
            message = f"{stamp()} {text}"
            print(message, flush=True)
            self.stream.write(message + "\n")

    def run(self, argv, *, check=True, timeout=60):
        self.log("$ " + shlex.join(map(str, argv)))
        result = sp.run(list(map(str, argv)), stdout=sp.PIPE, stderr=sp.STDOUT,
                        text=True, timeout=timeout)
        self.log(result.stdout.rstrip() + f"\n[exit={result.returncode}]")
        if check and result.returncode:
            raise RuntimeError(f"command failed: {shlex.join(map(str, argv))}")
        return result

    def json(self, name, data):
        (self.directory / name).write_text(json.dumps(data, indent=2) + "\n")


def fetch(audit, url, filename):
    audit.log("GET " + url)
    with urllib.request.urlopen(url, timeout=60) as response:
        data = response.read()
        audit.log(f"HTTP {response.status}; final URL {response.url}; bytes {len(data)}; "
                  f"sha256 {hashlib.sha256(data).hexdigest()}")
    (audit.directory / filename).write_bytes(data)
    return data


def repositories(audit, config_path):
    # Same duplicate-option semantics as GBS BrainConfigParser(strict=False).
    config = configparser.ConfigParser(strict=False)
    config.read(config_path)
    profile = config["general"]["profile"]
    if config[profile].get("buildconf"):
        raise RuntimeError("explicit profile buildconf requires a separate audit; refusing implicit override")
    chosen = None
    problems = []
    summary = []
    for name in config[profile]["repos"].split(","):
        name = name.strip()
        base = config[name]["url"].rstrip("/") + "/"
        try:
            data = fetch(audit, base + "repodata/repomd.xml", name + ".repomd.xml")
            root = ET.fromstring(data)
            result = dict(name=name, url=base, x86_64_packages=0)
            for entry in root:
                kind = entry.get("type")
                if kind not in ("primary", "build"):
                    continue
                href = entry.find("{*}location").get("href")
                data = fetch(audit, urllib.parse.urljoin(base, href), name + "." + kind + ".data")
                checksum = entry.find("{*}checksum")
                if checksum is None or hashlib.new(checksum.get("type"), data).hexdigest() != checksum.text:
                    raise RuntimeError("repodata checksum mismatch or missing checksum")
                decoded = gzip.decompress(data) if data[:2] == b"\x1f\x8b" else data
                if kind == "primary":
                    pkgs = [p for p in ET.fromstring(decoded) if p.findtext("{*}arch") == "x86_64"]
                    result["x86_64_packages"] = len(pkgs)
                    result["package_names"] = sorted(p.findtext("{*}name") for p in pkgs)
                else:
                    chosen = audit.directory / "buildconfig.conf"
                    chosen.write_bytes(decoded)
                    (audit.directory / (name + ".build.conf")).write_bytes(decoded)
                    result["buildconf_sha256"] = hashlib.sha256(decoded).hexdigest()
            if not result["x86_64_packages"]:
                problems.append(name + ": no x86_64 packages")
            summary.append(result)
        except Exception as error:
            problems.append(f"{name}: {error}")
            audit.log("REPOSITORY BLOCKER " + problems[-1])
    audit.json("repositories.json", summary)
    if chosen:
        # RepoParser replaces the selected buildconf as later standard repositories are read.
        raw = audit.run(["/usr/lib/build/queryconfig", "--dist", chosen,
                         "--archpath", "x86_64", "rawmacros"]).stdout
        macro_file = audit.directory / "x86_64.rpmmacros"
        macro_file.write_text(raw)
        value = audit.run(["rpm", "--macros", f"/usr/lib/rpm/macros:{macro_file}",
                           "--eval", "%{defined _toolchain}|%{_toolchain}"]).stdout.strip()
        if value != "1|clang":
            problems.append(f"_toolchain must be defined and select clang; found {value!r}; no --define workaround")
        # The x86_64 spec supplies the MLGO jobs default; reject a repository override.
        if re.search(r"(?m)^%mlgo_build_jobs\s", raw):
            problems.append("repository overrides mlgo_build_jobs; concurrency requires review")
    else:
        problems.append("no build configuration available; _toolchain UNKNOWN")
    if problems:
        raise RuntimeError("preflight blocked: " + "; ".join(problems))
    return chosen


def process_tree(root_pid):
    rows = {}
    for item in Path("/proc").iterdir():
        if not item.name.isdigit():
            continue
        try:
            fields = (item / "stat").read_text().rsplit(")", 1)[1].split()
            rows[int(item.name)] = (int(fields[1]), int(fields[21]) * os.sysconf("SC_PAGE_SIZE"))
        except (OSError, ValueError, IndexError):
            continue
    selected = {root_pid}
    while True:
        expanded = selected | {pid for pid, (parent, _) in rows.items() if parent in selected}
        if expanded == selected:
            break
        selected = expanded
    return {pid: rows[pid][1] for pid in selected if pid in rows}


def cgroup_stats(unit):
    if not unit:
        return {}
    result = sp.run(["systemctl", "--user", "show", unit, "-p", "ControlGroup", "-p",
                     "MemoryCurrent", "-p", "MemoryPeak", "-p", "MemoryMax"],
                    stdout=sp.PIPE, stderr=sp.DEVNULL, text=True, timeout=10)
    values = dict(line.split("=", 1) for line in result.stdout.splitlines() if "=" in line)
    if not values.get("ControlGroup"):
        return values
    path = Path("/sys/fs/cgroup") / values["ControlGroup"].lstrip("/")
    for name in ("memory.events", "memory.peak", "memory.stat", "cpu.stat", "cgroup.events"):
        try:
            values[name] = (path / name).read_text().strip()
        except OSError:
            pass
    return values


def oom_kills(stats):
    events = dict(line.split() for line in stats.get('memory.events', '').splitlines() if len(line.split()) == 2)
    return int(events.get('oom_kill', 0))


def stop_build(audit, child, unit):
    if unit:
        audit.run(["systemctl", "--user", "kill", "--kill-whom=all", "--signal=SIGKILL", unit], check=False)
    else:
        pids = process_tree(child.pid)
        for pid in sorted(pids, reverse=True):
            try:
                os.kill(pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            except PermissionError:
                audit.log(f"ERROR cannot signal descendant {pid}; privileged process may remain")
    if child.poll() is None:
        try:
            os.killpg(child.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
    child.wait(timeout=30)


def linker_output(argv, parent_argv):
    """The linker can hide -o in a response file; its clang parent still names it."""
    for source, words in (('linker_argv', argv), ('parent_driver_argv', parent_argv)):
        if '-o' in words and words.index('-o') + 1 < len(words):
            return words[words.index('-o') + 1], source
    return None, 'UNKNOWN'


def build(audit, args, plan, chosen, mechanism, *, command=None, input_text=None,
          completion_file=None, release_file=None, cache_check=True):
    if not cache_check and command is None:
        raise ValueError('default GBS builds must retain the CMake gate')
    unit = "llvm-baseline-" + uuid.uuid4().hex + ".scope" if mechanism == "systemd" else None
    if command is None:
        command = ["gbs", "-c", str(args.config), "build", "-A", "x86_64", "-B", str(args.buildroot),
                   "--threads", "1", "--include-all", "--define", "_smp_mflags -j4",
                   "-D", str(chosen), str(args.source)]
        if plan.get('certify_fingerprint'):
            completion_file = audit.directory/'gbs.exit'
            release_file = audit.directory/'gbs.release'
            # Preserve kernel peak/events before the scope disappears, including failed GBS.
            hold = ('import subprocess,sys,time\nfrom pathlib import Path\n'
                    'rc=subprocess.run(sys.argv[3:]).returncode\n'
                    'Path(sys.argv[1]).write_text(str(rc))\n'
                    'deadline=time.monotonic()+60\n'
                    'while not Path(sys.argv[2]).exists() and time.monotonic()<deadline: time.sleep(.1)\n'
                    'sys.exit(rc if rc else (0 if Path(sys.argv[2]).exists() else 125))\n')
            command = [sys.executable, '-c', hold, str(completion_file), str(release_file)] + command
    command = ["nice", "-n", "15", "ionice", "-c3"] + command
    if unit:
        command = ["systemd-run", "--user", "--scope", "--unit=" + unit, "-p",
                   f"MemoryMax={plan['memory_max_gib']}G", "-p", "MemorySwapMax=0"] + command
    else:
        cap = plan["memory_max_gib"] * GIB
        command = ["prlimit", f"--as={cap}:{cap}", "--"] + command
    command = ["/usr/bin/time", "-v", "-o", str(audit.directory / "time-v.txt")] + command
    audit.log("BUILD COMMAND (before execution): " + shlex.join(command))
    audit.json("launch.json", dict(command=command, unit=unit, mechanism=mechanism, plan=plan))
    stop = threading.Event()
    problem = []
    verified = {}
    start = time.monotonic()
    child = sp.Popen(command, stdin=sp.PIPE if input_text is not None else sp.DEVNULL,
                     stdout=sp.PIPE, stderr=sp.STDOUT, text=True,
                     errors="replace", bufsize=1, start_new_session=True)

    def output():
        with (audit.directory / "build.log").open("w", buffering=1) as log:
            for line in child.stdout:
                log.write(stamp() + " " + line)

    def monitor():
        try:
            next_sample = 0.0
            cache_seen = None
            completion_captured = False
            with (audit.directory / "samples.jsonl").open("w", buffering=1) as samples, \
                 (audit.directory / "process-memory.jsonl").open("w", buffering=1) as memory, \
                 (audit.directory / "linker-memory-observations.jsonl").open("w", buffering=1) as links:
                while not stop.is_set():
                    now = time.monotonic()
                    available = mem_available()
                    if available < 2 * GIB:
                        raise RuntimeError(f"MemAvailable {available} < 2 GiB: emergency stop")
                    tree = process_tree(child.pid)
                    rows = []
                    for pid in tree:
                        try:
                            proc = Path("/proc") / str(pid)
                            argv = (proc / "cmdline").read_bytes().decode(errors="replace").rstrip("\0").split("\0")
                            info = dict(line.split(":", 1) for line in (proc / "status").read_text().splitlines() if ":" in line)
                            rows.append(dict(pid=pid, argv=argv, info={key: info.get(key, "").strip()
                                for key in ("Name", "VmRSS", "VmHWM", "Threads")}))
                            if Path(argv[0]).name in ('ld.lld', 'lld'):
                                parent_argv = []
                                if '-o' not in argv:
                                    parent = Path('/proc') / info['PPid'].strip()
                                    parent_argv = (parent/'cmdline').read_bytes().decode(errors='replace').rstrip('\0').split('\0')
                                target, target_source = linker_output(argv, parent_argv)
                                if target is None:
                                    continue
                                output_path = proc/'root'/target.lstrip('/') if target.startswith('/') else proc/'cwd'/target
                                links.write(json.dumps(dict(timestamp=stamp(), elapsed=now-start, pid=pid,
                                    argv=argv, parent_argv=parent_argv, target=target, target_source=target_source, cwd=os.readlink(proc/'cwd'),
                                    vmhwm=info.get('VmHWM','').strip(), rss=info.get('VmRSS','').strip(),
                                    output_bytes=output_path.stat().st_size if output_path.exists() else None))+'\n')
                        except (OSError, ValueError):
                            continue
                    memory.write(json.dumps(dict(timestamp=stamp(), elapsed=now-start, rows=rows)) + "\n")
                    if release_file is not None and completion_file.exists() and not completion_captured:
                        # RPM has finished. Keep its shell alive until cumulative kernel counters are saved.
                        final_scope = cgroup_stats(unit)
                        audit.json("scope-after-rpm.json", final_scope)
                        if unit:
                            result = audit.run(["systemctl", "--user", "show", unit, "-p", "Result", "-p",
                                "MemoryPeak", "-p", "MemoryMax", "-p", "MemorySwapMax", "-p",
                                "CPUUsageNSec", "-p", "ActiveState"], check=False)
                            (audit.directory / "scope-after-rpm.log").write_text(result.stdout)
                        release_file.write_text(stamp() + "\n")
                        completion_captured = True
                        if oom_kills(final_scope):
                            raise RuntimeError('cgroup recorded an OOM kill; shell completion status is not sufficient')
                    if not unit and sum(tree.values()) > plan["memory_max_gib"] * GIB:
                        raise RuntimeError("aggregate process-tree RSS exceeds fallback budget")
                    if now >= next_sample:
                        sample = dict(timestamp=stamp(), elapsed=now-start, available_bytes=available,
                                      loadavg=Path("/proc/loadavg").read_text().strip(),
                                      process_tree_rss_bytes=sum(tree.values()), processes=tree,
                                      cgroup=cgroup_stats(unit),
                                      disk_free_bytes=shutil.disk_usage(args.buildroot.parent).free,
                                      free_m=sp.check_output(["free", "-m"], text=True))
                        samples.write(json.dumps(sample) + "\n")
                        next_sample = now + 30
                    if not cache_check:
                        stop.wait(2)
                        continue
                    if not verified and now - start >= CONFIG_GATE_SECONDS:
                        raise RuntimeError("no validated CMakeCache within 15 minutes")
                    # Also revalidate a copied cache whenever CMake rewrites it during a resume.
                    for cache in args.buildroot.glob("local/BUILD-ROOTS/*/home/abuild/rpmbuild/BUILD/llvm-*/build/CMakeCache.txt"):
                        signature = (str(cache), cache.stat().st_mtime_ns, cache.stat().st_size)
                        if signature == cache_seen:
                            continue
                        text = cache.read_text()
                        shutil.copy2(cache, audit.directory / "CMakeCache.txt")
                        values, errors = validate_cache(text, plan.get('cmake_parameters'),
                                                        certify_fingerprint=plan.get('certify_fingerprint'))
                        for key, value in (("LLVM_PARALLEL_COMPILE_JOBS", plan["compile_jobs"]),
                                           ("LLVM_PARALLEL_LINK_JOBS", plan["link_jobs"])):
                            if values.get(key) != str(value):
                                errors.append(f"{key} must be {value}, found {values.get(key)}")
                        audit.json("cache-gate.json", dict(path=str(cache), elapsed=now-start,
                                                         values=values, errors=errors))
                        if errors:
                            raise RuntimeError("CMake gate failed: " + "; ".join(errors))
                        verified.update(values)
                        cache_seen = signature
                        audit.log(f"CMAKE GATE PASS at {now-start:.1f}s: {cache}")
                        break
                    stop.wait(2)
        except Exception as error:
            problem.append(str(error))
            audit.log("BUILD ABORT: " + str(error))

    reader = threading.Thread(target=output, name="build-log", daemon=False)
    sampler = threading.Thread(target=monitor, name="build-sampler", daemon=False)
    reader.start()
    sampler.start()
    interrupted = None
    try:
        if input_text is not None:
            audit.log("CHROOT INPUT:\n" + input_text)
            child.stdin.write(input_text)
            child.stdin.close()
        while True:
            if problem:
                stop_build(audit, child, unit)
                return_code = child.returncode
                break
            try:
                return_code = child.wait(timeout=0.5)
                break
            except sp.TimeoutExpired:
                continue
    except BaseException as error:
        interrupted = error
        stop_build(audit, child, unit)
        return_code = child.returncode
    finally:
        stop.set()
        sampler.join()
        if child.poll() is None:
            stop_build(audit, child, unit)
        reader.join(timeout=30)
        if reader.is_alive():
            stop_build(audit, child, unit)
            reader.join(timeout=30)
        if not reader.is_alive():
            child.stdout.close()
        if child.stdin is not None and not child.stdin.closed:
            child.stdin.close()
        command_exit_code = None
        if completion_file is not None:
            try:
                command_exit_code = int(completion_file.read_text().strip())
                if command_exit_code:
                    problem.append(f"chroot command exit status: {command_exit_code}")
            except (OSError, ValueError) as error:
                problem.append(f"missing/invalid chroot completion status: {error}")
        audit.json("outcome.json", dict(exit_code=child.returncode, elapsed_seconds=time.monotonic()-start,
                                       command_exit_code=command_exit_code,
                                       cache_passed=bool(verified) if cache_check else None, problems=problem,
                                       sampler_reaped=not sampler.is_alive(), log_reader_reaped=not reader.is_alive(),
                                       interrupted=repr(interrupted) if interrupted else None))
    if interrupted:
        raise interrupted
    if return_code or problem or (cache_check and not verified):
        raise RuntimeError(f"build failed/stopped: exit={return_code}, cache_passed={bool(verified)}, {problem}")
    audit.log("BUILD COMMAND COMPLETE; RPMs still require verify_toolchain.sh and benchmark calibration"
              if cache_check else "EXPERIMENT COMMAND COMPLETE; CMake validation is a separate explicit step")


def main():
    parser = argparse.ArgumentParser(description=__doc__, epilog="Never overrides _toolchain; debuginfo uses -j4. Default: preflight only. "
        "--run may edit ONLY the three spec concurrency numbers, leaves the diff for review, and requires a new root. "
        "Logs stay in temp/. Interrupted/failed build roots are preserved, never deleted automatically.")
    parser.add_argument("--run", action="store_true", help="start GBS only after all preflight gates pass")
    parser.add_argument("--config", type=Path, default=WORKSPACE / "gbs_llvm.conf")
    parser.add_argument("--source", type=Path, default=WORKSPACE / "llvm")
    parser.add_argument("--expected-commit", default=EXPECTED_HEAD)
    parser.add_argument('--certify-fingerprint', choices=['hybrid-trial','archive-fix-trial'],
                        help='one exact pinned local trial; never widens baseline admission')
    parser.add_argument('--exclusive-lock-session', help='archive trial only: existing live exclusive lock session')
    parser.add_argument("--buildroot", type=Path, default=WORKSPACE / "temp/gbs-root-x86_64-baseline")
    parser.add_argument("--log-dir", type=Path, default=WORKSPACE / "temp/baseline-build" / dt.datetime.now().strftime("%Y%m%d-%H%M%S-%f"))
    args = parser.parse_args()
    for name in ("config", "source", "buildroot", "log_dir"):
        setattr(args, name, getattr(args, name).resolve())
    audit = Audit(args.log_dir)
    try:
        for command in (["nproc"], ["free", "-g"], ["df", "-h", args.buildroot.parent]):
            audit.run(command)
        cpus = int(audit.run(["nproc"]).stdout)
        validate_resources(mem_available(), shutil.disk_usage(args.buildroot.parent).free, cpus)
        head = audit.run(["git", "-C", args.source, "rev-parse", "HEAD"]).stdout.strip()
        if head != args.expected_commit:
            raise RuntimeError(f"source HEAD {head} differs from expected {args.expected_commit}")
        original = audit.run(["git", "-C", args.source, "show", "HEAD:" + str(SPEC)]).stdout
        current = (args.source / SPEC).read_text()
        status = audit.run(["git", "-C", args.source, "status", "--porcelain", "--untracked-files=all"]).stdout
        if args.certify_fingerprint:
            trial_source_identity(args.source, args.certify_fingerprint)
            if args.certify_fingerprint == 'archive-fix-trial':
                audit.json('exclusive-lock.json', archive_trial_root(args.buildroot, args.exclusive_lock_session))
            elif args.buildroot != WORKSPACE/'temp/gbs-root-x86_64-hybrid-trial':
                raise RuntimeError('hybrid trial requires the registered fresh buildroot')
        elif any(line[3:] != str(SPEC) for line in status.splitlines()) or not only_concurrency_changed(original, current):
            raise RuntimeError("source has changes beyond the permitted spec concurrency numbers")
        if args.buildroot.exists() and args.certify_fingerprint != 'archive-fix-trial':
            raise RuntimeError("fresh buildroot required: path already exists; preserve it and choose a new path")
        chosen = repositories(audit, args.config)
        metadata = {row['name']: hashlib.sha256((audit.directory/(row['name']+'.repomd.xml')).read_bytes()).hexdigest()
                    for row in json.loads((audit.directory/'repositories.json').read_text())}
        proposed = changed_concurrency(current, dict(ninja_jobs=4, compile_jobs=4, link_jobs=1))
        configuration = configuration_identity(head, proposed, args.config.read_bytes(), chosen.read_bytes(),
                                               repository_metadata=metadata)
        if args.certify_fingerprint:
            configuration.update(trial_source_identity(args.source, args.certify_fingerprint))
        plan = resource_plan(mem_available(), shutil.disk_usage(args.buildroot.parent).free,
                             cpus, configuration, certify_fingerprint=args.certify_fingerprint)
        audit.json("resource-plan.json", plan)
        audit.log('CAPACITY ADMISSION '+plan['admission']+'; 18 GiB cap, 4/4/1, debuginfo -j4')
        probe = audit.run(["systemd-run", "--user", "--scope", "-p", "MemoryMax=1G", "-p",
                           "MemorySwapMax=0", "/bin/true"], check=False)
        mechanism = "systemd" if probe.returncode == 0 else "prlimit"
        audit.log("MEMORY MECHANISM " + mechanism)
        if mechanism == "prlimit":
            raise RuntimeError('measured admission requires the same aggregate systemd cgroup limit; '
                               'per-process prlimit is not equivalent evidence')
        if not args.run:
            audit.log("PREFLIGHT PASS; no spec edit and no build. Use --run to proceed.")
            return 0
        # Re-check resource thresholds immediately before mutation and launch.
        current = (args.source / SPEC).read_text()
        proposed = changed_concurrency(current, dict(ninja_jobs=4, compile_jobs=4, link_jobs=1))
        configuration = configuration_identity(head, proposed, args.config.read_bytes(), chosen.read_bytes(),
                                               repository_metadata=metadata)
        if args.certify_fingerprint:
            configuration.update(trial_source_identity(args.source, args.certify_fingerprint))
        plan = resource_plan(mem_available(), shutil.disk_usage(args.buildroot.parent).free,
                             cpus, configuration, certify_fingerprint=args.certify_fingerprint)
        audit.json("resource-plan.json", plan)
        patched = changed_concurrency(current, plan)
        if args.certify_fingerprint:
            if patched != current:
                raise RuntimeError('certified trial concurrency must already be exact; refusing source mutation')
            trial_source_identity(args.source, args.certify_fingerprint)
            if args.certify_fingerprint == 'archive-fix-trial':
                archive_trial_root(args.buildroot, args.exclusive_lock_session)
            audit.json('source-fingerprint.json', configuration)
            (audit.directory/'source.diff').write_bytes(sp.check_output(
                ['git','-C',str(args.source),'diff','--no-ext-diff','--binary','HEAD']))
        else:
            assert only_concurrency_changed(original, patched)
            (args.source / SPEC).write_text(patched)
        diff = audit.run(["git", "-C", args.source, "diff", "HEAD", "--", SPEC]).stdout
        (audit.directory / "spec-concurrency.diff").write_text(diff)
        build(audit, args, plan, chosen, mechanism)
        return 0
    except (Exception, KeyboardInterrupt) as error:
        audit.log("STOPPED " + str(error))
        audit.json("stopped.json", dict(reason=str(error), time=stamp()))
        return 2
    finally:
        audit.stream.close()


if __name__ == "__main__":
    def signal_stop(signum, _frame):
        raise KeyboardInterrupt(f"signal {signum}")
    for signum in (signal.SIGTERM, signal.SIGINT, signal.SIGHUP, signal.SIGQUIT):
        signal.signal(signum, signal_stop)
    sys.exit(main())
