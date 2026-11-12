from pathlib import Path
import json,tarfile,hashlib,subprocess,gzip,collections,datetime
B=Path('/home/linhao/Toolchain/development/llvm-optimize-bolt');W=B.parent/'llvm-optimize';E=Path(__file__).parent;C=W/'temp/rebase-359934-20261111-r6/source'
def sha(p):
 with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
sources={}
for project in ('toolchain','basedev'):
 P=W/'temp/local-full-r6-20261111-compare'/project/'payload/llvm-src'
 sources[project]={}
 for side in ('local','qb'):
  tar=P/side/'llvm-22.1.8.tar.gz';sources[project][side]=dict(sha256=sha(tar),bytes=tar.stat().st_size)
  if project=='toolchain':
   with tarfile.open(tar,'r|gz') as tf:
    for m in tf:
     if m.name.endswith('/clang/bindings/python/.git_archival.txt'):
      sources[project][side]['git_archival_text']=tf.extractfile(m).read().decode()
      break
save(E/'source-container-details.json',sources)
z=json.loads((E/'source-attribution.json').read_text());verify=[]
for x in z['differences']:
 n=x['file']
 if n.startswith('packaging/'):
  r=subprocess.run(['git','-C',str(C),'show','fea0fe464d56e17f2c7588c557bfffd9f6ac352b:'+n],capture_output=True)
  verify.append(dict(file=n,git_rc=r.returncode,sha256=hashlib.sha256(r.stdout).hexdigest(),local_sha256=x['local'].get('sha256'),matches_git=r.returncode==0 and hashlib.sha256(r.stdout).hexdigest()==x['local'].get('sha256')))
save(E/'source-extra-packaging-git-check.json',verify)
print('SOURCE',json.dumps(sources));print('PACKAGING',len(verify),'all_git_equal',all(x['matches_git'] for x in verify))
fun={}
for kind in ('bolt-input','final-clang'):
 rows=json.load(gzip.open(E/'function-comparison'/(kind+'-different-functions.json.gz'),'rt'));c=collections.Counter()
 for r in rows:
  a,b=r['toolchain'],r['basedev']
  if a is None:c['only_basedev']+=1
  elif b is None:c['only_toolchain']+=1
  elif a['instruction_text_sha256']==b['instruction_text_sha256'] and a['instruction_lines']==b['instruction_lines']:c['address_only']+=1
  else:c['instruction_text_or_count']+=1
 fun[kind]=dict(c)
save(E/'function-comparison/categories.json',fun);print('FUNCTIONS',fun)
for project in ('toolchain','basedev'):
 rows=json.loads((E/project/'comparison/packages.json').read_text())
 print('PACKAGES',project,[(x['package'],x['status'],len(x['content_changes'])) for x in rows])
 src=next(x for x in rows if x['package']=='llvm-src');print('SOURCE changes',project,[(x.get('file',x.get('path')),list(x)) for x in src['content_changes']])
 a=json.loads((E/project/'audit.json').read_text());print('rawFlags',project,json.loads((E/project/'log-audit-raw.json').read_text())['flags'])
print('SUPPLEMENT 已结束 '+datetime.datetime.now().astimezone().isoformat()+' status=recorded')
