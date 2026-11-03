# Read-only source inputs. Reproduce resource_report.py's aggregation into new evidence only.
from pathlib import Path
import json
E=Path(__file__).parent;N=Path('/home/linhao/Toolchain/development/llvm-optimize/temp/night-20261103')
def rows(p):
 if not p.exists():return []
 return [json.loads(l) for l in p.open() if l.strip()]
summary={}
for name in ('toolchain','basedev'):
 src=N/name/'evidence';rs=rows(src/'resources.jsonl');du=rows(src/'du-root.jsonl');bp=rows(src/'bolt-process.jsonl');events=rows(src/'phase-events.jsonl');starts={};ends={}
 for r in events:
  if r.get('kind')=='end':ends.setdefault(r['phase'],r['time_ns'])
  else:starts.setdefault(r['phase'],r)
 ordered=sorted(starts.values(),key=lambda r:r['time_ns']);last=json.loads((src/'controller-result.json').read_text())['end_ns'];out=[]
 for i,e in enumerate(ordered):
  end=ends.get(e['phase'],ordered[i+1]['time_ns'] if i+1<len(ordered) else last)
  within=lambda r:e['time_ns']<=r['time_ns']<=end
  mem=[int(r['memory.current']) for r in rs if within(r) and r.get('memory.current','').strip().isdigit()];space=[r['home_available_bytes'] for r in rs if within(r)];disk=[int(r['stdout'].split()[0]) for r in du if within(r) and r.get('rc')==0 and r.get('stdout','').split() and r['stdout'].split()[0].isdigit()];bolt=[int(r['VmHWM'].split()[0])*1024 for r in bp if within(r) and 'VmHWM' in r]
  out.append(dict(phase=e['phase'],start_ns=e['time_ns'],end_ns=end,seconds=(end-e['time_ns'])/1e9,cgroup_sampled=max(mem,default=None),bolt_hwm=max(bolt,default=None),root_sampled=max(disk,default=None),filesystem_min=min(space,default=None)))
 lines=['|Phase|Seconds|Cgroup sampled bytes (includes cache)|llvm-bolt VmHWM bytes|Root du sampled bytes|Filesystem min available bytes|','|---|---|---|---|---|---|']
 for r in out:lines.append('|'+ '|'.join(str(r[k]) if r[k] is not None else 'UNKNOWN' for k in ('phase','seconds','cgroup_sampled','bolt_hwm','root_sampled','filesystem_min'))+'|')
 (E/name/'resource-table-postmortem.md').write_text('\n'.join(lines)+'\n');(E/name/'resource-table-postmortem.json').write_text(json.dumps(out,indent=2)+'\n')
 disk=[dict(r,bytes=int(r['stdout'].split()[0])) for r in du if r.get('rc')==0 and r.get('stdout','').split() and r['stdout'].split()[0].isdigit()]
 summary[name]=dict(root_peak_sample=max(disk,key=lambda r:r['bytes']) if disk else None,filesystem_min_sample={k:v for k,v in min(rs,key=lambda r:r['home_available_bytes']).items() if k in ('time_ns','home_available_bytes')},du_timeouts=sum(r.get('rc')!=0 for r in du),samples=len(rs),du_samples=len(du))
 if name=='toolchain':assert (src/'resource-table.md').read_text()=='\n'.join(lines)+'\n'
(E/'resource-postmortem-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
