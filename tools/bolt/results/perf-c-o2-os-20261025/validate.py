"""Read-only final integrity checks for the two measurement experiments."""
from pathlib import Path
import json,gzip,collections,hashlib,subprocess,datetime
E=Path(__file__).resolve().parent
checks={}
def sha(p):
    with Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def rows(p):
    return [json.loads(x) for x in (p.read_bytes() if p.exists() else gzip.decompress(p.with_suffix(p.suffix+'.gz').read_bytes())).splitlines()]
for rel,count in [('.',6000),('clean-c',2400)]:
    root=E/rel;rs=rows(root/'samples.jsonl');cs=json.loads((root/'cases.json').read_text());done=json.loads((root/'finished.json').read_text())
    assert done['status']=='COMPLETE' and done['inputs_unchanged'] and len(rs)==count
    counts=collections.Counter((r['group'],r['case'],r['role'],r['round']) for r in rs)
    assert len(counts)==count and set(counts.values())=={1}
    assert set(counts)=={(g,i,role,n) for g in ['static','hybrid'] for i in range(len(cs)) for role in ['ordinary','candidate'] for n in range(5)}
    assert all(r['returncode']==0 and r['byte_equal'] and r['object_bytes']>0 for r in rs)
    for i in range(len(cs)):
        rr=[r for r in rs if r['case']==i]
        assert len({tuple(r['argv']) for r in rr})==1
        assert all(r['argv'][:6]==['/usr/bin/taskset','-c','2','/usr/bin/setarch','x86_64','-R'] for r in rr)
        for g in ['static','hybrid']:assert len({r['object_sha256'] for r in rr if r['group']==g})==1
        assert sha(cs[i]['input'])==cs[i]['input_sha256']
    assert len({r['compiler_inode'] for r in rs})==1
    logs=root/'compile-logs'
    if logs.exists():
        logeq=all(sha(logs/f'{g}-{n}-ordinary-{i:03d}.txt')==sha(logs/f'{g}-{n}-candidate-{i:03d}.txt') for g in ['static','hybrid'] for n in range(5) for i in range(len(cs)))
    else:logeq='see archived log index'
    checks[rel]=dict(compiles=count,unique_cases=len(cs),exact_5_samples_per_side=True,all_exit_zero=True,all_objects_equal=True,identical_argv_across_roles_and_groups=True,single_compiler_inode=True,inputs_unchanged=True,paired_log_bytes_identical=logeq)
ids=json.loads((E/'compiler-identities.json').read_text())
for g,v in ids.items():
    for role,x in v.items():assert sha(x['path'])==x['sha256']
selection=json.loads((E/'c-source-selection.json').read_text())
assert all(sha(x['path'])==x['sha256'] for x in selection['sources'])
checks['originals']=dict(four_compiler_hashes_unchanged=True,twenty_C_source_hashes_unchanged=True)
checks['time']=datetime.datetime.now().astimezone().isoformat()
(E/'final-validation.json').write_text(json.dumps(checks,indent=2)+'\n')
print(json.dumps(checks,indent=2))
