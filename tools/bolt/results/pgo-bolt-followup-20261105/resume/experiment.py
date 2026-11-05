from pathlib import Path
import subprocess,json,os,sys,time,hashlib,datetime,importlib.util,re,statistics
W=Path('/home/linhao/Toolchain/development/llvm-optimize'); B=Path(str(W)+'-bolt')
F=W/'temp/pgo-bolt-followup-20261105'; E=Path(__file__).resolve().parent
D=W/'temp/pgo-resource-20261102/full/stage-D/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0'
T=W/'temp/night-20261103/toolchain/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0'
rel=Path('home/abuild/rpmbuild/BUILD/llvm-22.1.8/build')
def now():return datetime.datetime.now().astimezone().isoformat()
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(2**20),b''):h.update(b)
 return h.hexdigest()
def save(p,v):p.write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
def prefix(root):return [str(root/'lib64/ld-linux-x86-64.so.2'),'--library-path',':'.join(str(p) for p in [root/rel/'lib',root/rel/'lib64',root/'usr/lib64',root/'lib64'])]
def identity(p):return {'path':str(p),'bytes':p.stat().st_size,'sha256':sha(p)}
records=[]
phase=sys.argv[1]; out=E/phase;out.mkdir(exist_ok=False);work=F/phase;work.mkdir(exist_ok=False)
(work/'tmp').mkdir();env=dict(os.environ,TMPDIR=str(work/'tmp'),LC_ALL='C');env.pop('LLVM_PROFILE_FILE',None)
def run(tag,argv,stdout=None):
 log=out/(tag+'.log');timing=out/(tag+'.time');a=['/usr/bin/time','-v','-o',str(timing),*map(str,argv)];start=time.monotonic();load_before=os.getloadavg()
 save(out/(tag+'.argv.json'),a)
 with (stdout or log).open('xb') as so:
  if stdout:
   with log.open('xb') as se:r=subprocess.run(a,stdout=so,stderr=se,env=env,cwd=work)
  else:r=subprocess.run(a,stdout=so,stderr=subprocess.STDOUT,env=env,cwd=work)
 text=timing.read_text();m=re.search(r'Maximum resident set size \(kbytes\): (\d+)',text)
 row={'load_before':load_before,'load_after':os.getloadavg(),'tag':tag,'rc':r.returncode,'wall_s':time.monotonic()-start,'max_rss_bytes':int(m[1])*1024 if m else None,'argv':a};records.append(row);save(out/'commands.json',records)
 print(tag,'rc='+str(r.returncode),'wall='+str(row['wall_s']),flush=True)
 if r.returncode:raise RuntimeError(tag+' exit '+str(r.returncode))
 return row
status='failed';reason='not-completed';start=time.monotonic()
try:
 if phase=='instrument':
  assert sha(F/'reference-relocs-clang-22')=='1a72e99d92b857524a82c5cff257b48fc72b56e6290f6b90cd5d0dadd31741f7'
  (F/'profiles').mkdir(exist_ok=False)
  output=work/'clang-22'
  run('bolt-instrument',prefix(D)+[F/'llvm-bolt',F/'reference-relocs-clang-22','-instrument','--thread-count=1','-runtime-instrumentation-lib='+str(F/'tools/libbolt_rt_instr.a'),'-instrumentation-file='+str(F/'profiles/clang'),'-instrumentation-file-append-pid','-instrumentation-binpath='+str(output),'-o',output])
  output.chmod(0o755);save(out/'output.json',identity(output))
 elif phase=='train':
  units=json.loads((E.parent/'training.json').read_text());assert len(units)==23; rows=[]
  for i,u in enumerate(units):
   assert sha(u['path'])==u['sha256'];before=set((F/'profiles').glob('*.fdata'))
   args=u['compiler_args'];rec=run('%02d-%s'%(i,u['name']),prefix(D)+[F/'instrument/clang-22','--driver-mode=g++',*args,'-c',u['path'],'-o',work/(u['name']+'.o')])
   created=set((F/'profiles').glob('*.fdata'))-before
   assert len(created)==1,repr(created)
   p=created.pop();assert p.stat().st_size>0;rows.append({'unit':u,'profile':identity(p),'measurement':rec});save(out/'profiles.json',rows)
 elif phase=='merge':
  profiles=[Path(r['profile']['path']) for r in json.loads((E/'train/profiles.json').read_text())];assert len(profiles)==23
  p=work/'merged.fdata';run('merge-fdata',prefix(D)+[F/'tools/merge-fdata',*profiles],stdout=p);assert p.stat().st_size>0;save(out/'output.json',identity(p))
 elif phase=='optimize':
  opts=json.loads((E.parent/'options.json').read_text())['OPTIONS'];p=work/'clang-22';argv=prefix(D)+[F/'llvm-bolt',F/'reference-relocs-clang-22','-o',p,'-data='+str(F/'merge/merged.fdata'),*opts];run('bolt-optimize',argv);p.chmod(0o755)
  spec=importlib.util.spec_from_file_location('helper',W/'temp/debuglink-tb20261026/source/packaging/clang-bolt-helper.py');helper=importlib.util.module_from_spec(spec);spec.loader.exec_module(helper)
  counts=helper.match_counts((out/'bolt-optimize.log').read_text(),list(map(str,argv)),True,True);save(out/'profile-counts.json',counts);save(out/'output.json',identity(p));print('PROFILE_GATE_PASS',json.dumps(counts),flush=True)
 elif phase=='speed':
  units=json.loads((E.parent/'training.json').read_text());compilers={'nonpgo-bolt':(T,T/rel/'clang-bolt/clang.bolt.stripped'),'pgo':(D,D/rel/'clang-bolt/ordinary-clang-22'),'pgo-bolt':(D,F/'optimize/clang-22')}
  # Final non-PGO BOLT candidate path is supplied by the preserved identity.
  candidates=[T/rel/'clang-bolt/clang.candidate',T/rel/'clang-bolt/clang.bolt.stripped',T/rel/'clang-bolt/candidate/clang-22',T/rel/'clang-bolt/clang-22.bolt',T/rel/'bin/clang-22']
  expected='6c63c5c26bf68a7079d69ac8a41500c696267e1553a44e8be839632e9d676f17'
  matches=[p for p in candidates if p.is_file() and sha(p)==expected]
  assert matches,'certified T candidate not found in declared paths';compilers['nonpgo-bolt']=(T,matches[0]);save(out/'compiler-identities.json',{k:identity(p) for k,(r,p) in compilers.items()})
  rows=[]
  for rnd in range(3):
   names=list(compilers);names=names[rnd:]+names[:rnd]
   for name in names:
    root,compiler=compilers[name]
    for i,u in enumerate(units):
     args=[x for x in u['compiler_args'] if not re.fullmatch(r'-O(?:[0-3sgz]|fast)',x)];args+=['-O2']
     rec=run('%d-%s-%02d'%(rnd,name,i),prefix(root)+[compiler,'--driver-mode=g++',*args,'-c',u['path'],'-o',work/('%d-%s-%02d.o'%(rnd,name,i))]);rows.append({'round':rnd,'compiler':name,'unit':u['name'],**rec});save(out/'measurements.json',rows)
  summary={name:{'round_wall_s':[sum(r['wall_s'] for r in rows if r['compiler']==name and r['round']==n) for n in range(3)],'max_rss_bytes':max(r['max_rss_bytes'] for r in rows if r['compiler']==name)} for name in compilers}
  for v in summary.values():v['median_wall_s']=statistics.median(v['round_wall_s'])
  save(out/'summary.json',summary)
 else:raise ValueError(phase)
 status='ok';reason='completed'
except BaseException as e:
 reason=repr(e);raise
finally:
 save(out/'result.json',{'status':status,'reason':reason,'wall_s':time.monotonic()-start,'time':now()});print(phase.upper(),'已结束',now(),'status='+status,'reason='+reason,flush=True)
