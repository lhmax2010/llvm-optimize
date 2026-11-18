from pathlib import Path
import json,subprocess,hashlib,difflib,datetime
from rpm_extract import extract_selected
E=Path(__file__).resolve().parent
repo='/home/linhao/Toolchain/development/llvm-optimize/temp/ps5-helper-126/source'
H2='b06ee2ac62085748b1b137523582c989ac78184e';H4='7a7bc17467d4c5da9763e86e3c74a123b3ff0df2'
rows=json.loads((E/'package-results.json').read_text());result={}
for r in rows:
 if not r['name'].endswith('.src.rpm'):continue
 for side,rev in [('old',H2),('new',H4)]:
  bid=r[side]['build'];dest=E/'source-text'/bid
  names={d['file'] for d in r['changes']};extract_selected(Path(r[side]['path']),names,dest)
  helper=(dest/'clang-bolt-helper.py').read_bytes()
  blob=subprocess.check_output(['git','-C',repo,'show',rev+':packaging/clang-bolt-helper.py'])
  assert helper==blob,('helper blob mismatch',bid)
 a=E/'source-text'/r['old']['build'];b=E/'source-text'/r['new']['build']
 result[r['build']]={'baseline':r['baseline'],'files':[]}
 for d in r['changes']:
  name=d['file'];old=(a/name).read_bytes();new=(b/name).read_bytes()
  diff=''.join(difflib.unified_diff(old.decode().splitlines(True),new.decode().splitlines(True),fromfile=r['baseline']+'/'+name,tofile=r['build']+'/'+name))
  path=E/'source-diffs'/(r['build']+'-'+name+'.diff');path.parent.mkdir(exist_ok=True);path.write_text(diff)
  item={'file':name,'diff':str(path.relative_to(E)),'old_sha256':hashlib.sha256(old).hexdigest(),'new_sha256':hashlib.sha256(new).hexdigest()}
  if name=='clang-bolt-helper.py':item.update(classification='helper source change; both sides byte-identical to their Git blobs',status='PASS')
  elif name=='llvm.spec':
   def nonvcs(data):return b''.join(l for l in data.splitlines(True) if not l.startswith(b'VCS:'))
   onlyvcs=nonvcs(old)==nonvcs(new);item.update(only_vcs=onlyvcs,classification='generated VCS metadata' if onlyvcs else 'UNCLASSIFIED',status='CLASSIFIED' if onlyvcs else 'UNCLASSIFIED')
  else:
   marker=b'diff --git ';pos1=old.find(marker);pos2=new.find(marker)
   eq=pos1>=0 and pos2>=0 and old[pos1:]==new[pos2:]
   item.update(code_body_equal=eq,old_body_sha256=hashlib.sha256(old[pos1:]).hexdigest() if pos1>=0 else None,new_body_sha256=hashlib.sha256(new[pos2:]).hexdigest() if pos2>=0 else None,classification='UNCLASSIFIED pending inspection',status='UNCLASSIFIED')
  result[r['build']]['files'].append(item)
  print(r['build'],name,json.dumps(item),flush=True)
  if name!='clang-bolt-helper.py':print(diff[:20000],flush=True)
(E/'source-audit-initial.json').write_text(json.dumps(result,indent=2)+'\n')
gitdiff=subprocess.check_output(['git','-C',repo,'diff',H2,H4,'--','packaging/clang-bolt-helper.py'])
(E/'H2-to-H4-helper.diff').write_bytes(gitdiff)
(E/'source-git-name-status.txt').write_bytes(subprocess.check_output(['git','-C',repo,'diff','--name-status',H2,H4]))
end='SOURCE 已结束 '+datetime.datetime.now().astimezone().isoformat()+' status=COLLECTED';(E/'source-end.txt').write_text(end+'\n');print(end)
