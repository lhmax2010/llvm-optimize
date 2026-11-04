from common import *
W=Path('/home/linhao/Toolchain/development/llvm-optimize')
B=Path('/home/linhao/Toolchain/development/llvm-optimize-bolt')
s=json.loads((B/'tools/bolt/results/night-results-20261103/summary.json').read_text())
out={}
for project in ['toolchain','basedev']:
 work=W/f'temp/night-20261103/{project}/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/clang-bolt'
 row={'flags':s[project]['flags'],'warning_count':s[project]['warning_count'],'rpm_names':s[project]['rpm_names'],'files':[]}
 for name in ['clang.candidate']+(['clang-22.debug'] if project=='toolchain' else []):
  p=work/name;h=hashlib.sha256()
  with p.open('rb') as f:
   for data in iter(lambda:f.read(1048576),b''):h.update(data)
  row['files'].append({'path':str(p),'bytes':p.stat().st_size,'sha256':h.hexdigest()})
 p=work/'identity.json';identity=json.loads(p.read_text());row['identity']=identity
 out[project]=row
(E/'local-reference.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({k:v['files'] for k,v in out.items()},indent=2))
