#!/usr/bin/env python3
"""Census an independently extracted RPM set. Never edits archives or uses a build tree."""
import argparse
from collections import Counter
import json
from pathlib import Path
from inspect_llvm_archives import inspect


def census(root, owners_path, output):
    owners=json.loads(owners_path.read_text());output.mkdir(parents=True,exist_ok=False)
    rows=[];groups={};blockers=[]
    for path in sorted(root.rglob('*.a')):
        if path.is_symlink():
            raise ValueError(f'archive symlink needs explicit handling: {path}')
        rel='/'+str(path.relative_to(root));packages=sorted({x['rpm'] for x in owners[rel]})
        full=inspect(path);full['relative']=rel;full['packages']=packages
        target=output/'archives'/path.relative_to(root).with_suffix('.a.json');target.parent.mkdir(parents=True,exist_ok=True)
        target.write_text(json.dumps(full,indent=2)+'\n')
        row={k:full[k] for k in ['relative','packages','bytes','sha256','thin','member_count','bitcode','machine','other','index_entries','index_equals_machine_symbols','machine_symbol_entries']}
        rows.append(row)
        group='compiler-rt' if 'compiler-rt' in packages else ('libarcher_static.a' if path.name=='libarcher_static.a' else 'llvm-static-devel' if 'llvm-static-devel' in packages else 'other')
        row['group']=group;groups.setdefault(group,[]).append(row)
        if group in ('compiler-rt','libarcher_static.a') and (row['bitcode'] or row['other'] or row['thin']):
            blockers.append(row)
        print(json.dumps(row),flush=True)
    summary={key:dict(archives=len(vals),members=sum(r['member_count'] for r in vals),bitcode=sum(r['bitcode'] for r in vals),machine=sum(r['machine'] for r in vals),other=sum(r['other'] for r in vals),thin=sum(r['thin'] for r in vals),index_equals_machine_symbols=sum(r['index_equals_machine_symbols'] for r in vals)) for key,vals in groups.items()}
    result=dict(root=str(root),archives=rows,groups=summary,runtime_blockers=blockers,gate='FAIL_RUNTIME_FORMAT' if blockers else 'PASS')
    (output/'census.json').write_text(json.dumps(result,indent=2)+'\n')
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root',type=Path,required=True);p.add_argument('--owners',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    result=census(args.root,args.owners,args.output)
    print(json.dumps({'groups':result['groups'],'gate':result['gate']},indent=2))
    return 2 if result['runtime_blockers'] else 0

if __name__=='__main__':raise SystemExit(main())
