#!/usr/bin/env python3
"""Resume an audited copy of the completed LLVM tree using RPM --noprep.

Requires the source/archive/patch and root-copy evidence described in docs/13.
Does not initialize, clean, or edit the source tree/spec. Default: preflight only.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shlex
import shutil
import signal
import subprocess as sp
import sys
from types import SimpleNamespace

import build_llvm_x86_64 as guard


def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root', type=Path, required=True, help='independent copied scratch.x86_64.0 chroot from the audited baseline')
    p.add_argument('--evidence', type=Path, required=True, help='directory containing verified source and clone JSON')
    p.add_argument('--log-dir', type=Path, required=True, help='new, nonexisting audit directory under temp/')
    p.add_argument('--run', action='store_true', help='execute normal -ba --noprep with debuginfo -j4; cap remains 18 GiB')
    a = p.parse_args()
    root, evidence = a.root.resolve(), a.evidence.resolve()
    audit = guard.Audit(a.log_dir.resolve())
    try:
        for command in (['nproc'], ['free', '-g'], ['df', '-h', root]):
            audit.run(command)
        available = guard.mem_available()
        disk = shutil.disk_usage(root).free
        if available < 16 * guard.GIB or disk < 60 * guard.GIB:
            raise RuntimeError('resume requires MemAvailable >=16 GiB and disk >=60 GiB')
        source_proof = json.loads((evidence/'prepared-source-equivalence.json').read_text())
        patches = json.loads((evidence/'prep-patch-equivalence.json').read_text())
        clone = json.loads((evidence/'clone-result.json').read_text())
        if (any(x['errors'] for x in source_proof) or not patches or not all(x['equal'] for x in patches)
                or clone['reader_exit'] or clone['writer_exit'] or Path(clone['new']).resolve() != root):
            raise RuntimeError('source preparation or independent clone equivalence is not verified')
        old = Path(clone['old']).resolve()
        if root == old or root.name != 'scratch.x86_64.0' or root.parent.name != 'BUILD-ROOTS':
            raise RuntimeError('expected a separate GBS scratch.x86_64.0 root')
        if (root/'not-ready').exists():
            raise RuntimeError('copied build root has a not-ready marker; preserve and investigate')
        top = Path('home/abuild/rpmbuild')
        checks = ['home/abuild/.rpmmacros', 'home/abuild/.rpmrc',
                  str(top/'SOURCES/llvm.spec'), str(top/'BUILD/llvm-22.1.8/build/CMakeCache.txt'),
                  str(top/'BUILD/llvm-22.1.8/build/build.ninja'),
                  str(top/'BUILD/llvm-22.1.8/build/.ninja_log'),
                  str(top/'BUILD/llvm-22.1.8/build/.ninja_deps')]
        checks += [str(top/'BUILD/llvm-22.1.8/build/bin'/name) for name in ('clang-22','lld','llvm-ar')]
        identities = []
        for rel in checks:
            before, after = digest(old/rel), digest(root/rel)
            old_stat, new_stat = (old/rel).stat(), (root/rel).stat()
            independent = (old_stat.st_dev,old_stat.st_ino) != (new_stat.st_dev,new_stat.st_ino)
            identities.append(dict(path=rel, original=before, copied=after, equal=before == after,
                                   old_mtime_ns=old_stat.st_mtime_ns, copied_mtime_ns=new_stat.st_mtime_ns,
                                   independent_inode=independent))
        audit.json('clone-key-identities.json', identities)
        if not all(x['equal'] and x['independent_inode'] and x['old_mtime_ns']==x['copied_mtime_ns'] for x in identities):
            raise RuntimeError('copied spec, macro, or build configuration differs from original')
        if (root/top/'BUILDROOT').exists():
            raise RuntimeError('BUILDROOT must be absent before resume; do not reuse partially stripped files')
        values, errors = guard.validate_cache((root/top/'BUILD/llvm-22.1.8/build/CMakeCache.txt').read_text())
        if errors or values.get('LLVM_PARALLEL_COMPILE_JOBS') != '4' or values.get('LLVM_PARALLEL_LINK_JOBS') != '1':
            raise RuntimeError('copied CMake configuration does not match approved baseline: '+repr(errors))
        audit.json('copied-cache-validation.json', dict(values=values, errors=errors))
        plan = dict(available_bytes=available, disk_free_bytes=disk,
                    nproc=int(audit.run(['nproc']).stdout), memory_max_gib=18,
                    gbs_threads=1, ninja_jobs=4, compile_jobs=4, link_jobs=1,
                    debuginfo_jobs=4, observed_single_link_gib=16.831096649169922,
                    note='Resume keeps the approved 18 GiB cap; 8 GiB is no longer a valid link estimate.')
        audit.json('resource-plan.json', plan)
        audit.run(['systemd-run', '--user', '--scope', '-p', 'MemoryMax=1G', '-p', 'MemorySwapMax=0', '/bin/true'])
        if not a.run:
            audit.log('RESUME PREFLIGHT PASS; no build executed')
            return 0
        command = ['rpmbuild', '--define', '_srcdefattr (-,root,root)', '--nosignature',
                   '--target=x86_64', '--define', '_build_create_debug 1',
                   '--define', '_smp_mflags -j4', '-ba', '--noprep',
                   '/home/abuild/rpmbuild/SOURCES/llvm.spec']
        completion_path = '/home/abuild/llvm-resume-rpm.exit'
        completion_file = root/completion_path.lstrip('/')
        release_path = '/home/abuild/llvm-resume-rpm.release'
        release_file = root/release_path.lstrip('/')
        if completion_file.exists() or release_file.exists():
            raise RuntimeError('resume completion marker already exists; preserve prior execution')
        trap = ('status=$?; printf "%s\\n" "$status" > '+shlex.quote(completion_path)
                +'; while [ ! -e '+shlex.quote(release_path)+' ]; do sleep 0.2; done; exit "$status"')
        script = ('set -eu\n'
                  'trap '+shlex.quote(trap)+' EXIT\n'
                  'printf "RESUME_MACROS="\n'
                  'rpm --define "_smp_mflags -j4" --eval "%{_toolchain}|%{_smp_mflags}"\n'
                  'test "$(rpm --define "_smp_mflags -j4" --eval "%{_toolchain}|%{_smp_mflags}")" = "clang|-j4"\n'
                  'mkdir -p /home/abuild/rpmbuild/BUILDROOT\n'
                  'cd /home/abuild\n'
                  +shlex.join(command)+'\n')
        # Match GBS build-recipe-spec:180: a login shell for abuild.
        # Installed gbs chroot ignores the child's status, so verify our EXIT marker too.
        input_text='exec '+shlex.join(['su','-s','/bin/bash','-c',script,'-','abuild'])+'\n'
        (audit.directory/'abuild-resume.sh').write_text(script)
        (audit.directory/'chroot-input.sh').write_text(input_text)
        args = SimpleNamespace(buildroot=root.parents[2], config=guard.WORKSPACE/'gbs_llvm.conf',
                               source=guard.WORKSPACE/'llvm')
        # Hashing the preserved binaries may take time: re-check the start gates now.
        plan['available_bytes'] = guard.mem_available()
        plan['disk_free_bytes'] = shutil.disk_usage(root).free
        if plan['available_bytes'] < 16*guard.GIB or plan['disk_free_bytes'] < 60*guard.GIB:
            raise RuntimeError('resource thresholds no longer met immediately before resume')
        audit.run(['free','-g'])
        audit.run(['df','-h',root])
        audit.json('resource-plan.json',plan)
        guard.build(audit, args, plan, None, 'systemd',
                    command=['gbs', 'chroot', '--root', str(root)], input_text=input_text,
                    completion_file=completion_file, release_file=release_file)
        return 0
    except (Exception, KeyboardInterrupt) as error:
        audit.log('STOPPED '+str(error))
        audit.json('stopped.json', dict(reason=str(error), time=guard.stamp()))
        return 2
    finally:
        audit.stream.close()


if __name__ == '__main__':
    def interrupted(signum, _frame):
        raise KeyboardInterrupt(f'signal {signum}')
    for signum in (signal.SIGTERM, signal.SIGINT, signal.SIGHUP, signal.SIGQUIT):
        signal.signal(signum, interrupted)
    sys.exit(main())
