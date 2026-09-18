#!/usr/bin/env python3
"""Audit strip-debug: preserve all allocated sections, non-debug RELA, and symtab.

Read-only ELF64 parser. Relocations targeting removed debug sections may disappear;
the code/data relocations needed by BOLT must remain. No ELF bytes are modified.
"""
import argparse
import hashlib
import json
import mmap
from pathlib import Path
import struct
import subprocess


def sections(path):
    with path.open('rb') as f, mmap.mmap(f.fileno(),0,access=mmap.ACCESS_READ) as data:
        if data[:6]!=b'\x7fELF\x02\x01': raise ValueError('expected little-endian ELF64')
        offset=struct.unpack_from('<Q',data,40)[0]
        stride,count,names_index=struct.unpack_from('<HHH',data,58)
        hs=[struct.unpack_from('<IIQQQQIIQQ',data,offset+i*stride) for i in range(count)]
        n=hs[names_index];names=data[n[4]:n[4]+n[5]]
        getname=lambda h:names[h[0]:].split(b'\0',1)[0].decode()
        rows={}
        for h in hs:
            name=getname(h);payload=b'' if h[1]==8 else data[h[4]:h[4]+h[5]]
            rows[name]=dict(type=h[1],flags=h[2],address=h[3],bytes=h[5],
                           target=getname(hs[h[7]]) if h[1] in (4,9) else None,
                           sha256=hashlib.sha256(payload).hexdigest())
        return dict(bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),sections=rows)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--before',type=Path,required=True);p.add_argument('--after',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    if a.output.exists():p.error('new output directory required')
    a.output.mkdir(parents=True)
    old,new=sections(a.before),sections(a.after);errors=[]
    for label,path in [('before',a.before),('after',a.after)]:
        with (a.output/(label+'-sections.txt')).open('w') as out:
            subprocess.run(['readelf','-SW',str(path)],stdout=out,stderr=subprocess.STDOUT,check=True)
    for name,section in old['sections'].items():
        other=new['sections'].get(name)
        if section['flags']&2 and other!=section:errors.append('allocated section changed: '+name)
        if section['type'] in (4,9) and not section['target'].startswith(('.debug','.zdebug')):
            if other is None or other['bytes']!=section['bytes'] or other['target']!=section['target']:
                errors.append('code/data relocations missing/changed size: '+name)
    for name in ['.symtab','.rela.text']:
        if not new['sections'].get(name,{}).get('bytes'):errors.append('missing/empty '+name)
    if any(n.startswith(('.debug','.zdebug')) for n in new['sections']):errors.append('debug sections remain')
    result=dict(status='PASS' if not errors else 'BLOCKER',before=old,after=new,
                removed_sections=sorted(set(old['sections'])-set(new['sections'])),errors=errors)
    (a.output/'result.json').write_text(json.dumps(result,indent=2)+'\n')
    print(result['status'],old['bytes'],'->',new['bytes'],errors)
    return 0 if not errors else 2


if __name__=='__main__':raise SystemExit(main())
