from pathlib import Path
import json,shutil,subprocess,hashlib,shlex,os,sys,datetime,traceback
B=Path('/home/linhao/Toolchain/development/llvm-optimize-bolt');W=B.parent/'llvm-optimize';E=B/'tools/bolt/results/afternoon-20261105/item1';F=W/'temp/ompd-relink-20261105';F.mkdir(exist_ok=False)
R=W/'temp/night-20261103/toolchain/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0';build=R/'home/abuild/rpmbuild/BUILD/llvm-22.1.8/build'
sys.path.insert(0,str(B/'tools/bolt/overnight-20261105'));from section_compare import file_proof
sys.path.insert(0,str(B/'tools/bolt/night-launch-20261103'));from rpm_extract import extract_selected
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(n,v):(E/n).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
status='failed';reason='unfinished'
try:
 lines=(build/'build.ninja').read_text().splitlines();idx=next(i for i,l in enumerate(lines) if ': C_MODULE_LIBRARY_LINKER__ompdModule' in l);block=[]
 for l in lines[idx:]:
  if not l:break
  block.append(l)
 (E/'build-ninja.txt').write_text(f'{build}/build.ninja:L{idx+1}\n'+'\n'.join(block)+'\n')
 rule='C_MODULE_LIBRARY_LINKER__ompdModule_Release';out,tail=block[0][6:].split(': '+rule+' ',1);objs=tail.split('|')[0].split();vals=dict(l.strip().split(' = ',1) for l in block[1:] if ' = ' in l)
 rules=(build/'CMakeFiles/rules.ninja').read_text().splitlines();ri=next(i for i,l in enumerate(rules) if l=='rule '+rule);(E/'rules-ninja.txt').write_text('\n'.join(rules[ri:ri+6])+'\n')
 original=next(l.strip()[10:] for l in rules[ri:ri+6] if l.strip().startswith('command = '));save('original-command.json',{'template':original,'variables':vals,'objects':objs,'output':out})
 ident=[]
 for mode in ('new','old'):
  cwd=F/mode;cwd.mkdir();(cwd/'wrappers').mkdir()
  for obj in objs:
   dst=cwd/obj;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(build/obj,dst);ident.append({'source':str(build/obj),'copy':str(dst),'bytes':dst.stat().st_size,'sha256':sha(dst)})
  (cwd/out).parent.mkdir(parents=True,exist_ok=True)
  ld=cwd/'wrappers/ld.lld';ld.write_text('#!/bin/sh\nexec '+shlex.quote(str(R/'lib64/ld-linux-x86-64.so.2'))+' --library-path '+shlex.quote(str(R/'usr/lib64')+':'+str(R/'lib64'))+' '+shlex.quote(str(R/'usr/bin/ld.lld'))+' "$@"\n');ld.chmod(0o755)
  flags=shlex.split(vals['LINK_FLAGS']);flags=[x for x in flags if mode!='old' or x!='-Wl,--gc-sections']
  libs=[str(R/x.lstrip('/')) if x.startswith('/') else x for x in shlex.split(vals['LINK_LIBRARIES'])]
  argv=[str(R/'lib64/ld-linux-x86-64.so.2'),'--library-path',str(R/'usr/lib64')+':'+str(R/'lib64'),str(R/'usr/bin/clang'),'-fPIC',*shlex.split(vals['LANGUAGE_COMPILE_FLAGS']),*flags,'--sysroot='+str(R),'--ld-path='+str(ld),'-shared','-o',out,*objs,*libs]
  save(mode+'-argv.json',argv)
  for kind,extra in [('dryrun',['-###']),('link',[])]:
   p=subprocess.run(argv+extra,cwd=cwd,capture_output=True,text=True);(E/(mode+'-'+kind+'.stdout')).write_text(p.stdout);(E/(mode+'-'+kind+'.stderr')).write_text(p.stderr);assert p.returncode==0,(mode,kind,p.stderr)
  save(mode+'-result.json',{'path':str(cwd/out),'sha256':sha(cwd/out),'bytes':(cwd/out).stat().st_size})
 save('inputs.json',ident)
 # Compare the unprocessed link to its build output first. Packaged ELF has platform stripping/debuglink.
 comparisons=[]
 for mode,other in [('new',build/out),('old',W/'temp/debuglink-20261028/full-20261030/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0'/out)]:
  if mode=='old':other=W/'temp/debuglink-20261028/full-20261030/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build'/out
  p=F/mode/out;row={'mode':mode,'other':str(other),'new_sha':sha(p),'other_sha':sha(other),'bytes_identical':sha(p)==sha(other)}
  try:row['proof']=file_proof(other,p)
  except Exception as e:row['error']=str(e)
  comparisons.append(row)
 save('unstripped-comparison.json',comparisons)
 status='ok';reason='two-links-complete-packaging-comparison-next'
except BaseException as ex:reason=repr(ex);traceback.print_exc()
finally:
 save('result.json',{'status':status,'reason':reason});line='ITEM1_LINK 已结束 '+datetime.datetime.now().astimezone().isoformat()+' status='+status+' reason='+reason;(E/'link-end.txt').write_text(line+'\n');print(line,flush=True)
sys.exit(0 if status=='ok' else 1)
