from pathlib import Path
import importlib.util,json,hashlib,gzip,time,datetime,traceback,subprocess,struct,collections
W=Path('/home/linhao/Toolchain/development/llvm-optimize');B=W.with_name('llvm-optimize-bolt');E=Path(__file__).parent;S=W/'temp/rebase-359934-20261106/source'
def load(name,p):
 s=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
old=load('old',W/'temp/fifth-review-20261111/rerun3/environment/baseline-llvm-static-archives-native.py');new=load('new',S/'packaging/llvm-static-archives-native.py')
def census(data):
 assert data[:6]==b'\x7fELF\x02\x01'
 shoff=struct.unpack_from('<Q',data,40)[0];entsize,num,strings=struct.unpack_from('<HHH',data,58)
 assert entsize==64 and num>0 and strings<num
 sections=[struct.unpack_from('<IIQQQQIIQQ',data,shoff+i*entsize) for i in range(num)]
 ss=sections[strings];names=data[ss[4]:ss[4]+ss[5]]
 counts=collections.Counter();debug=collections.Counter()
 for sh in sections:
  if sh[1] not in (4,9):continue
  name=names[sh[0]:].split(b'\0',1)[0].decode()
  width=24 if sh[1]==4 else 16
  assert sh[9]==width and sh[5]%width==0
  for offset in range(sh[4],sh[4]+sh[5],width):
   kind=struct.unpack_from('<Q',data,offset+8)[0]&0xffffffff
   counts[kind]+=1
   if name.startswith('.rela.debug_'):debug[kind]+=1
 return counts,debug
totals={};status='failed' 
try:
 with gzip.open(E/'qb-archive-members.jsonl.gz','wt') as out:
  for tag,bid in [('toolchain','1225393'),('basedev','1225395')]:
   root=W/'temp/fifth-review-20261111/rerun3/qb-payload'/tag
   root.mkdir(parents=True,exist_ok=False)
   rpms=list((W/'temp/qb-1225393-1225395'/bid/'x86_64/rpms').glob('llvm-static-devel-*.rpm'))
   assert len(rpms)==1,rpms
   rpm=rpms[0]
   manifest=json.loads(gzip.decompress((B/'tools/bolt/results/qb-1225393-1225395/manifests'/bid/'x86_64'/(rpm.name+'.json.gz')).read_bytes()))
   with (E/(tag+'-extract.stderr')).open('wb') as err:
    p1=subprocess.Popen(['rpm2cpio',str(rpm)],stdout=subprocess.PIPE,stderr=err)
    p2=subprocess.Popen(['cpio','-idm','--no-absolute-filenames','*.a'],stdin=p1.stdout,stderr=err,cwd=root)
    p1.stdout.close();rc2=p2.wait();rc1=p1.wait()
   assert rc1==rc2==0,(rc1,rc2)
   (E/(tag+'-rpm-source.json')).write_text(json.dumps(dict(path=str(rpm),bytes=rpm.stat().st_size,sha256=hashlib.file_digest(rpm.open('rb'),'sha256').hexdigest(),commands=[['rpm2cpio',str(rpm)],['cpio','-idm','--no-absolute-filenames','*.a']],output=str(root)),indent=2)+'\n')
   summary=json.loads((W/'temp/night-20261103'/tag/'gbs-root/local/BUILD-ROOTS/scratch.x86_64.0/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/native-archive-conversion/summary.json').read_text())
   records={r['path']:r for r in summary['archives']}
   expected=sorted(k for k in manifest if k.endswith('.a'))
   paths=sorted(str(p.relative_to(root)) for p in root.rglob('*.a'))
   assert paths==expected and len(paths)==225,(tag,len(paths),len(expected))
   total=dict(qb=bid,archives=0,members=0,converted=0,preserved=0,old_checked=0,new_checked=0,old_preserved_forbidden=0,new_preserved_forbidden=0,new_rejections=0,bytes=0,PASS=True,relocation_census={},debug_relocation_census={},unknown_types=[])
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
      counts,debug_counts=census(data)
      for key,value in counts.items():total['relocation_census'][str(key)]=total['relocation_census'].get(str(key),0)+value
      for key,value in debug_counts.items():total['debug_relocation_census'][str(key)]=total['debug_relocation_census'].get(str(key),0)+value
      unknown=set(counts)-set(new.X86_64_RELOCATION_WIDTHS)
      if unknown:total['unknown_types']+=sorted(unknown)
      assert not unknown,(name,m['name'],unknown)
      old_elf=old.elf_details(data);new_elf=new.elf_details(data)
      old_pic=old.pic_relocations(data);new_pic=new.pic_relocations(data)
      row=dict(qb=bid,archive=name,ordinal=m['ordinal'],name=m['name'],sha256=m['sha256'],bytes=m['size'],preserved=preserved,old=old_pic,new=new_pic,elf_details_equal=old_elf==new_elf,relocation_census=dict(counts),debug_relocation_census=dict(debug_counts))
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
