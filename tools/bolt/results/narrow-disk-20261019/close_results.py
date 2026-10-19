from pathlib import Path
import json,subprocess,shutil,hashlib
E=Path(__file__).resolve().parent;W=E.parents[1];B=W.parent/'llvm-optimize-bolt';S=W/'temp/bolt-v4-20261013/v41/llvm-source';D=B/'tools/bolt/results/narrow-disk-20261019';push=json.loads((E/'push-result.json').read_text());assert push['PASS'];new=push['after'];pin=json.loads((E/'material-verification.json').read_text())['pin']
for pattern in ['push*','material-verification.json','verify_materials.py']:
 for p in E.glob(pattern):
  if p.is_file():shutil.copyfile(p,D/p.name)
p=D/'validation-summary.json';summary=json.loads(p.read_text());summary.update(sandbox_pushed=True,remote_before=push['before'],remote_after=new,material_pin=pin,raw_URLs_verified_before_push=304);p.write_text(json.dumps(summary,indent=2)+'\n')
p=B/'patches/bolt/draft-manifest.json';m=json.loads(p.read_text());m.update(qualification='NARROW_BOLT_SCOPE_ALL_CERTIFICATION_AND_SANDBOX_PUSH_PASS',sandbox_pushed=True,remote_before=push['before'],remote_after=new,remote_before_raw=(E/'push-before.stdout').read_text(),remote_after_raw=(E/'push-after.stdout').read_text(),sandbox_result='tools/bolt/results/narrow-disk-20261019/push-result.json',material_pin=pin,GitHub_raw_URLs_verified_before_sandbox=304,publication_order='Narrowed source 289 tests, byte comparisons, sh-e and five Tizen parses PASS; GitHub materials '+pin+' published and 304 raw URLs verified; exact-lease sandbox update and post-query PASS')
m['narrow_disk_revision']=summary;m['disk_diagnostics']=summary;p.write_text(json.dumps(m,indent=2)+'\n')
p=B/'docs/bolt/STATUS.md';s=p.read_text().replace('收窄磁盘诊断范围（认证PASS，待推）','收窄磁盘诊断范围（认证及推送PASS）');s=s.replace('材料先GitHub，随后按e246精确租约更新唯一bolt_pgo；推送结果另记收尾。','材料de32b57先GitHub，304raw核验PASS后以e246精确租约更新唯一bolt_pgo，推后已等于该源SHA；无refs/for、QB或新分支操作。');p.write_text(s)
p=B/'docs/bolt/27_disk_diagnostics.md';s=p.read_text();s+=f'''\n\n### 收窄修订推送结果\n\n第一至第三步全PASS后，以BASE e2463165的完整SHA作为唯一分支租约推送，远端从 `{push['before']}` 更新为 `{new}`，推后查询一致，rc0。没有refs/for、tizen_base、QB或新分支操作；e971未推。材料先发布于 `{pin}`，304个raw URL在推送前字节/SHA核验PASS。完整argv、stdout/stderr与两次查询见push-result.json、push-before/after.stdout，Gerrit原文如下：\n\n```text\n'''+push['stdout']+push['stderr']+f'''```\n\n供后续使用的软件包标识：`platform/upstream/llvm@{new}`。这里仅记录分支更新，未启动QB。收窄修订的SHA、范围、289测试与五项解析认证取代本页前半未采用e971的结论；前半作为历史证据保留。\n''';p.write_text(s)
# Closing identities and cleanup state, read only.
assert subprocess.check_output(['git','status','--porcelain'],cwd=S)==b''
helper=(S/'packaging/clang-bolt-helper.py').read_bytes();assert helper==(B/'tools/bolt/bolt_helper.py').read_bytes()
project=W/'temp/gbs-root-x86_64-archivefix-v2/.llvm-optimize-exclusive.lock'
check={'source_commit':new,'source_parent':subprocess.check_output(['git','rev-parse','HEAD^'],cwd=S,text=True).strip(),'source_clean':True,'helper_mirror_equal':True,'helper_sha256':hashlib.sha256(helper).hexdigest(),'spec_sha256':hashlib.sha256((S/'packaging/llvm.spec').read_bytes()).hexdigest(),'project_lock_exists_after':project.exists(),'own_overlay_in_final_mountinfo':str(E/'merged-rpm') in (E/'mountinfo-after.txt').read_text(),'graphical_prompts':1,'original_cmake_ninja_executed':False,'tizen_five_parse_pass':True,'sandbox_after':new,'material_pin':pin,'Gerrit_warning_lines':[l for l in push['stderr'].splitlines() if 'warning' in l.lower()]}
assert not check['project_lock_exists_after'] and not check['own_overlay_in_final_mountinfo'];(D/'closing-check.json').write_text(json.dumps(check,indent=2)+'\n')
print('closed:',new,'STATUS bytes',Path(B/'docs/bolt/STATUS.md').stat().st_size)
