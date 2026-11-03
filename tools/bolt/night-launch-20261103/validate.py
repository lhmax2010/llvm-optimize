"""Post-build checks; all writes go to a fresh validation directory, not history."""
from pathlib import Path
import argparse,os,json,subprocess,shutil,time,traceback,stat,importlib.util,re,mmap
from checks import *
from rpm_io import manifest
from rpm_extract import extract_selected
W=Path('/home/linhao/Toolchain/development/llvm-optimize')
B=W.parent/'llvm-optimize-bolt';T=Path(__file__).parent
CERT=W/'temp/debuglink-20261028/full-20261030'
SOURCE=W/'temp/review-20261102/source'

def rootpaths(D):
 R=D/'gbs-root/local/BUILD-ROOTS/scratch.x86_64.0';BUILD=R/'home/abuild/rpmbuild/BUILD/llvm-22.1.8/build';return R,BUILD,BUILD/'clang-bolt'

def run(argv,out,cwd=None,env=None,timeout=600):
 start=time.monotonic();p=subprocess.run([str(x) for x in argv],capture_output=True,text=True,cwd=cwd,env=env,timeout=timeout)
 Path(str(out)+'.stdout').write_text(p.stdout);Path(str(out)+'.stderr').write_text(p.stderr);save(str(out)+'.json',dict(argv=[str(x) for x in argv],rc=p.returncode,seconds=time.monotonic()-start));assert p.returncode==0,(argv,p.returncode,p.stderr[-3000:]);return p.stdout

def free():assert shutil.disk_usage('/home').free>=20*1024**3,'disk-stop: /home below 20GiB'
def loader(R,b):return [R/'lib64/ld-linux-x86-64.so.2','--library-path',str(R/'lib64')+':'+str(R/'usr/lib64'),b]
def packages(D):
 P=D/'products'; rpms=sorted(P.glob('RPMS/*.rpm'))+sorted(P.glob('SRPMS/*.rpm'))
 if not rpms:rpms=sorted((D/'gbs-root/local').glob('repos/**/*.rpm'))
 assert rpms,'no RPM products';out={}
 for rpm in rpms:
  p=subprocess.run(['rpm','-qp','--qf','%{NAME}\t%{ARCH}',str(rpm)],capture_output=True,text=True);assert p.returncode==0,(rpm,p.stderr);key=p.stdout.strip();key=key.split('\t')[0]+'\tsrc' if rpm.name.endswith('.src.rpm') else key;assert key not in out,('duplicate package',key);out[key]=rpm
 return out

def verify_manifest(P,O):
 rows=[]
 for line in (P/'SHA256SUMS').read_text().splitlines():
  hh,name=line.split(None,1);name=name.lstrip('* ');p=P/name;assert p.resolve().is_relative_to(P.resolve());actual=sha(p);assert actual==hh,(p,hh,actual);rows.append(dict(path=str(p),sha256=actual))
 save(O/'certified-sha-check.json',rows)

def rpm_compare(D,O,oldD,source_allowed):
 new,old=packages(D),packages(oldD);assert len(new)==23 and set(new)==set(old),(len(new),set(new)^set(old));rows=[];manifests={}
 for key in sorted(new):
  free();aa=manifest(old[key]);bb=aa if old[key]==new[key] else manifest(new[key]);manifests[key]=bb;assert set(aa)==set(bb),(key,'paths added/removed',set(aa)^set(bb))
  changes=[];times=[];proofs=[]
  for name in aa:
   a,b=dict(aa[name]),dict(bb[name]);at=a.pop('mtime');bt=b.pop('mtime')
   if at!=bt:times.append(dict(path=name,old=at,new=bt))
   if a!=b:changes.append(name)
  folder=O/'rpm-bytes'/key.replace('\t','-')
  if changes:
   extract_selected(old[key],set(changes),folder/'old');extract_selected(new[key],set(changes),folder/'new')
  for name in changes:
   a,b=aa[name],bb[name];assert all(a.get(k)==b.get(k) for k in ('mode','uid','gid','target')),(key,name,'metadata changed')
   x,y=folder/'old'/name,folder/'new'/name
   if key.endswith('\tsrc') and source_allowed:
    export=D/'export'/name;assert export.is_file() and sha(export)==sha(y),(name,'source payload is not the exact pinned export');proof=dict(classification='declared-source-export-change',export=str(export),old_sha=sha(x),new_sha=sha(y))
   else:proof=content_proof(x.read_bytes(),y.read_bytes())
   proofs.append(dict(path=name,**proof))
  row=dict(package=key,old_rpm=str(old[key]),new_rpm=str(new[key]),files=len(aa),content_changes=proofs,payload_mtime_changes=times,ar_date_only_files=sum(p['classification']=='allowed-ar-date-difference' for p in proofs),command_record_files=sum('command-record' in p['classification'] for p in proofs),PASS=True)
  rows.append(row);save(O/'rpm23.json',rows);save(O/(key.replace('\t','-')+'-manifest.json'),bb);print('RPM_PASS',key,flush=True)
 return manifests

def objects(D,O,reference):
 R,BUILD,WORK=rootpaths(D);units=json.loads((W/'docs/53_hybrid_local_validation_evidence/tu-inputs.json').read_text());assert len(units)==90
 V=O/'objects';V.mkdir();slot=V/'clang-22';slot.touch();ino=slot.stat().st_ino;results={}
 for role,src in [('reference',reference),('candidate',WORK/'clang.candidate')]:
  shutil.copyfile(src,slot);slot.chmod(0o755);assert slot.stat().st_ino==ino and sha(slot)==sha(src)
  for u in units:
   free();i=u['index'];d=V/f'{i:03d}';d.mkdir(exist_ok=True);inp=d/'input.ii';assert sha(u['copy'])==u['sha256']
   if not inp.exists():shutil.copyfile(u['copy'],inp)
   out=d/'same.o'
   # Fresh empty output prevents a stale success; no unlink or directory removal.
   with out.open('wb'):pass
   args=list(u['original_argv'][1:]);args.insert(0,'--no-default-config');args[args.index('-c')+1]=str(inp);args[args.index('-o')+1]=str(out);args=[('-resource-dir='+str(BUILD/'lib64/clang/22') if x.startswith('-resource-dir=') else x) for x in args]
   argv=loader(R,slot)+args;run(argv,d/(role+'-command'),cwd=V,env={**os.environ,'LC_ALL':'C'});assert out.is_file() and out.stat().st_size>0
   row=dict(target=u['target'],key=u['key'],sha256=sha(out),input_sha256=u['sha256'])
   if role=='reference':shutil.copyfile(out,d/'reference.o');results[i]={'reference':row}
   else:results[i]['candidate']=row;results[i]['byte_equal']=(d/'reference.o').read_bytes()==out.read_bytes();assert results[i]['byte_equal'],i
   save(O/'objects-progress.json',results)
  print('OBJECT_ROLE_DONE',role,flush=True)
 save(O/'objects90.json',dict(PASS=True,total=90,passed=90,reference=str(reference),reference_sha256=sha(reference),candidate_sha256=sha(WORK/'clang.candidate'),same_path_inode=ino,results=results))

def extra_identity(D,O,project):
 R,BUILD,WORK=rootpaths(D);identity=json.loads((WORK/'identity.json').read_text());proofs={}
 assert sha(WORK/'clang.bolt')==identity['before_sha256']
 state=json.loads((WORK/'install-state.json').read_text());assert state['installed_sha256']==identity['after_sha256']
 post=json.loads((WORK/'post-gate/post-result.json').read_text());assert all(post[k] is True for k in ['sha_unchanged','aliases_pass','strip_identity_pass']);save(O/'post-gate.json',post)
 tool=json.loads((WORK/'tool-build-verification.json').read_text());plan=json.loads((WORK/'tool-plan.json').read_text());assert tool['tool_build_verified'] is True and tool['planned_tasks']==tool['executed_tasks']==plan['tasks'];save(O/'tool-verify.json',tool);save(O/'tool-plan.json',plan)
 dynamic=run(['readelf','-d',WORK/'clang.candidate'],O/'candidate-dynamic');assert '(RPATH)' not in dynamic and re.findall(r'\(RUNPATH\).*?\[(.*?)\]',dynamic)==['$ORIGIN/../lib64']
 for name in ['tool-dry-run.txt','rewrite/bolt.log']:
  p=WORK/name;assert p.is_file();shutil.copyfile(p,O/('raw-'+p.name))
 if project=='toolchain':
  for name in ['ordinary-clang-22','clang-22.debug']:
   old=CERT/'products/binaries'/name;new=WORK/name;oldsha,newsha=sha(old),sha(new)
   proof={'classification':'identical'} if oldsha==newsha else content_proof(old.read_bytes(),new.read_bytes())
   proofs[name]=dict(old_sha256=oldsha,new_sha256=newsha,**proof)
 save(O/'identity-chain-extra.json',dict(prestrip_sha=identity['before_sha256'],installed_sha=state['installed_sha256'],comparisons=proofs,PASS=True))

def main(args):
 D=args.root;O=args.output or D/'validation';O.mkdir(parents=True,exist_ok=False);R,BUILD,WORK=rootpaths(D);result={'status':'failed','project':args.project,'checks':{},'historical_selftest':args.certified_selftest}
 try:
  verify_manifest(CERT/'products',O)
  logpath=D/'evidence/rpm-build-final.log'
  if not logpath.exists():logpath=D/'evidence/rpm-build.log'
  log=logpath.read_text(errors='replace');lines=log.splitlines();anchors={}
  needed=['BOLT_NINJA_EXIT_0','BOLT_PIPELINE_PASS','BOLT_COMPARE_ROOT_PASS','BOLT_CACHE_RELEASE','BOLT_POST_GATE_PASS','NATIVE_ARCHIVES_END']
  if args.project=='toolchain':needed+=['BOLT_DEBUG_SYMBOLS_PASS','BOLT_DEBUGLINK_PASS']
  if not args.certified_selftest:needed+=['TIZEN_HYBRID_LINK_OK']
  for token in needed:
   hit=[dict(line=i,text=t) for i,t in enumerate(lines,1) if token in t and '+ echo ' not in t and '+ printf ' not in t];assert hit,('missing anchor',token);anchors[token]=hit
  real=[dict(line=i,text=t) for i,t in enumerate(lines,1) if 'BOLT_REAL_GATE_PASS' in t and '+ echo ' not in t];assert len(real)>=3;anchors['BOLT_REAL_GATE_PASS']=real
  for token in ['BOLT_PROC_OK','BOLT_PROC_MISSING','BOLT_TOOL_DRY_RUN_BEGIN','BOLT_TOOL_DRY_RUN_END','BOLT_DISK_REPORT','BOLT_DISK_DIAGNOSIS']:
   anchors[token]=[dict(line=i,text=t) for i,t in enumerate(lines,1) if token in t and '+ echo ' not in t and '+ printf ' not in t]
  save(O/'anchors.json',anchors);result['checks']['anchors']='PASS'
  if args.certified_selftest:result['checks']['new_flags']='NOT APPLICABLE to historical log; separately tested using 51 real logs'
  else:save(O/'flags.json',flags_check(log,args.project));result['checks']['flags']='PASS'
  pipeline=json.loads((WORK/'pipeline-result.json').read_text());save(O/'profile-and-pipeline.json',pipeline)
  if args.project=='toolchain':assert pipeline['counts']==COUNTS
  else:assert pipeline['counts']['R']<.05 and pipeline['counts']['S_over_N']<.05
  save(O/'profile-log-excerpts.json',[dict(line=i,text=t) for i,t in enumerate(lines,1) if re.search(r'BOLT-(INFO|WARNING).*profile|profile.*functions|mismatch|unmatched',t,re.I)])
  identity=json.loads((WORK/'identity.json').read_text());save(O/'identity.json',identity);assert sha(WORK/'clang.candidate')==identity['after_sha256']
  extra_identity(D,O,args.project)
  if args.project=='toolchain':
   for key,expected in EXPECTED.items():
    if identity[key]!=expected:
     if key!='after_sha256':raise AssertionError((key,'SHA mismatch; original stage bytes unavailable for strict byte proof',identity[key],expected))
     save(O/(key+'-difference.json'),content_proof((CERT/'products/binaries/clang.candidate').read_bytes(),(WORK/'clang.candidate').read_bytes()))
   debug=(WORK/'clang-22.debug').read_bytes();assert hashlib.sha256(debug).hexdigest()==identity['debug_file']['sha256'];proof=debuglink_check((WORK/'clang.candidate').read_bytes(),debug);assert proof['crc32']==identity['debug_file']['crc32'];save(O/'debuglink.json',proof)
   lists=list(BUILD.parent.glob('**/debugfiles.list'));assert lists and any('clang-22.debug' in p.read_text() for p in lists);save(O/'debugfiles.json',[dict(path=str(p),text=p.read_text()) for p in lists])
   manifests=rpm_compare(D,O,CERT,not args.certified_selftest)
   pk=packages(D);ck=next(k for k in pk if k=='clang\tx86_64');dk=next(k for k in pk if k=='clang-debuginfo\tx86_64')
   assert manifests[ck]['usr/bin/clang-22']['sha256']==identity['after_sha256'];assert manifests[dk]['usr/lib/debug/usr/bin/clang-22.debug']['sha256']==identity['debug_file']['sha256']
   objects(D,O,CERT/'products/binaries/clang.candidate');result['checks'].update(identity='PASS',rpm23='PASS',debuglink='PASS',objects90='PASS')
  else:
   from release_checks import release_checks
   release_checks(D,O,args.peer,log,identity)
   reference=rootpaths(args.peer)[2]/'clang.candidate';assert reference.is_file(),'T final clang absent: D/T 90 TU unavailable';objects(D,O,reference);result['checks'].update(release='PASS',objects90='PASS')
  result['status']='ok'
 except BaseException:
  result['error']=traceback.format_exc();(O/'failure.txt').write_text(result['error']);raise
 finally:
  save(O/'result.json',result);print('VALIDATION 已结束',__import__('datetime').datetime.now().astimezone().isoformat(),'status='+result['status'],flush=True)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--project',choices=['toolchain','basedev'],required=True);p.add_argument('--root',type=Path,required=True);p.add_argument('--peer',type=Path);p.add_argument('--output',type=Path);p.add_argument('--certified-selftest',action='store_true');main(p.parse_args())
