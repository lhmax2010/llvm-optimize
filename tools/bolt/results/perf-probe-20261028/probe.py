from pathlib import Path
import os,json,subprocess,time,hashlib,shutil,re,traceback
W=Path('/home/linhao/Toolchain/development/llvm-optimize');B=W.parent/'llvm-optimize-bolt';D=Path(__file__).resolve().parent;E=B/'tools/bolt/results/perf-probe-20261028';E.mkdir(parents=True,exist_ok=True)
ROOT=W/'temp/oldtext-final-20261027/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0';BUILD=ROOT/'home/abuild/rpmbuild/BUILD/llvm-22.1.8/build';loader=[str(ROOT/'lib64/ld-linux-x86-64.so.2'),'--library-path',str(ROOT/'lib64')+':'+str(ROOT/'usr/lib64')]
def save(n,x):(E/n).write_text(json.dumps(x,indent=2)+'\n')
def run(n,argv,timeout=60):
 start=time.time();r=subprocess.run(list(map(str,argv)),cwd=D,capture_output=True,timeout=timeout,env={**os.environ,'LC_ALL':'C'})
 (E/(n+'.stdout')).write_bytes(r.stdout);(E/(n+'.stderr')).write_bytes(r.stderr);x={'argv':list(map(str,argv)),'rc':r.returncode,'start':start,'end':time.time(),'loadavg':Path('/proc/loadavg').read_text()};save(n+'.json',x);return r
def snapshot():
 rows={}
 for p in Path('/proc').iterdir():
  if p.name.isdigit():
   try:
    text=(p/'stat').read_text();tail=text[text.rfind(')')+2:].split();rows[p.name]={'cpu_ticks':int(tail[11])+int(tail[12]),'comm':text[text.find('(')+1:text.rfind(')')],'start_ticks':tail[19]}
   except (OSError,ValueError,IndexError):pass
 return rows
try:
 run('lscpu',['lscpu']);run('uname',['uname','-a']);run('dmesg',['dmesg']);run('processes',['ps','-eo','pid,ppid,pcpu,pmem,comm','--sort=-pcpu'])
 hardware={'perf_event_paranoid':Path('/proc/sys/kernel/perf_event_paranoid').read_text().strip(),'kptr_restrict':Path('/proc/sys/kernel/kptr_restrict').read_text().strip(),'sysfs':{}}
 for group in ['cpu_core','cpu_atom','cpu']:
  base=Path('/sys/bus/event_source/devices')/group
  for p in [base/'type',base/'cpus',*sorted((base/'caps').glob('*')),*sorted((base/'format').glob('*'))]:
   try:hardware['sysfs'][str(p)]=p.read_text().strip()
   except OSError as ex:hardware['sysfs'][str(p)]={'unreadable':str(ex)}
 save('hardware.json',hardware)
 start=time.monotonic();a=snapshot();time.sleep(3);b=snapshot();elapsed=time.monotonic()-start;hz=os.sysconf('SC_CLK_TCK');busy=[]
 for pid,y in b.items():
  if pid in a and a[pid]['start_ticks']==y['start_ticks']:
   cores=(y['cpu_ticks']-a[pid]['cpu_ticks'])/hz/elapsed
   if cores>.1:busy.append({'pid':pid,'comm':y['comm'],'cores':cores})
 save('load.json',{'seconds':elapsed,'loadavg':Path('/proc/loadavg').read_text(),'active_above_0_1_core':sorted(busy,key=lambda x:-x['cores']),'heavy_threshold_cores':.5,'heavy':[x for x in busy if x['cores']>=.5],'scope':'three-second read-only sample; ps cumulative PCpu is not instantaneous CPU load'})
 host=shutil.which('perf');run('host-perf-version',[host,'--version']);candidates=sorted(Path('/usr/lib').glob('**/perf'));candidates=[p for p in candidates if p.is_file() and os.access(p,os.X_OK)]
 perf=next((p for p in candidates if 'linux-hwe' in str(p)),Path(host));save('perf-selection.json',{'host':host,'existing_candidates':list(map(str,candidates)),'selected':str(perf),'note':'Existing binary used read-only because /usr/bin/perf wrapper lacks current-kernel package; no install and no kernel setting change. Userspace/kernel version mismatch recorded.'})
 run('perf-version',[perf,'--version']);lst=run('perf-list',[perf,'list']);(E/'perf-list-branch-excerpts.txt').write_text('\n'.join(l for l in lst.stdout.decode(errors='replace').splitlines() if re.search('branch|lbr|brs',l,re.I))+'\n')
 old=B/'tools/bolt/results/perf-c-o2-os-20261025';u=next(x for x in json.loads((old/'cases.json').read_text()) if x['language']=='C++' and x['option']=='-O2' and x['target']=='x86_64-tizen-linux-gnu')
 with Path(u['input']).open('rb') as f:assert hashlib.file_digest(f,'sha256').hexdigest()==u['input_sha256']
 args=[('-resource-dir='+str(BUILD/'lib64/clang/22') if x.startswith('-resource-dir=') else '--sysroot='+str(ROOT) if x.startswith('--sysroot=') else x) for x in u['argv']];args[args.index('-o')+1]=str(D/'single.o');command=['/usr/bin/taskset','-c','2','/usr/bin/setarch','x86_64','-R',*loader,str(BUILD/'clang-bolt/ordinary-clang-22'),*args];save('compile-input.json',{'case':u,'actual_compile_argv':command})
 br=run('record-branches',['/usr/bin/taskset','-c','2',perf,'record','-e','cycles:u','-b','-o',D/'branches.data','--',*command],timeout=180)
 branch_lines=[]
 if br.returncode==0:
  script=run('script-branches',[perf,'script','-i',D/'branches.data','-F','ip,brstack']);branch_lines=script.stdout.decode(errors='replace').splitlines();(E/'script-first20.txt').write_text('\n'.join(branch_lines[:20])+'\n');run('record-header',[perf,'report','-i',D/'branches.data','--stdio','--header-only'])
 else:run('record-cycles',['/usr/bin/taskset','-c','2',perf,'record','-e','cycles:u','-o',D/'cycles.data','--',*command],timeout=180)
 tools={}
 for name in ['llvm-profgen','perf2bolt','llvm-bolt','llvm-profdata']:
  p=BUILD/'bin'/name;tools[name]={'path':str(p),'exists':p.exists(),'symlink':os.readlink(p) if p.is_symlink() else None}
  if p.exists():tools[name]['version_rc']=run(name+'-version',[*loader,p,'--version']).returncode
 save('llvm-tools.json',tools)
 for name in ['llvm-profgen','llvm-bolt']:
  if tools[name]['exists']:run(name+'-help',[*loader,BUILD/'bin'/name,'--help'])
 has_stack=any('/' in line for line in branch_lines)
 conversion={'status':'NOT RUN','reason':'no successful branch-stack perf.data','branch_samples':len(branch_lines),'has_branch_stack':has_stack,'record_branches_rc':br.returncode}
 if br.returncode==0 and has_stack and tools['llvm-profgen']['exists']:
  x=run('profgen-convert',[*loader,BUILD/'bin/llvm-profgen','--perfdata='+str(D/'branches.data'),'--binary='+str(BUILD/'clang-bolt/ordinary-clang-22'),'--output='+str(D/'ordinary.afdo')],timeout=180);conversion.update(status='PASS' if x.returncode==0 else 'FAILED',rc=x.returncode,bytes=(D/'ordinary.afdo').stat().st_size if (D/'ordinary.afdo').exists() else None)
 save('conversion.json',conversion);run('processes-after',['ps','-eo','pid,ppid,pcpu,pmem,comm','--sort=-pcpu']);save('result.json',{'probe_completed':True,'sampling':'completed' if br.returncode==0 else 'unavailable','conversion':conversion,'final_load':Path('/proc/loadavg').read_text()})
except Exception:save('failure.json',{'error':traceback.format_exc()})
print((E/'result.json').read_text() if (E/'result.json').exists() else (E/'failure.json').read_text())
