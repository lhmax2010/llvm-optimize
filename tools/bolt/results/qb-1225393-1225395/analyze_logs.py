from pathlib import Path
import json,re,gzip,urllib.request,xml.etree.ElementTree as ET,hashlib,difflib,subprocess
E=Path(__file__).resolve().parent;B=E.parents[3];W=B.parent/'llvm-optimize'
def save(p,d):
 p=E/p;p.parent.mkdir(parents=True,exist_ok=True)
 if not isinstance(d,str):d=json.dumps(d,indent=2,ensure_ascii=False)+'\n'
 raw=d.encode()
 if len(raw)>1048576:p=p.with_name(p.name+'.gz');raw=gzip.compress(raw,mtime=0)
 p.write_bytes(raw)
def records(p):
 with gzip.open(p,'rt') as f:
  for i,line in enumerate(f,1):
   raw=line.rstrip('\n');s=re.sub(r'^\[\s*\d+s\] ?','',raw);yield i,raw,s
def analyze(p):
 anchors=[];flags=[];warnings=[];native=[];skipped=[];counts=[];post=[]
 for i,raw,s in records(p):
  if s.startswith('TIZEN_LLVM_'):
   (warnings if s.startswith('TIZEN_LLVM_FLAGS_WARNING') else flags).append(dict(line=i,raw=raw,text=s))
  if re.match(r'^(BOLT_.*(?:PASS|OK|MISSING)|BOLT_CACHE_RELEASE|BOLT_NINJA_EXIT_0|TIZEN_HYBRID_LINK_(?:OK|SKIP)|NATIVE_ARCHIVES_(?:BEGIN|END))',s):anchors.append(dict(line=i,raw=raw,text=s))
  if s.startswith('NATIVE_') and 'SKIP' in s:skipped.append(dict(line=i,raw=raw,text=s))
  if s.startswith('BOLT_DISK_REPORT ') and '"stage": "post"' in s:post.append(dict(line=i,raw=raw,text=s))
  if s.startswith('{'):
   try:j=json.loads(s)
   except ValueError:continue
   if 'counts' in j:counts.append(dict(line=i,counts=j['counts'],raw=raw))
   if 'converted' in j and 'path' in j:native.append(dict(line=i,raw=raw,record=j))
   if any(k in j for k in ['BOLT_DEBUG_SYMBOLS_PASS','BOLT_DEBUGLINK_PASS','BOLT_STRIP_IDENTITY','planned_tasks','preflight_pass','post_gate_pass']):
    anchors.append(dict(line=i,raw=raw,text=s))
 return dict(flags=flags,warnings=warnings,anchors=anchors,counts=counts,native=native,skipped=skipped,post=post,converted=sum(r['record']['converted'] for r in native),preserved=sum(r['record']['preserved'] for r in native),archives=len(native))
allres={}
for bid,old,proj,snap in [('1225393','1223601','Tizen-Base-Toolchain','tizen-base-toolchain_20261030.061318'),('1225395','1223602','Tizen-Base-Dev','tizen-base-dev_20261030.061217')]:
 a=analyze(E.parent/'qb-1223601-1223602'/old/'x86_64/llvm.buildlog.txt.gz');b=analyze(E/bid/'x86_64/llvm.buildlog.txt.gz')
 save(f'{bid}/anchors.txt','\n'.join(f"L{r['line']}: {r['raw']}" for r in sorted(b['flags']+b['warnings']+b['anchors']+b['post']+b['skipped'],key=lambda r:r['line']))+'\n')
 save(f'{bid}/native-records.json',b['native'])
 save(f'{bid}/profile-counts.json',b['counts'])
 oldtxt='\n'.join(r['text'] for r in a['flags']);newtxt='\n'.join(r['text'] for r in b['flags']);assert oldtxt==newtxt
 # Record exact before/after anchor lines; volatile JSON statistics remain visible.
 rows=[]
 for group in ['flags','warnings','anchors','post']:
  aa=[r['text'] for r in a[group]];bb=[r['text'] for r in b[group]]
  rows.append(dict(group=group,exact_after_timestamp_removal=aa==bb,old=a[group],new=b[group]))
 save(f'{bid}/anchor-comparison.json',rows)
 save(f'{bid}/anchor-comparison.diff',''.join(difflib.unified_diff([r['text']+'\n' for r in a['anchors']+a['post']],[r['text']+'\n' for r in b['anchors']+b['post']],fromfile=old,tofile=bid)))
 assert b['converted']==3853 and b['archives']==225
 assert not b['warnings']
 assert b['preserved']==11
 tools=[];bad=[];notfound=[]
 for ln,raw,clean in records(E/bid/'x86_64/llvm.buildlog.txt.gz'):
  if clean.startswith('NATIVE_ARCHIVES_TOOLS '):tools.append(dict(line=ln,raw=raw,record=json.loads(clean.split(' ',1)[1])))
  if clean.startswith(('NATIVE_ARCHIVES_CANCELLED','NATIVE_ARCHIVES_SIGCHLD_RESET')):bad.append(dict(line=ln,raw=raw))
  if 'not found' in clean.lower():notfound.append(dict(line=ln,raw=raw,shell_error=bool(re.search(r'(?:/bin/(?:ba)?sh|(?:^|: )(?:ba)?sh:|line \d+:).*not found',clean))))
 save(f'{bid}/tools-cancel-notfound.json',dict(tools=tools,prohibited=bad,not_found=notfound))
 assert not bad and not any(x['shell_error'] for x in notfound)
 assert len(tools)==1 and set(tools[0]['record']['tool_versions'].values())=={'22.1.8'},tools
 assert set(tools[0]['record']['tool_versions'])=={'compiler','disassembler','nm'}
 assert tools[0]['record']['tool_directory'].endswith('/build/bin'),tools
 assert any(x['text'].startswith('NATIVE_ARCHIVES_END ') and x['text'].endswith('PASS 225') for x in b['anchors'])
 postgate=[x['line'] for x in b['anchors'] if x['text']=='BOLT_POST_GATE_PASS']
 assert postgate and any(x['line']>postgate[-1] for x in b['post'])

 assert [r['counts'] for r in a['counts']]==[r['counts'] for r in b['counts']]
 base=f'https://download.tizen.org/snapshots/TIZEN/Tizen/{proj}/{snap}/repos/standard/packages/'
 url=base+'repodata/repomd.xml'
 with urllib.request.urlopen(url,timeout=120) as r:xml=r.read()
 save(f'{bid}/repomd.xml',xml.decode())
 configs=[n for n in ET.fromstring(xml) if 'build' in n.get('type','')]
 assert len(configs)==1,[(n.tag,n.attrib) for n in ET.fromstring(xml)]
 loc=next(c for c in configs[0] if c.tag.endswith('location')).get('href')
 url=base+loc
 with urllib.request.urlopen(url,timeout=120) as r:data=r.read()
 raw=gzip.decompress(data) if data[:2]==b'\x1f\x8b' else data
 save(f'{bid}/build.conf',raw.decode())
 conf=dict(url=url,download_bytes=len(data),download_sha256=hashlib.sha256(data).hexdigest(),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),note='SHA measured from immutable snapshot; QB logs do not print a SHA')
 save(f'{bid}/buildconf-provenance.json',conf)
 allres[bid]=dict(old_build=old,flags_equal=True,warning_count=0,converted=b['converted'],preserved_in_converted_archives=b['preserved'],native_archives_skipped=len(b['skipped']),archive_PASS_count=b['archives'],counts=[r['counts'] for r in b['counts']],buildconf=conf)
 print(bid,json.dumps(allres[bid]),flush=True)
save('analysis-summary.json',allres)
