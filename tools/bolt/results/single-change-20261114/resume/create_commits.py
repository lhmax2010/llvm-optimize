import pathlib,subprocess,json,os,re,email.parser,email.policy,datetime,difflib
B=pathlib.Path('/home/linhao/Toolchain/development/llvm-optimize-bolt');E=B/'tools/bolt/results/single-change-20261114/resume'
R=pathlib.Path('/home/linhao/Toolchain/development/llvm-optimize/temp/rebase-359934-20261106/source')
N=pathlib.Path('/home/linhao/Toolchain/development/llvm-optimize/temp/single-change-20261114/source')
ids=['c5244e13258bb541458dcd4a08254217d7c556a9','bde009d1197a09f7b7b76382a0166e03c841bdb9','2cdd37ff747765e99c2befa3e6e8a88663ab77fe']
base='13c3e223d9e1b35e4affb55255c5042f8c940f35'
def run(args,cwd=R,input=None,env=None):
 p=subprocess.run(args,cwd=cwd,input=input,capture_output=True,env=env)
 with (E/'commands.jsonl').open('a') as f:f.write(json.dumps({'argv':args,'cwd':str(cwd),'rc':p.returncode},ensure_ascii=False)+'\n')
 if p.returncode:raise RuntimeError(p.stderr.decode(errors='replace'))
 return p.stdout
G=['git','-c','gc.auto=0','-c','user.name=Hao Lin','-c','user.email=hao.lin@samsung.com']
msgs=[];bodies=[];proof=[]
for i,sha in enumerate(ids,1):
 msg=run(G+['cat-file','commit',sha]).split(b'\n\n',1)[1]
 patch=(B/f'patches/rebase-359934-20261113-r8/000{i}.patch').read_bytes()
 mail=email.parser.BytesParser(policy=email.policy.default).parsebytes(patch)
 subject=re.sub(r'^\[PATCH[^\]]*\] ','',str(mail['Subject']))
 body=patch.split(b'\n\n',1)[1].split(b'\n---\n',1)[0].rstrip(b'\n')+b'\n'
 reconstructed=subject.encode()+b'\n\n'+body
 assert reconstructed==msg,(i,'r8-message-mismatch')
 text=msg.decode();parts=text.rstrip('\n').rsplit('\n\n',1)
 trailers=parts[1].splitlines();assert len(trailers)==2 and trailers.count('Signed-off-by: Hao Lin <hao.lin@samsung.com>')==1 and sum(re.fullmatch(r'Change-Id: I[0-9a-f]{40}', t) is not None for t in trailers)==1
 bodies.append(parts[0].split('\n\n',1)[1]);msgs.append(text)
 (E/f'original-{i:04d}-message.txt').write_bytes(msg)
 proof.append({'part':i,'r8_message_byte_equal':True,'source':sha})
trailer='Signed-off-by: Hao Lin <hao.lin@samsung.com>\nChange-Id: I28171720d5bbbf9eaf491cdafc0aee0b43f9cd06\n'
headings=['[Part 1] cmake: use hybrid LLVM linkage on x86_64','[Part 2] packaging: optimize x86_64 clang with BOLT','[Part 3] packaging: fix x86 LLVM flags and archive mode']
titles={2:'x86_64: hybrid LLVM linkage and BOLT-optimized clang',3:'x86_64: hybrid linkage, BOLT clang, fixed flags and archives'}
intro={2:'Combine hybrid LLVM linkage and the guarded BOLT clang pipeline in\none x86_64 packaging change. Preserve the reviewed implementation\nand its controls; the component descriptions below remain unchanged.',3:'Combine hybrid LLVM linkage, the guarded BOLT clang pipeline, fixed\nx86_64 flags and declared archive debug mode in one packaging change.\nPreserve the reviewed implementation and its controls; the component\ndescriptions below remain unchanged.'}
messages={}
for n in [2,3]:
 text=titles[n]+'\n\n'+intro[n]+'\n\n'+'\n\n'.join(headings[i]+'\n\n'+bodies[i] for i in range(n))+'\n\n'+trailer
 assert max(map(len,text.splitlines()))<=72
 assert text.count('Change-Id:')==1
 (E/f'PS{n}-message.txt').write_text(text);messages[n]=text
 for i in range(n):
  section=text.split(headings[i]+'\n\n',1)[1].split('\n\n'+(headings[i+1] if i+1<n else 'Signed-off-by:'),1)[0]
  diff=''.join(difflib.unified_diff(bodies[i].splitlines(True),section.splitlines(True),fromfile=f'r8-part{i+1}',tofile=f'PS{n}-part{i+1}'))
  (E/f'PS{n}-part{i+1}.diff').write_text(diff);assert not diff
assert not N.exists(),str(N)
(E/'refs-before.txt').write_bytes(run(G+['for-each-ref','--format=%(refname) %(objectname)','refs/heads']))
(E/'source-status-before.txt').write_bytes(run(G+['status','--porcelain']))
out=run(G+['worktree','add','--detach',str(N),base]);(E/'worktree-create.stdout').write_bytes(out)
raw=(E/'c5244e13-commit.txt').read_text();a=re.search(r'^author (.*) <([^>]+)> (\d+) ([+-]\d+)$',raw,re.M)
assert a[1]=='Hao Lin' and a[2]=='hao.lin@samsung.com'
env=os.environ.copy();env.update(GIT_AUTHOR_NAME=a[1],GIT_AUTHOR_EMAIL=a[2],GIT_AUTHOR_DATE='@'+a[3]+' '+a[4])
result=[]
for n,oldtree in [(2,'c23914776684bf94fdd5961f447f7c24e7bb79bc'),(3,'b2e8af2477cf623a945aa80bf8288a262dd4a5a9')]:
 sha=run(G+['commit-tree',oldtree,'-p',base],cwd=N,input=messages[n].encode(),env=env).decode().strip()
 (E/f'PS{n}-commit.txt').write_bytes(run(G+['cat-file','commit',sha],cwd=N))
 result.append({'patch_set_intent':n,'sha':sha,'tree':oldtree,'parent':base,'worktree':str(N)})
 (E/'created-commits.json').write_text(json.dumps(result,indent=2)+'\n')
run(G+['checkout','--detach',result[-1]['sha']],cwd=N)
assert run(G+['status','--porcelain'],cwd=N)==b''
assert run(G+['for-each-ref','--format=%(refname) %(objectname)','refs/heads'])==(E/'refs-before.txt').read_bytes()
assert run(G+['status','--porcelain'])==(E/'source-status-before.txt').read_bytes()
(E/'r8-body-verification.json').write_text(json.dumps(proof,indent=2)+'\n')
print(json.dumps(result,indent=2));print('89步骤1 已结束 '+datetime.datetime.now().astimezone().isoformat()+' status=PASS')
