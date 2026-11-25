from pathlib import Path
import json
import os
import subprocess
import sys

A=Path(__file__).resolve().parent
W=A.parents[1]
B=W.with_name(W.name+'-bolt')
PREV=W/'archive/task151'
ROOT=A/'run'
sys.path.insert(0,str(B/'tools/skills/tizen-llvm-offline-profile/scripts'))
from pgo_pair import Pipeline, STAGES, file_identity, read, save

old=PREV/'G-profiles'
out=ROOT/'G-profiles'
previous=read(PREV/'G-config/config.json')
new_revision=(A/'recipe.sha').read_text().strip()

def rebase(data):
    if isinstance(data,str):
        return data.replace(str(PREV),str(ROOT))
    if isinstance(data,list):
        return [rebase(row) for row in data]
    if isinstance(data,dict):
        return {key:rebase(value) for key,value in data.items()}
    return data

config=rebase(previous)
config['source_commit']=new_revision
assert config['training']==previous['training']
training=read(Path(config['training']))
old_instance=Pipeline(previous,old,training)
new_instance=Pipeline(config,out,training)
src=Path(config['paths']['llvm'])
git=lambda *args: subprocess.check_output(['/usr/bin/git','-C',src,*args],text=True).strip()
assert git('rev-parse','HEAD')==new_revision
assert git('diff','--name-only',previous['source_commit'],new_revision).splitlines()==[
    'packaging/llvm-static-archives-native.py','packaging/llvm.spec']
assert git('status','--porcelain','--untracked-files=no')==''
save(ROOT/'G-config/config.json',config)
old_ir=read(old/'ir-source-identity.json')
save(out/'ir-source-identity.json',old_ir)
new_source={'commit':new_revision,'tree':git('rev-parse','HEAD^{tree}'),'snapshot':config['snapshot'],
            'recipe':file_identity(src/'packaging/llvm.spec'),'gbs_config':file_identity(config['paths']['gbs_config'])}
save(out/'source-identity.json',new_source)
for name in ('clang.profdata','ir-tools.json'):
    target=out/name
    os.link(old/name,target)
    assert file_identity(target)==file_identity(old/name)
stage_receipts=[]
for stage in STAGES[:3]:
    assert old_instance.checkpoint(stage)
    receipt=read(old/(stage+'.done.json'))
    receipt['identity']=new_instance.state_digest
    for asset in receipt['artifacts']:
        path=Path(asset['path'])
        if path.parent==old:
            path=out/path.name
            if path.name=='source-identity.json':
                asset.update(path=str(path),**file_identity(path))
            else:
                assert file_identity(path)=={k:asset[k] for k in ('bytes','sha256')}
                asset['path']=str(path)
    save(out/(stage+'.done.json'),receipt)
    assert new_instance.checkpoint(stage)
    stage_receipts.append(receipt)
record={'old_identity':old_instance.state_digest,'new_identity':new_instance.state_digest,
        'old_recipe':previous['source_commit'],'pgo_source':new_source,
        'ir_source':old_ir,'stages':stage_receipts,
        'profdata':{'path':str(out/'clang.profdata'),**file_identity(out/'clang.profdata')}}
save(ROOT/'G-config/recover-g3.json',record)
print('PASS: G1–G3 artifact identities and new checkpoints')
