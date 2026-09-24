#!/usr/bin/env python3
"""Compare native vs ThinLTO-IR/native section and symbol structure on one real TU.

Run inside a bounded scope. Does not convert archives or certify differences;
all differences are recorded for review before any archive conversion proceeds.
Uses the saved ARM sidecar without retargeting its preprocessed input.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import subprocess

from convert_static_archives import BACKEND_FLAGS, Commands


def describe(path, output):
    result = {}
    for option, name in [('-SW','sections'), ('-rW','relocations'), ('-sW','symbols')]:
        p = subprocess.run(['readelf', option, str(path)], text=True, capture_output=True, check=True)
        (output/(path.stem+'-'+name+'.txt')).write_text(p.stdout+p.stderr)
        result[name+'_raw'] = p.stdout
    sections = []
    for line in result['sections_raw'].splitlines():
        m = re.match(r'\s*\[\s*\d+\]\s+(\S+)\s+\S+\s+[0-9a-f]+\s+[0-9a-f]+\s+([0-9a-f]+)',line)
        if m and m[1] != 'NULL':
            sections.append(m[1])
    symbols = []
    for line in result['symbols_raw'].splitlines():
        m = re.match(r'\s*\d+:\s+\S+\s+\S+\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)(?:\s+(.*))?$',line)
        if m and m[4] != 'UND' and m[1] not in ('SECTION','FILE') and m[5]:
            symbols.append((m[5],m[1],m[2],m[3]))
    return dict(sha256=hashlib.sha256(path.read_bytes()).hexdigest(), bytes=path.stat().st_size,
                section_count=len(sections), sections=dict(Counter(sections)),
                text_function_sections=sum(s.startswith('.text.') for s in sections),
                relocations=dict(Counter(re.findall(r'\bR_[A-Z0-9_]+\b',result['relocations_raw']))),
                defined_symbols=symbols)


def differences(a,b):
    result = {}
    for field in ('sections','relocations','defined_symbols'):
        left=Counter(map(tuple,a[field])) if field=='defined_symbols' else Counter(a[field])
        right=Counter(map(tuple,b[field])) if field=='defined_symbols' else Counter(b[field])
        result[field] = dict(only_native=list((left-right).items()), only_ir_native=list((right-left).items()))
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--baseline',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--loader',required=True)
    p.add_argument('--library-path',required=True)
    a=p.parse_args();a.output.mkdir(parents=True,exist_ok=False)
    w=Path(__file__).resolve().parents[1]
    side=w/'tools/bench_inputs/real_tu/llvm_mc_AsmParser.flags.json'
    data=json.loads(side.read_text());ii=side.with_name(side.name.replace('.flags.json','.ii'))
    assert hashlib.sha256(ii.read_bytes()).hexdigest()==data['sha256']
    sysroot=next(f.split('=',1)[1] for f in data['preprocess_command'] if f.startswith('--sysroot='))
    assert Path(sysroot).is_dir()
    prefix=[a.loader,'--library-path',a.library_path,str(a.baseline/'usr/bin/clang-22'),
            '--no-default-config','--driver-mode=g++','--target='+data['target'],
            '--sysroot='+sysroot,'-resource-dir='+str(a.baseline/'usr/lib64/clang/22')]
    original=[f for f in data['flags'] if not f.startswith('-flto')]
    commands={
      'native':[*prefix,*original,'-x','c++-cpp-output','-c',str(ii),'-o',str(a.output/'native.o')],
      'bitcode':[*prefix,*original,'-flto=thin','-x','c++-cpp-output','-c',str(ii),'-o',str(a.output/'thin.bc')],
      'ir-native':[*prefix,*BACKEND_FLAGS,'-fPIC','-x','ir','-c',str(a.output/'thin.bc'),'-o',str(a.output/'ir-native.o')]}
    plan=dict(sidecar=str(side),sidecar_sha256=hashlib.sha256(side.read_bytes()).hexdigest(), input_sha256=data['sha256'],commands=commands,
              reason='Sidecar intentionally strips LTO; restore the original command ThinLTO option only in route B.',backend_flags=BACKEND_FLAGS)
    (a.output/'plan.json').write_text(json.dumps(plan,indent=2)+'\n')
    runner=Commands()
    try:
        for name,command in commands.items():
            dry=subprocess.run([*command,'-###'],text=True,capture_output=True,check=True)
            (a.output/(name+'-driver.txt')).write_text(dry.stdout+dry.stderr)
            runner.run(command,a.output/name)
        runner.run([a.loader,'--library-path',a.library_path,str(a.baseline/'usr/bin/llvm-dis'),str(a.output/'thin.bc'),'-o',str(a.output/'thin.ll')],a.output/'disassemble')
        left=describe(a.output/'native.o',a.output);right=describe(a.output/'ir-native.o',a.output)
        delta=differences(left,right)
        result=dict(status='REVIEW_REQUIRED' if any(v['only_native'] or v['only_ir_native'] for v in delta.values()) else 'PASS',
                    native=left,ir_native=right,differences=delta)
        (a.output/'comparison.json').write_text(json.dumps(result,indent=2)+'\n')
        print(json.dumps({k:v for k,v in result.items() if k not in ('native','ir_native')},indent=2))
    except BaseException as error:
        runner.cancel();(a.output/'failure.json').write_text(json.dumps(dict(reason=str(error)),indent=2)+'\n');raise


if __name__=='__main__':main()
