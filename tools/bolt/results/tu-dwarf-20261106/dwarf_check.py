"""Streaming, read-only DWARF inspection. Never relax the recorded comparison gate."""
from pathlib import Path
import argparse,collections,datetime,gzip,hashlib,itertools,json,mmap,os,re,signal,struct,subprocess,sys,threading,time,traceback
E=Path(__file__).resolve().parent;W=Path('/home/linhao/Toolchain/development/llvm-optimize');O=W/'temp/dwarf-check-20261106'
OLD='usr/src/debug/llvm-22.1.8-1.x86_64';NEW='usr/src/debug/llvm-22.1.8-2.1.x86_64'
POSITION_KEYS=re.compile(r'\b(abbr_offset|cu_offset|debug_info_offset|str_offsets_base)\s*=\s*0x[0-9a-fA-F]+')
LEAD=re.compile(r'^(\s*)0x[0-9a-fA-F]+:')
LINE_OFFSET=re.compile(r'(debug_line\[)0x[0-9a-fA-F]+(\])')
NEXT=re.compile(r'(next unit at )0x[0-9a-fA-F]+')
STMT=re.compile(r'(DW_AT_stmt_list\s*\()0x[0-9a-fA-F]+')
STRPOS=re.compile(r'((?:strp|strx|str_offset)\s*=\s*)0x[0-9a-fA-F]+')
def normalize(line,input_path):
 line=line.replace(OLD,NEW)
 if line.startswith(str(input_path)+':\tfile format '):line='<INPUT>:'+line[len(str(input_path))+1:]
 line=LEAD.sub(r'\1<SECTION_OFFSET>:',line);line=LINE_OFFSET.sub(r'\1<SECTION_OFFSET>\2',line);line=NEXT.sub(r'\1<SECTION_OFFSET>',line)
 line=POSITION_KEYS.sub(lambda m:m[1]+' = <SECTION_OFFSET>',line);line=STMT.sub(r'\1<SECTION_OFFSET>',line);line=STRPOS.sub(r'\1<SECTION_OFFSET>',line)
 # Never remove PC/range addresses, DW_OP values, constants, line/column,
 # DW_AT_type/reference values, or length fields. Only position labels above.
 return line
def sha(p):
 with Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def layout(m):
 assert m[:6]==b'\x7fELF\x02\x01','ELF64LE required';h=struct.unpack_from('<HHIQQQIHHHHHH',m,16)
 sh=[struct.unpack_from('<IIQQQQIIQQ',m,h[5]+i*h[10]) for i in range(h[11])];x=sh[h[12]];names=m[x[4]:x[4]+x[5]]
 return [(names[x[0]:].split(b'\0',1)[0].decode(),x) for x in sh]
def digest_section(m,s):
 h=hashlib.sha256()
 if s[1]!=8:
  for i in range(s[4],s[4]+s[5],1048576):h.update(m[i:min(i+1048576,s[4]+s[5])])
 return h.hexdigest()
def sections(a,b):
 with open(a,'rb') as fa,open(b,'rb') as fb,mmap.mmap(fa.fileno(),0,access=mmap.ACCESS_READ) as ma,mmap.mmap(fb.fileno(),0,access=mmap.ACCESS_READ) as mb:
  aa,bb=layout(ma),layout(mb);names_equal=[n for n,_ in aa]==[n for n,_ in bb];rows=[]
  if names_equal:
   for (n,x),(_,y) in zip(aa,bb):
    ah,bh=digest_section(ma,x),digest_section(mb,y);rows.append({'section':n,'old_size':x[5],'new_size':y[5],'old_sha256':ah,'new_sha256':bh,'equal':ah==bh and x[5]==y[5],'permitted_section':n in {'.debug_info','.debug_line','.debug_str','.debug_aranges'}})
  return {'old_names':[n for n,_ in aa],'new_names':[n for n,_ in bb],'names_and_order_equal':names_equal,'sections':rows,'other_sections_equal':names_equal and all(x['equal'] for x in rows if not x['permitted_section'])}
def dump(binary,section,base,deadline,argv):
 raw=base.with_suffix('.raw.txt.gz');norm=base.with_suffix('.normalized.txt.gz');err=base.with_suffix('.stderr');cmd=argv+['--'+section.replace('_','-'),str(binary)]
 info={'argv':cmd,'raw':str(raw),'normalized':str(norm),'stderr':str(err)}
 # CLI section switches use underscores in LLVM's --debug-info names, formed above.
 started=time.monotonic();timed=threading.Event()
 with err.open('wb') as ef,gzip.open(raw,'wt',compresslevel=1) as rf,gzip.open(norm,'wt',compresslevel=1) as nf:
  p=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=ef,text=True,errors='replace',start_new_session=True,bufsize=1)
  def expire():
   timed.set()
   try:os.killpg(p.pid,signal.SIGKILL)
   except ProcessLookupError:pass
  timer=threading.Timer(max(.01,deadline-time.monotonic()),expire);timer.start();n=0;h=hashlib.sha256();nh=hashlib.sha256()
  try:
   for line in p.stdout:
    rf.write(line);v=normalize(line,binary);nf.write(v);h.update(line.encode());nh.update(v.encode());n+=1
   rc=p.wait(timeout=10)
  finally:timer.cancel();p.stdout.close()
 info.update(rc=rc,timeout=timed.is_set(),seconds=time.monotonic()-started,lines=n,raw_text_sha256=h.hexdigest(),normalized_text_sha256=nh.hexdigest(),raw_gzip_sha256=sha(raw),normalized_gzip_sha256=sha(norm))
 if timed.is_set():raise TimeoutError(json.dumps(info))
 if rc:raise RuntimeError(json.dumps(info))
 return info
def category(section,a,b):
 if any(k in a+b for k in ['total_length:','prologue_length:','length =']):return 'encoding-length'
 if 'DW_AT_' in a+b:return 'DWARF-attribute-value'
 if section=='debug_line':return 'line-table-field'
 return 'other-text'
def compare(a,b,section,directory):
 context=directory/(section+'.contexts.txt.gz');count=0;line_count=0;before=collections.deque(maxlen=5);active=False;after=0;regions=0;examples=[];cats=collections.Counter();sample=None
 with gzip.open(a['raw'],'rt') as ar,gzip.open(b['raw'],'rt') as br,gzip.open(a['normalized'],'rt') as an,gzip.open(b['normalized'],'rt') as bn,gzip.open(context,'wt',compresslevel=1) as out:
  def emit(z):
   out.write(json.dumps(z,ensure_ascii=False)+'\n')
   if sample is not None and len(sample)<16:sample.append(z)
  for n,t in enumerate(itertools.zip_longest(ar,br,an,bn,fillvalue=None),1):
   ra,rb,na,nb=t;different=na!=nb;z={'line':n,'different':different,'old_raw':ra,'new_raw':rb,'old_normalized':na,'new_normalized':nb};line_count=n
   if different:
    count+=1;cats[category(section,na or '',nb or '')]+=1
    if not active:
     regions+=1;out.write('REGION '+str(regions)+'\n');sample=[] if len(examples)<5 else None
     if sample is not None:examples.append(sample)
     for prior in before:emit(prior)
     active=True
    emit(z);after=5
   elif active:
    emit(z);after-=1
    if after==0:active=False;sample=None
   before.append(z)
 return {'equal':count==0,'lines_compared':line_count,'different_lines':count,'regions':regions,'categories':dict(cats),'context_file':str(context),'context_sha256':sha(context),'examples':examples,'examples_limit':'first 5 regions, first 16 lines each; complete contexts in gzip'}
def memory_events():
 try:
  cg=next(x.split(':',2)[2] for x in Path('/proc/self/cgroup').read_text().splitlines() if x.startswith('0:'))
  return dict((k,int(v)) for k,v in (line.split() for line in (Path('/sys/fs/cgroup')/cg.lstrip('/')/'memory.events').read_text().splitlines()))
 except (OSError,StopIteration):return {}
def main():
 O.mkdir(exist_ok=False);pairs=json.loads((E/'dwarf-pairs.json').read_text());tool=json.loads((E/'dwarfdump-tool.json').read_text());argv=[tool['loader'],'--library-path',tool['library_path'],tool['tool']]
 results=[];initial_events=memory_events();stop_reason=None
 try:
  for pair in pairs:
   print('DWARF_FILE START index='+str(pair['index'])+' file='+pair['path'],flush=True)
   start=time.monotonic();row={**pair,'status':'UNKNOWN','sections':{},'dumps':{}};d=O/f"{pair['index']:03d}";d.mkdir()
   try:
    assert sha(pair['old'])==pair['old_sha'];assert sha(pair['new'])==pair['new_sha']
    row['structure']=sections(pair['old'],pair['new']);targets=['debug_info','debug_line','debug_aranges']
    if '.debug_str_offsets' in row['structure']['old_names'] or '.debug_str_offsets' in row['structure']['new_names']:targets.append('debug_str_offsets')
    # Thirty minutes per input file, including all requested sections.
    for side in ['old','new']:
     deadline=time.monotonic()+1800;row['dumps'][side]={}
     for section in targets:
      row['dumps'][side][section]=dump(Path(pair[side]),section,d/(side+'-'+section),deadline,argv)
    for section in targets:row['sections'][section]=compare(row['dumps']['old'][section],row['dumps']['new'][section],section,d)
    row['status']='PASS' if row['structure']['other_sections_equal'] and all(v['equal'] for v in row['sections'].values()) else 'DIFFERENT'
   except MemoryError as ex:row['error']='MemoryError';stop_reason='MemoryError'
   except Exception as ex:row['error']=str(ex);row['traceback']=traceback.format_exc()
   events=memory_events();row['memory_events']=events
   if any(events.get(k,0)>initial_events.get(k,0) for k in ('oom','oom_kill')):row['status']='UNKNOWN';stop_reason='cgroup-OOM'
   row['seconds']=time.monotonic()-start;row['end']=datetime.datetime.now().astimezone().isoformat();results.append(row);(E/'dwarf-results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
   print('DWARF_FILE 已结束',row['end'],'status='+row['status'],'index='+str(pair['index']),'file='+pair['path'],'seconds='+str(round(row['seconds'],3)),flush=True)
   if stop_reason:break
  summary={'stop_reason':stop_reason,'total':len(pairs),'processed':len(results),'counts':dict(collections.Counter(r['status'] for r in results))}
  (E/'dwarf-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
 finally:
  status='ok' if len(results)==132 and all(r['status']=='PASS' for r in results) else 'partial'
  line='ITEM3 已结束 '+datetime.datetime.now().astimezone().isoformat()+' status='+status+' reason=streaming-DWARF-check;see-per-file-results';(E/'item3-end.txt').write_text(line+'\n');print(line,flush=True)
if __name__=='__main__':main()
