from pathlib import Path
import collections,gzip,hashlib,importlib.util,json,mmap,os,posixpath,re,shutil,struct,time,datetime
E=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('checker',E/'dwarf_check.py');m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
rows=json.loads((E/'dwarf-results.json').read_text())
old=m.OLD.encode();new=m.NEW.encode()
def digest(mm,a,b):
 h=hashlib.sha256()
 for o in range(a,b,1048576):h.update(mm[o:min(b,o+1048576)])
 return h.hexdigest()
def unit(mm,start,limit):
 length=struct.unpack_from('<I',mm,start)[0];offset_size=4;head=start+4
 if length==0xffffffff:length=struct.unpack_from('<Q',mm,start+4)[0];offset_size=8;head=start+12
 end=head+length
 assert end<=limit and length>0
 version=struct.unpack_from('<H',mm,head)[0];hp=head+2+(2 if version==5 else 0)
 assert version in (2,3,4,5),version
 hlen=struct.unpack_from('<I' if offset_size==4 else '<Q',mm,hp)[0];hs=hp+offset_size;ps=hs+hlen
 assert ps<=end
 return dict(start=start,end=end,length=length,version=version,offset_size=offset_size,hlen=hlen,hs=hs,ps=ps,prefix=bytes(mm[head:hp]))
out=E/'contexts';out.mkdir(exist_ok=False)
rawmanifest=[];attributes=[];context_total=0;classification=collections.Counter()
for r in rows:
 for side,dd in r['dumps'].items():
  for section,d in dd.items():
   for kind in ('raw','normalized','stderr'):
    p=Path(d[kind]);rawmanifest.append({'index':r['index'],'side':side,'section':section,'kind':kind,'path':str(p),'bytes':p.stat().st_size,'sha256':m.sha(p) if kind=='stderr' else d[kind+'_gzip_sha256']})
 for section,c in r['sections'].items():
  if c['equal']:continue
  p=Path(c['context_file']);dest=out/(f"{r['index']:03d}-"+section+'.txt.gz')
  assert m.sha(p)==c['context_sha256'];shutil.copyfile(p,dest);assert m.sha(dest)==c['context_sha256'];context_total+=dest.stat().st_size
  with gzip.open(p,'rt') as f:
   for line in f:
    if line.startswith('REGION '):continue
    z=json.loads(line)
    if not z['different']:continue
    a,b=z['old_normalized'],z['new_normalized']
    if section=='debug_line' and re.match(r'^\s*(total_length|prologue_length): 0x[0-9a-f]+\n$',a or '') and re.match(r'^\s*(total_length|prologue_length): 0x[0-9a-f]+\n$',b or ''):
     classification['line-table-encoding-length']+=1
    elif section=='debug_info' and 'DW_AT_comp_dir' in (a or '') and 'DW_AT_comp_dir' in (b or ''):
     ap=re.search(r'\("([^"]*)"\)',a)[1];bp=re.search(r'\("([^"]*)"\)',b)[1]
     attributes.append({'index':r['index'],'path':r['path'],**z,'lexical_path_equal':posixpath.normpath(ap)==posixpath.normpath(bp),'old_normalized_path':ap,'new_normalized_path':bp})
     classification['comp-dir-repeated-slash']+=1
    else:classification['UNEXPLAINED']+=1;attributes.append({'index':r['index'],'path':r['path'],**z,'UNEXPLAINED':True})
(E/'raw-dump-manifest.json').write_text(json.dumps(rawmanifest,ensure_ascii=False,indent=2)+'\n')
(E/'attribute-differences.json').write_text(json.dumps(attributes,ensure_ascii=False,indent=2)+'\n')
proof=[];units_count=0
with gzip.open(E/'line-unit-proof.jsonl.gz','wt',compresslevel=6) as evidence:
 for r in rows:
  pr={'index':r['index'],'path':r['path'],'units':0,'status':'UNKNOWN','exceptions':[]}
  try:
   with open(r['old'],'rb') as fa,open(r['new'],'rb') as fb,mmap.mmap(fa.fileno(),0,access=mmap.ACCESS_READ) as a,mmap.mmap(fb.fileno(),0,access=mmap.ACCESS_READ) as b:
    aa=dict(m.layout(a))['.debug_line'];bb=dict(m.layout(b))['.debug_line'];i,j=aa[4],bb[4];ae=i+aa[5];be=j+bb[5]
    while i<ae and j<be:
     u,v=unit(a,i,ae),unit(b,j,be);ha,hb=bytes(a[u['hs']:u['ps']]),bytes(b[v['hs']:v['ps']])
     n=ha.count(old);dh=v['hlen']-u['hlen'];dl=v['length']-u['length']
     tests={'version_equal':u['version']==v['version'],'format_equal':u['offset_size']==v['offset_size'],'prefix_equal':u['prefix']==v['prefix'],'header_after_path_replace_equal':ha.replace(old,new)==hb,'program_bytes_equal':u['end']-u['ps']==v['end']-v['ps'] and digest(a,u['ps'],u['end'])==digest(b,v['ps'],v['end']),'length_growth_equals_path_growth':dh==dl==n*(len(new)-len(old))}
     row={'index':r['index'],'unit':pr['units'],'old_section_offset':i-aa[4],'new_section_offset':j-bb[4],'old_length':u['length'],'new_length':v['length'],'old_prologue_length':u['hlen'],'new_prologue_length':v['hlen'],'path_replacements':n,'tests':tests}
     evidence.write(json.dumps(row)+'\n');pr['units']+=1;units_count+=1
     if not all(tests.values()):pr['exceptions'].append(row)
     i,j=u['end'],v['end']
    assert i==ae and j==be,'unit count/section coverage differs'
    pr['status']='PASS' if not pr['exceptions'] else 'DIFFERENT'
  except Exception as e:pr['error']=repr(e)
  proof.append(pr)
(E/'line-unit-proof-summary.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n')
summary={'classification':dict(classification),'attribute_differences':len(attributes),'attribute_files':len({x['index'] for x in attributes}),'all_comp_dirs_lexically_equal':all(x.get('lexical_path_equal',False) for x in attributes),'line_proof_counts':dict(collections.Counter(p['status'] for p in proof)),'line_units':units_count,'context_bytes':context_total,'raw_dump_bytes':sum(x['bytes'] for x in rawmanifest),'max_pair_seconds':max(r['seconds'] for r in rows),'max_input_dump_seconds':max(sum(x['seconds'] for x in r['dumps'][side].values()) for r in rows for side in ['old','new']),'nonempty_stderr':[x for x in rawmanifest if x['kind']=='stderr' and x['bytes']]}
(E/'classification-summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(summary,ensure_ascii=False,indent=2))
print('ATTRIBUTE_FILES')
for i in sorted({x['index'] for x in attributes}):print(i,rows[i]['path'],sum(x['index']==i for x in attributes))
