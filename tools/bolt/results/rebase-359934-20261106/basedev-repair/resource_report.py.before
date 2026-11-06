"""Sampled resource tables, never infer an unobserved phase peak."""
from pathlib import Path
import json,re,datetime

def read(p,default=None):
 try:return json.loads(p.read_text())
 except (OSError,ValueError):return default

def rows(p):
 if not p.exists():return []
 out=[]
 for line in p.open():
  try:out.append(json.loads(line))
  except ValueError:pass
 return out

def number(s):
 try:return int(s)
 except (ValueError,TypeError):return None

def critical_stop(D,audit=None):
 E=D/'evidence'
 if audit and (audit['mounts']['stdout'] or audit['remaining_build_processes']):return 'residual-process-or-mount'
 if (E/'cleanup-failure.txt').exists():return 'cleanup-failed'
 if (E/'disk-stop.json').exists():return 'disk-stop'
 for directory in ('validation','validation-02'):
  failure=D/directory/'failure.txt';result=read(D/directory/'result.json',{})
  text=failure.read_text() if failure.exists() else ''
  if 'disk-stop:' in text:return 'disk-stop'
  if 'MemoryError' in text or result.get('reason') in ('memory-stop','memory-oom-stop'):return 'memory-oom-stop'
  service=read(D/directory/'service-result.json',{})
  if service.get('Result')=='oom-kill' or int(service.get('OOMKilled',0) or 0):return 'memory-oom-stop'
 for r in rows(E/'resources.jsonl')+[read(E/'build-result.json',{}).get('stats',{})]:
  for line in str(r.get('memory.events','')).splitlines():
   x=line.split()
   if len(x)==2 and x[0] in ('oom','oom_kill') and x[1].isdigit() and int(x[1]):return 'memory-oom-stop'
 if audit and re.search(r'Result=oom-kill',audit.get('services',{}).get('stdout','')):return 'memory-oom-stop'
 return None

def report(D,output=None):
 from log_support import canonical_log,log_summary
 E=D/'evidence';O=output or E;rs=rows(E/'resources.jsonl');du=rows(E/'du-root.jsonl');bolt=rows(E/'bolt-process.jsonl')
 source=log_summary(canonical_log(D));assert source['epoch_zero'] is not None,'GBS wall-clock origin missing'
 epoch=source['epoch_zero'];last=int((epoch+source['last_seconds'])*1e9)
 peak=number(read(E/'build-result.json',{}).get('stats',{}).get('memory.peak'))
 starts={};ends={}
 for phase,e in source['phases'].items():
  ns=int((epoch+e['seconds'])*1e9)
  if phase.endswith('-end'):ends[phase[:-4]]=ns
  else:starts[phase]=dict(phase=phase,time_ns=ns,text=e['text'],line=e['line'])
 ordered=sorted(starts.values(),key=lambda r:r['time_ns']);table=[]
 for i,e in enumerate(ordered):
  end=ordered[i+1]['time_ns'] if i+1<len(ordered) else last
  end=ends.get(e['phase'],end)
  def within(r):return e['time_ns']<=r['time_ns']<=end
  samples=[r for r in rs if within(r)];disks=[int(r['stdout'].split()[0]) for r in du if within(r) and r.get('rc')==0 and r.get('stdout','').split() and r['stdout'].split()[0].isdigit()]
  mem=[number(r.get('memory.current')) for r in samples];mem=[x for x in mem if x is not None]
  bp=[int(r['VmHWM'].split()[0])*1024 for r in bolt if within(r) and 'VmHWM' in r]
  free=[r['home_available_bytes'] for r in samples if 'home_available_bytes' in r]
  table.append(dict(phase=e['phase'],start_ns=e['time_ns'],end_ns=end,seconds=(end-e['time_ns'])/1e9 if end else None,anchor=e['text'],cgroup_sampled_max_bytes=max(mem,default=None),bolt_VmHWM_bytes=max(bp,default=None),root_du_sampled_max_bytes=max(disks,default=None),filesystem_min_available_bytes=min(free,default=None)))
 for name in ['ordinary-build','ordinary-install','BOLT','cache-release','archive-conversion','platform-post','packaging']:
  if name not in starts:table.append({'phase':name,'status':'UNKNOWN: no samples/anchor'})
 result=dict(log_source={k:v for k,v in source.items() if k!='selected'},time_basis='GBS [NNNs], wall clock from started build line; one-second granularity',all_process_VmHWM='UNKNOWN: original sampler only watched llvm-bolt',cgroup_lifetime_peak_includes_file_cache=peak,phases=table,missing_means='UNKNOWN; no extrapolation',cgroup_phase_metric='sampled memory.current maximum, not independent memory.peak',conditions=read(D/'plan.json',{}))
 (O/'resource-table.json').write_text(json.dumps(result,indent=2)+'\n')
 text=['|Phase|Seconds|Cgroup sampled bytes (includes cache)|llvm-bolt VmHWM bytes|Root du sampled bytes|Filesystem min available bytes|','|---|---|---|---|---|---|']
 for r in table:text.append('|'+ '|'.join(str(r.get(k)) if r.get(k) is not None else 'UNKNOWN' for k in ('phase','seconds','cgroup_sampled_max_bytes','bolt_VmHWM_bytes','root_du_sampled_max_bytes','filesystem_min_available_bytes'))+'|')
 (O/'resource-table.md').write_text('\n'.join(text)+'\n')
 return result
