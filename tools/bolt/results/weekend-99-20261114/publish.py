from pathlib import Path
import subprocess,sys,os
b=Path(__file__).resolve().parents[4];e=Path(__file__).resolve().parent
files=[]
for p in e.rglob('*'):
 if not p.is_file() or p.is_symlink():continue
 rel=p.relative_to(e)
 if any(x=='environment' or x.endswith('-scratch') for x in rel.parts):continue
 if p.stat().st_size>10_000_000:raise RuntimeError('oversize '+str(p))
 files.append(str(p.relative_to(b)))
files+=['docs/bolt/99_weekend.md','docs/bolt/STATUS.md']
subprocess.run(['git','add','-f','--',*files],cwd=b,check=True)
staged=subprocess.check_output(['git','diff','--cached','--name-only'],cwd=b,text=True).splitlines()
assert set(staged)<=set(files),staged
subprocess.run(['git','-c','gc.auto=0','-c','user.name=Hao Lin','-c','user.email=hao.lin@samsung.com','commit','-m',sys.argv[1]],cwd=b,check=True)
env=dict(os.environ,GIT_TERMINAL_PROMPT='0',GIT_SSH_COMMAND='ssh -o BatchMode=yes',GCM_INTERACTIVE='Never')
subprocess.run(['git','-c','gc.auto=0','push','origin','HEAD:refs/heads/bolt-v4'],cwd=b,env=env,check=True)
h=subprocess.check_output(['git','rev-parse','HEAD'],cwd=b,text=True).strip();r=subprocess.check_output(['git','ls-remote','origin','refs/heads/bolt-v4'],cwd=b,env=env,text=True);assert r.split()[0]==h;print('PUBLISHED',h,flush=True)
