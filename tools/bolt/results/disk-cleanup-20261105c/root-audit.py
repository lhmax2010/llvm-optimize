from pathlib import Path
import os,json,re,time
from checks import identity,mount_snapshot,process_snapshot,command,stamp
E=Path(__file__).resolve().parent;R='/home/linhao/qb_analysis'
a={'time':stamp(),'uid':os.geteuid(),'identity':identity(R),'mounts':mount_snapshot([R]),'processes':process_snapshot([R]),'mountinfo_matches':[],'mountinfo_errors':[]}
for p in Path('/proc').glob('[0-9]*/mountinfo'):
 try:
  for line in p.read_text().splitlines():
   decoded=re.sub(r'\\([0-7]{3})',lambda m:chr(int(m[1],8)),line)
   if R in decoded:a['mountinfo_matches'].append({'path':str(p),'line':line})
 except (FileNotFoundError,ProcessLookupError):pass
 except OSError as e:a['mountinfo_errors'].append(str(e))
r=command(['systemctl','list-units','--type=service','--state=active,activating,reloading,deactivating','--no-legend','--plain','--no-pager']);units=[l.split()[0] for l in r['stdout'].splitlines() if l.split()]
a['system_services_list']=r;a['system_services']=command(['systemctl','show',*units,'-p','Id','-p','ExecStart','-p','WorkingDirectory','-p','RootDirectory']) if units else {'rc':0,'stdout':''}
p=E/'services-user.json';a['user_services']=json.loads(p.read_text());a['user_services_age_seconds']=time.time()-p.stat().st_mtime
s=a['identity'];a['pass']=bool(a['uid']==0 and s.get('directory') and not s.get('symlink') and not s.get('parent_symlink') and s.get('realpath')==R and a['mounts']['rc']==0 and not a['mounts']['matches'] and not a['processes']['matches'] and not a['processes']['errors'] and not a['mountinfo_matches'] and not a['mountinfo_errors'] and r['rc']==0 and a['system_services']['rc']==0 and R not in a['system_services']['stdout'] and a['user_services']['listing']['rc']==0 and a['user_services']['show']['rc']==0 and R not in a['user_services']['show']['stdout'] and a['user_services_age_seconds']<180)
(E/'root-audit.json').write_text(json.dumps(a,ensure_ascii=False,indent=2));print('root precheck',a['pass'],'process matches',len(a['processes']['matches']),'errors',len(a['processes']['errors']),flush=True)
raise SystemExit(0 if a['pass'] else 20)
