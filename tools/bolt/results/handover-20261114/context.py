from inventory import *
def sha(p):
 with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
snap=json.load(open(E/'workspaces.json'))
local={}
for label,root in [('W',W),('B',B)]:
 records=[]
 for line in snap[label]['status']['stdout'].splitlines():
  path=line[3:]
  # git may quote unusual file names; preserve raw when not directly resolvable.
  p=root/path
  item={'git_status':line[:2],'path':str(p),'status_snapshot':snap[label]['status']['time']}
  try:
   item.update(exists=p.exists(),bytes=p.stat().st_size if p.is_file() else None,symlink=p.is_symlink())
   if p.is_file() and p.stat().st_size<1024**2:item['sha256']=sha(p)
   if p.is_file() and Path(str(p)+'.gz').exists():item['compressed_sibling']=str(p)+'.gz';item['contents_vs_sibling']='NOT COMPARED'
  except OSError as ex:item['error']=str(ex)
  records.append(item)
 local[label]=records
write('local-only-files.json',local)
config=git(W,'diff','--','gbs_llvm.conf');write('W-gbs-config-local-diff.json',config)
copies=[]
for rel in ['run-night.sh','test_serial.py','basedev/launcher.py','README.md','SHA256SUMS']:
 w=W/'tools/bolt/rebase-launch-20261111-r6'/rel;b=B/'tools/bolt/rebase-launch-20261111-r6'/rel
 rec={'relative':rel,'W':str(w),'B':str(b),'exists_W':w.exists(),'exists_B':b.exists()}
 if w.is_file() and b.is_file():rec.update(W_sha256=sha(w),B_sha256=sha(b),equal=w.read_bytes()==b.read_bytes())
 copies.append(rec)
write('entry-copy-drift.json',copies)
# Inventory candidate off-repository plans by name, without scanning all old repositories again.
candidates=[]
for parent in [W/'temp/pgo-bolt-followup-20261105',W/'temp/pgo-profiles-keep-20261102',W/'tools/bolt',B/'tools/bolt',B/'docs/bolt']:
 if not parent.exists():continue
 for p in parent.iterdir():
  if re.search(r'pgo|paired|profile|harden|乙一|hardening',p.name,re.I):
   candidates.append({'path':str(p),'type':'directory' if p.is_dir() else 'file','status':'candidate name only; experiments are not proof of product implementation'})
write('pgo-hardening-candidates.json',{'candidates':candidates,'scope':'top-level selected evidence/tools directories plus full W/B git porcelain; no repeat of OOM historical repository audit','conclusion':'No separately identified unpublished乙一/product-hardening implementation in successfully audited active worktrees; completeness UNKNOWN for OOM old-repository scan'})
# Read existing data for future-resource references, no rerun.
resources=json.load(open(B/'tools/bolt/results/night-82-84-20261113/84/all-results.json'))
write('resource-reference.json',[{'source_id':d['id'],'commit':d['commit'],'snapshot':d['snapshot'],'memory':d['memory'],'disk':d['disk']} for d in resources if d['environment']=='local'])
print('local files W/B',len(local['W']),len(local['B']))
print('ENTRY DRIFT',[(r['relative'],r.get('equal')) for r in copies])
p=json.load(open(E/'long-process-summary.json'))
print('LONG PROCESSES',[(r['pid'],r['comm'],r['elapsed_seconds']) for r in p['processes']])
query=run(['git','ls-remote','https://github.com/lhmax2010/llvm-optimize.git','refs/heads/main','refs/heads/bolt-v4'])
write('evidence-ls-remote-before.json',query);print(query['stdout'].strip())
write('context-only-instructions.json',[
 {'source':'本轮用户明确回复','date':'2026-11-14','instruction':'允许仅终止本次超时 du','scope':'仅85盘点新启动的超时du；不授权其他进程信号'},
 {'source':'当前对话历次任务；时间以文档/原始消息为准','instruction':'清理、完整构建、sandbox和refs/for授权均有任务范围；不得把历史一次授权当成85或第二批的授权','already_documented':'部分历史任务和STATUS中；85集中说明'},
 {'source':'当前对话用户要求','instruction':'PM只能读取GitHub bolt-v4；本地路径不是可交付证据，必须提供发布JSON/原文链接；本地大型产物只能登记路径/大小/身份，后续试验依赖该机器','already_documented':'本轮交接新增汇总'},
 {'source':'历次用户约束','instruction':'shell用POSIX sh；平台工具由对应构建根loader运行；原始失败不覆盖；需要登录/密码按当次任务规则停止或窗口登录，凭据不经终端','already_documented':'多个历史任务中散见，不是新的产品裁决'},
 {'source':'上下文审计结论','instruction':'没有可确认的、应覆盖v9而尚未写入证据的额外产品裁决；未核查其他会话或用户私有笔记，不能声称不存在','already_documented':'85记录可知范围'}])
print('已结束',datetime.datetime.now().astimezone().isoformat(),'step3 context inventory PARTIAL (historical repository blind spot retained)')
