from pathlib import Path
import importlib.util,json,hashlib,shlex,gzip,time
E=Path(__file__).parent;S=Path('/home/linhao/Toolchain/development/llvm-optimize/temp/rebase-359934-20261106/source')
def load(name,path):
 sp=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
old=load('old',E/'old-converter.py');new=load('new',S/'packaging/llvm-static-archives-native.py')
summary={}
with gzip.open(E/'replay-members.jsonl.gz','wt') as out:
 for tag,mode in [('toolchain','yes'),('basedev','no')]:
  paths=json.loads((E/(tag+'-settings-paths.json')).read_text());assert len(paths)==3853,len(paths)
  result={'members':len(paths),'equal':0,'mismatches':[]}
  for p in paths:
   data=Path(p).read_bytes();r=json.loads(data)
   cmd=shlex.join(r['recorded_command']).replace('\\','\\5C').replace('"','\\22')
   lines=[x+'\n' for x in r['evidence']]+['!llvm.commandline = !{!999999999}\n','!999999999 = !{!"'+cmd+'"}\n']
   a=old.ir_settings(lines,debug_info=mode);b=new.ir_settings(lines,debug_info=mode)
   z={'project':tag,'path':p,'settings_sha256':hashlib.sha256(data).hexdigest(),'original_command':r['recorded_command'],'old':a['flags'],'new':b['flags'],'recorded_flags':r['flags']}
   z['equal']=z['old']==z['new']==z['recorded_flags']
   result['equal']+=z['equal']
   if not z['equal']:result['mismatches'].append(z)
   out.write(json.dumps(z)+'\n')
  summary[tag]=result;print(tag,len(paths),result['equal'],flush=True)
(E/'replay-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
assert all(r['equal']==3853 for r in summary.values())
