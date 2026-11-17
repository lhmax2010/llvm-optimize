# First full-run failures

All suites completed. 735 unique tests; 724 PASS, 11 failing/error tests. One incomplete 2-test invocation was retained and replaced for accounting by a complete 11-test invocation after the collector fix. Raw executions: 737.

|Suite|Test|Kind|Category|Reason|
|---|---|---|---|---|
|review122-retained|test_complete_scan_signal_deadline_entire_message (__main__.Review122.test_complete_scan_signal_deadline_entire_message)|failures|b|122新增断言仍要求旧中性文字；新阶段文字含while signalling。可归入新测试文字适配，但因其他c类失败停止，未修改。|
|review114|test_deadline_partial_scan_never_empty_success (__main__.Hardening.test_deadline_partial_scan_never_empty_success)|errors|c|非字符串契约：proc_stat旧夹具返回6字段/旧断言要求6字段，新实现返回并解包7字段。超出3(a)文字替换授权；STOP，不修改。|
|review114|test_scan_permission_retains_other_members_and_fails (__main__.Hardening.test_scan_permission_retains_other_members_and_fails)|errors|c|非字符串契约：proc_stat旧夹具返回6字段/旧断言要求6字段，新实现返回并解包7字段。超出3(a)文字替换授权；STOP，不修改。|
|helper|test_single_zombie (test_second_review.SecondProcessTests.test_single_zombie)|errors|c|非字符串契约：proc_stat旧夹具返回6字段/旧断言要求6字段，新实现返回并解包7字段。超出3(a)文字替换授权；STOP，不修改。|
|helper|test_zombie_threads (test_second_review.SecondProcessTests.test_zombie_threads)|errors|c|非字符串契约：proc_stat旧夹具返回6字段/旧断言要求6字段，新实现返回并解包7字段。超出3(a)文字替换授权；STOP，不修改。|
|sessions110|test_proc_stat_session_field (__main__.SessionTests.test_proc_stat_session_field)|failures|c|非字符串契约：proc_stat旧夹具返回6字段/旧断言要求6字段，新实现返回并解包7字段。超出3(a)文字替换授权；STOP，不修改。|
|sessions110|test_foreign_session_excluded (__main__.SessionTests.test_foreign_session_excluded)|errors|c|非字符串契约：proc_stat旧夹具返回6字段/旧断言要求6字段，新实现返回并解包7字段。超出3(a)文字替换授权；STOP，不修改。|
|sessions110|test_session_dead_excluded (__main__.SessionTests.test_session_dead_excluded)|errors|c|非字符串契约：proc_stat旧夹具返回6字段/旧断言要求6字段，新实现返回并解包7字段。超出3(a)文字替换授权；STOP，不修改。|
|sessions110|test_session_matches_different_group (__main__.SessionTests.test_session_matches_different_group)|errors|c|非字符串契约：proc_stat旧夹具返回6字段/旧断言要求6字段，新实现返回并解包7字段。超出3(a)文字替换授权；STOP，不修改。|
|sessions110|test_session_zombie_excluded (__main__.SessionTests.test_session_zombie_excluded)|errors|c|非字符串契约：proc_stat旧夹具返回6字段/旧断言要求6字段，新实现返回并解包7字段。超出3(a)文字替换授权；STOP，不修改。|
|sessions110|test_zombie_leader_live_threads_included (__main__.SessionTests.test_zombie_leader_live_threads_included)|errors|c|非字符串契约：proc_stat旧夹具返回6字段/旧断言要求6字段，新实现返回并解包7字段。超出3(a)文字替换授权；STOP，不修改。|
