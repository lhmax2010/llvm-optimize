from pathlib import Path
import importlib.util,json,hashlib,gzip,time,sys,datetime
W=Path('/home/linhao/Toolchain/development/llvm-optimize');B=W.with_name('llvm-optimize-bolt');E=Path(__file__).parent;S=W/'temp/rebase-359934-20261106/source'
spec=importlib.util.spec_from_file_location('converter',S/'packaging/llvm-static-archives-native.py');a=importlib.util.module_from_spec(spec);spec.loader.exec_module(a)
totals={}
with gzip.open(E/'qb-archive-members.jsonl.gz','wt') as out:
 for tag,bid in [('toolchain','1221204'),('basedev','1221207')]:
  root=W/'temp/qb-1221204-1221207/payload'/tag/'llvm-static-devel-x86_64/new'
  manifest=json.loads((B/'tools/bolt/results/qb-1221204-1221207/comparison/manifests'/tag/'llvm-static-devel-x86_64-new.json').read_text())
  expected=sorted(k for k in manifest if k.endswith('.a'))
  paths=sorted(str(p.relative_to(root)) for p in root.rglob('*.a'))
  assert paths==expected and len(paths)==225,(tag,len(paths),len(expected))
  total=dict(qb=bid,archives=0,members=0,relocations=0,forbidden=0,bytes=0,PASS=True)
  for name in paths:
   p=root/name;info=a.inspect(p)
   assert info['sha256']==manifest[name]['sha256'],name
   assert info['bytes']==manifest[name]['bytes'] and not info['thin'] and info['other']==0 and info['bitcode']==0,name
   assert info['index_equals_machine_symbols'],name
   with p.open('rb') as f:
    for m in info['members']:
     f.seek(m['offset']);data=f.read(m['size']);assert hashlib.sha256(data).hexdigest()==m['sha256']
     check=a.pic_relocations(data)
     row=dict(qb=bid,archive=name,ordinal=m['ordinal'],name=m['name'],sha256=m['sha256'],bytes=m['size'],**check)
     out.write(json.dumps(row)+'\n')
     assert not check['forbidden'],row
     total['members']+=1;total['relocations']+=check['checked']
   total['archives']+=1;total['bytes']+=info['bytes']
   if total['archives']%25==0:print(tag,json.dumps(total),flush=True)
  totals[tag]=total;print(tag,json.dumps(total),flush=True)
(E/'qb-archive-summary.json').write_text(json.dumps(totals,indent=2)+'\n')
print('ARCHIVE_CHECK 已结束',datetime.datetime.now().astimezone().isoformat(),'status=ok')
