from pathlib import Path
import json,subprocess,os,tarfile,hashlib
W=Path('/home/linhao/Toolchain/development/llvm-optimize');B=W.parent/'llvm-optimize-bolt';D=Path(__file__).resolve().parent;E=B/'tools/bolt/results/qb-fail-20261028/meta/buildconf';rows=json.loads((E/'git-qb-spec-provenance.json').read_text())
for x in json.loads((E/'project-spec-coverage.json').read_text()):
 if not x['qb_commit'] or any(r['project']==x['project'] for r in rows):continue
 if x['exact_qb_commit_specs'] and not all(r['source']=='Gerrit tizen_base fallback' for r in x['exact_qb_commit_specs']):continue
 project=x['project'];commit=x['qb_commit'];key=project.replace('/','__');p=D/(key+'-qb.tar');url='ssh://review.tizen.org:29418/'+project
 row={'project':project,'url':url,'requested_commit':commit,'specs':[]}
 with p.open('wb') as o:
  r=subprocess.run(['git','archive','--remote='+url,commit,'packaging'],env=dict(os.environ,GIT_SSH_COMMAND='ssh -o BatchMode=yes -o ConnectTimeout=15'),stdout=o,stderr=subprocess.PIPE,timeout=120)
 row.update(archive_rc=r.returncode,archive_stderr=r.stderr.decode(errors='replace'))
 if r.returncode==0:
  with tarfile.open(p) as t:
   for m in t.getmembers():
    if m.isfile() and m.name.endswith('.spec'):
     data=t.extractfile(m).read();dest=E/'qb-specs'/key/Path(m.name).name;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data);row['specs'].append(dict(path=str(dest.relative_to(E)),source_path=m.name,bytes=len(data),sha256=hashlib.sha256(data).hexdigest()))
 rows.append(row);(E/'git-qb-spec-provenance.json').write_text(json.dumps(rows,indent=2)+'\n');print(project,r.returncode,len(row['specs']),row['archive_stderr'][:80],flush=True)
