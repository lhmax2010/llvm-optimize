#!/usr/bin/env python3
"""Read-only pre/post checks for the user's three explicitly approved copies.

This collector never removes files. Output is restricted to its evidence directory.
"""
import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys
import time

OUT = Path(__file__).resolve().parent
W = Path('/home/linhao/Toolchain/development/llvm-optimize')
B = Path('/home/linhao/Toolchain/development/llvm-optimize-bolt')
TARGETS = [
    W / 'temp/bolt-v4-20261015-review3/payload-merged',
    W / 'temp/bolt-v4-20261015-review4b/payload-merged',
    W / 'temp/bolt-v4-20261015-validation/baseline-extract',
]


def save(name, value):
    (OUT / (name + '.json')).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def run(name, argv):
    start = time.time()
    p = subprocess.run(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (OUT / (name + '.stdout')).write_bytes(p.stdout)
    (OUT / (name + '.stderr')).write_bytes(p.stderr)
    result = dict(argv=argv, exit_code=p.returncode, elapsed_seconds=time.time()-start,
                  stdout=p.stdout.decode(errors='replace'), stderr=p.stderr.decode(errors='replace'))
    save(name, result)
    return result


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024*1024), b''):
            h.update(block)
    return h.hexdigest()


def parent_inventory(target):
    root = target.parent
    errors, entries = [], []
    def walk(directory):
        try:
            children = sorted(os.scandir(directory), key=lambda x: x.name)
        except OSError as e:
            errors.append(str(e))
            return
        for item in children:
            path = Path(item.path)
            if path == target:
                continue
            try:
                s = path.lstat()
                entry = dict(path=str(path.relative_to(root)), mode=s.st_mode,
                             uid=s.st_uid, gid=s.st_gid, size=s.st_size,
                             blocks=s.st_blocks, mtime_ns=s.st_mtime_ns,
                             inode=s.st_ino, device=s.st_dev)
                if stat.S_ISREG(s.st_mode):
                    entry['sha256'] = digest(path)
                elif stat.S_ISLNK(s.st_mode):
                    entry['link_target'] = os.readlink(path)
                entries.append(entry)
                if stat.S_ISDIR(s.st_mode):
                    walk(path)
            except OSError as e:
                errors.append(str(e))
    walk(root)
    s = root.lstat()
    return dict(root=str(root), excluded=str(target), errors=errors, entries=entries,
                root_identity=dict(mode=s.st_mode, uid=s.st_uid, gid=s.st_gid,
                                   inode=s.st_ino, device=s.st_dev),
                paths=len(entries), regular_files=sum(stat.S_ISREG(e['mode']) for e in entries),
                regular_file_bytes=sum(e['size'] for e in entries if stat.S_ISREG(e['mode'])),
                allocated_bytes=sum(e['blocks']*512 for e in entries))


def unescape(s):
    return re.sub(r'\\([0-7]{3})', lambda m: chr(int(m[1], 8)), s)


def within(path, root):
    return path == root or path.startswith(root.rstrip('/') + '/')


def mounts():
    errors, vanished, matches, unique = [], [], [], set()
    count = 0
    for p in sorted(Path('/proc').glob('[0-9]*/mountinfo')):
        try:
            content = p.read_text()
        except FileNotFoundError:
            vanished.append(str(p))
            continue
        except OSError as e:
            errors.append(dict(path=str(p), error=str(e)))
            continue
        count += 1
        unique.add(hashlib.sha256(content.encode()).hexdigest())
        for line in content.splitlines():
            a, b = line.split(' - ', 1)
            af, bf = a.split(), b.split()
            mountpoint = unescape(af[4])
            for target in TARGETS:
                t = str(target)
                if within(mountpoint, t):
                    matches.append(dict(pid=p.parent.name, target=t, kind='mountpoint', line=line))
                if bf[0] == 'overlay':
                    for opt in bf[2].split(','):
                        key, _, val = opt.partition('=')
                        if key in ('lowerdir', 'upperdir', 'workdir'):
                            for member in val.split(':'):
                                member = unescape(member)
                                if within(member, t) or within(t, member):
                                    matches.append(dict(pid=p.parent.name, target=t, kind=key, line=line))
    return dict(proc_mountinfo_read=count, unique_snapshots=len(unique),
                errors=errors, vanished=vanished, matches=matches)


def main():
    phase = sys.argv[1]
    assert phase in ('before', 'after', 'recheck')
    assert os.geteuid() == 1000
    result = dict(phase=phase, time=datetime.datetime.now().astimezone().isoformat(), uid=os.geteuid(), items=[])
    result['df'] = run(phase+'-df-home', ['df', '-B1', '-T', '/home'])
    result['mounts'] = mounts()
    save(phase+'-mountinfo-check', result['mounts'])
    if phase == 'before':
        needles = [str(t) for t in TARGETS]
        run('docs-exact-path-search', ['rg', '-n', '-F'] + sum([['-e', n] for n in needles], []) + [str(B/'docs'),str(W/'docs')])
        run('docs-alias-search', ['rg', '-n', 'payload-merged|baseline-extract|bolt-v4-20261015-(review3|review4b|validation)', str(B/'docs'),str(W/'docs')])
        run('git-evidence-before', ['git','-C',str(B),'status','--short'])
    for i, target in enumerate(TARGETS, 1):
        name = phase+'-P'+str(i)
        item = dict(id='P'+str(i), path=str(target), exists=os.path.lexists(target),
                    realpath=os.path.realpath(target), target_symlink=target.is_symlink(),
                    parent_symlink=target.parent.is_symlink())
        if item['exists']:
            s = target.lstat()
            item['identity'] = dict(mode=s.st_mode, uid=s.st_uid, gid=s.st_gid, device=s.st_dev, inode=s.st_ino)
            item['findmnt'] = run(name+'-findmnt', ['findmnt','-T',str(target),'-n','-o','SOURCE,TARGET,FSTYPE'])
            if phase in ('before','recheck'):
                item['lsof'] = run(name+'-lsof', ['lsof','-nP','+D',str(target)])
                item['fuser'] = run(name+'-fuser', ['fuser','-v',str(target)])
            if phase == 'before':
                item['du'] = run(name+'-du', ['du','-sx','-B1','--',str(target)])
        if phase in ('before', 'after'):
            inv = parent_inventory(target)
            save(name+'-parent-inventory', inv)
            item['parent_summary'] = {k:v for k,v in inv.items() if k != 'entries'}
            if phase == 'after':
                prev = json.loads((OUT / ('before-P'+str(i)+'-parent-inventory.json')).read_text())
                item['parent_unchanged'] = inv == prev
                item['parent_du'] = run(name+'-parent-du', ['du','-sx','-B1','--',str(target.parent)])
        result['items'].append(item)
        save(phase+'-checks', result)
        print(json.dumps({k:v for k,v in item.items() if k not in ('lsof','fuser','du','parent_summary')},ensure_ascii=False), flush=True)
    save(phase+'-checks', result)


if __name__ == '__main__':
    main()
