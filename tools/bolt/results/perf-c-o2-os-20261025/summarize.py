from pathlib import Path
import json,statistics,math,csv,collections,gzip,hashlib
E=Path(__file__).resolve().parent; B=E.parents[3]
def geo(values):return math.exp(statistics.mean(math.log(x) for x in values))
def save(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
done=json.loads((E/'finished.json').read_text());assert done['status']=='COMPLETE' and done['inputs_unchanged']
raw=(E/'samples.jsonl').read_bytes() if (E/'samples.jsonl').exists() else gzip.decompress((E/'samples.jsonl.gz').read_bytes())
samples=[json.loads(x) for x in raw.decode().splitlines()];assert len(samples)==6000
cases=json.loads((E/'cases.json').read_text());grouped=collections.defaultdict(list)
for s in samples:grouped[s['group'],s['case']].append(s)
medians=[]
for (group,index),ss in sorted(grouped.items()):
    u=cases[index];a=[s['wall_s'] for s in ss if s['role']=='ordinary'];b=[s['wall_s'] for s in ss if s['role']=='candidate'];assert len(a)==len(b)==5
    am=statistics.median(a);bm=statistics.median(b)
    medians.append(dict(group=group,case=index,language=u['language'],option=u['option'],target=u['target'],name=u['name'],cohort=u['cohort'],ordinary_median_s=am,candidate_median_s=bm,ratio=bm/am,saved_percent=(1-bm/am)*100,ordinary_samples=a,candidate_samples=b,all_objects_equal=all(s['byte_equal'] for s in ss),input_sha256=u['input_sha256']))
assert len(medians)==600
with (E/'per-file-medians.csv').open('w') as f:
    w=csv.DictWriter(f,fieldnames=list(medians[0]),lineterminator='\n');w.writeheader();w.writerows(medians)
summary=[]
for group in ['static','hybrid']:
    for lang,opts in [('C',['-O2','-Os']),('C++',['-O2','-Os','-O3'])]:
        for opt in opts:
            for target in ['x86_64-tizen-linux-gnu','armv7l-tizen-linux-gnueabi','aarch64-tizen-linux-gnu']:
                rows=[x for x in medians if (x['group'],x['language'],x['option'],x['target'])==(group,lang,opt,target)];assert len(rows)==20
                ratio=geo(x['ratio'] for x in rows)
                summary.append(dict(group=group,language=lang,option=opt,target=target,files=20,ratio=ratio,saved_percent=(1-ratio)*100,all_objects_equal=all(x['all_objects_equal'] for x in rows),ordinary_median_range=[min(x['ordinary_median_s'] for x in rows),max(x['ordinary_median_s'] for x in rows)]))
old=json.loads((E.parent/'validation-performance.json').read_text());old_by_name=collections.defaultdict(list)
for r in old['rows']:old_by_name[r['key'].split('/')[1].split('-',1)[1]].append(r)
old_unique=[]
for name,rs in old_by_name.items():
    a=[v for r in rs for v in r['ordinary_s']];b=[v for r in rs for v in r['candidate_s']];old_unique.append(statistics.median(b)/statistics.median(a))
o3=[]
for group in ['static','hybrid']:
    for target in ['x86_64-tizen-linux-gnu','armv7l-tizen-linux-gnueabi','aarch64-tizen-linux-gnu']:
        rows=[x for x in medians if (x['group'],x['language'],x['option'],x['target'])==(group,'C++','-O3',target)]
        o3.append(dict(group=group,target=target,unique20_ratio=geo(x['ratio'] for x in rows),historical30_weight_ratio=geo([x['ratio'] for x in rows for _ in range(1 if x['cohort']=='arm-holdout' else 2)]),holdout10_ratio=geo(x['ratio'] for x in rows if x['cohort']=='arm-holdout')))
loads=[float(s[k]['loadavg'].split()[0]) for s in samples for k in ['before','after']]
freq=[int(s[k]['frequency_kHz']) for s in samples for k in ['before','after'] if s[k]['frequency_kHz'].isdigit()]
result=dict(status='COMPLETE',compiles=6000,comparison_outputs=5400,unequal_outputs=[dict(group=s['group'],case=s['case'],round=s['round'],role=s['role'],object_sha256=s['object_sha256']) for s in samples if not s['byte_equal']],summary=summary,o3=o3,old_x86_30_ratio=old['geometric_mean_ratio'],old_x86_unique20_ratio=geo(old_unique),load1=dict(min=min(loads),median=statistics.median(loads),max=max(loads)),boundary_frequency_kHz=dict(min=min(freq),median=statistics.median(freq),max=max(freq)),timed_compile_seconds=sum(s['wall_s'] for s in samples),compiler_inodes=sorted(set(s['compiler_inode'] for s in samples)),raw_samples_sha256=hashlib.sha256(raw).hexdigest())
save(E/'summary.json',result)
with (E/'hq-summary.csv').open('w') as f:
    w=csv.DictWriter(f,fieldnames=list(summary[0]),lineterminator='\n');w.writeheader();w.writerows(summary)
print(json.dumps(result,indent=2))
