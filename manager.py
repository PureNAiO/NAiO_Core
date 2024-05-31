import requests
import logging
from zabbix import Zabbix

#sage_assistant = 'http://127.0.0.1:5001/api'
saga_insight = 'http://127.0.0.1:5000/api'
zabbix_ip = 'http://127.0.0.1:3031'

logging.basicConfig(filename='log.txt',
                    level=logging.INFO,
                    format='%(asctime)s  %(filename)s : %(levelname)s  %(message)s',
                    datefmt='%Y-%m-%d %A %H:%M:%S')
logging.info('SAGA Manager Running!')


def http_msg(url, device_name:str, datas:dict):
    payload = {'device_name': device_name, 
               'datas': datas}
    response = requests.post(url, json=payload)
    response.raise_for_status()


def monitor():
    try:
        device = Zabbix(zabbix_ip)
        for device_name in device.inventory.keys():
            device.collector_host(device_name)
            if device.data:
                http_msg(saga_insight+'/datas', device_name, device.data)

    except Exception as e:
        logging.error(e)
