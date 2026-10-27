"""Summarize completed local measurements; never builds or pushes."""
from pathlib import Path
import json

D = Path(__file__).resolve().parent
B = D.parents[2] / 'llvm-optimize-bolt'
E = B / 'tools/bolt/results/oldtext-final-20261027'
V = E / 'validation'
read = lambda p: json.loads(p.read_text())
assert read(E / 'validation-result.json')['status'] == 'ok'
assert read(V / 'objects-current/result.json')['passed'] == 90
label = read(E / 'rss-accepted.json')['label']
result = read(V / label / 'result.json')
assert result['PASS'] and result['compiles'] == 1200
old = read(E.parent / 'runpath-fix-20261026/continue/rss-quiet-final.json')
previous = {(x['language'], x['target']): x['ratios']['candidate'] for x in old['summary']}
rows = []
for x in result['summary']:
    ratio = x['ratios']['candidate']
    rows.append({**x, 'previous_37_ratio': previous[x['language'], x['target']], 'change_percent': (ratio - 1) * 100})
(E / 'rss-comparison.json').write_text(json.dumps({'accepted_label': label, 'groups': rows}, indent=2) + '\n')
lines = ['language\ttarget\tfile\tordinary_KiB\tcandidate_KiB\tratio']
for x in read(V / label / 'per-file.json'):
    lines.append('\t'.join(map(str, [x['language'], x['target'], x['name'], x['medians']['ordinary'], x['medians']['candidate'], x['ratios']['candidate']])))
(E / 'rss-medians.tsv').write_text('\n'.join(lines) + '\n')
p = B / 'docs/bolt/39_use_old_text_final.md'
s = p.read_text()
intro = ('完整构建、全部门禁、23包比较和90 TU均通过；许可之外的RPM内容差异为零。最终clang为152,532,296字节，比原布局缩小16.75%，RUNPATH为`$ORIGIN/../lib64`。'
         f'运行时最大RSS相对ordinary的变化为{min(x["change_percent"] for x in rows):.2f}%至{max(x["change_percent"] for x in rows):.2f}%，下表按语言和目标分别列出。')
s = s.replace(s.split('\n\n')[1], intro, 1)
s = s.replace('90 TU：正在按37号同一实体路径方法执行，结果待补；不得由tiny/real或RPM一致性替代。',
              '90 TU全部PASS：30个输入×3目标，ordinary和candidate依次占用同一路径/实体，完整.o逐字节相同，不移除.GCC.command.line。见[objects-current/result.json](../../tools/bolt/results/oldtext-final-20261027/validation/objects-current/result.json)。')
s = s.replace('待执行。C/C++各20文件×3目标', '已完成1200次有效测量。C/C++各20文件×3目标')
table = '\n\n| 语言 | 目标 | 本轮old-text candidate/ordinary RSS | 变化 | 37号原布局比值 |\n|---|---|---:|---:|---:|\n'
for x in rows:
    table += f'| {x["language"]} | {x["target"]} | {x["ratios"]["candidate"]:.9f} | {x["change_percent"]:+.2f}% | {x["previous_37_ratio"]:.9f} |\n'
attempts = read(E / 'rss-attempts.json')
table += (f'\n接受的完整批次为`{label}`；共执行{len(attempts)}批，原始样本全部保留。'
          '逐文件5次中位数见[rss-medians.tsv](../../tools/bolt/results/oldtext-final-20261027/rss-medians.tsv)，'
          '汇总见[rss-comparison.json](../../tools/bolt/results/oldtext-final-20261027/rss-comparison.json)，'
          '负载判定见[rss-attempts.json](../../tools/bolt/results/oldtext-final-20261027/rss-attempts.json)。'
          f'每次time -v、argv、load和频率记录在validation/{label}/中。1200次测量的对象也全部通过逐字节检查。\n')
table += '''
| BOLT阶段 | 37号 | 本轮 | 差值 |
|---|---:|---:|---:|
| disk-report begin → compare-root | 883 s | 842 s | -41 s |
| llvm-bolt工具Ninja构建 | 108 s | 157 s | +49 s |

本轮重写进程的/proc观察窗口为44.045057秒，10ms采样的最大VmHWM为9,695,160 KiB；它是采样下界，不是wait4/GNU time的精确rusage。37号old-text实验为42.806872秒、GNU time最大RSS 9,686,616 KiB。37号原发布参数的重写没有同口径独立进程峰值记录，不能填充一个数值冒充对照；其bolt.log创建至最后写入约21.615秒，本轮对应41.878秒，仅作文件时间戳近似对照。资源限额与运行条件不同，不能把这些差值全部归因于参数。原始阶段行号和时间证据见[timing-comparison.json](../../tools/bolt/results/oldtext-final-20261027/timing-comparison.json)。
'''
s = s.replace('\n## 6. 操作记录、推送和保留', table + '\n## 6. 操作记录、推送和保留')
p.write_text(s)
print(json.dumps({'PASS': True, 'RSS': rows}, indent=2))
