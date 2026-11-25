from pathlib import Path
import json, os, re, subprocess, sys

A=Path(__file__).resolve().parent
W=A.parents[1]
B=W.with_name(W.name+"-bolt")
E=A/"evidence"
sys.path.insert(0,str(A/"bench"))
from bench import available, digest, memory_guard, write_json
N2=W/"archive/task149-run/resume/N2"
QB=B/"tools/bolt/results/qb-1232862-1232863"
G="/usr/bin/git"
R="/usr/bin/rpm"
CACHE=N2/"gbs-driver/local/cache/0cfb488eb037482dedd4b54a2239d81d"
ENV={**os.environ,"LC_ALL":"C","LD_LIBRARY_PATH":"","LD_PRELOAD":""}

def read(p):
    return json.loads(p.read_text())
def note(p,want=None):
    memory_guard()
    sha=digest(p)
    if want:
        assert p.stat().st_size==want["bytes"] and sha==want["sha256"],p
    return {"path":str(p),"sha256":sha,"bytes":p.stat().st_size}
def call(cmd):
    return subprocess.check_output(list(map(str,cmd)),text=True,env=ENV)
def extract(p,root,*patterns):
    memory_guard()
    with subprocess.Popen(["/usr/bin/rpm2cpio",str(p)],stdout=subprocess.PIPE,env=ENV) as c:
        q=subprocess.run(["/usr/bin/cpio","-idmu","--quiet","--no-absolute-filenames","--",*patterns],
                         cwd=root,stdin=c.stdout,env=ENV,check=True)
        c.stdout.close()
        assert c.wait()==0,p
def get_rpm(filename,tests=None):
    p=CACHE/filename
    return p,note(p,tests)
def qbrecord(build,release):
    return read(QB/"downloads"/str(build)/"x86_64"/f"clang-22.1.8-{release}.x86_64.rpm.json")
def elf_closure(loader,args,root):
    out=call([loader,*args,"--list",root/"usr/bin/clang-22"])
    found=[]
    for line in out.splitlines():
        match=re.search(r"(?:=>\s+)?(/[^\s]+)\s+\(0x[0-9a-f]+\)",line)
        if match:
            lib=Path(match[1])
            assert lib.resolve(strict=True).is_relative_to(root),line
            found.append(note(lib))
        elif "not found" in line or "=>" in line:
            raise RuntimeError(f"unresolved target library: {line}")
    assert found and any(Path(r["path"]).name=="libc.so.6" for r in found),out
    return out,found

def main():
    n2=next(r for r in read(B/"tools/bolt/results/task149-run/N2-rpm-identities.json") if Path(r["path"]).name=="clang-22.1.8-1.x86_64.rpm")
    qb=qbrecord(1232863,"2.1")
    alternate=qbrecord(1232862,"5.1")
    alt=note(Path(alternate["path"]),alternate)
    target={k:get_rpm(n) for k,n in {
        "glibc":"glibc-2.40-1.6.x86_64.rpm","libgcc":"libgcc-14.2.0-1.6.x86_64.rpm",
        "libstdc++":"libstdc++-14.2.0-1.6.x86_64.rpm","zlib":"zlib-1.3.1-1.6.x86_64.rpm"}.items()}
    inventory = {}
    tiny=A/"smoke.c"
    tiny.write_text("int add(int a, int b) { return a + b; }\n")
    private=A/"private"
    private.mkdir(exist_ok=True)
    for name,record in (("V0",n2),("V1",qb)):
        root=private/name
        root.mkdir()
        p=Path(record["path"])
        row={"source_rpm":note(p,record),"root":str(root),
             "source_rpm_vcs":call([R,"-qp","--qf","%{VCS}",p]),
             "runtime_provider_rpms":[r for _,r in target.values()],"status":"FAIL"}
        try:
            extract(p,root,"./usr/bin/clang-22")
            clang=root/"usr/bin/clang-22"
            section=call(["/usr/bin/readelf","-W","-S",clang])
            dynamic=call(["/usr/bin/readelf","-W","-d",clang])
            (E/f"{name}-sections.txt").write_text(section)
            (E/f"{name}-dynamic.txt").write_text(dynamic)
            bolted=[m[1] for m in re.finditer(r"(?mi)^\s*\[\s*\d+\]\s+(\S*bolt\S*)\s+",section)]
            row.update(clang=str(clang),sha256=digest(clang),clang_bytes=clang.stat().st_size,
                       bolt_sections=bolted,has_bolt_sections=bool(bolted))
            for lib,_ in target.values():
                extract(lib,root,"./lib64/*","./usr/lib64/*")
            loader=next(p for p in (root/"lib64/ld-linux-x86-64.so.2",root/"usr/lib64/ld-linux-x86-64.so.2") if p.is_file())
            library_path=[str(root/"lib64"),str(root/"usr/lib64")]
            loader_args=["--inhibit-cache","--library-path",":".join(library_path)]
            linked,closure=elf_closure(loader,loader_args,root)
            (E/f"{name}-loader-list.txt").write_text(linked)
            row.update(loader=str(loader),loader_sha256=digest(loader),library_path=library_path,library_closure=closure)
            args=[loader,*loader_args,clang,"--no-default-config","-fintegrated-cc1"]
            command=[*args,"--target=x86_64-tizen-linux-gnu","-O2","-c",tiny,"-o",root/"smoke.o"]
            for key,argv in (("version",[ *args,"--version"]),("compile",command)):
                memory_guard()
                run=subprocess.run(list(map(str,argv)),env=ENV,capture_output=True,text=True,timeout=90)
                row[key]={"command":list(map(str,argv)),"rc":run.returncode,"stdout":run.stdout,"stderr":run.stderr}
                if run.returncode:
                    raise RuntimeError(f"{name} {key} returned {run.returncode}: {run.stderr}")
            row["smoke_object"]=note(root/"smoke.o")
            row["status"]="PASS"
        except (RuntimeError,AssertionError,OSError,StopIteration,subprocess.SubprocessError) as ex:
            row["error"]=str(ex)
        inventory[name]=row
        write_json(E/"variants-partial.json",inventory)
    inventory["V2"]={"status":"PENDING","optimization":"PGO only"}
    inventory["V3"]={"status":"PENDING","optimization":"PGO and BOLT"}
    identity={"V0":"N2 PS5 with llvm_speedup off","V1":"QB 1232863 Toolchain x86_64, H4",
              "alternate_1232862_rpm":alt,"qb_h4_verified":read(QB/"source-tree.json"),
              "alternate_use":"Recorded but not used as a fifth benchmark variant",
              "runtime_source":"N2's frozen Tizen toolchain snapshot RPM cache, shared by both private roots",
              "source_delta_h4_to_ps5":call([G,"-C",W/"archive/task151/llvm-review.git","diff","--name-status",
                     "7a7bc17467d4c5da9763e86e3c74a123b3ff0df2","7b05a13744d1cf81a5e9cff22a27eb037bf1b6a8"])}
    write_json(E/"variant-provenance.json",identity)
    write_json(E/"variants.json",inventory)
    print({name:(row["status"],row.get("bolt_sections"),row.get("error")) for name,row in inventory.items()})
    return any(inventory[n]["status"]!="PASS" for n in ("V0","V1"))

if __name__=="__main__":
    raise SystemExit(main())
