
# def bold(func):
#     def wrapper(*args):
#         return (f"<b>{func(*args)}</b>")
#     return wrapper
# def italic(func):
#     def wrapper(*args):
#         return (f"<i>{func(*args)}</i>")
#     return wrapper
#
# # 警告：装饰器执行顺序与声明顺序相反，@bold先应用但后执行
# @bold
# @italic
# def greet(name):
#     return (f"Hello {name}")
# print(greet("Alice"))  # <b><i>Hello Alice</i></b>

from faker import Faker

# 创建Faker实例，指定中文
fake = Faker('zh_CN')

# 生成10条地址数据
for _ in range(10):
    address = fake.address()
    print(address)
    # 示例输出: 上海市东丽县上街 510474
    # 可以进一步拆分地址 components = address.split()
    components = address.split()
    print(components)
#
#
print("省份:", fake.province())    # 如: 广东省
print("城市:", fake.city())        # 如: 广州市
print("街道:", fake.street_name()) # 如: 东风路
print("门牌号:", fake.building_number()) # 如: 123号

# --------------------------------------------------------------------------------

# from mimesis import Address
# from mimesis.locales import Locale
#
# # 创建中文地址生成器
# address = Address(Locale.ZH)
#
# for _ in range(25):
#     full_address = f"{address.province()} {address.city()} {address.street_name()} {address.street_number()}"
#     print(full_address)

# --------------------------------------------------------------------------------

# import factory
# from faker import Faker
#
# fake = Faker('zh_CN')
#
#
# class AddressFactory(factory.Factory):
#     class Meta:
#         model = dict  # 可以替换为你的数据模型类
#
#     province = factory.LazyAttribute(lambda _: fake.province())
#     city = factory.LazyAttribute(lambda _: fake.city())
#     street = factory.LazyAttribute(lambda _: fake.street_name())
#     building_number = factory.LazyAttribute(lambda _: fake.building_number())
#     full_address = factory.LazyAttribute(
#         lambda o: f"{o.province}{o.city}{o.street}{o.building_number}"
#     )
#
#
# # 生成地址数据
# address_data = AddressFactory()
# print(address_data['full_address'])  # 如: 四川省成都市解放路156号


# --------------------------------------------------------------------------------


# from faker import Faker
# from geopy.geocoders import Nominatim
#
# fake = Faker('zh_CN')
# geolocator = Nominatim(user_agent="test_app")
#
# # 生成地址并获取坐标
# address = fake.address()
# location = geolocator.geocode(address)
# if location:
#     print(f"地址: {address}")
#     print(f"坐标: ({location.latitude}, {location.longitude})")