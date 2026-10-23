from pathlib import Path
import json,re,subprocess,datetime
E=Path('/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/bolt-on-hybrid-20261024')
print(datetime.datetime.now().astimezone().isoformat())
print(subprocess.run(['systemctl','--user','show','bolt-on-hybrid-20261024.service','-p','ActiveState','-p','Result'],capture_output=True,text=True).stdout.strip())
p=E/'rpm-build.log'
if p.exists():
 lines=p.read_text(errors='replace').splitlines();print('LINES',len(lines));hits=[l for l in lines if re.search(r'\[\d+/\d+\]',l)];print('LAST_PROGRESS',hits[-1][:240] if hits else 'none')
p=E/'resources.jsonl'
if p.exists():
 with p.open('rb') as f:
  f.seek(max(0,p.stat().st_size-20000));r=json.loads(f.read().splitlines()[-1])
 print('FREE_GiB',round(r['home_available_bytes']/2**30,3),'MEM',r.get('memory.current','').strip(),'EVENTS',r.get('memory.events','').replace('\n',';'))
p=E/'du-root.jsonl'
if p.exists():
 rows=[json.loads(l) for l in p.read_text().splitlines()];good=[r for r in rows if r.get('rc')==0 and r['stdout'].split() and r['stdout'].split()[0].isdigit()];print('DU',len(good),'/',len(rows),'PEAK_GiB',round(max(int(r['stdout'].split()[0]) for r in good)/2**30,3) if good else None)
for n in ['gate-stop.json','disk-stop.json','build-result.json','controller-result.json']:
 if (E/n).exists():print(n,(E/n).read_text()[:2000])

work=Path('/home/linhao/Toolchain/development/llvm-optimize/temp/bolt-on-hybrid-20261024/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/clang-bolt')
for name in ['tool-plan.json','tool-build.txt','reference-relocs.log','rewrite/bolt.log','pipeline-result.json','cache-release.json']:
 p=work/name
 if p.exists():
  print('BOLT_FILE',name,'bytes',p.stat().st_size)
  if name=='tool-build.txt':
   with p.open('rb') as f:
    f.seek(max(0,p.stat().st_size-4096));tail=f.read().decode(errors='replace').splitlines()
   print('BOLT_BUILD_LAST',tail[-1][:200] if tail else '')
try:
 p=Path('/home/linhao/Toolchain/development/llvm-optimize/temp/bolt-on-hybrid-20261024/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/native-archive-conversion/summary.json')
 x=json.loads(p.read_text());print('NATIVE_ARCHIVES',len(x.get('archives',[])),x.get('status'),'installed',sum(bool(a.get('installed')) for a in x.get('archives',[])))
except (OSError,ValueError):pass
