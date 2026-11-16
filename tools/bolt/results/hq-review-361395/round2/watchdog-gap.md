看门狗首轮以短命命令的后台子进程启动，仅留下首条采样，未持续记录。
04:45 左右复查发现末条仍为 2026-11-16T04:27:18.244266-08:00；不能证明未采样期间 MemAvailable 始终高于 6GiB。
恢复前现场 MemAvailable=19520232 kB，cgroup oom/oom_kill/oom_group_kill=0。
随后在长期存活的 systemd 交互 shell 中启动同一脚本（PID 448472），不修改阈值或资源上限。
完整时间范围见 watchdog-snapshot.jsonl；不将这一段缺口记成“全程看门狗通过”。
导出停止后不再运行产品检查，不为本次候选宣称完成全部资源审计。
