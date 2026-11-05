from pathlib import Path
import subprocess,json
from repo_backup import inspect_backup,BACKUP
p=BACKUP/'_selftest3/source';p.mkdir(parents=True,exist_ok=False)
def git(*a):
 q=subprocess.run(['git','-c','user.name=Hao Lin','-c','user.email=hao.lin@samsung.com','-C',str(p),*a],capture_output=True,text=True);assert q.returncode==0,(a,q.stderr);return q.stdout

git('init');(p/'file').write_text('baseline\n');git('add','file');git('commit','-m','fixture baseline');git('update-ref','refs/remotes/origin/main','HEAD');(p/'file').write_text('unpublished\n');git('commit','-am','fixture unpublished')
for n in [1,2]:
 (p/'file').write_text('stash '+str(n)+'\n');(p/f'new{n}').write_text('untracked stash content\n');git('stash','push','-u','-m','fixture '+str(n))
(p/'file').write_text('staged\n');git('add','file');(p/'file').write_text('unstaged\n')
r=inspect_backup(p,0,str(p),[str(p)]);assert r['safe_to_delete'] and r['unpublished_commits']==1 and r['stashes']==2 and r['tracked_dirty'];Path(__file__).with_suffix('.json').write_text(json.dumps(r,indent=2)+'\n');print('BACKUP_SELFTEST_PASS unpublished=1 stashes=2 staged_and_unstaged=true standalone_readback=true; fixture retained')
