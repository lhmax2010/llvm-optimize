"""39's export/prep/build argv and controller, with the established 37 driver layout.

Only the rehearsal monitor stops at CMake. No source, spec or toolchain edits.
Full mode starts a new root and completes GBS packaging; qualification is a
separate, mandatory next phase, never inferred from a successful GBS exit.
"""
from pathlib import Path
import datetime
import fcntl
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
import traceback

B = Path('/home/linhao/Toolchain/development/llvm-optimize-bolt')
W = B.parent / 'llvm-optimize'
T = Path(__file__).resolve().parent
OLD = B / 'tools/bolt/results/oldtext-final-20261027'
SOURCE = W / 'temp/rebase-359934-20261106/source'
COMMIT = os.environ.get('NIGHT_SOURCE_SHA', '')
assert len(COMMIT) == 40 and all(c in '0123456789abcdef' for c in COMMIT), 'explicit full source SHA required'
PROJECT = os.environ.get('FINAL_PROJECT', 'toolchain')
assert PROJECT in ('toolchain', 'basedev')
CONFIG = W / ('temp/final-20261103/configs/' + PROJECT + '/gbs.conf')
BUILDCONF = CONFIG.parent / 'build.conf'
BUILD_SHA = {'toolchain':'e5187fd758a663eec273a434090aaab9f8e32f80a036e3bca2cf0352dd286945',
             'basedev':'8ace286a5f98f2e02a79be275a64c22a86ea2b0034174c1e293381e181ce3f6a'}[PROJECT]
LOCK = W.parent / 'heavy-stage.lock'


def save(p, value):
    p.write_text(json.dumps(value, indent=2) + '\n')


def digest(p):
    with p.open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


def check_source():
    rev = subprocess.check_output(['git', '-C', str(SOURCE), 'rev-parse', 'HEAD', 'HEAD^{tree}'], text=True).splitlines()
    status = subprocess.check_output(['git', '-C', str(SOURCE), 'status', '--porcelain', '--untracked-files=no'], text=True)
    assert rev[0] == COMMIT and not status, (rev, status)
    assert digest(BUILDCONF) == BUILD_SHA, 'build.conf changed'
    for name, row in json.loads((T / 'provenance.json').read_text())['templates'].items():
        assert digest(Path(row['path'])) == row['sha256'], name + ' historical template changed'
    return {'commit': rev[0], 'tree': rev[1], 'status': status, 'buildconf_sha256': BUILD_SHA}


def properties(plan):
    return ['-p', 'MemoryMax=' + str(plan['MemoryMax_bytes']), '-p', 'MemorySwapMax=0',
            '-p', 'CPUQuota=1200%', '-p', 'Nice=10', '-p', 'IOSchedulingClass=best-effort',
            '-p', 'IOSchedulingPriority=7', '-p', 'OOMPolicy=stop', '-p', 'KillMode=control-group',
            '-p', 'TimeoutStopSec=120']


def stage(D, name, argv):
    E = D / 'evidence'
    save(E / (name + '-command.json'), argv)
    start = time.time_ns()
    with (E / (name + '.stdout')).open('wb') as o, (E / (name + '.stderr')).open('wb') as e:
        r = subprocess.run(argv, stdout=o, stderr=e)
    save(E / (name + '-stage.json'), {'rc': r.returncode, 'start_ns': start, 'end_ns': time.time_ns()})
    if r.returncode:
        raise RuntimeError(name + ' failed, rc=' + str(r.returncode))
    return r.returncode


def materialize(D, plan):
    E = D / 'evidence'
    old_e = str(OLD)
    for name in ('prep.py', 'run.py', 'build-runner.py'):
        text = (OLD / name).read_text()
        text = text.replace(old_e, str(E))
        text = text.replace("W=D.parent.parent;E=W.parent/'llvm-optimize-bolt/tools/bolt/results/oldtext-final-20261027'",
                            "W=Path(" + repr(str(W)) + ");E=D/'evidence'")
        text = text.replace("unit='oldtext-final-prep-20261027'", "unit=" + repr(plan['prep_unit']))
        text = text.replace("unit='oldtext-final-20261027.service'", "unit=" + repr(plan['build_unit']))
        text = text.replace("'-p','MemorySwapMax=0',", "'-p','MemorySwapMax=0','-p','CPUQuota=1200%',")
        if name == 'run.py':
            text = text.replace("G=D/'gbs-root'", "G=D/'gbs-driver'")
            # 348 tests / five RPM parses already certified against this exact source.
            text = text.replace("assert all(r['PASS'] for r in json.loads((E/'five-parse/matrix.json').read_text()))",
                                "assert plan['commit']=='" + COMMIT + "'")
            text = text.replace("import fcntl,json,os,shutil,subprocess,threading,time", "import fcntl,json,os,shutil,subprocess,threading,time,re")
            # Poll the build log before CMake can finish and reach the package's ninja.
            text = text.replace("while not stop.wait(2):\n  p=R/'.build.log'",
                                "while not stop.wait(.02 if plan['mode']=='rehearsal' else 2):\n  p=R/'.build.log'")
            text = text.replace(" position=0\n", " position=0;anchor=b''\n")
            text = text.replace("    src.seek(position);b=src.read();position+=len(b)",
                                "    src.seek(max(0,position-len(anchor)))\n"
                                "    if src.read(len(anchor))!=anchor or p.stat().st_size<position:\n"
                                "     append('log-restarts.jsonl',{'time_ns':time.time_ns(),'old_position':position});position=0\n"
                                "    src.seek(position);b=src.read();position+=len(b)\n"
                                "    src.seek(max(0,position-128));anchor=src.read(min(position,128))")
            marker = "    if b'BOLT_GATE_FAILED:' in b and reason is None:"
            guard = """    if plan['mode']=='rehearsal' and re.search(rb'\\+ cmake -G Ninja(?: |\\n)',b) and reason is None:
     reason='rehearsal-CMake-start'
     append('cmake-stop.jsonl',{'time_ns':time.time_ns(),'log':str(p),'chunk':b.decode(errors='replace')})
     result=subprocess.run(['systemctl','--user','stop',unit],capture_output=True,text=True)
     append('cmake-stop.jsonl',{'stop_rc':result.returncode,'stdout':result.stdout,'stderr':result.stderr,'time_ns':time.time_ns()})
     shutil.copyfile(p,E/'rpm-build-final.log')
     shutil.copyfile(p,E/'rpm-build.log')
     return
"""
            assert marker in text
            text = text.replace(marker, guard + marker)
        if name == 'run.py':
            text = text.replace("if file.exists() and reason is None:", "if False and file.exists() and reason is None:")
            needle = "    with (E/'rpm-build.log').open('ab') as out:out.write(b)"
            addition = """
    for ln in b.decode(errors='replace').splitlines():
     if '+ echo ' in ln or '+ printf ' in ln:continue
     for phase,phase_anchor in [('ordinary-build','Executing(%build)'),('ordinary-install','Executing(%install)'),('BOLT','BOLT_DISK_REPORT'),('cache-release',' cache-release '),('cache-release','BOLT_CACHE_RELEASE removed'),('archive-conversion','NATIVE_ARCHIVES_BEGIN'),('platform-post','find-debuginfo'),('packaging','Processing files:')]:
      if phase_anchor in ln:append('phase-events.jsonl',{'time_ns':time.time_ns(),'phase':phase,'text':ln})
     if 'BOLT_COMPARE_ROOT_PASS' in ln:append('phase-events.jsonl',{'time_ns':time.time_ns(),'phase':'BOLT','kind':'end','text':ln})
"""
            assert needle in text
            text = text.replace(needle,needle+addition)
        (D / name).write_text(text)
        compile(text, str(D / name), 'exec')
    # Use exactly 39's export invocation, substituting only commit/source/output.
    export = json.loads((OLD / 'export-result.json').read_text())['argv']
    export = [COMMIT if x == 'f308fe08eeaad4e219f8505449b88bd5f644ea8c' else
              str(D / 'export') if x.endswith('/oldtext-final-20261027/export') else
              str(SOURCE) if x.endswith('/oldtext-final-20261027/source') else x for x in export]
    export[export.index('-c') + 1] = str(CONFIG)
    save(D / 'export-command.json', export)


def final_audit(D, plan):
    E = D / 'evidence'
    result = {'source': check_source()}
    for name, argv in [('services', ['systemctl', '--user', 'show', plan['prep_unit'], plan['build_unit'],
                                     '-p', 'Id', '-p', 'ActiveState', '-p', 'SubState', '-p', 'Result', '-p', 'ControlGroup']),
                       ('mounts', ['findmnt', '-rn', '-o', 'TARGET,SOURCE,FSTYPE'])]:
        r = subprocess.run(argv, capture_output=True, text=True)
        text = r.stdout
        if name == 'mounts':
            text = '\n'.join(l for l in text.splitlines() if str(D) + '/' in l)
        result[name] = {'rc': r.returncode, 'stdout': text, 'stderr': r.stderr}
    procs = []
    for p in Path('/proc').iterdir():
        if not p.name.isdigit() or int(p.name) == os.getpid():
            continue
        try:
            cg = (p / 'cgroup').read_text()
            if any('/' + unit in cg for unit in (plan['prep_unit'], plan['build_unit'])):
                procs.append({'pid': int(p.name), 'cgroup': cg, 'argv': (p / 'cmdline').read_bytes().replace(b'\0', b' ').decode(errors='replace')})
        except (PermissionError, FileNotFoundError, ProcessLookupError):
            pass
    result['remaining_build_processes'] = procs
    save(E / 'final-audit.json', result)
    return result


def cleanup_mounts(D, label):
    """After our service has ended, ordinary umount of only our scratch root.

    Stopping the whole service left mounts in attempt 01. Use the physical
    root; never use --kill, --clean, force or lazy unmount. Do not assume the
    build program's exit cleanup completed when its process group terminated.
    """
    R = D / 'gbs-root/local/BUILD-ROOTS/scratch.x86_64.0'
    E = D / 'evidence'
    rows = []
    mounts = subprocess.check_output(['findmnt', '-rn', '-o', 'TARGET'], text=True).splitlines()
    if str(R / 'proc') in mounts:
        code = """import os,json
root=os.stat('/')
rows=[]
for pid in os.listdir('/proc'):
 if not pid.isdigit() or int(pid)==os.getpid(): continue
 try:
  s=os.stat('/proc/'+pid+'/root')
  if (s.st_dev,s.st_ino)==(root.st_dev,root.st_ino):
   rows.append({'pid':int(pid),'argv':open('/proc/'+pid+'/cmdline','rb').read().replace(b'\\0',b' ').decode(errors='replace')})
 except (FileNotFoundError,ProcessLookupError,PermissionError): pass
print(json.dumps(rows))
"""
        argv = ['sudo', '-n', '/usr/sbin/chroot', str(R), '/usr/bin/python3', '-B', '-c', code]
        r = subprocess.run(argv, capture_output=True, text=True)
        save(E / (label + '-root-processes.json'), dict(argv=argv, rc=r.returncode, stdout=r.stdout, stderr=r.stderr))
        assert r.returncode == 0 and json.loads(r.stdout) == [], 'scratch root still has processes'
    for _ in range(20):
        mounts = subprocess.check_output(['findmnt', '-rn', '-o', 'TARGET'], text=True).splitlines()
        ours = [m for m in mounts if m.startswith(str(R) + '/')]
        if not ours:
            break
        target = sorted(ours, key=lambda s: (s.count('/'), len(s)), reverse=True)[0]
        relative = target[len(str(R)):]
        assert relative in ('/proc', '/dev/pts', '/dev/shm', '/sys', '/proc/sys/fs/binfmt_misc'), target
        argv = ['sudo', '-n', '/usr/sbin/chroot', str(R), '/bin/umount', '-n', relative]
        r = subprocess.run(argv, capture_output=True, text=True)
        rows.append(dict(argv=argv, rc=r.returncode, stdout=r.stdout, stderr=r.stderr, time_ns=time.time_ns()))
        save(E / (label + '-mounts.json'), rows)
        assert r.returncode == 0, 'ordinary umount failed: ' + relative
    else:
        raise RuntimeError('too many stacked mounts')
    save(E / (label + '-mounts.json'), rows)


def worker(D):
    plan = json.loads((D / 'plan.json').read_text())
    E = D / 'evidence'
    status, reason = 'failed', 'unexpected-controller-error'
    start = time.time_ns()
    try:
        check_source()
        # Same shared exclusion as 39; cover preparation as well as full GBS.
        with LOCK.open('a+') as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            export = json.loads((D / 'export-command.json').read_text())
            rc = stage(D, 'export', export)
            save(E / 'export-result.json', {'argv': export, 'rc': rc})
            G = D / 'gbs-root'
            for sub in ('BUILD-ROOTS', 'sources', 'repos'):
                (G / 'local' / sub).mkdir(parents=True, exist_ok=True)
            driver = D / 'gbs-driver/local'
            driver.mkdir(parents=True)
            for sub in ('sources', 'repos'):
                (driver / sub).mkdir()
            (driver / 'BUILD-ROOTS').symlink_to(G / 'local/BUILD-ROOTS', target_is_directory=True)
            stage(D, 'prep-controller', ['python3', '-B', str(D / 'prep.py')])
            assert json.loads((E / 'prep-result.json').read_text())['rc'] == 0
            cleanup_mounts(D, 'post-prep-cleanup')
        # run.py acquires the same lock and copies the certified export to the exact GBS path.
        stage(D, 'run', ['python3', '-B', str(D / 'run.py')])
        result = json.loads((E / 'controller-result.json').read_text())
        if plan['mode'] == 'rehearsal':
            assert result['reason'] == 'rehearsal-CMake-start', result
            log = (E / 'rpm-build-final.log').read_text(errors='replace')
            assert 'Executing(%prep)' in log and 'Executing(%build)' in log
            assert '+ cmake -G Ninja' in log
            assert not any(x in log for x in ('+ ninja ', 'BOLT_PIPELINE_PASS', 'Build files have been written to:'))
            from log_support import audit_log_copy
            save(E/'log-copy-audit.json',audit_log_copy(D))
            status, reason = 'ok', 'rehearsal-complete-at-CMake'
        else:
            assert result['rc'] == 0 and result['reason'] is None, result
            assert json.loads((E / 'build-result.json').read_text())['exit_code'] == 0
            stage(D, 'validation', ['python3', '-B', str(T / 'validate.py'), '--project', PROJECT, '--root', str(D), '--peer', str(D.parent / 'toolchain')])
            status, reason = 'ok', 'build-and-validation-pass-install-test-deferred'
    except BaseException:
        (E / 'failure.txt').write_text(traceback.format_exc())
        traceback.print_exc()
        reason = 'build-or-validation-failed-see-failure'
    finally:
        try:
            # Refuse cleanup while either of this attempt's build services is live.
            for unit in (plan['prep_unit'], plan['build_unit']):
                state = subprocess.check_output(['systemctl', '--user', 'show', unit, '-p', 'ActiveState', '--value'], text=True).strip()
                assert state in ('inactive', 'failed'), (unit, state)
            cleanup_mounts(D, 'final-cleanup')
        except BaseException:
            status, reason = 'failed', 'cleanup-failed'
            (E / 'cleanup-failure.txt').write_text(traceback.format_exc())
        try:
            audit = final_audit(D, plan)
            if audit['mounts']['stdout'] or audit['remaining_build_processes']:
                status, reason = 'failed', 'residual-process-or-mount-see-final-audit'
            from resource_report import report, critical_stop
            report(D)
            critical = critical_stop(D, audit)
            if critical:
                status, reason = 'stopped', critical
        except BaseException:
            status, reason = 'stopped', 'final-audit-or-resource-report-failed'
            traceback.print_exc()
        try:
            save(E / 'result.json', {'status': status, 'reason': reason, 'start_ns': start, 'end_ns': time.time_ns()})
        finally:
            print('NIGHT_PROJECT 已结束', datetime.datetime.now().astimezone().isoformat(), 'status=' + status, 'reason=' + reason, flush=True)
    return 0 if status == 'ok' else 1


def launch(selection):
    assert selection in ('rehearsal', 'full'), 'use rehearsal or internal full'
    mode = 'rehearsal' if selection.startswith('rehearsal') else 'full'
    suffix = '-02' if selection == 'rehearsal-02' else ''
    identity = check_source()
    D = W / 'temp/rebase-359934-20261106' / (PROJECT if mode == 'full' else 'rehearsal/' + PROJECT)
    if suffix:
        D = D / 'retry-02'
    assert not D.exists(), 'fresh root required; preserve existing directory: ' + str(D)
    assert shutil.disk_usage('/home').free >= 20 * 1024**3
    mem = int(next(l.split()[1] for l in Path('/proc/meminfo').read_text().splitlines() if l.startswith('MemTotal:'))) * 1024
    D.mkdir(parents=True)
    (D / 'tmp').mkdir()
    (D / 'evidence').mkdir()
    plan = dict(identity, source=str(SOURCE), config=str(CONFIG), mode=mode,
                MemoryMax_bytes=mem - 8 * 1024**3, CPUQuota='1200%',
                prep_unit='rebase359934-' + PROJECT + '-' + mode + '-prep-20261106' + suffix + '.service',
                build_unit='rebase359934-' + PROJECT + '-' + mode + '-20261106' + suffix + '.service')
    save(D / 'plan.json', plan)
    shutil.copyfile(T / 'launcher.py', D / 'evidence/launcher-used.py')
    materialize(D, plan)
    unit = 'rebase359934-' + PROJECT + '-' + mode + '-controller-20261106' + suffix + '.service'
    argv = ['systemd-run', '--user', '--unit=' + unit, *properties(plan),
            '-p', 'WorkingDirectory=' + str(SOURCE),
            '-p', 'StandardOutput=append:' + str(D / 'controller.stdout'),
            '-p', 'StandardError=append:' + str(D / 'controller.stderr'),
            '--setenv=FINAL_PROJECT=' + PROJECT, '--setenv=NIGHT_SOURCE_SHA=' + COMMIT, '--setenv=TMPDIR=' + str(D / 'tmp'), '--setenv=PYTHONDONTWRITEBYTECODE=1',
            '/usr/bin/python3', '-B', str(T / 'launcher.py'), '--worker', str(D)]
    save(D / 'controller-command.json', argv)
    subprocess.run(argv, check=True)
    print('Started:', unit)
    print('Logs:', D)
    print('tail -f ' + str(D / 'controller.stdout'))
    return 0


if __name__ == '__main__':
    if len(sys.argv) == 3 and sys.argv[1] == '--worker':
        sys.exit(worker(Path(sys.argv[2])))
    if len(sys.argv) != 2:
        sys.exit('usage: launcher.py rehearsal|full')
    sys.exit(launch(sys.argv[1]))
