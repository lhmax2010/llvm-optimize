from pathlib import Path
import json,hashlib,subprocess,importlib.util,shutil,os
E=Path(__file__).resolve().parent;BASE=E.parent;W=Path('/home/linhao/Toolchain/development/llvm-optimize');D=W/'temp/runpath-fix-20261026';R=D/'gbs-root/local/BUILD-ROOTS/scratch.x86_64.0';BUILD=R/'home/abuild/rpmbuild/BUILD/llvm-22.1.8/build';WORK=BUILD/'clang-bolt';P=D/'products';OLD=W/'temp/bolt-on-hybrid-20261024/products';X=D/'continue-work'
s=importlib.util.spec_from_file_location('helper',D/'source/packaging/clang-bolt-helper.py');h=importlib.util.module_from_spec(s);s.loader.exec_module(h)
def sha(p):
 with Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def save(p,o):
 p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(o,indent=2)+'\n')
def loader(binary):return [str(R/'lib64/ld-linux-x86-64.so.2'),'--library-path',str(R/'lib64')+':'+str(R/'usr/lib64'),str(binary)]
def free():
 assert shutil.disk_usage('/home').free>=20*1024**3,'home free below 20 GiB'
