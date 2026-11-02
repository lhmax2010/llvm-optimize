#!/bin/sh
# One authorized invocation; all privileged actions and cleanup are here.
set -eu
PATH=/usr/sbin:/usr/bin:/sbin:/bin
export PATH
LC_ALL=C
export LC_ALL
ulimit -c 0
C='/home/linhao/Toolchain/development/llvm-optimize/temp/debuglink-20261028/full-20261030/install-test-root'
E='/home/linhao/Toolchain/development/llvm-optimize/temp/debuglink-20261028/full-20261030/evidence/install-test-20261102-resume2'
export C E
mounted=0
phase=entry
run() (
    name=$1
    shift
    printf '%s STEP %s\n' "$(date -Iseconds)" "$name"
    printf '%s\n' "$@" > "$E/$name.argv"
    rc=0
    "$@" > "$E/$name.stdout" 2> "$E/$name.stderr" || rc=$?
    printf '%s\n' "$rc" > "$E/$name.exit"
    cat "$E/$name.stdout" "$E/$name.stderr"
    return "$rc"
)
audit() {
    /usr/bin/python3 -B - <<'PY_AUDIT'
import os,json
from pathlib import Path
C=Path(os.environ['C']);E=Path(os.environ['E'])
mounts=[l for l in Path('/proc/self/mountinfo').read_text().splitlines() if str(C) in l]
processes=[]
for p in Path('/proc').glob('[0-9]*'):
    try:
        links={k:os.readlink(p/k) for k in ['root','cwd','exe'] if (p/k).exists()}
        if any(x==str(C) or x.startswith(str(C)+'/') for x in links.values()):
            processes.append({'pid':int(p.name),'links':links,'cmdline':(p/'cmdline').read_bytes().decode(errors='replace').replace('\0',' ')})
    except (FileNotFoundError,ProcessLookupError,PermissionError):pass
result={'mounts':mounts,'processes':processes}
print(json.dumps(result,indent=2))
assert not mounts and not processes,'residual mount or process'
PY_AUDIT
}
cleanup() {
    rc=$?
    trap - 0 1 2 15
    set +e
    if [ "$mounted" = 1 ]; then
        run proc-umount /usr/sbin/chroot "$C" /bin/umount /proc
        urc=$?
        if [ "$urc" != 0 ]; then rc=1; fi
    fi
    run cleanup-findmnt /usr/bin/findmnt -rn -o TARGET,SOURCE,FSTYPE
    audit > "$E/cleanup-audit.stdout" 2> "$E/cleanup-audit.stderr"
    arc=$?
    cat "$E/cleanup-audit.stdout" "$E/cleanup-audit.stderr"
    if [ "$arc" != 0 ]; then rc=1; fi
    if [ "$rc" = 0 ]; then state=ok; else state=failed; fi
    printf '%s\n' "$rc" > "$E/final.exit"
    printf 'DEBUGLINK_INSTALL FINISHED %s status=%s phase=%s\n' "$(date -Iseconds)" "$state" "$phase" > "$E/final-status.txt"
    cat "$E/final-status.txt"
    exit "$rc"
}
trap cleanup 0
trap 'exit 1' 1 2 15
printf '%s\n' "$(date -Iseconds)" > "$E/root-entry.txt"
phase=precheck
run precheck-audit audit
phase=device
[ ! -L "$C/dev/null" ] && [ -c "$C/dev/null" ]
[ "$(stat -c '%t:%T:%a' "$C/dev/null")" = '1:3:666' ]
printf '%s\n' 'DEVICE_NULL_PASS existing character 1:3 mode 0666; mknod skipped'
mkdir -p "$C/var/cache/ldconfig"
phase=install
run rpm-version /usr/sbin/chroot "$C" /usr/bin/rpm --version
run rpm-initdb /usr/sbin/chroot "$C" /usr/bin/rpm --dbpath /var/lib/rpm --initdb
# Runtime libraries are explicitly copied and hashed; no dependency RPM database
# was imported. --nodeps affects dependency bookkeeping, not payload installation.
run rpm-install /usr/sbin/chroot "$C" /usr/bin/rpm --dbpath /var/lib/rpm --noplugins --nodeps -ivh /rpms/clang-22.1.8-1.x86_64.rpm /rpms/clang-debuginfo-22.1.8-1.x86_64.rpm
run rpm-installed /usr/sbin/chroot "$C" /usr/bin/rpm --dbpath /var/lib/rpm -q clang clang-debuginfo
phase=installed-identity
run installed-identity /usr/bin/python3 -B - <<'PY_HASH'
import os,json,hashlib,struct,zlib
from pathlib import Path
C=Path(os.environ['C']);E=Path(os.environ['E'])
expected={'usr/bin/clang-22':'4f08e12d499ebd492ce4951f74915ba435f57f2e380dc6f3520f24644996cb17','usr/lib/debug/usr/bin/clang-22.debug':'be17f7222b30b9aff8e9cb30847b7348c5b9897096e382518410dfb053c2f281'}
result={}
for rel,sha in expected.items():
    p=C/rel
    with p.open('rb') as f:actual=hashlib.file_digest(f,'sha256').hexdigest()
    assert actual==sha,(rel,actual)
    result[rel]={'sha256':actual,'bytes':p.stat().st_size,'mode':oct(p.stat().st_mode&0o777)}
assert result['usr/lib/debug/usr/bin/clang-22.debug']['mode']=='0o644'
data=(C/'usr/bin/clang-22').read_bytes();h=struct.unpack_from('<16sHHIQQQIHHHHHH',data);off,ent,n,ni=h[6],h[11],h[12],h[13]
sections=[struct.unpack_from('<IIQQQQIIQQ',data,off+i*ent) for i in range(n)]
ss=sections[ni];names=data[ss[4]:ss[4]+ss[5]]
lookup={names[s[0]:names.index(b'\0',s[0])].decode():s for s in sections}
assert '.note.gnu.build-id' not in lookup
s=lookup['.gnu_debuglink'];raw=data[s[4]:s[4]+s[5]];end=raw.index(b'\0');crc=struct.unpack_from('<I',raw,(end+4)&~3)[0]
assert raw[:end]==b'clang-22.debug';assert crc==zlib.crc32((C/'usr/lib/debug/usr/bin/clang-22.debug').read_bytes())==1776780033
result['debuglink_crc32']=crc;result['build_id']='absent, same as 39'
(E/'installed-identity.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
PY_HASH
phase=proc
run proc-mount /usr/sbin/chroot "$C" /bin/mount -n -t proc none /proc
mounted=1
run proc-findmnt /usr/bin/findmnt -R "$C/proc"
phase=lldb
run lldb-auto /usr/bin/timeout 180 /usr/sbin/chroot "$C" /usr/bin/env -u LLVM_SYMBOLIZER_PATH LLDB_DEBUGSERVER_PATH=/usr/bin/lldb-server /usr/bin/lldb --no-lldbinit --batch -s /probe/install-20261102/probe.lldb
phase=symbolization
run symbolize-check /usr/bin/python3 -B - <<'PY_SYMBOLS'
import os,re,json,subprocess
from pathlib import Path
C=Path(os.environ['C']);E=Path(os.environ['E']);text=(E/'lldb-auto.stdout').read_text()
assert '/usr/bin/clang-22 /usr/lib/debug/usr/bin/clang-22.debug' in text,'no auto-loaded symbol file'
assert 'stop reason = signal SIGILL' in text,'expected real crash not observed'
bt=text.split('(lldb) bt all\n',1)[1].split('(lldb) image list',1)[0]
frames=[]
for line in bt.splitlines():
    if 'frame #' not in line or 'clang-22' not in line:continue
    m=re.search(r'frame #(\d+): (0x[0-9a-fA-F]+) clang-22`(.+)',line)
    assert m,('unnamed clang frame',line)
    name=re.sub(r' \+ \d+$','',m[3]);assert 'unnamed_symbol' not in name and name!='??'
    frames.append({'frame':int(m[1]),'absolute':m[2],'lldb_name':name})
assert len(frames)>=20,('too few clang frames',len(frames))
slide_line=[l for l in text.split('(lldb) image list -o -f -s\n',1)[1].splitlines() if '/usr/bin/clang-22' in l][0]
slide=int(re.search(r'0x[0-9a-fA-F]+',slide_line)[0],16)
samples=json.loads((E/'symbol-samples.json').read_text())
for f in frames:f['offset']=hex(int(f['absolute'],16)-slide)
addresses=[f['offset'] for f in frames]+[s['address'] for s in samples]
argv=['/usr/sbin/chroot',str(C),'/opt/symbolizer/llvm-symbolizer','--obj=/usr/lib/debug/usr/bin/clang-22.debug','--no-inlines','--demangle']
(E/'symbolizer.argv.json').write_text(json.dumps(argv,indent=2)+'\n');(E/'symbolizer.stdin').write_text('\n'.join(addresses)+'\n')
p=subprocess.run(argv,input='\n'.join(addresses)+'\n',text=True,capture_output=True,timeout=90)
(E/'symbolizer.stdout').write_text(p.stdout);(E/'symbolizer.stderr').write_text(p.stderr);assert p.returncode==0,p.stderr
blocks=[b.splitlines() for b in p.stdout.strip().split('\n\n')];assert len(blocks)==len(addresses),(len(blocks),len(addresses))
for f,block in zip(frames,blocks):
    f['symbolizer_name']=block[0];assert block[0]==f['lldb_name'],f
for i,s in enumerate(samples):
    part=text.split('(lldb) image lookup -a '+s['address']+'\n',1)[1].split('(lldb)',1)[0]
    m=re.search(r'Summary: clang-22`(.+)',part);assert m,('no LLDB sample',s)
    name=re.sub(r' \+ \d+$','',m[1]);resolved=blocks[len(frames)+i][0]
    assert name==resolved and name!='??',(s,name,resolved)
    s['lldb_name']=name;s['symbolizer_name']=resolved
result={'PASS':True,'automatic_debug_file':'/usr/lib/debug/usr/bin/clang-22.debug','crash':'SIGILL','clang_frames':len(frames),'named_clang_frames':len(frames),'slide':hex(slide),'frames':frames,'samples':samples,'cold_samples':sum('.cold' in s['selected_name'] for s in samples),'source_line_information':False}
(E/'symbolization-result.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
PY_SYMBOLS
phase=complete
