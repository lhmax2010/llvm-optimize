#!/usr/bin/env python3
"""One authorized removal, after checks; P2/P3 fail dependency checks and are skipped."""
import datetime
import importlib.util
import json
import os
from pathlib import Path
import stat
import subprocess
import time

D = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('collector', D / 'collect.py')
c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c)
target = Path('/home/linhao/Toolchain/development/llvm-optimize/temp/bolt-v4-20261015-review3/payload-merged')
assert os.geteuid() == 1000
before = json.loads((D/'before-checks.json').read_text())
review = json.loads((D/'dependency-review.json').read_text())
assert review['items'][0]['decision'] == 'eligible'
assert all(x['decision'] == 'SKIP' for x in review['items'][1:])
expected = before['items'][0]
result = dict(time=datetime.datetime.now().astimezone().isoformat(), uid=os.geteuid(),
              target=str(target), skipped=['P2', 'P3'], status='CHECKING')
checks = {}
s = target.lstat()
checks['path_identity'] = (os.path.realpath(target) == str(target) and
                          not target.is_symlink() and not target.parent.is_symlink() and
                          stat.S_ISDIR(s.st_mode) and s.st_ino == expected['identity']['inode'] and
                          s.st_dev == expected['identity']['device'])
fs = c.run('immediate-P1-findmnt', ['findmnt', '-T', str(target), '-n', '-o', 'SOURCE,TARGET,FSTYPE'])
checks['filesystem'] = fs['exit_code'] == 0 and fs['stdout'].split() == ['/dev/sda1', '/home', 'ext4']
for name, argv in [('lsof', ['lsof', '-nP', '+D', str(target)]), ('fuser', ['fuser', '-v', str(target)])]:
    r = c.run('immediate-P1-'+name, argv)
    checks[name] = r['exit_code'] == 1 and r['stdout'] == '' and r['stderr'] == ''
m = c.mounts()
c.save('immediate-mountinfo-check', m)
checks['mountinfo'] = not m['errors'] and not m['matches']
checks['du'] = expected['du']['exit_code'] == 0 and not expected['du']['stderr']
checks['parent_evidence'] = not expected['parent_summary']['errors']
checks['dependency'] = review['items'][0]['dependency_check'] == 'PASS'
result['checks'] = checks
c.save('execution', result)
if not all(checks.values()):
    result['status'] = 'SKIPPED_PRECHECK'
    result['skipped'] = ['P1', 'P2', 'P3']
    c.save('execution', result)
    print(json.dumps(result, ensure_ascii=False))
    raise SystemExit(0)

result['df_before'] = c.run('immediate-before-df-home', ['df','-B1','-T','/home'])
argv = ['rm', '-rf', '--one-file-system', '--', str(target)]
result['command'] = argv
result['started'] = datetime.datetime.now().astimezone().isoformat()
c.save('execution', result)
start = time.monotonic()
p = subprocess.run(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
(D/'rm-P1.stdout').write_bytes(p.stdout)
(D/'rm-P1.stderr').write_bytes(p.stderr)
result.update(exit_code=p.returncode, stdout=p.stdout.decode(errors='replace'),
              stderr=p.stderr.decode(errors='replace'), elapsed_seconds=time.monotonic()-start,
              target_remaining=os.path.lexists(target),
              ended=datetime.datetime.now().astimezone().isoformat())
result['df_after'] = c.run('immediate-after-df-home', ['df','-B1','-T','/home'])
if p.returncode or p.stderr or os.path.lexists(target):
    result['status'] = 'STOPPED_REMOVAL_FAILURE'
    remaining = []
    for root, dirs, files in os.walk(target, followlinks=False):
        for path in [Path(root)] + [Path(root)/f for f in files]:
            try:
                st = path.lstat()
                remaining.append(dict(path=str(path), uid=st.st_uid, gid=st.st_gid, mode=st.st_mode))
            except OSError as e:
                remaining.append(dict(path=str(path), error=str(e)))
    c.save('remaining-paths-and-owners', remaining)
else:
    result['status'] = 'P1_DELETED_P2_P3_SKIPPED'
c.save('execution', result)
print(json.dumps(result, ensure_ascii=False, indent=2))
