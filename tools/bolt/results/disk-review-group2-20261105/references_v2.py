import subprocess,json,gzip
from pathlib import Path
E=Path(__file__).resolve().parent;W=Path('/home/linhao/Toolchain/development/llvm-optimize');B=E.parents[3];N=json.loads((E/'targets.json').read_text())
for label,root,globs in [('main-docs',W/'docs',['*.md']),('bolt-docs',B/'docs',['*.md']),('main-scripts',W/'tools',['*.py','*.sh','*.conf']),('bolt-scripts',B/'tools',['*.py','*.sh','*.conf'])]:
 argv=['timeout','180','nice','-n','19','ionice','-c3','rg','-n','--no-heading','-F']
 for n in N:argv+=['-e',n]
 for g in globs:argv+=['-g',g]
 argv+=['-g','!**/disk-review-group2-20261105/**',str(root)]
 r=subprocess.run(argv,capture_output=True,text=True)
 for n in N:
  lines=[s for s in r.stdout.splitlines() if n in s]
  with gzip.open(E/n/(label+'-references-v2.txt.gz'),'wt') as f:f.write('\n'.join(lines)+'\n')
 (E/(label+'-search.json')).write_text(json.dumps({'argv':argv,'rc':r.returncode,'stderr':r.stderr,'matches':len(r.stdout.splitlines())},indent=2))
 print(label,r.returncode,len(r.stdout.splitlines()),flush=True)
