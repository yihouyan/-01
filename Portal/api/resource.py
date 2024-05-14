#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:test
# datetime:2020-8-4
# software: PyCharm



from flask_restful import Api

from api.department.interface_department import interfaceDepartment
from api.department.interface_department_staff import interfaceDepartmentStaff
from api.login.interface_login import interfaceLogin
from api.role.interface_permission import interfacePermission
from api.role.interface_role import interfaceRole
from api.role.interface_role_permission import interfaceRolePermission
from api.user.interface_basic import interfaceUserBasic
from api.user.interface_password import interfacePassword
from api.user.interface_user import interfaceUser
from api.user_group.interface_user_group import interfaceUserGroup
from api.user_group.interface_user_group_role import interfaceUserGroupRole
from api.user_group.interface_user_group_staff import interfaceUserGroupStaff

api = Api()

api.add_resource(
    interfaceDepartment,
    '/li-boss/<version>/department',
    '/li-boss/<version>/department/<int:dpt_id>'
)


api.add_resource(
    interfaceDepartmentStaff,
    '/li-boss/<version>/department/staff/<int:dpt_id>'
)

api.add_resource(
    interfaceUser,
    '/li-boss/<version>/user',
    '/li-boss/<version>/user/<int:user_id>',

)

api.add_resource(
    interfacePassword,
    '/li-boss/<version>/user/<int:user_id>/password'
)

api.add_resource(
    interfaceUserBasic,
    '/li-boss/<version>/user/<int:user_id>/base/info'
)

api.add_resource(
    interfaceRole,
    '/li-boss/<version>/role',
    '/li-boss/<version>/role/<int:role_id>'
)
api.add_resource(
    interfaceRolePermission,
    '/li-boss/<version>/role/<role_id>/permission'
)
api.add_resource(
    interfacePermission,
     '/li-boss/<version>/permission'
)

api.add_resource(
    interfaceUserGroup,
    '/li-boss/<version>/user/group',
    '/li-boss/<version>/user/group/<int:group_id>'
)


api.add_resource(
    interfaceUserGroupStaff,
    '/li-boss/<version>/user/group/<int:group_id>/staff'
)

api.add_resource(
    interfaceUserGroupRole,
    '/li-boss/<version>/user/group/<int:group_id>/role'
)

api.add_resource(
    interfaceLogin,
    '/li-boss/<version>/login'
)