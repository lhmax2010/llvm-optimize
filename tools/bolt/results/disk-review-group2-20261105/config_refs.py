from pathlib import Path
import subprocess,json,gzip
E=Path(__file__).resolve().parent;W=Path('/home/linhao/Toolchain/development/llvm-optimize');B=E.parents[3];N=json.loads((E/'targets.json').read_text());records=[]
for label,root in [('main-config',W/'tools'),('bolt-config',B/'tools')]:
 a=['timeout','120','nice','-n','19','ionice','-c3','rg','--hidden','--no-ignore','-n','--no-heading','-F']
 for n in N:a+=['-e',n]
 a+=['-g','*.json','-g','*.cjs','-g','*.js','-g','*.mjs','-g','*.pl','-g','*.bash','-g','!**/results/**','-g','!**/node_modules/**',str(root)]
 r=subprocess.run(a,capture_output=True,text=True);records.append({'label':label,'argv':a,'rc':r.returncode,'stderr':r.stderr})
 for n in N:
  lines=[l for l in r.stdout.splitlines() if n in l]
  with gzip.open(E/n/(label+'-references.txt.gz'),'wt') as f:f.write('\n'.join(lines)+'\n')
(E/'config-search.json').write_text(json.dumps(records,indent=2))
