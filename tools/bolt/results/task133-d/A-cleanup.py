from pathlib import Path
import hashlib,json,os,shutil,stat,subprocess
W=Path('/home/linhao/Toolchain/development/llvm-optimize');B=W.with_name('llvm-optimize-bolt')
R=W/'temp/deleted-repo-backup-20261105'; E=B/'tools/bolt/results/task133-d'; prior=B/'tools/bolt/results/task131'
def load(n):
    return json.loads((prior/n).read_text())
def save(n,v):
    (E/n).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
def cmd(*args,**kw):
    return subprocess.run(args,capture_output=True,check=True,**kw).stdout
G=['/usr/bin/git','-C',str(B)]
env={**os.environ,'GIT_TERMINAL_PROMPT':'0','GIT_NO_LAZY_FETCH':'1'}
advertised=[line.split('\t') for line in cmd(*G,'ls-remote','--refs','origin','refs/heads/*','refs/tags/*',env=env,text=True,timeout=45).splitlines()]
known=set(cmd(*G,'for-each-ref','--format=%(objectname)','refs/remotes/origin',text=True).splitlines())
anchors={sha:ref for sha,ref in advertised if sha in known}
assert anchors, 'STOP: no verified remote anchor in local object store'
reachable=set(cmd(*G,'rev-list','--objects','--no-object-names',*anchors,env=env,text=True).splitlines())
candidates={}
for row in load('backup-bundles.json'):
    if row['proven']: candidates[row['bundle']]={'kind':'bundle','prior':row}
for name,proof in load('backup-duplicates.json').items():
    candidates.setdefault(name,{'kind':'bundle'})['duplicate']=proof
for row in load('backup-other-files.json'):
    if 'remote_match' in row:candidates[row['path']]={'kind':'blob','prior':row}
assert len(candidates)==76
def identity(st):
    return (st.st_dev,st.st_ino,st.st_mode,st.st_size,st.st_mtime_ns,st.st_ctime_ns)
deleted=[];blocked=[];unreadable=[];retained=[]
before=shutil.disk_usage(R).free
def onerror(exc):
    p=Path(exc.filename)
    st=p.lstat()
    unreadable.append({'path':str(p),'uid':st.st_uid,'gid':st.st_gid,'mode':oct(stat.S_IMODE(st.st_mode)),'error':str(exc)})
for base,dirs,files in os.walk(R,followlinks=False,onerror=onerror):
    for name in files:
        p=Path(base)/name
        try:
            st=p.lstat()
            row={'path':str(p),'bytes':st.st_size,'uid':st.st_uid,'gid':st.st_gid,'mode':oct(stat.S_IMODE(st.st_mode))}
            if not stat.S_ISREG(st.st_mode) or p.resolve()!=p or not p.is_relative_to(R):
                retained.append({**row,'reason':'non-regular or symlink'})
                continue
            candidate=candidates.get(str(p))
            if not candidate:
                if not os.access(p,os.R_OK):
                    unreadable.append({**row,'error':'read access denied'})
                else:
                    retained.append({**row,'reason':'not in approved list'})
                continue
            with p.open('rb') as stream:
                if candidate['kind']=='bundle' and not os.access(p.parent,os.W_OK|os.X_OK):
                    blocked.append({**row,'reason':'deletion needs write access on root-owned parent',
                                    'parent_uid':p.parent.stat().st_uid,
                                    'parent_mode':oct(stat.S_IMODE(p.parent.stat().st_mode)),
                                    'prior_proof':candidate['prior']['unproven']==0,
                                    'duplicate':candidate.get('duplicate')})
                    continue
                # Use the same open file for both hashes and identity checks.
                if candidate['kind']=='bundle':
                    retained.append({**row,'reason':'bundle deletion withheld until live ancestor proof'})
                    continue
                oid=hashlib.sha1(f'blob {st.st_size}\0'.encode())
                sha=hashlib.sha256()
                for chunk in iter(lambda:stream.read(1048576),b''):
                    oid.update(chunk);sha.update(chunk)
                expected=candidate['prior']['remote_match']['blob']
                if oid.hexdigest()!=expected or expected not in reachable:
                    retained.append({**row,'reason':'blob no longer matches reachable verified content'})
                    continue
                if identity(os.fstat(stream.fileno()))!=identity(st):
                    retained.append({**row,'reason':'file changed while checking'})
                    continue
                # Open the real parent and operate by dirfd without following the leaf.
                fd=os.open(p.parent,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
                try:
                    if identity(os.stat(name,dir_fd=fd,follow_symlinks=False))!=identity(st):
                        retained.append({**row,'reason':'file changed before unlink'})
                        continue
                    try:
                        os.unlink(name,dir_fd=fd)
                    except PermissionError as exc:
                        blocked.append({**row,'reason':str(exc),'verified_git_blob':expected})
                        continue
                finally:
                    os.close(fd)
                deleted.append({**row,'allocated_bytes':st.st_blocks*512,'sha256':sha.hexdigest(),
                                'verified_git_blob':expected,'remote_anchors':anchors})
                save('A-deleted.json',deleted)
        except PermissionError as exc:
            onerror(exc)
    for name in dirs:
        p=Path(base)/name
        if p.is_symlink():
            retained.append({'path':str(p),'reason':'directory symlink not followed'})
for name,rows in [('deleted',deleted),('blocked',blocked),('unreadable',unreadable),('retained',retained)]:
    save('A-'+name+'.json',rows)
summary={'deleted':len(deleted),'blocked':len(blocked),'unreadable':len(unreadable),'retained_other':len(retained),
         'bytes_deleted':sum(r['bytes'] for r in deleted),'allocated_bytes_deleted':sum(r['allocated_bytes'] for r in deleted),
         'df_before':before,'df_after':shutil.disk_usage(R).free,'remote_anchors':anchors}
save('A-summary.json',summary)
print(summary)
