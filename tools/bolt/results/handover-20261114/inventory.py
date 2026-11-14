from pathlib import Path
import subprocess,os,json,re,datetime,hashlib
B=Path('/home/linhao/Toolchain/development/llvm-optimize-bolt');W=Path('/home/linhao/Toolchain/development/llvm-optimize')
E=B/'tools/bolt/results/handover-20261114'
os.environ.update(GIT_OPTIONAL_LOCKS='0',GIT_TERMINAL_PROMPT='0',PYTHONDONTWRITEBYTECODE='1',
 GIT_SSH_COMMAND='ssh -o BatchMode=yes -o StrictHostKeyChecking=yes -o ConnectTimeout=10 -o ConnectionAttempts=1')
def clean(s):
 s=re.sub(r'-----BEGIN [^-]*PRIVATE KEY-----.*?-----END [^-]*PRIVATE KEY-----','[REDACTED PRIVATE KEY]',s,flags=re.S)
 s=re.sub(r'(?i)((?:authorization|proxy-authorization)\s*[:=]\s*)([^\r\n]+)',r'\1[REDACTED]',s)
 s=re.sub(r'(?i)((?:password|passwd|access_token|refresh_token|client_secret|api[_-]?key|cookie|token)\s*[=:]\s*)([^\s,;]+)',r'\1[REDACTED]',s)
 s=re.sub(r'\b(?:gh[pousr]_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]+)\b','[REDACTED GITHUB TOKEN]',s)
 s=re.sub(r'(https?://)[^/@\s]+:[^/@\s]+@',r'\1[REDACTED]@',s)
 return s
def run(argv):
 p=subprocess.run(argv,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,errors='replace')
 return {'argv':argv,'rc':p.returncode,'stdout':clean(p.stdout),'stderr':clean(p.stderr),'time':datetime.datetime.now().astimezone().isoformat()}
def write(n,d): (E/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def git(p,*a):return run(['git','--no-optional-locks','-C',str(p),*a])
def repo(p):
 return {'path':str(p),'branch':git(p,'branch','--show-current'),'head':git(p,'rev-parse','HEAD'),
  'status':git(p,'status','--porcelain=v1','--untracked-files=all'),
  'unpushed_vs_local_remote_tracking':git(p,'log','--format=%H %aI %s','--branches','--tags','--not','--remotes'),
  'head_unpushed_vs_local_tracking':git(p,'log','--format=%H %aI %s','HEAD','--not','--remotes'),
  'stash':git(p,'stash','list','--format=%gd %H %gs'),
  'branches':git(p,'for-each-ref','--format=%(refname) %(objectname) %(upstream) %(upstream:track)','refs/heads','refs/remotes'),
  'worktrees':git(p,'worktree','list','--porcelain')}
def main():
 repos={'W':repo(W),'B':repo(B)}
 write('workspaces.json',repos)
 llvm=W/'temp/rebase-359934-20261106/source'
 origins=[llvm,W/'temp/hq-463c9a13/repo',W/'temp/rebase-359934-20261111-r6/source']
 done=set();trees=[]
 for orig in origins:
  if not orig.exists():continue
  listing=git(orig,'worktree','list','--porcelain')
  paths=[l[9:] for l in listing['stdout'].splitlines() if l.startswith('worktree ')]
  for p in paths:
   if p in done:continue
   done.add(p);trees.append(repo(Path(p)))
 write('llvm-workspaces.json',trees)
 ssh=['ssh','-o','BatchMode=yes','-o','StrictHostKeyChecking=yes','-o','ConnectTimeout=10','-o','ConnectionAttempts=1','-p','29418','lhmax2025@review.tizen.org']
 remote=run(['git','ls-remote','ssh://lhmax2025@review.tizen.org:29418/platform/upstream/llvm','refs/heads/sandbox/lhmax2025/bolt_pgo','refs/heads/tizen_base'])
 write('llvm-ls-remote.json',remote)
 for num in (361395,361396,361397):
  d=run(ssh+['gerrit','query','--format=JSON','--current-patch-set','--patch-sets','--all-approvals','--all-reviewers','--dependencies','--comments','change:'+str(num)])
  write('gerrit-'+str(num)+'.json',d)
  if d['rc']!=0:
   print('GERRIT UNKNOWN',num,d['stderr']);break
  parsed=[json.loads(l) for l in d['stdout'].splitlines() if l.strip()]
  write('gerrit-'+str(num)+'-parsed.json',parsed)
  print('GERRIT',num,[(v.get('status'),v.get('currentPatchSet',{}).get('number')) for v in parsed if 'number' in v])
 heads=dict((line.split()[1],line.split()[0]) for line in remote['stdout'].splitlines() if len(line.split())==2) if remote['rc']==0 else {}
 base='13c3e223d9e1b35e4affb55255c5042f8c940f35';head=heads.get('refs/heads/tizen_base')
 weekly={'remote_head':head,'baseline':base,'verdict':'UNKNOWN','reason':'remote/object unavailable; no fetch allowed in read-only repository'}
 if head:
  available=git(llvm,'cat-file','-e',head+'^{commit}')
  if available['rc']==0:
   weekly.update(tree=git(llvm,'rev-parse',head+'^{tree}'),baseline_tree=git(llvm,'rev-parse',base+'^{tree}'),
    ancestor=git(llvm,'merge-base','--is-ancestor',base,head),commits=git(llvm,'log','--format=fuller',base+'..'+head),
    nonmerge=git(llvm,'rev-list','--no-merges',base+'..'+head),diff_stat=git(llvm,'diff','--stat',base,head),diff=git(llvm,'diff',base,head))
   if head==base:weekly['verdict']='A'
   elif weekly['ancestor']['rc']==0 and not weekly['nonmerge']['stdout'].strip() and not weekly['diff']['stdout']:weekly['verdict']='B'
   else:weekly['verdict']='C'
   weekly['reason']='read-only local object comparison; no fetch'
 write('weekly-tizen-base.json',weekly)
 print('WEEKLY',weekly['verdict'],head,'worktrees',len(trees))
 # Step5 evidence only; no modification until literal comparison adjudicated.
 condition={}
 for label,revision in [('ps10',base),('fea','fea0fe464d56e17f2c7588c557bfffd9f6ac352b')]:
  d=git(llvm,'show',revision+':packaging/llvm-static-archives-native.py')
  ls=d['stdout'].splitlines()
  matches=[{'line':i,'raw':l} for i,l in enumerate(ls,1) if 'if symbol[3] != 0xfff1' in l]
  condition[label]={'revision':revision,'rc':d['rc'],'matches':matches,
   'contexts':[{'start':max(1,m['line']-4),'text':'\n'.join(ls[max(0,m['line']-5):m['line']+2])} for m in matches]}
 condition['literal_equal']=condition['ps10']['matches']==condition['fea']['matches']
 condition['condition_equal']=len(condition['ps10']['matches'])==len(condition['fea']['matches'])==1 and condition['ps10']['matches'][0]['raw']==condition['fea']['matches'][0]['raw']
 write('claims-ps10-check.json',condition);print('CLAIMS_CONDITION_EQUAL',condition['condition_equal'])
 print('已结束',datetime.datetime.now().astimezone().isoformat(),'step1-readonly PASS')
if __name__=='__main__':main()
