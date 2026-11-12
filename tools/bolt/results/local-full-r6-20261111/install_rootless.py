from pathlib import Path
import sys,os,json,subprocess,hashlib,datetime,re,resource,traceback,shutil
B=Path('/home/linhao/Toolchain/development/llvm-optimize-bolt');W=B.parent/'llvm-optimize';E=Path(__file__).parent/'install';C=W/'temp/local-full-r6-20261111-install/root'
sys.path.insert(0,str(B/'tools/bolt/night-launch-20261105'))
from checks import debuglink_check
from rpm_io import manifest
def save(p,x):p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def sha(p):
 with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
base=['bwrap','--unshare-user','--unshare-pid','--uid','0','--gid','0','--bind',str(C),'/','--bind',str(E),'/evidence','--proc','/proc','--dev','/dev','--chdir','/','--']
def run(name,argv,stdin=None,timeout=300):
 save(E/(name+'-command.json'),argv)
 with (E/(name+'.stdout')).open('wb') as o,(E/(name+'.stderr')).open('wb') as e:
  p=subprocess.run(argv,input=stdin.encode() if stdin is not None else None,stdout=o,stderr=e,timeout=timeout)
 save(E/(name+'-result.json'),dict(rc=p.returncode));assert p.returncode==0,(name,p.returncode)
 return (E/(name+'.stdout')).read_text()
result={};phase='identity'
try:
 z=json.loads((E.parent/'toolchain/comparison/rpm-identities.json').read_text())
 clang=Path(z['clang']['local']['path']);debug=Path(z['clang-debuginfo']['local']['path'])
 expected={n:manifest(rpm)[n]['sha256'] for n,rpm in [('usr/bin/clang-22',clang),('usr/lib/debug/usr/bin/clang-22.debug',debug)]}
 script='/bin/sh'
 install='set -eu\nulimit -c 0\n/usr/bin/rpm --dbpath /var/lib/rpm --initdb\n/usr/bin/rpm --dbpath /var/lib/rpm --noplugins --nodeps -ivh "$@"\n/usr/bin/rpm --dbpath /var/lib/rpm -q clang clang-debuginfo\n'
 phase='rpm-install';run('rpm-install',base+['/bin/sh','-c',install,'install','/rpms/'+clang.name,'/rpms/'+debug.name])
 actual={n:sha(C/n) for n in expected};assert actual==expected,dict(expected=expected,actual=actual)
 assert (C/'usr/lib/debug/usr/bin/clang-22.debug').stat().st_mode&0o777==0o644
 result['installed_sha256']=actual
 result['debuglink']=debuglink_check((C/'usr/bin/clang-22').read_bytes(),(C/'usr/lib/debug/usr/bin/clang-22.debug').read_bytes())
 save(E/'installed-identity.json',result)
 phase='lldb';text=run('lldb-auto',base+['/bin/sh','-c','ulimit -c 0; exec /usr/bin/env -u LLVM_SYMBOLIZER_PATH LLDB_DEBUGSERVER_PATH=/usr/bin/lldb-server /usr/bin/lldb --no-lldbinit --batch -s /probe/install-r6/probe.lldb'],timeout=240)
 assert '/usr/bin/clang-22 /usr/lib/debug/usr/bin/clang-22.debug' in text,'no automatically loaded symbol file'
 assert 'stop reason = signal SIGILL' in text,'expected real crash not observed'
 bt=text.split('(lldb) bt all\n',1)[1].split('(lldb) image list',1)[0];frames=[]
 for line in bt.splitlines():
  if 'frame #' not in line or 'clang-22' not in line:continue
  m=re.search(r'frame #(\d+): (0x[0-9a-fA-F]+) clang-22'+chr(96)+r'(.+)',line)
  assert m,('unnamed clang frame',line)
  name=re.sub(r' \+ \d+$','',m[3]);assert 'unnamed_symbol' not in name and name!='??'
  frames.append(dict(frame=int(m[1]),absolute=m[2],lldb_name=name))
 assert len(frames)==21,('expected 21 clang frames',len(frames))
 slide_line=[l for l in text.split('(lldb) image list -o -f -s\n',1)[1].splitlines() if '/usr/bin/clang-22' in l][0]
 slide=int(re.search(r'0x[0-9a-fA-F]+',slide_line)[0],16)
 for f in frames:f['offset']=hex(int(f['absolute'],16)-slide)
 samples=json.loads((E/'symbol-samples.json').read_text());addresses=[f['offset'] for f in frames]+[s['address'] for s in samples]
 phase='symbolizer';raw=run('symbolizer',base+['/opt/symbolizer/llvm-symbolizer','--obj=/usr/lib/debug/usr/bin/clang-22.debug','--no-inlines','--demangle'],'\n'.join(addresses)+'\n',timeout=120)
 (E/'symbolizer.stdin').write_text('\n'.join(addresses)+'\n')
 blocks=[b.splitlines() for b in raw.strip().split('\n\n')];assert len(blocks)==len(addresses)
 for f,block in zip(frames,blocks):f['symbolizer_name']=block[0];assert block[0]==f['lldb_name'],f
 for i,s in enumerate(samples):
  part=text.split('(lldb) image lookup -a '+s['address']+'\n',1)[1].split('(lldb)',1)[0]
  m=re.search(r'Summary: clang-22'+chr(96)+r'(.+)',part);assert m,('missing LLDB cold sample',s)
  name=re.sub(r' \+ \d+$','',m[1]);resolved=blocks[len(frames)+i][0];assert name==resolved and name!='??'
  s['lldb_name']=name;s['symbolizer_name']=resolved
 result.update(status='ok',clang_frames=21,named_and_cross_checked=21,frames=frames,cold_samples=samples,method='real RPM installation + LLDB in rootless bwrap namespace; no sudo; core disabled')
except BaseException as ex:
 result.update(status='UNKNOWN' if isinstance(ex,MemoryError) else 'failed',phase=phase,reason=str(ex));(E/'failure.txt').write_text(traceback.format_exc());raise
finally:
 mounts=subprocess.run(['findmnt','-rn','-o','TARGET,SOURCE,FSTYPE'],capture_output=True,text=True)
 residual=[l for l in mounts.stdout.splitlines() if str(C) in l];processes=[];blind=0
 for p in Path('/proc').glob('[0-9]*'):
  if int(p.name)==os.getpid():continue
  try:
   links={k:os.readlink(p/k) for k in ('root','cwd','exe')}
   if any(x==str(C) or x.startswith(str(C)+'/') for x in links.values()):processes.append(dict(pid=p.name,links=links))
  except PermissionError:blind+=1
  except (FileNotFoundError,ProcessLookupError):pass
 result['cleanup']=dict(findmnt_rc=mounts.returncode,mounts=residual,processes=processes,permission_blind_processes=blind,namespace_mounts='destroyed on namespace exit, host mounts unchanged')
 if residual or processes or mounts.returncode:result['status']='failed';result['cleanup_failed']=True
 save(E/'result.json',result)
 line='INSTALL_LLDB 已结束 '+datetime.datetime.now().astimezone().isoformat()+' status='+result.get('status','UNKNOWN')+' phase='+phase
 (E/'end.txt').write_text(line+'\n');print(line,flush=True)
