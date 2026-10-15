from pathlib import Path
import sys,json,shutil,subprocess,time,os,math,statistics
from new_session import E,R1,INNER,HOST,root_command
B=Path('/home/linhao/Toolchain/development/llvm-optimize-bolt');sys.path.insert(0,str(B/'tools/bolt'));import bolt_helper as h
target=json.loads((E/'active-target.json').read_text())['target'];units=json.loads((E/('assets-'+target+'-units.json')).read_text());assert len(units)==30
allowed=sorted(os.sched_getaffinity(0));cpu=2;h.require(cpu in allowed,'CPU2 unavailable');slot=HOST/'compiler/clang-22';h.disk_preflight(slot.parent,16*1024**3)
policy=Path('/sys/devices/system/cpu/cpu'+str(cpu)+'/cpufreq');topology=Path('/sys/devices/system/cpu/cpu'+str(cpu)+'/topology')
def readoptional(p):return p.read_text().strip() if p.exists() else 'unavailable'
def conditions():return {'host_loadavg':Path('/proc/loadavg').read_text().strip(),'cpu_current_kHz':readoptional(policy/'scaling_cur_freq'),'cpu_governor':readoptional(policy/'scaling_governor'),'monotonic':time.monotonic()}
# Require a quiet admission on the selected core; the shared lock excludes other heavy stages.
def core_ticks():
 line=next(x for x in Path('/proc/stat').read_text().splitlines() if x.startswith('cpu'+str(cpu)+' '));v=[int(x) for x in line.split()[1:]];return sum(v),v[3]+(v[4] if len(v)>4 else 0)
admission=[];deadline=time.monotonic()+3600
while True:
 a=core_ticks();time.sleep(1);b=core_ticks();delta=b[0]-a[0];busy=1-(b[1]-a[1])/max(1,delta);row={'selected_core_busy_fraction':busy,**conditions()};admission.append(row)
 if busy<=0.05:break
 if time.monotonic()>deadline:raise RuntimeError('STOP_QUIET_CPU_ADMISSION_TIMEOUT')
 print('WAIT_QUIET_CPU',cpu,busy,flush=True);time.sleep(10)
# Scope timeout/lock limit independently cap this stage; do not hold for another hour.
model=next((x.split(':',1)[1].strip() for x in Path('/proc/cpuinfo').read_text().splitlines() if x.startswith('model name')),'unavailable')
metadata={'CPU_model':model,'fixed_cpu':cpu,'host_affinity':allowed,'thread_siblings':readoptional(topology/'thread_siblings_list'),'governor':readoptional(policy/'scaling_governor'),'driver':readoptional(policy/'scaling_driver'),'min_kHz':readoptional(policy/'scaling_min_freq'),'max_kHz':readoptional(policy/'scaling_max_freq'),'parallel_compiles':1,'quiet_admission':admission,'order':'five rounds; ordinary then candidate on rounds 0/2/4, candidate then ordinary on rounds 1/3','same_entity_path':INNER+'/compiler/clang-22','timing':'record_call subprocess wall_s for taskset+clang only; prefix, chroot and compiler-copy/SHA outside timer','source_selection':'30 '+target+' entries from the90 SHA-certified assets;cohort repetitions retain requested weighting','target':units[0]['target'],'no_outliers_deleted':True}
slot_identity=(slot.stat().st_dev,slot.stat().st_ino);metadata['compiler_inode']=list(slot_identity)
rows=[{'key':u['key'],'source_id':u['source_id'],'cohort':u['provenance']['cohort'],'input_sha256':u['input_sha256'],'ordinary_s':[],'candidate_s':[],'measurements':[]} for u in units];start=time.monotonic();value={'status':'RUNNING','conditions':metadata,'rows':rows}
def save():value['wall_s']=time.monotonic()-start;h.save(E/('performance-'+target+'.json'),value)
for round_number in range(5):
 for role in (['ordinary','candidate'] if round_number%2==0 else ['candidate','ordinary']):
  source=R1/'home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/bin/clang-22' if role=='ordinary' else R1/'home/abuild/bolt-work/bolt-v4-20261014-fallback/clang.candidate';sha='7df0ff90dbca7f99ed6a642546281584dbfaab1528a94abf7a1bb524ca371b2c' if role=='ordinary' else '4ec07159aeb4f9300361b95955db05bfca06ece5b748796b28e9b8965145fff9'
  shutil.copyfile(source,slot);slot.chmod(0o755);h.require((slot.stat().st_dev,slot.stat().st_ino)==slot_identity,'compiler inode changed');h.require(h.digest(slot)==sha,'performance compiler copy identity mismatch')
  for i,u in enumerate(units):
   d=HOST/'performance'/u['key'];d.mkdir(parents=True,exist_ok=True);inner=INNER+'/performance/'+u['key'];args=list(u['argv']);args[-1]=inner+'/same.o';argv=['/usr/bin/taskset','-c',str(cpu)]+args;label='perf-'+target+'-'+str(round_number)+'-'+role+'-'+str(i).zfill(2)
   before=conditions();command='. '+h.quote(INNER+'/rpm-env-prefix.sh')+'; cd '+h.quote(inner)+'; exec python3 '+h.quote(INNER+'/record_call.py')+' '+h.quote(label)+' '+' '.join(h.quote(x) for x in argv)
   with (E/(label+'.txt')).open('w') as log:p=root_command(['/bin/sh','-c',command],True,stdout=log,stderr=subprocess.STDOUT,timeout=600)
   h.require(p.returncode==0,'performance compile failed '+label)
   measurement=json.loads((HOST/'calls'/(label+'.json')).read_text());rows[i][role+'_s'].append(measurement['wall_s']);rows[i]['measurements'].append({'round':round_number,'role':role,'wall_s':measurement['wall_s'],'before':before,'after':conditions(),'call':measurement});save()
   print('PERF',round_number,role,i+1,'/30',round(measurement['wall_s'],6),flush=True)
for row in rows:
 assert len(row['ordinary_s'])==len(row['candidate_s'])==5
 row['ordinary_median_s']=statistics.median(row['ordinary_s']);row['candidate_median_s']=statistics.median(row['candidate_s']);row['ratio']=row['candidate_median_s']/row['ordinary_median_s']
ratio=math.exp(statistics.mean(math.log(row['ratio']) for row in rows));value.update(geometric_mean_ratio=ratio,speedup_percent=(1-ratio)*100,criterion='candidate/ordinary geometric mean strictly < 0.98',status='PASS' if ratio<0.98 else 'FAIL_PERFORMANCE');save();print('PERFORMANCE',value['status'],'GEOMEAN',ratio,flush=True)
groups={}
for row in rows:groups.setdefault(row['source_id'],[]).append(row)
unique=[]
for source,group in sorted(groups.items()):
 ordinary_samples=[v for row in group for v in row['ordinary_s']];candidate_samples=[v for row in group for v in row['candidate_s']]
 om=statistics.median(ordinary_samples);cm=statistics.median(candidate_samples)
 unique.append({'source_id':source,'entry_count':len(group),'samples_per_role':len(ordinary_samples),'ordinary_median_s':om,'candidate_median_s':cm,'ratio':cm/om,'entry_median_geomean_ratio':math.exp(statistics.mean(math.log(row['ratio']) for row in group))})
assert len(unique)==20
holdout=[row for row in rows if row['cohort']=='arm-holdout'];assert len(holdout)==10
value['unique_sources']=unique
value['unique20_geometric_mean_ratio']=math.exp(statistics.mean(math.log(row['ratio']) for row in unique))
value['unique20_entry_median_weighted_ratio']=math.exp(statistics.mean(math.log(row['entry_median_geomean_ratio']) for row in unique))
value['holdout10_geometric_mean_ratio']=math.exp(statistics.mean(math.log(row['ratio']) for row in holdout))
value['unique20_method']='Group identical original source paths and input SHAs; pool all5/10 samples per role before median;20 source ratios equally weighted. No samples deleted.'
loads=[float(m[side]['host_loadavg'].split()[0]) for row in rows for m in row['measurements'] for side in ('before','after')]
freqs=[int(m[side]['cpu_current_kHz']) for row in rows for m in row['measurements'] for side in ('before','after') if m[side]['cpu_current_kHz'].isdigit()]
value['runtime_summary']={'load1_min':min(loads),'load1_median':statistics.median(loads),'load1_max':max(loads),'frequency_samples':len(freqs),'frequency_kHz_min':min(freqs) if freqs else None,'frequency_kHz_median':statistics.median(freqs) if freqs else None,'frequency_kHz_max':max(freqs) if freqs else None,'same_compiler_inode_verified_all10_copies':True,'total_compiles':sum(len(row['measurements']) for row in rows)}
save();sys.exit(0 if ratio<0.98 else 1)

