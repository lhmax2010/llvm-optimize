#!/usr/bin/env python3
"""Read-only originals; probe Tizen llvm-strip on three independent archive copies."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import time

from inspect_llvm_archives import inspect


def digest(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024*1024), b''):
            h.update(chunk)
    return h.hexdigest()


def command(argv, output, name):
    start = time.monotonic()
    result = subprocess.run(list(map(str, argv)), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (output/(name+'.stdout')).write_bytes(result.stdout)
    (output/(name+'.stderr')).write_bytes(result.stderr)
    row = dict(argv=list(map(str, argv)), exit=result.returncode, wall=time.monotonic()-start,
               stdout=result.stdout.decode(errors='replace'), stderr=result.stderr.decode(errors='replace'))
    (output/(name+'.json')).write_text(json.dumps(row, indent=2)+'\n')
    return row


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--build', type=Path, required=True)
    p.add_argument('--rpm-root', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args(); out=a.output.resolve();out.mkdir(parents=True,exist_ok=False)
    root=a.rpm_root.resolve();build=a.build.resolve()
    loader=root/'lib64/ld-linux-x86-64.so.2';strip=root/'usr/bin/llvm-strip'
    prefix=[loader,'--library-path',str(root/'usr/lib64')+':'+str(root/'lib64'),strip]
    result=dict(tool=str(strip),tool_sha256=digest(strip),loader=str(loader),loader_sha256=digest(loader),archives=[])
    result['version']=command([*prefix,'--version'],out,'version')
    result['dependencies']=command([*prefix[:3],'--list',strip],out,'dependencies')
    assert result['version']['exit']==0 and result['dependencies']['exit']==0
    names=['lib64/libLLVMAnalysis.a','lib64/libLLVMBinaryFormat.a','lib64/clang/22/lib/linux/libclang_rt.asan-x86_64.a']
    for index,name in enumerate(names):
        source=build/name;target=out/source.name
        before=inspect(source);shutil.copyfile(source,target)
        assert digest(target)==before['sha256']
        call=command([*prefix,'-g',target],out,'strip-'+str(index))
        after=inspect(target)
        row=dict(source=str(source),copy=str(target),before=before,after=after,command=call,
                 sha_changed=before['sha256']!=after['sha256'],
                 index_changed=before['index']!=after['index'],
                 member_payloads_unchanged=[m['sha256'] for m in before['members']]==[m['sha256'] for m in after['members']],
                 before_debug_members=sum(bool(m['debug_sections']) for m in before['members']),
                 after_debug_members=sum(bool(m['debug_sections']) for m in after['members']))
        assert digest(source)==before['sha256'],'read-only source changed'
        result['archives'].append(row)
        (out/'result.json').write_text(json.dumps(result,indent=2)+'\n')
        print(json.dumps(dict(name=source.name,exit=call['exit'],stderr=call['stderr'],sha_changed=row['sha_changed'],
                              before_index=before['index_entries'],after_index=after['index_entries'],
                              bitcode=before['bitcode'],machine=before['machine'],debug_before=row['before_debug_members'],debug_after=row['after_debug_members'])),flush=True)

if __name__=='__main__':main()
