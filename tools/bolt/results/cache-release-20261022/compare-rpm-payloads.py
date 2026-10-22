import json,sys
from pathlib import Path
A=Path(sys.argv[1]);B=Path(sys.argv[2]);out=Path(sys.argv[3]);rows=[]
a={x.name:x for x in A.glob('*.json')};b={x.name:x for x in B.glob('*.json')}
for name in sorted(set(a)|set(b)):
 if name not in a or name not in b:
  rows.append({'rpm':name,'missing_from':'baseline' if name not in a else 'revised'});continue
 old={x['path']:x for x in json.loads(a[name].read_text())};new={x['path']:x for x in json.loads(b[name].read_text())}
 changes=[];times=[]
 for path in sorted(set(old)|set(new)):
  if path not in old or path not in new:changes.append({'path':path,'before':old.get(path),'after':new.get(path)});continue
  delta={k:{'before':old[path].get(k),'after':new[path].get(k)} for k in set(old[path])|set(new[path]) if old[path].get(k)!=new[path].get(k)}
  if 'mtime' in delta:times.append({'path':path,**delta.pop('mtime')})
  if delta:changes.append({'path':path,'changes':delta})
 rows.append({'rpm':name,'file_count_before':len(old),'file_count_after':len(new),'payload_equal_except_mtime':not changes,'changes':changes,'mtime_changes':times})
out.write_text(json.dumps(rows,indent=2)+'\n')
print(json.dumps({'rpm_count':len(rows),'equal_except_mtime':sum(x.get('payload_equal_except_mtime',False) for x in rows),'not_equal':[x['rpm'] for x in rows if not x.get('payload_equal_except_mtime',False)]},indent=2))
