"""Summarize recorded samples only; no traversal of any build tree."""
import json,re,sys
from pathlib import Path
D=Path(__file__).resolve().parent
label=sys.argv[1]; E=D/label
records=[]
for file in ['du-root-complete.jsonl','du.jsonl']:
 p=E/file
 if not p.exists():continue
 for line in p.read_text().splitlines():
  try:r=json.loads(line)
  except ValueError:continue
  words=r.get('stdout','').split()
  if words and words[0].isdigit():
   records.append(dict(source=file,path=r.get('path','complete-chroot'),bytes=int(words[0]),time_ns=r['time_ns'],seconds=r.get('seconds'),rc=r.get('rc'),stderr=r.get('stderr','')))
peaks={}
for r in records:
 key=r['path']
 if key not in peaks or r['bytes']>peaks[key]['bytes']:peaks[key]=r
valid_peaks={}
for r in records:
 if r['rc']!=0:continue
 key=r['path']
 if key not in valid_peaks or r['bytes']>valid_peaks[key]['bytes']:valid_peaks[key]=r
resources=[]
p=E/'independent-guard.jsonl'
if p.exists():
 for line in p.read_text().splitlines():
  try:resources.append(json.loads(line))
  except ValueError:pass
markers=['Executing(%prep)','Executing(%build)','Executing(%install)','BOLT_DISK_REPORT','BOLT_PIPELINE_PASS','BOLT_COMPARE_ROOT_PASS','BOLT_CACHE_RELEASE','BOLT_POST_GATE_PASS','BOLT_GATE_FAILED','BOLT_DISK_DIAGNOSIS','find-debuginfo','llvm-static-archives-native.py','Processing files:','Wrote:','Bad exit status']
anchors=[]
p=E/'build.log'
if p.exists():
 for n,line in enumerate(p.read_text(errors='replace').splitlines(),1):
  hits=[x for x in markers if x in line]
  if hits:anchors.append(dict(line=n,markers=hits,text=line))
result={'label':label,'all_sampled_peaks_including_incomplete':peaks,'rc0_sampled_peaks':valid_peaks,'sample_count':len(records),'resource_last':resources[-1] if resources else None,'anchors':anchors}
(E/'recorded-summary.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'label':label,'peaks':{k:v['bytes'] for k,v in peaks.items()},'anchors':len(anchors)},indent=2))
