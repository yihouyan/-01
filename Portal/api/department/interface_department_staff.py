#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:test
# datetime:2021-5-21
# software: PyCharm



from flask import request
from flask_restful import Resource

from common.common_login_helper import login_required
from common.common_model_enum import modelEnum
from common.common_request_process import req
from common.common_response_code import response_code
from common.common_response_process import response_result_process
from core.department_singleton import department_singleton

from utils.api_version_verify import api_version
from utils.log_helper import lg


class interfaceDepartmentStaff(Resource):
    @api_version
    @login_required
    def get(self, version, dpt_id=None):
        xml = request.args.get('format')
        try:
            if dpt_id is None:
                data = response_code.NOT_FOUND
                return response_result_process(data, xml=xml)

            request_data = req.request_process(request, xml, modelEnum.department.value)
            if isinstance(request_data, bool):
                request_data = response_code.REQUEST_PARAM_FORMAT_ERROR
                return response_result_process(request_data, xml=xml)
            if not request_data:
                data = response_code.REQUEST_PARAM_MISSED
                return response_result_process(data, xml=xml)
            fields = ['current_page', 'page_size']
            must = req.verify_all_param_must(request_data, fields)
            if must:
                return response_result_process(must, xml=xml)
            par_type = {'page_size': int, 'current_page': int}
            param_type = req.verify_all_param_type(request_data, par_type)
            if param_type:
                return response_result_process(param_type, xml=xml)

            current_page, page_size = int(request_data.get('current_page')), int(request_data.get('page_size'))
            data = department_singleton.get_dpt_user_info_by_id(dpt_id, current_page, page_size)
            body = modelEnum.department.value.get('body')
            return response_result_process(data, xml_structure_str=body, xml=xml)
        except Exception as e:
            lg.error(e)
            error_data = response_code.GET_DATA_FAIL
            return response_result_process(error_data, xml=xml)

    @api_version
    @login_required
    def post(self, version, dpt_id=None):
        xml = request.args.get('format')
        try:
            if dpt_id is None:
                data = response_code.NOT_FOUND
                return response_result_process(data, xml=xml)
            request_data = req.request_process(request, xml, modelEnum.department.value)
            if isinstance(request_data, bool):
                request_data = response_code.REQUEST_PARAM_FORMAT_ERROR
                return response_result_process(request_data, xml=xml)
            if not request_data:
                data = response_code.REQUEST_PARAM_MISSED
                return response_result_process(data, xml=xml)
            fields = ['user_ids']
            must = req.verify_all_param_must(request_data, fields)
            if must:
                return response_result_process(must, xml=xml)
            par_type = {'user_ids': list}
            param_type = req.verify_all_param_type(request_data, par_type)
            if param_type:
                return response_result_process(param_type, xml=xml)
            user_ids = str(request_data.get('user_ids'))
            data = department_singleton.department_add_staff(dpt_id, user_ids)
            return response_result_process(data, xml=xml)
        except Exception as e:
            lg.error(e)
            error_data = response_code.ADD_DATA_FAIL
            return response_result_process(error_data, xml=xml)

    @api_version
    @login_required
    def delete(self, version, dpt_id=None):
        xml = request.args.get('format')
        try:
            if dpt_id is None:
                data = response_code.NOT_FOUND
                return response_result_process(data, xml=xml)
            request_data = req.request_process(request, xml, modelEnum.department.value)
            if isinstance(request_data, bool):
                request_data = response_code.REQUEST_PARAM_FORMAT_ERROR
                return response_result_process(request_data, xml=xml)
            if not request_data:
                data = response_code.REQUEST_PARAM_MISSED
                return response_result_process(data, xml=xml)
            fields = ['user_ids']
            must = req.verify_all_param_must(request_data, fields)
            if must:
                return response_result_process(must, xml=xml)
            par_type = {'user_ids': list}
            param_type = req.verify_all_param_type(request_data, par_type)
            if param_type:
                return response_result_process(param_type, xml=xml)
            user_ids = str(request_data.get('user_ids'))

            data = department_singleton.delete_department_staff(dpt_id, user_ids)
            return response_result_process(data, xml=xml)

        except Exception as e:
            lg.error(e)
            error_data = response_code.DELETE_DATA_FAIL
            return response_result_process(error_data, xml=xml)
