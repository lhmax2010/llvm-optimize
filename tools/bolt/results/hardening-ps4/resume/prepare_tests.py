from pathlib import Path
import shutil,difflib,json
E=Path(__file__).resolve().parent;X=Path('/home/linhao/Toolchain/development/llvm-optimize/temp/hardening-ps4-20261114')
old=Path('/home/linhao/Toolchain/development/llvm-optimize/temp/fifth-review-20261111/rerun3/environment');new=X/'environment'
assert not new.exists();shutil.copytree(old,new,symlinks=True)
rows=[]
for p in new.rglob('*.py'):
 s=p.read_text();t=s.replace('temp/rebase-359934-20261106/source','temp/hardening-ps4-20261114/source')
 if s!=t:
  p.write_text(t);rows.append(str(p));(E/(p.name+'.paths.diff')).write_text(''.join(difflib.unified_diff(s.splitlines(True),t.splitlines(True),fromfile=str(old/p.relative_to(new)),tofile=str(p))))
(E/'test-environment.json').write_text(json.dumps(dict(source=str(old),copy=str(new),path_changes=rows,product=str(X/'source'),excluded_tests={'test_r3.R3.test_messages':'Historical three-commit chain requirement does not apply to the explicitly authorized single hardening commit on PS3; not a converter fixture.'}),indent=2)+'\n')
print('prepared',new)
