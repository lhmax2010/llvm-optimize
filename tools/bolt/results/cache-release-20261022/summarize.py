from pathlib import Path
import json,time,gzip,re
D=Path(__file__).resolve().parent
report={'captured_at_ns':time.time_ns(),'status':'INCOMPLETE_MEMORY_ADMISSION_TIMEOUT','full_builds_completed':0,'segments':{}}
anchors=[]
for name in ['baseline-segment1','baseline-segment2','baseline-resume1']:
 e=D/name;r={}
 for field in ['du-root-complete','du','resource','independent-guard']:
  p=e/(field+'.jsonl')
  if not p.exists():continue
  rows=[json.loads(x) for x in p.read_text().splitlines()]
  if field=='du-root-complete':
   valid=[x for x in rows if x['rc']==0 and x['stdout'].split()]
   r['whole_chroot_sample_count']=len(valid)
   r['whole_chroot_peak_sample']=max(valid,key=lambda x:int(x['stdout'].split()[0])) if valid else None
   r['longest_du_seconds']=max((x['seconds'] for x in rows),default=0)
  elif field=='du':
   peaks={}
   for x in rows:
    if not x['stdout'].split():continue
    n=int(x['stdout'].split()[0]);key=x['path']
    if key not in peaks or n>int(peaks[key]['stdout'].split()[0]):peaks[key]=x
   r['directory_peaks']=peaks
  else:
   r[field+'_memory_peak']=max((int(x.get('memory.peak',0)) for x in rows),default=0)
   r[field+'_process_VmHWM_kB']=max((p['VmHWM_kB'] for x in rows for p in x.get('processes',[])),default=0)
   if rows:r[field+'_last']=rows[-1]
 p=e/'leases.jsonl'
 if p.exists():
  leases=[json.loads(x) for x in p.read_text().splitlines()];w=[x for x in leases if x.get('waiting')=='memory']
  r['leases']=leases
  if w:r['memory_admission']={'samples':len(w),'first_time_ns':w[0]['time_ns'],'last_time_ns':w[-1]['time_ns'],'min_available':min(x['available'] for x in w),'max_available':max(x['available'] for x in w),'timeout_seconds':3600}
 p=e/('rpm-build.log.gz' if name=='baseline-segment2' else 'build.log')
 if p.exists():
  lines=(gzip.open(p,'rt',errors='replace').read() if p.suffix=='.gz' else p.read_text(errors='replace')).splitlines()
  r['log']=str(p);r['log_lines']=len(lines);r['last_line']=lines[-1] if lines else ''
  for n,line in enumerate(lines,1):
   if any(k in line for k in ['Executing(%prep)','Executing(%build)','Executing(%install)','BOLT_DISK_REPORT','BOLT_PIPELINE_PASS','BOLT_COMPARE_ROOT_PASS','BOLT_POST_GATE_PASS','BOLT_CACHE_RELEASE','find-debuginfo','Wrote:']):anchors.append([name,str(n),line])
 report['segments'][name]=r
report['unrun']=['baseline %install and BOLT','baseline RPM packaging','revised full build','candidate SHA comparison','RPM payload comparison','full-build peak comparison']
(D/'partial-measurement.json').write_text(json.dumps(report,indent=2)+'\n')
(D/'timeline.tsv').write_text('segment\tline\toriginal\n'+''.join('\t'.join(row)+'\n' for row in anchors))
print(json.dumps({k:{a:v for a,v in r.items() if a in ['whole_chroot_sample_count','whole_chroot_peak_sample','longest_du_seconds','resource_memory_peak','resource_process_VmHWM_kB','memory_admission','log_lines','last_line']} for k,r in report['segments'].items()},indent=2))
