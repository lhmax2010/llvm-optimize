"""Build a line-addressed timeline from the two preserved raw package logs."""
import csv, json, re
from pathlib import Path

D = Path(__file__).resolve().parent
rows = []
for label, run in [('baseline-resume2', 'baseline-resume2'), ('revised', 'revised-run')]:
    p = D / run / 'rpm-build.log'
    if not p.exists():
        p = D / run / 'build.log'
    for number, line in enumerate(p.read_text(errors='replace').splitlines(), 1):
        match = re.match(r'\[\s*([0-9.]+)s\]', line)
        if not match:
            continue
        stage = None
        if 'BOLT_DISK_REPORT {' in line:
            stage = 'disk-report-' + json.loads(line.split('BOLT_DISK_REPORT ', 1)[1])['stage']
        else:
            for token in ['Executing(%prep)', 'Executing(%build)', 'Executing(%install)',
                          'BOLT_PIPELINE_PASS', 'BOLT_COMPARE_ROOT_PASS', 'BOLT_CACHE_RELEASE removed',
                          'NATIVE_ARCHIVES_BEGIN', 'NATIVE_ARCHIVES_END', 'BOLT_POST_GATE_PASS',
                          'Processing files:', 'Wrote:', 'Executing(%clean)']:
                if token in line and not re.search(r'\]\s*\+', line):
                    stage = token
                    break
            if '+ python3 -B ' in line and 'clang-bolt-helper.py install ' in line:
                stage = 'candidate-install-call'
            if '+ ' in line and 'find-debuginfo.sh' in line:
                stage = 'find-debuginfo-call'
        if stage:
            rows.append([label, str(p.relative_to(D)), number, match[1], stage, line])
with (D / 'timeline-final.tsv').open('w', newline='') as f:
    out = csv.writer(f, delimiter='\t')
    out.writerow(['round', 'log', 'line', 'native_seconds', 'stage', 'raw_text'])
    out.writerows(rows)
print('timeline rows', len(rows))
