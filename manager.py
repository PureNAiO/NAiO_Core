import requests
import os
import logging
import time
from zabbix import Zabbix

sage_assistant = 'http://127.0.0.1:5001/api'
saga_insight = 'http://183.6.42.206:3032/api'
zabbix_ip = 'http://127.0.0.1:3031'

logging.basicConfig(filename='log.txt',
                    level=logging.INFO,
                    format='%(asctime)s  %(filename)s : %(levelname)s  %(message)s',
                    datefmt='%Y-%m-%d %A %H:%M:%S')
logging.info('SAGA Manager Running!')

#Function Setting
open_if_check = False
open_data_upload = True


def http_msg(url, device_name:str, datas:dict):
    payload = {'device_name': device_name, 
               'datas': datas}
    response = requests.post(url, json=payload)
    #print(response.ok)
    response.raise_for_status()

def if_check(device, device_name, if_name, issue):
    if device.data[if_name] != 1 and issue:
        issue_data = {'if_name': if_name.split('(')[0],
                      'value': device.data[if_name]}
        http_msg(sage_assistant+'/datas', device_name, issue_data)
        logging.info('Send to Assistant')
        return False
    elif device.data[if_name] == 1:
        return True



def main():
    issue = True
    device_name = 'GZ Office CoreSW'
    if_name = 'Interface Vl888(): Operational status'
    while True:
        device = Zabbix(zabbix_ip)
        device.collector_host(device_name)
        #print(device.data)
        if device.data and open_if_check:
            issue = if_check(device, device_name, if_name, issue)
        if device.data and open_data_upload:
            http_msg(saga_insight+'/datas', device_name, device.data)
            logging.info('Send to Insight')
        time.sleep(60)


if __name__ == "__main__":
    main()
