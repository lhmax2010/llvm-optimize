"""Render final evidence-backed results after both retained RPM inventories exist."""
import json, sys
from pathlib import Path

D = Path(__file__).resolve().parent
B = Path('/home/linhao/Toolchain/development/llvm-optimize-bolt')
pin = sys.argv[1]
G = 1024 ** 3
measure = json.loads((D / 'measurement-comparison.json').read_text())
rpms = json.loads((D / 'rpm-comparison.json').read_text())
binary = [r for r in rpms if not r['rpm'].endswith('.src.rpm.json')]
source = [r for r in rpms if r['rpm'].endswith('.src.rpm.json')]
assert len(binary) == 22 and len(source) == 1
equal = all(r['payload_equal_except_mtime'] for r in binary)
ar_analysis = json.loads((D / 'rpm-difference-analysis/archive-differences.json').read_text())
assert all(r['equal_after_only_ar_timestamp_normalization'] for r in ar_analysis)
assert {(r['rpm'], r['path']) for r in ar_analysis} == {(r['rpm'].removesuffix('.json'), c['path']) for r in binary for c in r['changes']}
assert all(set(c['changes']) == {'sha256'} for r in binary for c in r['changes'])
new = json.loads((D / 'revised-run/completed-revised-summary.json').read_text())
old = json.loads((D / 'baseline-resume2/completed-baseline-summary.json').read_text())
identity = json.loads((D / 'rpm-validation/binary-identities.json').read_text())
assert identity['baseline'] == identity['revised']
candidate = identity['revised']['clang.candidate']
rawbase = 'https://raw.githubusercontent.com/lhmax2010/llvm-optimize/' + pin + '/tools/bolt/results/cache-release-20261022/'
def link(name, path):
    return '[' + name + '](' + rawbase + path + ')'

phase_names = {
    'ordinary-build': '普通构建（首轮为最后续跑段）',
    'ordinary-install': '普通安装',
    'bolt-through-compare-root': 'BOLT开始至compare-root',
    'static-conversion-and-install': 'compare-root后至find-debuginfo（含转换/安装）',
    'platform-post': '平台后处理至post报告',
    'packaging': 'RPM文件处理/打包',
}
text = '''\n## 13. 双轮最终结果（2026-10-23）\n\n'''
text += f'''两轮完整构建均成功，第二轮GBS退出0，耗时{new['result']['seconds']:.3f}秒；22个二进制RPM和1个源码RPM均已保全。首轮最终续跑段{old['result']['seconds']:.3f}秒仅代表该续跑段，不能与第二轮从零GBS总耗时直接比较。没有向Gerrit推送，也没有操作QB。\n\n'''
text += '''### 13.1 磁盘结论与口径\n\nBOLT四个固定报告时点的自有占用，首轮为0 / 3.762 / 4.345 / 4.346GiB；第二轮为0 / 3.762 / 4.345 / 3.226GiB。第二轮post数值较低，是正缓存增量随整个缓存删除后归零，并不代表工具或候选被额外清理。未运行BOLT-OFF第三轮，因此这些数值是BOLT自有路径与缓存正增量的实测，不能当作ON/OFF完整构建的因果峰值差。\n\n'''
text += f'''BOLT开始后、compare-root之前的整根瞬时增量观测值为首轮{measure['bolt_transient_root_growth_bytes']['baseline']/G:.3f}GiB、第二轮{measure['bolt_transient_root_growth_bytes']['revised']/G:.3f}GiB。它与固定报告时点不同，受采样对齐影响；不把分别采样的父子目录峰值相加。\n\n'''
text += f'''整轮完整chroot观测峰值 **{measure['baseline']['peak']['bytes']/G:.3f} → {measure['revised']['peak']['bytes']/G:.3f}GiB**，实测差 **{measure['sampled_peak_reduction_bytes']/G:.3f}GiB**。首轮峰值在静态库转换产物安装阶段，第二轮峰值提前到缓存释放之前的BOLT pipeline。首轮另有{measure['baseline_only_linker_residue_allocated_bytes']/G:.3f}GiB中断链接残留；扣除这个已知因素后的峰值改善**估算**为{measure['estimated_peak_reduction_excluding_known_residue_bytes']/G:.3f}GiB。不是第三轮受控实测，仍有续跑历史和采样差异。\n\n'''
text += f'''真实cache-release删除{new['cache_release']['files']:,}个文件、{new['cache_release']['allocated_bytes']:,}B（{new['cache_release']['allocated_bytes']/G:.3f}GiB），耗时{new['cache_release']['seconds']:.3f}秒。因此不能说“整轮峰值下降91GiB”：释放前的高占用仍然发生，主要收益在随后的转换、后处理和打包。\n\n'''
text += '| 阶段完整扫描的最高读数 | 首轮GiB | 第二轮GiB | 首轮减第二轮GiB |\n|---|---:|---:|---:|\n'
for key, name in phase_names.items():
    a = measure['baseline']['phases'][key]['peak']['bytes'] / G
    b = measure['revised']['phases'][key]['peak']['bytes'] / G
    text += f'| {name} | {a:.3f} | {b:.3f} | {a-b:.3f} |\n'
text += f'''\n上表只纳入扫描起止均在对应阶段内的完整读数，跨阶段扫描不强行归类。平台后处理阶段观测最高值下降{measure['phase_peak_reduction_bytes']['platform-post']/G:.3f}GiB；post报告之后的首个完整根读数为{measure['baseline']['post_after_sample']['bytes']/G:.3f} → {measure['revised']['post_after_sample']['bytes']/G:.3f}GiB，下降{measure['post_end_sample_reduction_bytes']/G:.3f}GiB。扣除已知首轮残留后，post结束时降幅**估算**{measure['estimated_post_end_reduction_excluding_known_residue_bytes']/G:.3f}GiB，与实际缓存释放量接近。各采样时刻和扫描时长保留，不用全盘df差替代本构建根占用。\n\n'''
text += '四次报告的原始字节数：\n\n| 阶段 | 首轮BOLT自有B | 第二轮BOLT自有B | 第二轮cache正增量B |\n|---|---:|---:|---:|\n'
for stage in ('begin', 'tool-built', 'pipeline', 'post'):
    a = measure['baseline']['reports'][stage]
    b = measure['revised']['reports'][stage]
    text += f"| {stage} | {a['used_bytes']:,} | {b['used_bytes']:,} | {b['cache_delta_allocated_bytes']:,} |\n"
text += '\n### 13.2 产物与门禁\n\n'
text += f'''完整RPM字节一致性不成立：时间元数据差异保留并按用户要求逐项归因，未放宽helper的任何产品门禁。两轮ordinary-clang-22、重链输入、llvm-bolt、BOLT输出、strip-all候选SHA一致；候选为 `{candidate}`，也与历史4ec07159一致。两轮均在各自新树构建llvm-bolt，非历史工具后备。工具计划与执行113/113、TF归档前后身份、匹配双门禁、安全属性、pipeline tiny、compare-root、原子安装和post tiny/SHA/别名全部PASS。\n\n225个Source1005转换归档的输入/输出SHA、大小、成员和转换统计全部相同，第二轮225个安装完成并最终PASS；缓存删除后未重建。平台后处理原样执行一次，post尾检最后通过。\n\n'''
text += '22个二进制RPM的文件清单、类型/模式、uid/gid、大小、链接目标和nlink逐包相同；mtime单列。部分静态归档完整SHA不同，下表如实列出；这些归档逐成员比较仅ar头时间字段不同，归档成员内容和其余字节均相同。没有改写保全的RPM或其载荷来抹平差异。RPM容器本身并非字节相同，构建时间等头字段和文件mtime另有原文记录。\n\n'
text += '| 二进制RPM | 载荷条目数 | 内容/类型/权限/链接比对 | mtime变化条目数 |\n|---|---:|---|---:|\n'
for row in binary:
    text += f"| {row['rpm'].removesuffix('.json')} | {row['file_count_after']} | {'完整SHA相同' if row['payload_equal_except_mtime'] else str(len(row['changes']))+'个ar时间头差异'} | {len(row['mtime_changes'])} |\n"
text += f'\n共有{len(ar_analysis)}个归档完整SHA不同；逐成员原始差异及仅归一ar头时间戳后的SHA见archive-differences.json。两轮平台脚本都调用brp-strip-static-archive /bin/strip，脚本原文执行strip -g。归档时间字段分别落在04:54:59–04:55:24与09:16:02–09:16:36（CST），与各自后处理时刻对应；判断为平台归档时间元数据差异，不是cache-release改变成员代码。\n\n'
text += '\n源码RPM按预期与二进制载荷分开：\n\n| 变化路径 | 变化字段 |\n|---|---|\n'
for c in source[0]['changes']:
    fields = ', '.join(sorted(c.get('changes', {}))) or 'added/deleted'
    text += f"| {c['path']} | {fields} |\n"
text += '\n源码包仅helper和spec两个文件的内容/大小不同。helper与各自源码完全匹配；导出spec的差异精确为三行cache-release改动及GBS自动生成的VCS提交号。源码tar、profile、Source1005、七个补丁及其他源码载荷均相同（文件mtime另列）。具体SHA见source-differences.json，不把源码包预期更新称作二进制包回归。\n\n'
text += '''源码仍为d20e873b2c7dfac10fab9235e2b781dad08dc4c7，父67619ec8bbbac7238a6cfc33a481ccfbcd12206f，作者/提交者/Signed-off-by均Hao Lin。spec SHA为64bff4b4f6a9587a28ba2b2663ce05b61a4c391bb59d9120beb2845cce488f1f，helper SHA为516bf4189415bed604eac2e74049ab2b148690c79b3fea4e420e3617527630f5。299测试与gbs export后的五项Tizen RPM解析认证沿用同一未改源码提交的已通过结果；构建期间没有再改生产文件。\n\n'''
text += '### 13.3 资源、采样限制和保留状态\n\n'
text += f'''第二轮cgroup峰值{new['memory_peak_bytes']:,}B，最大观察到单进程VmHWM为{new['max_observed_process']['VmHWM_KiB']:,}KiB（ld.lld）；oom/oom_kill均0。首轮cgroup峰值{old['memory_peak_bytes']:,}B、最大观察VmHWM {old['largest_observed_process_VmHWM']['VmHWM_KiB']:,}KiB，且有16→20GiB→无上限与中断续跑历史，耗时不能作纯优化因果比较。第二轮每段持锁秒数为{', '.join(f'{x:.3f}' for x in new['leases_seconds'])}，均小于3600秒，冻结仅为释放/重新取得共享锁，不做内存准入或低内存等待。\n\n'''
text += f'''第二轮完整根du有{new['du']['complete_samples']}个成功样本、{new['du']['incomplete_samples']}个临时文件竞态不完整样本，最长扫描{new['du']['longest_scan_seconds']:.3f}秒。每60秒为调度目标，I/O等待期间未能保持60秒完成一次；没有补造缺失读数。首轮早期空档和后处理长扫描见第9、10节。整轮峰值均为观测值而非连续上界。\n\n'''
text += '''两轮23个RPM、candidate、ordinary、llvm-bolt、identity和四份报告均保全并逐文件SHA核对；第二轮保全28,010文件、11,963,443,118B。只删除过用户授权的本次首轮新根cache以腾第二轮空间，第二轮cache由产品新增命令在compare-root后删除；历史树未动。第二轮挂载已清理，所有第二轮构建/监视服务inactive。首轮proc仍被VS Code PID4237的FD48/49持有，保留挂载与其余首轮树，未强制卸载、未终止编辑器；相关原文另存。只读证据查找和显示修正见monitor-corrections.json；源码RPM归因脚本首次遗漏GBS生成VCS行，补上该项后仅剩预期差异，未更换产品输入或修改产物。\n\n'''
text += '### 13.4 钉提交原始证据\n\n'
items = [
    ('双轮测量比较与公式', 'measurement-comparison.json'),
    ('第二轮完整结果与资源', 'revised-run/completed-revised-summary.json'),
    ('两轮候选/ordinary/工具SHA', 'rpm-validation/binary-identities.json'),
    ('逐包逐路径RPM差异', 'rpm-comparison.json'),
    ('归档成员与时间头差异', 'rpm-difference-analysis/archive-differences.json'),
    ('源码RPM差异归因', 'rpm-difference-analysis/source-differences.json'),
    ('RPM比较完整结果', 'rpm-validation/product-comparison-summary.json'),
    ('首轮RPM头字段', 'rpm-validation/baseline-rpm-headers.json'),
    ('第二轮RPM头字段', 'rpm-validation/revised-rpm-headers.json'),
    ('225归档转换比较', 'revised-run/archive-conversion-comparison.json'),
    ('真实缓存释放', 'revised-evidence/bolt-work/cache-release.json'),
    ('post尾检', 'revised-evidence/bolt-work/post-gate/post-result.json'),
    ('带行号时间线', 'timeline-final.tsv'),
    ('第二轮完整日志', 'revised-run/rpm-build.log.gz'),
    ('第二轮完整根du', 'revised-run/du-root-complete.jsonl'),
    ('证据SHA索引', 'build-evidence-provenance.json'),
]
text += '\n'.join('- ' + link(name, path) for name, path in items) + '\n'

p = B / 'docs/bolt/32_cache_release.md'
prior = p.read_text().split('\n## 13. ')[0]
lines = prior.splitlines()
lines[2] = '**最终状态：两轮完整构建、299测试、五项Tizen RPM解析、全部BOLT实物门禁PASS；候选不变，22个二进制RPM清单一致；部分ar头时间戳不同，成员内容一致，未宣称RPM逐字节相同。源码提交仅保留在本地，未推Gerrit。最终结论见第13节。**'
prior = '\n'.join(lines) + '\n'
prior = prior.replace('## 6. 双轮结果：资源停止，不能宣称完整认证', '## 6. 2026-10-22停止快照（后续已完成，见第13节）')
prior = prior.replace('## 7. 继续工作的条件与边界', '## 7. 当时继续工作的条件与边界')
prior = prior.replace('## 8. 原始证据', '## 8. 首次停止时的原始证据')
prior = prior.replace('## 9. 2026-10-23 内存释放后的续跑（进行中）', '## 9. 2026-10-23 内存释放后的续跑历史')
p.write_text(prior + text)
print('Rendered final section with evidence pin', pin)
