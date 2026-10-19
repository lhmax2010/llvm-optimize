from pathlib import Path
import subprocess,json,re
E=Path(__file__).parent;spec=E/'export/llvm.spec';rollback=E/'host-rollback.spec';rollback.write_text(spec.read_text().replace('%bcond_without clang_bolt','%bcond_with clang_bolt',1));results=[]
for label,target,extra,path in [('x86-on','x86_64-tizen-linux',[],spec),('x86-without','x86_64-tizen-linux',['--define','_without_clang_bolt 1'],spec),('x86-rollback','x86_64-tizen-linux',[],rollback),('armv7l','armv7l-tizen-linux',[],spec),('aarch64','aarch64-tizen-linux',[],spec)]:
 a=['rpmspec','-P','--target',target,'--define','_toolchain clang','--define','_sourcedir '+str(E/'export')]+extra+[str(path)]
 p=subprocess.run(a,capture_output=True,text=True);(E/('host-final-'+label+'.stdout')).write_text(p.stdout);(E/('host-final-'+label+'.stderr')).write_text(p.stderr)
 lines=[l for l in p.stdout.splitlines() if re.match('^(Source|Patch)[0-9]*:',l)]
 results.append({'label':label,'argv':a,'rc':p.returncode,'sources_patches':lines,'PASS':p.returncode==0 and len([l for l in lines if l.startswith('Patch')])==7})
ver=subprocess.check_output(['rpm','--version'],text=True);(E/'host-final-matrix.json').write_text(json.dumps({'host_version':ver.strip(),'supplemental_only':True,'NOT_TIZEN_CERTIFICATION':True,'matrix':results},indent=2)+'\n');assert all(r['PASS'] for r in results);print(ver.strip(),': supplemental host matrix 5 PASS; mandatory Tizen NOT RUN')
