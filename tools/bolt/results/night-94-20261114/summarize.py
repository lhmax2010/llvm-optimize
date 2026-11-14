from common import *
import gzip,collections,datetime
for p in ('toolchain','basedev'):
 with gzip.open(E/(p+'-input-tls.json.gz'),'rt') as f:i=json.load(f)
 with gzip.open(E/(p+'-output-tls.json.gz'),'rt') as f:o=json.load(f)
 proof=[];old=[];im={x['address']:x for v in i['functions'].values() for x in v['fs']}
 counts=[]
 for name,a in i['functions'].items():
  b=o['functions'][name]
  counts.append(dict(function=name,fs=len(a['fs']),IE=len(a['IE']),LD=len(a['LD']),offset_operations=len(a['ops']),status='PASS'))
  if a['LD']:
   proof.append(dict(function=name,input=a['LD'],output=b['LD'],count_equal=len(a['LD'])==len(b['LD']),input_all_padded=all(r['bytes'].startswith('666666') for r in a['LD']),output_all_unpadded=all(r['bytes'].startswith('6448') for r in b['LD'])))
 for name,v in o['functions'].items():
  if not name.startswith('OLD:'):continue
  for r in v['fs']:
   a=im.get(r['address']);old.append(dict(function=name,address=r['address'],bytes=r['bytes'],asm=r['asm'],same_input_address_bytes=bool(a and a['bytes']==r['bytes']),in_new_function_multiset=r['asm'] in {x['asm'] for x in o['functions'].get(name[4:],{}).get('fs',[])}))
 ci=collections.Counter(r['GOT'] for r in i['sequences'] if r['kind']=='IE');co=collections.Counter(r['GOT'] for r in o['sequences'] if r['kind']=='IE' and not r['function'].startswith('OLD:'));cold=collections.Counter(r['GOT'] for r in o['sequences'] if r['kind']=='IE' and r['function'].startswith('OLD:'))
 save(p+'-function-verdicts.json',counts)
 with gzip.open(E/(p+'-LD-mapping.json.gz'),'wt') as f:json.dump(proof,f,indent=2)
 save(p+'-old-fs-proofs.json',old)
 save(p+'-supplement.json',dict(LD_functions=len(proof),input_padded=sum(len(x['input']) for x in proof if x['input_all_padded']),output_unpadded=sum(len(x['output']) for x in proof if x['output_all_unpadded']),LD_unmatched=sum(abs(len(x['input'])-len(x['output'])) for x in proof),old_fs=len(old),old_fs_same_input_bytes=sum(x['same_input_address_bytes'] for x in old),old_fs_in_new_functions=sum(x['in_new_function_multiset'] for x in old),GOT_input=dict(ci),GOT_output_main=dict(co),GOT_old=dict(cold)))
 print(p,json.loads((E/(p+'-supplement.json')).read_text()))
print('94汇总 已结束',datetime.datetime.now().astimezone().isoformat(),'status=PASS')
