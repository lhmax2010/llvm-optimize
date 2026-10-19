from pathlib import Path
import subprocess,json,hashlib,time,difflib
E=Path(__file__).resolve().parent;W=E.parents[1];S=W/'temp/bolt-v4-20261013/v41/llvm-source';base='e2463165829cc91b0a1d60a3e0f915a587865f70'
def git(*a):return subprocess.check_output(['git',*a],cwd=S)
msg=(W/'temp/bolt-v4-20261019-disk-diagnostics/new-message.txt').read_text();needle='and shortfall from actual file sizes measured in this build.\n';assert needle in msg
msg=msg.replace(needle,needle+"If a failed step's log is unavailable, report unknown rather than\nguessing its cause.\n",1);assert max(map(len,msg.splitlines()))<=72
(E/'new-message.txt').write_text(msg);old=(W/'temp/bolt-v4-20261019-disk-diagnostics/base-message.txt').read_text();(E/'message.diff').write_text(''.join(difflib.unified_diff(old.splitlines(True),msg.splitlines(True),fromfile='e2463165 message',tofile='new message')))
assert git('rev-parse','HEAD').decode().strip()==base
subprocess.run(['git','add','--','packaging/llvm.spec','packaging/clang-bolt-helper.py'],cwd=S,check=True)
with (E/'amend.stdout').open('wb') as out,(E/'amend.stderr').open('wb') as err:r=subprocess.run(['git','-c','user.name=Hao Lin','-c','user.email=hao.lin@samsung.com','commit','--amend','--reset-author','-F',str(E/'new-message.txt')],cwd=S,stdout=out,stderr=err)
assert r.returncode==0
sha=git('rev-parse','HEAD').decode().strip();parent=git('rev-parse','HEAD^').decode().strip();assert parent=='67619ec8bbbac7238a6cfc33a481ccfbcd12206f'
(E/'source.diff').write_bytes(git('diff',base,sha));(E/'spec.diff').write_bytes(git('diff',base,sha,'--','packaging/llvm.spec'));(E/'helper.diff').write_bytes(git('diff',base,sha,'--','packaging/clang-bolt-helper.py'));(E/'new-commit.txt').write_bytes(git('cat-file','commit',sha))
files=[]
for name in ['llvm.spec','clang-bolt-helper.py','clang-bolt-v2.fdata.xz']:
 p=S/'packaging'/name;files.append({'path':'packaging/'+name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
(E/'release.json').write_text(json.dumps({'commit':sha,'base':base,'parent':parent,'tree':git('rev-parse','HEAD^{tree}').decode().strip(),'files':files,'author_committer':git('show','-s','--format=%an <%ae> / %cn <%ce>').decode().strip(),'max_message_line':max(map(len,msg.splitlines()))},indent=2)+'\n')
argv=['gbs','export','--spec','llvm.spec','--commit',sha,'--upstream-branch','sandbox/fangyu.he/llvm_optmize','--upstream-tag','upstream/22.1.8','--outdir-directly','-o',str(E/'export'),str(S)]
ver=subprocess.run(['gbs','--version'],capture_output=True,text=True);(E/'gbs-version.txt').write_text(ver.stdout+ver.stderr);start=time.monotonic()
with (E/'gbs-export.stdout').open('wb') as out,(E/'gbs-export.stderr').open('wb') as err:r=subprocess.run(argv,stdout=out,stderr=err)
(E/'gbs-export.json').write_text(json.dumps({'argv':argv,'rc':r.returncode,'seconds':time.monotonic()-start},indent=2)+'\n');assert r.returncode==0;print('new source',sha,'gbs export PASS')
