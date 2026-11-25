from pathlib import Path
import difflib, json, os, re, subprocess

A = Path(__file__).resolve().parent
W = A.parents[1]
B = W.with_name(W.name + "-bolt")
E = A / "evidence"
PREVIOUS = W / "archive/task153"
REPO = PREVIOUS / "ps6-suggestions.git"
PS6 = "06f3424c543a9645707f9afbbd9b5318280fffeb"
BASE = "f346dd75e87de324dc2abe61454ca1c49969d12d"
P1, P2, P3, OLD_P4 = (r["commit"] for r in json.loads((PREVIOUS/"evidence/patches.json").read_text()))
SPEC = "packaging/llvm.spec"
IDENTITY = dict(GIT_AUTHOR_NAME="Hao Lin", GIT_COMMITTER_NAME="Hao Lin",
                GIT_AUTHOR_EMAIL="hao.lin@samsung.com", GIT_COMMITTER_EMAIL="hao.lin@samsung.com")
INDEX = {**os.environ, **IDENTITY, "GIT_INDEX_FILE": str(A/"index")}

def git(*args, data=None):
    return subprocess.check_output(["/usr/bin/git", "-C", str(REPO), *args], input=data, env=INDEX)

def show(commit, file):
    return git("show", commit + ":" + file).decode()

def replace(text, before, after):
    if text.count(before) != 1:
        raise ValueError(f"unexpected starting text: {before}")
    return text.replace(before, after, 1)

def commit(parent, title, spec=None):
    git("read-tree", parent)
    if spec is not None:
        blob = git("hash-object", "-w", "--stdin", data=spec.encode()).decode().strip()
        git("update-index", "--cacheinfo", f"100644,{blob},{SPEC}")
    tree = git("write-tree").decode().strip()
    return git("commit-tree", tree, "-p", parent, data=(title.rstrip()+"\n").encode()).decode().strip()

def evidence(path, text):
    (E/path).write_text(text)

def json_out(path, value):
    evidence(path, json.dumps(value,indent=2,ensure_ascii=False)+"\n")

def selected_source(path, ranges=(), commit_id=PS6):
    lines = show(commit_id,path).splitlines()
    return path+"\n"+"".join(f"{i:4}  {line}\n" for i,line in enumerate(lines,1)
                                if not ranges or any(lo<=i<=hi for lo,hi in ranges))

assert git("rev-parse", "refs/heads/ps6-suggestions").decode().strip() == OLD_P4
assert git("rev-parse", PS6+"^",P1+"^",P2+"^",P3+"^").decode().splitlines() == [BASE,PS6,P1,P2]
old = show(P3,SPEC)
p5spec = replace(old, "%{_prefix}/bin/scan-view\n", "%{_prefix}/bin/scan-view\n%{_datadir}/scan-view\n")
p5spec = replace(p5spec, "%{_prefix}/share/*\n", "%{_prefix}/share/*\n"
                 "%exclude %{_datadir}/scan-build\n"
                 "%exclude %{_datadir}/scan-view\n"
                 "%exclude %{_mandir}/man1/scan-build.1*\n")
p5spec = replace(p5spec, "%{_prefix}/bin/scan-build-py\n", "%{_prefix}/bin/scan-build-py\n"
                 "%{_datadir}/scan-build\n%{_mandir}/man1/scan-build.1*\n")
assert p5spec.split("\n%files",1)[0]==old.split("\n%files",1)[0]

# Both retained builds must prove that the two explicit removals followed installation.
install_re = re.compile(r"-- Installing: \S*?(/usr/lib/(?:libear|libscanbuild)/\S+)\s*$")
rm_re = re.compile(r"\+ rm -rf [^\n]*?/usr/lib/(libear|libscanbuild)/")
logs = {
    "B1": W/"archive/task144/b1-a1/rpm-build.log",
    "N2": B/"tools/bolt/results/task149-run/N2-rpm-build.txt",
}
observed = {}
for name, path in logs.items():
    install, removed, selections = {}, {}, []
    with path.open(errors="replace") as lines:
        for i,line in enumerate(lines,1):
            install_match=install_re.search(line)
            remove_match=rm_re.search(line)
            if install_match:
                install[install_match[1]]=i
            if remove_match:
                removed[remove_match[1]]=i
            if install_match or remove_match:
                selections.append(f"{i}: {line}")
    assert len(install)==14 and set(removed)=={"libscanbuild","libear"}
    assert all(line < removed[name.split('/')[3]] for name,line in install.items())
    evidence(f"{name}-module-install-and-delete.txt",f"{path}\n"+"".join(selections))
    observed[name]={"path":str(path),"installed":install,"deletion_lines":removed}
paths = set(observed["B1"]["installed"])
assert paths==set(observed["N2"]["installed"])
json_out("module-install-history.json", observed)
p6spec = replace(p5spec, "rm -rf %{buildroot}/usr/lib/libear/*\n"
                 "rm -rf %{buildroot}/usr/lib/libscanbuild/*\n", "")
p6spec = replace(p6spec, "%{_prefix}/libexec/intercept-cc\n",
                 "%{_prefix}/libexec/intercept-cc\n%{_prefix}/lib/libscanbuild\n%{_prefix}/lib/libear\n")

source = []
for file,ranges in [
    ("clang/tools/scan-build/CMakeLists.txt", [(31,36),(68,94)]),
    ("clang/tools/scan-build/bin/scan-build", [(111,125),(446,469),(893,911),(941,948),(1909,1925)]),
    ("clang/tools/scan-view/CMakeLists.txt", [(1,12),(27,39)]),
    ("clang/tools/scan-view/bin/scan-view", []),
    ("clang/tools/scan-view/share/ScanView.py", [(8,17),(447,460),(749,759)]),
    ("clang/tools/scan-build-py/CMakeLists.txt", []),
    ("clang/tools/scan-build-py/bin/analyze-build", [(1,17)]),
    ("clang/tools/scan-build-py/bin/intercept-build", [(1,17)]),
    ("clang/tools/scan-build-py/bin/scan-build", [(1,17)]),
    ("clang/tools/scan-build-py/lib/libscanbuild/intercept.py", [(23,36)]),
    ("clang/tools/scan-build-py/lib/libscanbuild/report.py", [(1,65)]),
]:
    source.append(selected_source(file, ranges))
source.append(selected_source(SPEC, [(753,764)], P3))
evidence("source-excerpts.txt","\n".join(source))

p5 = commit(P3, "packaging: ship analyzer data with their tools", p5spec)
p6 = commit(p5, "packaging: retain scan-build-py runtime modules", p6spec)
message=git("cat-file","commit",OLD_P4).partition(b"\n\n")[2].decode("ascii")
header, rest = message.split("\n\nBuild BOLT",1)
body, p2_body, p3_body, p4_body, trailers = ("Build BOLT"+rest).rstrip("\n").split("\n\n")
assert p3_body.startswith("clang now ships ") and trailers.startswith("Change-Id:")
new_p3="""clang now ships scan-build, scan-build-py, analyze-build and
intercept-build together with the libexec scripts, the report
resources and the Python modules they use, and llvm ships the
scan-view data next to scan-view. llvm and clang provide the
llvm-xray, llvm-prof-tools and clang-analyzer names and obsolete
their older versions."""
new_body="\n\n".join((body,p2_body,new_p3,p4_body))
new_message="\n\n".join((header,new_body,trailers))+"\n"
p4=commit(p6,new_message)
assert git("cat-file","commit",p4).partition(b"\n\n")[2].decode()==new_message
assert not git("diff",p6,p4)
banned=re.compile(r'github|lhmax|llvm-optimize|sandbox|bolt-v4|codex|claude|openai|\b(?:chatgpt|cline|copilot|ai)\b|\btask[ _-]*\d{1,4}\b|\d{1,4}\s*号|/home/',re.I)
gates={"ascii_body":new_body.isascii(),"columns":max(map(len,new_body.splitlines())),
       "forbidden_body":banned.findall(new_body),"preserves_header_trailers":True,"changed_paragraphs":[3]}
assert gates["ascii_body"] and gates["columns"]<=72 and not gates["forbidden_body"]
json_out("message-gates.json",gates)
evidence("suggested-commit-message.txt",new_message)
evidence("p4-message.diff","".join(difflib.unified_diff(message.splitlines(True),new_message.splitlines(True),"153 P4","154 P4")))
evidence("parent-to-p6.diff",git("diff","--full-index",BASE,p6).decode())
evidence("p6-llvm.spec",p6spec)
evidence("p5-llvm.spec",p5spec)
evidence("p3-llvm.spec",old)
rows=[]
for i,(number,rev) in enumerate(zip((1,2,3,5,6,4),(P1,P2,P3,p5,p6,p4)),1):
    name=f"{i:04d}-suggestion-{number}.patch"
    patch = git("format-patch","--always","--no-signature","--full-index","--stdout","-1",rev)
    (E/name).write_bytes(patch)
    rows.append({"patch":number,"commit":rev,"file":name,
                 "tree":git("rev-parse",rev+"^{tree}").decode().strip(),
                 "diffstat":git("diff","--stat",rev+"^",rev).decode().strip()})
json_out("series.json",rows)
print(json.dumps(rows,indent=2))
