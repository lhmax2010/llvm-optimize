from common import *
import re,json
for bid,child in [(1216409,1216412),(1216410,1216413)]:
 lines=(D/f'{bid}-x86_64.log').read_text().splitlines();extra=[]
 for i,l in enumerate(lines,1):
  s=re.sub(r'^\[\s*\d+s\]\s?','',l)
  if s.startswith('{'):
   try:j=json.loads(s)
   except ValueError:continue
   if any(k in j for k in ['planned_tasks','plan_type','preflight_pass','bolt_task_count','BOLT_STRIP_IDENTITY','post_gate_pass','paths_checked','cmake_files_checked']):
    save(f'{bid}/record-L{i}.json',json.dumps(j,indent=2)+'\n');extra.append(f'L{i}: {l}')
  if any(k in l for k in ['NATIVE_ARCHIVES_BEGIN','find-debuginfo.sh','--debug-info ','--debug-symbols','/usr/lib/debug','/usr/src/debug']) and len(l)<2500:extra.append(f'L{i}: {l}')
 save(f'{bid}/additional-anchors.txt','\n'.join(extra)+'\n')
 cl=(D/f'{child}-full-log.txt').read_text().splitlines();matches=[]
 for i,l in enumerate(cl,1):
  if any(x in l for x in ['base_path_url:','repodata_url inside get_build_conf_text','snapshot_num_url:']) or ('pkg: llvm, spec_name: llvm,' in l):matches.append(f'L{i}: {l}')
 save(f'{child}/source-and-status-excerpts.txt','\n'.join(matches)+'\n')
