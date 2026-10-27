from pathlib import Path
D=Path(__file__).resolve().parent;S=D/'source/packaging';p=S/'clang-bolt-helper.py';s=p.read_text()
s=s.replace('def security_compare(ordinary, candidate):','def security_compare(ordinary, candidate, ignore_paths=False):').replace('differences = [key for key in before if before[key] != after[key]]','differences = [key for key in before if before[key] != after[key] and\n                   not (ignore_paths and key in (\'DT_RPATH\', \'DT_RUNPATH\'))]',1)
marker='def tiny_gate(ordinary, candidate, work, resource_dir=None):'
new='''def installed_baseline(root, output):
    entity = Path(root)/'usr/bin/clang-22'
    properties = security_properties(entity)
    result = {'path': str(entity), 'sha256': digest(entity),
              'DT_RPATH': properties['DT_RPATH'], 'DT_RUNPATH': properties['DT_RUNPATH'],
              'security_properties': properties}
    save(output, result)
    return result


def installed_security(baseline, candidate):
    require(Path(baseline).is_file(), 'installed-baseline missing: '+str(baseline))
    before = json.loads(Path(baseline).read_text())['security_properties']
    after = json.loads(json.dumps(security_properties(candidate)))
    differences = {k: {'installed_baseline': before.get(k), 'candidate': after.get(k)}
                   for k in before.keys() | after.keys() if before.get(k) != after.get(k)}
    require(not differences, 'installed-baseline security attributes differ: '+json.dumps(differences))
    return {'installed_security_preserved': True, 'baseline_sha256': digest(baseline),
            'candidate_sha256': digest(candidate)}


def rpath_layout(path):
    """Freeze headers and every file byte except the two permitted sections."""
    elf = ELF(path)
    try:
        allowed = sorted((s[4], s[4]+s[5]) for name, s in elf.by_name.items()
                         if name in ('.dynamic', '.dynstr'))
        cursor = 0; frozen = hashlib.sha256()
        for start, end in allowed:
            require(start >= cursor, 'overlapping RPATH sections')
            frozen.update(elf.data[cursor:start]); cursor = end
        frozen.update(elf.data[cursor:])
        dynamic = elf.by_name.get('.dynamic')
        tags = [struct.unpack_from('<qQ', elf.data, i)[0]
                for i in range(dynamic[4], dynamic[4]+dynamic[5], 16)] if dynamic else []
        return {'file_bytes': len(elf.data), 'program_headers': elf.phdrs,
                'section_headers': elf.sections, 'dynamic_tags': tags,
                'unchanged_bytes_sha256': frozen.hexdigest(),
                'code_sections': {name: hashlib.sha256(elf.data[s[4]:s[4]+s[5]]).hexdigest()
                                  for name, s in elf.by_name.items() if s[2] & 4 and s[1] != 8}}
    finally:
        elf.close()


def cmake_literal(value):
    require('\\x00' not in value, 'NUL in CMake argument')
    delimiter = '='
    while ']'+delimiter+']' in value:
        delimiter += '='
    return '['+delimiter+'['+value+']'+delimiter+']'


def adjust_rpath(candidate, baseline, work, identity):
    candidate, work = Path(candidate), Path(work)
    require(Path(baseline).is_file(), 'installed-baseline missing: '+str(baseline))
    expected = json.loads(Path(baseline).read_text())
    props = security_properties(candidate)
    keys = ('DT_RPATH', 'DT_RUNPATH')
    old, new = {k: props[k] for k in keys}, {k: expected[k] for k in keys}
    require([k for k in keys if old[k] is not None] == [k for k in keys if new[k] is not None],
            'RPATH tag types differ from installed-baseline')
    require(sum(old[k] is not None for k in keys) <= 1, 'multiple RPATH tags unsupported')
    layout = rpath_layout(candidate); stripped_sha = digest(candidate)
    if old != new:
        key = next(k for k in keys if old[k] is not None)
        script = work/'candidate-rpath.cmake'
        atomic_text(script, 'file(RPATH_CHANGE FILE '+cmake_literal(str(candidate))+\n                    ' OLD_RPATH '+cmake_literal(old[key])+' NEW_RPATH '+cmake_literal(new[key])+')\\n')
        call(['cmake', '-P', str(script)], work/'candidate-rpath.log', timeout=60)
    require(rpath_layout(candidate) == layout, 'RPATH_CHANGE changed ELF layout or non-path content')
    actual = security_properties(candidate)
    require({k: actual[k] for k in keys} == new, 'ELF RPATH differs from installed-baseline')
    log = work/'candidate-readelf.log'
    call(['readelf', '-dW', str(candidate)], log, timeout=60)
    text = log.read_text(); readelf_paths = {}
    for key in keys:
        matches = re.findall(r'\\('+key[3:]+r'\\)[^\\n]*\\[([^\\n]*)\\]', text)
        require(len(matches) <= 1, 'duplicate readelf path tag: '+key)
        readelf_paths[key] = matches[0] if matches else None
    require(readelf_paths == new, 'readelf RPATH differs from installed-baseline')
    checked = installed_security(baseline, candidate)
    identity.update(strip_all_sha256=stripped_sha, rpath_adjusted_sha256=digest(candidate),
                    after_sha256=digest(candidate), installed_baseline_sha256=digest(baseline),
                    rpath={'before': old, 'after': new, 'layout': layout, 'readelf': readelf_paths,
                           'security': checked})
    validate_identity(identity, candidate)
    save(work/'identity.json', identity)
    return identity


'''
s=s.replace(marker,new+marker)
s=s.replace("identity.get('after_sha256'), 'stripped candidate SHA mismatch'", "identity.get('rpath_adjusted_sha256', identity.get('after_sha256')), 'stripped candidate SHA mismatch'")
s=s.replace("result = {'installed_sha256':actual, 'identity':identity,", "identity = dict(identity, installed_sha256=actual)\n        result = {'installed_sha256':actual, 'identity':identity,")
s=s.replace("security = security_compare(ordinary, str(entity))", "security = security_compare(ordinary, str(entity), ignore_paths=True)\n    baseline = Path(ordinary).parent/'installed-baseline.json'\n    installed = installed_security(baseline, entity)")
s=s.replace("'strip_identity_pass': True, 'security': security}", "'strip_identity_pass': True, 'security': security, 'installed_security': installed}")
s=s.replace("descriptions = []\n    for index, line in enumerate(lines, 1):", "descriptions = []; completed = set()\n    for line in lines:")
s=s.replace("require(int(match[1]) == index and int(match[2]) == len(lines), 'non-contiguous or truncated BOLT plan: '+line)", "require(1 <= int(match[1]) <= len(lines) and int(match[2]) == len(lines) and\n                int(match[1]) not in completed, 'invalid or truncated BOLT plan: '+line)\n        completed.add(int(match[1]))")
s=s.replace("require(f == len(descriptions)+1 and f <= t, 'invalid real build progress: '+line)","require(1 <= f <= t and t == plan['tasks'] and f not in [c[0] for c in counters],\n                'invalid real build progress: '+line)")
s=s.replace("require(plan['plan_type'] != 'build' or bool(descriptions), 'build plan executed no tasks')", "require(set(descriptions) == set(plan['descriptions']) and len(descriptions) == plan['tasks'],\n            'executed task set/count differs from approved plan')")
s=s.replace("edge = (work/'link.original').read_text()\n    reference", "baseline = work/'installed-baseline.json'\n    require(baseline.is_file(), 'installed-baseline missing: '+str(baseline))\n    edge = (work/'link.original').read_text()\n    reference",1)
s=s.replace("security = security_compare(str(work/'ordinary-clang-22'), str(work/'clang.candidate'))", "identity = adjust_rpath(work/'clang.candidate',baseline,work,identity)\n    security = security_compare(str(work/'ordinary-clang-22'), str(work/'clang.candidate'), ignore_paths=True)")
s=s.replace("s=sub.add_parser('snapshot');", "s=sub.add_parser('installed-baseline');s.add_argument('root');s.add_argument('output')\n    s=sub.add_parser('snapshot');")
s=s.replace("elif a.cmd=='snapshot':", "elif a.cmd=='installed-baseline':result=installed_baseline(a.root,a.output)\n    elif a.cmd=='snapshot':")
p.write_text(s)
p=S/'llvm.spec';s=p.read_text().replace('python3 -B %{SOURCE1201} snapshot', 'python3 -B %{SOURCE1201} installed-baseline "%{buildroot}" "$BOLT_WORK/installed-baseline.json" || exit 1\npython3 -B %{SOURCE1201} snapshot',1).replace('-- ninja -j 1 llvm-bolt','-- ninja -j %{mlgo_build_jobs} llvm-bolt');p.write_text(s)
