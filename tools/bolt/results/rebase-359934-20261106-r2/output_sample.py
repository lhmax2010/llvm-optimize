from pathlib import Path
import importlib.util,json,subprocess,sys
from unittest.mock import patch
W=Path('/home/linhao/Toolchain/development/llvm-optimize');B=Path(str(W)+'-bolt');E=Path(__file__).resolve().parent
X=W/'temp/rebase-359934-20261106-r2';C=X/'c2/real-release-c2'
spec=importlib.util.spec_from_file_location('oldconverter',E/'before-llvm-static-archives-native.py');a=importlib.util.module_from_spec(spec);sys.modules[spec.name]=a;spec.loader.exec_module(a)
O=X/'output-equality';O.mkdir();root=O/'root';root.mkdir();build=O/'build';build.mkdir();(build/'CMakeCache.txt').write_text('# offline fixture\n')
subprocess.run(['/usr/bin/ar','qcDS',str(root/'fixture.a'),str(C/'real-release.bc')],check=True)
def retain(p,*args,**kwargs):assert Path(p).resolve().is_relative_to(O)
with patch.object(Path,'unlink',retain):
 ans=a.convert(root,build/'evidence',str(C/'tools/clang-22'),str(C/'tools/llvm-dis'),str(C/'tools/llvm-nm'),build,jobs=1,debug_info='no')
old=build/'evidence/archives/fixture.a';new=C/'positive-build/evidence/archives/fixture.a'
oi=a.inspect(old);ni=a.inspect(new)
rows=[{'old':x['sha256'],'new':y['sha256'],'name_old':x['name'],'name_new':y['name'],'same':x['sha256']==y['sha256']} for x,y in zip(oi['members'],ni['members'])]
assert len(oi['members'])==len(ni['members'])==1 and all(x['same'] for x in rows)
result={'PASS':True,'scope':'one real release bitcode member; not all 7706 outputs','old_archive':str(old),'new_archive':str(new),'members':rows}
(E/'output-sample-result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
