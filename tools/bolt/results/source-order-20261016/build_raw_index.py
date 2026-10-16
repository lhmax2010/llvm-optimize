from pathlib import Path
import subprocess,hashlib,json,urllib.request,concurrent.futures,time
E=Path(__file__).resolve().parent;B=E.parents[2]/'llvm-optimize-bolt';pin=subprocess.check_output(['git','-C',str(B),'rev-parse','HEAD'],text=True).strip()
paths=subprocess.check_output(['git','-C',str(B),'ls-tree','-r','--name-only',pin,'--','tools/bolt/results/source-order-20261016'],text=True).splitlines()+['docs/bolt/26_source_order_parse_fix.md','docs/bolt/STATUS.md','docs/bolt/maintenance.md','patches/bolt/0005-unconditional-bolt-sources.patch','patches/bolt/0000-clang-bolt-squashed.patch','patches/bolt/draft-manifest.json']
rows=[]
for name in sorted(paths):
 data=(B/name).read_bytes();rows.append({'path':name,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'branch_url':'https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/'+name,'pin_url':'https://raw.githubusercontent.com/lhmax2010/llvm-optimize/'+pin+'/'+name})
parts=[rows[i:i+30] for i in range(0,len(rows),30)];nav='、'.join(f'[{i+12}](10_raw_links_part{i+12}.md)' for i in range(len(parts)))
for i,part in enumerate(parts,12):
 text=f'# Raw 续表：Source 顺序修复与 RPM 解析（{i}）\n\n证据钉提交：`{pin}`。包括真实 stderr、展开后 Source/Patch 清单和准备错误原件。所有条目提供分支版与固定提交版。\n\n本轮索引：{nav}。\n\n| 文件 | 分支版 | 钉提交版 | 字节 | SHA256 |\n| --- | --- | --- | ---: | --- |\n'
 for r in part:text+=f"| {r['path']} | [bolt-v4]({r['branch_url']}) | [{pin[:7]}]({r['pin_url']}) | {r['bytes']} | {r['sha256']} |\n"
 p=B/f'docs/bolt/10_raw_links_part{i}.md';p.write_text(text);assert p.stat().st_size<50000
p=B/'docs/bolt/10_raw_links.md';p.write_text(p.read_text()+f'\n\n## 2026-10-16：Source 声明顺序与跨架构解析修复\n\n{nav}；完整认证材料钉提交 `{pin}`，共 {len(rows)} 项，每项均有分支版与固定 raw。26号报告后续 sandbox 发布结论另见其末尾。\n')
def verify(task):
 r,key=task;url=r[key];last=None
 for attempt in range(3):
  try:
   with urllib.request.urlopen(url,timeout=45) as response:data=response.read()
   actual=hashlib.sha256(data).hexdigest();assert actual==r['sha256'],(url,actual,r['sha256'])
   return {'url':url,'bytes':len(data),'sha256':actual,'PASS':True}
  except Exception as exc:last=repr(exc);time.sleep(1+attempt)
 return {'url':url,'PASS':False,'error':last}
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:results=list(pool.map(verify,[(r,k) for r in rows for k in ['branch_url','pin_url']]))
report={'material_pin':pin,'files':len(rows),'URLs_checked':len(results),'PASS':all(x['PASS'] for x in results),'results':results}
(E/'raw-publication-verification.json').write_text(json.dumps(report,indent=2)+'\n');(E/'raw-index-material-pin.txt').write_text(pin+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='results'},indent=2));assert report['PASS'],[x for x in results if not x['PASS']]
