from pathlib import Path
import urllib.request,json,gzip,hashlib,re,ast
W=Path('/home/linhao/Toolchain/development/llvm-optimize');E=W.parent/'llvm-optimize-bolt/tools/bolt/results/qb-meta-switch-20261028';D=Path(__file__).resolve().parent

def request(action,**kw):
 q=urllib.request.Request('http://127.0.0.1:18746',data=json.dumps(dict(action=action,**kw)).encode(),headers={'Content-Type':'application/json'})
 with urllib.request.urlopen(q,timeout=150) as r:return json.load(r)
prov=[]
for build in [1209720,1209725,1209726,1209727]:
 a=request('navigate',url=f'https://quickbuild.tizen.org/build/{build}/log');assert a['logged'];a=request('inspect');(D/f'qb-{build}-log-inspect.json').write_text(json.dumps(a,indent=2,ensure_ascii=False)+'\n')
 links=[x for x in a['links'] if x['text']=='Save' or 'download' in x['text'].lower() or ('download' in x['url'].lower() and 'log' in x['url'].lower())];print(build,links,flush=True)
 if not links:continue
 p=D/f'{build}-full-log.txt';meta=request('download',url=links[0]['url'],path=str(p));raw=p.read_bytes();dest=E/'qb'/f'{build}-full-log.txt.gz';dest.write_bytes(gzip.compress(raw,mtime=0));meta.update(file=str(dest.relative_to(E)),compressed_bytes=dest.stat().st_size,compressed_sha256=hashlib.sha256(dest.read_bytes()).hexdigest());prov.append(meta)
 lines=raw.decode(errors='replace').splitlines();select=set();packages=[]
 for i,line in enumerate(lines):
  if re.search(r'dod create project|DOD:|snapshot_info|dod_parent_url|USE_NGBS|repo_url:|repo_url =|buildconf|build_pkg_list_dic|create_meta_for_ngbs',line):select.update(range(max(0,i-1),min(len(lines),i+2)))
  if 'build_pkg_list_dic:' in line:
   try:packages.append({'line':i+1,'packages':ast.literal_eval(line.split('build_pkg_list_dic:',1)[1].strip())})
   except (ValueError,SyntaxError):pass
 (E/'qb'/f'{build}-excerpts.txt').write_text('\n'.join(f'{i+1}: {lines[i]}' for i in sorted(select))+'\n');(E/'qb'/f'{build}-packages.json').write_text(json.dumps(packages,indent=2)+'\n')
 print(build,'saved',len(raw),'lines',len(lines),'package lists',len(packages),flush=True)
(E/'qb/provenance.json').write_text(json.dumps(prov,indent=2)+'\n')
