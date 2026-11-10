from pathlib import Path
import importlib.util,json,hashlib,gzip,time,datetime,traceback
W=Path('/home/linhao/Toolchain/development/llvm-optimize');B=W.with_name('llvm-optimize-bolt');E=Path(__file__).parent;S=W/'temp/rebase-359934-20261106/source'
def load(name,p):
 s=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
old=load('old',E/'baseline-llvm-static-archives-native.py');new=load('new',S/'packaging/llvm-static-archives-native.py')
totals={};status='failed'
try:
 with gzip.open(E/'qb-archive-members.jsonl.gz','wt') as out:
  for tag,bid in [('toolchain','1223601'),('basedev','1223602')]:
   root=W/'temp/qb-1223601-1223602/payload'/tag/'llvm-static-devel-x86_64/new'
   manifest=json.loads((B/'tools/bolt/results/qb-1223601-1223602/comparison/manifests'/tag/'llvm-static-devel-x86_64-new.json').read_text())
   summary=json.loads((W/'temp/night-20261103'/tag/'gbs-root/local/BUILD-ROOTS/scratch.x86_64.0/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/native-archive-conversion/summary.json').read_text())
   records={r['path']:r for r in summary['archives']}
   expected=sorted(k for k in manifest if k.endswith('.a'))
   paths=sorted(str(p.relative_to(root)) for p in root.rglob('*.a'))
   assert paths==expected and len(paths)==225,(tag,len(paths),len(expected))
   total=dict(qb=bid,archives=0,members=0,converted=0,preserved=0,old_checked=0,new_checked=0,old_preserved_forbidden=0,new_preserved_forbidden=0,new_rejections=0,bytes=0,PASS=True)
   totals[tag]=total
   for name in paths:
    p=root/name;info=new.inspect(p);prior=old.inspect(p)
    assert info==prior,('ar parser differs',name)
    assert info['sha256']==manifest[name]['sha256'] and info['bytes']==manifest[name]['bytes'],name
    assert not info['thin'] and info['other']==0 and info['bitcode']==0 and info['index_equals_machine_symbols'],name
    record=records[name];results={m['ordinal']:m for m in record['results']}
    assert record['members']==info['member_count'],name
    with p.open('rb') as f:
     for m in info['members']:
      f.seek(m['offset']);data=f.read(m['size']);assert hashlib.sha256(data).hexdigest()==m['sha256']
      assert results[m['ordinal']]['name']==m['name']
      preserved=results[m['ordinal']]['preserved']
      old_elf=old.elf_details(data);new_elf=new.elf_details(data)
      old_pic=old.pic_relocations(data);new_pic=new.pic_relocations(data)
      row=dict(qb=bid,archive=name,ordinal=m['ordinal'],name=m['name'],sha256=m['sha256'],bytes=m['size'],preserved=preserved,old=old_pic,new=new_pic,elf_details_equal=old_elf==new_elf)
      out.write(json.dumps(row)+'\n')
      assert old_elf==new_elf,row
      assert old_pic==new_pic,row
      if not preserved:assert not new_pic['forbidden'],row
      total['members']+=1;total['preserved' if preserved else 'converted']+=1
      total['old_checked']+=old_pic['checked'];total['new_checked']+=new_pic['checked']
      if preserved:
       total['old_preserved_forbidden']+=len(old_pic['forbidden']);total['new_preserved_forbidden']+=len(new_pic['forbidden'])
    total['archives']+=1;total['bytes']+=info['bytes']
    if total['archives']%25==0:print(tag,json.dumps(total),flush=True)
   assert total['converted']==3853,(tag,total)
  status='ok'
except BaseException:
 (E/'qb-archive-failure.txt').write_text(traceback.format_exc());raise
finally:
 (E/'qb-archive-summary.json').write_text(json.dumps(dict(status=status,totals=totals),indent=2)+'\n')
 print('ARCHIVE_CHECK 已结束',datetime.datetime.now().astimezone().isoformat(),'status='+status,flush=True)
