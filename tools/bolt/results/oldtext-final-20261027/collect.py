"""Collect build evidence without changing source, artifacts, mounts or services."""
from pathlib import Path
import datetime,gzip,json,hashlib,shutil,re,subprocess,tarfile
W=Path('/home/linhao/Toolchain/development/llvm-optimize');D=Path(__file__).resolve().parent;E=W.parent/'llvm-optimize-bolt/tools/bolt/results/oldtext-final-20261027';R=D/'gbs-root/local/BUILD-ROOTS/scratch.x86_64.0';BUILD=R/'home/abuild/rpmbuild/BUILD/llvm-22.1.8/build';WORK=BUILD/'clang-bolt'
def save(name,obj):
 p=E/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,indent=2)+'\n')
for p in D.glob('*.py'):shutil.copyfile(p,E/p.name)
for base,prefix in [(WORK,'bolt-work')]:
 if base.exists():
  for p in base.rglob('*'):
   if p.is_file() and not p.is_symlink() and p.suffix in ('.json','.jsonl','.txt','.log','.sh','.original','.c','.cmake'):
    dest=E/prefix/p.relative_to(base);dest.parent.mkdir(parents=True,exist_ok=True)
    if p.stat().st_size>4*1024**2:
     with p.open('rb') as src,gzip.open(str(dest)+'.gz','wb') as out:shutil.copyfileobj(src,out)
    else:shutil.copyfile(p,dest)
native=BUILD/'native-archive-conversion'
if native.exists():
 with tarfile.open(E/'native-archive-evidence.tar.gz','w:gz') as out:
  for p in sorted(native.rglob('*')):
   if p.is_file() and not p.is_symlink() and p.suffix in ('.json','.jsonl','.txt','.log','.sh','.time'):
    out.add(p,arcname=str(p.relative_to(native)),recursive=False)
 if (native/'summary.json').exists():
  summary=json.loads((native/'summary.json').read_text());brief={k:v for k,v in summary.items() if k!='archives'}
  brief['archive_count']=len(summary.get('archives',[]));brief['archives']=[{k:v for k,v in a.items() if k!='results'} for a in summary.get('archives',[])]
  save('native-archives-summary.json',brief)
if BUILD.exists():
 for p in [BUILD/'CMakeCache.txt',BUILD/'build.ninja',BUILD/'CMakeFiles/rules.ninja']:
  if p.exists():
   dest=E/'build-metadata'/p.relative_to(BUILD);dest.parent.mkdir(parents=True,exist_ok=True)
   with p.open('rb') as src,gzip.open(str(dest)+'.gz','wb') as out:shutil.copyfileobj(src,out)
lines=(E/'rpm-build.log').read_text(errors='replace').splitlines();origin=None;anchors=[];last_exit=None
for i,line in enumerate(lines,1):
 if 'started "build llvm.spec" at ' in line:
  stamp=line.split(' at ',1)[1].rstrip('.');origin=datetime.datetime.strptime(stamp,'%a %b %d %H:%M:%S UTC %Y').replace(tzinfo=datetime.timezone.utc).timestamp()
 m=re.match(r'\[\s*(\d+)s\]\s?(.*)',line)
 if not m:continue
 sec=int(m[1]);text=m[2];kind=None
 if text.strip()=='+ exit 0':last_exit=dict(kind='build-end',line=i,elapsed_seconds=sec,time_ns=int((origin+sec)*1e9),raw=line)
 if 'Executing(%install)' in text and last_exit:anchors.append(last_exit)
 patterns=[('prep',r'Executing\(%prep\)'),('build',r'Executing\(%build\)'),('install',r'Executing\(%install\)'),('native-start',r'^NATIVE_ARCHIVES_BEGIN '),('native-end',r'^NATIVE_ARCHIVES_END '),('find-debuginfo',r'^\+ /usr/lib/rpm/find-debuginfo.sh'),('packaging',r'^Processing files:'),('finished',r' finished "build llvm.spec"'),('pipeline-pass',r'^BOLT_PIPELINE_PASS$'),('compare-root',r'^BOLT_COMPARE_ROOT_PASS$'),('post-pass',r'^BOLT_POST_GATE_PASS$'),('cache-release',r'^BOLT_CACHE_RELEASE '),('gate-failed',r'^BOLT_GATE_FAILED:'),('disk-report',r'^BOLT_DISK_REPORT ')]
 for n,pat in patterns:
  if re.search(pat,text):kind=n;break
 if text.startswith('+ python3') and 'disk-report ' in text:kind='disk-'+text.rsplit('disk-report ',1)[1].strip()
 if kind:anchors.append(dict(kind=kind,line=i,elapsed_seconds=sec,time_ns=int((origin+sec)*1e9) if origin else None,raw=line))
assert origin is not None
(E/'timeline.tsv').write_text('kind\tline\telapsed_seconds\tUTC\traw\n'+''.join(f"{a['kind']}\t{a['line']}\t{a['elapsed_seconds']}\t{datetime.datetime.fromtimestamp(a['time_ns']/1e9,datetime.timezone.utc).isoformat()}\t{a['raw']}\n" for a in anchors))
rows=[json.loads(l) for l in (E/'du-root.jsonl').read_text().splitlines()];valid=[dict(time_ns=r['time_ns'],end_ns=r['time_ns']+int(r['seconds']*1e9),bytes=int(r['stdout'].split()[0]),scan_seconds=r['seconds']) for r in rows if r.get('rc')==0 and r.get('stdout','').split() and r['stdout'].split()[0].isdigit()]
starts={}
for a in anchors:starts.setdefault(a['kind'],a['time_ns'])
end=max([r.get('end_ns',r['time_ns']) for r in valid]+[int((origin+int(re.match(r'\[\s*(\d+)s\]',lines[-1])[1]))*1e9)] if re.match(r'\[\s*(\d+)s\]',lines[-1]) else [int(origin*1e9)])
for f in ('build-result.json','controller-result.json'):
 if (E/f).exists():end=max(end,json.loads((E/f).read_text())['end_ns'])
starts.setdefault('finished',end)
phases={}
for name,begin,finish in [('ordinary-build','build','install'),('ordinary-install','install','disk-begin'),('BOLT','disk-begin','compare-root'),('cache-release','compare-root','native-start'),('native-conversion-install','native-start','find-debuginfo'),('platform-post','find-debuginfo','packaging'),('packaging','packaging','finished')]:
 if begin in starts:
  finish_ns=starts.get(finish,end);samples=[v for v in valid if starts[begin]<=v['time_ns'] and v['end_ns']<=finish_ns];phases[name]=dict(start_ns=starts[begin],end_ns=finish_ns,samples=len(samples),peak=max(samples,key=lambda x:x['bytes']) if samples else None,completed=finish in starts)
base=json.loads((W/'docs/53_hybrid_local_validation_evidence/disk-comparison.json').read_text())
save('disk-comparison.json',dict(peak=max(valid,key=lambda x:x['bytes']) if valid else None,complete_samples=len(valid),missing_samples=len(rows)-len(valid),phases=phases,anchors=anchors,hybrid_peak_bytes=base['peak']['bytes'],static_bolt_peak_bytes=base['baseline_peak_bytes'],limitations=['60-second scheduled du, scan timeout/missing preserved; discrete observed lower bound, not continuous peak','Prior full-static+BOLT had interrupted-linker residue; no causality claim for all observed differences']))
(E/'excerpts.txt').write_text('\n'.join(f"{i}: {l}" for i,l in enumerate(lines,1) if any(x in l for x in ['BOLT_','Executing(%','NATIVE_ARCHIVES_BEGIN','NATIVE_ARCHIVES_END']) or i>len(lines)-200)+'\n')
audit={}
for name,argv in [('source',['git','-C',str(D/'source'),'show','-s','--format=%H%n%T%n%P%n%an <%ae>%n%cn <%ce>']),('source_status',['git','-C',str(D/'source'),'status','--porcelain']),('df_home',['df','-B1','/home']),('mounts',['findmnt','-rn','-o','TARGET,SOURCE,FSTYPE']),('services',['systemctl','--user','show','oldtext-final-20261027.service','bolt-on-hybrid-controller-20261024.service','-p','Id','-p','ActiveState','-p','Result'])]:
 p=subprocess.run(argv,capture_output=True,text=True);audit[name]=dict(argv=argv,rc=p.returncode,stdout=p.stdout,stderr=p.stderr)
save('final-audit.json',audit)
print('COLLECTED',len(lines),'log lines,',len(valid),'complete samples')
