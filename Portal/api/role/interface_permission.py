#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:test
# datetime:2020-12-2
# software: PyCharm



from flask import request
from flask_restful import Resource

from common.common_login_helper import login_required
from common.common_model_enum import modelEnum
from common.common_response_code import response_code
from common.common_response_process import response_result_process
from core.role_permission_singleton import role_permission_singleton

from utils.api_version_verify import api_version
from utils.log_helper import lg


class interfacePermission(Resource):
    @api_version
    @login_required
    def get(self, version):
        xml = request.args.get('format')
        try:
            body = modelEnum.permission.value.get('body')
            data = role_permission_singleton.get_user_permission_info()
            return response_result_process(data, xml_structure_str=body, xml=xml)
        except Exception as e:
            lg.error(e)
            error_data = response_code.GET_DATA_FAIL
            return response_result_process(error_data, xml=xml)