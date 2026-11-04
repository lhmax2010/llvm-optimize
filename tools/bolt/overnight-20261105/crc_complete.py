from pathlib import Path
import json,mmap,datetime
from compare_rules import link_info,crc_file
B=Path('/home/linhao/Toolchain/development/llvm-optimize-bolt');W=B.parent/'llvm-optimize';E=B/'tools/bolt/results/baseline-attribution-20261105';O=W/'temp/attribution-20261105';rows=json.loads((E/'cert-debuglink-recheck.json').read_text());mans={}
for p in (E/'cert-manifests').glob('*-old.json'):
 k=p.name.removesuffix('-old.json');mans[k]={s:json.loads(p.with_name(k+'-'+s+'.json').read_text()) for s in ['old','new']}
out=[]
for r in rows:
 z={k:r[k] for k in ['package','path']}
 for side in ['old','new']:
  with open(r[side],'rb') as f:
   with mmap.mmap(f.fileno(),0,access=mmap.ACCESS_READ) as m:q=link_info(m)
  n=str(Path('usr/lib/debug')/Path(r['path']).parent/q['filename']);k=next(k for k in mans if n in mans[k][side]);poss=[O/'payload'/k/side/n,O/'debuglink-extra'/k/side/n]
  if side=='new':poss.append(W/'temp/qb-full-compare-20261105/toolchain'/k/'old'/n)
  symbol=next(p for p in poss if p.exists());actual=crc_file(symbol);z[side]={'filename':q['filename'],'stored_crc':q['crc32'],'actual_crc':actual,'symbol':str(symbol),'PASS':actual==q['crc32'],'prefix':q['prefix'].hex()}
 z['both_crc_match']=z['old']['PASS'] and z['new']['PASS'];z['filename_padding_equal']=z['old']['prefix']==z['new']['prefix'];out.append(z)
(E/'cert-all-crc.json').write_text(json.dumps(out,indent=2)+'\n');print('ALL_CRC 已结束',datetime.datetime.now().astimezone().isoformat(),'status=ok checked='+str(len(out))+' matched='+str(sum(x['both_crc_match'] and x['filename_padding_equal'] for x in out)),flush=True)
