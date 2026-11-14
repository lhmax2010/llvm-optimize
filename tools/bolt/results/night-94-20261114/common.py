import ast,struct,mmap,hashlib,json
from pathlib import Path
E=Path(__file__).resolve().parent; B=E.parents[3]
p=B/'tools/bolt/results/night-92-20261114/tls_forms.py'
n=next(n for n in ast.parse(p.read_text()).body if isinstance(n,ast.ClassDef) and n.name=='ELF')
exec(compile(ast.Module(body=[n],type_ignores=[]),str(p),'exec'))
def sha(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def save(n,x): (E/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def symbols(e):
 out=[]
 for s in e.s:
  if s['type']!=2:continue
  for o in range(s['offset'],s['offset']+s['size'],s['entsize']):
   name,info,other,ndx,v,size=struct.unpack_from('<IBBHQQ',e.m,o)
   if info&15==2 and ndx<len(e.s) and e.s[ndx]['flags']&4:
    out.append(dict(name=e.string(e.s[s['link']],name),section=e.s[ndx]['name'],address=v,size=size))
 return out
ids=json.loads((B/'tools/bolt/results/night-93-20261114/identities.json').read_text())
