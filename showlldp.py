from pprint import pprint
from nornir import InitNornir
from nornir.plugins.functions.text import print_result

nr = InitNornir(config_file="config.yaml")

from nornir.plugins.tasks.networking import napalm_get

leafs = nr.filter(role="leaf")

neighbors = leafs.run(name="Show lldp",task=napalm_get, getters=["lldp_neighbors"])

for leaf,result in neighbors.items():
  print("%s's neighbors are:" % (leaf))
  task = result[0]
  neighbors = task.result['lldp_neighbors']
  for neighbor in neighbors:
    connection = neighbors[neighbor]
    connection = connection[0]
    print("\t%s:%s connected via %s" % (connection['hostname'],connection['port'],neighbor))
  print('')
