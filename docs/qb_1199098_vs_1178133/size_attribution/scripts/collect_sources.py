"""Fetch exact-range source history/diffs; never check out or execute product source."""
from common import *
from urllib.parse import urlencode
REVISIONS={'llvm':('8dfebafe1a477b3dcc678ee4cb18a3a4306d5a7c','67619ec8bbbac7238a6cfc33a481ccfbcd12206f'),'qemu-accel':('e01aa7250a1a73aa8f88ba9ac4a05cbc954d1c9f','2737f3bf78ed33be4333114c0e5c741a1deca467')}
for repo,(old,new) in REVISIONS.items():
 base=f'https://git.tizen.org/cgit/platform/upstream/{repo}/'
 jobs=[('log/',{'id':new,'qt':'range','q':f'{old}..{new}','showmsg':1},f'{repo}_range_log.html'),('patch/',{'id':new,'id2':old},f'{repo}_range.patch'),('diff/',{'id':new,'id2':old},f'{repo}_full_diff.html'),('rawdiff/',{'id':new,'id2':old},f'{repo}_full.diff')]
 if repo=='llvm':jobs.append(('rawdiff/packaging/',{'id':new,'id2':old},'llvm_packaging.diff'))
 for path,query,name in jobs:
  try:fetch(base+path+'?'+urlencode(query),RAW/name)
  except Exception as e:
   with (RAW/'source_fetch_errors.jsonl').open('a') as f:f.write(json.dumps({'time':now(),'url':base+path+'?'+urlencode(query),'error':str(e)})+'\n')
