from pathlib import Path
import json,subprocess,hashlib,gzip,shutil,os,datetime,collections,shlex
B=Path('/home/linhao/Toolchain/development/llvm-optimize-bolt');W=B.parent/'llvm-optimize';E=Path(__file__).parent;C=W/'temp/rebase-359934-20261111-r6/source'
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def run(argv):
 p=subprocess.run(argv,capture_output=True,text=True);return dict(argv=argv,rc=p.returncode,stdout=p.stdout,stderr=p.stderr)
def sha(p):
 with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
source={k:run(['git','-C',str(C)]+argv) for k,argv in {'head':['rev-parse','HEAD'],'tree':['rev-parse','HEAD^{tree}'],'status':['status','--porcelain']}.items()}
assert source['head']['stdout'].strip()=='fea0fe464d56e17f2c7588c557bfffd9f6ac352b' and source['tree']['stdout'].strip()=='b2e8af2477cf623a945aa80bf8288a262dd4a5a9' and not source['status']['stdout']
save(E/'source-final.json',source)
s=run(['systemctl','--user','list-units','--all','--no-pager','--plain','rebase359934r6-*'])
save(E/'services-final.json',s)
d=run(['df','-B1','/home']);(E/'df-final.txt').write_text(d['stdout']+d['stderr'])
save(E/'disk-final.json',dict(time=datetime.datetime.now().astimezone().isoformat(),free_bytes=shutil.disk_usage('/home').free))
supp={}
for project in ('toolchain','basedev'):
 R=W/'temp/rebase-359934-20261111-r6'/project
 a=json.loads((E/project/'audit.json').read_text())
 q=R/'evidence/du-root.jsonl'
 bad=[]
 if q.exists():
  for l in q.open():
   z=json.loads(l)
   if z.get('rc'):bad.append(z)
 save(E/project/'du-nonzero-samples.json',bad)
 v=R/'validation/result.json';save(E/project/'entry-validation-result.json',json.loads(v.read_text()))
 raw=json.loads((E/project/'log-audit-raw.json').read_text())
 with (E/project/'required-log-excerpts.txt').open('w') as f:
  for field in ('flags','anchors','tools','native','post_gate','disk_reports'):
   f.write('\n['+field+']\n')
   for row in raw[field]:
    f.write('L'+str(row['line'])+': '+row['text']+'\n')
 flags={k:shlex.split(v['payload'].split('=',1)[1])[0].split() for k,v in a['final_flags'].items()}
 supp[project]=flags
save(E/'final-flags-tokens.json',supp)
diff={}
for name in ('CFLAGS','CXXFLAGS','LDFLAGS'):
 a,b=supp['toolchain'][name],supp['basedev'][name];ca,cb=collections.Counter(a),collections.Counter(b)
 diff[name]=dict(toolchain_only=list((ca-cb).elements()),basedev_only=list((cb-ca).elements()),same_after_removing_debug=[x for x in a if x not in ('-g2','-gdwarf-4','-g')]==b)
save(E/'final-flags-diff.json',diff)
# Preserve full disassembly locally; publish all function names/digests and a hash index.
pub=[];local=[]
for p in sorted(E.rglob('*')):
 if not p.is_file():continue
 rel=str(p.relative_to(E))
 if p.stat().st_size>100*1024*1024:
  local.append(dict(path=str(p),bytes=p.stat().st_size,sha256=sha(p),reason='full disassembly retained locally; per-function names/digests/differences published'))
 elif p.stat().st_size>1024*1024 and p.suffix not in ('.gz','.xz'):
  out=Path(str(p)+'.gz')
  if not out.exists():
   with p.open('rb') as fi,gzip.open(out,'wb',compresslevel=9) as fo:shutil.copyfileobj(fi,fo)
  pub.append(dict(original=rel,published=str(out.relative_to(E)),sha256=sha(p),gzip_sha256=sha(out)))
save(E/'large-local-artifacts.json',local);save(E/'compressed-publication.json',pub)
print('FLAGS_DIFF',json.dumps(diff));print('DF',d['stdout']);print('local-only-artifacts',len(local))
print('EVIDENCE 已结束 '+datetime.datetime.now().astimezone().isoformat()+' status=recorded')
