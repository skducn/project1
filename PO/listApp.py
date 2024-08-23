# -*- coding: utf-8 -*-
# *********************************************************************
# Author        : John
# Date          : 2019-12-23
# Description   : 列表对象层
# *********************************************************************
"""
todo：【转换】
1.1 两列表合并字典（后覆盖） print(dict(zip([1, 2], ['skducn', 'yoyo']))) # {1: 'skducn', 2: 'yoyo'}
1.2 enumerate索引列表转字典 print(dict(enumerate(['a','b','c'], start=1)))  # {1: 'a', 2: 'b', 3: 'c'}
1.3 fromkeys列表多对一值转字典
print(dict.fromkeys(['a', 5], 1))  # {'a':1, 5:1}
print(dict.fromkeys(['a', 5, 'tt'], "100"))  # {'a': '100', 5: '100', 'tt': '100'}
print(dict.fromkeys(['a', 5]))  # {'a': None, 5: None}
1.4 列表内两元组转字典（后覆盖） print(dict([('a', '123'), ('b', '456')]))  # {'a': '123', 'b': '456'}
1.5 列表中配对转字典（后覆盖） print(List_PO.listPair2dict(["a", "1", 100, 2]))  # {'a': '1', 100: 2}
1.6 列表中键值对格式转字典（后覆盖） print(List_PO.listKeyValue2dict(['a : 1', 'b : 2']))  # {'a': '1', 'b': '2'}
1.7 列表转字符串 print(",".join(['John', 'Doe', 'Jack', 'Bob', 'Smith']))  # John,Doe,Jack,Bob,Smith


todo：【操作元素】
2.1 生成元素索引 list(enumerate(['Spring', 'Summer', 'Fall', 'Winter'], start=1))
2.2 数字字符串与数字互相转换 list(map(int,['1','2','3'])))  # [1, 2, 3]
2.3 列表分裂 List_PO.split([1, 2, 3, '测试', 4, 5, "测试", 6], '测试', 0))  # [1,2,3]
2.4 列表分组 List_PO.group(['1', '2', '3', '4', '5', '6'], 2))  # [['1', '2'], ['3', '4'], ['5', '6']]  // 一个列表拆分成2个一组。
2.5 列表元素合成 List_PO.merge(["a", "b", "c", "d"], 4))  # ['abcd']   //列表中每4个元素合成一个元素
2.6 两列表元素相加或连接 joint([1, [111], "a", 0.01], [2, [222], "b", 0.07 , 66]))  # [3, [111, 222], 'ab', 0.08]
2.7 随机获取列表元素 print(List_PO.getRandomOne(['111', 222, [5, 6, '888'], {"a": 1, 2: "test"}]))
2.8 递归列表
from iteration_utilities import deepflatten
print(list(deepflatten([[1,2,3],[4,[5],[6,7]],[8,[9,[10]]]], depth=3)))  # [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  //多层递归
print([i for sublist in [[1,2,3],[3]] for i in sublist])  # [1, 2, 3, 3]  # 一层递归
2.9 列表元素计算后增加元素

todo：【比较】
3.1 删除两列表交集元素 print(List_PO.delIntersection(['01', '02', '03'], ['02', '05']))  # (['01', '03'], ['05'])
3.2 获取两列表相同元素 print(List_PO.getIntersection(['a', 'b', 'c', 'd'], ['b', 'c', 'kk', 'z']))  # ['b', 'c']
3.3 获取两列表中在list1且不在list2的元素 print([x for x in [1,2,3] if x not in [1,5,6]])
3.4 获取两列表相同元素的索引号 twoListGetSameIndex(['a', 'b', 'c', 'd'], ['a', 'k', 'c', 'z']))  # [1, 3]

todo：【替换】
4.1 批量替换1个到列表 print(List_PO.replaceOne(["1", 2, "3", "2", 2], 2, ""))  # ['1', '', '3', '2', '']
4.2 批量替换N个到列表 print(List_PO.replaceMore(["1", 2, "3", ":"], [":", 2], 7))  # ['1', 7, '3', 7]
4.3 批量替换N个到列表2 print(List_PO.replaceMore2(["1", 2, "3", ":"], {":": 12, 2: 77}))  # ['1', 77, '3', 12]
4.4 替换元素首字母大写且其余小写 replaceCapital(['adam', 'LISA', 'barT'])  # ['Adam', 'Lisa', 'Bart']

todo：【删除】
5.1 删除元素左右空格 print(List_PO.strip(['   glass', 'apple   ', '  greenleaf  ']))  # ['glass', 'apple', 'greenleaf']
5.2 删除特殊字符（\n\t\r\xa0等）print(List_PO.delSpecialChar(['0\n编号', '1\n既往史', 444, '2\n既\r往    史\t\n逻\xa0辑', 'abc']))   #  ['0编号', '1既往史', '444', '2既往史逻辑', 'abc']
5.3 删除指定的或模糊的元素 print(List_PO.dels(['0', "错误", '1', 123, "错误"], "错误"))  # ['0', '1', 123]  // 删除“错误”元素
5.4 删除重复的元素 print(List_PO.delDuplicateElement([2, "a", 1, "\n", "\n", 13, "", "test", 6, 2, "", "", 1, "a"]))  # [13, 'test', 6]
5.5 列表元素去重 print(List_PO.deduplication([2, 1, 13, 6, 2, 1]))  # [2, 1, 13, 6]

todo：【统计】
6 获取重复的元素数量 print(List_PO.getDuplicationCount([2, 1, 13, 6, 2, 1]))  # [(2, 2), (1, 2), (13, 1), (6, 1)]

todo：【应用】
7.1 对齐列表的键值对格式 alignKeyValue(['key1,value1', 'key1,value1'], ","))
7.2 需要计算每个产品的纳税额，税率为10%。并将纳税额作为第三个元素添加到每个产品信息中".center(100, "-"))
7.3 将列表中每个元素首字母进行大写转换
7.4 整数转数字列表
# print(list(map(int, str(12345))))  # [1, 2, 3, 4, 5]
# print([int(x) for x in str(12345)])  # [1, 2, 3, 4, 5]
7.5 两列表相乘
b1 = [100, 200, 300]
b2 = [1, 2, 3]
iterator = map(lambda x,y : x*y, b1, b2)
print(list(iterator))  # 输出：[100, 400, 900]
"""


from PO.ListPO import *
List_PO = ListPO()


"""【转换】"""

# # print("1.1 两列表合并字典（后覆盖）".center(100, "-"))
# print(dict(zip([1, 2], ['skducn', 'yoyo'])))  # {1: 'skducn', 2: 'yoyo'}
# print(dict(zip([1, 1], ['skducn', 'yoyo'])))  # {1: 'yoyo'}
#
# # print("1.2 enumerate索引列表转字典".center(100, "-"))
# print(dict(enumerate(['a','b','c'], start=1)))  # {1: 'a', 2: 'b', 3: 'c'}
#
# # print("1.3 fromkeys列表多对一值转字典".center(100, "-"))
# print(dict.fromkeys(['a', 5], 1))  # {'a':1, 5:1}
# print(dict.fromkeys(['a', 5, 'tt'], "100"))  # {'a':1, 5:1}
# print(dict.fromkeys(['a', 5]))  # {'a': None, 5: None}
#
# # print("1.4 列表内两元组转字典（后覆盖）".center(100, "-"))
# print(dict([('a', '123'), ('b', '456'), ('a', '100')]))  # {'a': '100', 'b': '456'}
#
# # print("1.5 列表中配对转字典（后覆盖）".center(100, "-"))
# print(List_PO.listPair2dict(["a", "1", 100, 2]))  # {'a': '1', 100: 2}
# print(List_PO.listPair2dict(["a", "1", "a", "2"]))  # {'a': '2'}   //如遇重复key则取后面的key值
# print(List_PO.listPair2dict(["a", "1", "b", "2", "c"]))  # {'a': '1', 'b': '2'}  //如果元素个数是奇数，则忽略最后一个元素
#
# # print("1.6 列表中键值对格式转字典（后覆盖）".center(100, "-"))
# print(List_PO.listKeyValue2dict(['a : 1', 'b : 2']))  # {'a': '1', 'b': '2'}
# print(List_PO.listKeyValue2dict(['a , 3', 'b , 4'], ","))  # {'a': '3', 'b': '4'}
# print(List_PO.listKeyValue2dict(['a : 1', 'b : 2', 'a : 133']))  # {'a': '133', 'b': '2'}  //如遇重复key则取后面的key值
# print(List_PO.listKeyValue2dict(['a : 1', '123b456', 'c : 3']))  # {'a': '1', 'c': '3'}   ////忽略不符合键值对格式
#
# # print("1.7 列表转字符串".center(100, "-"))
# print(",".join(['John', 'Doe', 'Jack', 'Bob', 'Smith']))  # John,Doe,Jack,Bob,Smith
#


"""[操作元素]"""

# print("2.1 生成元素索引".center(100, "-"))
# print(list(enumerate(['Spring', 'Summer', 'Fall', 'Winter'], start=1)))

# print("2.2 数字字符串与数字互相转换".center(100, "-"))
# print(list(map(int,['1','2','3'])))  # [1, 2, 3]
# print(list(map(str,[1,2,3])))  # ['1', '2', '3']
# print(list(map(str,[123, "a"])))  # ['123', 'a']

# print("2.3 列表分裂".center(100, "-"))
# print(List_PO.split([1, 2, 3, '测试', 4, 5, "测试", 6], '测试', 0))  # [1,2,3]
# print(List_PO.split([1, 2, 3, '测试', 4, 5, 6], '测试', 1))  # [4,5,6]
# print(List_PO.split([1, 2, 3, '测试', 4, 5, "测试", 6], '测试', 1))  # [4, 5, '测试', 6]   只处理第一个参数

# print("2.4 列表分组".center(100, "-"))
# print(List_PO.group(['1', '2', '3', '4', '5', '6'], 2))  # [['1', '2'], ['3', '4'], ['5', '6']]  // 一个列表拆分成2个一组。
# print(List_PO.group(['1', '2', '3', '4', '5', '6'], 3))  # [['1', '2', '3'], ['4', '5', '6']]
# print(List_PO.group(['1', '2', '3', '4', '5', '6'], 5))  # [['1', '2', '3', '4', '5'], ['6']]  // 一个列表拆分成5个一组，不足5个元素可组成子列表。
# print(numpy.array_split(['1', '2', '3', '4', '5', '6'], 2)[0])
# print(numpy.array_split(['1', '2', '3', '4', '5', '6'], 2)[1])
# print(numpy.array_split(['1', '2', '3', '4', '5', '6'], 5)) # [array(['1', '2'], dtype='<U1'), array(['3'], dtype='<U1'), array(['4'], dtype='<U1'), array(['5'], dtype='<U1'), array(['6'], dtype='<U1')]
# print(numpy.array_split(['1', '2', '3', '4', '5', '6'], 5)[0][1])  # 取0得['1', '2'] ，取1得 2
# print(numpy.array_split(['1', '2', '3', '4', '5', '6'], 5)[1])  # 取0得['1', '2'] ，取1得['3']

# print("2.5 列表元素合成".center(100, "-"))
# print(List_PO.merge(["a", "b", "c", "d"], 4))  # ['abcd']   //列表中每4个元素合成一个元素
# print(List_PO.merge(["a", "b", "c", "d"], 2))  # ['ab', 'cd']  //列表中每2个元素合成一个元素
# print(List_PO.merge(["a", "b", "c", "d", "e", "f"], 4))  # ['abcd', 'ef']  //列表中每4个元素合成一个元素，其余不足4个元素合成一个元素
# print(List_PO.merge(["a", "b", 123, "d", "e", "f"], 4))  # None  //列表元素必须是字符串，否则返回None
#
# print("2.6 两列表元素相加或连接".center(100, "-"))
# list1 = [1, [111], "a", 0.01]
# list2 = [2, [222], "b", 0.07 ,66]
# list3 = [-25, [222], "b", -0.07]
# list4 = [2, [222], "b", "111"]
# print(List_PO.joint([1, [111], "a", 0.01], [2, [222], "b", 0.07, 66]))  # [3, [111, 222], 'ab', 0.08]  //多余的元素被忽略
# print(List_PO.addTwoList(list1, list3))  # [-24, [111, 222], 'ab', -0.060000000000000005]   //注意浮点数负数计算出现问题，未知
# print(List_PO.addTwoList(list1, list4))  # None

# print("2.7 随机获取列表元素".center(100, "-"))
# print(List_PO.getRandomOne(['111', 222, [5, 6, '888'], {"a": 1, 2: "test"}]))


"""[比较]"""

# print("3.1 删除两列表交集元素".center(100, "-"))
# print(List_PO.delIntersection(['01', '02', '03'], ['02', '05']))  # (['01', '03'], ['05'])
# print(List_PO.delIntersection(['张三', '12', '33'], ['张三', '12']))  # (['33'], [])
# #
# print("3.2 获取两列表相同元素".center(100, "-"))
# print(List_PO.getIntersection(['a', 'b', 'c', 'd'], ['b', 'c', 'kk', 'z']))  # ['b', 'c']
# # #
# # print("3.3 获取两列表中在list1且不在list2的元素".center(100, "-"))
# print([x for x in [1,2,3] if x not in [1,5,6]])

# print("3.4 获取两列表相同元素的索引号".center(100, "-"))
# print(List_PO.twoListGetSameIndex(['a', 'b', 'c', 'd'], ['a', 'k', 'c', 'z']))  # [1, 3]

"""[替换]"""

# print("4.1 批量替换1个到列表".center(100, "-"))
# print(List_PO.replaceOne(["1", 2, "3", "2", 2], 2, ""))  # ['1', '', '3', '2', '']
# print(List_PO.replaceOne(["1", 2, "3", ":"], "3", 88))  # ['1', 2, 88, ':']
# print(List_PO.replaceOne(["1", 2, "3", 2, 2, 2], 2, "j"))  # ['1', 'j', '3', 'j', 'j', 'j']  //把所有2替换成j
#
# # print("4.2 替换元素多对一".center(100, "-"))
# print(List_PO.replaceMore(["1", 2, "3", ":"], [":", 2], 7))  # ['1', 7, '3', 7]
# print(List_PO.replaceMore(["1", 2, "3", ":"], [":", "2"], 7))  # ['1', 2, '3', 7]  //原列表中没有找到“2”所以不做替换。
# #
# print("4.3 批量替换N个到列表2".center(100, "-"))
# print(List_PO.replaceMore2(["1", 2, "3", ":"], {":": 12, 2: 77}))  # ['1', 77, '3', 12]
# print(List_PO.replaceMore2(["1", 2, "3", ":"], {":": 12, 1222: 77}))  # ['1', 2, '3', 12]   //如果某个key不存在，则忽略。

# print("4.4 替换元素首字母大写且其余小写".center(100, "-"))
# print(List_PO.replaceCapital(['adam', 'LISA', 'barT']))  # ['Adam', 'Lisa', 'Bart']

"""[删除]"""

# # print("5.1 删除元素左右空格".center(100, "-"))
# print(List_PO.strip(['   glass', 'apple   ', '  greenleaf  ']))  # ['glass', 'apple', 'greenleaf']
# #
# # print("5.2 删除特殊字符（\n\t\r\xa0等）".center(100, "-"))
# print(List_PO.delSpecialChar(['0\n编号', '1\n既往史', 444, '2\n既\r往    史\t\n逻\xa0辑', 'abc']))   #  ['0编号', '1既往史', '444', '2既往史逻辑', 'abc']
# print(List_PO.delSpecialChar(['\n\t\t\tCHF\xa0\r\n\r\n  \t64.90', '\n\t\tCHF\xa0\r\n\t58.40','\n\t\tCHF\xa0\r\t48.70']))  #['CHF64.90', 'CHF58.40', 'CHF48.70']
#
# # print("5.3 删除指定的或模糊的元素".center(100, "-"))
# print(List_PO.dels(['0', "错误", '1', 123, "错误"], "错误"))  # ['0', '1', 123]  // 删除“错误”元素
# print(List_PO.dels(['0', "错误", '1', 22, "错误内容"], "错误", "-like"))  # ['0', '1', 22]  //关键字vague表示模糊删除，删除包含“错误”的元素。
# print(List_PO.dels(['首页', '', '', '', '', '', '', '', '建档耗时统计', '档案更新监控'], ""))  # ['首页', '建档耗时统计', '档案更新监控']
# #
# # print("5.4 删除重复的元素".center(100, "-"))
# print(List_PO.delDuplicateElement([2, "a", 1, "\n", "\n", 13, "", "test", 6, 2, "", "", 1, "a"]))  # [13, 'test', 6]
# # #
# # # print("5.5 列表元素去重".center(100, "-"))
# print(List_PO.deduplication([2, 1, 13, 6, 2, 1]))  # [2, 1, 13, 6]


"""[统计]"""
#
# # print("6 获取重复的元素数量".center(100, "-"))
# print(List_PO.getDuplicationCount([2, 1, 13, 6, 2, 1]))  # [(2, 2), (1, 2), (13, 1), (6, 1)]
# print(List_PO.getDuplicationCount(['a', 'b', 'c', 'a']))  # [('a', 2), ('b', 1), ('c', 1)]
#
#
"""[应用]"""
#
# # print("7.1 对齐列表的键值对格式".center(100, "-"))
# list11 = List_PO.alignKeyValue(
#     ['1234567890,john', '123456,666', '123,baibai', '600065,', '600064,234j2po4j2oi34'], ",")
# for i in range(len(list11)):
#     print(list11[i])
# # # # 1234567890: john
# # # # 123456    : 666
# # # # 123       : baibai
# # # # 600065    :
# # # # 600064    : 234jpo4j2oi34


# # print("7.2 需要计算每个产品的纳税额，税率为10%。并将纳税额作为第三个元素添加到每个产品信息中".center(100, "-"))
# carts = [['SmartPhone', 400],
#          ['Tablet', 450],
#          ['Laptop', 700]]
# print(list(map(lambda item: [item[0], item[1], item[1] * 0.1], carts)))  # [['SmartPhone', 400, 40.0], ['Tablet', 450, 45.0], ['Laptop', 700, 70.0]]
#
#
# # print("7.3 将列表中每个元素首字母进行大写转换".center(100, "-"))
# names = ['david', 'peter', 'jenifer']
# new_names = map(lambda name: name.capitalize(), names)
# print(list(new_names))  # ['David', 'Peter', 'Jenifer']

# # # print("7.4 整数转数字列表".center(100, "-"))
# print(list(map(int, str(12345))))  # [1, 2, 3, 4, 5]
# print([int(x) for x in str(12345)])  # [1, 2, 3, 4, 5]

# # # print("7.5 两列表相乘".center(100, "-"))
b1 = [100, 200, 300]
b2 = [1, 2, 3]
iterator = map(lambda x,y : x*y, b1, b2)
print(list(iterator))  # 输出：[100, 400, 900]
