import requests
import time
import os
import logging
from zabbix import Zabbix

device_name = 'GZ Office CoreSW'
if_name = 'Interface Gi0/22(): Operational status'
sage_assistant = 'http://127.0.0.1:5001/api'
saga_insight = 'http://127.0.0.1:5002/api'

logging.basicConfig(filename='log.txt',
                    level=logging.INFO,
                    format='%(asctime)s  %(filename)s : %(levelname)s  %(message)s',
                    datefmt='%Y-%m-%d %A %H:%M:%S')
logging.info('SAGA Manager Running!')


def http_msg(url, datas: dict):
    payload = {'datas': datas}
    response = requests.post(url, data=payload)
    response.raise_for_status()


def main():
    try:
        start_time = time.time()
        while True:
            device = Zabbix()
            device.collector_host(device_name, start_time)
            print(device.data)

            if device.data and device.data[if_name] != 1:
                print('G0/22 Fail')
                http_msg(sage_assistant+'/datas', {if_name:device.data[if_name]})
            http_msg(saga_insight+'/datas', device.data)

            start_time = time.time()
            time.sleep(10*60)
    except Exception as error:
        logging.error(error)


if __name__ == "__main__":
    main()
