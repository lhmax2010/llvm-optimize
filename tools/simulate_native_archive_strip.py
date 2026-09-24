#!/usr/bin/env python3
"""Copy certified native archives, run the Tizen packaging strip, check each map.

Read-only inputs; never repairs a failed strip/index or skips a failed archive.
Run inside the enclosing resource scope. The old conversion summary identifies
original native members, including repeated archive member names by ordinal.
"""
import argparse
from collections import Counter
import json
from pathlib import Path
import re
import shutil
import time

from convert_static_archives import sha
from inspect_llvm_archives import inspect
from native_archive_commands import MeasuredCommands


def compare(before, after):
    identity=lambda x:[(m['ordinal'],m['name'],m['occurrence']) for m in x['members']]
    if identity(before)!=identity(after):
        raise ValueError('archive member count/order/name changed')
    if after['thin'] or after['bitcode'] or after['other']:
        raise ValueError('strip output contains non-native members')
    if any(m['debug_sections'] for m in after['members']):
        raise ValueError('debug sections survived strip -g')
    if not after['index_equals_machine_symbols']:
        raise ValueError('index is not the defined external-symbol multiset')
    if Counter(map(tuple,before['index']))!=Counter(map(tuple,after['index'])):
        raise ValueError('symbol-to-member mapping changed across strip')


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--conversion',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--rpm-root',type=Path,required=True)
    a=p.parse_args()
    old=a.conversion.resolve();out=a.output.resolve();r=a.rpm_root.resolve()
    out.mkdir(parents=True,exist_ok=False)
    summary=json.loads((old/'summary.json').read_text())
    if summary['status']!='PASS' or len(summary['archives'])!=225:
        raise ValueError('expected certified 225-archive input')
    prefix=[str(r/'lib64/ld-linux-x86-64.so.2'),'--library-path',
            str(r/'usr/lib64')+':'+str(r/'lib64'),str(r/'usr/bin/strip')]
    runner=MeasuredCommands();start=time.monotonic();result=dict(status='RUNNING',archives=[])
    def save(): (out/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
    try:
        runner.run([*prefix,'--version'],out/'strip-version')
        runner.run([*prefix[:3],'--list',prefix[3]],out/'strip-libraries')
        for item in summary['archives']:
            source=old/'archives'/item['path'];dest=out/'archives'/item['path']
            if sha(source)!=item['after_sha256']:
                raise ValueError('input identity differs: '+str(source))
            dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,dest)
        for item in summary['archives']:
            source=old/'archives'/item['path'];dest=out/'archives'/item['path']
            work=out/'checks'/item['path'];work.mkdir(parents=True)
            before=inspect(source);(work/'before.json').write_text(json.dumps(before,indent=2)+'\n')
            command=runner.run([*prefix,'-g',str(dest)],work/'strip',phase='strip')
            lines=(work/'strip.log').read_text().splitlines()
            format_errors=[line for line in lines if re.search(r'file format not recognized|file not recognized|plugin needed',line,re.I)]
            if format_errors:raise ValueError('GNU strip format errors: '+str(format_errors))
            after=inspect(dest);(work/'after.json').write_text(json.dumps(after,indent=2)+'\n')
            compare(before,after)
            with dest.open('rb') as stream:
                for m in after['members']:
                    stream.seek(m['offset']);head=stream.read(20)
                    if head[:6]!=b'\x7fELF\x02\x01' or int.from_bytes(head[16:18],'little')!=1 or int.from_bytes(head[18:20],'little')!=62:
                        raise ValueError('not ELF64 x86_64 ET_REL')
            native=[]
            for original in item['results']:
                if original['preserved']:
                    m=after['members'][original['ordinal']]
                    native.append(dict(ordinal=m['ordinal'],name=m['name'],sha256=m['sha256'],debug_sections=m['debug_sections']))
            result['archives'].append(dict(path=item['path'],before_bytes=before['bytes'],after_bytes=after['bytes'],
                before_sha256=before['sha256'],after_sha256=after['sha256'],members=after['member_count'],
                index_entries=after['index_entries'],preserved_native_members=native,strip=command,status='PASS'))
            save();print('STRIP_PASS',item['path'],flush=True)
        result.update(status='PASS',elapsed_seconds=time.monotonic()-start)
    except BaseException as error:
        runner.cancel();result.update(status='FAIL',reason=str(error),elapsed_seconds=time.monotonic()-start);raise
    finally:save()


if __name__=='__main__':main()
