from pathlib import Path
import json,re,urllib.request,urllib.parse,xml.etree.ElementTree as X,hashlib,subprocess,collections
W=Path('/home/linhao/Toolchain/development/llvm-optimize');B=W.parent/'llvm-optimize-bolt';D=Path(__file__).resolve().parent;E=B/'tools/bolt/results/qb-meta-switch-20261028';M=E/'metadata'
prov=[]
def get(url,p):
 try:
  with urllib.request.urlopen(url,timeout=90) as r:data=r.read();row=dict(url=url,final_url=r.url,status=r.status)
  p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data);row.update(file=str(p.relative_to(E)),bytes=len(data),sha256=hashlib.sha256(data).hexdigest());prov.append(row);return data
 except Exception as ex:prov.append(dict(url=url,error=str(ex)));return None
urls={'unified':'https://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Unified/tizen-unified_20261027.231956/','unified-toolchain':'https://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Unified-Toolchain/tizen-unified-toolchain_20261016.052151/'}
for name,root in urls.items():
 d=E/'repos'/name;url=root+'builddata/manifest/';raw=get(url,d/'manifest-index.html')
 if raw:
  for href in re.findall(r'href="([^"]+)"',raw.decode()):
   if href.endswith('.xml'):get(urllib.parse.urljoin(url,href),d/Path(href).name)
# Resolve public reference by the build.xml snapshot identity, not the mutable alias alone.
get('https://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Unified/reference/build.xml',E/'unified-reference-build.xml')
(E/'unified-source-provenance.json').write_text(json.dumps(prov,indent=2)+'\n')
def repos(path):return {p.get('name'):dict(p.attrib) for p in X.parse(path).getroot().iter('project') if p.get('name')}
a=repos(M/'Tizen-Unified-Toolchain/manifest.xml');b=repos(M/'Tizen-Unified/manifest.xml')
rows=dict(old_count=len(a),new_count=len(b),missing=[a[k] for k in sorted(a.keys()-b.keys())],added=[b[k] for k in sorted(b.keys()-a.keys())],changed=[dict(name=k,old=a[k],new=b[k]) for k in sorted(a.keys()&b.keys()) if a[k]!=b[k]])
(E/'unified-manifest-diff.json').write_text(json.dumps(rows,indent=2)+'\n');print('manifest',len(a),len(b),'missing',len(rows['missing']),'added',len(rows['added']),'changed',len(rows['changed']),flush=True)
old=json.loads((E/'repos/unified-toolchain/packages-all.json').read_text());new=json.loads((E/'repos/unified/packages-all.json').read_text());base=json.loads((E/'repos/base/packages-all.json').read_text());results={}
for arch in ['x86_64','armv7l','aarch64']:
 o=[r for r in old if r['arch'] in (arch,'noarch')];n=[r for r in new if r['arch'] in (arch,'noarch')];union=n+[r for r in base if r['arch'] in (arch,'noarch')];missing=sorted({p['name'] for p in o}-{p['name'] for p in n});after=sorted({p['name'] for p in o}-{p['name'] for p in union});caps=collections.defaultdict(list)
 for p in o:
  if p['name'] in after:
   for cap in {p['name'],*[x['name'] for x in p['provides']],*p['files']}:caps[cap].append(p['name'])
 newcaps=collections.defaultdict(list)
 for p in union:
  for cap in {p['name'],*[x['name'] for x in p['provides']],*p['files']}:newcaps[cap].append(p['name'])
 hits=[]
 for p in o:
  for req in p['requires']:
   if req['name'] in caps:hits.append(dict(package=p['name'],requirement=req,removed_providers=sorted(set(caps[req['name']])),new_name_providers=sorted(set(newcaps.get(req['name'],[])))))
 results[arch]=dict(missing_unified_only=missing,missing_even_with_base=after,binary_requires_hits=hits)
 print(arch,'missingUnified',len(missing),'withBase',len(after),'binary requires',len(hits),flush=True)
(E/'unified-missing-dependencies.json').write_text(json.dumps(results,indent=2)+'\n')
# Standard repository guard requires _repository to be defined. Temporary parsing input only.
conf=D/'unified-project-config-for-parser.conf';conf.write_text('%define _repository standard\n'+(M/'Tizen-Unified-Toolchain/project_config').read_text())
perl='my $c=Build::read_config_dist($ARGV[0],$ARGV[1],"/usr/lib/build/configs"); print JSON::PP->new->canonical->pretty->encode({map {$_=>$c->{$_}} grep {/^(preinstall|runscripts|required|support|keep|vminstall|substitute)$/} keys %$c});';checks=[]
for arch in ['x86_64','armv7l','aarch64']:
 q=subprocess.run(['perl','-I/usr/lib/build','-MBuild','-MJSON::PP','-e',perl,str(conf),arch],capture_output=True,text=True);assert q.returncode==0,q.stderr;parsed=json.loads(q.stdout);(E/f'unified-config-{arch}.json').write_text(q.stdout);(E/f'unified-config-{arch}.stderr').write_text(q.stderr)
 candidates=[p for p in new+base if p['arch'] in (arch,'noarch')]
 for kind,entries in parsed.items():
  entries=[(k,v) for k,vals in entries.items() for v in vals] if kind=='substitute' else [(None,v) for v in entries or []]
  for lhs,cap in entries:
   providers=[p['name']+'.'+p['arch'] for p in candidates if p['name']==cap or cap in p['files'] or any(x['name']==cap for x in p['provides'])]
   checks.append(dict(arch=arch,directive=kind,substitute_trigger=lhs,name=cap,providers=providers))
(E/'unified-config-providers.json').write_text(json.dumps(checks,indent=2)+'\n');print('config missing',[(x['arch'],x['name']) for x in checks if not x['providers']],flush=True)
