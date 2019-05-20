from pprint import pprint
from nornir import InitNornir
from nornir.plugins.functions.text import print_result

nr = InitNornir(config_file="config.yaml")

from nornir.plugins.tasks.networking import napalm_get

leafs = nr.filter(role="leaf")

leaffacts = leafs.run(name="Get facts",task=napalm_get, getters=["arp_table"])

print("%s\t\t\t%s\t\t\t%s\t\t%s" % ('Host', 'IP', 'MAC Address', 'Interface'))

for leaf,result in leaffacts.items():
  task = result[0]
  fact = task.result['arp_table']
  for arp_table in fact:
    print("%s\t\t%s\t\t%s\t%s" % (leaf, arp_table['ip'], arp_table['mac'], arp_table['interface']))
