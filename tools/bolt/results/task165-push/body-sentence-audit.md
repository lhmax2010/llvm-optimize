# P8 正文逐句核对

行号对应 [父提交 → P8 完整 diff](parent-to-p8.diff)。
另核对：父提交与 P8 的 armv7l 目标列表均包含 ARM;BPF；两侧没有新增 python3 Requires；独立包不面向 armv7l。MODULE linker flags 无差异。主 spec 第 105 行在 x86_64 补定义 _toolchain。

| 主张 | diff 行 | 结果 |
|---|---|---|
| Build BOLT from the standalone spec against installed LLVM on x86_64 and aarch64. | 686, 689, 794 | PASS |
| Standalone links libLLVM.so; in-tree links components; the mode precedes its consumers. | 36, 38, 53, 802 | PASS |
| Only standalone dylib builds compile the X86 mirror; otherwise optional. Runtime C and C++ flags are cleared only standalone. | 26, 35, 154 | PASS |
| Provider version and release checks, per-arch target registration, LDFLAGS, libdir suffix and CMake installation of merge-fdata. | 622, 689, 789, 800, 803, 806, 817, 823 | PASS |
| bolt requires libllvm at the same version. | 731 | PASS |
| Clang ships all four analysis entry points, libexec scripts, report assets, manual and Python modules. | 932, 994, 995, 997, 998, 999, 1012, 1013, 1014 | PASS |
| The scan-view data moves from llvm-devel to llvm. | 975, 976, 985 | PASS |
| Six shebang changes and six postconditions; Python runtime Requires unchanged. | 940, 946, 950 | PASS |
| The old names are provided and only earlier versions are obsoleted. | 856, 857, 858, 859, 868, 869 | PASS |
| Later revisions withdrew armv7l BOLT packaging and the llvm Python requirement. | 686, 856 | PASS |
| When enabled, the MLGO build extracts the per-architecture assets if the directory is absent, including skipped prep. | 876, 878, 881, 884, 887 | PASS |
| Standalone executable and shared-library flags get the SHA-1 build ID. | 803, 804 | PASS |
| The llvm spec adds the build ID only under _toolchain, which x86_64 always defines. | 896, 899, 900 | PASS |
| Module linker flags retain existing settings. | 803, 899 | PASS |
