"""Additional raw aggregates and non-exclusive rule memberships, derived from saved evidence."""
from common import *
import csv,collections,re

def read(n):return list(csv.DictReader((OUT/n).open()))
def save(n,rows):
 fields=list(dict.fromkeys(k for r in rows for k in r))
 with (OUT/n).open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
facts=[]
def fact(x):
 facts.append(x);return f'raw/coverage_facts.jsonl:{len(facts)}'
f=read('files_compare.csv');cats=read('category_summary.csv');summ=read('package_summary.csv');acc=read('clang_accel_sources.csv');detail=read('elf_detail.csv');meta=read('rpm_metadata.csv')
members=[]
for s in summ:
 rows=[r for r in f if (r['arch'],r['package'])==(s['arch'],s['package'])]
 for cat in ['新增文件','删除文件','qemu-accel 打包变化','链接方式变化','strip/调试信息变化','代码节变大']:
  matching=[r for r in rows if cat in r['categories_all'].split(';')];d=sum(int(r['delta_bytes']) for r in matching);total=int(s['path_delta_bytes'])
  r={'arch':s['arch'],'package':s['package'],'category':cat,'matching_paths':len(matching),'net_delta_bytes':d,'package_path_delta_bytes':total,'share_percent':format(100*d/total,'.8f') if total else '不适用','overlap_warning':'非互斥，不能跨类别相加','file_evidence':';'.join(r['old_evidence']+';'+r['new_evidence'] for r in matching)}
  r['derived_evidence']=fact(dict(kind='nonexclusive_category',**r));members.append(r)
save('category_membership.csv',members)
for side in ['old','new']:
 rows=[r for r in acc if r['side']==side];regular=[r for r in rows if r['type']=='regular'];matched=[r for r in regular if r['match_status']=='原样来自'];unmatched=[r for r in regular if r['match_status']=='无匹配']
 fact({'kind':'clang_accel_matches','side':side,'regular_files':len(regular),'matched_regular_files':len(matched),'matched_bytes':sum(int(r['size']) for r in matched),'unmatched_regular_files':len(unmatched),'unmatched_bytes':sum(int(r['size']) for r in unmatched),'matched_paths':[r['path'] for r in matched],'inventory':f'raw/{side}_armv7l_clang-accel-x86_64-armv7l_files.jsonl:1'})
for pkg in ['clang','llvm']:
 rows=[r for r in detail if r['package']==pkg]
 fact({'kind':'elf_selection','package':pkg,'selected_paths':len(set(r['path'] for r in rows)),'old_new_observations':len(rows),'has_symtab_count':sum(r['has_symtab']=='True' for r in rows),'has_debug_sections_count':sum(r['has_debug_sections']=='True' for r in rows),'missing_build_id_count':sum(r['build_id'].startswith('未获取') for r in rows),'raw_evidence':[r['readelf_evidence'] for r in rows]})
fact({'kind':'compression','observations':len(meta),'compressor_flags_counts':dict(collections.Counter(r['payloadcompressor']+'/'+r['payloadflags'] for r in meta)),'evidence':[r['header_evidence'] for r in meta]})
# Export all ELF records for auditing category decisions beyond top 30.
from analyze_sizes import inv,els
allrows=[]
for (side,arch,pkg,path),e in sorted(els.items()):
 r=inv[(side,arch,pkg)][path]
 allrows.append({'side':side,'arch':arch,'package':pkg,'path':path,'size':r['size'],'needed':';'.join(e['needed']),'has_symtab':e['symtab'],'debug_sections_json':json.dumps(e['debug'],sort_keys=True),'sections_json':json.dumps(e['sections'],sort_keys=True),'build_id':e['build_id'],'inventory_evidence':r['evidence'],'readelf_evidence':e['readelf_evidence']})
save('elf_all.csv',allrows)
fact({'kind':'all_elf','observations':len(allrows),'symtab_count':sum(r['has_symtab'] for r in allrows),'debug_sections_count':sum(r['debug_sections_json']!='{}' for r in allrows)})
with (RAW/'coverage_facts.jsonl').open('w') as out:
 for r in facts:out.write(json.dumps(r,ensure_ascii=False)+'\n')
print('coverage facts',len(facts))
