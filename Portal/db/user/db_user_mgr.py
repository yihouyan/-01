#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:test
# datetime:2021-7-27
# software: PyCharm



from common.common_time import get_system_datetime
from db.base import DbBase
from db.connection_pool import MysqlConn
from utils.log_helper import lg
import copy

from utils.status_code import response_code
from config import configuration

from werkzeug.security import generate_password_hash, check_password_hash


class DbUserMgr(DbBase):
    """
    用户相关数据库表操作类
    """

    def get_user_list(self, current_page, page_size, search_data=None):
        """
        获取用户列表
        :return:
        """
        conn = MysqlConn()
        try:
            start_num = (current_page - 1) * page_size
            condition = None
            search_condition = search_data
            if search_condition:
                for key in search_condition.keys():
                    condition = key + ' like "%' + search_condition[key] + '%"'
            db_name = configuration.get_database_name()
            fields = ("users.id,users.user_name,users.email,users.phone,users.position,"
                      "users.login_name,users.user_sex,users.create_time")
            sql_count, sql = self.create_get_page_sql(db_name, 'users', fields, start_num, page_size,
                                                      condition=condition)
            users_result = self.execute_fetch_pages(conn, sql_count, sql, current_page, page_size)
            users = copy.deepcopy(users_result["data_list"])
            if users:
                for user in users_result["data_list"]:
                    user_id = user["id"]
                    role_relations = [{"table_name": "user_roles", "join_condition": "user_roles.role_id=role.id"}]
                    condition = "user_roles.user_id=" + str(user_id)
                    role_name_query_sql = self.create_get_relation_sql(db_name, "role", "name", role_relations,
                                                                       condition=condition)

                    roles = self.execute_fetch_all(conn, role_name_query_sql)
                    role_name_str = ''
                    if len(roles) == 0:
                        pass
                    elif len(roles) == 1:
                        role_name_str = roles[0]["name"]
                    else:
                        for role in roles:
                            role_name_str += role["name"] + '|'
                    user["roles"] = role_name_str.rstrip('|')
                    group_relations = [
                        {"table_name": "user_user_group", "join_condition": "user_user_group.group_id=user_group.id"}]
                    condition = "user_user_group.user_id=" + str(user_id)
                    group_name_query_sql = self.create_get_relation_sql(db_name, "user_group", "name", group_relations,
                                                                        condition=condition)

                    groups = self.execute_fetch_all(conn, group_name_query_sql)
                    group_name_str = ''
                    if len(groups) == 0:
                        pass
                    elif len(groups) == 1:
                        group_name_str = groups[0]["name"]
                    else:
                        for group in groups:
                            group_name_str += group["name"] + '|'
                    user["groups"] = group_name_str.rstrip('|')
                    department_relations = [
                        {"table_name": "users_department", "join_condition": "users_department.dpt_id=department.id"}]
                    condition = "users_department.user_id=" + str(user_id)
                    department_name_query_sql = self.create_get_relation_sql(db_name, "department", "name",
                                                                             department_relations,
                                                                             condition=condition)

                    departments = self.execute_fetch_all(conn, department_name_query_sql)
                    department_name_str = ''
                    if len(departments) == 0:
                        pass
                    elif len(departments) == 1:
                        department_name_str = departments[0]["name"]
                    else:
                        for department in departments:
                            department_name_str += department["name"] + '|'
                    user["departments"] = department_name_str.rstrip('|')
            data = response_code.SUCCESS
            data["data"] = users_result.get('data_list')
            data["total"] = users_result.get('total_count')
            return data
        except Exception as e:
            lg.error(e)
            return response_code.GET_DATA_FAIL
        finally:
            conn.close()

    def get_all_user(self):
        """
        查询所有用户
        :return:
        """
        db_conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()
            table_name = 'users'
            fields = 'id,user_name,user_sex,email,phone,position,note_info,login_name'
            sql = self.create_select_sql(db_name, table_name, fields)
            result = self.execute_fetch_all(db_conn, sql)
            data = response_code.SUCCESS
            data['data'] = result
            return data
        except Exception as e:
            lg.error(e)
            return response_code.GET_DATA_FAIL
        finally:
            db_conn.close()

    def get_user_by_id(self, id):
        """
        通过id获取用户
        :return:
        """
        conn = MysqlConn()
        try:
            condition = "id='%s'" % id
            db_name = configuration.get_database_name()
            sql = self.create_select_sql(db_name, 'users', '*', condition=condition)
            return self.execute_fetch_one(conn, sql)
        except Exception as e:
            lg.error(e)
            return response_code.GET_DATA_FAIL
        finally:
            conn.close()

    def get_user_by_id_(self, id):
        """
        给前端使用的通过id获取用户
        :return:
        """
        conn = MysqlConn()
        try:
            condition = 'id=%s' % id
            db_name = configuration.get_database_name()
            fields = 'id,user_name,user_sex,email,phone,position,note_info,login_name,create_time'
            sql = self.create_select_sql(db_name, 'users', fields, condition=condition)
            data = response_code.SUCCESS
            data['data'] = self.execute_fetch_one(conn, sql)
            return data
        except Exception as e:
            lg.error(e)
            return response_code.GET_DATA_FAIL
        finally:
            conn.close()

    def get_user_by_ids(self, ids_tuple):
        """
        通过id元组获取用户
        :return:
        """
        conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()
            if len(ids_tuple) == 1:
                condition = 'id=%s' % ids_tuple[0]
            else:
                condition = 'id in %s' % str(ids_tuple)
            fields = 'id,user_name,user_sex,email,phone,position,note_info,login_name'
            sql = self.create_select_sql(db_name, 'users', fields, condition=condition)
            return self.execute_fetch_all(conn, sql)
        except Exception as e:
            lg.error(e)
            return response_code.GET_DATA_FAIL
        finally:
            conn.close()

    def get_user_by_name(self, name):
        """
        通过name获取用户
        :param name:
        :return:
        """
        conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()
            condition = 'user_name="%s"' % name
            user_fields = 'id,user_name,user_sex,email,pass_word,phone,position,create_time,note_info,login_name,icon'
            sql = self.create_select_sql(db_name, 'users', user_fields, condition=condition)
            user_info = self.execute_fetch_one(conn, sql)
            if user_info is None:
                return response_code.USER_NOT_EXIST
            user_id = user_info.get('id')

            role_relations = [{"table_name": "user_roles", "join_condition": "user_roles.role_id=role.id"}]
            condition = "user_roles.user_id=" + str(user_id)
            role_query_sql = self.create_get_relation_sql(db_name, "role", "role.id,role.name", role_relations,
                                                          condition=condition)
            roles = self.execute_fetch_all(conn, role_query_sql)
            user_info['roles'] = roles
            group_relations = [
                {"table_name": "user_user_group", "join_condition": "user_user_group.group_id=user_group.id"}]
            condition = "user_user_group.user_id=" + str(user_id)
            group_query_sql = self.create_get_relation_sql(db_name, "user_group", "user_group.id,user_group.name",
                                                           group_relations, condition=condition)
            groups = self.execute_fetch_all(conn, group_query_sql)
            user_info['groups'] = groups
            department_relations = [
                {"table_name": "users_department", "join_condition": "users_department.dpt_id=department.dpt_id"}]
            condition = "users_department.user_id=" + str(user_id)
            department_query_sql = self.create_get_relation_sql(db_name, "department",
                                                                "department.dpt_id,department.dpt_name",
                                                                department_relations, condition=condition)
            departments = self.execute_fetch_all(conn, department_query_sql)
            user_info['departments'] = departments
            permissions_id_set = set()
            if roles:
                for role in roles:
                    role_relations = [{"table_name": "roles_permission",
                                       "join_condition": "roles_permission.permission_id=permission.id"}]
                    condition = "roles_permission.role_id=" + str(role.get('id'))
                    permission_id_query_sql = self.create_get_relation_sql(db_name, "permission", "permission.id",
                                                                           role_relations, condition=condition)
                    permission_ids = self.execute_fetch_all(conn, permission_id_query_sql)
                    if permission_ids:
                        for permission_id in permission_ids:
                            permissions_id_set.add(permission_id['id'])
            permissions = []
            if permissions_id_set:
                for permission_id in permissions_id_set:
                    condition = 'id=%s' % permission_id
                    permission_sql = self.create_select_sql(db_name, 'permission', 'id,name', condition=condition)
                    permission = self.execute_fetch_one(conn, permission_sql)
                    permissions.append(permission)
            user_info['permissions'] = permissions
            menus = []
            if permissions_id_set:
                for permission_id in permissions_id_set:
                    menu_permission_relations = [
                        {"table_name": "permission_menu", "join_condition": "permission_menu.meun_id=menu.id"}]
                    condition = "permission_menu.permission_id=" + str(permission_id)
                    menu_fields = ("menu.id as menu_id,menu.name as menu_name,menu.url as menu_url,"
                                   "menu.icon as menu_icon,menu.sort as menu_sort,menu.p_id as menu_p_id,"
                                   "menu.is_router as isRouter,menu.router_parent as routerParent")
                    menu_query_sql = self.create_get_relation_sql(db_name, "menu", menu_fields,
                                                                  menu_permission_relations, condition=condition)
                    menu = self.execute_fetch_one(conn, menu_query_sql)
                    if menu:
                        menus.append(menu)
            user_info['menus_list'] = menus
            data = response_code.SUCCESS
            data['data'] = user_info
            return data
        except Exception as e:
            lg.error(e)
            return response_code.GET_DATA_FAIL
        finally:
            conn.close()

    def get_user(self, **kwargs):
        """
        条件查询用户
        :param kwargs:
        :return:
        """
        conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()
            condition = ''
            for key in kwargs.keys():
                if type(kwargs[key]) == int:
                    condition = '%s=%s' % (key, kwargs[key])
                else:
                    condition = '%s="%s"' % (key, kwargs[key])
            sql = self.create_select_sql(db_name, 'users', '*', condition=condition)
            return self.execute_fetch_one(conn, sql)
        except Exception as e:
            lg.error(e)
            return response_code.GET_DATA_FAIL
        finally:
            conn.close()

    def add_user(self, user):
        """
        添加用户
        :return:
        """
        conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()

            if_user = self.get_user(user_name=user['user_name'])
            if if_user:
                data = response_code.RECORD_EXIST
                return data
            fields = '(user_name,user_sex,email,pass_word,phone,position,create_time,note_info,login_name,icon)'
            create_time = get_system_datetime()
            pass_word = generate_password_hash('123456')
            value_tuple = (user['user_name'], user['user_sex'], user['email'], pass_word, user['phone'],
                           user['position'], create_time, user['note_info'], user['login_name'], user['icon'])
            insert_user_sql = self.create_insert_sql(db_name, 'users', fields, value_tuple)
            self.insert_exec(conn, insert_user_sql)
            new_user = self.get_user(user_name=user['user_name'])
            for dpt_id in eval(str(user['dpt_ids'])):
                insert_users_department_sql = self.create_insert_sql(db_name, 'users_department', '(user_id,dpt_id)',
                                                                     (new_user['ID'], dpt_id))
                self.insert_exec(conn, insert_users_department_sql)
            for group_id in eval(str(user['group_ids'])):
                insert_users_group_sql = self.create_insert_sql(db_name, 'user_user_group', '(user_id,group_id)',
                                                                (new_user['ID'], group_id))
                self.insert_exec(conn, insert_users_group_sql)
            for role_id in eval(str(user['role_ids'])):
                insert_users_role_sql = self.create_insert_sql(db_name, 'user_roles', '(user_id,role_id)',
                                                               (new_user['ID'], role_id))
                self.insert_exec(conn, insert_users_role_sql)
            data = response_code.SUCCESS
            return data
        except Exception as e:
            lg.error(e)
            conn.conn.rollback()
            return response_code.ADD_DATA_FAIL
        finally:
            conn.close()

    def del_user(self, ids):
        """
        删除指定用户
        :param id:
        :return:
        """
        conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()
            for id in eval(str(ids)):
                delete_role_condition = 'user_id=%s' % id
                delete_user_role_sql = self.create_delete_sql(db_name, 'user_roles',
                                                              delete_role_condition)
                self.delete_exec(conn, delete_user_role_sql)
                delete_department_condition = 'user_id=%s' % id
                delete_user_department_sql = self.create_delete_sql(db_name, 'users_department',
                                                                    delete_department_condition)
                self.delete_exec(conn, delete_user_department_sql)
                delete_group_condition = 'user_id=%s' % id
                delete_group_sql = self.create_delete_sql(db_name, 'user_user_group',
                                                          delete_group_condition)
                self.delete_exec(conn, delete_group_sql)
                delete_task_group_condition = 'user_id=%s' % id
                delete_task_group_sql = self.create_delete_sql(db_name, 'user_task_group',
                                                               delete_task_group_condition)
                self.delete_exec(conn, delete_task_group_sql)

                delete_user_condition = 'id=%s' % id
                delete_user_sql = self.create_delete_sql(db_name, 'users',
                                                         delete_user_condition)
                self.delete_exec(conn, delete_user_sql)

            data = response_code.SUCCESS
            return data
        except Exception as e:
            lg.error(e)
            return response_code.DELETE_DATA_FAIL
        finally:
            conn.close()

    def upd_user(self, user_json):
        """
        更新用户信息
        :param user:user json
        :return:
        """
        conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()
            user = user_json
            user_id = user.get('user_id')
            condition = 'id=%s' % user_id
            update_user_fields = ['user_name', 'user_sex', 'email', 'phone', 'position', 'note_info', 'login_name',
                                  'icon']
            update_user_fields_value = [user.get('user_name'), user.get('user_sex'), user.get('email'),
                                        user.get('phone'),
                                        user.get('position'), user.get('note_info'), user.get('login_name'),
                                        user.get('icon')]
            update_user_sql = self.create_update_sql(db_name, 'users', update_user_fields, update_user_fields_value,
                                                     condition)
            self.updete_exec(conn, update_user_sql)
            delete_role_condition = 'user_id=%s' % user_id
            delete_user_role_sql = self.create_delete_sql(db_name, 'user_roles',
                                                          delete_role_condition)
            self.delete_exec(conn, delete_user_role_sql)
            delete_department_condition = 'user_id=%s' % user_id
            delete_user_department_sql = self.create_delete_sql(db_name, 'users_department',
                                                                delete_department_condition)
            self.delete_exec(conn, delete_user_department_sql)
            delete_group_condition = 'user_id=%s' % user_id
            delete_group_sql = self.create_delete_sql(db_name, 'user_user_group',
                                                      delete_group_condition)
            self.delete_exec(conn, delete_group_sql)
            for dpt_id in eval(str(user['dpt_ids'])):
                insert_users_department_sql = self.create_insert_sql(db_name, 'users_department', '(user_id,dpt_id)',
                                                                     (user_id, dpt_id))
                self.insert_exec(conn, insert_users_department_sql)
            for group_id in eval(str(user['group_ids'])):
                insert_users_group_sql = self.create_insert_sql(db_name, 'user_user_group', '(user_id,group_id)',
                                                                (user_id, group_id))
                self.insert_exec(conn, insert_users_group_sql)
            for role_id in eval(str(user['role_ids'])):
                insert_users_role_sql = self.create_insert_sql(db_name, 'user_roles', '(user_id,role_id)',
                                                               (user_id, role_id))
                self.insert_exec(conn, insert_users_role_sql)
            data = response_code.SUCCESS
            return data
        except Exception as e:
            lg.error(e)
            return response_code.UPDATE_DATA_FAIL
        finally:
            conn.close()

    def upd_user_partial(self, user_json):
        """
        更新用户部分指定信息
        :param user_json:
        :return:
        """
        conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()
            user = user_json
            user_id = user.get('user_id')
            condition = 'id=%s' % user_id
            update_user_fields = ['user_name', 'email', 'phone', 'login_name']
            update_user_fields_value = [user.get('user_name'), user.get('email'), user.get('phone'),
                                        user.get('login_name')]
            update_user_sql = self.create_update_sql(db_name, 'users', update_user_fields, update_user_fields_value,
                                                     condition)
            self.updete_exec(conn, update_user_sql)
            data = response_code.SUCCESS
            return data
        except Exception as e:
            lg.error(e)
            return response_code.UPDATE_DATA_FAIL
        finally:
            conn.close()

    def pwd_modify(self, user_id, old_pwd, new_pwd):
        '''
        修改用户密码
        :return:
        '''
        conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()
            condition = 'id=%s' % user_id
            user_pwd_sql = self.create_select_sql(db_name, 'users', 'pass_word', condition)
            pwd_result = self.execute_fetch_one(conn, user_pwd_sql)
            if not check_password_hash(pwd_result.get('pass_word'), old_pwd):
                return response_code.LOGIN_IS_FAIL
            new_pass_word_hash = generate_password_hash(new_pwd)
            update_pwd_sql = self.create_update_sql(db_name, 'users', ['pass_word'], [new_pass_word_hash], condition)
            self.updete_exec(conn, update_pwd_sql)
            data = response_code.SUCCESS
            return data
        except Exception as e:
            lg.error(e)
            return response_code.UPDATE_DATA_FAIL
        finally:
            conn.close()

    def pwd_reset(self, user_ids):
        '''
        重置用户密码
        :return:
        '''
        conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()
            pass_word = generate_password_hash('123456')
            for user_id in eval(str(user_ids)):
                condition = 'id=%s' % user_id
                update_user_sql = self.create_update_sql(db_name, 'users', ['pass_word'], [pass_word], condition)
                self.updete_exec(conn, update_user_sql)
            data = response_code.SUCCESS
            return data
        except Exception as e:
            lg.error(e)
            return response_code.PASS_WORD_RESET_FAIL
        finally:
            conn.close()


user_mgr = DbUserMgr()
