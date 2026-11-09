from pathlib import Path
import tempfile,shutil,runpy,sys,json,os
scratch=Path(os.environ['TEST_SCRATCH']);scratch.mkdir(exist_ok=False)
keep=scratch/'retained-cleanup';keep.mkdir()
tempfile.tempdir=str(scratch)
class Preserved:
 def __init__(self,*a,**kw):self.name=tempfile.mkdtemp(*a,**kw)
 def __enter__(self):return self.name
 def __exit__(self,*a):pass
 def cleanup(self):pass
tempfile.TemporaryDirectory=Preserved
moves=[]
def preserve(p,*a,**kw):
 p=Path(p)
 if not p.exists() and not p.is_symlink():
  if kw.get('missing_ok') or kw.get('ignore_errors'):return
  raise FileNotFoundError(str(p))
 assert p.absolute().is_relative_to(scratch),str(p)
 target=keep/(str(len(moves))+'-'+p.name)
 p.rename(target);moves.append({'from':str(p),'to':str(target)})
Path.unlink=preserve
shutil.rmtree=preserve
script=Path(sys.argv[1]).resolve();sys.argv=sys.argv[1:];sys.path.insert(0,str(script.parent))
try:runpy.run_path(str(script),run_name='__main__')
finally:(scratch/'preserved-files.json').write_text(json.dumps(moves,indent=2)+'\n')
