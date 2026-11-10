from pathlib import Path
import sys,json,time,datetime,traceback
sys.path.insert(0,'/home/linhao/qb_fetch/.deps')
from playwright.sync_api import sync_playwright
E=Path(__file__).resolve().parent
status='failed'
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch(headless=False,executable_path='/home/linhao/.cache/ms-playwright/chromium-1243/chrome-linux64/chrome',args=['--disable-dev-shm-usage'])
  ctx=browser.new_context(service_workers='block');page=ctx.new_page()
  page.goto('https://quickbuild.tizen.org/build/1216400/overview',wait_until='domcontentloaded',timeout=90000)
  def logged():return not page.locator('input[type=password]').count() and not any(x in page.url.lower() for x in ['/signin','/login'])
  if not logged():print('BROWSER_LOGIN_REQUIRED: visible Chromium; credentials only in browser',flush=True)
  deadline=time.monotonic()+1800
  while not logged():
   if time.monotonic()>deadline:raise RuntimeError('manual login timeout')
   page.wait_for_timeout(2000)
  print('BROWSER_LOGIN_COMPLETE',flush=True)
  for bid in ['1216400','1216401']:
   url='https://quickbuild.tizen.org/build/'+bid+'/overview'
   page.goto(url,wait_until='domcontentloaded',timeout=90000);page.wait_for_timeout(1000)
   if not logged():raise RuntimeError('login expired')
   text=page.locator('body').inner_text()
   p=E/bid;p.mkdir(exist_ok=False)
   (p/'overview.txt').write_text(text)
   links=page.locator('a[href]').evaluate_all('(a)=>a.map(x=>({text:x.innerText,url:x.href}))')
   (p/'overview-links.json').write_text(json.dumps(links,ensure_ascii=False,indent=2)+'\n')
   print('OVERVIEW '+bid+'\n'+text,flush=True)
  browser.close();status='ok'
except Exception:traceback.print_exc()
finally:print('QB_CANDIDATES 已结束 '+datetime.datetime.now().astimezone().isoformat()+' status='+status,flush=True)
if status!='ok':raise SystemExit(1)
