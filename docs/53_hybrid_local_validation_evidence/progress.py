import json,re,subprocess,time
from pathlib import Path
W=Path('/home/linhao/Toolchain/development/llvm-optimize');E=W/'docs/53_hybrid_local_validation_evidence'
state=subprocess.run(['systemctl','--user','show','hybrid-local-20261023.service','-p','ActiveState','-p','SubState','-p','Result'],capture_output=True,text=True).stdout
print(time.strftime('%Y-%m-%d %H:%M:%S %Z'));print(state.strip())
p=E/'rpm-build.log'
if p.exists():
 lines=p.read_text(errors='replace').splitlines();print('log_lines',len(lines));print('\n'.join(x[:300] for x in lines[-3:]));samples=[l for l in lines if re.search(r'\[\d+/\d+\]',l)];print('last_progress',samples[-1][:240] if samples else 'none')
p=E/'resources.jsonl'
if p.exists():
 r=json.loads(p.read_text().splitlines()[-1]);print('free_GiB',round(r['home_available_bytes']/2**30,3));print('memory',r.get('memory.current'),'peak',r.get('memory.peak'),'events',r.get('memory.events'))
p=E/'du-root-complete.jsonl'
if p.exists():
 rows=[json.loads(l) for l in p.read_text().splitlines()];valid=[r for r in rows if r['rc']==0];print('du_samples',len(valid),'/',len(rows));print('last_du',valid[-1]['stdout'].strip() if valid else 'none');print('sampled_peak_GiB',max(int(r['stdout'].split()[0]) for r in valid)/2**30 if valid else None)
p=E/'controller-result.json'
if p.exists():print('FINAL',p.read_text())
