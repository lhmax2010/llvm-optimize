from pathlib import Path
import json,subprocess,difflib,hashlib,datetime,gzip,re
from rpm_extract import extract_selected
E=Path(__file__).resolve().parent
W=Path('/home/linhao/Toolchain/development/llvm-optimize')
S=W/'temp/rebase-359934-20261111-r6/source'
X=W/'temp/qb-1226850-1226851/source-audit'
old='60fabc723f30c5cc04146a9dd83487ebed63f259';new='fea0fe464d56e17f2c7588c557bfffd9f6ac352b'
def git(*a):return subprocess.check_output(['git','-C',str(S),*a],timeout=60)
rows=json.loads((E/'package-results.json').read_text());out=[]
for row in rows:
 if row['status']!='SOURCE_AUDIT_PENDING':continue
 names={x['file'] for x in row['changes']}
 assert names=={'llvm.spec','clang-bolt-helper.py','llvm-static-archives-native.py'},names
 assert not row['added'] and not row['removed']
 with gzip.open(E/'manifests'/row['build']/row['arch']/(row['name']+'.json.gz'),'rt') as f:manifest=json.load(f)
 patches=sorted(n for n in manifest if re.match(r'000[1-8]-.*\.patch$',n))
 assert len(patches)==8,patches
 for side in ['old','new']:extract_selected(row[side]['path'],names|set(patches),X/row['build']/side)
 a=X/row['build']/'old';b=a.parent/'new'
 proofs=[]
 for fn in sorted(names):
  aa=(a/fn).read_bytes();bb=(b/fn).read_bytes()
  (E/(row['build']+'-'+fn+'.diff')).write_text(''.join(difflib.unified_diff(aa.decode().splitlines(True),bb.decode().splitlines(True),fromfile='old/'+fn,tofile='new/'+fn)))
  gd=git('diff','--full-index',old,new,'--','packaging/'+fn)
  gp=E/('git-60fabc72-fea0fe46-'+fn+'.diff')
  if not gp.exists():gp.write_bytes(gd)
  if fn!='llvm.spec':
   assert aa==git('show',old+':packaging/'+fn)
   assert bb==git('show',new+':packaging/'+fn)
   proofs.append(dict(file=fn,old_matches_git=True,new_matches_git=True,status='PASS'))
  else:
   target=a.parent/'expected-from-git.spec';target.write_bytes(aa)
   cmd=['patch','--batch','--forward','--fuzz=0',str(target),str(gp)]
   p=subprocess.run(cmd,capture_output=True,text=True)
   (E/(row['build']+'-spec-git-patch-proof.txt')).write_text(repr(cmd)+'\n'+p.stdout+p.stderr+'\nrc='+str(p.returncode)+'\n')
   assert p.returncode==0,p.stdout+p.stderr
   before=target.read_bytes()
   av=re.findall(rb'^VCS:.*$',before,re.M);bv=re.findall(rb'^VCS:.*$',bb,re.M)
   assert len(av)==len(bv)==1 and old.encode() in av[0] and new.encode() in bv[0],(av,bv)
   assert before.replace(av[0],bv[0],1)==bb
   proofs.append(dict(file=fn,unmodified_git_patch_applied_with_fuzz_zero=True,VCS_old=av[0].decode(),VCS_new=bv[0].decode(),all_remaining_bytes_equal=True,status='PASS'))
 ps=[]
 for fn in patches:
  aa=(a/fn).read_bytes();bb=(b/fn).read_bytes();assert aa==bb,fn
  ps.append(dict(file=fn,sha256=hashlib.sha256(aa).hexdigest(),bytes=len(aa),status='PASS'))
 out.append(dict(build=row['build'],baseline=row['baseline'],changes=proofs,patches=ps,status='PASS'))
 print('SOURCE',row['build'],'PASS 3 files exactly git delta + VCS; 8 patches identical',flush=True)
(E/'source-audit.json').write_text(json.dumps(out,indent=2)+'\n')
end='B4 已结束 '+datetime.datetime.now().astimezone().isoformat()+' PASS'
(E/'b4-end.txt').write_text(end+'\n');print(end)
