#!/usr/bin/env python3
"""Read GNU/BSD ar metadata without executing members; retain duplicate identities.

GNU 32/64-bit symbol tables are decoded by member header offset, then normalized
into (symbol, ordinal, name, occurrence). No ranlib repairs are performed.
Thin members are never followed. Unsupported index layouts fail explicitly.
"""
import argparse
from collections import Counter
import hashlib
import json
import mmap
from pathlib import Path
import struct


def cstring(data, offset):
    if not 0 <= offset < len(data):
        raise ValueError('string offset outside table')
    end = data.find(b'\0', offset)
    if end < 0:
        raise ValueError('unterminated string')
    return data[offset:end].decode('utf-8', 'surrogateescape')


def member_kind(data):
    if data[:4] in (b'BC\xc0\xde', b'\xde\xc0\x17\x0b'):
        return 'bitcode'
    if (len(data) >= 20 and data[:4] == b'\x7fELF' and
            data[4] in (1, 2) and data[5] in (1, 2) and
            int.from_bytes(data[16:18], 'little' if data[5] == 1 else 'big') == 1):
        return 'machine'
    return 'other'


def elf_details(data):
    """Defined external symbols and debug sections in an ELF relocatable member."""
    if member_kind(data) != 'machine':
        raise ValueError('not a native ELF relocatable')
    bits, endian = data[4], '<' if data[5] == 1 else '>'
    if bits == 2:
        shoff = struct.unpack_from(endian+'Q', data, 40)[0]
        entsize, count, names_idx = struct.unpack_from(endian+'HHH', data, 58)
        fmt = endian+'IIQQQQIIQQ'; symfmt = endian+'IBBHQQ'
    else:
        shoff = struct.unpack_from(endian+'I', data, 32)[0]
        entsize, count, names_idx = struct.unpack_from(endian+'HHH', data, 46)
        fmt = endian+'IIIIIIIIII'; symfmt = endian+'IIIBBH'
    if not shoff:
        return [], []
    if entsize < struct.calcsize(fmt):
        raise ValueError('short ELF section header')
    zero = struct.unpack_from(fmt, data, shoff)
    if count == 0:
        count = zero[5]
    if names_idx == 0xffff:
        names_idx = zero[6]
    sections = [struct.unpack_from(fmt, data, shoff+i*entsize) for i in range(count)]
    def contents(section):
        start, size = section[4:6]
        if start+size > len(data):
            raise ValueError('ELF section outside member')
        return data[start:start+size]
    names = contents(sections[names_idx]) if names_idx else b'\0'
    debug = [cstring(names, s[0]) for s in sections
             if cstring(names, s[0]).startswith(('.debug', '.zdebug', '.rel.debug', '.rela.debug'))]
    symbols = []
    for s in sections:
        if s[1] != 2:  # SHT_SYMTAB, not dynamic symbols
            continue
        strings = contents(sections[s[6]])
        table = contents(s); stride = s[9]
        if stride < struct.calcsize(symfmt) or len(table) % stride:
            raise ValueError('invalid ELF symbol table')
        for pos in range(0, len(table), stride):
            fields = struct.unpack_from(symfmt, table, pos)
            name, info, ndx = (fields[0], fields[1], fields[3]) if bits == 2 else (fields[0], fields[3], fields[5])
            if info >> 4 in (1, 2, 10) and ndx != 0 and name:
                symbols.append(cstring(strings, name))
    return symbols, debug


def inspect(path):
    path = Path(path)
    with path.open('rb') as f, mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as data:
        magic = data[:8]
        if magic not in (b'!<arch>\n', b'!<thin>\n'):
            raise ValueError(f'not an archive: {path}')
        thin = magic == b'!<thin>\n'
        pos, longnames, raw_members, tables = 8, b'', [], []
        while pos < len(data):
            start = pos; header = data[pos:pos+60]
            if len(header) != 60 or header[58:60] != b'`\n':
                raise ValueError(f'invalid ar header at {pos}')
            name = header[:16].decode('ascii').rstrip(); size = int(header[48:58]); pos += 60
            special = name in ('/', '//', '/SYM64/')
            stored_size = size if not thin or special else (int(name[3:]) if name.startswith('#1/') else 0)
            if pos+stored_size > len(data):
                raise ValueError('ar member outside file')
            if name == '//':
                longnames = data[pos:pos+size]
            elif name in ('/', '/SYM64/'):
                tables.append((name, data[pos:pos+size]))
            else:
                raw_members.append(dict(header_offset=start, raw_name=name, offset=pos,
                                        size=size, mtime=header[16:28].decode().strip()))
            pos += stored_size + stored_size % 2
        members, offsets, native_map, occurrences = [], {}, [], Counter()
        for m in raw_members:
            name, off, size = m.pop('raw_name'), m['offset'], m['size']
            if name.startswith('#1/'):
                n = int(name[3:]); name = data[off:off+n].rstrip(b'\0').decode('utf-8', 'surrogateescape'); off += n; size -= n
            elif name.startswith('/'):
                n = int(name[1:]); end = longnames.find(b'/\n', n)
                if end < 0:
                    raise ValueError('invalid GNU long name')
                name = longnames[n:end].decode('utf-8', 'surrogateescape')
            else:
                name = name.removesuffix('/')
            if name.startswith('__.SYMDEF'):
                raise ValueError('BSD ar symbol table unsupported; refuse silent index loss')
            ordinal = len(members); occurrences[name] += 1
            m.update(name=name, ordinal=ordinal, occurrence=occurrences[name], offset=off, size=size)
            payload = data[off:off+size] if not thin else b''
            m['magic_hex'] = payload[:4].hex() if not thin else None
            m['kind'] = member_kind(payload) if not thin else 'other'
            m['sha256'] = hashlib.sha256(payload).hexdigest() if not thin else None
            m['debug_sections'] = []
            if m['kind'] == 'machine':
                symbols, m['debug_sections'] = elf_details(payload)
                native_map += [[s, ordinal, name, occurrences[name]] for s in symbols]
            offsets[m['header_offset']] = m; members.append(m)
        index = []
        if len(tables) > 1:
            raise ValueError('multiple ar indexes not supported')
        for name, table in tables:
            width = 8 if name == '/SYM64/' else 4
            if len(table) < width:
                raise ValueError('short ar index')
            count = int.from_bytes(table[:width], 'big'); names_start = width*(1+count)
            if names_start > len(table):
                raise ValueError('ar index offset array truncated')
            string_pos = names_start
            for n in range(count):
                offset = int.from_bytes(table[width*(n+1):width*(n+2)], 'big')
                if offset not in offsets:
                    raise ValueError('ar index references a non-member header')
                symbol = cstring(table, string_pos); string_pos = table.index(b'\0', string_pos)+1
                m = offsets[offset]; index.append([symbol, m['ordinal'], m['name'], m['occurrence']])
        counts = Counter(m['kind'] for m in members)
        return dict(path=str(path), bytes=len(data), sha256=hashlib.sha256(data).hexdigest(), thin=thin,
                    members=members, member_count=len(members), bitcode=counts['bitcode'],
                    machine=counts['machine'], other=counts['other'], index=index, index_entries=len(index),
                    index_equals_machine_symbols=Counter(map(tuple,index))==Counter(map(tuple,native_map)),
                    machine_symbol_entries=len(native_map))


def mapping_equal(left, right):
    """Offsets/mtime may change; ordered identities and every index pair may not."""
    identities = lambda x: [(m['name'],m['occurrence']) for m in x['members']]
    return identities(left)==identities(right) and left['index']==right['index']


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('archive', type=Path); p.add_argument('--compare', type=Path)
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args(); result=inspect(args.archive)
    if args.compare:
        other=inspect(args.compare); result={'left':result,'right':other,'mapping_equal':mapping_equal(result,other)}
    args.output.write_text(json.dumps(result,indent=2,ensure_ascii=True)+'\n')
    return 0 if not args.compare or result['mapping_equal'] else 2

if __name__ == '__main__':
    raise SystemExit(main())
