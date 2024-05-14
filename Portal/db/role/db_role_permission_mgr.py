#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:test
# datetime:2024-7-8
# software: PyCharm



import json

from common.common_time import get_system_datetime
from config import configuration
from db.base import DbBase
from db.connection_pool import MysqlConn

from utils.log_helper import lg
from utils.status_code import response_code


class DbRolePermissionMgr(DbBase):
    def get_user_permission_info(self):
        """
        获取所有的普通权限信息
        :return:
        """
        db_conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()
            table_name = 'permission'
            condition = 'permission_type=0 or permission_type=3'
            per_fields = 'id,name,create_time,p_id,permission_type'
            sql = self.create_select_sql(db_name, table_name, per_fields, condition)
            result = self.execute_fetch_all(db_conn, sql)
            data = response_code.SUCCESS
            data['data'] = result
            return data
        except Exception as e:
            lg.error(e)
            return response_code.GET_DATA_FAIL
        finally:
            db_conn.close()

    def get_data_permission_info(self):
        """
        获取所有的数据权限信息
        :return:
        """
        db_conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()
            table_name = 'permission'
            condition = 'permission_type=1'
            per_fields = 'id,name,create_time,p_id,permission_type'
            sql = self.create_select_sql(db_name, table_name, per_fields, condition)
            result = self.execute_fetch_all(db_conn, sql)
            data = response_code.SUCCESS
            data['data'] = result
            return data
        except Exception as e:
            lg.error(e)
            return response_code.GET_DATA_FAIL
        finally:
            db_conn.close()

    def get_all_roles(self):
        """
        获取所有的角色信息
        :return:
        """
        db_conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()
            table_name = 'role'
            role_fields = 'id,name,create_time,note_info,time_modify'
            sql = self.create_select_sql(db_name, table_name, role_fields)
            result = self.execute_fetch_all(db_conn, sql)
            data = response_code.SUCCESS
            data['data'] = result
            return data
        except Exception as e:
            lg.error(e)
            return response_code.GET_DATA_FAIL
        finally:
            db_conn.close()

    def get_pages_roles(self, current_page, page_size, search_data):
        """
        获取所有的角色信息
        :return:
        """
        db_conn = MysqlConn()
        try:
            start_num = (current_page - 1) * page_size
            db_name = configuration.get_database_name()
            table_name = 'role'
            param = search_data
            role_fields = 'id,name,create_time,note_info,time_modify'
            if param == {} or param == '':
                sql_count, sql = self.create_get_page_sql(db_name, table_name, role_fields, start_num, page_size)
            else:
                condition = None
                for key, value in param.items():
                    condition = "  %s like '%%%s%%'" % (key, value)
                sql_count, sql = self.create_get_page_sql(db_name, table_name, role_fields, start_num, page_size,
                                                          condition)


            result = self.execute_fetch_pages(db_conn, sql_count, sql, current_page, page_size)
            data = response_code.SUCCESS
            data["data"] = result.get('data_list')
            data["total"] = result.get('total_count')
            return data
        except Exception as e:
            lg.error(e)
            return response_code.GET_DATA_FAIL
        finally:
            db_conn.close()

    def add_role(self, role_name, note_info):
        """
        添加角色
        :param role_name: 角色名称
        :param note_info: 备注信息
        :return:
        """
        db_conn = MysqlConn()
        try:
            create_time = get_system_datetime()
            db_name = configuration.get_database_name()
            table_name = 'role'
            filed = 'name'
            condition = "name = '%s'" % role_name
            system_name_sql = self.create_select_sql(db_name, table_name, filed, condition)
            res = self.execute_fetch_one(db_conn, system_name_sql)
            if res:
                return response_code.RECORD_EXIST
            else:
                fields = '(name, create_time,note_info)'
                insert_data = (role_name, create_time, note_info)
                sql = self.create_insert_sql(db_name, table_name, fields, insert_data)
                self.execute_sql_return_count(db_conn, sql)
                return response_code.SUCCESS
        except Exception as e:
            lg.error(e)
            error_data = response_code.ADD_DATA_FAIL
            return error_data
        finally:
            db_conn.close()

    def update_role(self, role_id, role_name, note_info):
        """
        修改角色
        :param role_id: 角色ID
        :param role_name: 角色名称
        :param note_info: 备注信息
        :return:
        """
        db_conn = MysqlConn()
        try:
            time_modify = get_system_datetime()
            db_name = configuration.get_database_name()
            table_name = 'role'
            filed = 'name'
            condition = "id <> %s and name = '%s'" % (role_id, role_name)
            old_sql = self.create_select_sql(db_name, table_name, filed, condition)
            old_pla_name_data = self.execute_fetch_one(db_conn, old_sql)
            if old_pla_name_data:
                return response_code.RECORD_EXIST
            else:
                fields = ['id', 'name', 'note_info', 'time_modify']
                pla_data = [role_id, role_name, note_info, time_modify]
                update_condition = 'id = %s' % str(role_id)
                update_sql = self.create_update_sql(db_name, table_name, fields, pla_data, update_condition)
                self.execute_update_sql(db_conn, update_sql)
                return response_code.SUCCESS
        except Exception as  e:
            lg.error(e)
            return response_code.UPDATE_DATA_FAIL
        finally:
            db_conn.close()

    def delete_role(self, role_id):
        """
        删除角色
        :param role_id:
        :return:
        """
        db_conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()
            table_name = "role"
            role_per_table = "roles_permission"
            user_group_role_table = "user_group_role"
            user_role_table = "user_roles"

            filed = 'role_id'
            condition = "role_id = %s " % role_id
            role_per_sql = self.create_select_sql(db_name, role_per_table, filed, condition)
            role_per_data = self.execute_fetch_one(db_conn, role_per_sql)
            if role_per_data:
                condition = "role_id=%s" % role_per_data.get('role_id')
                del_association_sql = self.create_delete_sql(db_name, role_per_table, condition)
                self.execute_del_data(db_conn, del_association_sql)

            user_group_role_sql = self.create_select_sql(db_name, user_group_role_table, filed, condition)
            user_group_role_data = self.execute_fetch_one(db_conn, user_group_role_sql)
            if user_group_role_data:
                condition = "role_id=%s" % user_group_role_data.get('role_id')
                del_association_sql = self.create_delete_sql(db_name, user_group_role_table, condition)
                self.execute_del_data(db_conn, del_association_sql)

            user_role_sql = self.create_select_sql(db_name, user_role_table, filed, condition)
            user_role_data = self.execute_fetch_one(db_conn, user_role_sql)
            if user_role_data:
                condition = "role_id=%s" % user_role_data.get('role_id')
                del_association_sql = self.create_delete_sql(db_name, user_role_table, condition)
                self.execute_del_data(db_conn, del_association_sql)

            condition = "id=%s" % role_id
            sql = self.create_delete_sql(db_name, table_name, condition)
            self.execute_del_data(db_conn, sql)
            return response_code.SUCCESS
        except Exception as e:
            lg.error(e)
            return response_code.DELETE_DATA_FAIL
        finally:
            db_conn.close()

    def add_role_permission(self, role_id, per_keys):
        """
        给角色添加权限
        :param role_id: 角色id
        :param per_keys: 权限列表
        :return:
        """
        db_conn = MysqlConn()
        try:

            db_name = configuration.get_database_name()
            table_name = 'roles_permission'
            filed = 'role_id'
            condition = " role_id = '%s'" % role_id

            old_role_sql = DbBase.create_select_sql(self, db_name, table_name, filed, condition)
            old_role_id_data = DbBase.execute_fetch_one(self, db_conn, old_role_sql)
            if old_role_id_data:
                condition = "role_id=%s" % old_role_id_data.get('role_id')
                del_association_sql = self.create_delete_sql(db_name, table_name, condition)
                self.execute_del_data(db_conn, del_association_sql)
            for per_key in eval(per_keys):
                fields = '(role_id, permission_id)'
                pla_data = (role_id, per_key)
                sql = DbBase.create_insert_sql(self, db_name, table_name, fields, pla_data)
                DbBase.execute_sql_return_count(self, db_conn, sql)
            return response_code.SUCCESS
        except Exception as  e:
            lg.error(e)
            return response_code.ADD_DATA_FAIL
        finally:
            db_conn.close()

    def get_role_permission_info(self, role_id):
        """
        根据角色ID获取权限列表
        :param role_id: 角色ID
        :return:
        """
        db_conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()
            table_name = 'roles_permission'

            condition = 'role_id=%s' % role_id
            sql = DbBase.create_select_sql(self, db_name, table_name, 'permission_id', condition)
            result = DbBase.execute_fetch_all(self, db_conn, sql)
            permission_ids = [permission.get('permission_id') for permission in result]
            if len(permission_ids) != 0:
                permission_table = 'permission'
                if len(permission_ids) == 1:
                    condition = 'id = %s' % permission_ids
                else:
                    condition = 'id in %s' % str(tuple(permission_ids))
                per_p_sql = DbBase.create_select_sql(self, db_name, permission_table, 'p_id', condition)
                result = DbBase.execute_fetch_all(self, db_conn, per_p_sql)
                permission_p_ids = [permission.get('p_id') for permission in result]
                result = list(set(permission_ids).difference(set(permission_p_ids)))
            data = response_code.SUCCESS
            data['data'] = result
            return data
        except Exception as e:
            lg.error(e)
            return response_code.GET_DATA_FAIL
        finally:
            db_conn.close()

    def add_grafana_permission(self, param):
        """
        添加grafana权限
        :param param:
        :return:
        """
        db_conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()
            param_data = json.loads(param)

            condition = "p_id = 85"
            old_sql = self.create_select_sql(db_name, 'permission', 'grafana_id', condition)
            old_data = self.execute_fetch_all(db_conn, old_sql)
            old_grafana_ids = [i.get('grafana_id') for i in old_data]

            parent_ids, children_data, parent_insert_data = [], [], []

            for para in param_data:
                if para.get('type') == 'dash-folder':
                    grafana_id = para.get('id')
                    name = para.get('title')
                    parent_ids.append(grafana_id)
                    parent_insert_data.append(
                        {'grafana_id': grafana_id, 'name': name, 'p_id': 85, 'permission_type': 3})
                else:
                    grafana_id = para.get('id')
                    parent_id = para.get('folderId')
                    children_data.append({'grafana_id': grafana_id, 'parent_id': parent_id})

            for grafana_id in old_grafana_ids:
                if grafana_id in parent_ids:
                    pass
                else:
                    condition = "grafana_id= %s" % grafana_id

                    old_sql = self.create_select_sql(db_name, 'permission', 'id', condition)
                    old_data = self.execute_fetch_all(db_conn, old_sql)
                    for old in old_data:
                        old_condition = 'permission_id = %s' % old.get('id')
                        sql = self.create_delete_sql(db_name, 'grafana_permission', old_condition)
                        self.execute_del_data(db_conn, sql)

                        old_condition = 'permission_id = %s' % old.get('id')
                        sql = self.create_delete_sql(db_name, 'roles_permission', old_condition)
                        self.execute_del_data(db_conn, sql)
                    sql = self.create_delete_sql(db_name, 'permission', condition)
                    self.execute_del_data(db_conn, sql)

            for grafana in parent_insert_data:
                grafana_id = grafana.get('grafana_id')
                if grafana_id in old_grafana_ids:
                    pass
                else:
                    sql = self.insert_sql(db_name, 'permission', grafana)
                    self.execute_sql_return_count(db_conn, sql)

            gr_id_condition = "grafana_id <> 0 "
            per_sql = self.create_select_sql(db_name, 'permission', 'grafana_id,id', gr_id_condition)
            per_data = self.execute_fetch_all(db_conn, per_sql)
            for children in children_data:
                parent_id = children.get('parent_id')
                grafana_id = children.get('grafana_id')
                for per in per_data:
                    if parent_id == per.get('grafana_id'):
                        permission_id = per.get('id')
                        children['permission_id'] = permission_id
                        is_exist = 'grafana_id = %s and parent_id=%s and permission_id = %s' % (
                            grafana_id, parent_id, permission_id)
                        old_sql = self.create_select_sql(db_name, 'grafana_permission',
                                                         'grafana_id,parent_id,permission_id', is_exist)
                        old_data = self.execute_fetch_all(db_conn, old_sql)
                        if not old_data:
                            sql = self.insert_sql(db_name, 'grafana_permission', children)
                            self.execute_sql_return_count(db_conn, sql)
            return response_code.SUCCESS
        except Exception as e:
            lg.error(e)
            return response_code.ADD_DATA_FAIL
        finally:
            db_conn.close()

    def get_grafana_permission(self, user_id):
        """

        :param user_id:
        :return:
        """
        db_conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()
            condition = 'user_id = %s' % user_id
            role_sql = self.create_select_sql(db_name, 'user_roles', 'role_id', condition)
            role_data = self.execute_fetch_all(db_conn, role_sql)
            permission_ids = []
            for role in role_data:
                per_condition = 'role_id = %s' % role.get('role_id')
                per_sql = self.create_select_sql(db_name, 'roles_permission', 'permission_id', per_condition)
                per_data = self.execute_fetch_all(db_conn, per_sql)
                permission_ids += per_data
            gra_ids = []
            for per in permission_ids:
                gr_condition = 'id = %s and permission_type = 3 and grafana_id <> 0' % per.get('permission_id')
                gr_sql = self.create_select_sql(db_name, 'permission', 'grafana_id', gr_condition)
                gr_data = self.execute_fetch_one(db_conn, gr_sql)
                if gr_data:
                    gra_ids.append(gr_data)
            data = response_code.SUCCESS
            gra_id = [i.get("grafana_id") for i in gra_ids]
            data['data'] = gra_id
            return data
        except Exception as e:
            lg.error(e)
            return response_code.GET_DATA_FAIL
        finally:
            db_conn.close()


db_role_permission = DbRolePermissionMgr()
