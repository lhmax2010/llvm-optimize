import os,json,subprocess,datetime,pathlib,shlex
E=pathlib.Path(__file__).parent
B=E.parents[4]
C='/home/linhao/Toolchain/development/llvm-optimize/temp/gerrit-upload-20261113/source'
URL='ssh://lhmax2025@review.tizen.org:29418/platform/upstream/llvm'
BASE='13c3e223d9e1b35e4affb55255c5042f8c940f35'
ENV=dict(os.environ,GIT_SSH_COMMAND='ssh -o BatchMode=yes',GIT_TERMINAL_PROMPT='0',GIT_CONFIG_COUNT='1',GIT_CONFIG_KEY_0='push.followTags',GIT_CONFIG_VALUE_0='false')
def run(args,label=None,data=None,env=None):
    with (E/'commands.jsonl').open('a') as f: f.write(json.dumps({'argv':args,'label':label})+'\n')
    p=subprocess.run(args,cwd=C,env=env or ENV,input=data,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    if label:
        (E/(label+'.stdout')).write_bytes(p.stdout)
        (E/(label+'.stderr')).write_bytes(p.stderr)
    if p.returncode: raise RuntimeError(str(args)+' rc='+str(p.returncode)+' '+p.stderr.decode())
    return p.stdout
def git(*args,**kw): return run(['git',*args],**kw)
def end(step,status='PASS'):
    line=step+' 已结束 '+datetime.datetime.now().astimezone().isoformat()+' status='+status
    (E/(step+'-end.txt')).write_text(line+'\n');print(line,flush=True)
def query(cid,label):
    raw=run(['ssh','-o','BatchMode=yes','-p','29418','lhmax2025@review.tizen.org','gerrit','query','--format=JSON','--current-patch-set','change:'+cid],label)
    return [r for r in map(json.loads,raw.splitlines()) if r.get('type')!='stats']
