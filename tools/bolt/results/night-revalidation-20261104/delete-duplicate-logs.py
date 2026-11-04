"""User-authorized deletion of exactly two duplicate logs; no sudo."""
from pathlib import Path
import os,json,hashlib,gzip,subprocess,datetime,stat
W=Path('/home/linhao/Toolchain/development/llvm-optimize');B=W.parent/'llvm-optimize-bolt';E=Path(__file__).parent;N=W/'temp/night-20261103'
old=json.loads((B/'tools/bolt/results/night-results-20261103/summary.json').read_text());results=[]
def cmd(argv):
 p=subprocess.run(argv,capture_output=True,text=True);return dict(argv=argv,rc=p.returncode,stdout=p.stdout,stderr=p.stderr)
def info(f):
 h=hashlib.sha256();n=0;size=0
 for line in f:h.update(line);n+=1;size+=len(line)
 return dict(sha256=h.hexdigest(),lines=n,bytes=size)
for project in ('toolchain','basedev'):
 d=N/project;p=d/'evidence/rpm-build.log';row=dict(project=project,path=str(p),time=datetime.datetime.now().astimezone().isoformat(),status='skipped');results.append(row)
 try:
  assert p.is_file() and not p.is_symlink();st=p.stat();row.update(bytes=st.st_size,allocated_bytes=st.st_blocks*512)
  with p.open('rb') as f:
   row['first_1MiB_sha256']=hashlib.sha256(f.read(1048576)).hexdigest();f.seek(max(0,st.st_size-1048576));row['last_1MiB_sha256']=hashlib.sha256(f.read()).hexdigest()
  row['restarts']=sum(1 for _ in (d/'evidence/log-restarts.jsonl').open())
  original=Path(old[project]['log_source']);archive=B/'tools/bolt/results/night-results-20261103'/project/'gbs-success.log.gz'
  with original.open('rb') as f:current=info(f)
  with gzip.open(archive,'rb') as f:prior=info(f)
  row.update(original=str(original),original_identity=current,published_54_gzip=str(archive),published_identity=prior)
  assert current==prior;assert current['lines']==old[project]['log_lines'] and current['bytes']==old[project]['log_bytes']
  row['lsof']=cmd(['lsof','-nP','--',str(p)]);row['fuser']=cmd(['fuser','-v',str(p)])
  assert row['lsof']['rc']==1 and not row['lsof']['stdout'],'open file or lsof failure'
  assert row['fuser']['rc']==1 and not row['fuser']['stdout'],'open file or fuser failure'
  row['df_before']=cmd(['df','-B1','/home']);before=os.statvfs('/home');row['before_available']=before.f_bavail*before.f_frsize
  # Recheck inode/device and size immediately before the single allowed rm.
  now=p.stat();assert (st.st_dev,st.st_ino,st.st_size)==(now.st_dev,now.st_ino,now.st_size)
  row['rm']=cmd(['rm','--',str(p)]);assert row['rm']['rc']==0 and not p.exists()
  after=os.statvfs('/home');row['after_available']=after.f_bavail*after.f_frsize;row['released_df_bytes']=row['after_available']-row['before_available'];row['df_after']=cmd(['df','-B1','/home']);row['status']='deleted'
 except Exception as e:row['error']=str(e)
 finally:(E/'deletion.json').write_text(json.dumps(results,indent=2)+'\n');print(project,row['status'],row.get('error',''),flush=True)
