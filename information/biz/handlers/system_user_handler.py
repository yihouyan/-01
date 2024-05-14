#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:test
# datetime:2020-11-26
# software: PyCharm




import json
from libs.base_handler import BaseHandler
from models.server import SystemUser, model_to_dict
from websdk.db_context import DBContext
from opssdk.operate import MyCryptV2
from libs.common import exec_shell, is_number
from libs.server.push_system_user import PushSystemUser
import shortuuid


class SystemUserHanlder(BaseHandler):
    def get(self, *args, **kwargs):
        key = self.get_argument('key', default=None, strip=True)
        value = self.get_argument('value', default=None, strip=True)
        page_size = self.get_argument('page', default=1, strip=True)
        limit = self.get_argument('limit', default=10, strip=True)
        limit_start = (int(page_size) - 1) * int(limit)
        system_user_list = []
        with DBContext('r', None, True) as session:
            if key and value:
                count = session.query(SystemUser).filter_by(**{key: value}).count()
                system_user_data = session.query(SystemUser).filter_by(**{key: value}).order_by(
                    SystemUser.id).offset(limit_start).limit(int(limit))
            else:
                count = session.query(SystemUser).count()
                system_user_data = session.query(SystemUser).order_by(SystemUser.id).offset(
                    limit_start).limit(int(limit))

        for data in system_user_data:
            data_dict = model_to_dict(data)
            data_dict['create_time'] = str(data_dict['create_time'])
            data_dict['update_time'] = str(data_dict['update_time'])
            if data_dict['platform_users']:
                data_dict['platform_users'] = data_dict.get('platform_users', '').split(',')
            system_user_list.append(data_dict)

        return self.write(dict(code=0, msg='获取成功', count=count, data=system_user_list))

    def post(self, *args, **kwargs):
        data = json.loads(self.request.body.decode("utf-8"))
        name = data.get('name', None)  # 名称，也是唯一
        system_user = data.get('system_user', None)  # 系统用户
        platform_users = data.get('platform_users', [])  # 平台用户
        priority = data.get('priority', None)  # 优先级
        sudo_list = data.get('sudo_list', None)  # sudo权限
        bash_shell = data.get('bash_shell', None)  # sudo权限
        remarks = data.get('remarks', None)  # 备注

        if not name or not system_user or not priority or not sudo_list or not bash_shell:
            return self.write(dict(code=-2, msg='关键参数不能为空'))

        if not platform_users:
            return self.write(dict(code=-2, msg='请至少选择一个关联用户'))

        if not is_number(priority):
            return self.write(dict(code=-2, msg='优先级必须是数字'))

        with DBContext('r', None, True) as session:
            exist_id = session.query(SystemUser.id).filter(SystemUser.name == name).first()
            exist_priority = session.query(SystemUser.id).filter(SystemUser.priority == int(priority)).first()

        if exist_id:
            return self.write(dict(code=-2, msg='不要重复记录'))

        if exist_priority:
            return self.write(dict(code=-2, msg='优先级冲突'))

        key_name = shortuuid.uuid()
        init_keygen_cmd = 'ssh-keygen -t rsa -P "" -f /tmp/{}'.format(key_name)
        code, ret = exec_shell(init_keygen_cmd)
        if code == 0:
            with open('/tmp/{}'.format(key_name), 'r') as id_rsa, open(
                    '/tmp/{}.pub'.format(key_name), 'r') as id_rsa_pub:
                mc = MyCryptV2()  # 实例化
                _private_key = mc.my_encrypt(id_rsa.read())
                _public_key = mc.my_encrypt(id_rsa_pub.read())
                with DBContext('w', None, True) as session:
                    new_system_user = SystemUser(name=name, system_user=system_user, priority=priority,
                                                 sudo_list=sudo_list,
                                                 bash_shell=bash_shell, id_rsa=_private_key, id_rsa_pub=_public_key,
                                                 platform_users=','.join(platform_users),
                                                 remarks=remarks)
                    session.add(new_system_user)
            return self.write(dict(code=0, msg='添加成功'))
        else:
            return self.write(dict(code=-4, msg=ret))

    def put(self, *args, **kwargs):
        data = json.loads(self.request.body.decode("utf-8"))
        id = data.get('id', None)
        name = data.get('name', None)  # 名称，也是唯一
        system_user = data.get('system_user', None)  # 系统用户
        platform_users = data.get('platform_users', [])  # 平台用户
        priority = data.get('priority', None)  # 优先级
        sudo_list = data.get('sudo_list', None)  # sudo权限
        bash_shell = data.get('bash_shell', None)  # sudo权限
        remarks = data.get('remarks', None)  # 备注

        if not name or not system_user or not priority or not sudo_list or not bash_shell:
            return self.write(dict(code=-2, msg='关键参数不能为空'))

        if not platform_users:
            return self.write(dict(code=-2, msg='请至少选择一个关联用户'))

        if not is_number(priority):
            return self.write(dict(code=-2, msg='优先级必须是数字'))

        with DBContext('w', None, True) as session:
            exist_sudo_list = session.query(SystemUser.sudo_list).filter(SystemUser.id == id).first()
            if exist_sudo_list[0] != sudo_list:
                obj = PushSystemUser()
                obj.update_user_sudo(system_user, sudo_list)
            session.query(SystemUser).filter(SystemUser.id == id).update(
                {SystemUser.platform_users: ','.join(platform_users), SystemUser.priority: priority,
                 SystemUser.sudo_list: sudo_list, SystemUser.remarks: remarks})
        return self.write(dict(code=0, msg='编辑成功'))

    def delete(self, *args, **kwargs):
        data = json.loads(self.request.body.decode("utf-8"))
        id = data.get('id')
        if not id:
            return self.write(dict(code=-2, msg='关键参数不能为空'))

        with DBContext('w', None, True) as session:
            session.query(SystemUser).filter(SystemUser.id == id).delete(synchronize_session=False)

        self.write(dict(code=0, msg='删除成功'))


system_user_urls = [
    (r"/v1/cmdb/system_user/", SystemUserHanlder)
]
