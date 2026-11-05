import os,sys,json
from pathlib import Path
os.environ['NIGHT_SOURCE_SHA']='9e39fa8a61392652bb28b75fc26216675bcad1d5'
T=Path(__file__).resolve().parents[3]/'night-launch-20261105';sys.path.insert(0,str(T));import launcher
W=Path('/home/linhao/Toolchain/development/llvm-optimize');D=W/'temp/night-20261105/handoff-test';D.mkdir();(D/'evidence').mkdir();launcher.materialize(D,dict(prep_unit='fixture',build_unit='fixture',mode='full'))
s=(D/'run.py').read_text();start=s.index('def log_epoch(p):');end=s.index("prep_log_epoch=",start);env={};exec(s[start:end],env)
p=D/'source.log';p.write_bytes(b'[ 1s] OLD PREP\n');epoch=env['log_epoch'](p);assert env['log_epoch'](p)==epoch
# The sampler waits here: no old bytes have been appended.
copied=bytearray();p.write_bytes(b'[ 0s] NEW BUILD\n');assert env['log_epoch'](p)!=epoch
position=0;anchor=b'';events=[];env.update(p=p,position=position,anchor=anchor,time=__import__('time'),append=lambda n,v:events.append(n))
start=s.index('    src.seek(max(0,position-len(anchor)))');end=s.index('\n',s.index('anchor=src.read(min(position,128))',start));block='\n'.join(l[4:] for l in s[start:end].splitlines())
for b in [b'',b'[ 1s] Executing(%build)\n',b'[ 2s] + cmake -G Ninja\n']:
 with p.open('ab') as f:f.write(b)
 with p.open('rb') as f:env['src']=f;exec(block,env)
 copied.extend(env['b'])
assert bytes(copied)==p.read_bytes();assert not events
(D/'copied.log').write_bytes(copied)
print('PREP_HANDOFF_PASS old_prep_bytes=0 log_restarts=0 exact_copy=true')
