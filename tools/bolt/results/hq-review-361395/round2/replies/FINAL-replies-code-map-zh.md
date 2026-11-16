# PS5 回复与代码中文对照

候选 a061f4e415a895412516ffe076084f407f2d70a8；只供用户定位，不属于英文粘贴文本。行内评论的位置仍按原PS3，以下行号按PS5。

## H1/N1

packaging/clang-bolt-helper.py

239: def call(argv, log, cwd=None, timeout=300):
243:     previous = signal.getsignal(signal.SIGCHLD)
311:         if previous is not None and previous != signal.SIG_DFL:

## H2

packaging/clang-bolt-helper.py

190: _DEFERRED_SECOND_SIGNAL = None
193: def record_cancel(signum, frame):
194:     global _CANCEL_SIGNAL, _DEFERRED_SECOND_SIGNAL
197:             if _DEFERRED_SECOND_SIGNAL is None:
198:                 _DEFERRED_SECOND_SIGNAL = signum
240:     global _ACTIVE_GROUP, _SPAWNING, _DEFERRED_SECOND_SIGNAL
254:             _SPAWNING = True
261:                 if _DEFERRED_SECOND_SIGNAL is not None:
262:                     pending = _DEFERRED_SECOND_SIGNAL
263:                     _DEFERRED_SECOND_SIGNAL = None
1919:     global _CANCEL_SIGNAL, _SPAWNING, _DEFERRED_SECOND_SIGNAL
1921:     _DEFERRED_SECOND_SIGNAL = None

## H3-helper

packaging/clang-bolt-helper.py

1067: def debugfiles_gate(debugfiles_list, identity):
1080: def post_gate(root, state, ordinary, candidate_work, resource_dir=None, debugfiles_list=None):
1856:     s=sub.add_parser('post');s.add_argument('root');s.add_argument('state');s.add_argument('ordinary');s.add_argument('work');s.add_argument('--resource-dir');s.add_argument('--debugfiles-list',required=True)

## H3-spec

packaging/llvm.spec

966:     python3 -B %{SOURCE1201} post "%{buildroot}" "%{_builddir}/%{buildsubdir}/build/clang-bolt/install-state.json" "%{_builddir}/%{buildsubdir}/build/clang-bolt/ordinary-clang-22" "%{_builddir}/%{buildsubdir}/build/clang-bolt/post-gate" --resource-dir "%{buildroot}%{_libdir}/clang/%{llvm_version}" --debugfiles-list "%{_builddir}/%{buildsubdir}/debugfiles.list" || bolt_status_exit $? \

## H4

packaging/llvm-static-archives-native.py

121:         seen_longnames = False
134:                 if seen_longnames:
136:                 seen_longnames = True

## H5/N1

packaging/llvm-static-archives-native.py

1034: def _install_main():
1075: def install_main():
1086:         if previous is not None and previous != signal.SIG_DFL:

## 中文说明

H1：helper在子进程清理/回收后的finally恢复SIGCHLD；N1跳过None，避免恢复时的TypeError掩盖原错误。
H2：只在spawn临界区暂存第二个取消信号，登记进程组后处理；失败路径也处理。未调用pthread_sigmask，子进程信号掩码不变。
H3：spec明确传入debugfiles.list，helper不再猜目录层数；原成员、SHA/CRC、权限和debug identity检查保留。
H4：用seen_longnames记录是否已经出现GNU长名表，第一张为空也拒绝第二张。
H5：外层finally覆盖参数解析退出和转换错误；N1同样保护None恢复。
Q1–Q6：不改产品代码。Q2采用10处中5处闭合/5处结构相符的边界；Q3并行度另起change评估；Q5下一轮增加最小插件载入用例。
英文文件尚未发布；所有评论和回复均由用户本人发布。
