from pathlib import Path
import os,tempfile,shutil,runpy,json
E=Path(__file__).parent
scratch=Path('/home/linhao/Toolchain/development/llvm-optimize/temp/rebase-359934-20261106/tests');scratch.mkdir(exist_ok=False)
keep=scratch/'retained-cleanup';keep.mkdir()
tempfile.tempdir=str(scratch)
original=tempfile.TemporaryDirectory
class Preserved:
 def __init__(self,*args,**kw):self.name=tempfile.mkdtemp(*args,**kw)
 def __enter__(self):return self.name
 def __exit__(self,*args):pass
 def cleanup(self):pass
tempfile.TemporaryDirectory=Preserved
moves=[]
def preserve(p,*args,**kw):
 p=Path(p)
 if not p.exists() and not p.is_symlink():return
 assert p.resolve().is_relative_to(scratch),str(p)
 target=keep/(str(len(moves))+'-'+p.name);p.rename(target);moves.append({'from':str(p),'to':str(target)})
Path.unlink=preserve;shutil.rmtree=preserve
try:runpy.run_path(str(E/'test_regressions.py'),run_name='__main__')
finally:(E/'retained-test-files.json').write_text(json.dumps(moves,indent=2)+'\n')
