"""Read the exact Toolchain QB, verify its artifacts, and inspect package evidence."""
from collections import deque
from concurrent.futures import ThreadPoolExecutor
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import subprocess
import sys
from urllib.error import HTTPError
from urllib.parse import urljoin, urlparse
from urllib.request import urlopen
from xml.etree import ElementTree

A = Path(__file__).resolve().parent
W = A.parents[1]
B = W.with_name(W.name+"-bolt")
E = A/"evidence"
ART = A/"artifacts"
BUILD = "1242771"
REV = "a752ddf8e826ab70bffe2354619a7f9977513764"
BRANCH = "sandbox/lhmax2025/llvm-pgo-bolt-20261127-2"
PROJECT = "Tizen-Base-Toolchain"
BASE = "https://download.tizen.org/RBS/TIZEN/Tizen/" + PROJECT + "/tizen-base-toolchain_20261127.093703"
NODE = "/home/linhao/.local/bin/node"
CLIENT = W/"archive/task164/qb-read.mjs"
ARCHES = ("x86_64","aarch64","armv7l")
PACKAGES = ("clang","clang-devel","compiler-rt","libllvm","libomp","libomp-devel",
            "lldb","lldb-devel","llvm","llvm-devel","llvm-static-devel","python-clang")
SKILL = B/"tools/skills/tizen-llvm-offline-profile/scripts"
READELF = "/usr/bin/readelf"
TERMINAL = {"Successful","Failed","Cancelled","Canceled","Timed Out","Stopped"}
STAMP = re.compile(r"^\[\s*\d+s\]\s?")
GOOD_MARKERS = ("BOLT_PIPELINE_PASS","BOLT_REAL_GATE_PASS","BOLT_POST_GATE_PASS",
                "PGO_NINJA_CHECK","PGO_RUNTIME_CHECK","PGO_MATCH","NATIVE_ARCHIVES_END")
GATE_COUNTS = re.compile(r'"counts"\s*:\s*(\{[^{}]{0,1600}"S_over_N"\s*:\s*[^{}]{1,240}\})')
SECTION = re.compile(r"^\s*\[\s*\d+\]\s+(\S+)\s+\S+\s+[\da-f]+\s+[\da-f]+\s+([\da-f]+)\b",re.I)


class FilesPending(RuntimeError):
    pass


def read(path):
    return json.loads(path.read_text())


def save(path, obj):
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+"\n")
    tmp.replace(path)


def record(path):
    with path.open("rb") as f:
        digest = hashlib.file_digest(f,"sha256").hexdigest()
    return {"path":str(path),"bytes":path.stat().st_size,"sha256":digest}


def ensure_dirs():
    E.mkdir(exist_ok=True)
    ART.mkdir(exist_ok=True)


def overview():
    ensure_dirs()
    target = A/"qb-current.json"
    argv = [NODE,str(CLIENT),"view",f"/build/{BUILD}",str(target)]
    p = subprocess.run(argv,text=True,capture_output=True,timeout=200)
    if p.returncode:
        (A/"qb-read-last-error.txt").write_text(p.stdout+p.stderr)
        raise FilesPending("QB overview read failed, see qb-read-last-error.txt")
    d = read(target)
    fields = {r[0].strip():r[1].strip() for r in d["tables"] if len(r)==2}
    row = next(r for r in d["tables"] if len(r)>=4 and r[0]==BUILD)
    children = [r[:4] for r in d["tables"] if r and re.fullmatch(r"standard-.*",r[0])]
    if (fields.get("Build Package List")!=f"platform/upstream/llvm@{REV}" or
            f"/{PROJECT}/RBS/TRIGGER " not in d["title"] or
            not d["title"].endswith("20261127.093703")):
        raise ValueError("QB overview is not the requested source identity")
    published = fields.get("Download_URL","").rstrip("/")
    if published.startswith(("http:","https:")) and published.replace("http:","https:",1)!=BASE:
        raise ValueError("published URL differs from the matched QB root")
    out={"id":BUILD,"project":PROJECT,"branch":BRANCH,"revision":REV,"overall":row[1],
         "started_qb_clock":row[2],"duration":row[3].strip(),"children":children,
         "download":published,"manifest":fields.get("Manifest_URL"),"public_root":BASE}
    return out


def get(url, dest, timeout=90):
    if not url.startswith(BASE+"/"):
        raise ValueError(f"refusing URL outside the matched QB artifacts: {url}")
    dest.parent.mkdir(parents=True,exist_ok=True)
    if not dest.exists():
        tmp=dest.with_suffix(".part")
        with urlopen(url,timeout=timeout) as inp, tmp.open("wb") as out:
            remote=urlparse(inp.geturl())
            if remote.scheme!="https" or remote.hostname!="download.tizen.org":
                raise ValueError("artifact escaped download.tizen.org")
            while data := inp.read(1024*1024):
                out.write(data)
        tmp.replace(dest)
    return {**record(dest),"url":url}


def package_log(machine):
    missing={}
    for bucket in ("succeeded","failed","unresolvable","excluded"):
        url=f"{BASE}/builddata/buildlogs/standard/{machine}/{bucket}/llvm.buildlog.txt"
        try:
            artifact=get(url,ART/(machine+"."+bucket+".buildlog.txt"))
        except HTTPError as error:
            if error.code!=404:
                raise
            missing[bucket]=error.code
            continue
        return {"bucket":bucket,"artifact":artifact}
    raise FilesPending(f"{machine} worker package log not published: {missing}")


def archive_logs():
    basename = BASE.rsplit("/",1)[1]
    try:
        get(f"{BASE}/builddata/manifest/{basename}_standard.xml",E/"standard-manifest.xml")
    except HTTPError as error:
        if error.code==404: raise FilesPending("source manifest not published") from error
        raise
    sources = [p.get("revision") for p in ElementTree.parse(E/"standard-manifest.xml").iter("project")
               if p.get("name")=="platform/upstream/llvm"]
    if REV not in sources:
        raise ValueError(f"exact source revision absent from published manifest: {sources}")
    receipts = {}
    for machine in ARCHES:
        receipts[machine] = package_log(machine)
    save(E/"package-log-identities.json",receipts)
    return receipts


def early_error(body):
    if re.search(r"(^|\s)(?:clang-bolt-helper\.py: error:|BOLT_GATE_FAILED:)",body):
        if "BOLT_DISK_DIAGNOSIS" not in body:
            return "helper"
    if re.match(r"(?:FAILED\s*[:\[]|CMake Error|ninja: error:)",body):
        if not re.search(r"TryCompile|CMakeTmp|CMakeScratch",body):
            return "compile/configure/link"
    if re.search(r"fatal error:|LLVM ERROR:|ld\.lld: error:|collect2: error:",body):
        if not re.search(r"TryCompile|CMakeTmp|CMakeScratch",body):
            return "compile/configure/link"
    for needle,stage in (("Bad exit status","RPM scriptlet"),("Installed (but unpackaged)","RPM packaging"),
                         (" nothing provides ","dependency resolution"),("unresolvable:","dependency resolution"),
                         ("No space left on device","disk")):
        if needle in body and not body.startswith("+"):
            return stage
    return None


def log_details(machine, item):
    path=Path(item["artifact"]["path"])
    previous=deque(maxlen=40)
    error=None
    tail=[]
    gates, retries, matches, argv=[],[],[],[]
    phase="build worker preparation"
    start,end,target = [],[],[]
    with path.open("rb") as f:
        for i, raw in enumerate(f,1):
            content=raw.decode("utf-8",errors="replace").rstrip("\n")
            line=STAMP.sub("",content)
            if line.startswith("Building llvm for project"):
                target.append(line)
            if 'started "build llvm.spec"' in line: start.append(content)
            if any(x in line for x in ('finished "build llvm.spec"','failed "build llvm.spec"')): end.append(content)
            stage=re.match(r"Executing\((%[^)]+)\)",line)
            if stage:
                phase=stage[1]
            if line.startswith(GOOD_MARKERS):
                gates.append({"line":i,"text":content})
            if line.startswith("ARCHIVE_MEMBER_RETRY "):
                retries.append({"line":i,"text":content})
            if "-stale-threshold" in line:
                argv.append({"line":i,"observed":sorted(set(re.findall(r"(?<!\w)-stale-threshold(?:=| )\d+",line))),
                             "infer_stale":bool(re.search(r"[-=]infer-stale",line))})
            if '"counts"' in line:
                for m in GATE_COUNTS.finditer(line):
                    matches.append({"line":i,"counts":json.loads(m[1])})
            if item["bucket"] != "succeeded":
                category=early_error(line)
                if error is None and category:
                    error={"line":i,"phase":phase,"category":category,"text":content,
                           "first_context_line":i-len(previous)}
                    tail=[*previous,raw]
                elif error and i<=error["line"]+40:
                    tail.append(raw)
                previous.append(raw)
    if target and not any(PROJECT in row and f"arch '{machine}'" in row for row in target):
        raise ValueError(f"log belongs to a different project or architecture: {path}")
    if error:
        error["last_context_line"]=error["first_context_line"]+len(tail)-1
        (E/(machine+"-first-error-40x40.txt")).write_bytes(b"".join(tail))
    threshold = sorted({opt for observation in argv for opt in observation["observed"]})
    status = {"succeeded":"PASS","failed":"FAIL","excluded":"EXCLUDED","unresolvable":"UNRESOLVABLE"}[item["bucket"]]
    if status=="PASS" and not any("finished" in line for line in end):
        raise ValueError(f"unexpected success log trailer for {machine}")
    return {"status":status,"start":start,"end":end,"identity_lines":target,"error":error,"gates":gates,
            "archive_member_retry":retries,"bolt_counts":matches,"bolt_argv_markers":argv,
            "observed_threshold_options":threshold}


def audit_logs(receipts):
    audit={arch:log_details(arch,r) for arch,r in receipts.items()}
    save(E/"package-log-audit.json",audit)
    x=audit["x86_64"]
    (E/"x86_64-gates.txt").write_text("".join(f"{r['line']}: {r['text']}\n"
        for r in sorted([*x["gates"],*x["archive_member_retry"]],key=lambda o:o["line"])))
    return audit


class Listing(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links=[]
    def handle_starttag(self,tag,attrs):
        if tag=="a" and (href:=dict(attrs).get("href")):
            self.links.append(href)


def download_rpms():
    idx=BASE+"/repos/standard/packages/x86_64/"
    get(idx,E/"x86_64-rpm-index.html")
    listing=Listing()
    listing.feed((E/"x86_64-rpm-index.html").read_text())
    requests=[]
    for name in PACKAGES:
        copies=[file for file in listing.links if re.fullmatch(
            re.escape(name)+r"-22\.1\.8-[0-9.]+\.x86_64\.rpm",file)]
        if len(copies)!=1:
            raise FilesPending(f"expected one x86_64 RPM for {name}: {copies}")
        file=copies[0]
        requests.append((name,urljoin(idx,file),ART/"rpms"/file))
    def fetch(args):
        name,url,where=args
        proof=get(url,where,timeout=180)
        fields=subprocess.check_output(["/usr/bin/rpm","-qp","--qf","%{NAME}\n%{ARCH}\n%{SOURCERPM}\n%{VCS}\n",
                                        where],text=True).splitlines()
        if fields[:2]!=[name,"x86_64"] or fields[3]!=f"platform/upstream/llvm#{REV}":
            raise ValueError(f"unexpected RPM header for {name}: {fields}")
        return name, {**proof,"sourcerpm":fields[2],"vcs":fields[3]}
    with ThreadPoolExecutor(max_workers=4) as pool:
        data=dict(pool.map(fetch,requests))
    if len({r["sourcerpm"] for r in data.values()})!=1:
        raise ValueError("RPMs were made from different source packages")
    save(E/"rpm-downloads.json",data)
    return data


def extract(rpm, root, paths=()):
    root.mkdir(parents=True,exist_ok=True)
    argv=["/usr/bin/cpio","-idmu","--quiet","--no-absolute-filenames","--",*paths]
    with subprocess.Popen(["/usr/bin/rpm2cpio",str(rpm)],stdout=subprocess.PIPE) as cpio:
        subprocess.run(argv,stdin=cpio.stdout,cwd=root,check=True)
        cpio.stdout.close()
        if cpio.wait():
            raise ValueError(f"rpm2cpio failed: {rpm}")


def read_sections(path, name):
    text=subprocess.check_output([READELF,"-W","-S",path],text=True)
    (E/(name+"-sections.txt")).write_text(text)
    sections={match[1]:int(match[2],16) for line in text.splitlines()
              if (match:=SECTION.match(line)) and (match[1]==".text" or "bolt" in match[1].lower())}
    if ".text" not in sections:
        raise ValueError(f"missing .text in {name}")
    return {**record(path),"sections":sections}


def elf_check(data):
    sys.path.insert(0,str(SKILL))
    from runtime_dep_check import audit
    root=ART/"payload"
    verified=ART/"payload-complete.json"
    if not verified.exists():
        for r in data.values():
            extract(Path(r["path"]),root)
        save(verified,{k:v["sha256"] for k,v in data.items()})
    if read(verified)!={k:v["sha256"] for k,v in data.items()}:
        raise ValueError("extraction receipt differs from verified RPM hashes")
    result=audit(root,READELF)
    save(E/"runtime-elf-audit.json",result)
    source=W/"archive/task168/run/manifest.json"
    v3=read(source)["variants"]["V3"]
    local=read_sections(Path(v3["clang"]),"V3")
    if local["sha256"]!=v3["sha256"]:
        raise ValueError("local V3 differs from the tested compiler")
    product=read_sections(root/"usr/bin/clang-22","V3q")
    if not any("bolt" in n.lower() for n in product["sections"]):
        raise ValueError("QB compiler lacks BOLT sections")
    result={"same_sha256":local["sha256"]==product["sha256"],"V3":local,"V3q":product}
    save(E/"clang-comparison.json",result)
    return result


if __name__=="__main__":
    f=overview()
    print(f)
    if f["overall"] in TERMINAL:
        print({k:v["status"] for k,v in audit_logs(archive_logs()).items()})
