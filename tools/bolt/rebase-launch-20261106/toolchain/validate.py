"""Same-commit/same-snapshot QB baseline; bounded original GBS log reader."""
from pathlib import Path
import argparse,json,re,subprocess,traceback,datetime,hashlib
from validation_common import packages,rootpaths,save,sha,objects
from log_support import canonical_log,log_summary
from rpm_extract import extract_selected
from compare_rules import link_info,crc_file
T=Path(__file__).resolve().parent

def flags(lines):
 return [re.sub(r'^\[\s*\d+s\]\s?','',s) for s in lines if re.sub(r'^\[\s*\d+s\]\s?','',s).startswith(('TIZEN_LLVM_NORMALIZED_FLAGS ','TIZEN_LLVM_DROPPED_FLAGS ','TIZEN_LLVM_FLAGS_WARNING '))]

def main(a):
 D=a.root;O=D/'validation';O.mkdir(exist_ok=False);result={'status':'failed','checks':{}};q=json.loads((T/'qb-reference.json').read_text());R,BUILD,WORK=rootpaths(D)
 def check(name,fn):
  try:fn();result['checks'][name]='PASS';print('CHECK_PASS',name,flush=True)
  except MemoryError:raise
  except Exception:
   result['checks'][name]='FAIL'
   with (O/'failure.txt').open('a') as f:f.write(name+'\n'+traceback.format_exc())
   print('CHECK_FAIL',name,traceback.format_exc(),flush=True)
  finally:save(O/'result.json',result)
 try:
  log=log_summary(canonical_log(D));save(O/'log-input.json',{k:v for k,v in log.items() if k!='selected'});lines=list(log['selected'].values());identity=json.loads((WORK/'identity.json').read_text());save(O/'identity.json',identity)
  def f():
   actual=flags(lines);expected=[x['text'] for x in q['flags']];save(O/'flags.json',dict(actual=actual,expected=expected));assert actual==expected
  check('QB-flags-exact',f)
  def ident():
   rows=[dict(stage=k,actual=identity[k],expected=q['identity'][k]) for k in ['strip_all_sha256','rpath_adjusted_sha256','after_sha256']];save(O/'three-stage-sha.json',rows);assert sha(WORK/'clang.candidate')==identity['after_sha256'];assert all(x['actual']==x['expected'] for x in rows),rows
  check('QB-three-stage-sha-exact',ident)
  def profile():
   pipe=json.loads((WORK/'pipeline-result.json').read_text());save(O/'pipeline.json',pipe);assert pipe['counts']==q['counts']
  check('QB-profile-counts',profile)
  def anchors():
   needed=['BOLT_NINJA_EXIT_0','BOLT_PIPELINE_PASS','BOLT_DEBUG_SYMBOLS_PASS','BOLT_DEBUGLINK_PASS','BOLT_COMPARE_ROOT_PASS','BOLT_CACHE_RELEASE','BOLT_POST_GATE_PASS','NATIVE_ARCHIVES_END','TIZEN_HYBRID_LINK_OK'];rows={k:[s for s in lines if k in s and '+ echo ' not in s and '+ printf ' not in s] for k in needed+['BOLT_REAL_GATE_PASS']};save(O/'anchors.json',rows);assert all(rows[k] for k in needed);assert len(rows['BOLT_REAL_GATE_PASS'])>=3
  check('anchors',anchors)
  def debuglink():
   d=WORK/'clang-22.debug';x=link_info((WORK/'clang.candidate').read_bytes());assert x['filename']=='clang-22.debug' and x['crc32']==crc_file(d);assert sha(d)==identity['debug_file']['sha256'];save(O/'debuglink.json',{k:v for k,v in x.items() if k!='prefix'});ls=list(BUILD.parent.glob('**/debugfiles.list'));assert any('clang-22.debug' in p.read_text() for p in ls)
  check('debuglink-and-debugfiles',debuglink)
  new=packages(D);old={}
  for p in Path(q['rpm_directory']).rglob('*.rpm'):
   m=subprocess.check_output(['rpm','-qp','--qf','%{NAME}\t%{VERSION}\t%{RELEASE}\t%{ARCH}\t%{VCS}',str(p)],text=True);v=m.split('\t');key=v[0]+'\t'+('src' if p.name.endswith('.src.rpm') else v[3]);assert key not in old;old[key]=(p,m);assert q['commit'] in m
  assert len(old)==len(new)==23 and set(old)==set(new)
  rows=[dict(project='toolchain',path=str(old[k][0]),metadata=old[k][1],local_rpm=str(new[k])) for k in sorted(old)];save(O/'rpm-downloads.json',rows)
  def pkgs():
   with (O/'rpm-comparison.stdout').open('w') as out,(O/'rpm-comparison.stderr').open('w') as err:subprocess.run(['python3','-B',str(T/'compare_packages.py'),str(O),str(D)],stdout=out,stderr=err,check=True)
   r=json.loads((O/'item2-result.json').read_text());assert r['status']=='ok',r
  check('QB-23-packages',pkgs)
  # Preserve the existing 90-TU check, now using the QB compiler as reference.
  dest=O/'qb-clang';extract_selected(old['clang\tx86_64'][0],{'usr/bin/clang-22'},dest)
  check('QB-objects90',lambda:objects(D,O,dest/'usr/bin/clang-22'))
  result['status']='ok' if all(v=='PASS' for v in result['checks'].values()) else 'failed'
 except MemoryError:
  result.update(status='stopped',reason='memory-stop');(O/'failure.txt').write_text(traceback.format_exc())
 except Exception:
  result['error']=traceback.format_exc();(O/'failure-infrastructure.txt').write_text(result['error']);traceback.print_exc()
 finally:
  save(O/'result.json',result);print('VALIDATION 已结束',datetime.datetime.now().astimezone().isoformat(),'status='+result['status'],flush=True)
 return 0 if result['status']=='ok' else 1
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--project',choices=['toolchain'],required=True);p.add_argument('--peer');raise SystemExit(main(p.parse_args()))
