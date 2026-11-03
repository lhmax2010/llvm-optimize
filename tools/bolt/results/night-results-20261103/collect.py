from pathlib import Path
import json,gzip,shutil,hashlib,subprocess,re,datetime
B=Path('/home/linhao/Toolchain/development/llvm-optimize-bolt'); W=B.parent/'llvm-optimize';N=W/'temp/night-20261103';E=Path(__file__).parent
provenance=[]
def save(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def copy(p,to):
 if not p.is_file():return
 to.parent.mkdir(parents=True,exist_ok=True)
 if p.stat().st_size>1048576:
  to=to.with_name(to.name+'.gz')
  with p.open('rb') as i,gzip.open(to,'wb',compresslevel=1) as o:shutil.copyfileobj(i,o,1048576)
 else:shutil.copyfile(p,to)
 provenance.append(dict(source=str(p),destination=str(to.relative_to(E)),bytes=p.stat().st_size,sha256=sha(p)))
def cmd(argv,p):
 r=subprocess.run(argv,text=True,capture_output=True);save(p,dict(argv=argv,rc=r.returncode,stdout=r.stdout,stderr=r.stderr));return r
copy(N/'night.log',E/'night.log')
summary={}
for name in ('toolchain','basedev'):
 D=N/name;O=E/name;O.mkdir(exist_ok=True);R=D/'gbs-root/local/BUILD-ROOTS/scratch.x86_64.0';BUILD=R/'home/abuild/rpmbuild/BUILD/llvm-22.1.8/build';WORK=BUILD/'clang-bolt'
 for f in ('plan.json','controller.stdout','controller.stderr'):copy(D/f,O/f)
 for f in ('build-result.json','controller-result.json','result.json','failure.txt','validation-stage.json','validation-command.json','validation.stdout','validation.stderr','resource-table.md','resource-table.json','resources.jsonl','du-root.jsonl','bolt-process.jsonl','phase-events.jsonl','log-restarts.jsonl','run.py','build-runner.py','launcher-used.py','final-audit.json','cleanup-failure.txt'):
  copy(D/'evidence'/f,O/'evidence'/f)
 for f in ('result.json','failure.txt','certified-sha-check.json'):copy(D/'validation'/f,O/'validation'/f)
 copy(BUILD/'CMakeCache.txt',O/'CMakeCache.txt')
 for f in ('identity.json','pipeline-result.json','tool-plan.json','tool-build-verification.json','install-state.json','cache-release.json','post-gate/post-result.json','debug-symbols.json','disk-begin.json','disk-tool-built.json','disk-pipeline.json','disk-post.json'):
  copy(WORK/f,O/'work'/f)
 for p in (BUILD.parent).glob('*debugfiles.list'):copy(p,O/p.name)
 log=next((D/'gbs-driver/local/repos').glob('*/x86_64/logs/success/*/log.txt'));copy(log,O/'gbs-success.log')
 anchors=[];flags=[];native=[];post=[];warning=[]
 with log.open(errors='replace') as f:
  for i,line in enumerate(f,1):
   line=line.rstrip('\n');clean=re.sub(r'^\[\s*\d+s\]\s*','',line)
   if clean.startswith(('TIZEN_LLVM_NORMALIZED_FLAGS','TIZEN_LLVM_DROPPED_FLAGS','TIZEN_LLVM_FLAGS_WARNING')):flags.append(dict(line=i,text=line))
   if 'TIZEN_LLVM_FLAGS_WARNING' in clean and not clean.startswith('+'):warning.append(dict(line=i,text=line))
   if (re.search(r'BOLT_\w+(?:PASS|OK|MISSING)|BOLT_CACHE_RELEASE|TIZEN_HYBRID_LINK_OK|NATIVE_ARCHIVES_(BEGIN|END)',clean) and not clean.startswith('+')) or 'Executing(%' in clean:anchors.append(dict(line=i,text=line))
   if 'find-debuginfo' in clean or ('clang-22' in clean and ('stripped' in clean or 'extracting debug' in clean)) or 'rm -rf /usr/lib/debug' in clean:post.append(dict(line=i,text=line))
   if clean.startswith('NATIVE_ARCHIVE_INSTALLED '):native.append(dict(line=i,record=json.loads(clean.split(' ',1)[1])))
 save(O/'anchors.json',anchors);save(O/'flags.json',flags);save(O/'find-debuginfo.json',post);save(O/'native-installed-records.json',native)
 (O/'anchors.txt').write_text('\n'.join(f"L{r['line']}: {r['text']}" for r in flags+anchors+post)+'\n')
 pkgs=[]
 for p in sorted((D/'gbs-driver/local/repos').glob('*/x86_64/*RPMS/*.rpm')):
  r=subprocess.run(['rpm','-qp','--qf','%{NAME}\t%{ARCH}\t%{SIZE}\n',str(p)],text=True,capture_output=True)
  q=subprocess.run(['rpm','-qpl',str(p)],text=True,capture_output=True)
  row=dict(path=str(p),bytes=p.stat().st_size,query_rc=r.returncode,query=r.stdout,stderr=r.stderr,list_rc=q.returncode,files=q.stdout.splitlines(),list_stderr=q.stderr);pkgs.append(row)
 save(O/'rpm-inventory.json',pkgs)
 acc=D/'evidence/rpm-build.log';st=acc.stat();cache=next(x for x in (BUILD/'CMakeCache.txt').read_text().splitlines() if x.startswith('CMAKE_MODULE_LINKER_FLAGS:'))
 summary[name]=dict(log_source=str(log),log_bytes=log.stat().st_size,log_lines=i,accumulator_bytes=st.st_size,accumulator_allocated=st.st_blocks*512,log_restart_count=sum(1 for _ in (D/'evidence/log-restarts.jsonl').open()),flags=flags,warning_count=len(warning),module_cache_line=cache,validation_files=[dict(name=p.name,bytes=p.stat().st_size) for p in (D/'validation').glob('*') if p.is_file()],rpm_count=len(pkgs),rpm_names=[p['query'].split('\t')[0]+(' [src]' if p['path'].endswith('.src.rpm') else '') for p in pkgs],native_installed_archives=len(native),native_converted_members=sum(x['record']['converted'] for x in native),native_preserved_members=sum(x['record']['preserved'] for x in native),native_debug_members=sum(x['record']['debug_members'] for x in native))
cmd(['df','-B1','/home'],E/'df-final.json')
cmd(['systemctl','--user','show','llvm-night-20261103.service','night-toolchain-full-controller-20261103.service','night-basedev-full-controller-20261103.service','-p','Id','-p','ActiveState','-p','SubState','-p','Result','-p','ExecMainStatus','-p','MemoryPeak'],E/'services-final.json')
cmd(['journalctl','--user','-u','night-basedev-full-controller-20261103.service','--no-pager','-n','30'],E/'basedev-controller-journal.json')
r=subprocess.run(['findmnt','-rn','-o','TARGET,SOURCE,FSTYPE'],text=True,capture_output=True);save(E/'mounts-final.json',dict(argv=['findmnt','-rn','-o','TARGET,SOURCE,FSTYPE'],rc=r.returncode,matches=[l for l in r.stdout.splitlines() if str(N) in l],stderr=r.stderr))
cmd(['git','-C',str(W/'temp/review-20261102/source'),'status','--porcelain','--untracked-files=no'],E/'source-status.json')
cmd(['git','-C',str(W/'temp/review-20261102/source'),'rev-parse','HEAD','HEAD^{tree}'],E/'source-identity.json')
save(E/'summary.json',summary);save(E/'provenance.json',provenance)
print(json.dumps(summary,ensure_ascii=False,indent=2))
