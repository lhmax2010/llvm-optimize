from pathlib import Path
import subprocess,json,hashlib,difflib,shlex
E=Path(__file__).resolve().parent;W=E.parents[1];S=W/'temp/bolt-v4-20261013/v41/llvm-source';old='506dc25c86e4e2154150796d10b77b71d71ad6bb'
def git(*a):return subprocess.check_output(['git','-C',str(S),*a])
assert git('rev-parse','HEAD').decode().strip()==old
assert not git('status','--porcelain')
p=S/'packaging/llvm.spec';before=p.read_bytes()
block=b'%ifarch x86_64\n%if %{with clang_bolt}\nSource1200: clang-bolt-v2.fdata.xz\nSource1201: clang-bolt-helper.py\n%endif\n%endif\n'
assert before.count(block)==1
new=before.replace(block,b'',1).replace(b'Source1005: llvm-static-archives-native.py\n',b'Source1005: llvm-static-archives-native.py\nSource1200: clang-bolt-v2.fdata.xz\nSource1201: clang-bolt-helper.py\n',1)
p.write_bytes(new)
message=git('show','-s','--format=%B',old)
needle=b'Source1200/1201 and\nBOLT-specific BuildRequires are guarded by that same x86_64 BOLT condition.'
replacement=(b'Source1200/1201 are declared\nunconditionally because gbs inserts generated Patch declarations after the\nlast Source line, and conditional Sources would hide those declarations on\nother architectures and when BOLT is disabled. BOLT-specific BuildRequires\nremain guarded by the same x86_64 BOLT condition, leaving binary packages on\nother architectures unchanged while adding these two files to the source\npackage.')
assert message.count(needle)==1
updated=message.replace(needle,replacement)
(E/'commit-message-before.txt').write_bytes(message);(E/'commit-message-after.txt').write_bytes(updated)
(E/'commit-message.diff').write_text(''.join(difflib.unified_diff(message.decode().splitlines(True),updated.decode().splitlines(True),fromfile='506dc25-message',tofile='new-message')))
subprocess.run(['git','-C',str(S),'add','--','packaging/llvm.spec'],check=True)
subprocess.run(['git','-C',str(S),'-c','user.name=Hao Lin','-c','user.email=hao.lin@samsung.com','commit','--amend','--reset-author','--cleanup=verbatim','-F',str(E/'commit-message-after.txt')],check=True)
sha=git('rev-parse','HEAD').decode().strip();parent=git('rev-parse','HEAD^').decode().strip()
assert parent=='67619ec8bbbac7238a6cfc33a481ccfbcd12206f'
assert git('diff','--name-only',old,sha).decode().splitlines()==['packaging/llvm.spec']
assert git('show','-s','--format=%B',sha).rstrip(b'\n')==updated.rstrip(b'\n')
assert 'Change-Id: Ic98eab90cc017f127a66e1729b44fab8b8e8fb41' in updated.decode()
files=[]
for f in ['packaging/llvm.spec','packaging/clang-bolt-helper.py','packaging/clang-bolt-v2.fdata.xz','packaging/llvm-static-archives-native.py']:
 data=git('show',sha+':'+f);old_data=git('show',old+':'+f)
 if f!='packaging/llvm.spec':assert data==old_data
 files.append({'path':f,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'unchanged':data==old_data})
(E/'source.diff').write_bytes(git('diff','--no-ext-diff',old,sha,'--','packaging/llvm.spec'))
(E/'source-result.json').write_text(json.dumps({'old':old,'new':sha,'parent':parent,'tree':git('rev-parse','HEAD^{tree}').decode().strip(),'identity':git('show','-s','--format=%an <%ae>%n%cn <%ce>').decode().strip(),'files':files,'status':'PASS'},indent=2)+'\n')
argv=json.loads((E/'export-before-argv.json').read_text());argv[argv.index(old)]=sha;argv[argv.index(str(E/'export-before'))]=str(E/'export-after')
(E/'export-after-argv.json').write_text(json.dumps(argv,indent=2)+'\n');(E/'export-after.sh').write_text('#!/bin/sh\nset -eu\nexec '+shlex.join(argv)+'\n')
print(sha)
