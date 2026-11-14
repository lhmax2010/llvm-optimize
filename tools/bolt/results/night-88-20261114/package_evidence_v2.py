import hashlib,json,subprocess
from pathlib import Path
B=Path.cwd();E=B/'tools/bolt/results/night-88-20261114'
files=[p for p in sorted(E.rglob('*')) if p.is_file() and 'fixtures' not in p.relative_to(E).parts]
root='https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/'
intro='''# 88号证据 raw 链接索引

步骤1 PASS（30/30）；步骤2 T/D各2804条，PASS；步骤3 STOP（其他GBS重任务运行中，未启动BOLT）。

- [88号报告](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/docs/bolt/88_entry_sync_reloc_stats_report_stale.md)
- [STATUS](https://raw.githubusercontent.com/lhmax2010/llvm-optimize/bolt-v4/docs/bolt/STATUS.md)

`entry/fixtures/` 原件仅保留本地；交付其 tar.gz 副本及逐文件 SHA 清单，不删除原件。下面列出各证据文件；stdout/stderr 空文件也保留。旧87号计划与源码原件未修改。

'''
intro+='\n'.join(f'- [{p.relative_to(E)}]({root}{p.relative_to(B)})' for p in files if p.name!='README.md')+'\n'
(E/'README.md').write_text(intro)
files.append(E/'README.md')
selected=[str(p.relative_to(B)) for p in files]+['docs/bolt/88_entry_sync_reloc_stats_report_stale.md','docs/bolt/STATUS.md']
for p in selected:assert (B/p).stat().st_size<=10000000,p
subprocess.run(['git','add','-f','--',*selected],check=True)
staged=subprocess.check_output(['git','diff','--cached','--name-only','-z']).decode().split('\0');staged=[p for p in staged if p]
assert set(staged)<=set(selected),set(staged)-set(selected)
for p in selected:
 assert subprocess.check_output(['git','show',':'+p])==(B/p).read_bytes(),p
for p in staged:
 assert p.startswith('tools/bolt/results/night-88-20261114/') or p in selected[-2:]
 data=subprocess.check_output(['git','show',':'+p]);assert len(data)<=10000000
 if (not p.endswith('.gz')):
  assert b'-----BEGIN OPENSSH PRIVATE KEY-----' not in data and b'-----BEGIN RSA PRIVATE KEY-----' not in data
print(json.dumps({'staged_files':len(staged),'total_bytes':sum((B/p).stat().st_size for p in staged),'max_file_bytes':max((B/p).stat().st_size for p in staged),'paths':staged},indent=2))
