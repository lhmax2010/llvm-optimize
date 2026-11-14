from inventory import *
import pwd,stat,time,urllib.request,urllib.error
def machine():
 m={'timestamp':datetime.datetime.now().astimezone().isoformat(),'cpu_count':os.cpu_count(),
    'lscpu':run(['lscpu']),'meminfo':Path('/proc/meminfo').read_text(),'swaps':Path('/proc/swaps').read_text(),
    'df':{}}
 for path in ['/home','/var/tmp','/home/abuild']:
  p=Path(path);nearest=p
  while not nearest.exists() and nearest!=nearest.parent:nearest=nearest.parent
  m['df'][path]={'exists':p.exists(),'resolved':str(p.resolve()),'df_path':str(nearest),'df':run(['df','-B1','-P',str(nearest)]),'findmnt':run(['findmnt','-T',str(nearest),'-J'])}
 write('machine.json',m)
 commands={
  'units':['systemctl','--user','list-units','--all','--type=service','--type=scope','--no-legend','--no-pager','--plain'],
  'unit-files':['systemctl','--user','list-unit-files','--type=service','--type=timer','--no-pager'],
  'timers':['systemctl','--user','list-timers','--all','--no-pager'],
  'user-cron':['crontab','-l'],
  'system-timers':['systemctl','list-timers','--all','--no-pager'],
  'locks-kernel':['lslocks','--json'],
  'processes':['ps','-eo','pid,ppid,uid,etimes,stat,comm,args','--ww']}
 out={}
 for k,a in commands.items():
  try:out[k]=run(a)
  except OSError as ex:out[k]={'rc':None,'error':str(ex)}
 write('services-processes.json',out)
 process=[l for l in out['processes'].get('stdout','').splitlines()[1:] if re.search(r'\b(gbs|ninja|llvm-bolt|python[0-9.]*|rpmbuild)\b',l)]
 write('selected-processes.json',{'selection':'comm or command mentions gbs/ninja/llvm-bolt/python/rpmbuild; elapsed seconds included, no signals','lines':process})
 crons=[]
 paths=[Path('/etc/crontab'),Path('/etc/anacrontab')]
 for parent in ['/etc/cron.d','/etc/cron.hourly','/etc/cron.daily','/etc/cron.weekly','/etc/cron.monthly',str(Path.home()/'.config/systemd/user')]:
  p=Path(parent)
  if p.is_dir():
   for q in p.iterdir():
    try:
     st=q.lstat();crons.append({'path':str(q),'owner':st.st_uid,'mode':oct(stat.S_IMODE(st.st_mode)),'symlink':q.is_symlink(),'target':os.readlink(q) if q.is_symlink() else None})
     if q.is_file() and not q.is_symlink() and st.st_size<131072:paths.append(q)
    except OSError as ex:crons.append({'path':str(q),'error':str(ex)})
 for p in paths:
  if p.exists():
   try:crons.append({'path':str(p),'content':clean(p.read_text(errors='replace'))})
   except OSError as ex:crons.append({'path':str(p),'error':str(ex)})
 write('scheduled-config.json',crons)
 print('machine/process/timer snapshot complete',flush=True)
def discover():
 roots=[W/'temp',B/'temp'];repos=[];locks=[];errors=[];directories=[]
 skip={'BUILD-ROOTS','BUILD','BUILDROOT','gbs-root','gbs-driver','node_modules','.git','.cache','payload','rpm-bytes','objects','products','binaries'}
 for base in roots:
  if not base.exists():continue
  directories.extend(str(p) for p in base.iterdir() if p.is_dir() and not p.is_symlink())
  for root,dirs,files in os.walk(base,followlinks=False,onerror=lambda e:errors.append(str(e))):
   p=Path(root);depth=len(p.relative_to(base).parts)
   if '.git' in dirs or '.git' in files:
    repos.append(str(p));dirs[:]=[];continue
   for name in files+dirs:
    if name.endswith('.lock') or name.endswith('.lock.json') or name in ('lock','locks') or ('exclusive' in name and 'lock' in name):
     f=p/name
     try:
      s=f.lstat();rec={'path':str(f),'uid':s.st_uid,'owner':pwd.getpwuid(s.st_uid).pw_name,'mode':oct(stat.S_IMODE(s.st_mode)),'mtime':datetime.datetime.fromtimestamp(s.st_mtime).astimezone().isoformat(),'size':s.st_size,'symlink':f.is_symlink()}
      if f.is_file() and not f.is_symlink() and s.st_size<65536:rec['owner_record']=clean(f.read_text(errors='replace'))
      locks.append(rec)
     except OSError as e:locks.append({'path':str(f),'error':str(e)})
   dirs[:]=[n for n in dirs if n not in skip and depth<5 and not (p/n).is_symlink()]
 write('discovery.json',{'roots':[str(x) for x in roots],'max_depth':5,'pruned_names':sorted(skip),'repositories':repos,'directories':directories,'errors':errors})
 write('lock-files.json',{'locks':locks,'blind_spots':'bounded depth5; build trees, .git internals and inaccessible directories not scanned; no lock acquired/released','errors':errors})
 known={r['path'] for r in json.load(open(E/'llvm-workspaces.json'))}
 additional=[]
 for p in repos:
  if p in known:continue
  rec=repo(Path(p));additional.append(rec);print('repo',p,flush=True)
 write('additional-repositories.json',additional)
def rest():
 for num in (361395,361396,361397):
  for kind,path in [('detail','detail?o=DETAILED_LABELS&o=DETAILED_ACCOUNTS&o=ALL_REVISIONS&o=MESSAGES'),('comments','comments'),('reviewers','reviewers/')]:
   url='https://review.tizen.org/gerrit/changes/'+str(num)+'/'+path
   result={'url':url,'method':'GET','credential':'none (existing SSH query already succeeded; no new credentials)','time':datetime.datetime.now().astimezone().isoformat()}
   try:
    with urllib.request.urlopen(urllib.request.Request(url,headers={'Accept':'application/json'}),timeout=20) as f:
     body=f.read().decode('utf-8','replace');result.update(status=f.status,final_url=f.url,body=clean(body))
     raw=body[5:] if body.startswith(")]}'") else body
     try:result['parsed']=json.loads(clean(raw))
     except ValueError:result['state']='UNKNOWN non-JSON, no login attempted'
   except Exception as ex:result.update(state='UNKNOWN',error=clean(str(ex)))
   write('gerrit-rest-'+str(num)+'-'+kind+'.json',result)
   print('REST',num,kind,result.get('status'),result.get('state','JSON'),flush=True)
if __name__=='__main__':
 machine();discover();rest()
 print('已结束',datetime.datetime.now().astimezone().isoformat(),'step2 snapshot PASS')
