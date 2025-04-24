# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2025-4-17
# Description: # RBAC
# RBAC 并不是 Python 中的一个具体库，而是一种访问控制模型，即基于角色的访问控制（Role - Based Access Control）。在 Python 开发中，可以使用相关的库来实现 RBAC 模型。
# 主要概念
# 角色（Role）：定义了一组权限的集合，例如 “管理员”、“普通用户” 等。
# 用户（User）：系统中的实体，可以被分配一个或多个角色。
# 权限（Permission）：对系统资源的操作许可，如读取、写入、删除等。
# *****************************************************************
# 这个示例中，我们定义了权限、角色和用户的映射关系，并实现了一个简单的权限检查函数。

# 定义权限
permissions = {
    "read": "可以读取数据",
    "write": "可以写入数据",
    "delete": "可以删除数据"
}

# 定义角色
roles = {
    "admin": ["read", "write", "delete"],
    "user": ["read"]
}

# 定义用户和角色的映射
users = {
    "Alice": "admin",
    "Bob": "user"
}

def check_permission(user, action):
    role = users.get(user)
    if role:
        role_permissions = roles.get(role)
        if role_permissions and action in role_permissions:
            return True
    return False

# 检查用户权限
print(check_permission("Alice", "write"))
print(check_permission("Bob", "delete"))