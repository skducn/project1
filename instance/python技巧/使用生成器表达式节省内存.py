# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2023-1-1
# Description: 当你处理大数据集时，生成器表达式可以节省大量内存，因为它只在需要时生成数据。
# *****************************************************************

# 不推荐：使用列表存储所有平方数
squares_list = [i ** 2 for i in range(1000000)]

# 推荐：使用生成器表达式
squares_generator = (i ** 2 for i in range(1000000))

# 计算总和
print(sum(squares_list))  # 需要大量内存
print(sum(squares_generator))  # 内存使用较少








