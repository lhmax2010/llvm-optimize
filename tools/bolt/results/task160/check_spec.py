import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'candidates'))
import candidate as c

p = ROOT.parents[1] / "temp/task131/pgo-dev/packaging/llvm.spec"
d = ROOT/'spec-parse'
data={}
for arch in ('x86_64','aarch64','armv7l'):
    for mode in ('default','without-bolt','without-speedup'):
        if arch != 'x86_64' and mode != 'default':
            continue
        original=c.logged
        def log_with_mode(*args,**kwargs):
            name,cmd=args[1:3]
            if mode!='default' and name.startswith('retry-'):
                macro={'without-bolt':'_without_clang_bolt 1','without-speedup':'_without_llvm_speedup 1'}[mode]
                cmd=[*cmd[:-1],'--define',macro,cmd[-1]]
            return original(args[0],name,cmd,**kwargs)
        c.logged=log_with_mode
        try:
            output=c.expand(d,'retry-'+mode,arch,p)
        finally:
            c.logged=original
        rows=[line for line in output.splitlines() if '--address-space-bytes' in line]
        if arch=='x86_64':
            assert len(rows)==1 and '--jobs 4 --address-space-bytes 4294967296 --retry-address-space-bytes 8589934592' in rows[0]
            assert ('bolt_status_exit' in rows[0]) == (mode=='default')
        else:
            assert not rows
        data[arch+'/'+mode]={'status':'PASS','lines':rows}
print(json.dumps(data,indent=2))
