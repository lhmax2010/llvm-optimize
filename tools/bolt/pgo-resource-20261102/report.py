"""Summarize measured data only. Missing/short-lived processes remain UNKNOWN."""
from common import *
import sys

def readjson(p,default=None):return json.loads(p.read_text()) if p.exists() else default
def jsonlines(p):
 if p.exists():
  for l in p.read_text().splitlines():yield json.loads(l)
def maximum(rows,key):
 valid=[r for r in rows if isinstance(r.get(key),(int,float))]
 return max(valid,key=lambda r:r[key]) if valid else 'UNKNOWN'
def summarize(d):
 report={'scope':str(d),'limitations':['cgroup includes file cache','VmHWM is lifetime high-water mark of observed processes; <2s processes may be missed','du only at stage/log boundaries; disk maximum is boundary-observed, not true instantaneous peak','D substage peaks use one open memory.peak FD reset at observed anchors; boundary lag recorded by timestamps'] ,'stages':[]}
 for sub in sorted(d.glob('stage-*/evidence/*')):
  if not sub.is_dir() or not (sub/'controller.json').exists():continue
  result=readjson(sub/'service-result.json',{});proc=list(jsonlines(sub/'processes.jsonl'));disk=list(jsonlines(sub/'du-boundaries.jsonl'));fs=list(jsonlines(sub/'filesystem.jsonl'))
  row={'stage':sub.parent.parent.name+'/'+sub.name,'result':result,'cgroup_peak_bytes':int(result['stats']['memory.peak']) if result.get('stats',{}).get('memory.peak','').strip().isdigit() else 'UNKNOWN','seconds':(result['end_ns']-result['start_ns'])/1e9 if 'end_ns' in result else 'UNKNOWN','process_VmHWM_max':maximum(proc,'VmHWM_bytes'),'root_boundary_disk_max':maximum(disk,'bytes'),'filesystem_available_min':min(fs,key=lambda r:r['available_bytes']) if fs else 'UNKNOWN','subphases':[]}
  boundaries=list(jsonlines(sub/'boundaries.jsonl'));last_end=result.get('start_ns')
  for peak in jsonlines(sub/'phase-peaks.jsonl'):
   phase=peak.get('phase');end=peak.get('time_ns');seconds=(end-last_end)/1e9 if end and last_end else 'UNKNOWN';last_end=end or last_end
   # Include entry and exit boundary scans; do not claim an instantaneous peak.
   relevant={b['time_ns'] for b in boundaries if b.get('from')==phase or b.get('to')==phase}
   row['subphases'].append({'phase':phase,'observed_seconds':seconds,'cgroup_peak':peak,'process_VmHWM_max':maximum([r for r in proc if r['phase']==phase],'VmHWM_bytes'),'root_boundary_disk_max':maximum([r for r in disk if r.get('boundary_ns') in relevant],'bytes'),'filesystem_available_min':min([r for r in fs if r['phase']==phase],key=lambda r:r['available_bytes'],default='UNKNOWN')})
  report['stages'].append(row)
 save(d/'resources-summary.json',report);return report
if __name__=='__main__':print(json.dumps(summarize(Path(sys.argv[1])),indent=2))
