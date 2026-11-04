"""Finished-run facts only; missing stages remain NOT RUN/UNKNOWN."""
from pathlib import Path
import json,datetime
E=Path(__file__).parent;D=Path('/home/linhao/Toolchain/development/llvm-optimize/temp/pgo-resource-20261102/full')
summary=json.loads((D/'resources-summary.json').read_text());result=json.loads((D/'result.json').read_text());rows=summary['stages'];facts={'result':result,'stages':{},'prepare':[]}
for r in rows:
 if r['stage'].endswith('/prepare'):facts['prepare'].append(r)
for name in 'ABCD':
 matches=[r for r in rows if r['stage'].endswith('/'+name)]
 facts['stages'][name]=matches[0] if matches else {'status':'NOT RUN'}
fs=[]
for p in D.glob('stage-*/evidence/*/filesystem.jsonl'):
 with p.open() as f:
  for line in f:
   r=json.loads(line);r['source']=str(p);fs.append(r)
facts['home_min']=min(fs,key=lambda r:r['available_bytes']) if fs else 'UNKNOWN'
for label,rel in [('profraw','stage-A/evidence/profraw.json'),('profdata','stage-A/evidence/profdata.json')]:
 p=D/rel;facts[label]=json.loads(p.read_text()) if p.exists() else {'status':'NOT RUN / no completed stage manifest'}
work=D/'stage-D/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/clang-bolt'
facts['BOLT_pipeline']=json.loads((work/'pipeline-result.json').read_text()) if (work/'pipeline-result.json').exists() else {'status':'no pipeline-result.json'}
# Select actual profile/gate evidence with original line numbers, without invoking tools.
excerpts=[]
for p in [D/'stage-D/evidence/D/stdout',D/'stage-D/evidence/D/stderr',D/'stage-D/evidence/rpm-build.log',work/'rewrite/bolt.log']:
 if p.exists():
  with p.open(errors='replace') as f:
   for i,line in enumerate(f,1):
    if any(s in line for s in ('BOLT_GATE_FAILED','BOLT_PIPELINE_PASS','BOLT-WARNING','mismatch','profile data','profile for','BOLT-INFO:','Traceback','No space left','oom-kill')):excerpts.append(dict(source=str(p),line=i,text=line.rstrip('\n')))
facts['profile_excerpts']=excerpts
facts['two_roots_coexist']=(D/'stage-A/gbs-root').exists() and (D/'stage-D/gbs-root').exists()
facts['continuous_combined_root_peak']='UNKNOWN: experiment du is boundary-only; do not sum independent historical peaks'
(E/'finished-facts.json').write_text(json.dumps(facts,indent=2)+'\n')
print(json.dumps({k:v for k,v in facts.items() if k not in ('profile_excerpts','stages','prepare')},indent=2))
for k,r in facts['stages'].items():print(k,r.get('seconds'),r.get('cgroup_peak_bytes'),r.get('process_VmHWM_max'),r.get('root_boundary_disk_max'))
