from pathlib import Path
import json,subprocess
E=Path(__file__).resolve().parent;B=E.parents[3];W=Path('/home/linhao/Toolchain/development/llvm-optimize')
names=list(json.loads((E/'doc-references.json').read_text()))
(E/'path-patterns.txt').write_text('\n'.join(names)+'\n')
scopes=dict(docs=[str(p) for repo in [W,B] for p in (repo/'docs').rglob('*.md') if p.name!='38_temp_cleanup_inventory.md'],scripts=[p for p in json.loads((E/'grep-script-scope.json').read_text())['files'] if str(E) not in p])
commands=[]
for label,files in scopes.items():
 argv=['rg','--no-heading','-n','-F','-f',str(E/'path-patterns.txt'),'--']+files
 r=subprocess.run(argv,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 (E/(label+'-grep.txt')).write_bytes(r.stdout);(E/(label+'-grep.stderr')).write_bytes(r.stderr);commands.append(dict(scope=label,argv=argv,rc=r.returncode))
(E/'grep-commands.json').write_text(json.dumps(commands,indent=2)+'\n')
print([(r['scope'],r['rc']) for r in commands])
