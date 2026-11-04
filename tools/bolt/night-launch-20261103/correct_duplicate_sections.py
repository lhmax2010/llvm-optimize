"""Recheck only previously rejected duplicate-name ELF inputs; no other retries."""
from pathlib import Path
import sys,json,datetime,traceback
from checks import save,file_proof
D=Path(sys.argv[1]);O=D/'validation-02';E=O/'section-parser-correction';E.mkdir(exist_ok=False)
status='failed'
try:
 rows=json.loads((O/'rpm23.json').read_text());out=[]
 for p in rows:
  for c in p['content_changes']:
   if c.get('error')!='duplicate section names':continue
   base=O/'rpm-bytes'/p['package'].replace('\t','-');a=base/'old'/c['path'];b=base/'new'/c['path']
   try:r=file_proof(a,b)
   except AssertionError as e:r=dict(classification='FAIL',error=str(e))
   row=dict(package=p['package'],path=c['path'],old_error=c['error'],result=r);out.append(row);save(E/'results.json',out);print(p['package'],c['path'],r['classification'],r.get('error',''),flush=True)
 status='ok'
except BaseException:traceback.print_exc()
finally:
 (E/'ended.txt').write_text('SECTION_RECHECK 已结束 '+datetime.datetime.now().astimezone().isoformat()+' status='+status+'\n');print((E/'ended.txt').read_text(),flush=True)
sys.exit(0 if status=='ok' else 1)
