"""Read the four build overviews through the previously authenticated browser."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
import re
import subprocess

from audit import W, E, read, save

IDS = ("1241534","1241535","1241584","1241585")
NODE = "/home/linhao/.local/bin/node"
CLIENT = W/"archive/task164/qb-read.mjs"


def overview(build):
    dest = E/build/"qb-overview.json"
    kwargs = {"text":True,"capture_output":True,"check":True,"timeout":200}
    subprocess.run([NODE,str(CLIENT),"view",f"/build/{build}",str(dest)],**kwargs)
    d = read(dest)
    row = next(r for r in d["tables"] if len(r)>=4 and r[0]==build)
    if not row[2]:
        raise ValueError(f"QB begin time not found for {build}")
    started = datetime.fromisoformat(row[2])
    units = {"day":86400,"hour":3600,"minute":60,"second":1}
    parts = re.findall(r"(\d+)\s+(days?|hours?|minutes?|seconds?)",row[3])
    ended = started + timedelta(seconds=sum(int(n)*units[k.rstrip("s")] for n,k in parts))
    fields = {r[0].strip():r[1].strip() for r in d["tables"] if len(r)==2}
    observed = {"id":build,"status":row[1],"start_qb_clock":started.isoformat(sep=" "),
            "end_qb_clock":ended.isoformat(sep=" ") if parts else None,"duration":row[3].strip(),
            "build_package_list":fields.get("Build Package List"),"download":fields.get("Download_URL"),
            "manifest":fields.get("Manifest_URL"),"title":d["title"]}
    children=[]
    for r in d["tables"]:
        if len(r)>=3 and re.fullmatch(r"https://quickbuild\.tizen\.org/build/\d+",r[1]):
            children.append({"repository_arches":r[0],"url":r[1],"status":r[2]})
    observed["children"]=children
    save(E/build/"qb-identity.json",observed)
    return observed


if __name__=="__main__":
    status=subprocess.check_output([NODE,str(CLIENT),"status"],text=True,timeout=15).strip()
    if status!="SESSION_OPEN":
        raise SystemExit("AUTH_REQUIRED")
    with ThreadPoolExecutor(max_workers=4) as workers:
        result=list(workers.map(overview,IDS))
    for row in result:
        print(row)
