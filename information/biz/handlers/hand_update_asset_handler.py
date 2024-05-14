#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:test
# datetime:2022-7-19
# software: PyCharm




import json
from libs.base_handler import BaseHandler
from models.server import Server, AdminUser
from websdk.db_context import DBContext
import tornado.web
from tornado import gen
from concurrent.futures import ThreadPoolExecutor
from tornado.concurrent import run_on_executor
from libs.server.collect_asset_info import get_server_sysinfo
from libs.server.server_common import update_asset, rsync_public_key
from websdk.web_logs import ins_log
import datetime


class HandUpdateAssetHandler(BaseHandler):
    _thread_pool = ThreadPoolExecutor(1)

    @run_on_executor(executor='_thread_pool')
    def asset_update(self, id_list):
        with DBContext('r', None, True) as session:
            for i in id_list:
                server_list = session.query(Server.ip, Server.port, AdminUser.system_user,
                                            AdminUser.user_key, Server.state).outerjoin(AdminUser,
                                                                                        AdminUser.admin_user == Server.admin_user).filter(
                    Server.id == i).all()
                ins_log.read_log('info', '手动触发更新资产')
                rsync_sucess_list = rsync_public_key(server_list)
                if rsync_sucess_list:
                    asset_data = get_server_sysinfo(server_list)
                    ins_log.read_log('info', '资产信息：{}'.format(asset_data))
                    update_asset(asset_data)

    @gen.coroutine
    def post(self, *args, **kwargs):
        data = json.loads(self.request.body.decode("utf-8"))
        id_list = data.get('id_list', None)
        if not id_list:
            return self.write(dict(code=1, msg='关键参数不能为空'))

        try:
            yield gen.with_timeout(datetime.timedelta(seconds=120), [self.asset_update(id_list)],
                                   quiet_exceptions=tornado.gen.TimeoutError)
        except gen.TimeoutError:
            return self.write(dict(code=-2, msg='TimeOut'))
        return self.write(dict(code=0, msg='任务执行完成，提醒： 完成状态为：True, 错误状态：False， False状态下可点击查看日志进行排错'))


asset_hand_server_urls = [
    (r"/v1/cmdb/server/asset_update/", HandUpdateAssetHandler)
]
