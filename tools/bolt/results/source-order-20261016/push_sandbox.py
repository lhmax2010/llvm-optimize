from pathlib import Path
import subprocess,json,sys,time
E=Path(__file__).resolve().parent;S=E.parents[1]/'temp/bolt-v4-20261013/v41/llvm-source';branch='refs/heads/sandbox/lhmax2025/bolt_pgo';old='506dc25c86e4e2154150796d10b77b71d71ad6bb';new=json.loads((E/'source-result.json').read_text())['new'];result={'branch':branch,'old_expected':old,'new_expected':new,'review_push':False,'new_branch_created':False,'started':time.time()}
def git(*args):return subprocess.check_output(['git','-C',str(S),*args])
assert json.loads((E/'verification-summary.json').read_text())['status']=='PASS_REQUIRED'
assert json.loads((E/'raw-publication-verification.json').read_text())['PASS']
assert git('rev-parse','HEAD').decode().strip()==new
assert git('rev-parse','HEAD^').decode().strip()=='67619ec8bbbac7238a6cfc33a481ccfbcd12206f'
assert not git('status','--porcelain')
assert git('diff','--no-ext-diff',old,new,'--','packaging/llvm.spec')==(E/'source.diff').read_bytes()
assert git('cat-file','commit',new).split(b'\n\n',1)[1]==(E/'commit-message-after.txt').read_bytes()
before=git('ls-remote','origin',branch).decode();(E/'sandbox-before-push.txt').write_text(before);result['before_raw']=before
if before.split()!=[old,branch]:
 result.update(status='STOP',reason='Remote not at specified lease');(E/'sandbox-result.json').write_text(json.dumps(result,indent=2)+'\n');raise SystemExit('STOP remote lease does not equal 506dc25: '+before)
argv=['git','-C',str(S),'push','--force-with-lease='+branch+':'+old,'origin',new+':'+branch];result['push_argv']=argv
r=subprocess.run(argv,capture_output=True,text=True);(E/'sandbox-push.stdout').write_text(r.stdout);(E/'sandbox-push.stderr').write_text(r.stderr);result['push_rc']=r.returncode
if r.returncode:
 result.update(status='REJECTED',stdout=r.stdout,stderr=r.stderr);(E/'sandbox-result.json').write_text(json.dumps(result,indent=2)+'\n');print(r.stdout+r.stderr);raise SystemExit(r.returncode)
after=git('ls-remote','origin',branch).decode();(E/'sandbox-after-push.txt').write_text(after);result['after_raw']=after;result['status']='PASS' if after.split()==[new,branch] else 'STOP_REMOTE_MISMATCH';(E/'sandbox-result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));assert result['status']=='PASS'
