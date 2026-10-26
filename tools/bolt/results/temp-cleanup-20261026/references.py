from pathlib import Path
import json,subprocess,os
E=Path(__file__).resolve().parent;W=Path('/home/linhao/Toolchain/development/llvm-optimize');B=E.parents[3]
paths=[p for p in (W/'temp').iterdir() if p.is_dir() and not p.is_symlink()]+[p for p in Path('/var/tmp').iterdir() if p.is_dir() and any(x in p.name for x in ['llvm','gbs','hybrid','bolt'])]
argv=['fuser','-v']+list(map(str,paths));r=subprocess.run(argv,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
(E/'fuser-checked.stdout').write_bytes(r.stdout);(E/'fuser-checked.stderr').write_bytes(r.stderr);(E/'fuser-checked.json').write_text(json.dumps(dict(argv=argv,rc=r.returncode),indent=2)+'\n')
# Limit grep to analysis scripts; never recursively grep source/build/system trees.
scripts=set()
for repo in [W,B]:
 for root in [repo/'docs',repo/'tools']:
  for ext in ['*.py','*.sh']:
   scripts.update(str(p) for p in root.rglob(ext) if p.is_file())
if (E/'scripts.json').exists():scripts.update(json.loads((E/'scripts.json').read_text()))
refs={p.name:[] for p in paths}
for raw in sorted(scripts):
 p=Path(raw)
 if E in p.parents:continue
 try:lines=p.read_text(errors='replace').splitlines()
 except OSError:continue
 for i,line in enumerate(lines,1):
  for name in refs:
   if name in line:refs[name].append(dict(file=raw,line=i,text=line))
(E/'script-references.json').write_text(json.dumps(refs,ensure_ascii=False,indent=2)+'\n')
(E/'grep-script-scope.json').write_text(json.dumps(dict(files=sorted(scripts),method='literal top-level directory-name search, analysis scripts outside build roots only'),indent=2)+'\n')
print('fuser',r.returncode,'script files',len(scripts),'references',sum(map(len,refs.values())))
