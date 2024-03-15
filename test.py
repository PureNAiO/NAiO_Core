from pyzabbix.api import ZabbixAPI

zapi = ZabbixAPI(server='http://10.1.1.57:3031')
zapi.login(api_token='b38f37bf1536fba3f7b591960ab63b51b3b20b5384af15aa8b55bacb55b3625b')
inventory = {host['host']: host['hostid'] for host in zapi.host.get(monitored_hosts=1, output='extend')}
print(inventory)