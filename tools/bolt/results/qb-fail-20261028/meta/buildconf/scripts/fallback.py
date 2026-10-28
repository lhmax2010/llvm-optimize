from pathlib import Path
import json,subprocess,os,tarfile,hashlib
W=Path('/home/linhao/Toolchain/development/llvm-optimize');B=W.parent/'llvm-optimize-bolt';D=Path(__file__).resolve().parent;E=B/'tools/bolt/results/qb-fail-20261028/meta/buildconf';q=json.loads((E/'1211018-package-lists.json').read_text())[0]['packages'];names={x.rsplit('-',2)[0] for x in (E/'srpm-list.txt').read_text().splitlines()}
missing=[x for x in q if x.rsplit('/',1)[-1] not in names];rows=[]
for project in missing:
 key=project.replace('/','__');p=D/(key+'.tar');env=dict(os.environ,GIT_SSH_COMMAND='ssh -o BatchMode=yes -o ConnectTimeout=15')
 url='ssh://review.tizen.org:29418/'+project
 rev=subprocess.run(['git','ls-remote',url,'refs/heads/tizen_base'],env=env,capture_output=True,text=True,timeout=60)
 row={'project':project,'url':url,'requested_ref':'refs/heads/tizen_base','snapshot_manifest_commit':q[project],'ls_remote_rc':rev.returncode,'ls_remote':rev.stdout,'ls_remote_stderr':rev.stderr}
 with p.open('wb') as o:
  r=subprocess.run(['git','archive','--remote='+url,'refs/heads/tizen_base','packaging'],env=env,stdout=o,stderr=subprocess.PIPE,timeout=120)
 row.update(archive_rc=r.returncode,archive_stderr=r.stderr.decode(errors='replace'),specs=[])
 if r.returncode==0:
  with tarfile.open(p) as t:
   for m in t.getmembers():
    if m.isfile() and m.name.endswith('.spec'):
     data=t.extractfile(m).read();dest=E/'git-specs'/key/Path(m.name).name;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data);row['specs'].append(dict(path=str(dest.relative_to(E)),source_path=m.name,bytes=len(data),sha256=hashlib.sha256(data).hexdigest()))
 rows.append(row);(E/'git-spec-provenance.json').write_text(json.dumps(rows,indent=2)+'\n');print(project,r.returncode,len(row['specs']),row['archive_stderr'][:100],flush=True)
