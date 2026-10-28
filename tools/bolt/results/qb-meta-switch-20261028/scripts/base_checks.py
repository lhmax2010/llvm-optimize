from pathlib import Path
import json,re,collections,subprocess
W=Path('/home/linhao/Toolchain/development/llvm-optimize');B=W.parent/'llvm-optimize-bolt';E=B/'tools/bolt/results/qb-meta-switch-20261028';P=B/'tools/bolt/results/qb-fail-20261028/meta/buildconf';D=Path(__file__).resolve().parent
old=json.loads((E/'repos/toolchain/packages-all.json').read_text());new=json.loads((E/'repos/base/packages-all.json').read_text());cov=json.loads((P/'project-spec-coverage.json').read_text());usage={r['file']:r for r in json.loads((P/'spec-macro-usage.json').read_text())};specs={}
for r in cov:
 if not r['qb_commit']:continue
 rows=sorted(r['exact_qb_commit_specs'],key=lambda s:(s['source']=='Gerrit exact QB commit',s['source']=='local immutable Git object'))
 chosen={Path(s['file']).name:s for s in rows}
 for s in chosen.values():specs[(r['project'],s['file'])]=s
allres={}
for arch in ['x86_64','armv7l','aarch64']:
 a=[r for r in old if r['arch'] in (arch,'noarch')];b=[r for r in new if r['arch'] in (arch,'noarch')];missing=sorted({r['name'] for r in a}-{r['name'] for r in b});providers=collections.defaultdict(list);newproviders=collections.defaultdict(list)
 for r in a:
  if r['name'] in missing:
   for n in {r['name'],*[p['name'] for p in r['provides']],*r['files']}:providers[n].append(r['name'])
 for r in b:
  for n in {r['name'],*[p['name'] for p in r['provides']],*r['files']}:newproviders[n].append(r['name'])
 hits=[];unresolved=[]
 for (project,file),s in specs.items():
  lines=(P/file).read_text().splitlines();mac={};conds=[];i=0;section='main'
  for line in lines:
   m=re.match(r'^\s*%(?:define|global)\s+(\w+)\s+(.+)',line)
   if m and not any(t in m[2] for t in ['%(','%{lua:']):mac[m[1]]=m[2].strip()
   m=re.match(r'^(Name|Version|Release):\s*(\S+)',line,re.I)
   if m:mac[m[1].lower()]=m[2]
  def expand(s):
   for _ in range(12):
    t=re.sub(r'%\{(\w+)\}',lambda m:mac.get(m[1],m[0]),s)
    if t==s:break
    s=t
   return s
  while i<len(lines):
   n=i+1;line=lines[i];i+=1
   if re.match(r'^\s*%if',line):conds.append(line.strip())
   elif re.match(r'^\s*%else',line):
    if conds:conds[-1]='ELSE of '+conds[-1]
   elif re.match(r'^\s*%endif',line):
    if conds:conds.pop()
   if line.startswith('%package'):section=line.strip()
   m=None if line.lstrip().startswith('#') else re.search(r'\b(BuildRequires|Requires)(?:\([^)]*\))?\s*:\s*(.*)',line,re.I)
   if not m:continue
   logical=line
   while logical.endswith('\\') and i<len(lines):logical=logical[:-1]+lines[i];i+=1
   expanded=expand(logical);found=[]
   for cap,pkgs in providers.items():
    if re.search(r'(?<![A-Za-z0-9_+./-])'+re.escape(cap)+r'(?![A-Za-z0-9_+./-])',expanded):
     found.append(dict(capability=cap,removed_packages=sorted(set(pkgs)),alternative_name_providers=sorted(set(newproviders.get(cap,[])))))
   if found:hits.append(dict(project=project,file=file,line=n,kind=m[1],raw=logical,expanded=expanded,conditions=list(conds),section=section,matches=found))
   if '%{' in expanded or '%(' in expanded:unresolved.append(dict(project=project,file=file,line=n,text=expanded))
 # Actual binary requirements cross-check, preserving versions.
 binaryhits=[]
 for r in a:
  for req in r['requires']:
   if req['name'] in providers:binaryhits.append(dict(package=r['name'],arch=r['arch'],requirement=req,removed_providers=sorted(set(providers[req['name']])),new_name_providers=sorted(set(newproviders.get(req['name'],[])))))
 allres[arch]=dict(missing_packages=missing,spec_hits=hits,binary_requires_hits=binaryhits,unresolved_dependency_lines=unresolved)
 print(arch,'removed',missing,'spec hit lines',len(hits),'binary hit count',len(binaryhits),flush=True)
(E/'base-missing-dependencies.json').write_text(json.dumps(allres,indent=2,ensure_ascii=False)+'\n')
# Use the installed libbuild parser to evaluate architecture conditions and macros, without executing any spec.
perl='my $c=Build::read_config_dist($ARGV[0],$ARGV[1],"/usr/lib/build/configs"); print JSON::PP->new->canonical->pretty->encode({map {$_=>$c->{$_}} grep {/^(preinstall|runscripts|required|support|keep|vminstall|substitute|hostarch|target)$/} keys %$c});'
results=[]
for arch in ['x86_64','armv7l','aarch64']:
 p=E/'metadata/Tizen-Base-Toolchain/project_config';cmd=['perl','-I/usr/lib/build','-MBuild','-MJSON::PP','-e',perl,str(p),arch];r=subprocess.run(cmd,capture_output=True,text=True);assert r.returncode==0,r.stderr
 parsed=json.loads(r.stdout);(E/f'base-config-{arch}.json').write_text(r.stdout);prov=collections.defaultdict(list)
 for pkg in new:
  if pkg['arch'] not in (arch,'noarch'):continue
  for cap in {pkg['name'],*[x['name'] for x in pkg['provides']],*pkg['files']}:prov[cap].append(pkg['name']+'.'+pkg['arch'])
 for kind in ['preinstall','runscripts','required','support','keep','vminstall','substitute']:
  entries=parsed.get(kind,[])
  if kind=='substitute':entries=[(key,value) for key,values in entries.items() for value in values]
  else:entries=[(None,x) for x in entries]
  for lhs,cap in entries:
   providers=sorted(set(prov.get(cap,[])));allarch=[p['name']+'.'+p['arch'] for p in new if cap==p['name'] or any(x['name']==cap for x in p['provides'])];oldsame=[p['name']+'.'+p['arch'] for p in old if p['arch'] in (arch,'noarch') and (p['name']==cap or any(x['name']==cap for x in p['provides']))]
   results.append(dict(arch=arch,directive=kind,substitute_trigger=lhs,name=cap,providers=providers,other_arch_providers=sorted(set(allarch)-set(providers)),old_same_arch_providers=sorted(set(oldsame))))
 (E/f'base-config-{arch}.stderr').write_text(r.stderr)
(E/'base-config-providers.json').write_text(json.dumps(results,indent=2)+'\n')
print('config missing unique',sorted({r['name'] for r in results if not r['providers']}),flush=True)
