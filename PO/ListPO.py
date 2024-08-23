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
1.8 整数转数字列表
# print(list(map(int, str(12345))))  # [1, 2, 3, 4, 5]
# print([int(x) for x in str(12345)])  # [1, 2, 3, 4, 5]

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

todo：【其他】
7 对齐列表的键值对格式 alignKeyValue(['key1,value1', 'key1,value1'], ","))
"""


from random import choice
from collections import Counter
from PO.StrPO import *
Str_PO = StrPO()


class ListPO:

    def __init__(self):
        pass

    """[转换]"""

    def listPair2dict(self, varList):

        # 1.5 列表中配对转字典（覆盖update）
        # print(List_PO.listPair2dict(["a", "1", 100, 2]))  # {'a': '1', 100: 2}
        # print(List_PO.listPair2dict(["a", "1", "a", "2"]))  # {'a': '2'}   //如遇重复key则取后面的key值
        # print(List_PO.listPair2dict(["a", "1", "b", "2", "c"]))  # {'a': '1', 'b': '2'}  //如果元素个数是奇数，则忽略最后一个元素

        dict4 = {}
        if len(varList) < 2:
            return None
        elif len(varList) % 2 == 0:
            for i in range(0, len(varList), 2):
                dict4.update({varList[i]: varList[i + 1]})
            return dict4
        else:
            for i in range(0, len(varList[:-1]), 2):
                dict4.update({varList[i]: varList[i + 1]})
            return dict4

    def listKeyValue2dict(self, varList, varSign=":"):

        # 1.6 列表中键值对格式转字典（覆盖update）
        # print(List_PO.listKeyValue2dict(['a : 1', 'b : 2']))  # {'a': '1', 'b': '2'}
        # print(List_PO.listKeyValue2dict(['a , 3', 'b , 4'], ","))  # {'a': '3', 'b': '4'}
        # print(List_PO.listKeyValue2dict(['a : 1', 'b : 2', 'a : 133']))  # {'a': '133', 'b': '2'}  //如遇重复key则取后面的key值
        # print(List_PO.listKeyValue2dict(['a : 1', '123b456', 'c : 3']))  # {'a': '1', 'c': '3'}   ////忽略不符合键值对格式

        dict3 = {}
        try:
            for item in varList:
                if varSign in item:
                    keys = item.split(varSign)
                    dict3.update({keys[0].strip(): keys[1].strip()})
            return dict3
        except:
            return None


    """【操作元素】"""

    def split(self, varList, varElement, varMode):

        # 2.3 列表分裂
        # print(List_PO.split([1, 2, 3, '测试', 4, 5, "测试", 6], '测试', 0))  # [1,2,3]
        # print(List_PO.split([1, 2, 3, '测试', 4, 5, 6], '测试', 1))  # [4,5,6]
        # print(List_PO.split([1, 2, 3, '测试', 4, 5, "测试", 6], '测试', 1))  # [4, 5, '测试', 6]   只处理第一个参数

        if varMode == 1:
            list3 = []
            a = ""
            for i in varList:
                if i == varElement:
                    a = 1
                if a == 1:
                    list3.append(i)
            list3.pop(0)
            return list3
        elif varMode == 0:
            # 将列表中某个元素之前的元素组成一个新的列表， 如 [1,2,3,'审核信息',4,5,6] 变为 [1,2,3]
            list4 = []
            for i in varList:
                if varElement == i:
                    break
                list4.append(i)
            return list4

    def group(self, varList, varNum):

        # 2.4 列表分组
        # print(List_PO.group(['1', '2', '3', '4', '5', '6'], 2))  # [['1', '2'], ['3', '4'], ['5', '6']]  // 一个列表拆分成2个一组。
        # print(List_PO.group(['1', '2', '3', '4', '5', '6'], 3))  # [['1', '2', '3'], ['4', '5', '6']]
        # print(List_PO.group(['1', '2', '3', '4', '5', '6'], 5))  # [['1', '2', '3', '4', '5'], ['6']]  // 一个列表拆分成5个一组，不足5个元素可组成子列表。
        # print(numpy.array_split(['1', '2', '3', '4', '5', '6'], 2)[0])
        # print(numpy.array_split(['1', '2', '3', '4', '5', '6'], 2)[1])
        # print(numpy.array_split(['1', '2', '3', '4', '5', '6'], 5)) # [array(['1', '2'], dtype='<U1'), array(['3'], dtype='<U1'), array(['4'], dtype='<U1'), array(['5'], dtype='<U1'), array(['6'], dtype='<U1')]
        # print(numpy.array_split(['1', '2', '3', '4', '5', '6'], 5)[0][1])  # 取0得['1', '2'] ，取1得 2
        # print(numpy.array_split(['1', '2', '3', '4', '5', '6'], 5)[1])  # 取0得['1', '2'] ，取1得['3']

        try:
            list_of_groups = zip(*(iter(varList),) * varNum)
            end_list = [list(i) for i in list_of_groups]
            count = len(varList) % varNum
            end_list.append(varList[-count:]) if count != 0 else end_list
            return end_list

            # 方法2：通过切片可以一次append添加多个元素，如 list.append(varList[0:2]),即一条命令可以添加2个元素
            # l_valueAll = []
            # for i in range(0, len(varList), varNum):
            #     l_valueAll.append(varList[i:i+varNum])
            # return (l_valueAll)
        except:
            return None

    def merge(self, varList, varNum):

        # 2.5 列表元素合并

        # 列表元素必须是字符串，不支持数字或内嵌子列表。
        # print(List_PO.merge(["a", "b", "c", "d"], 4))  # ['abcd']   //列表中每4个元素合成一个元素
        # print(List_PO.merge(["a", "b", "c", "d"], 2))  # ['ab', 'cd']  //列表中每2个元素合成一个元素
        # print(List_PO.merge(["a", "b", "c", "d", "e", "f"], 4))  # ['abcd', 'ef']  //列表中每4个元素合成一个元素，其余不足4个元素合成一个元素
        # print(List_PO.merge(["a", "b", 123, "d", "e", "f"], 4))  # None  //列表元素必须是字符串，否则返回None

        list1 = []
        str1 = ""
        addition_number = 0
        i = 1
        try:
            while addition_number < len(varList):
                while i <= varNum:
                    if addition_number > len(varList) - 1:
                        break
                    else:
                        str1 = str1 + varList[addition_number]
                        addition_number += 1
                    i += 1
                list1.append(str1)
                str1 = ""
                i = 1
            return list1
        except:
            return None


    def joint(self, varList1, varList2):

        """2.6 两列表元素相加或连接
        将两个列表中的对应元素相加，并返回结果列表。
        相加结果列表。如果两个列表长度不一致或元素类型不一致，则返回None。
        """
        return [i + j for i, j in zip(varList1, varList2)]


    """[比较]"""

    
    def delIntersection(self, varList1, varList2):

        # 3.1 比较两组列表，各自去掉交集元素
        
        a = [x for x in varList1 if x in varList2]  # 两个列表中都存在
        return [y for y in (varList1) if y not in a], [
            y for y in (varList2) if y not in a
        ]  # 两个列表中的不同元素

    def getIntersection(self, varList1, varList2):
        
        # 3.2 获取两表交集元素
        
        return [x for x in varList1 if x in varList2]  # 两个列表中都存在
    
    def getIntersectionIndex(self, varList1, varList2):

        # 3.4 获取两表交集元素的索引号
        
        error_index = []
        if len(varList1) == len(varList2):
            for i in range(0, len(varList1)):
                # 两个列表对应元素相同，则直接过
                if varList1[i] == varList2[i]:
                    pass
                else:
                    # 两个列表对应元素不同，则输出对应的索引
                    error_index.append(i)
            if error_index == []:
                return None
            else:
                return error_index
        else:
            return "error, 两列表元素数量不一致"


    """[替换]"""


    def replaceOne(self, varList, varSource, varDest):

        # 4.1 一对多替换原列表中元素
        
        return [varDest if i == varSource else i for i in varList]


    def replaceMore(self, varList, varSourceList, varDest):

        # 4.2 批量替换N个到列表
        # 多对一，多个元素被一个元素替换，影响原列表。
        # print(List_PO.listReplaceElements(["1", 2, "3", ":"], [":", 2], 7))  # ['1', 7, '3', 7]

        return [varDest if i in varSourceList else i for i in varList]



    def replaceMore2(self, varList, varDict):

        # 4.3 批量替换N个到列表2

        return [varDict[i] if i in varDict else i for i in varList]



    def replaceCapital(self, varList):

        # 4.4 替换元素首字母大写且其余小写
        
        return list(map(lambda s: s[0:1].upper() + s[1:].lower(), varList))


    """[删除]"""


    def strip(self, varList):

        # 5.1 删除元素左右空格
        
        return [n.strip() for n in varList]


    def delSpecialChar(self, varList):

        # 5.2 删除特殊字符
        # 如：\n\t\r\xa0等

        return ["".join([i.strip() for i in str(a).strip()]) for a in varList]
        # return ([''.join([i.strip() for i in str(a).strip().replace(varSource, varDest)]) for a in varList])


    def dels(self, varList, varPartElement, varMode="-accurate"):

        # 5.3 删除指定的或模糊的元素

        tmpList = []
        for i in range(len(varList)):
            if varMode == "-accurate":
                if varPartElement != varList[i]:
                    tmpList.append(varList[i])
            else:
                if type(varPartElement) != type(varList[i]):
                    tmpList.append(varList[i])
                elif varPartElement not in varList[i]:
                    tmpList.append(varList[i])
        return tmpList

    
    def delDuplicateElement(self, varList):

        # 5.4 删除重复的元素
        
        return [item for item in varList if varList.count(item) == 1]


    def deduplication(self, varList):

        # 5.5 列表元素去重

        return sorted(set(varList), key=varList.index)
        # 列表去重,并从小到大排列
        # def duplicateRemovalBySort(self, varList):
        #     return list(set(varList))



    def getDuplicationCount(self, varList):

        # 6 获取重复的元素数量

        counter = Counter()
        counter.update(varList)
        return counter.most_common()


    def getRandomOne(self, varList):

        # 7 随机获取列表元素

        return choice(varList)


    def alignKeyValue(self, varList, varSplit):

        # 8 对齐列表的键值对格式

        l1 = []
        l2 = []
        try:
            for i in range(len(varList)):
                varCount = varList[i].count(varSplit)
                if varCount == 1:
                    l1.append(str(varList[i]).split(varSplit)[0])  # key
                    l2.append(str(varList[i]).split(varSplit)[1])  # value
                elif varCount > 1:
                    for j in range(0, len(str(varList[i]).split(varSplit)) - 1, 2):
                        l1.append(
                            str(varList[i]).split(varSplit)[j].replace(varSplit, "")
                        )  # key
                        l2.append(
                            str(varList[i]).split(varSplit)[j + 1].replace(varSplit, "")
                        )  # value
                else:
                    l1.append(
                        str(varList[i])
                            .replace("(", "（")
                            .replace(")", "）")
                            .replace(varSplit, "")
                    )  # key
                    l2.append("")  # value

            # print(l1)
            # print(l2)
            # 排版
            count = 0
            for i in range(len(l1)):
                if len(l1[i]) > count:
                    count = len(l1[i])
            for i in range(len(l1)):
                if Str_PO.isChinese(l1[i]):
                    # 全部是汉字
                    if count != len(l1[i]):
                        l1[i] = l1[i] + "  " * (count - len(l1[i])) + ":"
                    else:
                        l1[i] = l1[i] + ":"
                elif Str_PO.isContainChinese(l1[i]):
                    # 部分是汉字 ? 未处理 同上
                    l1[i] = l1[i] + "  " * (count - len(l1[i])) + ":"
                else:
                    # 全部是非汉字
                    l1[i] = l1[i] + " " * (count - len(l1[i])) + ":"
            # print(l1)
            # print(l2)
            c = [i + j for i, j in zip(l1, l2)]
            return c
        except:
            print(
                "[ERROR], "
                + sys._getframe(1).f_code.co_name
                + ", line "
                + str(sys._getframe(1).f_lineno)
                + ", in "
                + sys._getframe(0).f_code.co_name
                + ", SourceFile '"
                + sys._getframe().f_code.co_filename
                + "'"
            )

