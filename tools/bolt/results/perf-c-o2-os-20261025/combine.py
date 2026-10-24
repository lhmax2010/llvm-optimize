"""Prefer the predeclared warning-free C experiment; preserve all initial C results."""
from pathlib import Path
import json,statistics,math,csv,shutil,collections,gzip
E=Path(__file__).resolve().parent
def geo(v):return math.exp(statistics.mean(math.log(x) for x in v))
def save(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
def load_rows(p):
    raw=p.read_text() if p.exists() else gzip.decompress(p.with_suffix(p.suffix+'.gz').read_bytes()).decode()
    return [json.loads(x) for x in raw.splitlines()]
base=json.loads((E/'summary.json').read_text())
assert 'total_measured_compiles' not in base,'Run original summarize.py first, once'
main=load_rows(E/'samples.jsonl');clean=load_rows(E/'clean-c/samples.jsonl')
assert len(main)==6000 and len(clean)==2400
end=json.loads((E/'clean-c/finished.json').read_text());assert end['status']=='COMPLETE' and end['inputs_unchanged']
units=json.loads((E/'clean-c/cases.json').read_text());cases=json.loads((E/'cases.json').read_text())
official=[]
for r in main:
    if r['language']=='C++':official.append(dict(r,experiment='main-matrix'))
for r in clean:
    official.append(dict(r,experiment='clean-c',case=units[r['case']]['original_matrix_case'],clean_case=r['case']))
assert len(official)==6000
groups=collections.defaultdict(list)
for r in official:groups[r['group'],r['case']].append(r)
medians=[]
for (group,index),ss in sorted(groups.items()):
    u=cases[index];a=[s['wall_s'] for s in ss if s['role']=='ordinary'];b=[s['wall_s'] for s in ss if s['role']=='candidate'];assert len(a)==len(b)==5
    am=statistics.median(a);bm=statistics.median(b)
    medians.append(dict(group=group,case=index,experiment=ss[0]['experiment'],language=u['language'],option=u['option'],target=u['target'],name=u['name'],cohort=u['cohort'],ordinary_median_s=am,candidate_median_s=bm,ratio=bm/am,saved_percent=(1-bm/am)*100,ordinary_samples=a,candidate_samples=b,all_objects_equal=all(s['byte_equal'] for s in ss),input_sha256=u['input_sha256']))
assert len(medians)==600
summary=[]
for cell in base['summary']:
    rs=[r for r in medians if all(r[k]==cell[k] for k in ['group','language','option','target'])];assert len(rs)==20
    ratio=geo(r['ratio'] for r in rs)
    summary.append(dict(cell,ratio=ratio,saved_percent=(1-ratio)*100,all_objects_equal=all(r['all_objects_equal'] for r in rs),ordinary_median_range=[min(r['ordinary_median_s'] for r in rs),max(r['ordinary_median_s'] for r in rs)]))
save(E/'main-matrix-summary.json',base)
shutil.copyfile(E/'per-file-medians.csv',E/'main-matrix-per-file-medians.csv')
all_rows=main+clean
loads=[float(r[k]['loadavg'].split()[0]) for r in all_rows for k in ['before','after']]
freq=[int(r[k]['frequency_kHz']) for r in all_rows for k in ['before','after'] if r[k]['frequency_kHz'].isdigit()]
result=dict(base,summary=summary,compiles=6000,total_measured_compiles=8400,auxiliary_warning_C_compiles=2400,comparison_outputs=5400,total_comparison_outputs=7560,unequal_outputs=[dict(group=r['group'],case=r['case'],round=r['round'],role=r['role'],experiment=r['experiment']) for r in official if not r['byte_equal']],all_8400_zero_exit=all(r['returncode']==0 for r in all_rows),all_8400_objects_equal=all(r['byte_equal'] for r in all_rows),warning_inclusive_C_summary=[r for r in base['summary'] if r['language']=='C'],load1=dict(min=min(loads),median=statistics.median(loads),max=max(loads)),boundary_frequency_kHz=dict(min=min(freq),median=statistics.median(freq),max=max(freq)),compiler_inodes_by_experiment={x:sorted(set(r['compiler_inode'] for r in official if r['experiment']==x)) for x in ['main-matrix','clean-c']},measurement_end=end['end'],timed_compile_seconds=sum(r['wall_s'] for r in official),total_timed_compile_seconds=sum(r['wall_s'] for r in all_rows),clean_c_nonempty_logs=([str(p.relative_to(E)) for p in (E/'clean-c/compile-logs').glob('*.txt') if p.stat().st_size] if (E/'clean-c/compile-logs').exists() else json.loads((E/'clean-c/compile-log-index.json').read_text())['nonempty']))
save(E/'summary.json',result)
for name,rs in [('per-file-medians.csv',medians),('hq-summary.csv',summary),('warning-inclusive-c-summary.csv',result['warning_inclusive_C_summary'])]:
    with (E/name).open('w') as f:w=csv.DictWriter(f,fieldnames=list(rs[0]),lineterminator='\n');w.writeheader();w.writerows(rs)
print(json.dumps(result,indent=2))
