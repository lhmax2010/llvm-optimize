from pathlib import Path
import json,subprocess,difflib,hashlib,datetime,re
from rpm_extract import extract_selected
E=Path(__file__).resolve().parent;W=Path('/home/linhao/Toolchain/development/llvm-optimize');S=W/'temp/rebase-359934-20261106/source';X=W/'temp/qb-1225393-1225395'
def git(*args):return subprocess.check_output(['git','-C',str(S),*args],timeout=30)
old='a65688b1377e91819fcd46a18da36d52b3312089';new='8a50d7122346258fd1171d270861a4ae28a8717c'
om=git('show','-s','--format=%B',old).strip();nm=git('show','-s','--format=%B',new).strip()
added=b'AddLLVM.cmake and AddClang.cmake are installed on every architecture,\nso the llvm-devel and clang payloads on armv7l and aarch64 carry the\nnew text. TIZEN_HYBRID_LINK is set only by the x86_64 recipe; elsewhere\nthe new function returns at once and the generated build is unchanged.\n\n'
assert nm==om.replace(b' Quickbuild verification remains pending.',b'').replace(b'Signed-off-by:',added+b'Signed-off-by:')
audit=[]
for row in json.loads((E/'package-results.json').read_text()):
 if row['status']!='SOURCE_AUDIT_PENDING':continue
 assert not row['added'] and not row['removed']
 names={x['file'] for x in row['changes']}
 assert names=={'llvm.spec','llvm-static-archives-native.py','0008-cmake-use-hybrid-LLVM-linkage-on-x86_64.patch'}
 for side in ['old','new']:
  d=X/'source-audit'/row['build']/side
  if not d.exists():extract_selected(row[side]['path'],names,d)
 a=X/'source-audit'/row['build']/'old';b=a.parent/'new';patch='0008-cmake-use-hybrid-LLVM-linkage-on-x86_64.patch'
 aa=(a/patch).read_bytes();bb=(b/patch).read_bytes()
 bodya=aa[aa.index(b'diff --git '):];bodyb=bb[bb.index(b'diff --git '):];assert bodya==bodyb
 for content,msg in [(aa,om),(bb,nm)]:
  # Compare the actual Subject title and body directly to the Git commit message.
  # GBS omits the format-patch [PATCH] email prefix; it is not commit prose.
  subj=content.split(b'\nSubject: ',1)[1].split(b'\n---\n',1)[0]
  assert subj==msg,(subj,msg)
 for f in names:
  ad=(a/f).read_text();bd=(b/f).read_text()
  (E/(row['build']+'-'+f+'.diff')).write_text(''.join(difflib.unified_diff(ad.splitlines(True),bd.splitlines(True),fromfile='old/'+f,tofile='new/'+f)))
 assert (a/'llvm-static-archives-native.py').read_bytes()==git('show','fa4f9978:packaging/llvm-static-archives-native.py')
 assert (b/'llvm-static-archives-native.py').read_bytes()==git('show','60fabc72:packaging/llvm-static-archives-native.py')
 audit.append({'build':row['build'],'files':sorted(names),'patch_diff_body_equal':True,'message_matches_git':True,
 'exactly_two_authorized_message_changes':True,'body_sha256':hashlib.sha256(bodya).hexdigest(),'status':'PASS'})
(E/'source-audit.json').write_text(json.dumps(audit,indent=2)+'\n')
print(json.dumps(audit,indent=2))
end='ITEM2 已结束 '+datetime.datetime.now().astimezone().isoformat()+' status=ok reason=102_binary_payloads_and_two_source_whitelists_pass'
(E/'item2-ending.txt').write_text(end+'\n');print(end)
# Item3 source-only precheck.
diff=git('diff','--full-index','463c9a13','13c3e223')
(E/'ps7-to-ps10.diff').write_bytes(diff)
stat=git('diff','--stat','463c9a13','13c3e223');(E/'ps7-to-ps10.stat').write_bytes(stat);print(stat.decode())
print(git('diff','--name-only','463c9a13','13c3e223').decode())
spec=git('show','13c3e223:packaging/llvm.spec').decode()
lines=spec.splitlines()
hits=[i for i,s in enumerate(lines) if 'SOURCE1005' in s or 'llvm-static-archives-native' in s]
(E/'ps10-converter-spec-context.txt').write_text('\n'.join(f'{i+1}: {lines[i]}' for hit in hits for i in range(max(0,hit-25),min(len(lines),hit+30)))+'\n')
