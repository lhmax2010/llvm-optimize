#!/usr/bin/env python3
"""Generate graph-based LLVM NEEDED expectations and check installed ELF files.

No compiler, build, or inspected ELF is executed. readelf is the only external
inspection command. Exit codes: 0 PASS, 1 FAIL, 2 inspection/input error,
3 ANALYSIS_PENDING (expected shared input absent from DT_NEEDED).
"""
import argparse
from collections import Counter, deque
import fnmatch
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess

STATIC = {'bin/clang-22', 'bin/lld', 'bin/llvm-ar'}
EXCEPTIONS = {'bin/llvm-tblgen', 'bin/clang-tblgen', 'bin/lldb-tblgen',
              'bin/llvm-config', 'bin/llvm-exegesis'}
CATEGORIES = ('static_three_groups', 'upstream_static_exceptions',
              'neither_shared_library', 'dynamic_llvm', 'dynamic_llvm_clang_cpp')
SPEC_ALIASES = {'clang++-22': 'clang++',
                'x86_64-tizen-linux-gnu-clang': 'clang',
                'x86_64-tizen-linux-gnu-clang++': 'clang++'}


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def shared_inputs(libraries):
    return {'libLLVM': bool(re.search(r'(?<![A-Za-z0-9_])libLLVM\.so(?:\.|\b)', libraries)),
            'libclang-cpp': bool(re.search(r'(?<![A-Za-z0-9_])libclang-cpp\.so(?:\.|\b)', libraries))}


def category(output, expected):
    if output in STATIC or output in EXCEPTIONS:
        if any(expected.values()):
            raise ValueError('static policy conflicts with graph: ' + output)
        return CATEGORIES[0] if output in STATIC else CATEGORIES[1]
    llvm, clang = expected['libLLVM'], expected['libclang-cpp']
    if clang and not llvm:
        raise ValueError('clang-cpp-only graph is outside the five certified categories: ' + output)
    return CATEGORIES[4] if clang else CATEGORIES[3] if llvm else CATEGORIES[2]


def canonical_alias(name, aliases):
    seen = set()
    while name in aliases:
        if name in seen:
            raise ValueError('alias cycle: ' + name)
        seen.add(name)
        name = aliases[name]
    return name


def generate(graph_path, aliases_path, patterns_path):
    graph = json.loads(Path(graph_path).read_text())
    aliases = dict(json.loads(Path(aliases_path).read_text()), **SPEC_ALIASES)
    patterns = [p for p in Path(patterns_path).read_text().splitlines() if p and not p.startswith('#')]
    names = [r['output'] for r in graph]
    if len(set(names)) != len(names):
        raise ValueError('duplicate graph outputs')
    declared = lambda p: any(fnmatch.fnmatchcase(p, pattern) for pattern in patterns)
    targets = []
    for r in graph:
        output = r['output']
        expected = shared_inputs(r['link_libraries'])
        if expected != {'libLLVM': r['libLLVM_so'], 'libclang-cpp': r['libclang_cpp_so']}:
            raise ValueError('stored graph booleans disagree with link inputs: ' + output)
        candidates = []
        if output.startswith(('bin/', 'lib64/')):
            candidates.append('/usr/' + output)
        if output.startswith('bin/'):
            name = output[4:]
            candidates.extend('/usr/bin/' + a for a in sorted(aliases)
                              if canonical_alias(a, aliases) == name)
        paths = sorted(set(p for p in candidates if declared(p)))
        # llvm.spec moves these files to its SDK directory after CMake install.
        if output in {'bin/lldb', 'bin/lldb-argdumper', 'bin/lldb-server'}:
            paths.extend(p for p in patterns if '*' not in p and
                         '/sdk_tools/lldb/bin/' in p and Path(p).name == Path(output).name)
        # %install copies liblldb.so*, not the broader %files liblldb*.so*.
        if output.startswith('lib64/liblldb.so'):
            sdk_path = '/home/owner/share/tmp/sdk_tools/lldb/lib64/' + Path(output).name
            if declared(sdk_path):
                paths.append(sdk_path)
        targets.append({'build_output': output, 'category': category(output, expected),
                        'expected_needed': expected, 'install_paths': sorted(set(paths)),
                        'install_scope': 'declared_in_rpm_files' if paths else 'graph_only_or_not_explicitly_listed',
                        'graph_line': r['line'], 'rule': r['rule']})
    return {'schema': 1, 'basis': 'docs/52 CMake configuration a; no runtime NEEDED observations',
            'sources': {Path(p).name: sha(p) for p in [graph_path, aliases_path, patterns_path]},
            'spec_alias_evidence': 'x86_64-hybrid-install.txt:6,8,9',
            'categories': dict(Counter(r['category'] for r in targets)),
            'target_count': len(targets), 'aliases': aliases, 'targets': targets}


def self_check(table, graph_path, aliases_path, patterns_path):
    regenerated = generate(graph_path, aliases_path, patterns_path)
    if table != regenerated:
        raise ValueError('expectation table differs from regenerated graph expectations')
    if table['target_count'] != 188:
        raise ValueError('expected 188 graph targets, got ' + str(table['target_count']))
    rows = {r['build_output']: r for r in table['targets']}
    for name in ['obj2yaml', 'yaml2obj']:
        if rows['bin/' + name]['category'] != 'neither_shared_library':
            raise ValueError('incorrect neither-library classification: ' + name)
    mapped = {}
    for row in table['targets']:
        for p in row['install_paths']:
            if p in mapped:
                raise ValueError('ambiguous install path: ' + p)
            mapped[p] = row['build_output']
    return {'status': 'PASS', 'graph_targets': 188, 'table_targets': len(rows),
            'missing_targets': [], 'duplicate_targets': [],
            'category_counts': table['categories'], 'declared_install_paths': len(mapped),
            'installed_bin_paths': sum(p.startswith('/usr/bin/') for p in mapped),
            'aliases': len(table['aliases']), 'obj2yaml_yaml2obj': 'neither_shared_library',
            'source_digests': table['sources']}


def rooted_path(root, logical):
    """Resolve absolute/relative symlinks inside a logical filesystem root."""
    root = Path(root).resolve()
    pending = deque(PurePosixPath('/' + logical.lstrip('/')).parts[1:])
    parts, followed = [], 0
    while pending:
        part = pending.popleft()
        if part in ('', '.'):
            continue
        if part == '..':
            if not parts:
                raise ValueError('path escapes logical root: ' + logical)
            parts.pop()
            continue
        p = root.joinpath(*parts, part)
        if p.is_symlink():
            followed += 1
            if followed > 40:
                raise ValueError('symlink loop: ' + logical)
            link = os.readlink(p)
            if link.startswith('/'):
                parts = []
            pending.extendleft(reversed(PurePosixPath(link).parts[1:] if link.startswith('/')
                                        else PurePosixPath(link).parts))
        else:
            parts.append(part)
    return root.joinpath(*parts)


def find_target(table, logical, resolved):
    explicit = [r for r in table['targets'] if logical in r['install_paths']]
    if len(explicit) == 1:
        return explicit[0]
    name = canonical_alias(PurePosixPath(logical).name, table['aliases'])
    # Covers SONAME symlinks, SDK relocation, and qemu-accel cp -aL aliases.
    matches = [r for r in table['targets'] if PurePosixPath(r['build_output']).name
               in {name, resolved.name}]
    if len(matches) != 1:
        raise ValueError('unmapped or ambiguous ELF: ' + logical)
    return matches[0]


def needed_status(expected, needed):
    actual = {'libLLVM': any(re.fullmatch(r'libLLVM\.so(?:\..+)?', n) for n in needed),
              'libclang-cpp': any(re.fullmatch(r'libclang-cpp\.so(?:\..+)?', n) for n in needed)}
    unexpected = sorted(k for k in expected if actual[k] and not expected[k])
    missing = sorted(k for k in expected if expected[k] and not actual[k])
    status = 'FAIL' if unexpected else 'ANALYSIS_PENDING' if missing else 'PASS'
    return {'status': status, 'actual_shared': actual,
            'unexpected_shared': unexpected, 'missing_expected_shared': missing}


def inspect_paths(table, root, paths, readelf='readelf', require_declared=False):
    results, seen = [], set()
    for logical in paths:
        logical = logical.strip()
        if not logical or logical in seen:
            continue
        seen.add(logical)
        row = {'path': logical}
        try:
            resolved = rooted_path(root, logical)
            row['resolved'] = str(resolved)
            if resolved.is_dir():
                if any(logical in t['install_paths'] for t in table['targets']):
                    raise ValueError('expected installed link target is a directory: ' + logical)
                row['status'] = 'SKIP_DIRECTORY'
            else:
                with resolved.open('rb') as f:
                    magic = f.read(4)
                if magic != b'\x7fELF':
                    if any(logical in t['install_paths'] for t in table['targets']):
                        raise ValueError('expected installed link target is not ELF: ' + logical)
                    row['status'] = 'SKIP_NON_ELF'
                else:
                    target = find_target(table, logical, resolved)
                    p = subprocess.run([readelf, '-dW', str(resolved)], capture_output=True,
                                       text=True, timeout=30, env=dict(os.environ, LC_ALL='C'))
                    row.update(build_output=target['build_output'], category=target['category'],
                               expected_needed=target['expected_needed'],
                               readelf_argv=[readelf, '-dW', str(resolved)],
                               readelf_exit=p.returncode, stdout=p.stdout, stderr=p.stderr)
                    if p.returncode:
                        raise ValueError('readelf failed: ' + str(p.returncode))
                    needed = re.findall(r'\(NEEDED\).*?\[([^\]]+)\]', p.stdout)
                    row['needed'] = needed
                    row.update(needed_status(target['expected_needed'], needed))
        except (OSError, ValueError, subprocess.TimeoutExpired) as ex:
            row.update(status='ERROR', error=str(ex))
        results.append(row)
    if require_declared:
        declared = {p for r in table['targets'] for p in r['install_paths']}
        for missing in sorted(declared - seen):
            results.append({'path': missing, 'status': 'ERROR',
                            'error': 'declared installed target missing from input path list'})
    counts = Counter(r['status'] for r in results)
    if counts['ERROR']:
        code, status = 2, 'ERROR'
    elif counts['FAIL']:
        code, status = 1, 'FAIL'
    elif counts['ANALYSIS_PENDING']:
        code, status = 3, 'ANALYSIS_PENDING'
    elif not counts['PASS']:
        code, status = 2, 'ERROR_NO_ELF_CHECKED'
    else:
        code, status = 0, 'PASS'
    return {'status': status, 'exit_code': code, 'counts': dict(counts),
            'note': 'A missing expected DT_NEEDED requires analysis (e.g. --as-needed), never automatic PASS.',
            'results': results}


def write_json(path, data):
    Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')


def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest='action', required=True)
    for action in ['generate', 'self-check']:
        s = sub.add_parser(action)
        s.add_argument('--graph', type=Path, required=True)
        s.add_argument('--aliases', type=Path, required=True)
        s.add_argument('--rpm-paths', type=Path, required=True)
        if action == 'self-check':
            s.add_argument('--table', type=Path, required=True)
        s.add_argument('--output', type=Path, required=True)
    s = sub.add_parser('check')
    s.add_argument('--table', type=Path, required=True)
    s.add_argument('--root', type=Path, default=Path('/'))
    s.add_argument('--paths', type=Path, required=True, help='actual RPM-listed file paths, one per line')
    s.add_argument('--readelf', default='readelf')
    s.add_argument('--require-declared', action='store_true',
                   help='also reject any declared installed target omitted from the path list')
    s.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    try:
        if args.action == 'generate':
            write_json(args.output, generate(args.graph, args.aliases, args.rpm_paths))
        elif args.action == 'self-check':
            table = json.loads(args.table.read_text())
            write_json(args.output, self_check(table, args.graph, args.aliases, args.rpm_paths))
        else:
            result = inspect_paths(json.loads(args.table.read_text()), args.root,
                                   args.paths.read_text().splitlines(), args.readelf, args.require_declared)
            write_json(args.output, result)
            print(json.dumps({'status': result['status'], 'counts': result['counts']}))
            return result['exit_code']
    except (OSError, ValueError, KeyError) as ex:
        p.exit(2, 'ERROR: ' + str(ex) + '\n')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
