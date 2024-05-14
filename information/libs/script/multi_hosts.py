#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:test
# datetime:2023-5-26
# software: PyCharm



import json
import requests


def add_host():
    add_user_url = 'https://codo.domain.com/api/cmdb2/v1/cmdb/server/'
    csrf_task_url = 'https://codo.domain.com/api/task/v2/task/accept/'

    auth_key = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9nVzZXJuYW1lIjoieWFuZ2gFPLN6g"

    the_body = json.dumps({
        "hostname": 'hostname',
        "ip": "1.1.1.1",
        "port": "22",
        "public_ip": "2.2.2.2",
        "idc": "AWS",
        "admin_user": "root",
        "region": "us-east-1",
    })

    req1 = requests.get(csrf_task_url, cookies=dict(auth_key=auth_key))
    csrf_key = json.loads(req1.text)['csrf_key']
    cookies = dict(auth_key=auth_key, csrf_key=csrf_key)
    req = requests.post(add_user_url, data=the_body, cookies=cookies)
    req_code = json.loads(req.text)['code']
    if req_code != 0:
        print(json.loads(req.text)['msg'])
        exit(-111)
    else:
        print(json.loads(req.text)['msg'])


if __name__ == '__main__':
    add_host()
