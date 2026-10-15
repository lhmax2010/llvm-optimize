"""Reproducible text-only analysis of saved RPM inventories/readelf output; no RPM execution."""
from common import *
import csv,re,collections,posixpath,hashlib

def writecsv(name,rows,fields=None):
 rows=list(rows)
 if fields is None:fields=list(dict.fromkeys(k for r in rows for k in r))
 with (OUT/name).open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)

def rawrows(name):
 p=RAW/name
 return [dict(json.loads(l),evidence=f'raw/{name}:{i}') for i,l in enumerate(p.read_text().splitlines(),1)]

def elf(rec):
 if not rec or not rec.get('elf'):return None
 name=rec['readelf_file'];lines=(OUT/name).read_text().splitlines()
 needed=[];sections={};srefs={};neededrefs=[];bid='未获取';bidref='';commands=[];typ='';machine=''
 for i,line in enumerate(lines,1):
  ref=f'{name}:{i}'
  m=re.search(r'\(NEEDED\).*Shared library: \[(.+?)\]',line)
  if m:needed.append(m[1]);neededrefs.append(ref)
  m=re.match(r'\s*\[\s*\d+\]\s+(\S+)\s+(\S+)\s+([0-9a-fA-F]+)\s+([0-9a-fA-F]+)\s+([0-9a-fA-F]+)\s+',line)
  if m:sections[m[1]]=int(m[5],16);srefs[m[1]]=ref
  if 'Build ID:' in line:bid=line.split('Build ID:',1)[1].strip();bidref=ref
  if line.startswith('COMMAND:'):commands.append(ref)
  if line.strip().startswith('Type:'):typ=line.split('Type:',1)[1].strip()
  if line.strip().startswith('Machine:'):machine=line.split('Machine:',1)[1].strip()
 debug={k:v for k,v in sections.items() if k.startswith(('.debug_','.zdebug_'))}
 assert sections,(name,'no sections parsed')
 return {'needed':sorted(needed),'sections':sections,'section_evidence':srefs,'debug':debug,'symtab':'.symtab' in sections,'build_id':bid if bid!='未获取' else '未获取（readelf -n 未列出 Build ID）','build_id_evidence':bidref or ';'.join(commands),'needed_evidence':';'.join(neededrefs) or ';'.join(commands),'readelf_evidence':';'.join(commands),'type':typ,'machine':machine}

completed=[];inv={};els={};rpmrows=[]
for p in sorted(RAW.glob('*_complete.json')):
 c=json.loads(p.read_text());side,arch,pkg=c['side'],c['arch'],c['package'];key=(side,arch,pkg)
 completed.append(c);records=rawrows(p.name.replace('_complete.json','_files.jsonl'));inv[key]={r['path']:r for r in records}
 hn=p.name.replace('_complete.json','_rpm_header.txt');head={l.split('=',1)[0]:l.split('=',1)[1] for l in (RAW/hn).read_text().splitlines()}
 els.update({(side,arch,pkg,r['path']):elf(r) for r in records if r.get('elf')})
 rpmrows.append({'side':side,'snapshot':c['snapshot'],'arch':arch,'package':pkg,'rpm':c['rpm'],'url':c['url'],'sha256':c['rpm_sha256'],'rpm_bytes':c['rpm_bytes'],'version_release':head['VERSION']+'-'+head['RELEASE'],'payloadcompressor':head['PAYLOADCOMPRESSOR'],'payloadflags':head['PAYLOADFLAGS'],'rpm_header_SIZE':head['SIZE'],'rpm_header_ARCHIVESIZE':head['ARCHIVESIZE'],'regular_path_bytes':c['regular_path_bytes'],'unique_regular_bytes':c['unique_regular_bytes'],'symlink_path_bytes':c['symlink_path_bytes'],'metadata_evidence':f'raw/{p.name}:2-23','header_evidence':f'raw/{hn}:1-12','inventory_evidence':c['inventory']+':1','extraction_deleted':c['extraction_deleted']})
assert len(completed)==14, f'Need all 14 RPMs; found {len(completed)}'
assert all(not c['missing_paths'] and c['extraction_deleted'] for c in completed)
writecsv('rpm_metadata.csv',rpmrows)
# Content matching is performed only on regular bytes. Symlinks are separately matched by link text.
accel=[];amap={}
for side in ['old','new']:
 source=collections.defaultdict(list);links=collections.defaultdict(list)
 for pkg in ['clang','llvm','libllvm']:
  for r in inv[(side,'x86_64',pkg)].values():
   if r['type']=='regular':source[r['sha256']].append(r)
   elif r['type']=='symlink':links[r['link_target']].append(r)
 for r in inv[(side,'armv7l','clang-accel-x86_64-armv7l')].values():
  matches=[];method='不适用（目录或其他元数据）';value='';status='不适用'
  if r['type']=='regular':
   method='regular_file_sha256';value=r['sha256'];matches=source[value];status='原样来自' if matches else '无匹配'
  elif r['type']=='symlink':
   method='symlink_target_text_sha256';value=hashlib.sha256(r['link_target'].encode()).hexdigest();matches=links[r['link_target']];status='链接文本匹配（非文件内容匹配）' if matches else '无匹配'
  row={'side':side,'snapshot':r['snapshot'],'package':r['package'],'path':r['path'],'type':r['type'],'size':r['size'],'sha256':value,'hash_kind':method,'match_status':status,'source_matches':';'.join(m['package']+':'+m['path'] for m in matches),'inventory_evidence':r['evidence'],'source_evidence':';'.join(m['evidence'] for m in matches),'link_target':r.get('link_target','')}
  accel.append(row);amap[(side,r['path'])]=row
writecsv('clang_accel_sources.csv',accel)
writecsv('clang_accel_unmatched.csv',[r for r in accel if r['match_status']=='无匹配'],list(accel[0]))
# Raw derived hashes of symlink text preserve derivation and the source inventory line.
with (RAW/'symlink_hashes.jsonl').open('w') as f:
 for r in accel:
  if r['type']=='symlink':f.write(json.dumps(r,ensure_ascii=False)+'\n')

files=[];groups=sorted({(a,p) for s,a,p in inv});metrics={};codes=['.text','.rodata','.data.rel.ro','.eh_frame'];targets={'libLLVM.so.22.1','libclang-cpp.so.22.1'}
for arch,pkg in groups:
 old,new=inv[('old',arch,pkg)],inv[('new',arch,pkg)]
 for path in sorted(set(old)|set(new)):
  a,b=old.get(path),new.get(path);av=a['size'] if a else 0;bv=b['size'] if b else 0;delta=bv-av;tags=[]
  ae=els.get(('old',arch,pkg,path));be=els.get(('new',arch,pkg,path))
  presence='两边都有' if a and b else '仅旧有' if a else '仅新有'
  if not a:tags.append('新增文件')
  if not b:tags.append('删除文件')
  if pkg=='clang-accel-x86_64-armv7l' and ((a and amap[('old',path)]['match_status']=='无匹配') or (b and amap[('new',path)]['match_status']=='无匹配') or not(a and b)):
   tags.append('qemu-accel 打包变化')
  if ae and be:
   if (set(ae['needed'])&targets)-(set(be['needed'])&targets):tags.append('链接方式变化')
   if ae['symtab']!=be['symtab'] or set(ae['debug'])!=set(be['debug']):tags.append('strip/调试信息变化')
   if ae['needed']==be['needed'] and any(be['sections'].get(s,0)>ae['sections'].get(s,0) for s in codes):tags.append('代码节变大')
  # Mutually exclusive accounting; all overlapping flags remain available.
  order=['新增文件','删除文件','qemu-accel 打包变化','链接方式变化','strip/调试信息变化','代码节变大']
  primary=next((c for c in order if c in tags),'未分类' if delta else '大小未变')
  row={'arch':arch,'package':pkg,'path':path,'old_size':av,'new_size':bv,'delta_bytes':delta,'presence':presence,'old_type':a['type'] if a else '不存在','new_type':b['type'] if b else '不存在','old_elf':bool(ae),'new_elf':bool(be),'old_sha256':a.get('sha256') or '' if a else '', 'new_sha256':b.get('sha256') or '' if b else '', 'categories_all':';'.join(tags),'primary_category':primary,'old_evidence':a['evidence'] if a else f'raw/old_{arch}_{pkg}_files.jsonl:1 (完整列表中无该路径)','new_evidence':b['evidence'] if b else f'raw/new_{arch}_{pkg}_files.jsonl:1 (完整列表中无该路径)','old_readelf_evidence':ae['readelf_evidence'] if ae else '', 'new_readelf_evidence':be['readelf_evidence'] if be else ''}
  files.append(row)
writecsv('files_compare.csv',files)
top=[];etop=[];summary=[];cats=[];rawfacts=[]
for arch,pkg in groups:
 rows=[r for r in files if (r['arch'],r['package'])==(arch,pkg)]
 for rank,r in enumerate(sorted([r for r in rows if r['old_type']!='directory' and r['new_type']!='directory'],key=lambda r:(-r['delta_bytes'],r['path']))[:30],1):top.append(dict(rank=rank,**r))
 old=next(c for c in completed if (c['side'],c['arch'],c['package'])==('old',arch,pkg));new=next(c for c in completed if (c['side'],c['arch'],c['package'])==('new',arch,pkg))
 total=sum(r['delta_bytes'] for r in rows);regold=old['regular_path_bytes'];regnew=new['regular_path_bytes']
 sm={'arch':arch,'package':pkg,'old_rpm_bytes':old['rpm_bytes'],'new_rpm_bytes':new['rpm_bytes'],'rpm_delta_bytes':new['rpm_bytes']-old['rpm_bytes'],'old_path_bytes':sum(r['old_size'] for r in rows),'new_path_bytes':sum(r['new_size'] for r in rows),'path_delta_bytes':total,'old_regular_bytes':regold,'new_regular_bytes':regnew,'regular_delta_bytes':regnew-regold,'old_unique_regular_bytes':old['unique_regular_bytes'],'new_unique_regular_bytes':new['unique_regular_bytes'],'old_file_paths':sum(r['old_type'] not in ('directory','不存在') for r in rows),'new_file_paths':sum(r['new_type'] not in ('directory','不存在') for r in rows),'added_paths':sum(r['presence']=='仅新有' for r in rows),'removed_paths':sum(r['presence']=='仅旧有' for r in rows),'old_complete_evidence':f'raw/old_{arch}_{pkg}_complete.json:10-17','new_complete_evidence':f'raw/new_{arch}_{pkg}_complete.json:10-17'}
 rawfacts.append(dict(kind='package_summary',**sm));sm['derived_evidence']=f'raw/analysis_facts.jsonl:{len(rawfacts)}';summary.append(sm)
 for cat in ['新增文件','删除文件','qemu-accel 打包变化','链接方式变化','strip/调试信息变化','代码节变大','未分类','大小未变']:
  cr=[r for r in rows if r['primary_category']==cat];d=sum(r['delta_bytes'] for r in cr)
  c={'arch':arch,'package':pkg,'category':cat,'paths':len(cr),'net_delta_bytes':d,'package_path_delta_bytes':total,'share_percent':format(100*d/total,'.8f') if total else '不适用（分母为零）','share_exact_fraction':f'{d}/{total}' if total else '', 'old_inventory_evidence':f'raw/old_{arch}_{pkg}_files.jsonl:1','new_inventory_evidence':f'raw/new_{arch}_{pkg}_files.jsonl:1'}
  rawfacts.append(dict(kind='primary_category',**c));c['derived_evidence']=f'raw/analysis_facts.jsonl:{len(rawfacts)}';cats.append(c)
 if arch=='x86_64' and pkg in ('clang','llvm'):
  chosen=sorted([r for r in rows if r['old_elf'] or r['new_elf']],key=lambda r:(-r['delta_bytes'],r['path']))[:30]
  for rank,r in enumerate(chosen,1):etop.append(dict(selection='top_30_elf_by_delta',rank=rank,**r))
# Control: the SONAME path can be a symlink; select its resolved regular ELF and preserve link evidence.
for side in ['old','new']:
 lib=inv[(side,'x86_64','libllvm')];p='/usr/lib64/libLLVM.so.22.1';chain=[]
 while p in lib and lib[p]['type']=='symlink':
  r=lib[p];chain.append(r['evidence']);p=posixpath.normpath(posixpath.join(posixpath.dirname(p),r['link_target']))
 assert p in lib and lib[p]['elf'],('libLLVM control',side,p)
 rr=next(r for r in files if (r['arch'],r['package'],r['path'])==('x86_64','libllvm',p))
 # add a control row once; endpoint names are normally identical.
 if not any(r['package']=='libllvm' and r['path']==p for r in etop):etop.append(dict(selection='libLLVM_control',rank=1,**rr))
writecsv('package_summary.csv',summary);writecsv('top30_files.csv',top);writecsv('category_summary.csv',cats)
with (RAW/'analysis_facts.jsonl').open('w') as f:
 for r in rawfacts:f.write(json.dumps(r,ensure_ascii=False)+'\n')
edetail=[];esections=[]
for r in etop:
 for side in ['old','new']:
  key=(side,r['arch'],r['package'],r['path']);e=els.get(key);rec=inv[(side,r['arch'],r['package'])].get(r['path'])
  if e:
   row={'selection':r['selection'],'rank':r['rank'],'side':side,'arch':r['arch'],'package':r['package'],'path':r['path'],'size':rec['size'],'needed':';'.join(e['needed']),'needs_libLLVM_so_22_1':'libLLVM.so.22.1' in e['needed'],'needs_libclang_cpp_so_22_1':'libclang-cpp.so.22.1' in e['needed'],'has_symtab':e['symtab'],'has_debug_sections':bool(e['debug']),'symtab_size':e['sections'].get('.symtab',0),'debug_sections_json':json.dumps(e['debug'],sort_keys=True),'debug_bytes':sum(e['debug'].values()),'build_id':e['build_id'],'elf_type':e['type'],'machine':e['machine'],'inventory_evidence':rec['evidence'],'needed_evidence':e['needed_evidence'],'build_id_evidence':e['build_id_evidence'],'readelf_evidence':e['readelf_evidence']}
   for sec in codes:row[sec+'_bytes']=e['sections'].get(sec,0);row[sec+'_evidence']=e['section_evidence'].get(sec,e['readelf_evidence']+' (该节不存在)')
   edetail.append(row)
   for sec,size in e['sections'].items():esections.append({'side':side,'arch':r['arch'],'package':r['package'],'path':r['path'],'section':sec,'bytes':size,'evidence':e['section_evidence'][sec]})
  else:edetail.append({'selection':r['selection'],'rank':r['rank'],'side':side,'arch':r['arch'],'package':r['package'],'path':r['path'],'readelf_evidence':'未获取：该路径不存在或不是 ELF'})
writecsv('elf_detail.csv',edetail);writecsv('elf_sections.csv',esections)
# Machine-readable validation summary with references, not test cases duplicating an implementation.
validation={'rpm_count':len(completed),'all_extractions_deleted':all(c['extraction_deleted'] for c in completed),'all_header_regular_sizes_match':all(r['size']==r['rpm_header_size'] for d in inv.values() for r in d.values() if r['type']=='regular'),'all_header_sha256_match':all(r['sha256']==r['rpm_header_digest'] for d in inv.values() for r in d.values() if r['type']=='regular'),'all_readelf_exit_zero':all(re.findall(r'^EXIT: (\d+)$',(OUT/r['readelf_file']).read_text(),re.M)==['0']*4 for d in inv.values() for r in d.values() if r.get('elf')),'all_category_sums_reconcile':all(sum(c['net_delta_bytes'] for c in cats if (c['arch'],c['package'])==(s['arch'],s['package']))==s['path_delta_bytes'] for s in summary),'files_compare_rows':len(files),'elf_detail_rows':len(edetail),'regular_elf_observations':len(els),'max_individual_raw_bytes':max(p.stat().st_size for p in RAW.rglob('*') if p.is_file())}
(RAW/'validation.json').write_text(json.dumps(validation,indent=2)+'\n')
print(json.dumps(validation));print(json.dumps(summary,ensure_ascii=False,indent=2))
