# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2023-1-1
# Description: 当有多个条件判断时，可以考虑使用字典来简化代码，并提高效率。
# *****************************************************************

# 不推荐：使用多重if-else
def get_grade(score):
    if score >= 90:
        return 'A'
    elif score >= 80:
        return 'B'
    elif score >= 70:
        return 'C'
    else:
        return 'D'

# 推荐：使用字典映射
grade_mapping = {
    (90, 100): 'A',
    (80, 89): 'B',
    (70, 79): 'C',
    (0, 69): 'D'
}
def get_grade_dict(score):
    for key, value in grade_mapping.items():
        if key[0] <= score <= key[1]:
            return value
print(get_grade(85))  # 输出: B
print(get_grade_dict(85))  # 输出: B






