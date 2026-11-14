from pathlib import Path
import os,sys,json,hashlib,importlib.util,subprocess,shlex,time,datetime,threading,traceback,collections,shutil
E=Path(__file__).parent; B=E.parents[4]; W=Path('/home/linhao/Toolchain/development/llvm-optimize');X=W/'temp/weekend99-replay-20261114'
UNIT='weekend99-step5-20261114.service'
# Enforce one 120-minute budget for the entire step, including preparation and first replay.
started=int(subprocess.check_output(['systemctl','--user','show',UNIT,'-p','ActiveEnterTimestampMonotonic','--value'],text=True).strip())/1e6
done=threading.Event();stage='remaining-preflight'
# Reuse exactly the same audited helpers and watchdog, without executing the first driver.
helpers=(E/'replay.py').read_text();exec(compile(helpers[helpers.index('def sha('):helpers.index('thread=threading.Thread')],str(E/'replay.py')+'[helpers]','exec'))
first=json.loads((E/'result.json').read_text());assert first['status']=='PASS',first
thread=threading.Thread(target=guard,daemon=True);thread.start()
result={'status':'STOP','start':now(),'source':first['source'],'converted':1093,'preserved':7,'archives':10,'rows':[],'prior_10_result':'debug-output-comparison.json'}
try:
 new=load('remaining_converter',E/'new-converter.py');new.log_startup_context()
 R=W/'temp/night-20261105/toolchain/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0';BUILD=R/'home/abuild/rpmbuild/BUILD/llvm-22.1.8/build';sources=BUILD/'lib64'
 paths={n:X/'tools'/n for n in ('clang-22','llvm-dis','llvm-nm')};build=X/'build'
 shipping=json.loads((E/'shipping-toolchain-archives.json').read_text());done_names={r['archive'] for r in json.loads((E/'debug-output-comparison.json').read_text())}
 remaining=[r for r in shipping if Path(r['path']).name not in done_names];assert len(remaining)==215
 (X/'remaining').mkdir()
 for index,row in enumerate(remaining):
  name=Path(row['path']).name;stage='remaining-'+name;work=X/'remaining'/f'{index:03d}';work.mkdir();root=work/'input';root.mkdir();inp=root/name;source=sources/name
  before=new.validate_archive(source);assert before['bitcode']+before['machine']==before['member_count'];shutil.copy2(source,inp);assert sha(inp)==before['sha256']
  summary=new.convert(root,work/'new',paths['clang-22'],paths['llvm-dis'],paths['llvm-nm'],build,jobs=2,debug_info='yes');assert summary['status']=='CONVERTED'
  if before['bitcode']:
   assert len(summary['archives'])==1
   converted=summary['archives'][0]['converted'];preserved=summary['archives'][0]['preserved'];candidate=work/'new/archives'/name
  else:
   assert not summary['archives'] and summary['native_archives_skipped']==1
   converted=0;preserved=before['machine'];candidate=inp
  a=new.inspect(candidate);b=new.inspect(row['path'])
  assert a['sha256']==row['sha256']==b['sha256'] and a['bytes']==b['bytes'],(name,'archive-byte-difference',a['sha256'],b['sha256'])
  assert {k:v for k,v in a.items() if k!='path'}=={k:v for k,v in b.items() if k!='path'},(name,'inspect-difference')
  members=[{'ordinal':m['ordinal'],'name':m['name'],'sha256':m['sha256']} for m in a['members']]
  assert members==[{'ordinal':m['ordinal'],'name':m['name'],'sha256':m['sha256']} for m in b['members']]
  record={'archive':name,'input':str(source),'input_sha256':before['sha256'],'reference':row['path'],'output_sha256':a['sha256'],'bytes':a['bytes'],'converted':converted,'preserved':preserved,'members':members,'byte_identical':True,'temporary_candidate':str(candidate),'candidate_deleted_after_sha_record':True}
  result['rows'].append(record);result['converted']+=converted;result['preserved']+=preserved;result['archives']+=1
  dump('remaining-progress.json',result)
  # Only own, newly created temporary files; no historical input/reference is ever removed.
  assert candidate.is_relative_to(X/'remaining') and inp.is_relative_to(X/'remaining')
  candidate.unlink()
  if inp.exists():inp.unlink()
  print('FULL_REPLAY_IDENTICAL',index+1,len(remaining),name,'converted_total',result['converted'],now(),flush=True)
 assert result['archives']==225 and result['converted']==3853 and result['preserved']==11,result
 result['status']='PASS'
except BaseException:
 result['failure']=traceback.format_exc();print(result['failure'],flush=True)
finally:
 done.set();thread.join();result['end']=now();result['total_step_seconds']=time.monotonic()-started;result['memory_peak']=(cg/'memory.peak').read_text().strip();result['memory_events']=(cg/'memory.events').read_text();dump('result-full.json',result)
 print('99步骤5全量 已结束',result['end'],'status='+result['status'],flush=True)
sys.exit(0 if result['status']=='PASS' else 1)
