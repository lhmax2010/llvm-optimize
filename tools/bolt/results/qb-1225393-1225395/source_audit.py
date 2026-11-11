from pathlib import Path
import json,subprocess,difflib,hashlib,datetime
from rpm_extract import extract_selected
E=Path(__file__).resolve().parent
W=Path('/home/linhao/Toolchain/development/llvm-optimize')
S=W/'temp/rebase-359934-20261106/source'
X=W/'temp/qb-1225393-1225395'
rows=json.loads((E/'package-results.json').read_text())
def git(*args):return subprocess.check_output(['git','-C',str(S),*args],timeout=30)
old='a65688b1377e91819fcd46a18da36d52b3312089';new='8a50d7122346258fd1171d270861a4ae28a8717c'
om=git('show','-s','--format=%B',old).decode().strip();nm=git('show','-s','--format=%B',new).decode().strip()
(E/'hybrid-message.diff').write_text(''.join(difflib.unified_diff(om.splitlines(True),nm.splitlines(True),fromfile=old,tofile=new)))
print((E/'hybrid-message.diff').read_text())
# Exact two authorized prose changes, ignoring only wrapping.
oldparas=om.split('\n\n');newparas=nm.split('\n\n')
print('OLD PARAS',json.dumps(oldparas,ensure_ascii=False))
print('NEW PARAS',json.dumps(newparas,ensure_ascii=False))
audit=[]
for row in rows:
 if row['status']!='SOURCE_AUDIT_PENDING':continue
 assert not row['added'] and not row['removed']
 names={x['file'] for x in row['changes']}
 assert names=={'llvm.spec','llvm-static-archives-native.py','0008-cmake-use-hybrid-LLVM-linkage-on-x86_64.patch'}
 for side in ['old','new']:
  d=X/'source-audit'/row['build']/side
  extract_selected(row[side]['path'],names,d)
 a=X/'source-audit'/row['build']/'old';b=a.parent/'new'
 patch='0008-cmake-use-hybrid-LLVM-linkage-on-x86_64.patch'
 aa=(a/patch).read_bytes();bb=(b/patch).read_bytes()
 bodya=aa[aa.index(b'diff --git '):];bodyb=bb[bb.index(b'diff --git '):];assert bodya==bodyb
 for content,rev in [(aa,old),(bb,new)]:
  exported=git('format-patch','-1','--stdout',rev)
  # GBS may use a different [PATCH] sequence label; commit message and diff body must match.
  start=content.index(b'\nSubject: ');end=content.index(b'\n---\n')
  c=content[start:end].decode();ex=exported[exported.index(b'\nSubject: '):exported.index(b'\n---\n')].decode()
  import re
  norm=lambda s:re.sub(r'\[PATCH[^\]]*\]', '[PATCH]',s)
  assert norm(c)==norm(ex),(rev,c,ex)
 for f in names:
  ad=(a/f).read_text();bd=(b/f).read_text()
  (E/(row['build']+'-'+f+'.diff')).write_text(''.join(difflib.unified_diff(ad.splitlines(True),bd.splitlines(True),fromfile='old/'+f,tofile='new/'+f)))
 assert (a/'llvm-static-archives-native.py').read_bytes()==git('show','fa4f9978:packaging/llvm-static-archives-native.py')
 assert (b/'llvm-static-archives-native.py').read_bytes()==git('show','60fabc72:packaging/llvm-static-archives-native.py')
 audit.append({'build':row['build'],'files':sorted(names),'patch_diff_body_equal':True,'message_matches_git':True,
  'body_sha256':hashlib.sha256(bodya).hexdigest(),'status':'PASS'})
(E/'source-audit.json').write_text(json.dumps(audit,indent=2)+'\n')
print('SOURCE AUDIT',audit)
