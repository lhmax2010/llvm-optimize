from pathlib import Path
import re,json,difflib,collections,subprocess,gzip,ast,xml.etree.ElementTree as X
W=Path('/home/linhao/Toolchain/development/llvm-optimize');B=W.parent/'llvm-optimize-bolt';E=B/'tools/bolt/results/qb-fail-20261028/meta/buildconf';F=B/'tools/bolt/results/qb-meta-fix-and-snapshot-20261028/snapshots';R=W/'temp/qb-meta-20261028/repo'
def parse(p):
 ls=p.read_text().splitlines();out=[];inside=False;conditions=[];i=0
 while i<len(ls):
  raw=ls[i];n=i+1;s=raw.strip();i+=1
  if s=='Macros:':inside=True;continue
  if s==':Macros':inside=False;continue
  if not s or s.startswith('#'):continue
  if re.match(r'%if\b|%ifarch\b|%ifnarch\b',s):conditions.append(s);out.append(dict(line=n,category='condition',key=s,text=raw,conditions=list(conditions)));continue
  if s.startswith('%endif'):
   out.append(dict(line=n,category='condition',key='%endif',text=raw,conditions=list(conditions)))
   if conditions:conditions.pop()
   continue
  block=[raw]
  while block[-1].endswith('\\') and i<len(ls):block.append(ls[i]);i+=1
  define=re.match(r'%(?:define|global)\s+([\w]+)(?:\([^)]*\))?\s*(.*)',s)
  macro=re.match(r'%([\w]+)(?:\([^)]*\))?\s*(.*)',s)
  directive=re.match(r'([\w]+):\s*(.*)',s)
  if define:category='%define';key=define[1]
  elif inside and macro:category='Macros';key=macro[1]
  elif directive:category=directive[1].lower();key=directive[1]
  else:category='other';key=s
  out.append(dict(line=n,category=category,key=key,text='\n'.join(block),conditions=list(conditions)))
 return out
old=parse(F/'toolchain/build.conf');new=parse(F/'base/build.conf')
def identity(row):return (row['category'],row['key'],row['text'],tuple(row['conditions']))
co=collections.Counter(identity(x) for x in old);cn=collections.Counter(identity(x) for x in new)
removed=[x for x in old if co[identity(x)]>cn[identity(x)]];added=[x for x in new if cn[identity(x)]>co[identity(x)]]
changed=sorted(set(x['key'] for x in removed+added if x['category'] in ('%define','Macros')))
search=sorted(set(changed+['_toolchain_override','optflags','build_ldflags','CC','CXX','AR','RANLIB','CFLAGS','CXXFLAGS','LDFLAGS','debug_package','_enable_debug_packages']))
(E/'config-classification.json').write_text(json.dumps(dict(removed=removed,added=added,changed_macro_names=changed,indirect_search_names=search),indent=2)+'\n')
with (E/'config-classification.tsv').open('w') as f:
 f.write('side\tline\tcategory\tkey\tconditions\ttext\n')
 for side,rows in [('old-only',removed),('new-only',added)]:
  for x in rows:f.write('\t'.join([side,str(x['line']),x['category'],x['key'],';'.join(x['conditions']),x['text'].replace('\n','\\n')])+'\n')
# Full directory types/history are evidence, not a claim QB reads every file.
files=subprocess.check_output(['git','-C',str(R),'ls-files'],text=True).splitlines();counts=collections.Counter(Path(p).name for p in files)
(E/'repository-file-types.json').write_text(json.dumps(counts,indent=2)+'\n')
for label,args in [('override-name-history',['log','--all','--format=fuller','--name-status','--',' :(glob)**/*build.conf*'.strip(),':(glob)**/*config*']),('toolchain-config-diffs',['log','--format=fuller','--since=2026-10-01','-p','--','TIZEN/Tizen/Tizen-Base-Toolchain/project_config']),('tools-override-example',['show','HEAD:Tools/Tools-devbase-tools/project_config'])]:
 p=subprocess.run(['git','-C',str(R),*args],capture_output=True,text=True);(E/(label+'.txt')).write_text(p.stdout+p.stderr)
manifest=X.parse(R/'TIZEN/Tizen/Tizen-Base-Toolchain/manifest.xml');projects=[p.attrib for p in manifest.getroot().findall('project')];(E/'manifest-projects.json').write_text(json.dumps(projects,indent=2)+'\n')
for name,p in [('1202084',B/'tools/bolt/results/qb-timeout-20261021/child/1202084-full-log.txt.gz'),('1211018',B/'tools/bolt/results/qb-fail-20261028/1211014/1211018-child-full-log.txt.gz')]:
 ls=gzip.decompress(p.read_bytes()).decode(errors='replace').splitlines();rows=[]
 for i,line in enumerate(ls):
  if 'build_pkg_list_dic:' in line:
   dic=ast.literal_eval(line.split('build_pkg_list_dic:',1)[1].strip());rows.append({'line':i+1,'packages':dic})
 (E/(name+'-package-lists.json')).write_text(json.dumps(rows,indent=2)+'\n')
 select=set()
 for start,end in ([(308,350),(389,435),(508,510),(5468,5479),(5512,5517)] if name=='1211018' else [(308,350)]):select.update(range(start-1,min(end,len(ls))))
 (E/(name+'-config-flow.txt')).write_text('\n'.join(f'{i+1}: {ls[i]}' for i in sorted(select))+'\n')
print('changed macro names',changed);print('manifest projects',len(projects));print('categories',sorted(set(x['category'] for x in old+new)))
