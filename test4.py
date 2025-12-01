list1 = [1,2,3,4,5]
list2 = [1,2,3]

for item1, item2 in zip(list1, list2):
    print(item1, item2)


from itertools import zip_longest
for item1, item2 in zip_longest(list1, list2):
    print(item1, item2)  # 长度不足时补None