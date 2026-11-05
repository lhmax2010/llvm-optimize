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
