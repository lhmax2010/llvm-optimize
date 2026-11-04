"""Read-only attribution of all 449 prior rejected payloads; scratch-only extraction."""
from pathlib import Path
import sys,json,hashlib,stat,struct,mmap,re,collections,gzip,difflib,datetime,subprocess,traceback
from compare_rules import *
B=Path('/home/linhao/Toolchain/development/llvm-optimize-bolt');W=B.parent/'llvm-optimize';E=B/'tools/bolt/results/baseline-attribution-20261105';O=W/'temp/attribution-20261105';O.mkdir(exist_ok=False)
sys.path.append(str(B/'tools/bolt/night-launch-20261103'))
from rpm_io import manifest
from rpm_extract import extract_selected
CERT=W/'temp/debuglink-20261028/full-20261030';T=W/'temp/night-20261103/toolchain'
def save(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def sha(p):
 with Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def norm(s):return re.sub(r'\.llvm\.[0-9]+', '.llvm.<N>',s)
def emit(f,x):f.write(json.dumps(x,ensure_ascii=False)+'\n')
def ranges(a,b):
 out=[];start=None;n=min(len(a),len(b))
 for block in range(0,n,1048576):
  x,y=bytes(a[block:block+1048576]),bytes(b[block:block+1048576]);x=x[:n-block];y=y[:n-block]
  if x==y:
   if start is not None:out.append([start,block]);start=None
   continue
  for k,(u,v) in enumerate(zip(x,y),block):
   if u!=v and start is None:start=k
   if u==v and start is not None:out.append([start,k]);start=None
 if start is not None:out.append([start,n])
 if len(a)!=len(b):out.append([n,max(len(a),len(b))])
 return out
namesout=gzip.open(E/'all-changed-names.jsonl.gz','wt');auditout=gzip.open(E/'all-section-audits.jsonl.gz','wt');unknownout=gzip.open(E/'unexplained-ranges.jsonl.gz','wt')
def symrows(data,h,ss,s):
 st=bytes(ss[s['raw'][6]]['content']);fmt='<IBBHQQ' if data[4]==2 else '<IIIBBH';sz=struct.calcsize(fmt);assert s['raw'][9]==sz
 for i in range(0,s['size'],sz):
  z=struct.unpack_from(fmt,s['content'],i)
  if data[4]!=2:z=(z[0],z[3],z[4],z[5],z[1],z[2])
  end=st.find(b'\0',z[0]);assert end>=0
  yield (st[z[0]:end].decode(errors='replace'),*z[1:])
def symbols(a,ha,sa,x,b,hb,sb,y,ctx):
 aa=list(symrows(a,ha,sa,x));bb=list(symrows(b,hb,sb,y));ca=collections.Counter((norm(z[0]),*z[1:]) for z in aa);cb=collections.Counter((norm(z[0]),*z[1:]) for z in bb);changes=0
 for i in range(max(len(aa),len(bb))):
  u=aa[i] if i<len(aa) else None;v=bb[i] if i<len(bb) else None
  if u!=v:changes+=1;emit(namesout,dict(**ctx,kind='symbol',index=i,old=u,new=v,suffix_only=bool(u and v and norm(u[0])==norm(v[0]) and u[1:]==v[1:])))
 ex=[{'side':'old','symbol':list(k),'count':n} for k,n in (ca-cb).items()]+[{'side':'new','symbol':list(k),'count':n} for k,n in (cb-ca).items()]
 if ex:emit(namesout,dict(**ctx,kind='symbol-semantic-exceptions',exceptions=ex))
 return dict(suffix_only_semantic_multiset_equal=ca==cb,changed_rows=changes,exceptions=len(ex),old_count=len(aa),new_count=len(bb))
def auditelf(a,b,ctx):
 va,ha,sa=layout(a);vb,hb,sb=layout(b);out={'context':ctx,'old_sections':[s['name'] for s in sa],'new_sections':[s['name'] for s in sb],'changes':[]};out['program_headers_equal']=chunk_equal(va[ha[4]:ha[4]+ha[8]*ha[9]],vb[hb[4]:hb[4]+hb[8]*hb[9]])
 if not out['program_headers_equal']:emit(unknownout,{**ctx,'reason':'program headers changed','old_phoff':ha[4],'new_phoff':hb[4],'ranges_relative':ranges(va[ha[4]:ha[4]+ha[8]*ha[9]],vb[hb[4]:hb[4]+hb[8]*hb[9]])})
 out['header_changes']=[{'index':i,'old':u,'new':v} for i,(u,v) in enumerate(zip(ha,hb)) if u!=v]
 if [s['name'] for s in sa]!=[s['name'] for s in sb]:out['unexplained']='section names/order/count';emit(unknownout,{**ctx,'reason':out['unexplained']})
 for i,(x,y) in enumerate(zip(sa,sb)):
  same=chunk_equal(x['content'],y['content']);meta=[dict(field=k,old=u,new=v) for k,u,v in zip(('name-index','type','flags','addr','offset','size','link','info','align','entsize'),x['raw'],y['raw']) if u!=v]
  if same and not meta:continue
  n=x['name'];r=dict(section=n,old_offset=x['offset'],new_offset=y['offset'],old_size=x['size'],new_size=y['size'],equal=same,metadata=meta)
  if not same:
   if n in ('.symtab','.dynsym'):
    r.update(symbols(va,ha,sa,x,vb,hb,sb,y,{**ctx,'section':n}));r['class']='symbol-suffix-only' if r['suffix_only_semantic_multiset_equal'] else 'unexplained-symbols'
   elif n in ('.strtab','.dynstr'):
    c,d=strings(x['content']),strings(y['content']);cn=collections.Counter();dn=collections.Counter()
    for s,count in c.items():cn[norm(s)]+=count
    for s,count in d.items():dn[norm(s)]+=count
    for s in sorted(c.keys()|d.keys()):
     if c[s]!=d[s]:emit(namesout,{**ctx,'section':n,'kind':'string-count','string':s,'old_count':c[s],'new_count':d[s],'normalized':norm(s)})
    r.update(normalized_string_multisets_equal=cn==dn);r['class']='string-suffix-only' if cn==dn else 'unexplained-string-table'
   elif n in RECORDS:
    r['class']='record';r['old_strings']=dict(strings(x['content']));r['new_strings']=dict(strings(y['content']))
    if n=='.comment':
     try:r['comment_rule']=comment_changed(x['content'],y['content'])
     except AssertionError as ex:r['class']='unexplained-comment';r['error']=str(ex)
   else:r['class']='unexplained';r['ranges_relative']=ranges(x['content'],y['content']);emit(unknownout,{**ctx,**r})
  if r.get('class','').startswith('unexplained-'):emit(unknownout,{**ctx,**r,'ranges_relative':ranges(x['content'],y['content'])})
  out['changes'].append(r)
 if any(r.get('class','').startswith('unexplained') and r['section'] not in RECORDS for r in out['changes']):
  out['recorded_commands']={side:{s['name']:dict(strings(s['content'])) for s in ss if s['name'] in ('.GCC.command.line','.llvmcmd')} for side,ss in [('old',sa),('new',sb)]}
 emit(auditout,out)
 return {k:out[k] for k in ('program_headers_equal','header_changes')}|{'changed_sections':[{'section':r['section'],'class':r.get('class','metadata-only')} for r in out['changes']]}
def index_symbols(m,allm):
 data=m['body'];wide=m['name']=='/SYM64/';size=8 if wide else 4;fmt='>Q' if wide else '>I';n=struct.unpack_from(fmt,data)[0];assert size*(n+1)<=len(data);offsets=struct.unpack_from('>'+('Q' if wide else 'I')*n,data,size);ss=bytes(data[size*(n+1):]).split(b'\0');assert len(ss)>=n;targets={r['offset']:r['name'] for r in allm};return [(ss[i].decode(errors='replace'),targets.get(offsets[i],'<invalid>'),offsets[i]) for i in range(n)]
def auditfile(a,b,ctx):
 with open(a,'rb') as fa,open(b,'rb') as fb:
  with mmap.mmap(fa.fileno(),0,access=mmap.ACCESS_READ) as ma,mmap.mmap(fb.fileno(),0,access=mmap.ACCESS_READ) as mb:
   # inner scope releases every exported view before mmap.close
   error=None
   try:answer=auditdata(ma,mb,ctx)
   except Exception as ex:error=str(ex);ex.__traceback__=None
  if error:return {'unexplained_audit_error':error}
  return answer
def auditdata(a,b,ctx):
 if bytes(a[:4])==b'\x7fELF':return {'ELF':auditelf(a,b,ctx)}
 if bytes(a[:8])!=b'!<arch>\n':return {'text_or_other':True}
 aa,bb=ar_members(a),ar_members(b);r={'member_order_equal':[m['name'] for m in aa]==[m['name'] for m in bb],'members':[]};assert r['member_order_equal'],'archive names/order differ'
 for x,y in zip(aa,bb):
  mc={**ctx,'member':x['name']};equal=chunk_equal(x['body'],y['body']);z={'name':x['name'],'old_size':x['size'],'new_size':y['size'],'old_date':x['header'][16:28].decode(),'new_date':y['header'][16:28].decode(),'equal':equal}
  if not equal:
   if x['name'] in ('/','/SYM64/'):
    u,v=index_symbols(x,aa),index_symbols(y,bb);ok=len(u)==len(v) and all(norm(p[0])==norm(q[0]) and p[1]==q[1] for p,q in zip(u,v));z['index_suffix_and_target_equal']=ok;z['old_symbols']=len(u);z['new_symbols']=len(v)
    for i in range(max(len(u),len(v))):
     p=u[i] if i<len(u) else None;q=v[i] if i<len(v) else None
     if p!=q:emit(namesout,{**mc,'kind':'archive-index','index':i,'old':p,'new':q,'suffix_and_target_equal':bool(p and q and norm(p[0])==norm(q[0]) and p[1]==q[1])})
   elif bytes(x['body'][:4])==b'\x7fELF':z['ELF']=auditelf(x['body'],y['body'],mc)
   else:z['unexplained']=True;emit(unknownout,{**mc,'reason':'non-ELF archive member changed','ranges_relative':ranges(x['body'],y['body'])})
  r['members'].append(z)
 return r
rejected=json.loads((B/'tools/bolt/results/night-revalidation-20261104/T-rpm-rejected-files.json').read_text());summary=[]
try:
 rpms={};mans={}
 for side,root in [('old',CERT/'products'),('new',T/'gbs-driver/local/repos')]:
  for p in root.glob('**/*.rpm'):
   if p.name.endswith('.src.rpm'):continue
   key=subprocess.check_output(['rpm','-qp','--qf','%{NAME}\t%{ARCH}',str(p)],text=True)
   if key in rpms.get(side,{}):continue
   rpms.setdefault(side,{})[key]=p
 for key in sorted({r['package'] for r in rejected}):
  names={r['path'] for r in rejected if r['package']==key};mans[key]={}
  for side in ['old','new']:
   p=rpms[side][key];mm=manifest(p);mans[key][side]=mm;save(E/'cert-manifests'/(key.replace('\t','-')+'-'+side+'.json'),mm)
   dest=O/'payload'/key.replace('\t','-')/side
   needed={n for n in names if not (side=='new' and (W/'temp/qb-full-compare-20261105/toolchain'/key.replace('\t','-')/'old'/n).is_file())}
   if needed:extract_selected(p,needed,dest)
  for name in sorted(names):
   a=O/'payload'/key.replace('\t','-')/'old'/name;b=O/'payload'/key.replace('\t','-')/'new'/name;b=b if b.exists() else W/'temp/qb-full-compare-20261105/toolchain'/key.replace('\t','-')/'old'/name;assert sha(a)==mans[key]['old'][name]['sha256'];assert sha(b)==mans[key]['new'][name]['sha256'];ctx={'package':key,'path':name};strict=None
   try:strict=file_proof(a,b)
   except Exception as ex:strict={'classification':'FAIL','error':str(ex)}
   audit=auditfile(a,b,ctx)
   if name.endswith('AddLLVM.cmake'):
    (E/'AddLLVM.cmake.diff').write_text(''.join(difflib.unified_diff(a.read_text().splitlines(True),b.read_text().splitlines(True),fromfile=str(a),tofile=str(b))))
   summary.append({**ctx,'old':str(a),'new':str(b),'old_sha':sha(a),'new_sha':sha(b),'strict':strict,'audit':audit});print('ATTRIBUTION',key,name,strict['classification'],flush=True)
  save(E/'attribution-files.json',summary)
 save(E/'item3-audit-result.json',{'status':'ok','audited':len(summary),'requested':len(rejected)})
except BaseException as ex:
 save(E/'item3-audit-result.json',{'status':'stopped','reason':str(ex),'audited':len(summary),'requested':len(rejected)});traceback.print_exc();raise
finally:
 namesout.close();auditout.close();unknownout.close();line='ATTRIBUTION_AUDIT 已结束 '+datetime.datetime.now().astimezone().isoformat()+' '+json.dumps(json.loads((E/'item3-audit-result.json').read_text()));(E/'item3-audit-end.txt').write_text(line+'\n');print(line,flush=True)
