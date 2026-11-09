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
for bid,old,proj,snap in [('1221204','1216409','Tizen-Base-Toolchain','tizen-base-toolchain_20261030.061318'),('1221207','1216410','Tizen-Base-Dev','tizen-base-dev_20261030.061217')]:
 a=analyze(E.parent/'qb-1216409-1216410'/old/'x86_64/llvm.buildlog.txt.gz');b=analyze(E/bid/'x86_64/llvm.buildlog.txt.gz')
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
 # Source payload must match the exact corresponding Git blobs.
 s=W/'temp/rebase-359934-20261106/source';proof=[]
 for side,rev in [('old','9e39fa8a61392652bb28b75fc26216675bcad1d5'),('new','7d5e28ca89ed68e3360765bc4e42234eaaabae27')]:
  p=W/'temp/qb-1221204-1221207/payload'/('toolchain' if bid=='1221204' else 'basedev')/'llvm-src'/side
  data=(p/'llvm-static-archives-native.py').read_bytes();gitdata=subprocess.check_output(['git','-C',str(s),'show',rev+':packaging/llvm-static-archives-native.py'])
  assert data==gitdata
  proof.append(dict(file='llvm-static-archives-native.py',side=side,git_revision=rev,sha256=hashlib.sha256(data).hexdigest(),git_blob_identical=True))
 oldspec=(p.parent/'old/llvm.spec').read_text();newspec=(p.parent/'new/llvm.spec').read_text()
 assert oldspec.replace('9e39fa8a61392652bb28b75fc26216675bcad1d5','7d5e28ca89ed68e3360765bc4e42234eaaabae27')==newspec
 save(f'{bid}/source-attribution.json',dict(converter=proof,spec_only_vcs_changed=True))
 allres[bid]=dict(old_build=old,flags_equal=True,warning_count=0,converted=b['converted'],preserved_in_converted_archives=b['preserved'],native_archives_skipped=len(b['skipped']),archive_PASS_count=b['archives'],counts=[r['counts'] for r in b['counts']],buildconf=conf,source_differences_fully_attributed=True)
 print(bid,json.dumps(allres[bid]),flush=True)
save('analysis-summary.json',allres)
