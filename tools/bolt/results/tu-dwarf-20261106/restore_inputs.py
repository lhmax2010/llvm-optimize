from pathlib import Path
import os,json,time,hashlib,shutil,signal,collections
W=Path('/home/linhao/Toolchain/development/llvm-optimize');B=W.parent/'llvm-optimize-bolt';E=B/'tools/bolt/results/tu-dwarf-20261106';O=W/'temp/tu-inputs-restored-20261106'
assert not O.exists(),str(O);O.mkdir()
rows=json.loads((E/'original-tu-inputs.json').read_text());bysha=collections.defaultdict(list)
for u in rows:bysha[u['sha256']].append(u)
sizes={u['bytes'] for u in rows};found={};checked=[];errors=[];dirs=0;files=0;start=time.monotonic()
def timeout(sig,frame):raise TimeoutError('per-file SHA timeout 45s')
signal.signal(signal.SIGALRM,timeout)
def consider(p):
 global files
 try:
  st=p.stat();files+=1
  if not p.is_file() or st.st_size not in sizes:return
  signal.alarm(45)
  with p.open('rb') as f:h=hashlib.file_digest(f,'sha256').hexdigest()
  signal.alarm(0)
  checked.append({'path':str(p),'bytes':st.st_size,'sha256':h})
  if h in bysha and h not in found:
   for u in bysha[h]:
    dest=O/(str(u['index']).zfill(3)+'.ii');shutil.copyfile(p,dest)
    with dest.open('rb') as f:dh=hashlib.file_digest(f,'sha256').hexdigest()
    assert dh==h
   found[h]=str(p);print('FOUND',len(found),'/',len(bysha),str(p),flush=True)
 except (OSError,TimeoutError) as ex:signal.alarm(0);errors.append({'path':str(p),'error':str(ex)})
roots=[W/'temp',W/'tools',W/'docs',B]
# Restrict traversal to the requested trees; skip virtual mounts, symlink dirs, and new output.
for root in roots:
 for directory,sub,names in os.walk(root,followlinks=False,onerror=lambda ex:errors.append({'path':ex.filename,'error':str(ex)})):
  dirs+=1;d=Path(directory);sub[:]=[n for n in sub if not (d/n).is_symlink() and not os.path.ismount(d/n) and d/n!=O and n not in ('.git',)]
  for n in names:
   p=d/n
   if p.is_symlink():continue
   consider(p)
   if len(found)==len(bysha) or time.monotonic()-start>900:break
  if len(found)==len(bysha) or time.monotonic()-start>900:break
 if len(found)==len(bysha) or time.monotonic()-start>900:break
out=[]
for u in rows:
 v=dict(u);v['original_copy']=u['copy'];v['source_copy_found']=found.get(u['sha256']);v['restored']=u['sha256'] in found
 if v['restored']:v['copy']=str(O/(str(u['index']).zfill(3)+'.ii'))
 out.append(v)
summary={'found':sum(x['restored'] for x in out),'total':len(out),'regenerated':0,'seconds':time.monotonic()-start,'directories':dirs,'files_stat_checked':files,'timed_out':time.monotonic()-start>900,'errors':errors,'all_recovered':len(found)==len(bysha)}
(E/'restore-search.json').write_text(json.dumps(summary,indent=2)+'\n');(E/'restore-candidates.json').write_text(json.dumps(checked,indent=2)+'\n');(E/'restored-inputs.json').write_text(json.dumps(out,indent=2)+'\n')
if summary['all_recovered']:
 (O/'tu-inputs.json').write_text(json.dumps(out,indent=2)+'\n')
 (O/'SHA256SUMS').write_text(''.join(u['sha256']+'  '+str(u['index']).zfill(3)+'.ii\n' for u in rows))
print('RESTORE',json.dumps({k:v for k,v in summary.items() if k!='errors'}),flush=True)
