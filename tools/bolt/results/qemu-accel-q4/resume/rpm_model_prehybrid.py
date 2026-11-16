import pathlib,subprocess,json,hashlib,struct,stat,fnmatch,posixpath
W=pathlib.Path('/home/linhao/Toolchain/development/llvm-optimize')
E=pathlib.Path('/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/qemu-accel-q4/resume')
E=E/'prehybrid'
E.mkdir()
DIRS={'old':W/'temp/archive-fix-v2-final-20261009/continue-20261009/new-rpm-repo','new':W/'temp/qb-1226850-1226851/1226850/x86_64/rpms'}
PATTERNS=['/usr/bin/clang-*','/usr/bin/clang++','/usr/bin/opt','/usr/bin/lli','/usr/bin/llc','/usr/bin/llvm-*','/usr/bin/lld','/usr/bin/ld.lld','/usr/lib64/libLTO.so*','/usr/lib64/LLVMgold.so*']
def dyn(data):
 if not data.startswith(b'\x7fELF'):return None
 assert data[4:6]==b'\x02\x01'
 phoff=struct.unpack_from('<Q',data,32)[0];ents,n=struct.unpack_from('<HH',data,54)
 loads=[];dynamic=None
 for i in range(n):
  typ,flags,off,va,pa,sz,mem,align=struct.unpack_from('<IIQQQQQQ',data,phoff+i*ents)
  if typ==1:loads.append((va,off,sz))
  if typ==2:dynamic=(off,sz)
 if dynamic is None:return {'needed':[]}
 tags=[]
 for p in range(dynamic[0],sum(dynamic),16):
  tag,val=struct.unpack_from('<qQ',data,p)
  if tag==0:break
  tags.append((tag,val))
 sva=next((v for t,v in tags if t==5),None)
 if sva is None:return {'needed':[]}
 st=next(off+sva-va for va,off,sz in loads if va<=sva<va+sz)
 def txt(v):
  a=st+v;return data[a:data.index(b'\0',a)].decode()
 return {'needed':[txt(v) for t,v in tags if t==1],'soname':[txt(v) for t,v in tags if t==14],'runpath':[txt(v) for t,v in tags if t in (15,29)]}
def readexact(f,n):
 b=f.read(n)
 if len(b)!=n:raise ValueError(('short read',len(b),n))
 return b
allresults={}
for role,d in DIRS.items():
 records={};rpms=[]
 for rpm in sorted(d.glob('*.x86_64.rpm')):
  if not rpm.name.startswith(('clang-','llvm-','libllvm-','libclang-')) or any(k in rpm.name for k in ('debuginfo','debugsource','static-devel')):continue
  print(role,rpm.name,flush=True)
  raw=subprocess.check_output(['rpm','-qp','--qf','[%{FILENAMES}\t%{FILESIZES}\t%{FILEMODES}\t%{FILELINKTOS}\t%{FILEDIGESTS}\n]',str(rpm)])
  (E/(role+'-'+rpm.name+'.files.tsv')).write_bytes(raw)
  metadata={}
  for line in raw.decode().splitlines():
   path,size,mode,link,digest=line.split('\t');metadata[path]={'size':int(size),'mode':int(mode),'link':link,'header_digest':digest,'package':rpm.name}
  h=hashlib.sha256()
  with rpm.open('rb') as f:
   for block in iter(lambda:f.read(1048576),b''):h.update(block)
  rpms.append({'path':str(rpm),'size':rpm.stat().st_size,'sha256':h.hexdigest()})
  groups={};waiting=[]
  with (E/(role+'-'+rpm.name+'.cpio.stderr')).open('wb') as err:
   proc=subprocess.Popen(['rpm2cpio',str(rpm)],stdout=subprocess.PIPE,stderr=err)
   f=proc.stdout
   while True:
    hdr=readexact(f,110);assert hdr[:6] in (b'070701',b'070702')
    vals=[int(hdr[i:i+8],16) for i in range(6,110,8)]
    ino,mode,uid,gid,nlink,mtime,size,maj,minor,rmaj,rmin,namesize,check=vals
    name=readexact(f,namesize)[:-1].decode();readexact(f,(-110-namesize)%4)
    if name=='TRAILER!!!':break
    path='/'+name.removeprefix('./').lstrip('/')
    wanted=path.startswith('/usr/bin/') or (path.startswith('/usr/lib') and '.so' in path)
    if wanted:data=readexact(f,size)
    else:
     left=size
     while left:
      n=min(left,1048576);readexact(f,n);left-=n
    readexact(f,(-size)%4)
    if wanted and stat.S_ISREG(mode):
     row=dict(metadata[path]);key=(maj,minor,ino)
     if size:
      extra={'sha256':hashlib.sha256(data).hexdigest(),'elf':dyn(data)};groups[key]=extra;row.update(extra)
     else:waiting.append((path,key))
     records[path]=row
    elif wanted and stat.S_ISLNK(mode):records[path]=dict(metadata[path])
   # Drain cpio block padding before waiting.
   while f.read(1048576):pass
   assert proc.wait()==0
  for path,key in waiting:
   if records[path]['size']:
    assert key in groups,(path,key)
    records[path].update(groups[key])
  del groups
 def resolve(path):
  seen=set()
  while path in records and stat.S_ISLNK(records[path]['mode']):
   assert path not in seen;seen.add(path)
   link=records[path]['link'];path=posixpath.normpath(link if link.startswith('/') else posixpath.join(posixpath.dirname(path),link))
  return path
 seeds=sorted(p for p in records if any(fnmatch.fnmatchcase(p,pat) for pat in PATTERNS))
 selected=set(seeds);queue=list(seeds);external={}
 while queue:
  p=queue.pop();real=resolve(p)
  if real not in records:raise ValueError(('missing target',p,real))
  if real not in selected:selected.add(real);queue.append(real)
  elf=records[real].get('elf')
  if not elf:continue
  for lib in elf['needed']:
   targets=[x for x in records if x in ['/usr/lib64/'+lib,'/lib64/'+lib]]
   if not targets:external.setdefault(lib,set()).add(p);continue
   target=targets[0]
   if target not in selected:selected.add(target);queue.append(target)
 rows=[]
 clang='/usr/bin/clang-22'
 for p in sorted(selected):
  real=resolve(p);r=records[real]
  clang_alias=(p.startswith('/usr/bin/clang-') or p=='/usr/bin/clang++') and p!=clang and r.get('sha256')==records[clang].get('sha256')
  rows.append({'path':p,'resolved':real,'package':records[p]['package'],'source_bytes':r['size'],'simulated_regular_bytes':0 if clang_alias else r['size'],'clang_symlink_restored':clang_alias,'sha256':r.get('sha256'),'elf':r.get('elf')})
 # Add plain clang and the two target-triple aliases (three links per target).
 byhash={r['sha256']:r['simulated_regular_bytes'] for r in rows if r['simulated_regular_bytes'] and r['sha256']}
 result={'role':role,'rpms':rpms,'patterns':PATTERNS,'seeds':seeds,'files':rows,'external_needed':{k:sorted(v) for k,v in external.items()},'summary':{'selected_paths':len(rows),'regular_paths':sum(r['simulated_regular_bytes']>0 for r in rows),'restored_clang_links':sum(r['clang_symlink_restored'] for r in rows),'additional_links_per_target':3,'logical_regular_bytes':sum(r['simulated_regular_bytes'] for r in rows),'unique_content_bytes_before_patchelf':sum(byhash.values()),'unique_regular_contents':len(byhash)}}
 (E/(role+'-model.json')).write_text(json.dumps(result,indent=2)+'\n');allresults[role]=result
 print(result['summary'],flush=True)
old={x['path']:x for x in allresults['old']['files']};new={x['path']:x for x in allresults['new']['files']}
rows=[{'path':p,'old':old.get(p),'new':new.get(p),'delta':new.get(p,{}).get('simulated_regular_bytes',0)-old.get(p,{}).get('simulated_regular_bytes',0)} for p in sorted(old.keys()|new.keys())]
(E/'file-comparison.json').write_text(json.dumps(rows,indent=2)+'\n')
(E/'file-comparison.tsv').write_text('path\told_regular_bytes\tnew_regular_bytes\tdelta\told_package\tnew_package\n'+''.join('\t'.join(map(str,[r['path'],(r['old'] or {}).get('simulated_regular_bytes',0),(r['new'] or {}).get('simulated_regular_bytes',0),r['delta'],(r['old'] or {}).get('package','-'),(r['new'] or {}).get('package','-')]))+'\n' for r in rows))
print('TOTAL DELTA',sum(r['delta'] for r in rows))
