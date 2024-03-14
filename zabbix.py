from pyzabbix.api import ZabbixAPI

## Note ##
# Interface Operational status: 1 is up, 2 is down

class Zabbix:
    def __init__(self, zabbix_url):
        # Create ZabbixAPI class instance
        self.zapi = ZabbixAPI(server=zabbix_url)
        self.zapi.login(api_token='853c722b91fc6747784fcea0aa02f51abccfc1961be12d49f82065866740ab92')
        self.inventory = {host['host']: host['hostid'] for host in self.zapi.host.get(monitored_hosts=1, output='extend')}
        self.data = {}

    def collector_host(self, device_name, start_time):
        host_id = self.inventory[device_name]
        result = self.zapi.item.get(hostids=host_id)
        metrics: dict = {info['itemid']: info['name'] for info in result}
        history = self.zapi.history.get(hostids=host_id, itemids=list(metrics.keys()), time_from=int(start_time))
        for info in history:
            item_id = info['itemid']
            item_name = metrics[item_id]
            item_value = info['value']
            self.data[item_name] = item_value







