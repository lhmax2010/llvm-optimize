from gates import *
URL='ssh://lhmax2025@review.tizen.org:29418/platform/upstream/llvm'
SSH=['ssh','-o','BatchMode=yes','-p','29418','lhmax2025@review.tizen.org','gerrit','query','--format=JSON','--current-patch-set','--patch-sets']
ps2='d0b2e82aa90b11251a13b67d890642bf2fa6f66c';ps3='ecb2dec72ec5afde9c6c70f166e2ac12b47c093e'
assert json.loads((E/'local-gates-PASS.json').read_text())['PASS']
ls=run('before-ls-remote',['git','ls-remote',URL,'refs/heads/tizen_base','refs/heads/sandbox/lhmax2025/bolt_pgo']).decode()
remote={line.split()[1]:line.split()[0] for line in ls.splitlines()}
assert remote['refs/heads/tizen_base']=='61ef5d31ca91025c414c748477bef0c64ddfa67c',remote
assert remote['refs/heads/sandbox/lhmax2025/bolt_pgo']=='2cdd37ff747765e99c2befa3e6e8a88663ab77fe',remote
raw=run('361395-before',SSH+['change:361395'])
rows=[json.loads(l) for l in raw.splitlines() if l.strip()];changes=[r for r in rows if 'project' in r]
assert len(changes)==1,rows
c=changes[0]
assert c['project']=='platform/upstream/llvm' and c['branch']=='tizen_base' and c['status']=='NEW',c
assert c['id']=='I28171720d5bbbf9eaf491cdafc0aee0b43f9cd06',c
assert str(c['currentPatchSet']['number'])=='1' and c['currentPatchSet']['revision']=='c5244e13258bb541458dcd4a08254217d7c556a9',c
for sha,tree in [(ps2,'c23914776684bf94fdd5961f447f7c24e7bb79bc'),(ps3,'b2e8af2477cf623a945aa80bf8288a262dd4a5a9')]:
 raw=run(sha[:8]+'-identity',['git','cat-file','commit',sha])
 header,msg=raw.split(b'\n\n',1)
 assert b'tree '+tree.encode() in header.splitlines()
 assert b'parent 13c3e223d9e1b35e4affb55255c5042f8c940f35' in header.splitlines()
 assert msg==(E.parent/'resume'/('PS2-message.txt' if sha==ps2 else 'PS3-message.txt')).read_bytes()
(E/'remote-preflight-PASS.json').write_text(json.dumps({'PASS':True,'time':now(),'remote':remote,'change':c},indent=2)+'\n')
print('90步骤1 已结束',now(),'status=PASS',flush=True)
