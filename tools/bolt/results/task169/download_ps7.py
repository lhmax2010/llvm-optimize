from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import urljoin
from urllib.request import urlopen

A = Path(__file__).resolve().parent
ARCH = ("x86_64","aarch64","armv7l")
BUILDS = ("1241534","1241535")
PACKAGES = ("clang","llvm","llvm-devel")

class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
    def handle_starttag(self, tag, attrs):
        if tag == "a" and (href := dict(attrs).get("href")):
            self.links.append(href)


def requests():
    for build in BUILDS:
        root = A/build
        state = json.loads((root/"public-log-locations.json").read_text())
        for machine in ARCH:
            assert state[machine]["result"]["status"] == "succeeded"
            index = state[machine]["rpm_index"]
            parser = Links()
            parser.feed((root/(machine+"-rpm-index.html")).read_text())
            for package in PACKAGES:
                pattern = rf"{re.escape(package)}-22\.1\.8-[0-9]+(?:\.[0-9]+)*\.{machine}\.rpm"
                urls = [urljoin(index,u) for u in parser.links if re.fullmatch(pattern,u)]
                if len(urls) != 1:
                    raise RuntimeError(f"expected one release for {build} {machine} {package}: {urls}")
                yield build, machine, package, urls[0]


def fetch(req):
    build, machine, package, url = req
    folder = A/build/"rpms"/machine
    folder.mkdir(parents=True,exist_ok=True)
    target = folder/url.rsplit("/",1)[-1]
    blob = target.with_suffix(".part")
    if not target.is_file():
        with urlopen(url,timeout=180) as r, blob.open("wb") as f:
            if not r.geturl().startswith("https://download.tizen.org/"):
                raise RuntimeError(f"unexpected download origin: {r.geturl()}")
            while data := r.read(1024*1024):
                f.write(data)
        blob.replace(target)
    with target.open("rb") as f:
        if f.read(4) != b"\xed\xab\xee\xdb":
            raise RuntimeError(f"not an RPM: {target}")
        f.seek(0)
        sha = hashlib.file_digest(f,"sha256").hexdigest()
    result = {"build":build,"arch":machine,"package":package,"url":url,"path":str(target),
              "bytes":target.stat().st_size,"sha256":sha}
    print(f"{build} {machine} {package} {result['bytes']} {sha}",flush=True)
    return result


if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=4) as workers:
        rows = list(workers.map(fetch,requests()))
    assert len(rows) == 18
    (A/"ps7-downloads.json").write_text(json.dumps(rows,indent=2)+"\n")
