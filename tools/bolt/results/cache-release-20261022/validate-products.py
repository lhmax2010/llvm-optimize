"""Read-only retained product comparison; inventories are separate evidence files."""
import hashlib, json, subprocess, sys, time
from pathlib import Path

D = Path(__file__).resolve().parent
E = D / 'rpm-validation'
E.mkdir(exist_ok=True)

def sha(p):
    h = hashlib.sha256()
    with p.open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()

def run(name, argv):
    start = time.time_ns()
    with (E / (name + '.stdout')).open('w') as out, (E / (name + '.stderr')).open('w') as err:
        p = subprocess.run(argv, stdout=out, stderr=err)
    (E / (name + '.json')).write_text(json.dumps({'argv': argv, 'rc': p.returncode,
        'start_ns': start, 'end_ns': time.time_ns()}, indent=2) + '\n')
    if p.returncode:
        raise RuntimeError(name + ' failed; see saved stdout/stderr')

identities = {}
for label in ('baseline', 'revised'):
    root = D / (label + '-products')
    identities[label] = {name: sha(root / 'binaries' / name)
                        for name in ('clang.candidate', 'ordinary-clang-22', 'llvm-bolt')}
    binary = sorted((root / 'RPMS').rglob('*.rpm'))
    source = sorted((root / 'SRPMS').rglob('*.rpm'))
    assert len(binary) == 22 and len(source) == 1, (label, len(binary), len(source))
    header_rows = []
    for rpm in binary + source:
        p = subprocess.run(['rpm', '-qp', '--qf',
            '%{NAME}\t%{VERSION}\t%{RELEASE}\t%{ARCH}\t%{BUILDTIME}\t%{BUILDHOST}\n',
            str(rpm)], capture_output=True, text=True)
        assert p.returncode == 0, (rpm, p.stderr)
        header_rows.append({'rpm': rpm.name, 'kind': 'source' if rpm in source else 'binary',
                            'bytes': rpm.stat().st_size, 'sha256': sha(rpm),
                            'header': p.stdout, 'stderr': p.stderr})
    (E / (label + '-rpm-headers.json')).write_text(json.dumps(header_rows, indent=2) + '\n')
(E / 'binary-identities.json').write_text(json.dumps(identities, indent=2) + '\n')
assert identities['baseline']['clang.candidate'] == identities['revised']['clang.candidate'], identities

for label in ('baseline', 'revised'):
    for kind in ('RPMS', 'SRPMS'):
        run(label + '-' + kind, [sys.executable, '-B', str(D / 'rpm_inventory.py'),
            str(D / (label + '-products') / kind), str(D / (label + '-rpm-inventory'))])
run('payload-comparison', [sys.executable, '-B', str(D / 'compare-rpm-payloads.py'),
    str(D / 'baseline-rpm-inventory'), str(D / 'revised-rpm-inventory'),
    str(D / 'rpm-comparison.json')])
rows = json.loads((D / 'rpm-comparison.json').read_text())
summary = {'candidate_equal': True, 'identities': identities,
           'binary_rpms': [r for r in rows if not r['rpm'].endswith('.src.rpm.json')],
           'source_rpms': [r for r in rows if r['rpm'].endswith('.src.rpm.json')]}
(E / 'product-comparison-summary.json').write_text(json.dumps(summary, indent=2) + '\n')
print(json.dumps({'candidate_equal': True,
    'binary_rpm_count': len(summary['binary_rpms']),
    'binary_payload_equal_except_mtime': sum(r.get('payload_equal_except_mtime', False) for r in summary['binary_rpms']),
    'source_rpm_count': len(summary['source_rpms'])}, indent=2))
