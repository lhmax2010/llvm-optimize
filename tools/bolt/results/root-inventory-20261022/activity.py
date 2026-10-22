#!/usr/bin/env python3
import json,subprocess,os,re,datetime
from pathlib import Path
D=Path(__file__).resolve().parent;E=Path('/home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261022-root-inventory')
units=json.loads((D/'activity-unit-paths.json').read_text());rows=(E/'lsof-complete.stdout').read_text(errors='replace').splitlines();hits={u:[] for u in units};raw=[]
for l in rows[1:]:
 matched=[u for u in units if re.search(re.escape(u)+r'(?=/|$|\s)',l)]
 if matched:
  raw.append(l)
  m=re.match(r'^(\S+)\s+(\d+)\s',l)
  if m:
   for u in matched:
    rec={'command':m[1],'pid':int(m[2])}
    if rec not in hits[u]:hits[u].append(rec)
(D/'lsof-root-matches.txt').write_text('\n'.join([rows[0]]+raw)+'\n')
(D/'activity-by-unit.json').write_text(json.dumps(hits,indent=2)+'\n')
for name,args in [('fuser-all',['fuser','-v',*units]),('ps-after',['ps','-eo','pid,ppid,uid,lstart,stat,comm']),('lslocks-after',['lslocks','-o','PID,COMMAND,TYPE,MODE,PATH']),('df-final',['df','-B1','-T'])]:
 p=subprocess.run(args,capture_output=True,text=True,timeout=120)
 (D/(name+'.stdout')).write_text(p.stdout);(D/(name+'.stderr')).write_text(p.stderr)
 (D/(name+'.json')).write_text(json.dumps({'argv':args,'rc':p.returncode,'time':datetime.datetime.now().astimezone().isoformat()},indent=2)+'\n')
locks=[]
for u in units+['/home/linhao/Toolchain/development/llvm-optimize','/home/linhao/Toolchain/development']:
 for suffix in ['.llvm-optimize-exclusive.lock','.gbs.lock','.build.lock','heavy-stage.lock']:
  p=Path(u)/suffix
  r={'path':str(p),'exists':p.exists()}
  if p.exists():
   s=p.stat();r.update({'bytes':s.st_size,'mtime':s.st_mtime})
  locks.append(r)
(D/'lock-presence.json').write_text(json.dumps(locks,indent=2)+'\n')
mounts=[];errors=0;checked=0
for p in Path('/proc').iterdir():
 if not p.name.isdigit():continue
 checked+=1
 try:txt=(p/'mountinfo').read_text()
 except OSError:errors+=1;continue
 relevant=[l for l in txt.splitlines() if ' - overlay ' in l or 'llvm-optimize' in l]
 if relevant:mounts.append({'pid':p.name,'lines':relevant})
(D/'process-mounts.json').write_text(json.dumps({'matching_processes':mounts,'unreadable_or_gone':errors,'processes_checked':checked},indent=2)+'\n')
print('lsof rows',len(raw),'roots with hits',[(k,v) for k,v in hits.items() if v],'mount pids',len(mounts),'unreadable',errors)
