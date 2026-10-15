"""Integrity/reconciliation checks over acquired evidence; no compilation or product execution."""
from common import *
import csv,re,hashlib,collections,subprocess
from bs4 import BeautifulSoup
from urllib.parse import urlparse,parse_qs
errors=[]
def check(v,msg):
 if not v:errors.append(msg)
files=list(OUT.rglob('*'));textfiles=[p for p in files if p.is_file() and p.suffix not in ('.pyc',)]
counts={str(p.relative_to(OUT)):len(p.read_bytes().splitlines()) for p in textfiles}
refcount=0
for p in list(OUT.glob('*.csv'))+[OUT/'SIZE_FINDINGS.md']:
 for match in re.finditer(r'(raw/[^\s;:,<>"\[\]()]+):(\d+)(?:-(\d+))?',p.read_text()):
  path,first,last=match[1],int(match[2]),int(match[3] or match[2]);refcount+=1
  check(path in counts,f'{p.name}: missing {path}')
  if path in counts:check(1<=first<=last<=counts[path],f'{p.name}: range {path}:{first}-{last}, total {counts[path]}')
fetches=[json.loads(l) for l in (RAW/'fetch_manifest.jsonl').read_text().splitlines()]
for m in fetches:
 p=ROOT/m['file']
 if str(p).startswith(str(RAW)):
  check(p.exists(),'missing fetched '+m['file'])
  if p.exists():check(sha(p)==m['sha256'],'fetched body SHA changed '+m['file'])
extraction_check_available=(TEMP/'extract').is_dir()
extraction_clean=not any((TEMP/'extract').iterdir()) if extraction_check_available else None
if extraction_check_available:check(extraction_clean,'extraction remnants')
check(not list(OUT.rglob('*.rpm')),'RPM under output')
# Every range commit in HTML has a corresponding format-patch entry, and conversely.
commits=list(csv.DictReader((OUT/'source_commits.csv').open()))
for repo in ['llvm','qemu-accel']:
 s=BeautifulSoup((RAW/f'{repo}_range_log.html').read_text(),'html.parser')
 htmlset={parse_qs(urlparse(a['href']).query)['id'][0] for td in s.select('td.logsubject') for a in [td.find('a')]}
 csvset={r['commit'] for r in commits if r['repository']==repo and r['direction']=='old..new'}
 check(htmlset==csvset,repo+' range commits mismatch')
# Validate final llvm.spec diff by applying line records in memory to the downloaded old endpoint.
changes=list(csv.DictReader((OUT/'source_changes.csv').open()))
for repo,oldname,newname,path in [('llvm','llvm_old_llvm.spec','llvm_new_llvm.spec','packaging/llvm.spec'),('qemu-accel','qemu-accel_old_armv7l_retry.spec','qemu-accel_new_armv7l_retry.spec','packaging/qemu-accel-armv7l.spec')]:
 old=(RAW/oldname).read_text().splitlines();new=(RAW/newname).read_text().splitlines();removed={};added={}
 for r in changes:
  if r['repository']!=repo or not r['scope'].startswith('endpoint') or r['file']!=path:continue
  if r['sign']=='-':removed[int(r['old_line'])]=r['text'];check(old[int(r['old_line'])-1]==r['text'],'removed text mismatch '+str(r))
  else:added[int(r['new_line'])]=r['text'];check(new[int(r['new_line'])-1]==r['text'],'added text mismatch '+str(r))
 check([l for i,l in enumerate(old,1) if i not in removed]==[l for i,l in enumerate(new,1) if i not in added],repo+' unchanged endpoint content mismatch')
result={'checked_at':now(),'raw_references_checked':refcount,'reference_errors':errors,'all_checks_pass':not errors,'csv_files':sorted(p.name for p in OUT.glob('*.csv')),'raw_files':sum(p.is_file() for p in RAW.rglob('*')),'output_bytes_excluding_python_cache':sum(p.stat().st_size for p in textfiles),'no_rpm_under_output':not list(OUT.rglob('*.rpm')),'no_extraction_directories_left':extraction_clean,'extraction_check_available':extraction_check_available,'free_temp_bytes':__import__('shutil').disk_usage(TEMP).free if TEMP.exists() else '未获取（本机无采集临时目录）'}
(RAW/'final_validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False,indent=2));raise SystemExit(bool(errors))
