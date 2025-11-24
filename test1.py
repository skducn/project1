l_data = ['1.00', '002186', '1.03亿', '4.56%', '28.79', '27.53','1.00', '332186', '13.03亿', '44.56%', '238.79', '247.53']
if '002186' in l_data:
    index = l_data.index('002186')  # 全 聚 德
    new_index = index + 1
    l_data.pop(new_index)
    l_data.pop(new_index)
if '332186' in l_data:
    index = l_data.index('332186')  # 全 聚 德
    new_index = index + 1
    l_data.pop(new_index)
    l_data.pop(new_index)

print(l_data)

