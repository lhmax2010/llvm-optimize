from pathlib import Path
import sys,json,hashlib,gzip,subprocess,re,collections,datetime,traceback,resource
B=Path('/home/linhao/Toolchain/development/llvm-optimize-bolt');W=B.parent/'llvm-optimize';E=Path(__file__).resolve().parent;O=E/'function-comparison';O.mkdir(exist_ok=False)
sys.path.insert(0,str(B/'tools/bolt/night-launch-20261105'))
from rpm_extract import extract_selected
def save(p,x):p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def sha(p):
 with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def disassemble(project,kind,path):
 D=W/'temp/rebase-359934-20261111-r6'/project;R=D/'gbs-root/local/BUILD-ROOTS/scratch.x86_64.0'
 builds=list((R/'home/abuild/rpmbuild/BUILD').glob('llvm-*/build'));assert len(builds)==1
 tool=builds[0]/'bin/llvm-objdump';loader=R/'lib64/ld-linux-x86-64.so.2'
 argv=[str(loader),'--library-path',':'.join(map(str,[builds[0]/'lib64',R/'lib64',R/'usr/lib64'])),str(tool),'--disassemble','--no-show-raw-insn',str(path)]
 out=O/(project+'-'+kind+'.txt.gz');err=O/(project+'-'+kind+'.stderr')
 save(O/(project+'-'+kind+'-command.json'),dict(argv=argv,tool_sha256=sha(tool),input_sha256=sha(path),input_bytes=path.stat().st_size))
 rows=[];current=None;h=None
 with err.open('wb') as ef,gzip.open(out,'wt',compresslevel=1) as of:
  p=subprocess.Popen(argv,stdout=subprocess.PIPE,stderr=ef,text=True)
  for line in p.stdout:
   of.write(line)
   m=re.match(r'^([0-9a-fA-F]+) <(.+)>:\s*$',line)
   if m:
    if current:current['instruction_text_sha256']=h.hexdigest();rows.append(current)
    current=dict(name=m[2],address=m[1],instruction_lines=0);h=hashlib.sha256()
   elif current and re.match(r'^\s*[0-9a-fA-F]+:',line):
    text=re.sub(r'^\s*[0-9a-fA-F]+:\s*','',line)
    h.update(text.encode());current['instruction_lines']+=1
  if current:current['instruction_text_sha256']=h.hexdigest();rows.append(current)
  assert p.wait()==0,('llvm-objdump failed',str(err))
 save(O/(project+'-'+kind+'-functions.json'),rows)
 return rows
result={}
try:
 for kind in ('bolt-input','final-clang'):
  inputs={};missing=[]
  for project in ('toolchain','basedev'):
   if kind=='bolt-input':
    p=W/'temp/local-full-r6-20261111-materials'/project/'reference-relocs-clang-22'
   else:
    identities=E/project/'comparison/rpm-identities.json'
    if not identities.exists():missing.append(project+': no RPM manifest');continue
    z=json.loads(identities.read_text());rpm=Path(z['clang']['local']['path'])
    dest=W/'temp/local-full-r6-20261111-materials'/project/'final-clang-rpm';dest.mkdir(parents=True,exist_ok=False)
    extract_selected(rpm,{'usr/bin/clang-22'},dest);p=dest/'usr/bin/clang-22'
   if p.exists():inputs[project]=p
   else:missing.append(str(p))
  if missing:result[kind]=dict(status='UNKNOWN',missing=missing);continue
  aa=disassemble('toolchain',kind,inputs['toolchain']);bb=disassemble('basedev',kind,inputs['basedev'])
  def keyed(rows):
   counter=collections.Counter();out={}
   for r in rows:
    i=counter[r['name']];counter[r['name']]+=1;out[(r['name'],i)]=r
   return out
  a,b=keyed(aa),keyed(bb);changes=[]
  for k in sorted(a.keys()|b.keys()):
   x,y=a.get(k),b.get(k)
   if x!=y:changes.append(dict(name=k[0],occurrence=k[1],toolchain=x,basedev=y))
  with gzip.open(O/(kind+'-different-functions.json.gz'),'wt') as f:json.dump(changes,f)
  result[kind]=dict(status='recorded',toolchain_functions=len(aa),basedev_functions=len(bb),different_functions=len(changes),identical_function_records=len(a.keys()&b.keys())-sum(k in a and k in b and a[k]!=b[k] for k in a.keys()&b.keys()),scope='functions identified by llvm-objdump from available symbols; instruction leading addresses removed, operand addresses retained; includes address-only differences; no causal claim')
  save(O/'result.json',result)
except BaseException as ex:
 result['error']=dict(status='UNKNOWN' if isinstance(ex,MemoryError) else 'failed',reason=str(ex));(O/'failure.txt').write_text(traceback.format_exc());raise
finally:
 save(O/'result.json',result);line='FUNCTION_COMPARE 已结束 '+datetime.datetime.now().astimezone().isoformat()+' result='+json.dumps(result,ensure_ascii=False);(O/'end.txt').write_text(line+'\n');print(line,flush=True)
