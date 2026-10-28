from pathlib import Path
import json,re,collections,xml.etree.ElementTree as X
W=Path('/home/linhao/Toolchain/development/llvm-optimize');E=W.parent/'llvm-optimize-bolt/tools/bolt/results/qb-meta-switch-20261028';D=E/'second-ruling'
old=json.loads((E/'repos/unified-toolchain/packages-all.json').read_text());new=json.loads((E/'repos/unified/packages-all.json').read_text());base=json.loads((D/'base-current/packages-all.json').read_text())
oldrepos={p.get('name') for p in X.parse(E/'repos/unified-toolchain/tizen-unified-toolchain_20261016.052151_standard.xml').iter('project')};newrepos={p.get('name') for p in X.parse(D/'unified-standard.xml').iter('project')};removed=oldrepos-newrepos
new=[p for p in new if p.get('vcs','').split('#')[0] in newrepos]
caps=collections.defaultdict(list)
for p in old:
 if p.get('vcs','').split('#')[0] in removed:
  for c in set([p['name']]+[x['name'] for x in p['provides']]+p['files']):caps[c].append({k:p[k] for k in ('name','arch','ver','rel','vcs')})
patterns={c:re.compile(r'(?<![\w.+/-])'+re.escape(c)+r'(?![\w.+/-])') for c in caps}
allbr=[];hits=[];rawhits=[];scanned=[]
for prov in (D/'specs').glob('*/provenance.json'):
 row=json.loads(prov.read_text())
 for entry in row['specs']:
  p=D/entry['path'];ls=p.read_text(errors='replace').splitlines();mac={};name='';scanned.append(entry['path'])
  for i,l in enumerate(ls,1):
   m=re.match(r'\s*%(?:define|global)\s+(\w+)\s+(.+)',l)
   if m:mac[m[1]]=m[2]
   m=re.match(r'\s*(Name|Version|Release)\s*:\s*(.+)',l,re.I)
   if m:mac[m[1].lower()]=m[2]
  def expand(s):
   for _ in range(15):
    t=re.sub(r'%\{([\w]+)\}',lambda m:mac.get(m[1],m[0]),s)
    if t==s:break
    s=t
   return s
  for i,l in enumerate(ls,1):
   if l.lstrip().startswith('#'):continue
   for c in caps:
    if patterns[c].search(l):rawhits.append(dict(project=row['project'],spec=entry['path'],line=i,text=l,capability=c))
   m=re.search(r'(?i)\bBuildRequires(?:\([^)]*\))?\s*:\s*(.*)',expand(l))
   if not m:continue
   dep=m[1];j=i
   while dep.endswith('\\') and j<len(ls):dep=dep[:-1]+' '+ls[j];j+=1
   expanded=expand(dep);r=dict(project=row['project'],revision=row['revision'],spec=entry['path'],line=i,text=l,dependency=dep,expanded=expanded)
   allbr.append(r)
   for c,providers in caps.items():
    if patterns[c].search(expanded):
     alternatives={}
     for arch in ['x86_64','armv7l','aarch64']:
      alternatives[arch]=[dict(name=p['name'],arch=p['arch'],ver=p['ver'],rel=p['rel'],vcs=p.get('vcs'),source_layer='Unified' if p in new else 'Base-Toolchain') for p in new+base if p['arch'] in (arch,'noarch') and (p['name']==c or c in p['files'] or any(x['name']==c for x in p['provides']))]
     hits.append(dict(r,capability=c,removed_providers=providers,alternatives=alternatives))
for n,v in [('scanned-specs',scanned),('buildrequires-lines',allbr),('buildrequires-hits',hits),('removed-capability-text-hits',rawhits)]: (D/(n+'.json')).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
print('specs',len(scanned),'BR',len(allbr),'HITS',len(hits));print(json.dumps(hits,ensure_ascii=False,indent=2)[:5000])
