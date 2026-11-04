from common import *
import struct,collections
r=json.loads((E/'binary-comparison.json').read_text())['1216409/clang-22.debug'];out={}
def sections(p):
 with p.open('rb') as f:
  h=f.read(64);off=struct.unpack_from('<Q',h,40)[0];sz,n,si=struct.unpack_from('<HHH',h,58);f.seek(off);raw=f.read(sz*n);ss=[struct.unpack_from('<IIQQQQIIQQ',raw,i*sz) for i in range(n)];s=ss[si];f.seek(s[4]);names=f.read(s[5]);tab={names[s[0]:].split(b'\0')[0].decode():s for s in ss};d={}
  for name in ['.GCC.command.line','.comment']:
   s=tab[name];f.seek(s[4]);data=f.read(s[5]);d[name]={'offset':s[4],'size':s[5],'sha256':hashlib.sha256(data).hexdigest(),'strings':dict(collections.Counter(x.decode(errors='replace') for x in data.split(b'\0') if x))}
  return d
for side in ['local','qb']:out[side]=sections(Path(r[side+'_path']))
(E/'1216409/symbol-sections.json').write_text(json.dumps(out,indent=2)+'\n')
for side,d in out.items():
 print(side,'comment',d['.comment']);print(side,'command unique',len(d['.GCC.command.line']['strings']));print(list(d['.GCC.command.line']['strings'])[:2])
