from pathlib import Path
import subprocess,json,shutil,os
D=Path(__file__).resolve().parent;S=D/'source';E=D.parent.parent.parent/'llvm-optimize-bolt/tools/bolt/results/runpath-fix-20261026'
msg=subprocess.check_output(['git','-C',str(S),'log','-1','--format=%B'],text=True).replace('certify the dry-run and serial llvm-bolt build,','certify the dry-run and parallel llvm-bolt build,').replace('performance outside LLVM workloads. ninja -j1 does not cap linker\nmemory.', 'performance outside LLVM workloads. The Ninja job limit does not cap\nlinker memory.')
(D/'commit-message.txt').write_text(msg)
subprocess.run(['git','-C',str(S),'-c','user.name=Hao Lin','-c','user.email=hao.lin@samsung.com','commit','--amend','-F',str(D/'commit-message.txt')],check=True)
plan=json.loads((D/'plan.json').read_text());plan['commit']=subprocess.check_output(['git','-C',str(S),'rev-parse','HEAD'],text=True).strip();(D/'plan.json').write_text(json.dumps(plan,indent=2));(E/'preflight.json').write_text(json.dumps(plan,indent=2))
(D/'export').rename(D/'export-initial');(D/'export').mkdir()
for f in (D/'export-initial').glob('*.tar.*'):shutil.copyfile(f,D/'export'/f.name)
old=json.loads((E/'export-result.json').read_text());argv=old['argv'];argv[argv.index('--commit')+1]=plan['commit']
for name in ('export.stdout','export.stderr','export-result.json'):(E/name).rename(E/('initial-'+name))
with (E/'export.stdout').open('wb') as o,(E/'export.stderr').open('wb') as e:p=subprocess.run(argv,stdout=o,stderr=e,env={**os.environ,'TMPDIR':str(D/'tmp')})
(E/'export-result.json').write_text(json.dumps({'argv':argv,'rc':p.returncode},indent=2));assert p.returncode==0
shutil.copyfile(D/'export/llvm.spec',E/'exported.spec');print('FINAL_EXPORT_PASS',plan['commit'])
