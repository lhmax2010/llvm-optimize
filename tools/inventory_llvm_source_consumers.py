#!/usr/bin/env python3
"""List direct LLVM development-package requirements in a saved source primary.xml.

Architecture is the metadata's architecture, usually src. This inventory does not
infer which target architectures build a package or which libraries it links.
Use the package spec and actual build logs for those separate questions.
"""
import argparse
import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as ET

NS = {'c': 'http://linux.duke.edu/metadata/common',
      'r': 'http://linux.duke.edu/metadata/rpm'}


def scan(path):
    data = Path(path).read_bytes()
    root = ET.fromstring(data)
    packages = root.findall('c:package', NS)
    rows = []
    for package in packages:
        requirements = [dict(x.attrib) for x in
                        package.findall('c:format/r:requires/r:entry', NS)]
        selected = sorted({x['name'] for x in requirements} &
                          {'llvm-static-devel', 'llvm-devel'})
        if not selected:
            continue
        location = package.find('c:location', NS)
        checksum = package.find('c:checksum', NS)
        version = package.find('c:version', NS)
        rows.append(dict(name=package.findtext('c:name', namespaces=NS),
                         arch=package.findtext('c:arch', namespaces=NS),
                         version=dict(version.attrib),
                         location=location.attrib['href'],
                         checksum_type=checksum.attrib['type'], checksum=checksum.text,
                         matches=selected, requires=requirements))
    return dict(primary=str(Path(path).resolve()),
                primary_sha256=hashlib.sha256(data).hexdigest(),
                total_records=len(packages), consumers=rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('primary', type=Path)
    parser.add_argument('--output', type=Path, help='JSON file; stdout when omitted')
    args = parser.parse_args()
    result = json.dumps(scan(args.primary), indent=2) + '\n'
    if args.output:
        args.output.write_text(result)
    else:
        print(result, end='')


if __name__ == '__main__':
    main()
