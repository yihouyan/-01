#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:test
# datetime:2024-11-5
# software: PyCharm



from enum import Enum, unique


@unique
class modelEnum(Enum):
    """
    请求模块枚举类
    """

    user = {'root': 'users', 'body': 'user'}
    department = {'root': 'departments', 'body': 'department'}
    role = {'root': 'roles', 'body': 'role'}
    user_group = {'root': 'user_groups', 'body': 'user_group'}
    login = {'root': 'logins', 'body': 'login'}
    permission = {'root': 'permissions', 'body': 'permission'}
    role_permission = {'root': 'role_permissions', 'body': 'role_permission'}
