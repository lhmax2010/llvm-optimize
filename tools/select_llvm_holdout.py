#!/usr/bin/env python3
"""Lock ten held-out LLVM TUs by subsystem and historical Ninja durations.

No candidate compiler is executed. One TU per group, duration 2..12 seconds,
closest to 6 seconds, object path breaks ties. Exclude every training source.
The clang CodeGen group excludes TargetBuiltins to cover the other frontend.
Writes the entire eligible pool before preprocessing or performance evaluation.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

GROUPS = {
    'ast': 'tools/clang/lib/AST/', 'parse': 'tools/clang/lib/Parse/',
    'driver': 'tools/clang/lib/Driver/', 'frontend_codegen': 'tools/clang/lib/CodeGen/',
    'ir': 'lib/IR/', 'analysis': 'lib/Analysis/',
    'aarch64': 'lib/Target/AArch64/', 'x86': 'lib/Target/X86/',
    'object': 'lib/Object/', 'profiledata': 'lib/ProfileData/',
}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--build-root', type=Path, required=True)
    p.add_argument('--training', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True, help='new directory for selection and evidence')
    a = p.parse_args()
    a.output.mkdir(parents=True, exist_ok=False)
    root = a.build_root.resolve()
    build = root/'home/abuild/rpmbuild/BUILD/llvm-22.1.8/build'
    raw = (build/'.ninja_log').read_bytes()
    (a.output/'ninja-log.txt').write_bytes(raw)
    training = json.loads(a.training.read_text())
    excluded = {r['object'] for r in training}
    durations = {}
    for line in raw.decode().splitlines():
        fields = line.split('\t')
        if len(fields) == 5 and fields[3].endswith('.cpp.o'):
            durations[fields[3]] = (int(fields[1])-int(fields[0]))/1000
    pools, selected = {}, []
    for group, prefix in GROUPS.items():
        pool = [dict(object=obj, build_wall_s=wall) for obj, wall in durations.items()
                if obj.startswith(prefix) and obj not in excluded and 2 <= wall <= 12
                and not (group == 'frontend_codegen' and '/TargetBuiltins/' in obj)]
        pool.sort(key=lambda row: (abs(row['build_wall_s']-6), row['object']))
        if not pool:
            raise RuntimeError('no eligible input in '+group)
        pools[group] = pool
        selected.append(dict(group=group, **pool[0]))
    command = [str(root/'usr/lib64/ld-linux-x86-64.so.2'), '--library-path',
               str(root/'usr/lib64'), str(root/'usr/bin/ninja'), '-t', 'compdb-targets']
    command += [r['object'] for r in selected]
    database = subprocess.check_output(command, cwd=build, text=True)
    (a.output/'compdb.json').write_text(database)
    by_output = {r['output']: r for r in json.loads(database)}
    for row in selected:
        row['file'] = by_output[row['object']]['file']
    if {r['file'] for r in selected} & {r['file'] for r in training}:
        raise RuntimeError('training source overlap')
    evidence = dict(rule=__doc__, groups=GROUPS, seed=20260920, scales=[1,2,2],
                    ninja_log=str(build/'.ninja_log'), ninja_log_sha256=hashlib.sha256(raw).hexdigest(),
                    command=command, eligible_pools=pools, training_overlap=[], selection=selected)
    for filename, data in [('selection.json', selected), ('selection-evidence.json', evidence)]:
        (a.output/filename).write_text(json.dumps(data, indent=2)+'\n')
    print(json.dumps(selected, indent=2))


if __name__ == '__main__':
    main()
