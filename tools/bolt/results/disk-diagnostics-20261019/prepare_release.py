from pathlib import Path
import subprocess,json,difflib,textwrap,hashlib,os
E=Path(__file__).parent;S=E.parent/'bolt-v4-20261013/v41/llvm-source';B=E.parents[2]/'llvm-optimize-bolt'
def run(a,**kw):return subprocess.run(a,check=True,**kw)
# Re-capture final generated script, never execute install or post.
D=E/'host-capture';r=json.loads((D/'result.json').read_text());env=os.environ.copy();env['BOLT_CAPTURE']=str(D/'install.sh')
p=subprocess.run(r['argv'],capture_output=True,text=True,env=env);(D/'stdout').write_text(p.stdout);(D/'stderr').write_text(p.stderr)
syntax=subprocess.run(['/bin/sh','-n',str(D/'install.sh')],capture_output=True,text=True);(D/'syntax.stderr').write_text(syntax.stderr)
assert syntax.returncode==0 and (D/'install.sh').read_text().count('disk-report ')==4
r.update(rc=p.returncode,syntax_rc=syntax.returncode,copy_only=True,product_script_executed=False);(D/'result.json').write_text(json.dumps(r,indent=2)+'\n')
old=(E/'base-message.txt').read_text();new=old
needle='The binary Source is the existing profile v2'
para=('No disk-space thresholds are imposed; each stage records free space.\n'
'If a step fails because its disk is full, stop before replacing the\n'
'packaged clang and report current free space, estimated requirements\n'
'and shortfall from actual file sizes measured in this build.\n\n')
new=new.replace(needle,para+needle,1)
oldopen='Still open: full release-mode build; accel/worker identity; first real\n%install execution; cleanup cannot be guaranteed without matching /proc;\nperformance outside LLVM workloads.'
newopen=('Quickbuild x86_64 completed %install on this same implementation before\n'
'the Source-order fix. Still open: full release-mode build; accel/worker\n'
'identity; cleanup cannot be guaranteed without matching /proc;\n'
'performance outside LLVM workloads.')
assert oldopen in new;new=new.replace(oldopen,newopen,1)
assert max(map(len,new.splitlines()))<=72 and new.splitlines()[0]==old.splitlines()[0]
(E/'new-message.txt').write_text(new);(E/'message.diff').write_text(''.join(difflib.unified_diff(old.splitlines(True),new.splitlines(True),fromfile='BASE message',tofile='new message')))
changed=subprocess.check_output(['git','diff','--name-only'],cwd=S,text=True).splitlines();assert changed and set(changed)<=set(['packaging/clang-bolt-helper.py','packaging/llvm.spec']),changed
run(['git','add','--']+changed,cwd=S)
run(['git','-c','user.name=Hao Lin','-c','user.email=hao.lin@samsung.com','commit','--amend','--reset-author','-F',str(E/'new-message.txt')],cwd=S)
sha=subprocess.check_output(['git','rev-parse','HEAD'],cwd=S,text=True).strip();parent=subprocess.check_output(['git','rev-parse','HEAD^'],cwd=S,text=True).strip();assert parent=='67619ec8bbbac7238a6cfc33a481ccfbcd12206f'
(E/'source.diff').write_bytes(subprocess.check_output(['git','diff','e2463165829cc91b0a1d60a3e0f915a587865f70',sha],cwd=S))
(E/'new-commit.txt').write_bytes(subprocess.check_output(['git','cat-file','commit',sha],cwd=S))
files=[]
for name in ['llvm.spec','clang-bolt-helper.py','clang-bolt-v2.fdata.xz','llvm-static-archives-native.py']:
 p=S/'packaging'/name;files.append({'path':'packaging/'+name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
value={'commit':sha,'parent':parent,'tree':subprocess.check_output(['git','rev-parse','HEAD^{tree}'],cwd=S,text=True).strip(),'files':files,'title_length':len(new.splitlines()[0]),'max_message_line':max(map(len,new.splitlines())),'author':subprocess.check_output(['git','show','-s','--format=%an <%ae> / %cn <%ce>'],cwd=S,text=True).strip()}
(E/'release.json').write_text(json.dumps(value,indent=2)+'\n');print(json.dumps(value,indent=2))
