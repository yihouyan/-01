#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:test
# datetime:2021-5-2
# software: PyCharm




from libs.ansibleAPI.runner import Runner
from libs.common import M2human


def get_host_info(server_list):
    if not isinstance(server_list, list):
        raise ValueError()

    for host in server_list:
        ip = host[0]
        user = host[2]
        host_dict = {
            "host": host[0],
            "port": host[1],
            "user": host[2],
        }

        runner = Runner(
            module_name="setup",
            module_args="",
            remote_user=user,
            pattern="all",
            hosts=host_dict,
            timeout=10,

        )

        result = runner.run()

        if result['dark']:
            msg = {
                ip: {
                    'status': False,
                    'msg': result['dark'][ip]['msg']
                }
            }
            return msg

        else:
            asset_data = {
                ip: {
                    'status': True,
                    'msg': '获取资产成功',
                }
            }  # ip为key 数据为value
            try:
                sn = result['contacted'][ip]['ansible_facts']['ansible_product_serial']
            except KeyError:
                sn = 'Null'
            try:
                host_name = result['contacted'][ip]['ansible_facts']['ansible_fqdn']
                if host_name == "localhost6.localdomain6": host_name = result['contacted'][ip]['ansible_facts']['ansible_hostname']
            except KeyError:
                host_name = 'Null'

            try:
                cpu = result['contacted'][ip]['ansible_facts']['ansible_processor'][-1]
            except KeyError:
                cpu = 'Null'

            try:
                cpu_cores = result['contacted'][ip]['ansible_facts']['ansible_processor_vcpus']
            except KeyError:
                cpu_cores = 'Null'

            try:
                memory = result['contacted'][ip]['ansible_facts']['ansible_memtotal_mb']
            except KeyError:
                memory = 'Null'

            try:
                disk = sum([int(result['contacted'][ip]['ansible_facts']["ansible_devices"][i]["sectors"]) * \
                            int(result['contacted'][ip]['ansible_facts']["ansible_devices"][i][
                                    "sectorsize"]) / 1024 / 1024 / 1024 \
                            for i in result['contacted'][ip]['ansible_facts']["ansible_devices"] if
                            i[0:2] in ("sd", "ss", "vd", "xv")])
            except KeyError:
                disk = 'Null'


            try:
                os_type = " ".join((result['contacted'][ip]['ansible_facts']["ansible_distribution"],
                                    result['contacted'][ip]['ansible_facts']["ansible_distribution_version"]))
            except KeyError:
                os_type = 'Null'

            try:

                os_kernel = result['contacted'][ip]['ansible_facts']['ansible_kernel']
            except KeyError:
                os_kernel = 'Null'

            asset_data[ip]['sn'] = sn
            asset_data[ip]['host_name'] = host_name
            asset_data[ip]['cpu'] = cpu
            asset_data[ip]['cpu_cores'] = cpu_cores
            asset_data[ip]['memory'] = M2human(memory)
            asset_data[ip]['disk'] = disk
            asset_data[ip]['os_type'] = os_type
            asset_data[ip]['os_kernel'] = os_kernel

        return asset_data


def get_server_sysinfo(server_list):
    return get_host_info(server_list)




if __name__ == '__main__':
    pass
