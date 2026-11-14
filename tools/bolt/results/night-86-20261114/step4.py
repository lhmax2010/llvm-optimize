import pathlib,json,gzip,re,hashlib,datetime,collections
E=pathlib.Path(__file__).resolve().parent;B=E.parents[3];R=B/'tools/bolt/results/pgo-resource-full-20261104';A=R/'full/stage-A'
read=lambda p:json.loads(p.read_text())
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for c in iter(lambda:f.read(1048576),b''):h.update(c)
 return h.hexdigest()
ident=read(R/'script-identities.json');script_proofs=[]
for n in ['driver.py','train.py','common.py']:
 p=B/'tools/bolt/pgo-resource-20261102'/n
 script_proofs.append(dict(path=str(p),saved_sha256=ident[n],current_sha256=sha(p),match=sha(p)==ident[n]))
 assert sha(p)==ident[n],('historical-script-changed',n)
ls=(A/'evidence/A/stdout').read_text().splitlines();hits=[];groups=[];last=None
for i,l in enumerate(ls,1):
 if re.match(r'^\[\d+/\d+\]',l):last=dict(line=i,text=l)
 if 'Running out of static counters' in l:
  hits.append(dict(line=i,text=l))
  if groups and groups[-1]['end']==i-1:groups[-1]['end']=i;groups[-1]['count']+=1
  else:groups.append(dict(start=i,end=i,count=1,preceding_progress=last))
assert len(hits)==830
training=read(A/'training-commands.json');outputs=[]
for i,row in enumerate(training):
 base=A/'evidence/B'/(str(i)+'-'+row['name']+'.stdout')
 o=[]
 for p in [base,pathlib.Path(str(base)+'.stderr')]:
  lines=p.read_text().splitlines()
  o.append(dict(path=str(p),bytes=p.stat().st_size,sha256=sha(p),warning_matches=[dict(line=n,text=l) for n,l in enumerate(lines,1) if 'Running out of static counters' in l]))
 result=read(pathlib.Path(str(base)+'.result.json'))
 outputs.append(dict(index=i,name=row['name'],profile_pattern=row['LLVM_PROFILE_FILE'],logs=o,result=result))
assert len(outputs)==23 and not any(x['warning_matches'] for o in outputs for x in o['logs'])
cmd=read(A/'evidence/C/command.json');raws=[x for x in cmd if x.endswith('.profraw')]
inventory=read(R/'profile-final-inventory.json');recorded={d['path']:d for d in inventory if d['path'].endswith('.profraw')}
assert len(raws)==23 and set(raws)==set(recorded)
keep=pathlib.Path('/home/linhao/Toolchain/development/llvm-optimize/temp/pgo-profiles-keep-20261102')
verified=[]
for path in raws:
 p=keep/pathlib.Path(path).name;old=recorded[path];idx=int(p.name.split('-',1)[0]);assert 0<=idx<23
 pattern=training[idx]['LLVM_PROFILE_FILE'];pat=re.escape(pathlib.Path(pattern).name).replace('%m',r'\d+(?:_\d+)?').replace('%p',r'\d+')
 assert re.fullmatch(pat,p.name),(pat,p.name)
 h=sha(p);assert h==old['sha256'] and p.stat().st_size==old['bytes']
 verified.append(dict(original=path,current=str(p),bytes=p.stat().st_size,sha256=h,training_index=idx))
pd=read(A/'evidence/profdata.json');pp=keep/'clang.profdata';assert sha(pp)==pd['sha256'] and pp.stat().st_size==pd['bytes']
# Read preserved process maxima without attributing individual untagged warnings to a PID.
with gzip.open(A/'evidence/A/process-maxima.json.gz','rt') as f:processes=json.load(f)
def records(x):
 if isinstance(x,dict):
  if any(k in x for k in ['cmdline','command','argv']):yield x
  for v in x.values():yield from records(v)
 elif isinstance(x,list):
  for v in x:yield from records(v)
tools=[]
for x in records(processes):
 text=json.dumps(x)
 if 'tblgen' in text:tools.append(x)
# Only finite preserved evidence; no current process queries or executions.
(E/'counter-warning-groups.json').write_text(json.dumps(groups,indent=2)+'\n')
(E/'counter-warning-lines.json').write_text(json.dumps(hits,indent=2)+'\n')
(E/'A-tblgen-process-records.json').write_text(json.dumps(tools,indent=2)+'\n')
(E/'training-warning-audit.json').write_text(json.dumps(outputs,indent=2)+'\n')
(E/'merge-input-trace.json').write_text(json.dumps(dict(command=cmd,profiles=verified,profdata=pd,current_profdata=str(pp),scripts=script_proofs),indent=2)+'\n')
# Save historical script excerpts with numbered lines proving phase directory separation.
extract=[]
p=B/'tools/bolt/pgo-resource-20261102/driver.py';lines=p.read_text().splitlines()
for start,end in [(51,88)]:
 extract.append('\n'.join(f'{i}: {lines[i-1]}' for i in range(start,min(end,len(lines))+1)))
extract.append('train.py:\n'+(B/'tools/bolt/pgo-resource-20261102/train.py').read_text())
(E/'profile-path-separation.txt').write_text('\n\n'.join(extract))
res=dict(status='PASS_WITH_UNKNOWN',time=datetime.datetime.now().astimezone().isoformat(),A_warning_count=len(hits),A_warning_groups=len(groups),A_tblgen_sample_records=len(tools),B_training_count=len(outputs),B_warning_count=0,merge_inputs=len(raws),all_inputs_match_training_patterns_and_retained_SHA=True,profdata_bytes=pd['bytes'],profdata_sha256=pd['sha256'],warning_phase='已证明：A构建阶段，不是B训练',exact_warning_PID='UNKNOWN：警告无PID/命令标记；Ninja目标和采样tblgen命令支持构建生成工具归属，不能逐条锁定PID',A_profraw_in_merge='已证明：未进入本次显式23文件合并清单。B开始时profiles.mkdir()新建专用目录；A在env -i下未指定该LLVM_PROFILE_FILE；C清单全部对应B的0–22训练模式，留存SHA一致。A各进程的实际默认profraw路径/内容未保存，UNKNOWN。',training_warning='已证明：23条B训练stdout/stderr均无该警告；不等于证明未来负载不会耗尽')
(E/'step4-result.json').write_text(json.dumps(res,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(res,ensure_ascii=False,indent=2));print('86步骤4 已结束 '+res['time']+' status='+res['status'])
