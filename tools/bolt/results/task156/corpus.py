from collections import Counter
import json, re, shutil, sys, tarfile
from pathlib import Path

A=Path(__file__).resolve().parent
W=A.parents[1]
B=W.with_name(W.name+"-bolt")
E=A/"evidence"
sys.path.insert(0,str(A/"bench"))
from bench import digest, memory_guard, write_json
QB=B/"tools/bolt/results/perf-c-o2-os-20261025"
TARGET="x86_64-tizen-linux-gnu"
RESTORED=W/"temp/tu-inputs-restored-20261106/tu-inputs.json"
TOOL=(W/"archive/task138-d/resume-config.json")
KIT=W/"archive/server-kit-136/release/skill/references/training-set.json"
VARC=W/"archive/task133-n-20261118/G-config/training.json"
NAME_RE=re.compile(r"(?m)^#\s+1\s+\"([^\"]+\.(?:c|cpp|cc|cxx))\"")

def read(p):
    return json.loads(p.read_text())
def canon_source(path):
    return Path(path).stem.lower()
def parse_source(path):
    with path.open("rb") as f:
        data=f.read(4096).decode(errors="replace")
    found=NAME_RE.search(data)
    if not found:
        raise ValueError(f"cannot identify source TU: {path}")
    return found[1]
def flags(original, input_path):
    # The historical records distinguish source preprocessing and compilation.
    # Embedded line markers and macro expansions already cover includes.
    opt=[]
    i=1
    while i<len(original):
        arg=original[i]
        i+=1
        if arg in ("--library-path","-x","-o","-MF","-MT","-MQ","-I","-isystem"):
            i+=1
        elif (arg in ("-c","-E","-MD","-MMD","-MP","--no-default-config","-fintegrated-cc1") or
              arg.startswith(("--sysroot=","-resource-dir=","-I","-isystem","/")) or
              re.fullmatch(r"-O(?:[0-3sgz]|fast)?",arg)):
            continue
        else:
            opt.append(arg)
    assert "--target="+TARGET in opt,(input_path,opt)
    assert all(not s.startswith(("-fprofile","-fauto-profile","-flto","-MJ","-save-temps","@")) for s in opt)
    return [*opt,"-O2"]

def cutoffs(n):
    if n < 256*1024:
        return "small"
    if n < 8*1024**2:
        return "medium"
    return "large"

def main():
    existing_profile=Path(read(TOOL)["training"])
    files=list(dict.fromkeys((KIT,VARC,existing_profile)))
    training=read(KIT)
    identity={(r["name"],r["target"],r["bytes"],r["sha256"]) for r in training}
    assert len(identity)==23
    for path in files:
        assert {(r["name"],r["target"],r["bytes"],r["sha256"]) for r in read(path)}==identity,path
    exclusion_names=set()
    for r in read(VARC):
        p=Path(r["file"])
        if p.is_file() and p.suffix in (".i",".ii"):
            original=parse_source(p)
        else:
            original=p.name.rsplit("_",1)[-1]
        exclusion_names.add(canon_source(original))
    # Derive the same source identity from the retained earlier target suite,
    # including copies whose digest varies with the preprocessing target.
    restored=read(RESTORED)
    exclude_hashes={r["sha256"] for r in training}
    for r in restored:
        if "-training/" in r["key"]:
            exclude_hashes.add(r["sha256"])
            exclusion_names.add(canon_source(parse_source(Path(r["copy"]))))
    train={"manifests":[str(p) for p in files],"matched_entries":len(identity),
           "target_and_sha":[{"name":n,"target":t,"bytes":s,"sha256":h} for n,t,s,h in sorted(identity)],
           "packages":["llvm for real TUs","synthetic A/B/C"],
           "excluded_hashes":sorted(exclude_hashes),"excluded_source_stems":sorted(exclusion_names)}
    write_json(E/"training-overlap-policy.json",train)

    cdir=A/"corpus"/"zlib"
    cdir.mkdir(parents=True,exist_ok=True)
    carchive=QB/"c-preprocessed-inputs.tar.gz"
    selection=read(QB/"c-source-selection.json")
    candidates=[]
    with tarfile.open(carchive,"r:gz") as tar:
        for index, item in enumerate(selection["sources"]):
            memory_guard()
            src=item["path"]
            stem=Path(src).stem
            key=f"{index:02}-{stem}.i"
            member=tar.getmember(f"{TARGET}/O2/{key}")
            assert member.isfile()
            dst=cdir/key
            with tar.extractfile(member) as inp,dst.open("wb") as out:
                shutil.copyfileobj(inp,out)
            cmd=QB/f"preprocess-{TARGET}-O2-{index}.json"
            original=read(cmd)["argv"]
            assert read(cmd)["rc"]==0 and src in original
            assert Path(parse_source(dst)).name==Path(src).name,(dst,parse_source(dst),src)
            candidates.append(("zlib","c",dst,src,original,str(cmd),None))

    for r in restored:
        if "-holdout/" not in r["key"] or r["target"]!=TARGET:
            continue
        path=Path(r["copy"])
        src=parse_source(path)
        candidates.append(("llvm","c++",path,src,r["original_argv"],f"{RESTORED}#{r['index']}",r["sha256"]))

    admitted=[]
    exclusions=[]
    seen=set()
    paths=set()
    for package,lang,path,src,original,receipt,expected in candidates:
        memory_guard()
        sha=digest(path)
        assert expected is None or expected==sha,path
        identity=canon_source(src)
        paths.add(str(path))
        if sha in exclude_hashes or identity in exclusion_names:
            exclusions.append({"path":str(path),"reason":"training overlap","source":src})
            continue
        assert (package,identity) not in seen,(package,identity)
        seen.add((package,identity))
        size=path.stat().st_size
        admitted.append({"id":package+"-"+Path(src).stem,"package":package,"language":lang,
                         "target":TARGET,"source_tu":src,"path":str(path),"sha256":sha,
                         "bytes":size,"size_band":cutoffs(size),"flags":flags(original,path),
                         "flag_receipt":receipt,"original_flags_argv":original})

    joined=sorted(admitted,key=lambda r:(r["language"],r["bytes"],r["id"]))
    cs=[r for r in joined if r["language"]=="c"]
    cpps=[r for r in joined if r["language"]=="c++"]
    # Pick ten equally spaced quantiles of C size and all ten C++ inputs.
    c_pilot=[cs[round(i*(len(cs)-1)/9)] for i in range(10)]
    pilot=[r for pair in zip(c_pilot,cpps) for r in pair]
    assert len(pilot)==20 and len({r["id"] for r in pilot})==20
    write_json(E/"corpus.json",{"inputs":joined,"target":TARGET})
    write_json(E/"pilot-corpus.json",{"inputs":pilot,"target":TARGET})
    write_json(E/"corpus-summary.json",{"inputs":len(joined),"packages":dict(Counter(r["package"] for r in joined)),
        "languages":dict(Counter(r["language"] for r in joined)),"size_bands":dict(Counter(r["size_band"] for r in joined)),
        "size_min":min(r["bytes"] for r in joined),"size_max":max(r["bytes"] for r in joined),
        "seen_candidate_paths":sorted(paths),"exclusions":exclusions,
        "archive_sha256":digest(carchive),"pilot_size_bands":dict(Counter(r["size_band"] for r in pilot))})
    print("Confirmed corpus",len(joined),"pilot",len(pilot))

if __name__=="__main__":
    main()
