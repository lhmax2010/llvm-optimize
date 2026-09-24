#!/usr/bin/env python3
# Standalone RPM Source; copied policy from the certified docs/28 converter.
# Embedded inspect_llvm_archives.py SHA256 81008a4859172318da880f224e53c5136958c29ebc9e12194e8f729fbd2d9ae0
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


# Embedded convert_static_archives.py SHA256 26089402335e36f93a04086e8ad77db799a71e87f5b462e58ec97932807ceffa
#!/usr/bin/env python3
"""Convert bitcode archive members to native objects, without changing inputs.

Use inside a separately bounded cgroup. Four workers, 4 GiB AS per tool;
the first failure cancels work and terminates outstanding child processes.
Outputs and evidence require a new directory. GNU ar preserves member order
and duplicate names by taking each input from a separate ordinal directory.
"""
import argparse
from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, wait
import hashlib
import json
import os
from pathlib import Path
import re
import signal
import shlex
import struct
import subprocess
import threading
import time


# Verified against the saved real-TU command and LLVM 22 source. These options
# must be supplied to native code generation; they are not recovered merely by
# loading IR. Debug metadata, CPU/features and linkage remain in the input IR.
BACKEND_FLAGS = ['-O3', '-ffunction-sections', '-fdata-sections',
                 '-funique-section-names', '-faddrsig', '-g', '-gdwarf-4',
                 '-ffp-contract=on']


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def ir_settings(lines, require_recorded_options=False):
    """Read relocation flags and retained function attributes, never edit IR."""
    retained = []
    triple = None
    levels = {}
    cpus, features = set(), set()
    command_id, recorded_command = None, None
    for line in lines:
        if line.startswith('!llvm.commandline = '):
            match = re.fullmatch(r'!llvm.commandline = !\{!(\d+)\}\s*', line)
            if not match:
                raise ValueError('exactly one recorded command is required')
            command_id = match[1]
        if command_id is not None and line.startswith('!'+command_id+' = '):
            match = re.fullmatch(r'!\d+ = !\{!"(.*)"\}\s*', line)
            if not match:
                raise ValueError('invalid recorded command metadata')
            recorded_command = shlex.split(re.sub(r'\\([0-9A-Fa-f]{2})',
                lambda m: chr(int(m[1], 16)), match[1]))
        if line.startswith('target triple = '):
            triple = line.split('"')[1]
            retained.append(line.rstrip())
        if line.startswith('attributes #'):
            retained.append(line.rstrip())
            cpus.update(re.findall(r'"target-cpu"="([^"]+)"', line))
            features.update(re.findall(r'"target-features"="([^"]+)"', line))
        if line.startswith('!') and any('"'+n+'"' in line for n in ('PIC Level', 'PIE Level', 'Code Model')):
            retained.append(line.rstrip())
            match = re.search(r'!"(PIC Level|PIE Level|Code Model)", i32 (\d+)', line)
            if not match:
                raise ValueError('unrecognized relocation flag: '+line.rstrip())
            key, value = match.groups()
            if key in levels and levels[key] != int(value):
                raise ValueError('conflicting relocation flags')
            levels[key] = int(value)
    if not triple or not triple.startswith('x86_64-'):
        raise ValueError('only an explicit x86_64 IR target is certified')
    pic, pie = levels.get('PIC Level', 0), levels.get('PIE Level', 0)
    if pic not in (0, 1, 2) or pie not in (0, 1, 2) or (pie and pie != pic):
        raise ValueError('unsupported PIC/PIE flags')
    if 'Code Model' in levels:
        raise ValueError('explicit code model requires separate certification')
    if require_recorded_options:
        if not recorded_command:
            raise ValueError('missing original command: backend policy cannot be certified')
        optimizations = [x for x in recorded_command if re.fullmatch(r'-O(?:[0-3szg]|fast)', x)]
        if not optimizations or optimizations[-1] != '-O3':
            raise ValueError('original optimization level is not O3')
        for option in ('function-sections', 'data-sections'):
            settings = [x for x in recorded_command if x in ('-f'+option, '-fno-'+option)]
            if not settings or settings[-1] != '-f'+option:
                raise ValueError('original command lacks enabled '+option)
        if '-gdwarf-4' not in recorded_command:
            raise ValueError('original DWARF setting not certified')
    # Function-level CPU/features remain in the IR; do not override with -march.
    flags = ['--no-default-config', '--target='+triple, '-x', 'ir', *BACKEND_FLAGS, '-c']
    flags += ([{1: '-fpie', 2: '-fPIE'}[pie]] if pie else
              [{1: '-fpic', 2: '-fPIC'}[pic]] if pic else ['-fno-pic', '-fno-pie'])
    return dict(triple=triple, pic_level=pic, pie_level=pie, target_cpu=sorted(cpus),
                target_features=sorted(features), flags=flags, evidence=retained,
                recorded_command=recorded_command)


def pic_relocations(data):
    """Reject absolute relocations in read-only allocated x86_64 sections.

    Debug relocations are excluded. Absolute 32-bit relocations against
    non-absolute symbols are also rejected in writable allocated sections.
    PC-relative relocations are not all forbidden: e.g. hidden symbols and
    .eh_frame legitimately use them. A consumer GNU ld -shared check follows.
    """
    if member_kind(data) != 'machine' or data[4:6] != b'\x02\x01' or struct.unpack_from('<H', data, 18)[0] != 62:
        raise ValueError('not x86_64 ELF64 little-endian ET_REL')
    off = struct.unpack_from('<Q', data, 40)[0]
    stride, count = struct.unpack_from('<HH', data, 58)
    if not count:
        count = struct.unpack_from('<IIQQQQIIQQ', data, off)[5]
    sections = [struct.unpack_from('<IIQQQQIIQQ', data, off+i*stride) for i in range(count)]
    checked, forbidden = 0, []
    for section in sections:
        if section[1] not in (4, 9):
            continue
        target = sections[section[7]]
        if not target[2] & 2:  # SHF_ALLOC; excludes all debug sections
            continue
        symbols = sections[section[6]]
        for pos in range(section[4], section[4]+section[5], section[9]):
            _, info = struct.unpack_from('<QQ', data, pos)
            kind, symbol_index = info & 0xffffffff, info >> 32
            symbol = struct.unpack_from('<IBBHQQ', data, symbols[4]+symbol_index*symbols[9])
            checked += 1
            # SHN_ABS references do not need runtime relocation.
            if symbol[3] != 0xfff1 and (kind in (10, 11) or (kind == 1 and not target[2] & 1)):
                forbidden.append(dict(type=kind, target_section=section[7], symbol_index=symbol_index))
    return dict(checked=checked, forbidden=forbidden)


class Commands:
    def __init__(self):
        self.stop = threading.Event()
        self.lock = threading.Lock()
        self.children = set()

    def cancel(self):
        self.stop.set()
        with self.lock:
            for child in self.children:
                try:
                    os.killpg(child.pid, signal.SIGTERM)
                except ProcessLookupError:
                    pass

    def run(self, argv, prefix, stdout=None):
        prefix = Path(prefix)
        timing = prefix.with_suffix('.time')
        log = prefix.with_suffix('.log')
        command = ['/usr/bin/time', '-f', '%e %U %S %M %x', '-o', str(timing),
                   'prlimit', '--as=4294967296', '--core=0', '--', *map(str, argv)]
        start = time.monotonic()
        with log.open('wb') as err:
            with self.lock:
                if self.stop.is_set():
                    raise RuntimeError('cancelled after first failure')
                child = subprocess.Popen(command, stdout=stdout if stdout is not None else err,
                                         stderr=err, start_new_session=True)
                self.children.add(child)
            try:
                rc = child.wait()
            finally:
                with self.lock:
                    self.children.discard(child)
        record = dict(argv=list(map(str, argv)), bounded_argv=command,
                      elapsed_seconds=time.monotonic()-start, exit=rc)
        if timing.exists():
            record['time_raw'] = timing.read_text()
            line = record['time_raw'].splitlines()[-1].split()
            if len(line) == 5:
                record.update(wall=float(line[0]), user=float(line[1]), sys=float(line[2]), max_rss_kib=int(line[3]))
        prefix.with_suffix('.json').write_text(json.dumps(record, indent=2)+'\n')
        if rc:
            self.cancel()
            raise RuntimeError(f'command failed ({rc}): {argv}; see {log}')
        return record


def convert(root, output, clang, disassembler, loader=None, library_path=None):
    output.mkdir(parents=True, exist_ok=False)
    command = Commands()
    prefix = ([str(loader), '--library-path', library_path] if loader else [])
    summary = dict(started=time.time(), input_root=str(root), output_root=str(output),
                   workers=4, as_bytes=4*1024**3, archives=[], status='RUNNING')
    def save():
        (output/'summary.json').write_text(json.dumps(summary, indent=2)+'\n')
    save()
    def interrupted(sig, frame):
        command.cancel()
        raise KeyboardInterrupt(f'signal {sig}')
    old_handlers = {sig: signal.signal(sig, interrupted) for sig in (signal.SIGTERM, signal.SIGINT)}
    try:
        for archive in sorted(root.rglob('*.a')):
            if archive.is_symlink():
                raise ValueError('archive symlink not certified: '+str(archive))
            before = inspect(archive)
            if not before['bitcode']:
                continue  # compiler-rt and any other native archive are unchanged
            if before['thin'] or before['other']:
                raise ValueError('unsupported archive format: '+str(archive))
            rel = archive.relative_to(root)
            work = output/'members'/rel
            work.mkdir(parents=True)
            (work/'before.json').write_text(json.dumps(before, indent=2)+'\n')
            paths = []
            with archive.open('rb') as stream:
                for member in before['members']:
                    if Path(member['name']).name != member['name'] or member['name'] in ('.', '..'):
                        raise ValueError('unsafe archive member name')
                    folder = work/f"{member['ordinal']:05d}"
                    folder.mkdir()
                    source = folder/'input.bc'
                    target = folder/member['name']
                    if target == source:
                        raise ValueError('reserved input name collision')
                    stream.seek(member['offset'])
                    payload = stream.read(member['size'])
                    if hashlib.sha256(payload).hexdigest() != member['sha256']:
                        raise ValueError('extracted member SHA mismatch')
                    (source if member['kind'] == 'bitcode' else target).write_bytes(payload)
                    paths.append((member, source, target))
            def process(item):
                member, source, target = item
                if member['kind'] == 'machine':
                    if sha(target) != member['sha256']:
                        raise ValueError('native member changed')
                    relocs = pic_relocations(target.read_bytes())
                    (source.parent/'relocations.json').write_text(json.dumps(relocs, indent=2)+'\n')
                    return dict(ordinal=member['ordinal'], name=member['name'], preserved=True,
                                relocation_check=relocs)
                text_ir = source.with_suffix('.ll')
                with text_ir.open('wb') as out:
                    command.run([*prefix, str(disassembler), str(source), '-o', '-'], source.parent/'disassemble', stdout=out)
                with text_ir.open() as lines:
                    settings = ir_settings(lines, require_recorded_options=True)
                (source.parent/'ir-settings.json').write_text(json.dumps(settings, indent=2)+'\n')
                text_ir.unlink()
                record = command.run([*prefix, str(clang), *settings['flags'], str(source), '-o', str(target)], source.parent/'convert')
                data = target.read_bytes()
                relocs = pic_relocations(data)  # also verifies x86_64 ET_REL
                (source.parent/'relocations.json').write_text(json.dumps(relocs, indent=2)+'\n')
                if settings['pic_level'] and relocs['forbidden']:
                    raise ValueError('non-PIC relocation in '+str(target))
                return dict(ordinal=member['ordinal'], name=member['name'], preserved=False,
                            settings=settings, conversion=record, sha256=sha(target))
            results = []
            iterator = iter(paths)
            with ThreadPoolExecutor(max_workers=4) as pool:
                pending = {pool.submit(process, item) for item in list(next(iterator, None) for _ in range(4)) if item is not None}
                try:
                    while pending:
                        done, pending = wait(pending, return_when=FIRST_COMPLETED)
                        for future in done:
                            results.append(future.result())
                        for _ in done:
                            item = next(iterator, None)
                            if item is not None:
                                pending.add(pool.submit(process, item))
                except BaseException:
                    command.cancel()
                    for future in pending:
                        future.cancel()
                    raise
            target_archive = output/'archives'/rel
            target_archive.parent.mkdir(parents=True, exist_ok=True)
            command.run(['/usr/bin/ar', 'qcDS', str(target_archive), *[str(t) for _, _, t in paths]], work/'pack')
            command.run(['/usr/bin/ar', 'sD', str(target_archive)], work/'index')
            after = inspect(target_archive)
            (work/'after.json').write_text(json.dumps(after, indent=2)+'\n')
            if [(m['name'], m['occurrence']) for m in before['members']] != [(m['name'], m['occurrence']) for m in after['members']]:
                raise ValueError('member identity or order changed')
            if after['bitcode'] or after['other'] or not after['index_equals_machine_symbols']:
                raise ValueError('output format/index mismatch')
            for old, new in zip(before['members'], after['members']):
                if old['kind'] == 'machine' and old['sha256'] != new['sha256']:
                    raise ValueError('native member not preserved in archive')
            record = dict(path=str(rel), before_sha256=before['sha256'], after_sha256=after['sha256'],
                          before_bytes=before['bytes'], after_bytes=after['bytes'], members=before['member_count'],
                          converted=before['bitcode'], preserved=before['machine'], index_entries=after['index_entries'],
                          debug_members=sum(bool(m['debug_sections']) for m in after['members']),
                          results=sorted(results, key=lambda x:x['ordinal']))
            summary['archives'].append(record)
            save()
            print(json.dumps({k:v for k,v in record.items() if k!='results'}), flush=True)
            for _, source, target in paths:
                if source.exists():
                    source.unlink()
                target.unlink()
        summary['status'] = 'PASS'
        return summary
    except BaseException as error:
        command.cancel()
        summary.update(status='FAIL', reason=str(error))
        raise
    finally:
        summary['elapsed_seconds'] = time.time()-summary['started']
        save()
        for sig, handler in old_handlers.items():
            signal.signal(sig, handler)


# Packaging entry: input install tree stays intact until every conversion passes.
def install_main():
    import shutil
    parser = argparse.ArgumentParser(description="Convert installed x86_64 ThinLTO archives before unchanged RPM brp strip")
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--build', type=Path, required=True)
    parser.add_argument('--evidence', type=Path, required=True)
    args = parser.parse_args()
    root, build, output = args.root.resolve(), args.build.resolve(), args.evidence.resolve()
    if root == Path('/') or output.is_relative_to(root):
        parser.error('separate non-system install root and evidence directory required')
    print('NATIVE_ARCHIVES_BEGIN', time.time(), flush=True)
    result = convert(root, output, build/'bin/clang-22', build/'bin/llvm-dis')
    for record in result['archives']:
        destination = root/record['path']
        candidate = output/'archives'/record['path']
        if sha(destination) != record['before_sha256'] or sha(candidate) != record['after_sha256']:
            raise RuntimeError('archive identity changed before install replacement')
        shutil.copyfile(candidate, destination)
        if sha(destination) != record['after_sha256']:
            raise RuntimeError('archive copy identity mismatch')
        print('NATIVE_ARCHIVE_INSTALLED', json.dumps({k:v for k,v in record.items() if k!='results'}), flush=True)
    print('NATIVE_ARCHIVES_END', time.time(), 'PASS', len(result['archives']), flush=True)

if __name__ == '__main__':
    install_main()
