from pathlib import Path
import subprocess,json,textwrap,re,hashlib,difflib
E=Path(__file__).resolve().parent;W=E.parents[1];S=W/'temp/bolt-v4-20261013/v41/llvm-source';old='af82efed1a688ba0877a4b4ca723922abbc96d20'
def git(*a):return subprocess.check_output(['git','-C',str(S),*a])
assert git('rev-parse','HEAD^{tree}')==git('rev-parse',old+'^{tree}')
assert not git('status','--porcelain')
raw=git('cat-file','commit',old);message=raw.split(b'\n\n',1)[1];oldtext=message.decode();lines=oldtext.splitlines();newlines=['packaging: optimize x86_64 clang with BOLT']
pending=[];kind=None
def flush():
 if pending:
  chunks=textwrap.wrap(' '.join(pending),width=72,break_long_words=False,break_on_hyphens=False,replace_whitespace=False)
  if kind=='paths':assert all(chunk.endswith(',') for chunk in chunks[:-1])
  newlines.extend(chunks);pending.clear()
for line in lines[1:]:
 if not line:
  flush();kind=None;newlines.append('');continue
 if line.startswith(('Change-Id:','Signed-off-by:')):
  flush();kind=None;newlines.append(line);continue
 current='paths' if line.startswith(('build/tools/clang/','clang/tools/driver/')) else 'prose'
 if kind!=current:flush()
 kind=current;pending.append(line)
flush()
newtext='\n'.join(newlines)+'\n'
assert len(newlines[0])<=50 and max(map(len,newlines))<=72
assert ' '.join(oldtext.split('\n',1)[1].split())==' '.join(newtext.split('\n',1)[1].split())
for line in lines:
 if line.startswith(('build/tools/clang/','clang/tools/driver/')):
  chunks=textwrap.wrap(line,width=72,break_long_words=False,break_on_hyphens=False)
  assert all(chunk.endswith(',') for chunk in chunks[:-1])
  assert all(token in newtext for token in line.split())
for trailer in ['Change-Id: Ic98eab90cc017f127a66e1729b44fab8b8e8fb41','Signed-off-by: Hao Lin <hao.lin@samsung.com>']:assert oldtext.splitlines().count(trailer)==newlines.count(trailer)==1
(E/'old.commit').write_bytes(raw);(E/'old-message.txt').write_bytes(message);(E/'new-message.txt').write_text(newtext)
argv=['git','-C',str(S),'-c','user.name=Hao Lin','-c','user.email=hao.lin@samsung.com','commit','--amend','--cleanup=verbatim','-F',str(E/'new-message.txt')]
r=subprocess.run(argv,capture_output=True,text=True);(E/'amend.stdout').write_text(r.stdout);(E/'amend.stderr').write_text(r.stderr);assert r.returncode==0,r.stderr
new=git('rev-parse','HEAD').decode().strip();newraw=git('cat-file','commit',new);actual=newraw.split(b'\n\n',1)[1];assert actual==newtext.encode();(E/'new.commit').write_bytes(newraw)
tree=git('rev-parse',new+'^{tree}').decode().strip();assert tree==git('rev-parse',old+'^{tree}').decode().strip()
parent=git('rev-parse',new+'^').decode().strip();assert parent=='67619ec8bbbac7238a6cfc33a481ccfbcd12206f'
assert not git('diff',old,new) and not git('status','--porcelain')
identity=git('show','-s','--format=%an <%ae>%n%cn <%ce>',new).decode().splitlines();assert identity==['Hao Lin <hao.lin@samsung.com>']*2
(E/'message.diff').write_text(''.join(difflib.unified_diff(oldtext.splitlines(True),newtext.splitlines(True),fromfile='af82efed-message',tofile='new-message')))
result={'status':'PASS','old':old,'new':new,'tree':tree,'tree_equal':True,'source_diff_empty':True,'body_whitespace_normalized_equal':True,'body_normalized_sha256':hashlib.sha256(' '.join(newtext.split('\n',1)[1].split()).encode()).hexdigest(),'subject_characters':len(newlines[0]),'max_line_characters':max(map(len,newlines)),'path_lines_preserved':True,'parent':parent,'identity':identity,'amend_argv':argv}
(E/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));print('--- git cat-file commit: complete new message ---');print(actual.decode(),end='')
