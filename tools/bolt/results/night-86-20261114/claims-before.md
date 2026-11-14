# 0003 v2：重定位描述与代码对应

只核对记录，不修改LLVM源码或提交说明。基准提交：fea0fe464d56e17f2c7588c557bfffd9f6ac352b；文件：packaging/llvm-static-archives-native.py；SHA256：c56a126b51128106ca351e8820f4c6d9ee73d46dd72b65a267ebae890e70027b。

结论：重定位相关5个完整句子均有代码对应，0句标为“与代码不符”。拆开覆盖7项要求：动态专用类型、表外拒绝、CREL拒绝、8/16位PIC、既有32/64位PIC、字段越界、压缩目标声明大小。条件范围和NONE例外在下面明列。此为静态逐句核对，不是新增运行测试，也不证明全归档或全包等价。

[完整代码只读快照](../resume3-20261112/fea0fe46-converter.txt)、[同提交x86_64.def](../resume3-20261112/fea0fe46-x86_64.def.txt)、[表枚举及既有条件核对](../resume3-20261112/relocation-table-code-check.json)。

## 句1：对应

> Harden archive and relocation parsing against malformed sizes, size fields, long-name numbers and offsets, section tables, section payloads and indexes.

ar成员大小/长名称数字和偏移/索引，以及ELF节表、载荷和重定位表索引均有显式验证。此描述表示这些检查存在，不声称覆盖所有可能的畸形输入。

fea0fe46，llvm-static-archives-native.py，第107–110行原文：

~~~python
def ar_decimal(value):
    if re.fullmatch(r'[0-9]+', value) is None:
        raise ValueError('invalid ar long-name number: '+value)
    return int(value)
~~~

fea0fe46，llvm-static-archives-native.py，第121–141行原文：

~~~python
        while pos < len(data):
            start = pos; header = data[pos:pos+60]
            if len(header) != 60 or header[58:60] != b'`\n':
                raise ValueError(f'invalid ar header at {pos}')
            if not re.fullmatch(rb'[0-9]+ *', header[48:58]):
                raise ValueError('invalid ar member size field')
            name = header[:16].decode('ascii').rstrip(); size = int(header[48:58]); pos += 60
            special = name in ('/', '//', '/SYM64/')
            stored_size = size if not thin or special else (ar_decimal(name[3:]) if name.startswith('#1/') else 0)
            if stored_size < 0 or stored_size > len(data)-pos:
                raise ValueError('ar member outside file')
            if name == '//':
                longnames = data[pos:pos+size]
            elif name in ('/', '/SYM64/'):
                tables.append((name, data[pos:pos+size]))
            else:
                raw_members.append(dict(header_offset=start, raw_name=name, offset=pos,
                                        size=size, mtime=header[16:28].decode().strip()))
            pos += stored_size + stored_size % 2
            if pos > len(data):
                raise ValueError('missing ar member alignment byte')
~~~

fea0fe46，llvm-static-archives-native.py，第145–158行原文：

~~~python
            if name.startswith('#1/'):
                n = ar_decimal(name[3:])
                if not 0 <= n <= size:
                    raise ValueError('invalid BSD long name length')
                name = data[off:off+n].rstrip(b'\0').decode('utf-8', 'surrogateescape'); off += n; size -= n
            elif name.startswith('/'):
                n = ar_decimal(name[1:])
                if not 0 <= n < len(longnames):
                    raise ValueError('GNU long name offset outside table')
                if n and longnames[n-1:n] != b'\n':
                    raise ValueError('GNU long name offset inside entry')
                end = longnames.find(b'/\n', n)
                if end < 0:
                    raise ValueError('invalid GNU long name')
~~~

fea0fe46，llvm-static-archives-native.py，第175–190行原文：

~~~python
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
~~~

fea0fe46，llvm-static-archives-native.py，第481–517行原文：

~~~python
    if (len(data) < 64 or member_kind(data) != 'machine' or
            data[4:6] != b'\x02\x01' or struct.unpack_from('<H', data, 18)[0] != 62):
        raise ValueError('not x86_64 ELF64 little-endian ET_REL')
    off = struct.unpack_from('<Q', data, 40)[0]
    stride, count = struct.unpack_from('<HH', data, 58)
    if not off or stride != 64 or off + 64 > len(data):
        raise ValueError('invalid ELF section table')
    if not count:
        count = struct.unpack_from('<IIQQQQIIQQ', data, off)[5]
    if not count or count > (len(data)-off) // stride:
        raise ValueError('ELF section table outside member')
    sections = [struct.unpack_from('<IIQQQQIIQQ', data, off+i*stride) for i in range(count)]
    checked, forbidden = 0, []
    for section in sections:
        if section[1] == 0x40000014:
            raise ValueError('unsupported CREL relocation section')
        if section[1] not in (0, 8) and section[4] + section[5] > len(data):
            raise ValueError('ELF section outside member')
    for section in sections:
        if section[1] not in (4, 9):
            continue
        if section[6] >= count or section[7] >= count:
            raise ValueError('relocation link/info outside section table')
        target = sections[section[7]]
        limit = target[5]
        if target[2] & 0x800:  # SHF_COMPRESSED: offsets use uncompressed size.
            if target[5] < 24 or target[4] + 24 > len(data):
                raise ValueError('short compressed ELF section header')
            limit = struct.unpack_from('<IIQQ', data, target[4])[2]
        symbols = sections[section[6]]
        if (symbols[1] != 2 or symbols[9] != 24 or symbols[5] % 24 or
                symbols[4] + symbols[5] > len(data)):
            raise ValueError('invalid relocation symbol table')
        relocation_stride = 24 if section[1] == 4 else 16
        if (section[9] != relocation_stride or section[5] % relocation_stride or
                section[4] + section[5] > len(data)):
            raise ValueError('invalid relocation table')
~~~

fea0fe46，llvm-static-archives-native.py，第526–528行原文：

~~~python
            if symbol_index >= symbol_count:
                raise ValueError('relocation symbol index outside table')
            symbol = struct.unpack_from('<IBBHQQ', data, symbols[4]+symbol_index*symbols[9])
~~~

## 句2：对应

> Check each relocation against an explicit x86_64 field width table taken from LLVM 22.1.8, excluding seven dynamic-linking-only types: COPY, GLOB_DAT, JUMP_SLOT, RELATIVE, DTPMOD64, TLSDESC and IRELATIVE.

宽度表37种，源码x86_64.def共44种；恰好排除COPY(5)、GLOB_DAT(6)、JUMP_SLOT(7)、RELATIVE(8)、DTPMOD64(16)、TLSDESC(36)、IRELATIVE(37)。类型名/数值另与同提交x86_64.def核对；本次未联网重新审查ABI规范。

fea0fe46，llvm-static-archives-native.py，第382–394行原文：

~~~python
# LLVM 22.1.8 ELFRelocs/x86_64.def numbers; x86-64 psABI section 4.4,
# Relocation Types and Large Model Relocation Types (LP64 field bytes).
# Dynamic-loader-only relocations are deliberately absent from the accepted
# table. COPY has no fixed-size field; TLSDESC_CALL is a zero-width marker.
# 0 R_X86_64_NONE: 0 bytes; psABI Relocation Types: none (linker marker); accept.
# 1 R_X86_64_64: 8 bytes; psABI Relocation Types: word64; accept.
# 2 R_X86_64_PC32: 4 bytes; psABI Relocation Types: word32; accept.
# 3 R_X86_64_GOT32: 4 bytes; psABI Relocation Types: word32; accept.
# 4 R_X86_64_PLT32: 4 bytes; psABI Relocation Types: word32; accept.
# 5 R_X86_64_COPY: 0 bytes; psABI Relocation Types: none (COPY has no fixed field); reject dynamic-only.
# 6 R_X86_64_GLOB_DAT: 8 bytes; psABI Relocation Types: word64; reject dynamic-only.
# 7 R_X86_64_JUMP_SLOT: 8 bytes; psABI Relocation Types: word64; reject dynamic-only.
# 8 R_X86_64_RELATIVE: 8 bytes; psABI Relocation Types: word64; reject dynamic-only.
~~~

fea0fe46，llvm-static-archives-native.py，第402–402行原文：

~~~python
# 16 R_X86_64_DTPMOD64: 8 bytes; psABI Relocation Types: word64; reject dynamic-only.
~~~

fea0fe46，llvm-static-archives-native.py，第422–468行原文：

~~~python
# 36 R_X86_64_TLSDESC: 16 bytes; psABI Relocation Types: word64 x 2; reject dynamic-only.
# 37 R_X86_64_IRELATIVE: 8 bytes; psABI Relocation Types: word64; reject dynamic-only.
# 41 R_X86_64_GOTPCRELX: 4 bytes; psABI Relocation Types: word32; accept.
# 42 R_X86_64_REX_GOTPCRELX: 4 bytes; psABI Relocation Types: word32; accept.
# 43 R_X86_64_CODE_4_GOTPCRELX: 4 bytes; psABI Relocation Types: word32; accept.
# 44 R_X86_64_CODE_4_GOTTPOFF: 4 bytes; psABI Relocation Types: word32; accept.
# 45 R_X86_64_CODE_4_GOTPC32_TLSDESC: 4 bytes; psABI Relocation Types: word32; accept.
# 50 R_X86_64_CODE_6_GOTTPOFF: 4 bytes; psABI Relocation Types: word32; accept.
X86_64_RELOCATION_WIDTHS = {
    0: 0,  # R_X86_64_NONE
    1: 8,  # R_X86_64_64
    2: 4,  # R_X86_64_PC32
    3: 4,  # R_X86_64_GOT32
    4: 4,  # R_X86_64_PLT32
    9: 4,  # R_X86_64_GOTPCREL
    10: 4,  # R_X86_64_32
    11: 4,  # R_X86_64_32S
    12: 2,  # R_X86_64_16
    13: 2,  # R_X86_64_PC16
    14: 1,  # R_X86_64_8
    15: 1,  # R_X86_64_PC8
    17: 8,  # R_X86_64_DTPOFF64
    18: 8,  # R_X86_64_TPOFF64
    19: 4,  # R_X86_64_TLSGD
    20: 4,  # R_X86_64_TLSLD
    21: 4,  # R_X86_64_DTPOFF32
    22: 4,  # R_X86_64_GOTTPOFF
    23: 4,  # R_X86_64_TPOFF32
    24: 8,  # R_X86_64_PC64
    25: 8,  # R_X86_64_GOTOFF64
    26: 4,  # R_X86_64_GOTPC32
    27: 8,  # R_X86_64_GOT64
    28: 8,  # R_X86_64_GOTPCREL64
    29: 8,  # R_X86_64_GOTPC64
    30: 8,  # R_X86_64_GOTPLT64
    31: 8,  # R_X86_64_PLTOFF64
    32: 4,  # R_X86_64_SIZE32
    33: 8,  # R_X86_64_SIZE64
    34: 4,  # R_X86_64_GOTPC32_TLSDESC
    35: 0,  # R_X86_64_TLSDESC_CALL
    41: 4,  # R_X86_64_GOTPCRELX
    42: 4,  # R_X86_64_REX_GOTPCRELX
    43: 4,  # R_X86_64_CODE_4_GOTPCRELX
    44: 4,  # R_X86_64_CODE_4_GOTTPOFF
    45: 4,  # R_X86_64_CODE_4_GOTPC32_TLSDESC
    50: 4,  # R_X86_64_CODE_6_GOTTPOFF
}
~~~

fea0fe46，llvm-static-archives-native.py，第520–525行原文：

~~~python
            r_offset, info = struct.unpack_from('<QQ', data, pos)
            kind, symbol_index = info & 0xffffffff, info >> 32
            if kind not in X86_64_RELOCATION_WIDTHS:
                raise ValueError('uncertified x86_64 relocation type: '+str(kind))
            if kind != 0 and r_offset + X86_64_RELOCATION_WIDTHS[kind] > limit:
                raise ValueError('relocation offset outside target section')
~~~

## 句3：对应

> Reject types outside the table and CREL sections.

CREL节类型0x40000014直接抛ValueError；所有REL/RELA条目的类型均须在宽度表内，包括非ALLOC调试节的条目。

fea0fe46，llvm-static-archives-native.py，第494–498行原文：

~~~python
    for section in sections:
        if section[1] == 0x40000014:
            raise ValueError('unsupported CREL relocation section')
        if section[1] not in (0, 8) and section[4] + section[5] > len(data):
            raise ValueError('ELF section outside member')
~~~

fea0fe46，llvm-static-archives-native.py，第520–525行原文：

~~~python
            r_offset, info = struct.unpack_from('<QQ', data, pos)
            kind, symbol_index = info & 0xffffffff, info >> 32
            if kind not in X86_64_RELOCATION_WIDTHS:
                raise ValueError('uncertified x86_64 relocation type: '+str(kind))
            if kind != 0 and r_offset + X86_64_RELOCATION_WIDTHS[kind] > limit:
                raise ValueError('relocation offset outside target section')
~~~

## 句4：对应

> For PIC, reject 8- and 16-bit absolute relocations in allocated sections when they reference non-absolute symbols; retain the existing 32- and 64-bit PIC checks.

只有目标节SHF_ALLOC且符号非SHN_ABS时，8/16/32/32S绝对重定位进入forbidden；64位绝对重定位还要求目标不是SHF_WRITE。转换成员settings.pic_level非零时据forbidden报错。原生成员仅记录禁止项，不因forbidden列表非空报错。32/64位条件与60fabc72逐字相同。

fea0fe46，llvm-static-archives-native.py，第474–479行原文：

~~~python
    Absolute 8-, 16- and 32-bit relocations against non-absolute symbols
    are forbidden in both writable and read-only ALLOC sections; 64-bit
    absolute relocations are forbidden in read-only ALLOC sections.
    SHN_ABS references remain allowed. Debug sections are excluded from
    the PIC policy, but all relocation indexes and target byte ranges are
    validated. PC-relative relocations may be legitimate (e.g. .eh_frame).
~~~

fea0fe46，llvm-static-archives-native.py，第529–535行原文：

~~~python
            if not target[2] & 2:
                continue
            checked += 1
            # SHN_ABS references do not need runtime relocation.
            if symbol[3] != 0xfff1 and (kind in (10, 11, 12, 14) or (kind == 1 and not target[2] & 1)):
                forbidden.append(dict(type=kind, target_section=section[7], symbol_index=symbol_index))
    return dict(checked=checked, forbidden=forbidden)
~~~

fea0fe46，llvm-static-archives-native.py，第850–871行原文：

~~~python
                if member['kind'] == 'machine':
                    if sha(target) != member['sha256']:
                        raise ValueError('native member changed')
                    relocs = pic_relocations(target.read_bytes())
                    atomic_json(source.parent/'relocations.json', relocs)
                    return dict(ordinal=member['ordinal'], name=member['name'], preserved=True,
                                relocation_check=relocs)
                text_ir = source.with_suffix('.ll')
                with text_ir.open('wb') as out:
                    command.run([disassembler, str(source), '-o', '-'], source.parent/'disassemble', stdout=out)
                with text_ir.open() as lines:
                    settings = ir_settings(lines, arch=arch, debug_info=debug_info)
                atomic_json(source.parent/'ir-settings.json', settings)
                text_ir.unlink()
                record = command.run([compiler, *settings['flags'], str(source), '-o', str(target)], source.parent/'convert')
                data = target.read_bytes()
                if settings['policy']['dwarf'] is None and elf_details(data)[1]:
                    raise ValueError('release conversion unexpectedly emitted debug sections')
                relocs = pic_relocations(data)
                atomic_json(source.parent/'relocations.json', relocs)
                if settings['pic_level'] and relocs['forbidden']:
                    raise ValueError('non-PIC relocation in '+str(target))
~~~

## 句5：对应

> Validate relocation field bounds against the target section; for compressed targets, use the declared uncompressed size as the bound.

非NONE类型检查r_offset+字段宽度不超过目标节limit；普通目标limit=sh_size，SHF_COMPRESSED目标从Elf64_Chdr.ch_size取声明解压大小，并检查24字节头可读。R_X86_64_NONE(0)无重定位字段，代码明确跳过其偏移越界检查。零宽TLSDESC_CALL仍要求offset不大于limit；没有验证实际解压后长度。草稿描述的是字段和声明大小，不应解读为每种标记都检查偏移或执行了解压。

fea0fe46，llvm-static-archives-native.py，第504–509行原文：

~~~python
        target = sections[section[7]]
        limit = target[5]
        if target[2] & 0x800:  # SHF_COMPRESSED: offsets use uncompressed size.
            if target[5] < 24 or target[4] + 24 > len(data):
                raise ValueError('short compressed ELF section header')
            limit = struct.unpack_from('<IIQQ', data, target[4])[2]
~~~

fea0fe46，llvm-static-archives-native.py，第519–525行原文：

~~~python
        for pos in range(section[4], section[4]+section[5], section[9]):
            r_offset, info = struct.unpack_from('<QQ', data, pos)
            kind, symbol_index = info & 0xffffffff, info >> 32
            if kind not in X86_64_RELOCATION_WIDTHS:
                raise ValueError('uncertified x86_64 relocation type: '+str(kind))
            if kind != 0 and r_offset + X86_64_RELOCATION_WIDTHS[kind] > limit:
                raise ValueError('relocation offset outside target section')
~~~

## “既有32/64位检查”的历史对照

只读60fabc72同一路径，第419–425行：

~~~python
            symbol = struct.unpack_from('<IBBHQQ', data, symbols[4]+symbol_index*symbols[9])
            if not target[2] & 2:
                continue
            checked += 1
            # SHN_ABS references do not need runtime relocation.
            if symbol[3] != 0xfff1 and (kind in (10, 11, 12, 14) or (kind == 1 and not target[2] & 1)):
                forbidden.append(dict(type=kind, target_section=section[7], symbol_index=symbol_index))
~~~

上述条件与fea0fe46第533行完全相同。本次未读取其他历史版本来外推更早的行为。
