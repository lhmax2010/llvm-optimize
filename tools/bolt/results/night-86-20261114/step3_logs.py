import pathlib,gzip,re,json,hashlib
E=pathlib.Path(__file__).resolve().parent;B=E.parents[3];R=B/'tools/bolt/results'
sources=[]
for proj in ['toolchain','basedev']:
 sources.append(('74-'+proj,'local-product',R/'local-full-r6-20261111'/proj/'rewrite-bolt.log'))
 sources.append(('74-'+proj+'-build','local-product-wrapper',R/'local-full-r6-20261111'/proj/'original-build.log.gz'))
for n in ['1226850','1226851']:sources.append((n,'QB-product-saved',R/'qb-1226850-1226851'/n/'x86_64/llvm.buildlog.txt.gz'))
old=list((R/'pgo-resource-full-20261104/full/stage-D').rglob('rewrite/bolt.log'));assert len(old)==1
sources.append(('58-D','PGO-old-profile',old[0]))
for mode,name in [('instrument','bolt-instrument.log'),('optimize','bolt-optimize.log')]:sources.append(('59-'+mode,'PGO-new-profile',R/'pgo-bolt-followup-20261105/resume'/mode/name))
result=[]
for id,group,p in sources:
 matches=[]
 with (gzip.open(p,'rt',errors='replace') if p.suffix=='.gz' else p.open(errors='replace')) as f:
  for i,l in enumerate(f,1):
   if re.search(r'Failed to analyze \d+ relocations|jump past end.*replacing with nop',l):
    matches.append(dict(line=i,text=l.rstrip(),kind='relocations' if 'Failed to analyze' in l else 'nop'))
 d=dict(id=id,group=group,path=str(p),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),matches=matches,relocation_warning_lines=sum(x['kind']=='relocations' for x in matches),nop_lines=sum(x['kind']=='nop' for x in matches))
 result.append(d);print(id,'reloc',d['relocation_warning_lines'],'nop',d['nop_lines'])
 for m in matches: print(m['line'],m['text'])
(E/'bolt-warning-lines.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
