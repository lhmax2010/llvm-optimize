from pathlib import Path
import json,os,collections
E=Path(__file__).resolve().parent;W=Path('/home/linhao/Toolchain/development/llvm-optimize');T=W/'temp'
assert (E/'hash-complete.json').exists()
u=json.loads((E/'units.json').read_text());sub=json.loads((E/'subunits.json').read_text());hard=json.loads((E/'hardlinks.json').read_text());assets=json.loads((E/'assets-found.json').read_text());hashed=json.loads((E/'asset-hashes.json').read_text())+json.loads((E/'asset-hashes-supplement.json').read_text())+json.loads((E/'asset-hashes-inode-aliases.json').read_text());runtime=json.loads((E/'runtime-preservation.json').read_text())['files']
du={r['path']:r for r in u+sub};hh={x['path']:x for x in hashed if 'sha256' in x};allhash=collections.defaultdict(list)
for x in hashed:
 if 'sha256' in x:allhash[x['sha256']].append(x['path'])
conservative=[str(T/'bolt-v4-20261022-cache-release/baseline-root'),str(T/'bolt-v4-20261022-cache-release/revised-root'),str(T/'hybrid-local-20261023/gbs-root'),str(T/'bolt-on-hybrid-20261024/gbs-root'),'/var/tmp/llvm-optimize-x86-archivefix-20261013/local/BUILD-ROOTS/scratch.x86_64.0/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/lto.cache']
extra=[str(T/'toolchain-archivefix-v2-final'),str(T/'toolchain-llvm-strip'),str(T/'toolchain-release-x86-20261013'),str(T/'bolt-v4-20261016-source-order/upper-parse'),'/var/tmp/llvm-optimize-archivefix-v2-final-20261009/independent-install']
def inside(p,roots):return any(p==r or p.startswith(r+'/') for r in roots)
def reclaim(roots):
 gross=sum(du[r]['bytes'] for r in roots);subtract=0;details=[]
 for key,h in hard.items():
  present=[p for p in h['paths'] if inside(p,roots)];count=sum(any(p==r or p.startswith(r+'/') for p in present) for r in roots)
  if not count:continue
  # du counts each inode once in each independently measured selected scope.
  # If any link survives (including outside scan), its data blocks are not freed.
  survives=len(present)<h['nlink'];delta=(count if survives else count-1)*h['allocated']
  if delta:subtract+=delta;details.append(dict(inode=key,bytes_subtracted=delta,links_inside=len(present),nlink=h['nlink'],paths=h['paths']))
 return dict(gross_du_bytes=gross,hardlink_adjustment=subtract,estimated_unlinked_bytes=gross-subtract,adjustments=details)
# Preserve every RPM in selected roots, plus identity/profile/key compiler assets.
# Unknown duplicate hashes are conservatively charged as an extra copy.
saves=[]
for x in assets:
 p=x['path'];name=Path(p).name
 if not inside(p,conservative):continue
 if not (p.endswith('.rpm') or name in ['clang-22','ordinary-clang-22','llvm-bolt','identity.json','profile.fdata','clang-bolt-v2.fdata.xz']):continue
 z=dict(x);h=hh.get(p,{}).get('sha256');copies=[q for q in allhash.get(h,[]) if not inside(q,conservative+extra)] if h else []
 z.update(sha256=h,same_sha_outside_plan=copies,action='already preserved' if copies else 'save before delete');saves.append(z)
for x in runtime:
 saves.append(dict(x,path=x['resolved'],same_sha_outside_plan=[],action='save before delete',reason='docs34 Tizen runtime/resource; symlink layout must also be preserved'))
# Deduplicate copies by content where hashed; otherwise by inode (not basename).
seen=set();copybytes=0
for x in saves:
 x['copy_budget_allocated']=0
 if x['action']!='save before delete':continue
 key=('sha',x['sha256']) if x.get('sha256') else ('inode',x.get('dev'),x.get('ino'))
 if key not in seen:seen.add(key);x['copy_budget_allocated']=x['allocated'];copybytes+=x['allocated']
plans={}
for label,roots in [('conservative',conservative),('aggressive',conservative+extra)]:
 fs={}
 for name,prefix in [('home','/home/'),('var_tmp','/var/tmp/')]:
  rr=[r for r in roots if r.startswith(prefix)];v=reclaim(rr);v['paths']=rr;v['copy_budget_allocated']=copybytes if name=='home' else 0;v['net_reclaim_estimate']=v['estimated_unlinked_bytes']-v['copy_budget_allocated'];fs[name]=v
 plans[label]=fs
(E/'preserve-before-delete.json').write_text(json.dumps(saves,indent=2)+'\n')
(E/'scenarios.json').write_text(json.dumps(plans,indent=2)+'\n')
(E/'asset-duplicates.json').write_text(json.dumps({k:v for k,v in allhash.items() if len(v)>1},indent=2)+'\n')
print(json.dumps({k:{f:{x:z for x,z in v.items() if x not in ['adjustments','paths']} for f,v in fs.items()} for k,fs in plans.items()},indent=2))
