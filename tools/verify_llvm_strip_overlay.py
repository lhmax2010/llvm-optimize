#!/usr/bin/env python3
"""Strip native archive copies twice with Tizen llvm-strip; keep full evidence.

Requires an enclosing memory-limited scope. Inputs are read-only. A failed
command, member-identity check, debug check, index check or determinism check
stops the experiment. GNU comparison inputs are historical stripped copies,
not repaired or rewritten here.
"""
import argparse
from collections import Counter
import json
from pathlib import Path
import shutil
import time

from convert_static_archives import sha
from inspect_llvm_archives import inspect
from native_archive_commands import MeasuredCommands
from simulate_native_archive_strip import compare


def identities(data):
    return [(m['ordinal'], m['name'], m['occurrence']) for m in data['members']]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('conversion', 'runtime-build', 'baseline', 'gnu-native', 'rpm-root', 'output'):
        parser.add_argument('--'+name, type=Path, required=True)
    args = parser.parse_args()
    out=args.output.resolve(); out.mkdir(parents=True, exist_ok=False)
    conversion=json.loads((args.conversion/'summary.json').read_text())
    assert conversion['status']=='CONVERTED' and len(conversion['archives'])==225
    r=args.rpm_root.resolve()
    prefix=[str(r/'lib64/ld-linux-x86-64.so.2'), '--library-path',
            str(r/'usr/lib64')+':'+str(r/'lib64'), str(r/'usr/bin/llvm-strip')]
    runner=MeasuredCommands(); started=time.monotonic()
    summary=dict(status='RUNNING', archives=[], strip_prefix=prefix,
                 strip_sha256=sha(r/'usr/bin/llvm-strip'), loader_sha256=sha(r/'lib64/ld-linux-x86-64.so.2'))
    def save():
        (out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    try:
        runner.run([*prefix, '--version'], out/'version')
        runner.run([*prefix[:3], '--list', prefix[3]], out/'libraries')
        inputs=[]
        for item in conversion['archives']:
            rel=Path(item['path']); path=args.conversion/'archives'/rel
            data=inspect(path)
            assert data['sha256']==item['after_sha256'], str(path)
            inputs.append(('development', rel, path, args.gnu_native/rel))
        runtimes=sorted((args.baseline/'usr/lib64/clang/22/lib/linux').glob('*.a'))
        assert len(runtimes)==45, len(runtimes)
        for baseline in runtimes:
            rel=baseline.relative_to(args.baseline)
            path=args.runtime_build/'lib64/clang/22/lib/linux'/baseline.name
            assert path.is_file(), str(path)
            inputs.append(('compiler-rt', rel, path, baseline))
        for category, rel, original, gnu in inputs:
            summary.update(current_archive=str(rel), current_category=category)
            save()
            work=out/'checks'/rel; work.mkdir(parents=True)
            before=inspect(original)
            assert not before['thin'] and not before['bitcode'] and not before['other'], str(original)
            (work/'before.json').write_text(json.dumps(before,indent=2)+'\n')
            results=[]
            for number in (1,2):
                summary['current_run']=number;save()
                dest=out/('run-'+str(number))/rel;dest.parent.mkdir(parents=True,exist_ok=True)
                shutil.copyfile(original,dest)
                assert inspect(dest)['sha256']==before['sha256']
                measurement=runner.run([*prefix,'-g',str(dest)],work/('strip-'+str(number)),phase='strip')
                log=(work/('strip-'+str(number)+'.log')).read_text()
                assert not log.strip(), 'unexpected strip output: '+log
                after=inspect(dest)
                (work/('after-'+str(number)+'.json')).write_text(json.dumps(after,indent=2)+'\n')
                compare(before,after)
                with dest.open('rb') as stream:
                    for member in after['members']:
                        stream.seek(member['offset']); header=stream.read(20)
                        assert header[:6]==b'\x7fELF\x02\x01' and int.from_bytes(header[16:18],'little')==1 and int.from_bytes(header[18:20],'little')==62
                results.append(dict(sha256=after['sha256'],bytes=after['bytes'],measurement=measurement))
            assert results[0]['sha256']==results[1]['sha256'], 'strip output is not deterministic'
            native=inspect(gnu)
            assert identities(native)==identities(after), 'GNU comparison member identities differ'
            changed_members=[dict(ordinal=a['ordinal'],name=a['name'],occurrence=a['occurrence'],
                                  llvm_sha256=a['sha256'],gnu_sha256=b['sha256'])
                             for a,b in zip(after['members'],native['members']) if a['sha256']!=b['sha256']]
            mapping_equal=Counter(map(tuple,after['index']))==Counter(map(tuple,native['index']))
            difference=('ARCHIVE_IDENTICAL' if after['sha256']==native['sha256'] else
                        'ARCHIVE_CONTAINER_ONLY' if not changed_members else 'ELF_MEMBER_BYTES')
            row=dict(category=category,path=str(rel),original=str(original),original_sha256=before['sha256'],
                     members=after['member_count'],index_entries=after['index_entries'],runs=results,
                     gnu_comparison=str(gnu),gnu_sha256=native['sha256'],difference=difference,
                     changed_members=changed_members,index_mapping_equal_to_gnu=mapping_equal,
                     status='PASS')
            summary['archives'].append(row);save()
            print('LLVM_STRIP_OVERLAY_PASS',category,str(rel),difference,len(changed_members),flush=True)
        summary.update(status='PASS',elapsed_seconds=time.monotonic()-started,
                       categories=dict(Counter(r['difference'] for r in summary['archives'])))
    except BaseException as error:
        runner.cancel();summary.update(status='FAIL',reason=type(error).__name__+': '+str(error),elapsed_seconds=time.monotonic()-started)
        raise
    finally:
        save()


if __name__=='__main__':
    main()
