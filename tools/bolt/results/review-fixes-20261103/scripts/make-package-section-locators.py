from pathlib import Path
import subprocess,json,hashlib,lzma,os,shutil
W=Path('/home/linhao/Toolchain/development/llvm-optimize');B=W.parent/'llvm-optimize-bolt';S=W/'temp/review-20261102/source';D=W/'temp/review-20261103';E=D/'evidence';P=B/'patches/review-20261103';P.mkdir(exist_ok=True)
def git(*a):return subprocess.check_output(['git',*a],cwd=S)
bolt=git('rev-parse','HEAD').decode().strip();hybrid=git('rev-parse','HEAD^').decode().strip();base='67619ec8bbbac7238a6cfc33a481ccfbcd12206f';tree=git('rev-parse','HEAD^{tree}').decode().strip()
for commit,name in [(hybrid,'0001-cmake-use-hybrid-LLVM-linkage-on-x86_64.patch'),(bolt,'0002-packaging-optimize-x86_64-clang-with-BOLT.patch')]:
 (P/name).write_bytes(git('format-patch','-1',commit,'--stdout','--full-index','--binary'))
 (P/(name[:4]+'-commit-message.txt')).write_bytes(git('show','-s','--format=%B',commit))
(P/'0002-text-only.diff').write_bytes(git('diff','--full-index',hybrid,bolt,'--','.',':(exclude)packaging/clang-bolt-v2.fdata.xz'))
files=[f for f in git('diff','--name-only',base,bolt).decode().splitlines() if not f.endswith('.xz')];assert len(files)==8
blobs=[]
for f in files:
 p=P/'files'/f;p.parent.mkdir(parents=True,exist_ok=True);data=git('show',bolt+':'+f);p.write_bytes(data);blobs.append({'path':f,'blob':git('rev-parse',bolt+':'+f).decode().strip(),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
(P/'text-file-blobs.json').write_text(json.dumps(blobs,indent=2)+'\n');(P/'text-files-ls-tree.txt').write_bytes(git('ls-tree','-r',bolt,'--',*files));(P/'final-tree-top-level.txt').write_bytes(git('ls-tree',bolt));(P/'final-tree-ls-tree.txt.xz').write_bytes(lzma.compress(git('ls-tree','-r',bolt)))
(P/'source-identities.json').write_text(json.dumps({'base':base,'hybrid':hybrid,'bolt':bolt,'tree':tree,'status':'Section-table locator exception approved; lightweight checks pass; full build and release qualification pending','gerrit_pushed':False},indent=2)+'\n')
idx=D/'patch-apply-section-locators.index';assert not idx.exists();env=dict(os.environ,GIT_INDEX_FILE=str(idx));subprocess.run(['git','read-tree',base],cwd=S,env=env,check=True)
for p in sorted(P.glob('000[12]-*.patch')):subprocess.run(['git','apply','--cached',str(p)],cwd=S,env=env,check=True)
actual=subprocess.check_output(['git','write-tree'],cwd=S,env=env,text=True).strip();assert actual==tree;(E/'section-locators-patch-apply.json').write_text(json.dumps({'base':base,'expected_tree':tree,'actual_tree':actual,'PASS':True})+'\n')
print(hybrid,bolt,tree)
