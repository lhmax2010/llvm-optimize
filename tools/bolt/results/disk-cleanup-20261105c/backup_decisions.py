from pathlib import Path
import os,json,re,subprocess,hashlib
from checks import command,stamp
E=Path(__file__).resolve().parent;R=Path('/home/linhao/Toolchain/development/llvm-optimize/temp/deleted-repo-backup-20261105')
a=json.loads((E/'backup-plan.json').read_text());out=[]
(E/'backup-du-before.json').write_text(json.dumps(command(['timeout','120','nice','-n','19','ionice','-c3','du','-sx','-B1',str(R)],130),indent=2));(E/'backup-df-before.json').write_text(json.dumps(command(['df','-B1','/home']),indent=2))
for x in a:
 d=Path(x['directory']);v=d/'verified.git';j=json.loads((d/'inspection-before.json').read_text());details=[]
 for sha in x.get('patch_commit_order',[]):
  p=command(['git','--no-optional-locks','-c','safe.directory='+str(v),'-C',str(v),'show','-s','--format=%P',sha]);details.append({'commit':sha,'parents':p['stdout'].split() if p['rc']==0 else 'UNKNOWN','query_rc':p['rc']})
 x['patch_base_details']={'unpublished.patch':details,'index.patch':x['head'],'worktree.patch':{'commit':x['head'],'apply_index_patch_first':True},'stashes':[]}
 for p in sorted(d.glob('stash-*.commit.txt')):
  lines=p.read_text();x['patch_base_details']['stashes'].append({'file':p.name,'commit':re.findall(r'^commit ([0-9a-f]{40})$',lines,re.M),'parents':re.findall(r'^parent ([0-9a-f]{40})$',lines,re.M)})
 x['uid']=d.stat().st_uid;x['gid']=d.stat().st_gid;x['writable']=os.access(d,os.W_OK)
 x['action']='retained';x['execution_reason']='preconditions not met: '+ '; '.join(x['reasons']) if not x['eligible'] else 'root-owned non-writable backup; user permits root deletion only in part 1; no sudo in part 2'
 if x['eligible'] and x['writable']:raise RuntimeError('unexpected writable eligible backup: review before executing')
 out.append(x)
(E/'backup-manifests.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
(E/'backup-unclassified-top.json').write_text(json.dumps([str(p) for p in R.iterdir() if p.is_dir() and not any(Path(x['directory']).is_relative_to(p) for x in out)],indent=2))
(E/'backup-du-after.json').write_text(json.dumps(command(['timeout','120','nice','-n','19','ionice','-c3','du','-sx','-B1',str(R)],130),indent=2));(E/'backup-df-after.json').write_text(json.dumps(command(['df','-B1','/home']),indent=2))
line='BACKUP_SLIM 已结束 '+stamp()+' status=skipped reason=9-eligible-but-root-owned;17-unproven;no-second-sudo'
(E/'backup-finished.txt').write_text(line+'\n');print(line,flush=True)
