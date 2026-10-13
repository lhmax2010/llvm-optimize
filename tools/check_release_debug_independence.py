#!/usr/bin/env python3
"""Compare debug/release IR conversion products under the docs/49 contract.

Read-only ELF ET_REL inspection, no compiler/Source invocation. REL has an
implicit addend: exact equality of the entire target-section payload covers
its encoded addend; RELA addends are compared explicitly. Section numbers and
string-table offsets are not semantic identities. Repeated section names are
disambiguated by occurrence. Retained symbol and relocation order is checked.
"""
import argparse
import collections
import difflib
import hashlib
import json
from pathlib import Path
import struct


def parse(data):
    if len(data) < 52 or data[:4] != b'\x7fELF' or data[4] not in (1, 2) or data[5] != 1:
        raise ValueError('expected little-endian ELF32/ELF64')
    bits = data[4]
    if struct.unpack_from('<H', data, 16)[0] != 1:
        raise ValueError('expected ET_REL')
    shoff = struct.unpack_from('<I' if bits == 1 else '<Q', data, 32 if bits == 1 else 40)[0]
    stride, count, names = struct.unpack_from('<HHH', data, 46 if bits == 1 else 58)
    fmt = '<IIIIIIIIII' if bits == 1 else '<IIQQQQIIQQ'
    def take(start, size):
        if start < 0 or size < 0 or start > len(data) or size > len(data)-start:
            raise ValueError('ELF data outside file')
        return data[start:start+size]
    if stride < struct.calcsize(fmt):
        raise ValueError('invalid section header stride')
    zero = struct.unpack(fmt, take(shoff, struct.calcsize(fmt)))
    count = count or zero[5]
    names = zero[6] if names == 0xffff else names
    take(shoff, count*stride)
    sections = [struct.unpack_from(fmt, data, shoff+i*stride) for i in range(count)]
    def payload(i):
        s = sections[i]
        return b'' if s[1] == 8 else take(s[4], s[5])
    def string(blob, offset):
        if offset >= len(blob):
            raise ValueError('string offset outside table')
        return blob[offset:blob.index(b'\0', offset)].decode('utf-8')
    if not 0 < names < count or sections[names][1] != 3:
        raise ValueError('invalid section name table')
    strings = payload(names)
    section_names = [string(strings, s[0]) for s in sections]
    occurrences = collections.Counter(); identities = []
    for name in section_names:
        identities.append([name, occurrences[name]]); occurrences[name] += 1
    symbols = {}; extensions = {}
    for i, s in enumerate(sections):
        if s[1] == 18:
            if s[6] in extensions or s[9] != 4 or s[5] % 4:
                raise ValueError('invalid extended symbol index table')
            extensions[s[6]] = struct.unpack('<'+'I'*(s[5]//4), payload(i))
    for i, s in enumerate(sections):
        if s[1] != 2:
            continue
        symfmt = '<IIIBBH' if bits == 1 else '<IBBHQQ'
        if s[9] < struct.calcsize(symfmt) or s[5] % s[9] or sections[s[6]][1] != 3:
            raise ValueError('invalid symbol table')
        table, strings = payload(i), payload(s[6]); rows = []
        for n, pos in enumerate(range(0, len(table), s[9])):
            f = struct.unpack_from(symfmt, table, pos)
            name, value, size, info, other, idx = f if bits == 1 else (f[0], f[4], f[5], f[1], f[2], f[3])
            if idx == 0xffff:
                idx = extensions[i][n]
                if not 0 < idx < count:
                    raise ValueError('invalid extended symbol section')
                section = identities[idx]
            elif idx in (0, 0xfff1, 0xfff2):
                section = {0: ['UND', 0], 0xfff1: ['ABS', 0], 0xfff2: ['COMMON', 0]}[idx]
            elif idx >= 0xff00 or idx >= count:
                raise ValueError('uncertified symbol section index')
            else:
                section = identities[idx]
            rows.append(dict(name=string(strings, name), type=info & 15, binding=info >> 4,
                             visibility=other & 3, section=section, value=value, size=size))
        symbols[i] = rows
    alloc = []
    for i, s in enumerate(sections):
        if s[2] & 2:
            alloc.append(dict(section=identities[i], flags=s[2], size=s[5],
                              nobits=s[1] == 8, content=payload(i)))
    relocs = []
    for i, s in enumerate(sections):
        if s[1] not in (4, 9):
            continue
        if s[7] >= count or s[6] not in symbols:
            raise ValueError('invalid relocation target/symbol table')
        if not sections[s[7]][2] & 2:
            continue
        fmt = ('<IIi' if s[1] == 4 else '<II') if bits == 1 else ('<QQq' if s[1] == 4 else '<QQ')
        if s[9] < struct.calcsize(fmt) or s[5] % s[9]:
            raise ValueError('invalid relocation stride')
        table = payload(i)
        for pos in range(0, len(table), s[9]):
            f = struct.unpack_from(fmt, table, pos)
            kind, si = (f[1] & 255, f[1] >> 8) if bits == 1 else (f[1] & 0xffffffff, f[1] >> 32)
            symbol = symbols[s[6]][si]
            relocs.append(dict(target=identities[s[7]], offset=f[0], type=kind,
                               symbol=symbol['name'],
                               section_symbol=symbol['section'] if symbol['type'] == 3 else None,
                               addend=f[2] if s[1] == 4 else 'implicit: target bytes checked',
                               format='RELA' if s[1] == 4 else 'REL'))
    def is_debug(name):
        return name.startswith(('.debug', '.zdebug', '.rel.debug', '.rela.debug'))
    kept = []; excluded = []
    for i, rows in symbols.items():
        for row in rows:
            if row['type'] == 4 or (row['type'] == 3 and is_debug(row['section'][0])):
                excluded.append(row)
            else:
                kept.append(row)
    return dict(alloc=alloc, relocations=relocs, symbols=kept, excluded_symbols=excluded,
                debug_sections=[n for n in section_names if is_debug(n)])


def serializable(obj):
    return {**obj, 'alloc': [{**s, 'content': dict(bytes=len(s['content']),
                    sha256=hashlib.sha256(s['content']).hexdigest())} for s in obj['alloc']]}


def compare(debug, release):
    # Equality uses actual bytes, not their serialized digests.
    result = {k: debug[k] == release[k] for k in ('alloc', 'relocations', 'symbols')}
    result['release_no_debug'] = not release['debug_sections']
    delta = {}
    left, right = serializable(debug), serializable(release)
    for k, equal in result.items():
        if not equal and k != 'release_no_debug':
            delta[k] = ''.join(difflib.unified_diff(
                json.dumps(left[k], indent=2).splitlines(True),
                json.dumps(right[k], indent=2).splitlines(True),
                fromfile='debug/'+k, tofile='release/'+k))
    if not result['release_no_debug']:
        delta['release_no_debug'] = json.dumps(release['debug_sections'])
    return dict(status='PASS' if all(result.values()) else 'FAIL', checks=result, differences=delta)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('debug', type=Path); p.add_argument('release', type=Path)
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args(); d, r = parse(a.debug.read_bytes()), parse(a.release.read_bytes())
    result = compare(d, r); result.update(debug=serializable(d), release=serializable(r))
    a.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('debug','release')}, indent=2))
    return 0 if result['status'] == 'PASS' else 1


if __name__ == '__main__':
    raise SystemExit(main())
