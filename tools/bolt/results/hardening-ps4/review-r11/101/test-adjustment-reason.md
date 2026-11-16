PM 裁决 F1/F3 改变了该诊断的输出约定。

只将96号新增 test_startup_all_signal_states 的 unset CFLAGS/CXXFLAGS 断言从 []/[] 改为 None/None；该测试没有 default_int_handler 断言，故无需第二处调整。基线模块引用改为历史只读绝对路径，数据与判断不变。原103项测试副本SHA与96号环境一致。
