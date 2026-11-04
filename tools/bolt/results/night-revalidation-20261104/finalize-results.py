"""Summarize original and targeted results without replacing any raw verdict."""
from pathlib import Path
import json,datetime,subprocess
W=Path('/home/linhao/Toolchain/development/llvm-optimize');E=Path(__file__).parent;N=W/'temp/night-20261103'
rows={}
for project in ('toolchain','basedev'):
 O=N/project/'validation-02';assert (O/'ended.txt').exists()
 original=json.loads((O/'result.json').read_text());effective=json.loads(json.dumps(original))
 effective['raw_result']='result.json';effective['corrections']=[]
 if project=='toolchain':
  rpm=json.loads((O/'rpm23-corrected.json').read_text());assert len(rpm)==23
  effective['corrections'].append({'check':'rpm23','file':'rpm23-corrected.json','PASS':sum(r['PASS'] for r in rpm),'FAIL':sum(not r['PASS'] for r in rpm)})
 else:
  r=json.loads((O/'release-check-resume/result.json').read_text());assert r['status']=='ok'
  assert 'FileExistsError' in original['checks']['release'].get('error','')
  effective['checks']['release']={'status':'PASS','targeted_result':'release-check-resume/result.json','original_failure_retained':'result.json'}
  effective['corrections'].append({'check':'release','reason':'identical shared RPM header path; extraction-only fix, targeted recheck'})
 effective['status']='ok' if all(c['status']=='PASS' for c in effective['checks'].values()) else 'failed'
 (O/'result-effective.json').write_text(json.dumps(effective,indent=2)+'\n');rows[project]=effective
(E/'effective-results.json').write_text(json.dumps(rows,indent=2)+'\n')
units=['night-revalidation-'+p+'-20261104.service' for p in ('toolchain','basedev','release-resume','section-correction')]
checks=[]
for unit in units:
 cmd=['systemctl','--user','show',unit,'-p','ActiveState','-p','SubState','-p','Result','-p','MainPID','-p','ControlGroup','-p','MemoryPeak']
 p=subprocess.run(cmd,capture_output=True,text=True);checks.append(dict(argv=cmd,rc=p.returncode,stdout=p.stdout,stderr=p.stderr));assert 'ActiveState=active' not in p.stdout
(E/'ended-service-checks.json').write_text(json.dumps(checks,indent=2)+'\n')
line='REVALIDATION_EFFECTIVE 已结束 '+datetime.datetime.now().astimezone().isoformat()+' status='+('ok' if all(v['status']=='ok' for v in rows.values()) else 'failed')+' reason=T-strict-file-differences;D-release-targeted-check-applied'
with (E/'revalidation.log').open('a') as f:f.write(line+'\n')
print(line)
