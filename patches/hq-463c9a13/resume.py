"""Read remote/source objects; only the disposable clone receives a trial cherry-pick."""
from pathlib import Path
import os,subprocess,json,datetime,hashlib,re
W=Path('/home/linhao/Toolchain/development/llvm-optimize');R=W/'temp/hq-463c9a13/repo';E=Path(__file__).parent
HQ='463c9a133a6dfea9adf1e6c8e07ab705cbf2a587';OURS='9e39fa8a61392652bb28b75fc26216675bcad1d5';URL='ssh://lhmax2025@review.tizen.org:29418/platform/upstream/llvm'
env=dict(os.environ,GIT_SSH_COMMAND='ssh -o BatchMode=yes',GIT_TERMINAL_PROMPT='0',LC_ALL='C');commands=json.loads((E/'commands.json').read_text())
def save(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def run(label,args,allow=(0,)):
 label=label+'-resume' if (E/(label+'.stdout')).exists() else label
 start=datetime.datetime.now().astimezone().isoformat();r=subprocess.run(args,cwd=R,env=env,capture_output=True)
 (E/(label+'.stdout')).write_bytes(r.stdout);(E/(label+'.stderr')).write_bytes(r.stderr)
 row=dict(label=label,argv=args,cwd=str(R),start=start,end=datetime.datetime.now().astimezone().isoformat(),returncode=r.returncode);commands.append(row);save(E/'commands.json',commands)
 if r.returncode not in allow:raise RuntimeError((label,r.returncode,r.stderr.decode(errors='replace')))
 return r

def git(label,*args,allow=(0,)):return run(label,['git','-c','pack.threads=2',*args],allow)
q=[json.loads(l) for l in (E/'gerrit-query.jsonl').read_text().splitlines() if '"project"' in l][0];ref=q['currentPatchSet']['ref']
git('fetch-9b8d74af','fetch',URL,'9b8d74af825d3caab67f8ff7cbc19fcda8a7ad64')
parent=git('parent','rev-parse',HQ+'^').stdout.decode().strip();base=git('tizen-base-head','rev-parse','refs/remotes/origin/tizen_base').stdout.decode().strip()
anc=[]
for name in ('refs/remotes/origin/tizen_base','f999bd40','9b8d74af','67619ec8','d4d6ca16','f2553114',OURS):
 full=git('resolve-'+name.split('/')[-1],'rev-parse',name+'^{commit}').stdout.decode().strip()
 for a,b in ((full,HQ),(HQ,full)):
  r=git('ancestor-'+a[:8]+'-'+b[:8],'merge-base','--is-ancestor',a,b,allow=(0,1));anc.append(dict(name=name,ancestor=a,descendant=b,exit_code=r.returncode,is_ancestor=r.returncode==0))
r=git('hq-parent-in-ours','merge-base','--is-ancestor',parent,OURS,allow=(0,1));parent_in_ours=r.returncode==0
git('merge-base-hq-ours','merge-base',HQ,OURS)
files={}
for name,sha in [('hq',HQ),('hybrid','d4d6ca16'),('bolt','f2553114'),('flags',OURS)]:
 files[name]=git('files-'+name,'diff-tree','--no-commit-id','--name-only','-r',sha).stdout.decode().splitlines()
oursfiles=set().union(*(set(files[k]) for k in ('hybrid','bolt','flags')))
save(E/'overlap.json',dict(files=files,intersection=sorted(set(files['hq'])&oursfiles),per_commit={k:sorted(set(files['hq'])&set(files[k])) for k in ('hybrid','bolt','flags')}))
# Source1005 was modified. Also export its spec call site, shared by 356627/356639.
paths=['packaging/llvm-static-archives-native.py','packaging/llvm.spec'];versions={'hq':HQ,'ours':OURS,'parent':parent}
for label,sha in versions.items():
 for path in paths:
  r=git('show-'+label+'-'+Path(path).name,'show',sha+':'+path);p=E/'files'/label/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(r.stdout)
for a,b in [('parent','hq'),('ours','hq'),('parent','ours')]:
 for path in paths:
  r=git('diff-'+a+'-'+b+'-'+Path(path).name,'diff','--no-ext-diff','--full-index',versions[a],versions[b],'--',path);p=E/'diffs'/(a+'-to-'+b+'-'+Path(path).name+'.diff');p.parent.mkdir(exist_ok=True);p.write_bytes(r.stdout)
# Sparse checkout only reduces local files; the index and history remain complete.
git('sparse-init','sparse-checkout','init','--cone');git('sparse-packaging','sparse-checkout','set','packaging')
git('trial-branch','switch','-c','hq-463c9a13-probe',OURS)
git('trial-before','status','--porcelain=v1')
r=git('cherry-pick','-c','user.name=Hao Lin','-c','user.email=hao.lin@samsung.com','cherry-pick','--no-commit',HQ,allow=(0,1))
pick_rc=r.returncode
conflicts=git('conflict-files','diff','--name-only','--diff-filter=U').stdout.decode().splitlines()
git('unmerged-index','ls-files','-u');git('trial-status','status','--porcelain=v1');git('trial-diff-stat','diff','--stat');git('trial-cached-stat','diff','--cached','--stat');git('trial-diff','diff','--no-ext-diff');git('trial-cached-diff','diff','--cached','--no-ext-diff')
blocks=[]
for path in conflicts:
 content=(R/path).read_bytes();p=E/'conflicts'/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(content)
 lines=content.decode(errors='replace').splitlines(keepends=True);start=None
 for i,line in enumerate(lines):
  if line.startswith('<<<<<<<'):start=i
  if start is not None and line.startswith('>>>>>>>'):
   blocks.append(dict(path=path,start_line=start+1,end_line=i+1,text=''.join(lines[start:i+1])));start=None
save(E/'conflict-blocks.json',blocks)
abort=git('cherry-pick-abort','cherry-pick','--abort',allow=(0,128))
git('after-abort-status','status','--porcelain=v1');git('after-abort-head','rev-parse','HEAD')
save(E/'summary.json',dict(hq=HQ,parent=parent,tizen_base_head=base,ours=OURS,gerrit_status=q['status'],change=q['number'],change_ref=ref,parent_is_ancestor_of_ours=parent_in_ours,ancestry=anc,versions=versions,exported_paths=paths,cherry_pick_exit_code=pick_rc,conflicts=conflicts,conflict_blocks=len(blocks),abort_exit_code=abort.returncode,trial_branch='hq-463c9a13-probe'))
print(json.dumps(json.loads((E/'summary.json').read_text()),indent=2))
