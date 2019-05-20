import logging
import ruamel.yaml
from nornir import InitNornir
nr = InitNornir(config_file="config.yaml")
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks.networking import napalm_configure, napalm_get
from nornir.plugins.tasks.text import template_file

def addvlan(task, vlans):
  # we render the template for the platform passing desired_users and users_to_remove
  vlan_config = task.run(task=template_file,path=f"templates/{task.host.platform}",template="vlan.j2",vlans=vlans,severity_level=logging.DEBUG)
  # we load the resulting configuration into the device
  task.run(task=napalm_configure,
    configuration=vlan_config.result)

# we load from a yaml file the users we want
yaml = ruamel.yaml.YAML()
with open("data/vlans.yaml", "r") as f:
  vlans = yaml.load(f.read())
leafs = nr.filter(role="leaf")
# we call manage_users passing the users we loaded from the yaml file
r = leafs.run(task=addvlan,vlans=vlans)
print_result(r)
