from pathlib import Path
import subprocess,json,xml.etree.ElementTree as X,difflib,hashlib
W=Path('/home/linhao/Toolchain/development/llvm-optimize');B=W.parent/'llvm-optimize-bolt';E=B/'tools/bolt/results/qb-meta-switch-20261028';D=E/'second-ruling';R=W/'temp/qb-meta-20261028/repo'
def git(*a):return subprocess.check_output(['git',*a],cwd=R)
assert json.loads((D/'closure-summary.json').read_text())['status']=='PASS'
assert not git('status','--porcelain')
r=subprocess.run(['git','fetch','origin','master'],cwd=R,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(D/'unified-fetch.txt').write_bytes(r.stdout);assert r.returncode==0
base=git('rev-parse','origin/master').decode().strip();assert base==(D/'master-before.txt').read_text().strip(),'master advanced; recheck inputs before committing'
subprocess.run(['git','switch','--detach','origin/master'],cwd=R,check=True)
f='TIZEN/Tizen/Tizen-Unified-Toolchain/snapshot_info';before=(R/f).read_bytes();after=(D/'unified-proposed-snapshot_info.xml').read_bytes();(R/f).write_bytes(after)
x,y=X.fromstring(before),X.fromstring(after);assert X.tostring(x.find('base'))==X.tostring(y.find('base'))
assert git('diff','--name-only').decode().splitlines()==[f]
num=git('diff','--numstat').decode().split();assert num[:2]==['2','2']
removed=json.loads((E/'unified-fixed-source-comparison.json').read_text())['missing_from_new'];cs=json.loads((D/'closure-summary.json').read_text())
msg='''Use Unified sources for Unified Toolchain

Build Tizen-Unified-Toolchain from the Tizen-Unified reference snapshot
20261027.231956. Keep base unchanged, so dependency packages and the
base build.conf continue to come from Tizen-Base-Toolchain. Leave the
project's own project_config and all other project files unchanged.

QB 1211018 resolves 251 source repositories from the Base snapshot,
although 3c78318b left the 245-entry Toolchain meta manifest unchanged.
All entries match that snapshot apart from the requested LLVM override.
QB 1209720/1209727 separately log the reference snapshot_num_url and
base_path_url; repository setup and get_build_conf_text use the latter.

The Unified standard manifest no longer builds these 17 repositories:

'''+''.join('  '+n+'\n' for n in removed)+f'''
The exact-revision audit covers all 1030 remaining repositories and
{cs['specs']} specs, preserving conditional BuildRequires branches. None of
the {cs['buildrequires_lines']} BuildRequires entries references the 134 capabilities recorded
for those removed repositories. Thus none relies exclusively on their
outputs; the existing Base-Toolchain dependency layer is retained.

Merge after Base-Toolchain produces a snapshot from the Base sources,
in coordination with its normal dependency-snapshot reference update,
to avoid combining new Unified sources with old dependency packages.

Signed-off-by: Hao Lin <hao.lin@samsung.com>
'''
assert all(len(l)<=72 for l in msg.splitlines()),[(len(l),l) for l in msg.splitlines() if len(l)>72]
(D/'unified-message.txt').write_text(msg)
subprocess.run(['git','add',f],cwd=R,check=True)
r=subprocess.run(['git','-c','user.name=Hao Lin','-c','user.email=hao.lin@samsung.com','commit','-F',str(D/'unified-message.txt')],cwd=R,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(D/'unified-commit-output.txt').write_bytes(r.stdout);print(r.stdout.decode());assert r.returncode==0
sha=git('rev-parse','HEAD').decode().strip();assert git('rev-parse','HEAD^').decode().strip()==base
assert git('diff','--name-only','HEAD^','HEAD').decode().splitlines()==[f]
assert git('diff','--numstat','HEAD^','HEAD').decode().split()[:2]==['2','2']
assert b'Change-Id: I' in git('show','-s','--format=%B','HEAD')
assert git('show','-s','--format=%an <%ae>%n%cn <%ce>','HEAD').decode().splitlines()==['Hao Lin <hao.lin@samsung.com>']*2
(D/'unified-final.diff').write_bytes(git('diff','HEAD^','HEAD'));(D/'unified-final-commit.txt').write_bytes(git('show','-s','--format=fuller','HEAD'))
(D/'unified-validation.json').write_text(json.dumps(dict(commit=sha,parent=base,xml_valid=True,changed_files=[f],added_lines=2,removed_lines=2,base_identical=True,closure_status='PASS',independent_of_base_review=True),indent=2)+'\n')
a=['git','push','origin',sha+':refs/for/master'];(D/'unified-push-command.txt').write_text(' '.join(a)+'\n');r=subprocess.run(a,cwd=R,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(D/'unified-push.txt').write_bytes(r.stdout);print(r.stdout.decode());print('PUSH EXIT',r.returncode);assert r.returncode==0
