a= [[6, '用户模块', None, '{1:"select count(*) from user where nick_name=\'李四\' and user_name=\'zhangsan\'"，"validation"：{"name":"张三",\'age\':\'20\',\'sex\':"1"}}', '新增用户.py'], [7, '系统模块', None, '{1:"select count(*) from user where nick_name=\'张三\' and user_name=\'zhangsan\'"，"validation"：{"name":"张三",\'age\':\'20\',\'sex\':"1"}}', '系统.py']]

for i in range(len(a)):
    print(a[i][1])