"""Data checks for a read-only report, not an LLVM/product test."""
from pathlib import Path
import json,os,hashlib,datetime
D=Path(__file__).resolve().parent
rows=json.loads((D/'inventory.json').read_text());units=json.loads((D/'du-units.json').read_text());extra=json.loads((D/'du-additional.json').read_text());scenario=json.loads((D/'reclaim-scenario.json').read_text())
checks={}
checks['all_local_filesystems_scanned']=all((D/f'du-filesystem-{i}.json').exists() and json.loads((D/f'du-filesystem-{i}.json').read_text())['returncode'] in (0,1) for i in range(3))
checks['independent_candidates_complete']=len(units)==85 and len(extra)==3 and all('bytes' in r for r in units+extra)
checks['only_over_5_GiB_in_table']=all(r['bytes']>5*2**30 for r in rows)
checks['unique_paths']=len(rows)==len({r['path'] for r in rows})
checks['filesystem_mapping']=all(r['device_number']==os.stat(r['mountpoint']).st_dev for r in rows)
lookup={r['path']:r for r in rows}
checks['scenario_matches_independent_du']=all(lookup[r['path']]['bytes']==r['allocated_bytes'] for r in scenario['roots'])
checks['no_external_hardlinks_or_read_errors_in_four_roots']=not scenario['external_hardlink_inodes'] and not scenario['errors']
checks['reclaim_arithmetic']=sum(r['allocated_bytes'] for r in scenario['roots'])-scenario['preserve_copy_reservation']==scenario['net_reclaim_scenario']
checks['preservation_14_sha256']=len(scenario['preserve_files'])==14 and all(len(r['sha256'])==64 for r in scenario['preserve_files'])
hard=json.loads((D/'rpm-hardlinks.json').read_text())['files'];checks['22_RPM_hardlinks']=len(hard)==22 and all(r['same_inode'] for r in hard)
assets=json.loads((D/'preserve-assets.json').read_text())+json.loads((D/'additional-assets.json').read_text());checks['17_asset_hashes']=len(assets)==17 and all('sha256' in r and 'error' not in r for r in assets)
checks['citation_paths_and_lines']=not json.loads((D/'report-validation.json').read_text())['citation_errors']
result={'time':datetime.datetime.now().astimezone().isoformat(),'checks':checks,'all_pass':all(checks.values()),'rows':len(rows),'bytes_planned_net_reclaim':scenario['net_reclaim_scenario'],'limitation':'Permission blind spots are reported, not considered empty. No deletion performed.'}
(D/'final-validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False,indent=2))
raise SystemExit(0 if result['all_pass'] else 1)
