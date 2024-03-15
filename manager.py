import requests
import time
import os
import logging
from zabbix import Zabbix

sage_assistant = 'http://10.1.1.57:5001/api'
saga_insight = 'http://10.1.1.57:5002/api'
zabbix_ip = 'http://10.1.1.57:3031'

logging.basicConfig(filename='log.txt',
                    level=logging.INFO,
                    format='%(asctime)s  %(filename)s : %(levelname)s  %(message)s',
                    datefmt='%Y-%m-%d %A %H:%M:%S')
logging.info('SAGA Manager Running!')


def http_msg(url, device_name:str, datas:dict):
    payload = {'device_name': device_name, 
               'datas': datas}
    response = requests.post(url, json=payload)
    print(response.ok)
    response.raise_for_status()


def main():
    issue = True
    device_name = 'GZ Office CoreSW'
    if_name = 'Interface Gi0/22(): Operational status'
    start_time = time.time()
    while True:
        device = Zabbix(zabbix_ip)
        device.collector_host(device_name, start_time)
        print(device.data)

        #if device.data[if_name] != 1 and issue:
        if not issue:
            print('G0/22 Fail')
            issue_data = {'if_name': if_name.split('(')[0],
                            'value': device.data[if_name]}
            #http_msg(sage_assistant+'/datas', device_name, issue_data)
            issue = False
        else:
            issue = True
        if device.data:
            http_msg(saga_insight+'/datas', device_name, device.data)

        start_time = time.time()
        time.sleep(10*60)


if __name__ == "__main__":
    main()
