"""Local-only release-path exceptions approved 2026-11-06; fail closed.

Line-unit decoding is derived from doc 67's classify_dwarf.py. Existing
dwarfdump output can be reused only for exact input SHAs and pinned provenance;
unknown inputs are dumped with the platform loader, not host LLVM.
"""
from pathlib import Path
import collections,gzip,hashlib,importlib.util,itertools,json,mmap,os,posixpath,re,struct,subprocess,threading,time,signal
from section_compare import layout,chunk_equal,digest
B=Path('/home/linhao/Toolchain/development/llvm-optimize-bolt')
E=B/'tools/bolt/results/tu-dwarf-20261106'
MANIFEST_SHA='95f3a2094b83a9c8d4a7e311f839d4b54397787ba32b3945855d37bfa3654c47'
PREFIX=re.compile(rb'usr/src/debug/llvm-[0-9]+\.[0-9]+\.[0-9]+-[0-9.]+\.x86_64')
CACHE={};ROWS=None
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for data in iter(lambda:f.read(1048576),b''):h.update(data)
 return h.hexdigest()
def unit(mm,start,limit):
 length=struct.unpack_from('<I',mm,start)[0];width=4;head=start+4
 if length==0xffffffff:length=struct.unpack_from('<Q',mm,start+4)[0];width=8;head=start+12
 end=head+length;assert 0<length and end<=limit,'line unit bounds'
 version=struct.unpack_from('<H',mm,head)[0];assert version in (2,3,4,5),'line version'
 hp=head+2+(2 if version==5 else 0)
 hlen=struct.unpack_from('<I' if width==4 else '<Q',mm,hp)[0];hs=hp+width;ps=hs+hlen
 assert ps<=end,'line prologue bounds'
 return dict(start=start,end=end,length=length,version=version,width=width,hlen=hlen,hs=hs,ps=ps,hp=hp,prefix=bytes(mm[head:hp]))
def line_proof(a,b,old,new):
 i=j=0;rows=[]
 while i<len(a) and j<len(b):
  u,v=unit(a,i,len(a)),unit(b,j,len(b))
  ha,hb=bytes(a[u['hs']:u['ps']]),bytes(b[v['hs']:v['ps']])
  n=ha.count(old);delta=n*(len(new)-len(old))
  assert u['width']==v['width'] and u['prefix']==v['prefix'],'line format/version prefix'
  assert ha.replace(old,new)==hb,'line directory/file/prologue bytes'
  assert chunk_equal(a[u['ps']:u['end']],b[v['ps']:v['end']]),'line program bytes'
  assert v['length']-u['length']==v['hlen']-u['hlen']==delta,'line total/prologue length increment'
  rows.append(dict(old_offset=i,new_offset=j,old_length=u['length'],new_length=v['length'],old_prologue=u['hlen'],new_prologue=v['hlen'],replacements=n,expected_delta=delta))
  i,j=u['end'],v['end']
 assert i==len(a) and j==len(b),'line unit count'
 return rows
def comp_dir(a,b,old,new):
 assert len(a.encode())==len(b.encode()),'comp_dir byte length'
 x=a.replace(old.decode(),new.decode())
 assert re.sub('/+','/',x)==re.sub('/+','/',b),'comp_dir non-slash difference'
 assert posixpath.normpath(x)==posixpath.normpath(b),'comp_dir POSIX lexical path'
 return dict(old=a,new=b,old_bytes=len(a.encode()),new_bytes=len(b.encode()))
def info_difference(a,b,old,new):
 # Same attribute name, indentation and enclosing syntax. Only its value differs.
 pattern=r'^(\s*DW_AT_comp_dir\s*\(")([^"]*)("\)\n?)$'
 x,y=re.fullmatch(pattern,a),re.fullmatch(pattern,b)
 assert x and y and x[1]==y[1] and x[3]==y[3],('non-comp_dir attribute difference',a,b)
 return comp_dir(x[2],y[2],old,new)
def normal(line,path,old,new):
 line=line.replace(old.decode(),new.decode())
 if line.startswith(str(path)+':\tfile format '):line='<INPUT>:'+line[len(str(path))+1:]
 line=re.sub(r'^(\s*)0x[0-9a-fA-F]+:',r'\1<SECTION_OFFSET>:',line)
 line=re.sub(r'(next unit at )0x[0-9a-fA-F]+',r'\1<SECTION_OFFSET>',line)
 line=re.sub(r'\b(abbr_offset|cu_offset|debug_info_offset|str_offsets_base)\s*=\s*0x[0-9a-fA-F]+',lambda m:m[1]+' = <SECTION_OFFSET>',line)
 line=re.sub(r'(DW_AT_stmt_list\s*\()0x[0-9a-fA-F]+',r'\1<SECTION_OFFSET>',line)
 line=re.sub(r'((?:strp|strx|str_offset)\s*=\s*)0x[0-9a-fA-F]+',r'\1<SECTION_OFFSET>',line)
 return line
def tool():
 t=json.loads((E/'dwarfdump-tool.json').read_text())
 assert sha(t['tool'])==t['tool_sha256'] and sha(t['loader'])==t['loader_sha256'],'platform dwarfdump identity'
 return [t['loader'],'--library-path',t['library_path'],t['tool']]
def rows():
 global ROWS
 if ROWS is None:
  p=E/'dwarf-results.json.gz';assert sha(p)==MANIFEST_SHA,'doc67 manifest changed'
  with gzip.open(p,'rt') as f:rr=json.load(f)
  ROWS={(r['old_sha'],r['new_sha']):r for r in rr}
 return ROWS
def cached_info(key,old,new):
 r=rows().get(key)
 if not r:return None
 # The pinned prior full streaming comparison covers every output line.
 # Recheck the exact input and compressed output identities before reusing it.
 outputs=[]
 for side in ('old','new'):
  d=r['dumps'][side]['debug_info'];assert d['rc']==0 and not d['timeout']
  for k in ('raw','normalized'):
   assert sha(d[k])==d[k+'_gzip_sha256'],'cached dwarfdump bytes changed'
   outputs.append(dict(path=d[k],sha256=d[k+'_gzip_sha256']))
 c=r['sections']['debug_info'];changes=[]
 if c['different_lines']:
  p=Path(c['context_file']);assert sha(p)==c['context_sha256']
  with gzip.open(p,'rt') as f:
   for line in f:
    if line.startswith('REGION '):continue
    z=json.loads(line)
    if not z['different']:continue
    assert z['old_normalized']==normal(z['old_raw'],r['old'],old,new)
    assert z['new_normalized']==normal(z['new_raw'],r['new'],old,new)
    changes.append(info_difference(z['old_raw'],z['new_raw'],old,new))
  assert len(changes)==c['different_lines'],'incomplete difference contexts'
 else:
  assert c['equal'] and r['dumps']['old']['debug_info']['normalized_text_sha256']==r['dumps']['new']['debug_info']['normalized_text_sha256']
 return dict(method='SHA-bound doc67 full-stream result and complete contexts',changes=changes,lines=c['lines_compared'],outputs=outputs,manifest_sha256=MANIFEST_SHA)
def fresh_info(a,b,old,new,out,deadline):
 argv=tool();paths=[]
 for i,p in enumerate((a,b)):
  dest=out/('info-'+str(i)+'.txt.gz');err=out/('info-'+str(i)+'.stderr')
  with err.open('wb') as ef,gzip.open(dest,'wt',compresslevel=1) as f:
   child=subprocess.Popen(argv+['--debug-info',str(p)],stdout=subprocess.PIPE,stderr=ef,text=True,start_new_session=True)
   timed=threading.Event()
   def stop():
    timed.set()
    try:os.killpg(child.pid,signal.SIGKILL)
    except ProcessLookupError:pass
   timer=threading.Timer(max(.01,deadline-time.monotonic()),stop);timer.start()
   try:
    for line in child.stdout:f.write(line)
    rc=child.wait()
   finally:timer.cancel();child.stdout.close()
   if timed.is_set():raise TimeoutError('dwarfdump per-file 30-minute limit')
   assert rc==0 and not err.stat().st_size,('dwarfdump failure/warning',rc,str(err))
  paths.append(dest)
 changes=[];count=0
 with gzip.open(paths[0],'rt') as x,gzip.open(paths[1],'rt') as y:
  for count,(u,v) in enumerate(itertools.zip_longest(x,y),1):
   assert u is not None and v is not None,'DWARF line count'
   if normal(u,a,old,new)!=normal(v,b,old,new):changes.append(info_difference(u,v,old,new))
 return dict(method='fresh platform llvm-dwarfdump --debug-info streaming',changes=changes,lines=count,outputs=list(map(str,paths)),argv=argv)
def string_proof(a,b,old,new,compdirs):
 # Compare the complete string pool, including strings unused by DIEs.
 allowed={(r['old'].encode(),r['new'].encode()) for r in compdirs}
 i=j=0;changed=[]
 while i<len(a) and j<len(b):
  # mmap section memoryviews have no find(); bounded strings, not full pool copy.
  ae=i
  while ae<len(a) and a[ae]!=0:ae+=1
  be=j
  while be<len(b) and b[be]!=0:be+=1
  assert ae<len(a) and be<len(b),'unterminated debug string'
  x,y=bytes(a[i:ae]),bytes(b[j:be])
  if x!=y:
   assert x.replace(old,new)==y or (x,y) in allowed,('unapproved .debug_str change',x[:300],y[:300])
   changed.append(dict(old_offset=i,new_offset=j,old_bytes=len(x),new_bytes=len(y),old=x.decode(),new=y.decode()))
  i,j=ae+1,be+1
 assert i==len(a) and j==len(b),'debug string pool count'
 return changed
def debug_pair(a,b,output=None):
 a,b=Path(a),Path(b);key=(sha(a),sha(b))
 if key in CACHE:return CACHE[key]
 if key[0]==key[1]:return dict(classification='identical')
 outbase=Path(output or os.environ.get('DWARF_PROOF_DIR','/home/linhao/Toolchain/development/llvm-optimize/temp/dwarf-rule-20261106/proofs'))
 out=outbase/(key[0]+'-'+key[1]);out.mkdir(parents=True,exist_ok=False)
 deadline=time.monotonic()+1800
 def expired(*args):raise TimeoutError('debug-pair per-file 30-minute limit')
 previous=signal.signal(signal.SIGALRM,expired);signal.setitimer(signal.ITIMER_REAL,1800)
 try:
  with a.open('rb') as fa,b.open('rb') as fb,mmap.mmap(fa.fileno(),0,access=mmap.ACCESS_READ) as ma,mmap.mmap(fb.fileno(),0,access=mmap.ACCESS_READ) as mb:
   # All memoryviews must be released before closing maps, including failures.
   aa=bb=sa=sb=None
   try:
    aa,ha,sa=layout(ma);bb,hb,sb=layout(mb)
    assert [s['name'] for s in sa]==[s['name'] for s in sb],'section count/name/order'
    assert ma[:16]==mb[:16] and all(x==y for i,(x,y) in enumerate(zip(ha,hb)) if i!=5),'ELF header'
    assert ma[ha[4]:ha[4]+ha[8]*ha[9]]==mb[hb[4]:hb[4]+hb[8]*hb[9]],'program headers'
    ad={s['name']:s for s in sa};bd={s['name']:s for s in sb}
    assert len(ad)==len(sa),'duplicate debug section names'
    ap=set(PREFIX.findall(bytes(ad['.debug_line']['content'])));bp=set(PREFIX.findall(bytes(bd['.debug_line']['content'])))
    assert len(ap)==len(bp)==1,('ambiguous release prefix',ap,bp)
    old,new=next(iter(ap)),next(iter(bp));assert old.split(b'llvm-')[0]==new.split(b'llvm-')[0]
    allowed={'.debug_info','.debug_line','.debug_str'};structural=[];different=[]
    for x,y in zip(sa,sb):
     name=x['name'];same=chunk_equal(x['content'],y['content'])
     assert all(u==v for i,(u,v) in enumerate(zip(x['raw'],y['raw'])) if i not in (4,5)),('section metadata',name)
     if x['flags']&2:assert x['raw']==y['raw'] and same,('ALLOC metadata/content',name)
     if name not in allowed:assert x['size']==y['size'] and same,('strict section bytes',name)
     if not same:different.append(name)
     for k in ['offset','size']:
      if x[k]!=y[k]:structural.append(dict(section=name,field='sh_'+k,old=x[k],new=y[k]))
    line=line_proof(ad['.debug_line']['content'],bd['.debug_line']['content'],old,new)
    info=cached_info(key,old,new)
    if info is None:info=fresh_info(a,b,old,new,out,deadline)
    strings=string_proof(ad['.debug_str']['content'],bd['.debug_str']['content'],old,new,info['changes'])
    changed=[(x,y) for x,y in zip(sa,sb) if x['size']!=y['size']]
    for x,y in zip(sa,sb):
     if x['offset']!=y['offset']:
      assert not x['flags']&2 and any(x['offset']>=u['offset']+u['size'] and y['offset']>=v['offset']+v['size'] for u,v in changed),('unexplained offset',x['name'])
    if ha[5]!=hb[5]:assert changed,'unexplained shoff'
    if len(ma)!=len(mb):assert changed,'unexplained file size'
    # Preserve the previous opaque-gap check; zero alignment padding only.
    def gaps(buf,h,ss):
     end=0;out=[]
     spans=[(0,h[7]),(h[4],h[4]+h[8]*h[9]),(h[5],h[5]+h[10]*h[11])]+[(s['offset'],s['offset']+s['size']) for s in ss if s['type']!=8 and s['size']]
     for lo,hi in sorted(spans):
      if lo>end and any(buf[end:lo]):out.append(bytes(buf[end:lo]))
      end=max(end,hi)
     if end<len(buf) and any(buf[end:]):out.append(bytes(buf[end:]))
     return out
    assert gaps(ma,ha,sa)==gaps(mb,hb,sb),'opaque ELF bytes'
    with gzip.open(out/'line-units.json.gz','wt') as f:json.dump(line,f)
    answer=dict(classification='approved-release-path-DWARF',old_sha256=key[0],new_sha256=key[1],old_prefix=old.decode(),new_prefix=new.decode(),prefix_length_delta=len(new)-len(old),line_units=len(line),line_proof=str(out/'line-units.json.gz'),debug_info=info,debug_string_changes=strings,changed_sections=different,structural_changes=structural,old_shoff=ha[5],new_shoff=hb[5],old_bytes=len(ma),new_bytes=len(mb),all_other_sections_equal=True)
    (out/'result.json').write_text(json.dumps(answer,ensure_ascii=False,indent=2)+'\n');CACHE[key]=answer
   except BaseException as exc:
    exc.__traceback__=None
    # Local loop views may retain mappings after an assertion.
    x=y=None
    raise
   finally:
    x=y=None;ad=bd=None;sa=sb=None;aa=bb=None;changed=None
  return answer
 finally:
  signal.setitimer(signal.ITIMER_REAL,0);signal.signal(signal.SIGALRM,previous)
