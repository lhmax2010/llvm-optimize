from pathlib import Path
import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
import tempfile

A=Path(__file__).resolve().parent
W=A.parents[1]
SOURCE=W/'temp/deleted-repo-backup-20261105'
ARCHIVE=W/'archive/backup-unique/task160'
PRIOR=W/'archive/task149-clean2'
GIT='/usr/bin/git'
ENV={**os.environ,'GIT_OPTIONAL_LOCKS':'0','GIT_TERMINAL_PROMPT':'0'}


def invoke(repo,*args,env=ENV):
    p=subprocess.run([GIT,'-C',repo,'-c','safe.directory='+str(repo),'-c','pack.threads=2',
                      '-c','pack.windowMemory=64m',*args],env=env,capture_output=True,text=True,timeout=1800)
    if p.returncode:
        raise RuntimeError(p.stderr.strip() or p.stdout.strip() or f'git exited {p.returncode}')
    return p.stdout,p.stderr


def refs(repo):
    text,_=invoke(repo,'for-each-ref','--format=%(refname)%09%(objectname)')
    return dict(line.split('\t') for line in text.splitlines())


def identity(path):
    st=path.lstat()
    if stat.S_ISLNK(st.st_mode):
        data=os.fsencode(os.readlink(path))
        return {'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'type':'symlink'}
    if not stat.S_ISREG(st.st_mode):
        raise ValueError(f'not an ordinary file or symlink: {path}')
    with path.open('rb') as stream:
        sha=hashlib.file_digest(stream,'sha256').hexdigest()
    return {'bytes':st.st_size,'sha256':sha,'type':'file'}


def available():
    d=os.statvfs('/home')
    return d.f_bavail*d.f_frsize


def confined(p):
    if not p.is_relative_to(SOURCE) or p==SOURCE or p.parent.resolve(strict=True)!=p.parent:
        raise ValueError(f'outside the authorized directory: {p}')
    if p.lstat().st_dev!=SOURCE.stat().st_dev:
        raise ValueError(f'different filesystem: {p}')


def remove_repo(p):
    confined(p)
    if p.is_symlink() or p.resolve(strict=True)!=p:
        raise ValueError(f'aliased repository: {p}')
    mounts=Path('/proc/self/mountinfo').read_text().splitlines()
    if any(Path(re.sub(r'\\([0-7]{3})',lambda m:chr(int(m[1],8)), line.split()[4])).is_relative_to(p)
           for line in mounts):
        raise ValueError(f'mount below repository: {p}')
    for directory, dirs, files in os.walk(p,followlinks=False):
        base=Path(directory)
        if not os.access(base,os.W_OK|os.X_OK):
            raise PermissionError(base)
        if any((base/name).lstat().st_dev!=p.stat().st_dev for name in dirs+files):
            raise ValueError('repository contains another filesystem')
    command=subprocess.run(['/usr/bin/lsof','-t','+D',p],text=True,capture_output=True,timeout=30)
    if command.stdout or command.stderr or command.returncode not in (0,1):
        raise RuntimeError('repository has open files or lsof was inconclusive: '+command.stdout+command.stderr)
    shutil.rmtree(p)


def all_objects(repo):
    rows,_=invoke(repo,'cat-file','--batch-all-objects','--batch-check=%(objectname)')
    return set(rows.splitlines())


def backup(p):
    confined(p)
    start=available()
    original=refs(p)
    fsck,errors=invoke(p,'fsck','--unreachable','--no-reflogs','--full')
    lost={match[2]:match[1] for line in fsck.splitlines()
          if (match:=re.fullmatch(r'(?:unreachable|dangling) (commit|tag) ([0-9a-f]{40,64})',line))}
    if (p/'.git').exists():
        status,_=invoke(p,'status','--porcelain=v1','--untracked-files=all')
        # Worktree and index contents do not live in a bundle.
    else:
        status=''
    with tempfile.TemporaryDirectory(dir=A,prefix='verify-bundle-') as work:
        temp=Path(work)
        staging=temp/'staging.git'
        subprocess.run([GIT,'init','--quiet','--bare',staging],check=True,env=ENV)
        objects,_=invoke(p,'rev-parse','--path-format=absolute','--git-path','objects')
        objects=Path(objects.strip()).resolve(strict=True)
        if not objects.is_relative_to(SOURCE):
            raise ValueError(f'object store outside authorized backup: {objects}')
        if (objects/'info/alternates').exists():
            raise ValueError('repository has a dependent alternate object store')
        (staging/'objects/info/alternates').write_text(str(objects)+'\n')
        head=subprocess.run([GIT,'-C',p,'rev-parse','--verify','HEAD'],text=True,capture_output=True,env=ENV)
        head_id=head.stdout.strip() if head.returncode==0 else None
        if head_id and head_id not in original.values():
            lost.setdefault(head_id,'commit')
        extra={f'refs/lost/{sha}':sha for sha in sorted(lost)}
        if extra.keys() & original.keys():
            raise ValueError('temporary ref overlaps existing ref')
        combined=original|extra
        if not combined:
            raise ValueError('no commit/tag refs to bundle')
        for name,sha in sorted(combined.items()):
            invoke(staging,'update-ref',name,sha)
        bundle=ARCHIVE/'bundles'/p.relative_to(SOURCE).with_suffix('.bundle')
        bundle.parent.mkdir(parents=True,exist_ok=True)
        if bundle.exists():
            raise FileExistsError(bundle)
        invoke(staging,'bundle','create',str(bundle),*sorted(combined))
        info,error=invoke(staging,'bundle','verify',str(bundle))
        contents,_=invoke(staging,'bundle','list-heads',str(bundle))
        heads={name:sha for sha,name in (line.split(' ',1) for line in contents.splitlines())}
        assert heads==combined
        clone=temp/'clone.git'
        subprocess.run([GIT,'clone','--quiet','--mirror','--',bundle,clone],env=ENV,check=True,timeout=1800)
        assert refs(clone)==combined
        invoke(clone,'bundle','verify',str(bundle))
        missing=all_objects(p)-all_objects(clone)
        row={'repository':str(p),'original_refs':original,'lost_refs':extra,'lost_types':lost,
             'bundle':str(bundle),**identity(bundle),'verify_output':info+error,
             'fsck_stderr':errors,'objects_not_in_bundle':sorted(missing),'worktree_status':status,
             'clone_refs_exact':True}
    try:
        if missing:
            raise ValueError('standalone objects outside bundled commit/tag reachability')
        if status:
            raise ValueError('uncommitted working tree or index data')
        if refs(p)!=original:
            raise ValueError('source refs changed')
        remove_repo(p)
        row['decision']='DELETED'
    except (ValueError, OSError, RuntimeError) as error:
        row.update(decision='RETAINED',reason=str(error))
    row.update(df_before=start,df_after=available())
    return row


def main():
    start=available()
    ARCHIVE.mkdir(parents=True,exist_ok=True)
    if SOURCE.resolve(strict=True)!=SOURCE or ARCHIVE.resolve(strict=True)!=ARCHIVE:
        raise ValueError('aliased storage roots')
    initial=json.loads((PRIOR/'backup-repositories.json').read_text())['repositories']
    rows=[]
    for old in initial:
        p=Path(old['repository'])
        if p.lstat().st_uid!=os.getuid() or not os.access(p.parent,os.W_OK|os.X_OK):
            rows.append({'repository':str(p),'decision':'RETAINED',
                         'reason':'source owner or parent permissions prevent clean removal'})
            continue
        try:
            rows.append(backup(p))
        except (ValueError, OSError, RuntimeError, AssertionError, subprocess.SubprocessError) as error:
            rows.append({'repository':str(p),'decision':'RETAINED','reason':str(error)})
    files=[]
    for row in (PRIOR/'backup-non-git.tsv').read_text().splitlines():
        src, *_ = row.split('\t')
        src=Path(src)
        dst=ARCHIVE/'non-git'/src.relative_to(SOURCE)
        record={'source':str(src),'destination':str(dst)}
        try:
            confined(src)
            record.update(identity(src))
            if not os.access(src.parent,os.W_OK|os.X_OK):
                raise PermissionError(src.parent)
            dst.parent.mkdir(parents=True,exist_ok=True)
            if dst.parent.resolve(strict=True)!=dst.parent or dst.parent.stat().st_dev!=src.lstat().st_dev:
                raise ValueError('aliased target or different filesystem')
            if dst.exists() or dst.is_symlink():
                raise FileExistsError(dst)
            inode=src.lstat().st_ino
            src.rename(dst)
            assert dst.lstat().st_ino==inode and identity(dst)=={k:record[k] for k in ('bytes','sha256','type')}
            record['decision']='MOVED'
        except (OSError, ValueError) as error:
            record.update(decision='RETAINED',reason=str(error))
        files.append(record)
    data={'scope':str(SOURCE),'archive':str(ARCHIVE),'df_before':start,'df_after':available(),
          'repositories':rows,'non_git':files}
    data['df_delta']=data['df_after']-start
    (A/'evidence/backup-results.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps({'df_delta':data['df_delta'],'moved':sum(x['decision']=='MOVED' for x in files),
                      'deleted':sum(x['decision']=='DELETED' for x in rows)},indent=2))


if __name__=='__main__':
    main()
