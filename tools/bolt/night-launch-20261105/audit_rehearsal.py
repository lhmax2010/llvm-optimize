from pathlib import Path
import json,re,shlex,sys,hashlib
from validate import flags
from log_support import audit_log_copy
T=Path(__file__).parent;W=Path('/home/linhao/Toolchain/development/llvm-optimize');D=W/'temp/night-20261105/rehearsal/toolchain';D=D/'retry-02' if '--retry-02' in sys.argv else D;E=D/'evidence';q=json.loads((T/'qb-reference.json').read_text());result=json.loads((E/'result.json').read_text());assert result['status']=='ok',result
lines=(E/'rpm-build-final.log').read_text().splitlines();actual=flags(lines);assert actual==[r['text'] for r in q['flags']],(actual,q['flags'])
cs=[l for l in lines if '+ cmake -G Ninja ' in l];assert len(cs)==1;keys=['CMAKE_C_FLAGS','CMAKE_CXX_FLAGS','CMAKE_EXE_LINKER_FLAGS','CMAKE_SHARED_LINKER_FLAGS']
def extract(s):
 argv=shlex.split(s.split('+ ',1)[1]);return {k:next(a.split('=',1)[1] for a in argv if a.startswith('-D'+k+'=')) for k in keys}
cm=extract(cs[0]);expected=extract(q['cmake'][0]['text']);assert cm==expected,(cm,expected)
a=json.loads((E/'final-audit.json').read_text());assert not a['mounts']['stdout'] and not a['remaining_build_processes'];assert not any('+ ninja ' in l for l in lines)
src=D/'gbs-root/local/BUILD-ROOTS/scratch.x86_64.0/.build.log';dst=E/'rpm-build.log'
assert src.read_bytes()==dst.read_bytes()
copy_sha=hashlib.sha256(src.read_bytes()).hexdigest()
r=dict(log_copy_sha256=copy_sha,PASS=True,result=result,flags=actual,cmake=cm,cmake_raw=cs[0],log_copy=audit_log_copy(D),cleanup=a)
(E/'rehearsal-audit.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
