"""Read-only phase/du/RPM size comparison; missing samples are not imputed."""
import datetime,hashlib,json,re
from pathlib import Path
W=Path('/home/linhao/Toolchain/development/llvm-optimize');D=Path(__file__).resolve().parent;E=W/'docs/53_hybrid_local_validation_evidence';B=W/'temp/bolt-v4-20261022-cache-release'
log=(E/'rpm-build.log').read_text(errors='replace').splitlines();origin=None;anchors=[];last_exit=None
for i,line in enumerate(log,1):
 if 'started "build llvm.spec" at ' in line:
  stamp=line.split(' at ',1)[1].rstrip('.');origin=datetime.datetime.strptime(stamp,'%a %b %d %H:%M:%S UTC %Y').replace(tzinfo=datetime.timezone.utc).timestamp()
 m=re.match(r'\[\s*(\d+)s\]\s?(.*)',line)
 if not m:continue
 sec=int(m[1]);text=m[2];kind=None
 if text.strip()=='+ exit 0':last_exit={'kind':'build-end','line':i,'elapsed_seconds':sec,'time_ns':int((origin+sec)*1e9) if origin else None,'raw':line}
 if 'Executing(%install)' in text and last_exit:anchors.append(last_exit)
 if 'Executing(%prep)' in text:kind='prep'
 elif 'Executing(%build)' in text:kind='build'
 elif 'Executing(%install)' in text:kind='install'
 elif text.startswith('NATIVE_ARCHIVES_BEGIN '):kind='native-start'
 elif text.startswith('NATIVE_ARCHIVES_END '):kind='native-end'
 elif text.startswith('+ /usr/lib/rpm/find-debuginfo.sh'):kind='find-debuginfo'
 elif text.startswith('Processing files:'):kind='packaging'
 elif ' finished "build llvm.spec"' in text:kind='finished'
 if kind:anchors.append({'kind':kind,'line':i,'elapsed_seconds':sec,'time_ns':int((origin+sec)*1e9) if origin else None,'raw':line})
assert origin is not None
if not any(a['kind']=='finished' for a in anchors):
 end=json.loads((E/'build-result.json').read_text())['end_ns']
 anchors.append({'kind':'finished','line':None,'elapsed_seconds':(end/1e9-origin),'time_ns':end,'raw':'build-result.json end_ns; GBS exit 0 (no finished timestamp in RPM log)'})
(E/'timeline.tsv').write_text('kind\tline\telapsed_seconds\tUTC\traw\n'+''.join(f"{a['kind']}\t{a['line']}\t{a['elapsed_seconds']}\t{datetime.datetime.fromtimestamp(a['time_ns']/1e9,datetime.timezone.utc).isoformat()}\t{a['raw']}\n" for a in anchors))
rows=[json.loads(l) for l in (E/'du-root-complete.jsonl').read_text().splitlines()];valid=[{'time_ns':r['time_ns'],'end_ns':r['time_ns']+int(r['seconds']*1e9),'bytes':int(r['stdout'].split()[0]),'scan_seconds':r['seconds']} for r in rows if r.get('rc')==0 and r.get('stdout','').strip()]
if (E/'final-size-root.json').exists():
 r=json.loads((E/'final-size-root.json').read_text())
 if r['rc']==0:valid.append({'time_ns':r['start_ns'],'end_ns':r['end_ns'],'bytes':int(r['stdout'].split()[0]),'scan_seconds':(r['end_ns']-r['start_ns'])/1e9,'source':'immediate post-build, before validation installation'})
starts={}
for a in anchors:starts.setdefault(a['kind'],a['time_ns'])
phases={}
for name,begin,end in [('ordinary-build','build','install'),('ordinary-install','install','native-start'),('static-conversion','native-start','native-end'),('static-conversion-install','native-start','find-debuginfo'),('platform-post','find-debuginfo','packaging'),('packaging','packaging','finished')]:
 if begin in starts and end in starts:
  samples=[r for r in valid if starts[begin]<=r['time_ns'] and r['end_ns']<=starts[end]];phases[name]={'start_ns':starts[begin],'end_ns':starts[end],'seconds':(starts[end]-starts[begin])/1e9,'samples':len(samples),'peak':max(samples,key=lambda r:r['bytes']) if samples else None}
base=json.loads((B/'measurement-comparison.json').read_text())
result={'log_origin_utc':datetime.datetime.fromtimestamp(origin,datetime.timezone.utc).isoformat(),'anchors':anchors,'complete_samples':len(valid),'missing_samples':sum(r.get('rc')!=0 for r in rows),'peak':max(valid,key=lambda r:r['bytes']) if valid else None,'phases':phases,'baseline':base['baseline'],'baseline_peak_bytes':base['baseline']['peak']['bytes'],'baseline_bolt_fixed_report_peak_bytes':max(r['used_bytes'] for r in base['baseline']['reports'].values()),'baseline_only_interrupted_linker_residue_bytes':base['baseline_only_linker_residue_allocated_bytes'],'limitations':['Observed discrete du peaks, not continuous maxima','GBS fresh downloads and baseline resumed build timing differ','Baseline includes BOLT; 4.3 GiB owned report includes ThinLTO cache positive increment, do not double subtract it','No baseline cache/root mutation performed']}
if result['peak']:result['root_peak_reduction_bytes']=result['baseline_peak_bytes']-result['peak']['bytes']
(E/'disk-comparison.json').write_text(json.dumps(result,indent=2)+'\n')
if (E/'rpm-identities.json').exists():
 old={r['rpm']:r for r in json.loads((B/'rpm-validation/baseline-rpm-headers.json').read_text())};new=json.loads((E/'rpm-identities.json').read_text());out=[]
 for r in new:
  o=old[r['name']];out.append({'rpm':r['name'],'baseline_bytes':o['bytes'],'hybrid_bytes':r['bytes'],'delta_bytes':r['bytes']-o['bytes'],'delta_percent':100*(r['bytes']/o['bytes']-1),'baseline_sha256':o['sha256'],'hybrid_sha256':r['sha256']})
 (E/'rpm-size-comparison.json').write_text(json.dumps(out,indent=2)+'\n')
print('summarized',len(valid),'complete samples',flush=True)
