from pathlib import Path
import json,hashlib,subprocess,shutil,time,sys
D=Path(__file__).resolve().parent;W=D.parent.parent;E=W.parent/'llvm-optimize-bolt/tools/bolt/results/runpath-fix-20261026';R=D/'gbs-root/local/BUILD-ROOTS/scratch.x86_64.0';BUILD=R/'home/abuild/rpmbuild/BUILD/llvm-22.1.8/build';WORK=BUILD/'clang-bolt'
mode=sys.argv[1];assert mode in ('current','oldtext');V=R/('home/abuild/runpath-objects-'+mode);V.mkdir(exist_ok=True);O=E/('objects-'+mode);O.mkdir(exist_ok=True)
assert json.loads((E/'build-result.json').read_text())['exit_code']==0
units=json.loads((W/'docs/53_hybrid_local_validation_evidence/tu-inputs.json').read_text());assert len(units)==90
roles=[('ordinary',WORK/'ordinary-clang-22'),('candidate',WORK/'clang.candidate' if mode=='current' else R/'home/abuild/runpath-oldtext/clang.candidate')]
slot=V/'clang-22';slot.touch();inode=slot.stat().st_ino;results={};start=time.monotonic()
def sha(p):
 with Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
for role,src in roles:
 shutil.copyfile(src,slot);slot.chmod(0o755);assert sha(src)==sha(slot) and slot.stat().st_ino==inode
 for u in units:
  i=u['index'];d=V/f'{i:03d}';d.mkdir(exist_ok=True);inp=d/'input.ii';assert sha(u['copy'])==u['sha256']
  if not inp.exists():shutil.copyfile(u['copy'],inp)
  out=d/'same.o';out.unlink(missing_ok=True);args=list(u['original_argv']);args[0]='/'+str(slot.relative_to(R));args.insert(1,'--no-default-config');args[args.index('-c')+1]='/'+str(inp.relative_to(R));args[args.index('-o')+1]='/'+str(out.relative_to(R));args=[('-resource-dir=/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/lib64/clang/22' if x.startswith('-resource-dir=') else x) for x in args]
  stamp=time.monotonic();p=subprocess.run(['sudo','-n','/usr/sbin/chroot',str(R),*args],capture_output=True,text=True,timeout=600)
  (O/f'{role}-{i}.stdout').write_text(p.stdout);(O/f'{role}-{i}.stderr').write_text(p.stderr);assert p.returncode==0 and out.is_file(),(role,i,p.stderr)
  row={'target':u['target'],'key':u['key'],'sha256':sha(out),'bytes':out.stat().st_size,'seconds':time.monotonic()-stamp,'argv':args,'input_sha256':u['sha256'],'rc':p.returncode}
  if role=='ordinary':shutil.copyfile(out,d/'ordinary.o');results[i]={'ordinary':row}
  else:
   results[i]['candidate']=row;results[i]['byte_equal']=(d/'ordinary.o').read_bytes()==out.read_bytes()
   assert results[i]['byte_equal'],i
  (O/'progress.json').write_text(json.dumps({'role':role,'index':i,'results':results},indent=2));print('OBJECT',mode,role,i,flush=True)
result={'PASS':all(x['byte_equal'] for x in results.values()),'total':90,'passed':sum(x['byte_equal'] for x in results.values()),'seconds':time.monotonic()-start,'same_path_inode':inode,'roles':[{ 'role':r,'path':str(p),'sha256':sha(p)} for r,p in roles],'results':results};(O/'result.json').write_text(json.dumps(result,indent=2));print('OBJECTS_PASS',mode,90,flush=True)
