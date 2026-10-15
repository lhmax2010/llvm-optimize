import json,re,time,hashlib,os
from pathlib import Path
E=Path(__file__).resolve().parent;G=1024**3
rows=[json.loads(x) for x in (E/'samples.jsonl').read_text().splitlines()] if (E/'samples.jsonl').exists() else []
phases={}
for r in rows:
 d=phases.setdefault(r['phase'],{'start':r['time'],'last':r['time'],'samples':0,'max_sampled_cgroup_current':0,'max_cumulative_kernel_peak':0,'max_observed_process_VmHWM_kB':0})
 d['last']=r['time'];d['samples']+=1;d['max_sampled_cgroup_current']=max(d['max_sampled_cgroup_current'],int(r.get('memory.current',0)));d['max_cumulative_kernel_peak']=max(d['max_cumulative_kernel_peak'],int(r.get('memory.peak',0)));d['max_observed_process_VmHWM_kB']=max([d['max_observed_process_VmHWM_kB']]+[p['VmHWM_kB'] for p in r['processes']])
for v in phases.values():v['observed_span_seconds']=v['last']-v['start']
result={'phases':phases,'measurement_note':'0.5-second requested sampling, actual timestamps retained; phase current maxima are observed, memory.peak is cumulative kernel peak, not reset per phase. VmHWM is maximum among observed processes; short-lived processes may be missed.'}
if rows:result.update(samples=len(rows),minimum_host_available_bytes=min(r['available_bytes'] for r in rows),minimum_disk_free_bytes=min(r['free_bytes'] for r in rows),disk_consumed_highwater_bytes=json.loads((E/'disk-plan.json').read_text())['free_before']-min(r['free_bytes'] for r in rows),max_process_VmHWM_kB=max(p['VmHWM_kB'] for r in rows for p in r['processes']))
if (E/'final-cgroup.json').exists():result['final_cgroup']=json.loads((E/'final-cgroup.json').read_text())
if (E/'rehearsal-result.json').exists():result['rehearsal']=json.loads((E/'rehearsal-result.json').read_text())
(E/'resource-summary.json').write_text(json.dumps(result,indent=2)+'\n')
text=(E/'rpmbuild.log').read_text(errors='replace') if (E/'rpmbuild.log').exists() else ''
anchors={a:len(re.findall(r'^'+a+r'(?: |$)',text,re.M)) for a in ['BOLT_BUILDROOT_OK','BOLT_PROC_OK','BOLT_PROC_MISSING','BOLT_TOOL_DRY_RUN_BEGIN','BOLT_TOOL_DRY_RUN_END','BOLT_NINJA_EXIT_0','BOLT_PIPELINE_PASS','BOLT_COMPARE_ROOT_PASS','BOLT_POST_GATE_PASS']}
checks={'anchors':anchors,'rpmbuild_final_lines':text.splitlines()[-45:],'historical_candidate_sha256':'4ec07159aeb4f9300361b95955db05bfca06ece5b748796b28e9b8965145fff9','candidate_sha_equality_required':False}
(E/'execution-summary.json').write_text(json.dumps(checks,indent=2)+'\n');print(json.dumps({'resources':result,'anchors':anchors},indent=2))
