# 原始列表
data_list = [{'TZ_STZB043': '是'}, {'TZ_STZB044': '是'}, {'TZ_STZB045': '是'}]
# 目标key
target_key = 'TZ_STZB045'

# 方法2：使用any()函数（更简洁）
key_exists_2 = any(target_key in item for item in data_list)
print(f"\n使用any()函数判断结果：{'存在' if key_exists_2 else '不存在'}")

print(key_exists_2)


if any('TZ_STZB045' in item for item in data_list):
    print("存在")
