from pathlib import Path
import urllib.request,json,hashlib
W=Path('/home/linhao/Toolchain/development/llvm-optimize');E=W.parent/'llvm-optimize-bolt/tools/bolt/results/qb-meta-switch-20261028';D=Path(__file__).resolve().parent

def request(action,**kw):
 req=urllib.request.Request('http://127.0.0.1:18746',data=json.dumps(dict(action=action,**kw)).encode(),headers={'Content-Type':'application/json'})
 with urllib.request.urlopen(req,timeout=100) as r:return json.load(r)
a=request('navigate',url='https://quickbuild.tizen.org/build/1209720');print(a)
if not a['logged']:raise SystemExit('LOGIN_REQUIRED')
a=request('inspect');(D/'qb-1209720-inspect.json').write_text(json.dumps(a,indent=2,ensure_ascii=False)+'\n');p=E/'qb';p.mkdir(exist_ok=True);request('capture',dir=str(p),name='1209720-overview')
print(a['text'][:4200]);print(json.dumps([l for l in a['links'] if any(s in l['text'].lower() for s in ['log','120','child','profil','build'])],ensure_ascii=False)[:4500])
