#!/bin/sh
set -eu
umask 022
cd "$(dirname "$0")"
exec nice -n 19 ionice -c2 -n7 python3 -B - <<'PY'
"""Read-only checks shared by preparation and the printed deletion script."""
from pathlib import Path
import datetime
import json
import os
import re
import stat
import subprocess


def stamp():
    return datetime.datetime.now().astimezone().isoformat()


def command(argv, timeout=60):
    try:
        p = subprocess.run(argv, capture_output=True, text=True, timeout=timeout)
        return dict(argv=argv, rc=p.returncode, stdout=p.stdout, stderr=p.stderr)
    except subprocess.TimeoutExpired as e:
        def text(v):
            return v.decode(errors='replace') if isinstance(v, bytes) else v or ''
        return dict(argv=argv, rc=124, stdout=text(e.stdout), stderr=text(e.stderr))


def beneath(value, target):
    value = value.removesuffix(' (deleted)')
    return value == target or value.startswith(target + os.sep)


def process_snapshot(targets):
    result = dict(time=stamp(), matches=[], errors=[])
    proc = Path(os.sep) / 'proc'
    for pid in proc.iterdir():
        if not pid.name.isdigit():
            continue
        try:
            links = [pid / 'cwd', pid / 'root', pid / 'exe']
            try:
                links += list((pid / 'fd').iterdir())
            except PermissionError as e:
                result['errors'].append(str(e))
            for link in links:
                try:
                    value = os.readlink(link)
                except PermissionError as e:
                    result['errors'].append(str(e)); continue
                except (FileNotFoundError, ProcessLookupError, OSError):
                    continue
                for target in targets:
                    if beneath(value, target):
                        result['matches'].append(dict(target=target, pid=int(pid.name), link=str(link), value=value))
            try:
                maps = (pid / 'maps').read_text().splitlines()
            except PermissionError as e:
                result['errors'].append(str(e)); maps = []
            except (FileNotFoundError, ProcessLookupError):
                maps = []
            for line in maps:
                fields = line.split(None, 5)
                if len(fields) != 6 or not fields[5].startswith(os.sep):
                    continue
                for target in targets:
                    if beneath(fields[5], target):
                        result['matches'].append(dict(target=target, pid=int(pid.name), link=str(pid / 'maps'), value=fields[5]))
        except (FileNotFoundError, ProcessLookupError):
            continue
    return result


def mount_snapshot(targets):
    r = command(['findmnt', '-rn', '-o', 'TARGET,SOURCE,FSTYPE,OPTIONS'])
    matches = []
    for line in r['stdout'].splitlines():
        # Decode findmnt's octal/hex escapes before comparing path boundaries.
        decoded = re.sub(r'\\x([0-9a-fA-F]{2})', lambda m: chr(int(m[1], 16)), line)
        for target in targets:
            fields = decoded.split()
            at = fields[0] if fields else ''
            option_paths = re.split(r'[,=: ]', decoded)
            if beneath(at, target) or any(beneath(x, target) for x in option_paths):
                matches.append(dict(target=target, line=line))
    r['matches'] = matches
    return r


def user_services(prefix=None):
    prefix = prefix or []
    listing = command(prefix + ['systemctl', '--user', 'list-units', '--type=service',
                                '--state=active,activating,reloading,deactivating',
                                '--no-legend', '--plain', '--no-pager'])
    units = [line.split()[0] for line in listing['stdout'].splitlines() if line.split()]
    show = command(prefix + ['systemctl', '--user', 'show', *units,
                            '-p', 'Id', '-p', 'ActiveState', '-p', 'ExecStart',
                            '-p', 'WorkingDirectory', '-p', 'RootDirectory', '-p', 'ControlGroup']) if units else dict(rc=0, stdout='', stderr='', argv=[])
    return dict(listing=listing, show=show)


def identity(path):
    p = Path(path)
    try:
        s = p.lstat()
        return dict(exists=True, directory=stat.S_ISDIR(s.st_mode), symlink=stat.S_ISLNK(s.st_mode),
                    parent_symlink=p.parent.is_symlink(), realpath=os.path.realpath(p),
                    dev=s.st_dev, inode=s.st_ino, uid=s.st_uid, gid=s.st_gid)
    except FileNotFoundError:
        return dict(exists=False)


def parent_snapshot(targets):
    result = []
    for parent in sorted({str(Path(p).parent) for p in targets}):
        rows = []
        for p in sorted(Path(parent).iterdir()):
            if str(p) in targets:
                continue
            s = p.lstat()
            rows.append(dict(name=p.name, inode=s.st_ino, dev=s.st_dev, mode=s.st_mode,
                             uid=s.st_uid, gid=s.st_gid,
                             link=os.readlink(p) if p.is_symlink() else None,
                             size=s.st_size if stat.S_ISREG(s.st_mode) else None,
                             mtime_ns=s.st_mtime_ns if stat.S_ISREG(s.st_mode) else None))
        result.append(dict(parent=parent, entries=rows))
    return result

TARGETS = ['/home/linhao/Toolchain/development/llvm-optimize/temp/final-20261103/toolchain-rehearsal/gbs-root', '/home/linhao/Toolchain/development/llvm-optimize/temp/final-20261103/basedev-rehearsal/gbs-root', '/home/linhao/Toolchain/development/llvm-optimize/temp/final-20261103/basedev-rehearsal/retry-02/gbs-root', '/home/linhao/Toolchain/development/llvm-optimize/temp/second-review-20261104/toolchain-rehearsal/gbs-root', '/home/linhao/Toolchain/development/llvm-optimize/temp/second-review-20261104/basedev-rehearsal/gbs-root', '/home/linhao/Toolchain/development/llvm-optimize/temp/archive-index-fix-rpm-20260923', '/home/linhao/Toolchain/development/llvm-optimize/temp/archive-fix-rebind-20260923', '/home/linhao/Toolchain/development/llvm-optimize/temp/static-native-conversion-20260924', '/home/linhao/Toolchain/development/llvm-optimize/temp/toolchain-hybrid-trial', '/home/linhao/Toolchain/development/llvm-optimize/temp/hybrid-trial-20260922']

import hashlib
import sys
import time
E = Path.cwd()
assert os.geteuid() == 0
plan = json.loads((E/'plan.json').read_text())
assert plan['targets'] == TARGETS and len(TARGETS) == 10
assert not (E/'root-entry.json').exists(), 'single root invocation only'
(E/'root-entry.json').write_text(json.dumps({'time':stamp(),'uid':os.geteuid()})+'\n')

def save(name, value):
    (E/name).write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')

def df(path):
    r=command(['df','-B1','-T',path])
    assert r['rc']==0,r
    r['available_bytes']=int(r['stdout'].splitlines()[-1].split()[4])
    return r

def emit(text):
    line=stamp()+' '+text
    print(line,flush=True)
    with (E/'execution.log').open('a') as f:f.write(line+'\n')

def remaining_root_owned(p):
    for root,ds,fs in os.walk(p,followlinks=False):
        for q in [Path(root)]+[Path(root)/n for n in ds+fs]:
            try:
                st=q.lstat()
                if st.st_uid==0:return dict(path=str(q),uid=0,mode=oct(st.st_mode))
            except FileNotFoundError:pass
    return None

def delete_run(number,label,argv):
    name='delete-%02d-%s.log'%(number,label)
    emit('COMMAND '+repr(argv))
    start=time.monotonic()
    with (E/name).open('w') as log:
        p=subprocess.run(argv,stdout=log,stderr=subprocess.STDOUT)
    return dict(argv=argv,rc=p.returncode,seconds=time.monotonic()-start,log=name)

runtime=str(Path(os.sep)/'run'/'user'/'1000')
user_prefix=['setpriv','--reuid=1000','--regid=1000','--init-groups']
svc_prefix=user_prefix+['env','XDG_RUNTIME_DIR='+runtime,'DBUS_SESSION_BUS_ADDRESS=unix:path='+runtime+'/bus']
uid_check=command(user_prefix+['id','-u']);save('ordinary-uid.json',uid_check)
assert uid_check['rc']==0 and uid_check['stdout'].strip()=='1000'
result=dict(start=stamp(),items=[],status='running',df_before=df(str(Path(TARGETS[0]).parent)))
save('execution.json',result)
try:
    assert parent_snapshot(TARGETS)==json.loads((E/'parent-before-final.json').read_text()), 'parent contents changed before root execution'
    for previous in plan['items']:
        number=previous['number'];target=previous['target'];assert target==TARGETS[number-1]
        row=dict(number=number,path=target,status='skipped',reason=list(previous['skip_reasons']))
        result['items'].append(row)
        if row['reason']:
            emit('SKIP %s %s'%(number,row['reason']));save('execution.json',result);continue
        ident=identity(target);expected=previous['identity']
        if not (ident.get('directory') and not ident.get('symlink') and not ident.get('parent_symlink') and ident.get('realpath')==target and ident.get('dev')==expected.get('dev') and ident.get('inode')==expected.get('inode')):
            row['reason'].append('identity changed or not a real directory')
        mounts=mount_snapshot([target]);procs=process_snapshot([target]);services=user_services(svc_prefix)
        checks=dict(identity=ident,mounts=mounts,processes=procs,services=services)
        save('root-precheck-%02d.json'%number,checks)
        if mounts['rc'] or mounts['matches']:row['reason'].append('mount/overlay reference or findmnt failure')
        if procs['matches'] or procs['errors']:row['reason'].append('process use or privileged /proc visibility failure')
        if services['listing']['rc'] or services['show']['rc'] or target in services['show']['stdout']:row['reason'].append('active user service or failed query')
        if row['reason']:
            emit('SKIP %s %s'%(number,row['reason']));save('execution.json',result);continue
        row['df_before']=df(str(Path(target).parent));row['started']=stamp()
        hint=previous.get('root_owned_probe',{}).get('stdout','').splitlines()
        hint=hint[0] if hint else None
        unwritable_root=None
        if hint and beneath(hint,target) and Path(hint).is_dir() and not Path(hint).is_symlink() and Path(hint).lstat().st_uid==0:
            writable=command(user_prefix+['test','-w',hint])
            row['ordinary_write_check']=writable
            if writable['rc']==1:unwritable_root=hint
            elif writable['rc']!=0:raise RuntimeError('ordinary writable-directory check failed')
        row['root_used']=False
        if unwritable_root:
            row['ordinary']=dict(skipped=True,reason='root-owned directory is not writable by ordinary UID',path=unwritable_root)
            row['root_used']=True
            row['root']=delete_run(number,'root',['rm','-rf','--one-file-system','--',target])
            if row['root']['rc']!=0:raise RuntimeError('privileged rm failed; no retry')
        else:
            row['ordinary']=delete_run(number,'ordinary',user_prefix+['rm','-rf','--one-file-system','--',target])
        row['df_after_ordinary_or_direct_root']=df(str(Path(target).parent))
        if os.path.lexists(target):
            owned=remaining_root_owned(target);row['root_owned_remaining']=owned
            if not owned:
                row['status']='partial';row['reason'].append('ordinary removal incomplete without root-owned residue; no escalation')
            else:
                # Recheck all three use conditions immediately before privileged removal.
                m=mount_snapshot([target]);p=process_snapshot([target]);v=user_services(svc_prefix)
                save('root-recheck-%02d.json'%number,dict(mounts=m,processes=p,services=v))
                if m['rc'] or m['matches'] or p['matches'] or p['errors'] or v['listing']['rc'] or v['show']['rc'] or target in v['show']['stdout']:
                    row['status']='partial';row['reason'].append('residue has use/visibility problem; root removal skipped')
                else:
                    now=identity(target)
                    assert now['dev']==expected['dev'] and now['inode']==expected['inode'] and not now['symlink'] and now['realpath']==target
                    row['root_used']=True
                    row['root']=delete_run(number,'root',['rm','-rf','--one-file-system','--',target])
        row['remaining']=os.path.lexists(target);row['df_after']=df(str(Path(target).parent));row['ended']=stamp()
        row['released_bytes']=row['df_after']['available_bytes']-row['df_before']['available_bytes']
        if not row['remaining']:row['status']='deleted'
        elif row['status']=='skipped':row['status']='partial'
        emit('%s %s released_bytes=%s'%(row['status'].upper(),number,row['released_bytes']));save('execution.json',result)
        if row.get('root',{}).get('rc',0)!=0:
            raise RuntimeError('privileged rm failed; stop, preserve remaining paths')
    result['parents_after']=parent_snapshot(TARGETS)
    result['parents_unchanged']=result['parents_after']==json.loads((E/'parent-before-final.json').read_text())
    result['presence']=[dict(path=p,exists=os.path.lexists(p)) for p in TARGETS]
    assert result['parents_unchanged'],'non-target parent entries changed'
    result['status']='ok' if len(result['items'])==10 and all(r['status']=='deleted' for r in result['items']) else 'partial'
except BaseException as error:
    import traceback
    result['status']='failed';result['error']=repr(error);(E/'root-traceback.txt').write_text(traceback.format_exc())
finally:
    result['ended']=stamp();result['df_after']=df(str(Path(TARGETS[0]).parent))
    result['released_bytes']=result['df_after']['available_bytes']-result['df_before']['available_bytes']
    save('execution.json',result)
    emit('DISK_CLEANUP FINISHED status='+result['status'])
sys.exit(0 if result['status']=='ok' else 1)

PY
