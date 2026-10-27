"""Stream every payload byte; do not materialize a second install root."""
from pathlib import Path
import subprocess,hashlib,stat,json,importlib.util,sys,time
D=Path(__file__).resolve().parent;W=D.parent.parent;E=W.parent/'llvm-optimize-bolt/tools/bolt/results/runpath-fix-20261026';R=D/'gbs-root/local/BUILD-ROOTS/scratch.x86_64.0';P=W/'temp/bolt-on-hybrid-20261024/products';RP=R/'home/abuild/rpmbuild'
spec=importlib.util.spec_from_file_location('helper',D/'source/packaging/clang-bolt-helper.py');h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)
assert json.loads((E/'build-result.json').read_text())['exit_code']==0
assert len(list((RP/'RPMS/x86_64').glob('*.rpm')))==22
assert len(list((RP/'SRPMS').glob('*.rpm')))==1
out=E/'rpm-comparison';out.mkdir(exist_ok=True)
def manifest(rpm):
    p=subprocess.Popen(['rpm2cpio',str(rpm)],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    f=p.stdout;rows={};hard={};pending=[]
    def read(n):
        b=b''
        while len(b)<n:
            c=f.read(n-len(b));assert c,'short cpio read';b+=c
        return b
    while True:
        header=read(110);assert header[:6] in (b'070701',b'070702')
        v=[int(header[6+8*i:14+8*i],16) for i in range(13)]
        ino,mode,uid,gid,nlink,mtime,size,maj,min_,rmaj,rmin,namesize,check=v
        name=read(namesize).rstrip(b'\0').decode();read((-110-namesize)%4)
        if name=='TRAILER!!!':break
        hh=hashlib.sha256();remaining=size;link=b''
        while remaining:
            data=read(min(remaining,1024*1024));hh.update(data);remaining-=len(data)
            if stat.S_ISLNK(mode):link+=data
        read((-size)%4);name=name.removeprefix('./')
        row={'mode':mode,'uid':uid,'gid':gid,'bytes':size,'sha256':hh.hexdigest(),'mtime':mtime}
        if stat.S_ISLNK(mode):row['target']=link.decode()
        if stat.S_ISREG(mode) and nlink>1:
            key=(maj,min_,ino);pending.append((name,key))
            if size or key not in hard:hard[key]=(size,hh.hexdigest())
        rows[name]=row
    f.read();stderr=p.stderr.read();assert p.wait()==0,stderr
    for name,key in pending:rows[name]['bytes'],rows[name]['sha256']=hard[key]
    return rows
rows=[]
for new in sorted((RP/'RPMS/x86_64').glob('*.rpm'))+sorted((RP/'SRPMS').glob('*.rpm')):
    old=(P/('SRPMS' if new.name.endswith('.src.rpm') else 'RPMS')/new.name);assert old.is_file(),old
    a,b=manifest(old),manifest(new);assert a.keys()==b.keys(),new.name
    changed=[];times=[]
    for key in sorted(a):
        x=dict(a[key]);y=dict(b[key]);tx=x.pop('mtime');ty=y.pop('mtime')
        if tx!=ty:times.append({'path':key,'old':tx,'new':ty})
        if x!=y:
            assert all(x[k]==y[k] for k in ('mode','uid','gid')), (new.name,key,'type/mode/owner changed')
            changed.append({'path':key,'old':x,'new':y})
    allowed={'llvm.spec','clang-bolt-helper.py'} if new.name.endswith('.src.rpm') else {'usr/bin/clang-22'} if new.name.startswith('clang-22.') else set()
    result={'rpm':new.name,'old_rpm_sha256':h.digest(old),'new_rpm_sha256':h.digest(new),'old_rpm_bytes':old.stat().st_size,'new_rpm_bytes':new.stat().st_size,'paths':len(a),'changed':changed,'mtime_changes':times,'PASS':all(x['path'] in allowed for x in changed)}
    (out/(new.name+'.json')).write_text(json.dumps({'result':result,'old_files':a,'new_files':b},indent=2)+'\n');rows.append(result);(out/'summary.json').write_text(json.dumps(rows,indent=2)+'\n')
    print('RPM',new.name,'changed',len(changed),'timestamps',len(times),'PASS',result['PASS'],flush=True)
    assert result['PASS'],result
old=P/'binaries/clang.candidate';new=RP/'BUILD/llvm-22.1.8/build/clang-bolt/clang.candidate'
a,b=h.rpath_layout(old),h.rpath_layout(new)
comparison={'old_sha256':h.digest(old),'new_sha256':h.digest(new),'exclude_only':['.dynstr','.dynamic'],'old':a,'new':b,'PASS':a==b}
(out/'clang-non-path-bytes.json').write_text(json.dumps(comparison,indent=2)+'\n');assert comparison['PASS'],'clang changes outside .dynstr/.dynamic'
print('RPM_PAYLOAD_AND_ELF_PASS',flush=True)
