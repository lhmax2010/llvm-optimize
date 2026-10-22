#!/usr/bin/env python3
"""Evidence for the user's P2/P3 deletion after waiving historical script dependencies.

prepare is read-only on target trees. execute is the exact authorized one-time
operation; it never touches P1, P4, original RPMs or any historical script.
"""
import datetime
import importlib.util
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import time

D = Path(__file__).resolve().parent
prior = D.parent / 'approved-root-cleanup-20261022/collect.py'
spec = importlib.util.spec_from_file_location('collector', prior)
c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c)
c.OUT = D
T = Path('/home/linhao/Toolchain/development/llvm-optimize/temp')
TARGETS = {
    'P2': T / 'bolt-v4-20261015-review4b/payload-merged',
    'P3': T / 'bolt-v4-20261015-validation/baseline-extract',
}
c.TARGETS = list(TARGETS.values())
SCRIPTS = [
    T / 'bolt-v4-20261015-review4b/real_gates.py',
    T / 'bolt-v4-20261015-install-rehearsal/disk_budget.py',
    T / 'bolt-v4-20261015-validation/expected.py',
]


def stamp():
    return datetime.datetime.now().astimezone().isoformat()


def scripts():
    rows = []
    for p in SCRIPTS:
        s = p.lstat()
        rows.append(dict(path=str(p), sha256=c.digest(p), inode=s.st_ino,
                         mode=s.st_mode, uid=s.st_uid, gid=s.st_gid,
                         size=s.st_size, mtime_ns=s.st_mtime_ns))
    return rows


def check(label, target, previous=None):
    name = label + '-' + target.parent.name
    s = target.lstat()
    r = dict(path=str(target), time=stamp(), identity=dict(inode=s.st_ino, device=s.st_dev))
    fs = c.run(name+'-findmnt', ['findmnt','-T',str(target),'-n','-o','SOURCE,TARGET,FSTYPE'])
    tests = dict(exact_realpath=os.path.realpath(target)==str(target),
                 target_not_symlink=not target.is_symlink(),
                 parent_not_symlink=not target.parent.is_symlink(),
                 target_is_directory=stat.S_ISDIR(s.st_mode),
                 filesystem=fs['exit_code']==0 and fs['stdout'].split()==['/dev/sda1','/home','ext4'])
    for k, argv in [('lsof',['lsof','-nP','+D',str(target)]),('fuser',['fuser','-v',str(target)])]:
        out = c.run(name+'-'+k, argv)
        tests[k] = out['exit_code']==1 and out['stdout']=='' and out['stderr']==''
    mounts = c.mounts()
    c.save(name+'-mountinfo', mounts)
    tests['mountinfo'] = not mounts['errors'] and not mounts['matches']
    if previous:
        tests['same_inode_device'] = r['identity'] == previous['identity']
    r['checks'] = tests
    r['pass'] = all(tests.values())
    c.save(name+'-checks', r)
    return r


def prepare():
    r = dict(time=stamp(), uid=os.geteuid(), items={},
             user_waiver='Only the no-other-script-dependency condition for P2/P3 is waived. Historical scripts will not run again; re-extract original 22 RPMs first if rerun is needed. P4 remains unapproved.',
             collector_sha256=c.digest(prior))
    r['df'] = c.run('before-df-home', ['df','-B1','-T','/home'])
    r['scripts'] = scripts()
    for name, target in TARGETS.items():
        x = check('before', target)
        x['du'] = c.run('before-'+name+'-du', ['du','-sx','-B1','--',str(target)])
        inv = c.parent_inventory(target)
        c.save('before-'+name+'-parent-inventory', inv)
        x['pass'] = x['pass'] and not inv['errors'] and x['du']['exit_code']==0 and not x['du']['stderr']
        r['items'][name] = x
        c.save('before', r)
        print(name, 'PASS' if x['pass'] else 'SKIP', flush=True)
    c.save('before', r)


def execute():
    assert not (D/'execution.json').exists(), 'one-time execution only'
    before = json.loads((D/'before.json').read_text())
    r = dict(started=stamp(), uid=os.geteuid(), items=[], status='RUNNING')
    assert scripts() == before['scripts'], 'historical scripts changed before deletion'
    r['df_before'] = c.run('immediate-before-df-home', ['df','-B1','-T','/home'])
    c.save('execution', r)
    for name, target in TARGETS.items():
        x = dict(id=name, path=str(target), status='SKIP_PRECHECK')
        if before['items'][name]['pass']:
            check_now = check('immediate', target, before['items'][name])
            if check_now['pass']:
                argv = ['rm','-rf','--one-file-system','--',str(target)]
                x.update(command=argv, started=stamp())
                t = time.monotonic()
                p = subprocess.run(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                (D/('rm-'+name+'.stdout')).write_bytes(p.stdout)
                (D/('rm-'+name+'.stderr')).write_bytes(p.stderr)
                x.update(exit_code=p.returncode, stdout=p.stdout.decode(errors='replace'),
                         stderr=p.stderr.decode(errors='replace'), elapsed_seconds=time.monotonic()-t,
                         ended=stamp(), remaining=os.path.lexists(target))
                x['status'] = 'DELETED' if not p.returncode and not p.stderr and not x['remaining'] else 'STOP_REMOVAL_FAILURE'
        r['items'].append(x)
        c.save('execution', r)
        print(name, x['status'], flush=True)
        if x['status']=='STOP_REMOVAL_FAILURE':
            rows = []
            for root, dirs, files in os.walk(target,followlinks=False):
                for item in [Path(root)] + [Path(root)/n for n in dirs+files]:
                    s = item.lstat()
                    rows.append(dict(path=str(item),uid=s.st_uid,gid=s.st_gid,mode=s.st_mode))
            c.save('remaining-paths-and-owners', rows)
            break
    r['df_after'] = c.run('immediate-after-df-home', ['df','-B1','-T','/home'])
    r['scripts_after'] = scripts()
    r['scripts_unchanged'] = r['scripts_after'] == before['scripts']
    r['parents'] = {}
    for name,target in TARGETS.items():
        inv = c.parent_inventory(target)
        c.save('after-'+name+'-parent-inventory', inv)
        prev = json.loads((D/('before-'+name+'-parent-inventory.json')).read_text())
        r['parents'][name] = dict(unchanged=inv==prev, summary={k:v for k,v in inv.items() if k!='entries'},
                                  du=c.run('after-'+name+'-parent-du',['du','-sx','-B1','--',str(target.parent)]))
    r['ended'] = stamp()
    r['status'] = ('PASS' if len(r['items'])==2 and all(x['status']=='DELETED' for x in r['items']) and
                   r['scripts_unchanged'] and all(x['unchanged'] for x in r['parents'].values()) else 'STOP_OR_SKIPPED')
    c.save('execution',r)
    print('RESULT', r['status'], flush=True)


if __name__=='__main__':
    assert os.geteuid()==1000
    assert sys.argv[1] in ('prepare','execute')
    (prepare if sys.argv[1]=='prepare' else execute)()
