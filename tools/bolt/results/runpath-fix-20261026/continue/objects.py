from common import *
import time,sys
mode=sys.argv[1];assert mode in ('current','oldtext');V=X/('objects-'+mode);V.mkdir();O=E/('objects-'+mode);O.mkdir()
units=json.loads((W/'docs/53_hybrid_local_validation_evidence/tu-inputs.json').read_text());assert len(units)==90
roles=[('ordinary',WORK/'ordinary-clang-22'),('candidate',WORK/'clang.candidate' if mode=='current' else D/'old-text/clang.candidate')]
slot=V/'clang-22';slot.touch();inode=slot.stat().st_ino;results={};start=time.monotonic()
for role,src in roles:
 shutil.copyfile(src,slot);slot.chmod(0o755);assert sha(src)==sha(slot) and slot.stat().st_ino==inode
 for u in units:
  free();i=u['index'];d=V/f'{i:03d}';d.mkdir(exist_ok=True);inp=d/'input.ii';assert sha(u['copy'])==u['sha256']
  if not inp.exists():shutil.copyfile(u['copy'],inp)
  out=d/'same.o';out.unlink(missing_ok=True);args=list(u['original_argv'][1:]);args.insert(0,'--no-default-config');args[args.index('-c')+1]=str(inp);args[args.index('-o')+1]=str(out);args=[('-resource-dir='+str(BUILD/'lib64/clang/22') if x.startswith('-resource-dir=') else x) for x in args]
  argv=loader(slot)+args;stamp=time.monotonic();p=subprocess.run(argv,capture_output=True,text=True,timeout=600,cwd=V,env={**os.environ,'LC_ALL':'C'})
  (O/f'{role}-{i}.stdout').write_text(p.stdout);(O/f'{role}-{i}.stderr').write_text(p.stderr)
  row={'target':u['target'],'key':u['key'],'sha256':sha(out) if out.is_file() else None,'seconds':time.monotonic()-stamp,'argv':argv,'input_sha256':u['sha256'],'rc':p.returncode}
  save(O/'last.json',row);assert p.returncode==0 and out.is_file(),(role,i,p.stderr)
  if role=='ordinary':shutil.copyfile(out,d/'ordinary.o');results[i]={'ordinary':row}
  else:results[i]['candidate']=row;results[i]['byte_equal']=(d/'ordinary.o').read_bytes()==out.read_bytes();assert results[i]['byte_equal'],i
  save(O/'progress.json',{'role':role,'index':i,'results':results});print('OBJECT',mode,role,i,flush=True)
result={'PASS':all(x['byte_equal'] for x in results.values()),'total':90,'passed':sum(x['byte_equal'] for x in results.values()),'seconds':time.monotonic()-start,'same_path_inode':inode,'roles':[{'role':r,'path':str(p),'sha256':sha(p)} for r,p in roles],'results':results};save(O/'result.json',result);print('OBJECTS_PASS',mode,90,flush=True)
