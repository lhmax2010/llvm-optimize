from pathlib import Path
import hashlib
import json
import os
import stat
import time
from checks import *

E = Path(__file__).parent
T = Path('/home/linhao/Toolchain/development/llvm-optimize/temp')
REL = ['final-20261103/toolchain-rehearsal/gbs-root',
       'final-20261103/basedev-rehearsal/gbs-root',
       'final-20261103/basedev-rehearsal/retry-02/gbs-root',
       'second-review-20261104/toolchain-rehearsal/gbs-root',
       'second-review-20261104/basedev-rehearsal/gbs-root',
       'archive-index-fix-rpm-20260923', 'archive-fix-rebind-20260923',
       'static-native-conversion-20260924', 'toolchain-hybrid-trial',
       'hybrid-trial-20260922']
TARGETS = [str(T / p) for p in REL]


def save(name, value):
    (E / name).write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')


def digest(p):
    h = hashlib.sha256()
    with p.open('rb') as f:
        while b := f.read(4 * 1024 * 1024): h.update(b)
    return h.hexdigest()


assert os.geteuid() == 1000
save('df-before.json', command(['df', '-B1', '-T', str(T)]))
save('parent-before.json', parent_snapshot(TARGETS))
mounts = mount_snapshot(TARGETS); save('mounts-before.json', mounts)
processes = process_snapshot(TARGETS); save('processes-before.json', processes)
services = user_services(); save('services-before.json', services)
plan = dict(time=stamp(), uid=os.geteuid(), targets=TARGETS, items=[],
            proc_blind_spots=len(processes['errors']),
            note='Unprivileged /proc blind spots must be resolved by the single authorized root invocation before any deletion.')
for number, target in enumerate(TARGETS, 1):
    p = Path(target); ident = identity(target); reasons = []
    if not (ident.get('directory') and not ident.get('symlink') and not ident.get('parent_symlink') and ident.get('realpath') == target):
        reasons.append('path identity/symlink check failed')
    if mounts['rc'] or any(x['target'] == target for x in mounts['matches']): reasons.append('mount or overlay reference / failed findmnt')
    if any(x['target'] == target for x in processes['matches']): reasons.append('open process cwd/root/exe/fd')
    if services['listing']['rc'] or services['show']['rc']: reasons.append('cannot query user services')
    if target in services['show']['stdout']: reasons.append('active user service references target')
    row = dict(number=number, target=target, identity=ident, skip_reasons=reasons)
    if ident.get('directory'):
        row['root_owned_probe'] = command(['find', target, '-xdev', '-uid', '0', '-print', '-quit'], 60)
        row['du'] = command(['du', '-sx', '-B1', target], 180 if number >= 6 else 30)
        if number >= 6:
            listing = []
            for child in sorted(p.iterdir()):
                s = child.lstat()
                listing.append(dict(name=child.name, mode=oct(s.st_mode), uid=s.st_uid,
                                    gid=s.st_gid, bytes=s.st_size, mtime_ns=s.st_mtime_ns,
                                    link=os.readlink(child) if child.is_symlink() else None))
            save('inventory-%02d-top.json' % number, listing)
            rpms = []; errors = []
            for root, ds, fs in os.walk(p, followlinks=False, onerror=lambda e: errors.append(str(e))):
                ds[:] = [n for n in ds if not (Path(root)/n).is_symlink()]
                for name in sorted(fs):
                    if not name.lower().endswith('.rpm'): continue
                    f = Path(root) / name
                    try:
                        before = f.stat(); sha = digest(f); after = f.stat()
                        assert (before.st_ino,before.st_size,before.st_mtime_ns) == (after.st_ino,after.st_size,after.st_mtime_ns)
                        rpms.append(dict(path=str(f), relative=str(f.relative_to(p)), bytes=after.st_size,
                                         sha256=sha, symlink=f.is_symlink()))
                    except (OSError, AssertionError) as e: errors.append(str(f)+': '+str(e))
            save('inventory-%02d-rpms.json' % number, dict(files=rpms, errors=errors))
            row['rpm_count'] = len(rpms)
            row['inventory_errors'] = errors
            if errors or row['du']['rc'] != 0: reasons.append('required inventory incomplete')
    row['status'] = 'SKIP' if reasons else 'READY_FOR_PRIVILEGED_RECHECK'
    plan['items'].append(row); save('plan.json', plan)
    print(stamp(), number, row['status'], 'rpms', row.get('rpm_count', 'n/a'), flush=True)
save('parent-before-final.json', parent_snapshot(TARGETS))
assert json.loads((E/'parent-before.json').read_text()) == json.loads((E/'parent-before-final.json').read_text()), 'parents changed during preparation'
print('PREPARATION FINISHED', stamp(), flush=True)
