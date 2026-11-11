from pathlib import Path
import sys,json,hashlib,gzip,datetime,time,traceback,re
sys.path.insert(0,'/home/linhao/qb_fetch/.deps')
from playwright.sync_api import sync_playwright
E=Path('/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/qb-1225393-1225395')
def save(rel,data,url):
 if isinstance(data,str):data=data.encode()
 p=E/rel;p.parent.mkdir(parents=True,exist_ok=True)
 row={'url':url,'raw_bytes':len(data),'raw_sha256':hashlib.sha256(data).hexdigest()}
 if len(data)>1048576:p=p.with_name(p.name+'.gz');data=gzip.compress(data,mtime=0)
 assert not p.exists(),p
 p.write_bytes(data);row.update(file=str(p.relative_to(E)),bytes=len(data),sha256=hashlib.sha256(data).hexdigest())
 with (E/'provenance.jsonl').open('a') as f:f.write(json.dumps(row)+'\n')
 return p
status='failed'
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch(headless=False,executable_path='/home/linhao/.cache/ms-playwright/chromium-1243/chrome-linux64/chrome',args=['--disable-dev-shm-usage'])
  ctx=browser.new_context(service_workers='block');page=ctx.new_page()
  page.goto('https://quickbuild.tizen.org/build/1225393/overview',wait_until='domcontentloaded',timeout=90000)
  def logged():return not page.locator('input[type=password]').count() and not any(x in page.url.lower() for x in ['/signin','/login'])
  if not logged():print('BROWSER_LOGIN_REQUIRED: visible Chromium; enter credentials only in browser',flush=True)
  deadline=time.monotonic()+1800
  while not logged():
   if time.monotonic()>deadline:raise RuntimeError('manual login timeout')
   page.wait_for_timeout(2000)
  print('BROWSER_LOGIN_COMPLETE',flush=True)
  for bid in [1225393,1225395]:
   for tab in ['overview','log']:
    url=f'https://quickbuild.tizen.org/build/{bid}/{tab}'
    page.goto(url,wait_until='domcontentloaded',timeout=90000)
    page.wait_for_timeout(1000)
    if not logged():raise RuntimeError('login expired')
    text=page.locator('body').inner_text()
    if tab=='overview':
     fields=dict(line.split('\t',1) for line in text.splitlines() if '\t' in line)
     assert fields.get('Build Package List')=='platform/upstream/llvm@60fabc723f30c5cc04146a9dd83487ebed63f259',fields.get('Build Package List')
     profile=fields.get('Profile URL','')
     assert profile.rstrip('/').endswith(('/tizen-base-toolchain_20261030.061318','/tizen-base-dev_20261030.061217')),profile

    save(f'{bid}/{tab}.txt',text,url)
    links=page.locator('a[href]').evaluate_all('(a)=>a.map(x=>({text:x.innerText,url:x.href}))')
    # Save only navigation/download links, never browser state or request headers.
    save(f'{bid}/{tab}-links.json',json.dumps(links,indent=2),url)
    if tab=='overview':print('OVERVIEW',bid,text,flush=True)
    else:
     downloads=[r for r in links if r['text'].strip()=='Save']
     if not downloads:raise RuntimeError('Save link absent '+str(bid))
     response=ctx.request.get(downloads[0]['url'],timeout=120000)
     if response.status!=200:raise RuntimeError('download HTTP '+str(response.status))
     data=response.body()
     if b'type="password"' in data[:200000]:raise RuntimeError('login content rejected')
     save(f'{bid}/full-log.txt',data,downloads[0]['url'])
     print('PARENT_LOG',bid,len(data),hashlib.sha256(data).hexdigest(),flush=True)
  browser.close();status='ok'
except Exception:
 traceback.print_exc()
finally:
 print('QB_BROWSER 已结束',datetime.datetime.now().astimezone().isoformat(),'status='+status,flush=True)
if status!='ok':raise SystemExit(1)
