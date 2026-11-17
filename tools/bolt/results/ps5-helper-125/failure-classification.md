# 第一轮失败分类

739项，733通过，3 FAIL + 3 ERROR，全部(b)；(a)=0，(c)=0。既有722项全通过。

- test_deadline_member_list_twenty_limit (__main__.Review122.test_deadline_member_list_twenty_limit)：122 新夹具仍以额外的位置元素携带名称；与125的附加属性规则不符
- test_snapshot_twenty_limit (__main__.Review122.test_snapshot_twenty_limit)：122 新夹具仍以额外的位置元素携带名称；与125的附加属性规则不符
- test_stat_name_parentheses (__main__.Review122.test_stat_name_parentheses)：122 新夹具仍以额外的位置元素携带名称；与125的附加属性规则不符
- test_member_read_eio_continues (__main__.Review122.test_member_read_eio_continues)：122 新夹具仍以额外的位置元素携带名称；与125的附加属性规则不符
- test_member_read_emfile_continues (__main__.Review122.test_member_read_emfile_continues)：122 新夹具仍以额外的位置元素携带名称；与125的附加属性规则不符
- test_real_scan_names_survive_exit_without_comm_reads (__main__.Review122.test_real_scan_names_survive_exit_without_comm_reads)：122 新夹具仍以额外的位置元素携带名称；与125的附加属性规则不符

125授权的一次新测试纠正：用 comm 属性替代122新夹具的第7/4元素；不改场景、清理结果、错误类型、名称或20项上限的期望。产品不再修改。第二轮从头739/739通过。
