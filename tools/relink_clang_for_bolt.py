#!/usr/bin/env python3
"""Relink only the existing clang-22 Ninja edge, with --emit-relocs, under 18 GiB.

No spec, CMake, Ninja file or baseline executable is edited. Reuses the existing
ThinLTO cache; writes ELF and linker dependency output into a new chroot directory.
Default is plan only. Uses the build guard's sampler, emergency stop and cleanup.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shlex
import shutil
import signal
from types import SimpleNamespace
import uuid

import build_llvm_x86_64 as guard


def rewrite_command(original, destination):
    original = original.strip()
    if '\n' in original or not original.startswith(': && ') or not original.endswith(' && :'):
        raise RuntimeError('unexpected Ninja link command framing')
    payload = original[len(': && '):-len(' && :')]
    old_output = '-o bin/clang-22 '
    old_dep = '--dependency-file=tools/clang/tools/driver/CMakeFiles/clang.dir/link.d'
    if payload.count(old_output)!=1 or payload.count(old_dep)!=1 or '--emit-relocs' in payload:
        raise RuntimeError('unexpected link output/dependency arguments')
    # Keep the original shell escaping, notably the literal $ORIGIN rpath.
    payload = payload.replace(old_output, '-o '+shlex.quote(str(destination/'clang-22'))+' ')
    payload = payload.replace(old_dep, '--dependency-file='+shlex.quote(str(destination/'clang-link.d')))
    return payload+' -Wl,--emit-relocs'


def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root', type=Path, required=True, help='existing R1 scratch.x86_64.N root')
    p.add_argument('--log-dir', type=Path, required=True, help='new directory under workspace temp/')
    p.add_argument('--run', action='store_true', help='execute the single link after validation')
    a = p.parse_args()
    root, log = a.root.resolve(), a.log_dir.resolve()
    if not root.is_relative_to(guard.WORKSPACE/'temp') or not log.is_relative_to(guard.WORKSPACE/'temp'):
        p.error('root and log-dir must be under workspace temp/')
    audit = guard.Audit(log)
    inner_build = Path('/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build')
    build = root/str(inner_build).lstrip('/')
    destination = Path('/home/abuild')/('bolt-relocs-'+uuid.uuid4().hex[:12])
    host_destination = root/str(destination).lstrip('/')
    profile = json.loads(guard.BASELINE_PROFILE.read_text())
    watched = [build/'bin/clang-22', build/'build.ninja', build/'CMakeCache.txt',
               guard.WORKSPACE/'temp/toolchain-baseline/usr/bin/clang']
    before = {}
    try:
        for command in (['nproc'],['free','-g'],['df','-h',root]): audit.run(command)
        available, disk = guard.mem_available(), shutil.disk_usage(root).free
        cpus = int(audit.run(['nproc']).stdout)
        guard.validate_resources(available,disk,cpus)
        values, errors = guard.validate_cache((build/'CMakeCache.txt').read_text(),profile['cmake_parameters'])
        if errors: raise RuntimeError('baseline cache changed: '+repr(errors))
        before = {str(path):digest(path) for path in watched}
        audit.json('preserved-inputs-before.json',before)
        # Query only the requested final edge, never all dependencies or a build.
        query = [str(root/'usr/lib64/ld-linux-x86-64.so.2'),'--library-path',str(root/'usr/lib64'),
                 str(root/'usr/bin/ninja'),'-C',str(build),'-t','commands','-s','bin/clang-22']
        original = audit.run(query).stdout
        command = rewrite_command(original,destination)
        (log/'original-link-command.txt').write_text(original)
        (log/'relocs-link-command.txt').write_text(command+'\n')
        audit.json('relink-plan.json',dict(build=str(build),output=str(host_destination/'clang-22'),
                   dependency_file=str(host_destination/'clang-link.d'),
                   reused_thinlto_cache=str(build/'lto.cache'),
                   added_optimization_independent_flag='-Wl,--emit-relocs',
                   original_command=original,command=command))
        if not a.run:
            audit.log('PLAN ONLY; no linker executed')
            return 0
        audit.run(['systemd-run','--user','--scope','-p','MemoryMax=1G','-p','MemorySwapMax=0','/bin/true'])
        if host_destination.exists(): raise RuntimeError('refusing existing output directory')
        completion = destination/'link.exit'; release = destination/'release'
        trap = ('status=$?; printf "%s\\n" "$status" > '+shlex.quote(str(completion))+
                '; while [ ! -e '+shlex.quote(str(release))+' ]; do sleep .2; done; exit "$status"')
        script = ('set -eu\nmkdir '+shlex.quote(str(destination))+'\ntrap '+shlex.quote(trap)+
                  ' EXIT\ncd '+shlex.quote(str(inner_build))+'\n'+command+'\n')
        stdin = 'exec '+shlex.join(['su','-s','/bin/bash','-c',script,'-','abuild'])+'\n'
        (log/'abuild-relink.sh').write_text(script)
        plan = dict(memory_max_gib=18,compile_jobs=4,link_jobs=1,ninja_jobs=4,gbs_threads=1,
                    operation='AUTHORIZED_SINGLE_RELINK',cmake_parameters=profile['cmake_parameters'])
        # Validate resources again after ELF hashes and the Ninja query.
        guard.validate_resources(guard.mem_available(),shutil.disk_usage(root).free,cpus)
        args = SimpleNamespace(buildroot=root.parents[2],config=guard.WORKSPACE/'gbs_llvm.conf',
                               source=guard.WORKSPACE/'llvm')
        guard.build(audit,args,plan,None,'systemd',command=['gbs','chroot','--root',str(root)],
                    input_text=stdin,completion_file=root/str(completion).lstrip('/'),
                    release_file=root/str(release).lstrip('/'))
        output = host_destination/'clang-22'
        audit.run(['readelf','-SW',output])
        audit.run(['readelf','-d',output])
        audit.json('output.json',dict(path=str(output),bytes=output.stat().st_size,sha256=digest(output)))
        return 0
    except (Exception, KeyboardInterrupt) as error:
        audit.json('stopped.json',dict(reason=str(error),time=guard.stamp()))
        audit.log('STOPPED '+str(error))
        return 2
    finally:
        if before:
            after = {str(path):digest(path) for path in watched}
            audit.json('preserved-inputs-after.json',after)
            audit.json('preservation-check.json',dict(equal=before==after,before=before,after=after))
        audit.stream.close()


if __name__ == '__main__':
    def interrupted(signum, frame): raise KeyboardInterrupt(f'signal {signum}')
    for sig in (signal.SIGINT,signal.SIGTERM,signal.SIGHUP,signal.SIGQUIT):
        signal.signal(sig,interrupted)
    raise SystemExit(main())
