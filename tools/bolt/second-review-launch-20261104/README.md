# 第二轮评审：仅启动演练

沿用 dca920a8 的 gbs-driver 布局及 docs50 的日志重写检测和普通卸载流程；模板 SHA 见 provenance.json。本轮源码和根目录独立，原脚本和历史根保持原样。full 模式被入口明确拒绝。

```sh
/bin/sh tools/bolt/second-review-launch-20261104/launch.sh toolchain rehearsal
/bin/sh tools/bolt/second-review-launch-20261104/launch.sh basedev rehearsal
```

两次必须串行；监测到真实 CMake 命令即停止，不运行 Ninja。本地 systemd 资源限制不写进 spec/helper。日志和 final-audit 都留在本轮新根；文档见 docs/bolt/51_second_review_fixes.md。
