"""Compare measured complete-root samples without treating df as root usage."""
import json
from pathlib import Path

D = Path(__file__).resolve().parent

def load(label, run):
    phases = json.loads((D / run / 'phase-summary.json').read_text())
    reports = {stage: json.loads((D / (label + '-products') / 'work' /
               ('disk-' + stage + '.json')).read_text())
               for stage in ('begin', 'tool-built', 'pipeline', 'post')}
    samples = []
    for line in (D / run / 'du-root-complete.jsonl').read_text().splitlines():
        row = json.loads(line)
        if row['rc'] == 0:
            samples.append(dict(time_ns=row['time_ns'],
                                end_ns=row['time_ns'] + int(row['seconds'] * 1e9),
                                bytes=int(row['stdout'].split()[0]),
                                scan_seconds=row['seconds']))
    anchors = phases['anchors']
    def first(kind):
        return next(x['time_ns'] for x in anchors if x['kind'] == kind)
    windows = [
        ('ordinary-build', samples[0]['time_ns'], first('install-start')),
        ('ordinary-install', first('install-start'), reports['begin']['time_ns']),
        ('bolt-through-compare-root', reports['begin']['time_ns'], first('compare-root-pass')),
        ('static-conversion-and-install', first('compare-root-pass'), first('find-debuginfo')),
        ('platform-post', first('find-debuginfo'), reports['post']['time_ns']),
        ('packaging', reports['post']['time_ns'], samples[-1]['end_ns'] + 1),
    ]
    windows_out = {}
    for name, start, end in windows:
        # Whole scans must be inside a phase; crossing scans are not assigned.
        selected = [x for x in samples if start <= x['time_ns'] and x['end_ns'] <= end]
        windows_out[name] = {'start_ns': start, 'end_ns': end, 'samples': len(selected),
                             'peak': max(selected, key=lambda x: x['bytes']) if selected else None}
    return {'run': run, 'complete_sample_count': len(samples),
            'peak': max(samples, key=lambda x: x['bytes']), 'phases': windows_out,
            'begin_after_sample': next((x for x in samples if x['time_ns'] >= reports['begin']['time_ns']), None),
            'post_after_sample': next((x for x in samples if x['time_ns'] >= reports['post']['time_ns']), None),
            'reports': {s: {k: r.get(k) for k in ('time_ns', 'used_bytes', 'free_bytes',
                         'cache_delta_allocated_bytes', 'cache_net_allocation_delta_bytes')}
                        for s, r in reports.items()}}

baseline = load('baseline', 'baseline-resume2')
revised = load('revised', 'revised-run')
out = {'baseline': baseline, 'revised': revised,
       'sampled_peak_reduction_bytes': baseline['peak']['bytes'] - revised['peak']['bytes'],
       'phase_peak_reduction_bytes': {
           p: (baseline['phases'][p]['peak']['bytes'] - revised['phases'][p]['peak']['bytes'])
           if baseline['phases'][p]['peak'] and revised['phases'][p]['peak'] else None
           for p in baseline['phases']},
       'limitations': ['Discrete du samples, not continuous peak.',
                      'Phase assignment excludes scans crossing boundaries.',
                      'Baseline resume2 follows prior compilation/resume segments; earlier samples must also be checked.',
                      'Filesystem free includes unrelated activity and is not a root-attributed delta.']}
residue = json.loads((D / 'revised-run/baseline-linker-temporary-residue.json').read_text())['total_allocated_bytes']
out['baseline_only_linker_residue_allocated_bytes'] = residue
out['estimated_peak_reduction_excluding_known_residue_bytes'] = out['sampled_peak_reduction_bytes'] - residue
out['post_end_sample_reduction_bytes'] = baseline['post_after_sample']['bytes'] - revised['post_after_sample']['bytes']
out['estimated_post_end_reduction_excluding_known_residue_bytes'] = out['post_end_sample_reduction_bytes'] - residue
out['bolt_transient_root_growth_bytes'] = {
    label: data['phases']['bolt-through-compare-root']['peak']['bytes'] - data['begin_after_sample']['bytes']
    for label, data in [('baseline', baseline), ('revised', revised)]}
out['limitations'].append('Subtracting known baseline-only residue is an estimate, not a controlled third build; sampling and resume-history differences remain.')
(D / 'measurement-comparison.json').write_text(json.dumps(out, indent=2) + '\n')
print(json.dumps({k: v for k, v in out.items() if k not in ('baseline', 'revised')}, indent=2))
