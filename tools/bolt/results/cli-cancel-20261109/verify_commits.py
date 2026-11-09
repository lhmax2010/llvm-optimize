from pathlib import Path
import subprocess,json,hashlib
B=Path('/home/linhao/Toolchain/development/llvm-optimize-bolt');S=B.parent/'llvm-optimize/temp/rebase-359934-20261106/source';E=Path(__file__).parent
def g(*a):return subprocess.check_output(['git','-C',str(S),*a])
base='13c3e223d9e1b35e4affb55255c5042f8c940f35';old1='a73a7da32049569b1360e9c13d0633c168b8f173';old2='7d11ad53629ac7b670664fcbe6aee8348848d5d6';old3='5a27edb4265366781f07049ad17a3796f2e05301'
assert g('branch','--show-current').decode().strip()=='bolt-on-359934'
assert not g('status','--porcelain')
chain=g('rev-list','--reverse',base+'..HEAD').decode().splitlines();assert len(chain)==3 and chain[0]==old1
assert g('rev-parse',old1+'^{tree}').decode().strip()=='3d961cbb04f5446f84d2089b4f65f3178f2bd7fa'
d2=g('diff','--full-index',old2,chain[1]);df=g('diff','--full-index',old3,chain[2]);assert d2==df==(E/'fix.diff').read_bytes()
assert g('diff','--name-only',old3,chain[2]).decode().splitlines()==['packaging/clang-bolt-helper.py']
oldd=g('diff','--full-index',old2,old3);newd=g('diff','--full-index',chain[1],chain[2]);assert oldd==newd
assert g('show',old3+':packaging/llvm.spec')==g('show','HEAD:packaging/llvm.spec')
identities=[]
for old,new in zip([old1,old2,old3],chain):
 msg=g('show','-s','--format=%B',new).decode();title=msg.splitlines()[0];assert len(title)<=50
 trailer=msg.strip().split('\n\n')[-1].splitlines()
 assert len(trailer)==2 and {l.split(':',1)[0] for l in trailer}=={'Change-Id','Signed-off-by'},trailer
 assert 'Signed-off-by: Hao Lin <hao.lin@samsung.com>' in trailer
 parsed=subprocess.check_output(['git','interpret-trailers','--parse'],input=msg.encode()).decode();assert 'Change-Id: ' in parsed
 oldmsg=g('show','-s','--format=%B',old).decode();assert msg==oldmsg
 who=g('show','-s','--format=%an <%ae>%n%cn <%ce>',new).decode().splitlines();assert who==['Hao Lin <hao.lin@samsung.com>']*2,who
 identities.append(dict(sha=new,tree=g('rev-parse',new+'^{tree}').decode().strip(),title=title,title_length=len(title),message=msg,trailers=parsed,author=who[0],committer=who[1]))
(E/'commit-identities.json').write_text(json.dumps(identities,indent=2)+'\n')
(E/'third-commit-old.diff').write_bytes(oldd);(E/'third-commit-new.diff').write_bytes(newd)
(E/'final.diff').write_bytes(df)
result=dict(PASS=True,first_sha_tree_unchanged=True,second_diff_only_helper_fix=True,third_own_diff_byte_identical=True,third_message_unchanged=True,final_diff_equals_second_diff=True,trailers_and_titles_PASS=True,source_clean=True,head=chain[-1],third_diff_sha256=hashlib.sha256(oldd).hexdigest())
(E/'pre-push-proof.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
for r in identities:print(r['sha'],r['tree'],r['title'])
