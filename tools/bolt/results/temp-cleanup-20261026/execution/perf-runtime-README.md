# 34号性能测量运行环境保全

以后重跑34号测量，须把loader、运行库和resource-dir指向本目录：

- loader: `lib64/ld-linux-x86-64.so.2`
- library path: `lib64`（保留`lib64 -> usr/lib64`及库自身相对符号链接）
- clang resource-dir: `resource-dir`

源自 hybrid+BOLT gbs-root；8个运行库和完整build/lib64/clang/22已按runtime-preservation.json核对SHA。源码、products与原测量脚本均未修改。
