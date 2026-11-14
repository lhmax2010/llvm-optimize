import collections,datetime,gzip,json
from pathlib import Path
E=Path(__file__).resolve().parent;B=E.parents[3]
data=json.load(gzip.open(E/'toolchain-forms-full.json.gz','rt'));rows=[]
for r in data:
 for sr in r['same_sequence_supported']:
  ins=next(i for i in r['instructions'] if i['address']<=sr['offset']<i['address']+i['size'])
  rows.append({'tls_type':r['type'],'tls_offset':hex(r['offset']),'supported_offset':hex(sr['offset']),'supported_type':sr['type'],'supported_symbol':sr['symbol']['name'],'actual_instruction':ins['raw'],'location_in_instruction':sr['offset']-ins['address'],'tls_form':r['category']})
assert len(rows)==len({r['supported_offset'] for r in rows})==1951
out={'counts':[{'tls_type':t,'instruction':k,'count':n} for (t,k),n in collections.Counter((r['tls_type'],r['actual_instruction'].split('\t')[1]) for r in rows).items()],'rows':rows,'interpretation':'Passes input filtering and supported-type check; does not prove every record is registered or applied by BOLT.'}
with gzip.open(E/'supported-sequence-records.json.gz','wt') as f:json.dump(out,f,indent=2)
others=[{'offset':hex(r['offset']),'instruction':r['containing_instruction']['raw'],'symbol':r['symbol']['name']} for r in data if r['category']=='other']
(E/'other-16-instructions.json').write_text(json.dumps(others,indent=2)+'\n')
extracts=[]
for path,ranges in [(B/'tools/bolt/results/night-87-20261114/source/bolt_lib_Rewrite_RewriteInstance.cpp',[(2474,2481),(2549,2558),(2583,2597),(3024,3052)]),(E/'X86MCSymbolizer.cpp',[(52,92),(95,137),(151,173)])]:
 lines=path.read_text().splitlines();extracts.append(str(path.relative_to(B)))
 for a,z in ranges:extracts.extend(f'{n}: {lines[n-1]}' for n in range(a,z+1))
(E/'source-handling-excerpts.txt').write_text('\n'.join(extracts)+'\n')
print('92步骤1补充 已结束',datetime.datetime.now().astimezone().isoformat(),'status=待验证')
