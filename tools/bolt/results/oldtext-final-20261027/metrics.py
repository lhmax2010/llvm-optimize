from pathlib import Path
import json,re,subprocess,datetime
D=Path(__file__).resolve().parent;E=D.parent.parent.parent/'llvm-optimize-bolt/tools/bolt/results/oldtext-final-20261027';W=D.parent.parent;R=D/'gbs-root/local/BUILD-ROOTS/scratch.x86_64.0';WORK=R/'home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/clang-bolt'
rows=(E/'rpm-build.log').read_text(errors='replace').splitlines();a={}
for i,s in enumerate(rows,1):
 m=re.match(r'\[\s*(\d+)s\] (.*)',s)
 if not m:continue
 text=m[2];key=None
 if text.startswith('BOLT_DISK_REPORT '):key='disk-'+json.loads(text.removeprefix('BOLT_DISK_REPORT '))['stage']
 if text=='BOLT_COMPARE_ROOT_PASS':key='compare-root'
 if text=='BOLT_NINJA_EXIT_0':key='tool-end'
 if text.startswith('+ bolt_checked tool-build '):key='tool-start'
 if key and key not in a:a[key]={'line':i,'seconds':int(m[1]),'raw':s}
prev=json.loads((E.parent/'runpath-fix-20261026/timing-comparison.json').read_text())['current_durations']
metrics={'anchors':a,'durations':{'begin_to_compare_root':a['compare-root']['seconds']-a['disk-begin']['seconds'],'ninja_tool_build':a['tool-end']['seconds']-a['tool-start']['seconds']},'previous_37':prev}
obs=[json.loads(l) for l in (E/'bolt-process.jsonl').read_text().splitlines()]
found=[x for x in obs if x['event']=='found'];gone=[x for x in obs if x['event']=='gone'];samples=[x for x in obs if x['event']=='sample'];hwm=[int(x['VmHWM'].split()[0]) for x in samples if 'VmHWM' in x]
metrics['rewrite_observed']={'pid':found[0]['pid'] if found else None,'seconds':(gone[-1]['time_ns']-found[0]['time_ns'])/1e9 if found and gone else None,'sampled_max_VmHWM_KiB':max(hwm) if hwm else None,'sample_count':len(samples),'note':'Observed /proc process window and 10ms VmHWM samples; sampling lower bound, not wait4 rusage.'}
metrics['rewrite_file_times']={}
for name,p in [('new',WORK/'rewrite/bolt.log'),('previous_37',W/'temp/runpath-fix-20261026/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/clang-bolt/rewrite/bolt.log')]:
 r=subprocess.run(['stat','--printf=%w\n%y\n',str(p)],text=True,capture_output=True)
 metrics['rewrite_file_times'][name]={'path':str(p),'rc':r.returncode,'stdout':r.stdout,'stderr':r.stderr,'note':'File creation to last log write is a file-timestamp approximation, not a process timer.'}
old=json.loads((E.parent/'runpath-fix-20261026/continue/oldtext-result.json').read_text());metrics['previous_oldtext_experiment']={'seconds':old['seconds'],'max_RSS_KiB':9686616,'method':'GNU time -v; report 37 section 10.3'}
(E/'timing-comparison.json').write_text(json.dumps(metrics,indent=2)+'\n')
print(json.dumps({k:v for k,v in metrics.items() if k not in ('anchors','rewrite_file_times')},indent=2))
