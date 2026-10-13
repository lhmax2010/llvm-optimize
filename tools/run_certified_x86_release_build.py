#!/usr/bin/env python3
"""One explicitly registered PS3/PS2 build; no generic capacity exemption.

Uses the existing build monitor, CMake gate and cleanup. Frozen experimental
inputs and October 13 admission rules do not widen the ordinary build gate.
Default checks local evidence only; --run permits the single full GBS invocation.
"""
import argparse
import fcntl
import hashlib
import json
from pathlib import Path
import shutil
import signal
import subprocess
import time
from types import SimpleNamespace

import build_llvm_x86_64 as guard
from run_bolt_stage import summarize

W = Path(__file__).resolve().parents[1]
E = W/'temp/release-x86-full-build-20261013/latest-base'
ROOT = Path('/var/tmp/llvm-optimize-x86-archivefix-20261013')
SOURCE = E/'source'
HEAD = '4c36e899dffee2869af9afd174346e3eb9a7d7ca'
BUDGET = 236006948864
ADMISSION = 283208338637
FLOOR = 30*guard.GIB
HASHES = {
    W/'gbs_llvm.conf': '28f1caf93cd39738a7da1e0da8d5f945f7372963bb9823a507f9157294272169',
    E/'gbs-build.conf': 'd1ff39acbaffd03f3c626e9fa8c4a397ea902066e722fd305539cb298de7ab34',
    E/'repository-preflight/buildconfig.conf': '1e7610b6a922d27b80eb59c1c78bdf716f7de2e8e24700e0ee7c62522739ed52',
    E/'repository-preflight/repo.base-standard.repomd.xml': '2a99108e748092148d1161f4ef5e50fbaa57d98132460db6ad02852fea4a39a5',
    E/'repository-preflight/repo.unified-standard.repomd.xml': 'e7af3f222f0ce958678d964589f2d156e8b47ba463ac0b3b0b96c74663382200',
    SOURCE/'packaging/llvm.spec': 'e88ef4cb4cfc4010bceb62a94389f517aedff0b2c2df819ba64dd988d9910426',
    SOURCE/'packaging/llvm-static-archives-native.py': 'c43523c0ce04fc3310e670ff97823db8260c21250dc3172575a18db56500082e',
    W/'patches/archive-index-fix/ps3/0001-packaging-fix-llvm-static-devel-with-ThinLTO.patch': '0d777afbf7b1a7b86afc5c1da5f7bef6b622315efc1316be0cac2b6e782d94e7',
    W/'patches/llvm-strip/ps2/0001-packaging-use-llvm-strip-for-x86_64-archives.patch': 'c679f342a72d52de92914cd2d0007c981e0d6d22a6b378f811ca8ee8e12da9ff',
}


def verify_inputs(round_number=1):
    files = {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in HASHES}
    for p, expected in HASHES.items():
        if files[str(p)] != expected:
            raise RuntimeError('unregistered input: '+str(p))
    def git(*args):
        return subprocess.check_output(['git','-C',str(SOURCE),*args],text=True).strip()
    if git('rev-parse','HEAD') != HEAD or git('status','--porcelain','--untracked-files=all'):
        raise RuntimeError('candidate source HEAD/status differs from registration')
    if json.loads((E/'repository-preflight/result.json').read_text())['status'] != 'PASS':
        raise RuntimeError('repository preflight did not pass')
    for p in (W/'temp/.llvm-optimize-exclusive.lock',
              W/'temp/gbs-root-x86_64-archivefix-v2/.llvm-optimize-exclusive.lock'):
        lock = json.loads(p.read_text())
        expected_session = ('release-x86-latest-base-20261013' if round_number == 1
                            else 'release-x86-round2-launch-20261013')
        if lock['session'] != expected_session:
            raise RuntimeError('wrong project lock owner')
        Path('/proc',str(lock['pid'])).stat()
    if ROOT.exists():
        raise RuntimeError('fresh root already exists; no build retry')
    return files


def disk_admission(free, round_number=1):
    normal = free >= ADMISSION and free-BUDGET >= FLOOR
    exception = (round_number == 2 and 0 < ADMISSION-free <= guard.GIB
                 and free-BUDGET >= 40*guard.GIB)
    if not (normal or exception):
        raise RuntimeError(f'disk admission failed: {free}; budget={BUDGET}; required={ADMISSION}; floor={FLOOR}')
    return dict(free_bytes=free,required_bytes=ADMISSION,budget_bytes=BUDGET,
                shortfall_bytes=max(0,ADMISSION-free),remaining_after_budget_bytes=free-BUDGET,
                pm_exception_used=exception and not normal,round_number=round_number)


def run_paths(round_number):
    if round_number == 1:
        return E, 'gbs-invoked.json'
    if round_number == 2:
        return E.parent/'round2-launch', 'gbs-invoked-round2.json'
    raise ValueError('unregistered build round')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run',action='store_true')
    parser.add_argument('--round',dest='round_number',type=int,choices=(1,2),default=1)
    args = parser.parse_args()
    run_e, marker = run_paths(args.round_number)
    if (run_e/marker).exists():
        raise RuntimeError('GBS invocation already recorded; no retry')
    files = verify_inputs(args.round_number)
    admission = disk_admission(shutil.disk_usage(ROOT.parent).free,args.round_number)
    if not args.run:
        print(json.dumps(dict(status='PASS',files=files,root=str(ROOT),admission=admission),indent=2)); return
    audit = guard.Audit(run_e/'full-build-scope')
    lock = Path('/home/linhao/Toolchain/development/heavy-stage.lock').open('a')
    locked = False
    try:
        start = time.monotonic()
        while True:
            try:
                fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB); locked=True; break
            except BlockingIOError:
                audit.json('heavy-lock-wait.json',dict(time=guard.stamp(),wait_seconds=time.monotonic()-start))
                if time.monotonic()-start >= 7200: raise RuntimeError('shared lock timeout')
                time.sleep(30)
        audit.json('heavy-lock-acquired.json',dict(time=guard.stamp(),wait_seconds=time.monotonic()-start))
        start = time.monotonic(); readings=[]
        while True:
            available=guard.mem_available()
            readings.append(dict(time=guard.stamp(),available_bytes=available,required_bytes=10*guard.GIB))
            audit.json('admission.json',readings)
            if available >= 10*guard.GIB: break
            if time.monotonic()-start >= 3600: raise RuntimeError('memory admission timeout')
            time.sleep(300)
        files=verify_inputs(args.round_number); free=shutil.disk_usage(ROOT.parent).free
        admission=disk_admission(free,args.round_number)
        audit.json('disk-admission.json',admission)
        for cmd in (['nproc'],['free','-g'],['df','-h',str(ROOT.parent)],
                    ['systemd-run','--user','--scope','-p','MemoryMax=1G','-p','MemorySwapMax=0','/bin/true']):
            audit.run(cmd)
        # Fixed trial, not the historical archive-fix certification profile.
        plan=dict(memory_max_gib=18,ninja_jobs=6,compile_jobs=6,link_jobs=2,debuginfo_jobs=4,
                  gbs_threads=1,available_bytes=available,disk_free_bytes=free,disk_floor_bytes=FLOOR,
                  admission='EXPLICIT_PS3_PS2_LATEST_BASE_TRIAL',files=files,head=HEAD,
                  round_number=args.round_number,disk_admission=admission,
                  # Select only the ordinary static CMake contract and final cgroup capture.
                  certify_fingerprint='archive-fix-trial',
                  cmake_parameters=dict(LLVM_TARGETS_TO_BUILD='X86;ARM;AArch64;BPF',
                    LLVM_ENABLE_PROJECTS='clang;lldb;clang-tools-extra;lld;compiler-rt;openmp',
                    CMAKE_C_COMPILER='clang',CMAKE_CXX_COMPILER='clang++',LLVM_ENABLE_RTTI='ON',
                    LLVM_BUILD_LLVM_DYLIB='ON',LLVM_PARALLEL_COMPILE_JOBS='6',LLVM_PARALLEL_LINK_JOBS='2'))
        audit.json('registered-plan.json',plan)
        with (run_e/marker).open('x') as f:
            json.dump(dict(time=guard.stamp(),root=str(ROOT),head=HEAD),f)
        guard.build(audit,SimpleNamespace(buildroot=ROOT,source=SOURCE,config=E/'gbs-build.conf',spec='llvm.spec'),
                    plan,E/'repository-preflight/buildconfig.conf','systemd')
    except BaseException as error:
        audit.json('stopped.json',dict(time=guard.stamp(),error=repr(error))); raise
    finally:
        if locked: fcntl.flock(lock,fcntl.LOCK_UN)
        lock.close(); audit.json('heavy-lock-released.json',dict(time=guard.stamp()))
        if (audit.directory/'outcome.json').exists(): summarize(audit.directory)
        audit.stream.close()


if __name__ == '__main__':
    for sig in (signal.SIGTERM,signal.SIGINT,signal.SIGHUP):
        signal.signal(sig,lambda sig,frame: (_ for _ in ()).throw(KeyboardInterrupt(str(sig))))
    main()
