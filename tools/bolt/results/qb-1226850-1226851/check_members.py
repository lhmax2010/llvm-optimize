from pathlib import Path
import json,gzip,hashlib,datetime,sys,re
from ar_members import members
from rpm_extract import extract_selected
E=Path(__file__).parent;W=Path('/home/linhao/Toolchain/development/llvm-optimize')
X=W/'temp/qb-1226850-1226851/member-check';X.mkdir(exist_ok=False)
results=[]
for row in json.loads((E/'package-results.json').read_text()):
 if not row['name'].startswith('llvm-static-devel-'):continue
 key=row['build']+'-'+row['arch'];names={x['file'] for x in row['archives']}
 print('START',key,len(names),'archives',flush=True)
 for side in ('old','new'):extract_selected(row[side]['path'],names,X/key/side)
 records=[]
 for n in sorted(names):
  a,b=members(X/key/'old'/n),members(X/key/'new'/n)
  diff=[dict(index=i,old=x,new=y) for i,(x,y) in enumerate(zip(a,b)) if x!=y]
  assert len(a)==len(b) and not diff,(key,n,diff[:2])
  records.append(dict(file=n,old=a,new=b,content_members=sum(x['name'] not in ('/','//','/SYM64/') for x in a),status='PASS'))
 with gzip.open(E/(key+'-members.json.gz'),'wt') as f:json.dump(records,f)
 native=[]
 with gzip.open(E/row['build']/row['arch']/'llvm.buildlog.txt.gz','rt') as f:
  for i,l in enumerate(f,1):
   text=re.sub(r'^\[\s*\d+s\] ?','',l).strip()
   if text.startswith('{'):
    try:z=json.loads(text)
    except ValueError:continue
    if 'converted' in z and 'preserved' in z and 'path' in z:native.append(dict(line=i,record=z,raw=l.rstrip()))
 if row['arch']=='x86_64':
  assert len(records)==225 and len(native)==225
  assert sum(x['record']['converted'] for x in native)==3853 and sum(x['record']['preserved'] for x in native)==11
 else:assert not native
 result=dict(build=row['build'],arch=row['arch'],archives=len(records),members=sum(x['content_members'] for x in records),converted=sum(x['record']['converted'] for x in native),native_members_preserved=sum(x['record']['preserved'] for x in native),conversion_applicable=row['arch']=='x86_64',status='PASS',evidence=key+'-members.json.gz')
 results.append(result)
 (E/(key+'-conversion-records.json')).write_text(json.dumps(native,indent=2)+'\n')
 (E/'member-summary.json').write_text(json.dumps(results,indent=2)+'\n')
 print('RESULT',json.dumps(result),flush=True)
end='B3 已结束 '+datetime.datetime.now().astimezone().isoformat()+' PASS'
(E/'b3-end.txt').write_text(end+'\n');print(end,flush=True)
