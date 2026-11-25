from pathlib import Path
import difflib,json,os,re,subprocess

A=Path("/home/linhao/Toolchain/development/llvm-optimize/archive/task153")
E=A/"evidence"
PS6="06f3424c543a9645707f9afbbd9b5318280fffeb"
BASE="f346dd75e87de324dc2abe61454ca1c49969d12d"
NAME="Hao Lin"
EMAIL="hao.lin@samsung.com"
AUTHOR_ENV={**os.environ,"GIT_AUTHOR_NAME":NAME,"GIT_AUTHOR_EMAIL":EMAIL,
            "GIT_COMMITTER_NAME":NAME,"GIT_COMMITTER_EMAIL":EMAIL,
            "GIT_INDEX_FILE":str(A/"prepare-index")}
REPO=A/"ps6-suggestions.git"
SPEC="packaging/llvm.spec"
CPP="bolt/lib/Target/X86/X86BoltMnemonicTables.cpp"

def git(*args, data=None):
    return subprocess.check_output(["/usr/bin/git","-C",str(REPO),*args],input=data,env=AUTHOR_ENV)

def replace(text,old,new):
    assert text.count(old)==1,old
    return text.replace(old,new,1)

def load(ref,path):
    return git("show",ref+":"+path).decode()

def commit(parent, name, edits=None, message=None):
    git("read-tree",parent)
    for path,text in dict(edits or {}).items():
        blob=git("hash-object","-w","--stdin",data=text.encode()).decode().strip()
        git("update-index","--add","--cacheinfo","100644,"+blob+","+path)
    new_tree=git("write-tree").decode().strip()
    target=git("commit-tree",new_tree,"-p",parent,data=(message or name+"\n").encode()).decode().strip()
    assert bool(edits)==(new_tree!=git("rev-parse",parent+"^{tree}").decode().strip())
    return target

assert git("rev-parse",PS6+"^").decode().strip()==BASE
old=load(PS6,SPEC)
spec=old
for n in ("llvm-xray","llvm-prof-tools","clang-analyzer"):
    spec=replace(spec,f"Obsoletes: {n} <= %{{version}}-%{{release}}",
                 f"Provides: {n} = %{{version}}-%{{release}}\nObsoletes: {n} < %{{version}}-%{{release}}")
p1=commit(PS6,"packaging: retain versioned analyzer and profiling provides",{SPEC:spec})
comment=replace(spec,
    "# DESTDIR, not a prefix under buildroot: the openmp install script creates its\n"
    "# libgomp/libiomp5 symlinks under $DESTDIR/usr/lib, which is the build\n"
    "# environment's /usr/lib when DESTDIR is unset.",
    "# Use DESTDIR with the normal install prefix: OpenMP creates the\n"
    "# libgomp/libiomp5 symlinks under $DESTDIR plus its configured\n"
    "# library directory (%{_libdir} for this build).")
assert [l for l in spec.splitlines() if not l.startswith("#")]==[l for l in comment.splitlines() if not l.startswith("#")]
p2=commit(p1,"packaging: describe the OpenMP alias install directory",{SPEC:comment})
before=load(PS6,CPP)
cpp=before
macros=[("GET_REGINFO_MC_DESC","X86GenRegisterInfo.inc"),
        ("GET_X86_MNEMONIC_TABLES_CPP","X86GenMnemonicTables.inc"),
        ("ENTRY","MCTargetDesc/X86EncodingOptimizationForImmediate.def")]
for macro,file in macros:
    line=f'#include "{file}"'
    cpp=replace(cpp,line,line+f"\n#undef {macro}")
cpp=replace(cpp,"                              const MCSubtargetInfo &STI) {",
            "                       const MCSubtargetInfo &STI) {")
first=cpp.splitlines()
macro_rows=[]
for macro,file in macros:
    def_line=next(i for i,l in enumerate(first,1) if l.startswith("#define "+macro))
    use_line=next(i for i,l in enumerate(first,1) if l==f'#include "{file}"')
    undef_line=next(i for i,l in enumerate(first,1) if l=="#undef "+macro)
    assert def_line<use_line==undef_line-1
    macro_rows.append(dict(macro=macro,definition=def_line,last_use=use_line,undef=undef_line,include=file))
assert {m.group(1) for m in re.finditer(r"(?m)^#define (\w+)",before)}=={m[0] for m in macros}
p3=commit(p2,"bolt: undefine X86 mirror inclusion macros",{CPP:cpp})
new_body="""Build BOLT from the standalone llvm-tools-subpkgs spec against the
installed LLVM packages on x86_64 and aarch64. That build links
libLLVM.so, while in-tree BOLT keeps linking the LLVM component
libraries; BOLT_LLVM_LINK_MODE selects the mode before its consumers.
The X86 helper mirror is compiled only for the standalone dylib build
and is listed in LLVM_OPTIONAL_SOURCES otherwise, and the inherited
runtime C and C++ flags are cleared only for standalone builds.

The standalone spec pins its LLVM provider build requirements to the
LLVM version and checks that the installed providers share one version
and release, sets BOLT_TARGETS_TO_BUILD per architecture and verifies
target registration, keeps the distribution LDFLAGS, derives
LLVM_LIBDIR_SUFFIX from %{_lib}, and lets CMake install merge-fdata
once. bolt requires libllvm = %{version} at runtime.

clang now ships scan-build, scan-build-py, analyze-build and
intercept-build together with the libexec scripts they run. The
llvm-xray, llvm-prof-tools and clang-analyzer package names are
provided and obsoleted by llvm and clang.

The --build-id=sha1 flag is added to the executable and shared-library
linker flags; module linker flags keep their existing settings."""
original=git("cat-file","commit",PS6).partition(b"\n\n")[2].decode("ascii")
old_header,old_body_and_trailers=original.split("\n\nKeep in-tree BOLT",1)
old_body,trailers=old_body_and_trailers.split("\n\nChange-Id:",1)
assert len(re.findall(r"(?m)^\* [0-9a-f]+ - ",old_header))==9
message=old_header+"\n\n"+new_body+"\n\nChange-Id:"+trailers
assert message.isascii()
forbidden=re.compile(r'github|lhmax|llvm-optimize|sandbox|bolt-v4|codex|claude|openai|\b(?:chatgpt|cline|copilot|ai)\b|\btask[ _-]*\d{1,4}\b|\d{1,4}\s*号|/home/',re.I)
assert max(map(len,new_body.splitlines()))<=72 and not forbidden.search(new_body)
p4=commit(p3,"message only",message=message)
assert git("cat-file","commit",p4).partition(b"\n\n")[2].decode()==message
git("update-ref","refs/heads/ps6-suggestions",p4)
gates={"ascii":message.isascii(),"new_body_max_columns":max(map(len,new_body.splitlines())),
       "body_forbidden_hits":forbidden.findall(new_body),
       "inherited_long_lines":[{"line":i,"columns":len(l),"text":l} for i,l in enumerate(message.splitlines(),1) if len(l)>72],
       "inherited_forbidden_lines":[{"line":i,"text":l} for i,l in enumerate(message.splitlines(),1) if forbidden.search(l)],
       "history_title_and_trailers_preserved":True}
(E/"message-gates.json").write_text(json.dumps(gates,indent=2)+"\n")
(E/"ps6-message-original.txt").write_text(original)
(E/"suggested-commit-message.txt").write_text(message)
(E/"commit-message.diff").write_text("".join(difflib.unified_diff(original.splitlines(True),message.splitlines(True),"PS6", "suggested")))
(E/"macro-lines.json").write_text(json.dumps(macro_rows,indent=2)+"\n")
(E/"llvm.spec").write_text(comment)
(E/"patch1-llvm.spec").write_text(spec)
(E/"base-to-patch3.diff").write_bytes(git("diff","--full-index",BASE+".."+p3))
data=[]
for i,rev in enumerate((p1,p2,p3,p4),1):
    path=E/f"{i:04d}-suggestion-{i}.patch"
    path.write_bytes(git("format-patch","--stdout","--always","--full-index","--no-signature",
                         "--subject-prefix=PATCH", "-1",rev))
    stat=git("diff","--stat",rev+"^",rev).decode()
    tree=git("rev-parse",rev+"^{tree}").decode().strip()
    data.append(dict(number=i,commit=rev,tree=tree,patch=path.name,diffstat=stat))
(E/"patches.json").write_text(json.dumps(data,indent=2)+"\n")
print(json.dumps(data,indent=2))
print(json.dumps(gates,indent=2))
