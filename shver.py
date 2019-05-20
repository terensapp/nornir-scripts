from nornir import InitNornir
nr = InitNornir(config_file="config.yaml")
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks.networking import napalm_cli

leafs = nr.filter(role="leaf")
r = leafs.run(name="Running 'show version'",task=napalm_cli,commands=["show version"])

for host,task_results in r.items():
  task = task_results[0]
  result = task.result
  print(f"{host}: {result}")
