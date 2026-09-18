#!/usr/bin/env python3
"""Add BOLT to an existing experimental build, preserving baseline ELF evidence.

Requires all 10 relink equality checks. Changes only this build's CMake project
list, never spec/source. Configures, validates, dry-runs, then builds three named
BOLT targets under the shared 18 GiB guard. Existing baseline ELFs must not change.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shlex
import shutil
import subprocess
import sys

import build_llvm_x86_64 as guard


def digest(path):
    with path.open('rb') as f: return hashlib.file_digest(f,'sha256').hexdigest()


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root',type=Path,required=True)
    p.add_argument('--equality',type=Path,required=True)
    p.add_argument('--relocs',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True,help='new evidence directory under temp/')
    p.add_argument('--configured-evidence',type=Path,help='previous evidence after successful configure; preserve it and retry only target build')
    a=p.parse_args();root=a.root.resolve();out=a.output.resolve();w=guard.WORKSPACE
    if not root.is_relative_to(w/'temp') or not out.is_relative_to(w/'temp') or out.exists():
        p.error('existing root and new output under workspace temp/ required')
    equality=json.loads(a.equality.read_text())
    if equality['status']!='PASS' or len(equality['units'])!=10 or not all(x['byte_equal'] for x in equality['units']):
        p.error('all 10 real TU byte comparisons must PASS first')
    out.mkdir();inner='/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build';build=root/inner.lstrip('/')
    profile=json.loads(guard.BASELINE_PROFILE.read_text())
    cache_source=a.configured_evidence/'before/CMakeCache.txt' if a.configured_evidence else build/'CMakeCache.txt'
    values,errors=guard.validate_cache(cache_source.read_text(),profile['cmake_parameters'])
    if errors: raise RuntimeError('not the original baseline cache: '+repr(errors))
    files=[w/'gbs_llvm.conf',w/'llvm/packaging/llvm.spec',a.relocs.resolve(),
           root/'home/abuild/rpmbuild/SOURCES/llvm.spec']
    for base in [build,w/'temp/toolchain-baseline/usr']:
        files += [base/'bin'/name for name in ['clang-22','clang++','ld.lld','llvm-ar','llvm-ranlib']]
    def snapshot(label):
        dest=out/label;dest.mkdir()
        rows={str(f):dict(bytes=f.stat().st_size,sha256=digest(f)) for f in files}
        for name in ['CMakeCache.txt','build.ninja','CMakeFiles/rules.ninja','.ninja_log',
                     'include/llvm/Config/llvm-config.h','include/llvm/Config/config.h']:
            f=build/name
            if f.exists():
                target=dest/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(f,target)
        (dest/'identities.json').write_text(json.dumps(rows,indent=2)+'\n')
        return rows
    before=snapshot('before')
    if a.configured_evidence:
        historical=json.loads((a.configured_evidence/'before/identities.json').read_text())
        if before!=historical: raise RuntimeError('baseline identities changed since first configure')
        # Keep the original cache as the baseline for semantic comparisons.
        shutil.copy2(cache_source,out/'before/CMakeCache.original.txt')
    def stage(label,body):
        script=out/(label+'.sh');script.write_text(body+'\n')
        cmd=[sys.executable,str(w/'tools/run_bolt_stage.py'),'--root',str(root),
             '--cwd',inner,'--log-dir',str(out/label),'--script',str(script)]
        with (out/(label+'-console.log')).open('w') as f:
            subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT,check=True)
    try:
        projects=values['LLVM_ENABLE_PROJECTS']+';bolt'
        if not a.configured_evidence:
            stage('configure',shlex.join(['cmake','-S',values['CMAKE_HOME_DIRECTORY'],'-B','.',
                                         '-DLLVM_ENABLE_PROJECTS='+projects]))
        after_config=snapshot('after-configure')
        expected=dict(profile['cmake_parameters']);expected['LLVM_ENABLE_PROJECTS']=projects
        new,errors=guard.validate_cache((build/'CMakeCache.txt').read_text(),expected)
        changes={k:dict(before=values.get(k),after=new.get(k)) for k in set(values)|set(new) if values.get(k)!=new.get(k)}
        (out/'cache-changes.json').write_text(json.dumps(changes,indent=2,sort_keys=True)+'\n')
        (out/'configuration-check.json').write_text(json.dumps(dict(errors=errors,baseline_elfs_unchanged=before==after_config),indent=2)+'\n')
        if errors or before!=after_config: raise RuntimeError('configuration changed baseline flags/ELFs')
        # Absolute paths in the graph require the same chroot even for a dry run.
        # perf2bolt is llvm-bolt's POST_BUILD symlink, not a standalone Ninja target.
        stage('dry-run','ninja -n -j4 llvm-bolt merge-fdata')
        dry=(out/'dry-run/build.log').read_text()
        (out/'ninja-dry-run.log').write_text(dry)
        if 'Re-running CMake' in dry: raise RuntimeError('dry run only plans regeneration; target graph not yet audited')
        tasks=[line for line in dry.splitlines() if re.search(r'\[\d+/\d+\]',line)]
        # This generated 45-byte anchor is rewritten by configure. Its archive
        # POST_BUILD copies and byte-compares the same prebuilt PIC runtime.
        tf_source=build.parent/'mlgo_verify_assets/mlgo_sysroot/xla_aot_runtime_src'
        tf_archive=build/'lib64/libtf_xla_runtime.a'
        tf_prebuilt=tf_source/'libtf_xla_runtime_prebuilt.a'
        tf_proof=dict(before=digest(tf_archive),prebuilt=digest(tf_prebuilt),
                      cmake=(tf_source/'CMakeLists.txt').read_text())
        if tf_proof['before']!=tf_proof['prebuilt']:
            raise RuntimeError('existing TF runtime differs from audited prebuilt input')
        shutil.copy2(tf_archive,out/'libtf_xla_runtime.before.a')
        (out/'tf-runtime-proof.json').write_text(json.dumps(tf_proof,indent=2)+'\n')
        tf_edges=['Building C object lib64/tf_runtime/CMakeFiles/tf_xla_runtime.dir/tf_xla_runtime_dummy.c.o',
                  'Linking C static library lib64/libtf_xla_runtime.a']
        # Refuse unexpected recompilation of baseline LLVM/Clang objects or executables.
        unexpected=[line for line in tasks if (('Building ' in line or 'Linking ' in line) and 'tools/bolt/' not in line
                       and not any(name in line for name in ['bin/llvm-bolt','bin/merge-fdata','lib64/libLLVMBOLT'])
                       and not any(line.endswith(edge) for edge in tf_edges))]
        (out/'dry-run-check.json').write_text(json.dumps(dict(task_count=len(tasks),unexpected=unexpected),indent=2)+'\n')
        if unexpected: raise RuntimeError('dry run would rebuild baseline targets; inspect evidence before proceeding')
        stage('build','ninja -j4 llvm-bolt merge-fdata')
        tf_proof['after']=digest(tf_archive)
        (out/'tf-runtime-proof.json').write_text(json.dumps(tf_proof,indent=2)+'\n')
        if tf_proof['after']!=tf_proof['before']: raise RuntimeError('TF runtime archive changed')
        after=snapshot('after-build')
        (out/'preservation-check.json').write_text(json.dumps(dict(equal=before==after,before=before,after=after),indent=2)+'\n')
        if before!=after: raise RuntimeError('baseline ELF/spec/config changed during incremental build')
        tools=[]
        for name in ['llvm-bolt','perf2bolt','merge-fdata']:
            path=build/'bin'/name
            tools.append(dict(name=name,path=str(path),bytes=path.stat().st_size,sha256=digest(path)))
        (out/'tools.json').write_text(json.dumps(tools,indent=2)+'\n')
        print('BOLT_INCREMENTAL_BUILD_PASS',flush=True)
        return 0
    except Exception as error:
        (out/'stopped.json').write_text(json.dumps(dict(error=str(error)),indent=2)+'\n')
        print('STOPPED',error,flush=True);return 2


if __name__=='__main__': raise SystemExit(main())
