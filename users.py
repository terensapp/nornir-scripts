import logging
import ruamel.yaml
from nornir import InitNornir
nr = InitNornir(config_file="config.yaml")
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks.networking import napalm_configure, napalm_get
from nornir.plugins.tasks.text import template_file

def manage_users(task, desired_users):
  # get users from device
  state_users = task.run(task=napalm_get,getters=["users"],severity_level=logging.DEBUG)
  # let's verify if the users we got are in desired_users
  # if they are not we have to remove them
  users_to_remove = []
  for user in state_users.result["users"]:
    if user not in desired_users:
      users_to_remove.append(user)
  # we render the template for the platform passing desired_users and users_to_remove
  users_config = task.run(task=template_file,path=f"templates/{task.host.platform}",template="users.j2",desired_users=desired_users,remove_users=users_to_remove,severity_level=logging.DEBUG)
  # we load the resulting configuration into the device
  task.run(task=napalm_configure,
    configuration=users_config.result)

# we load from a yaml file the users we want
yaml = ruamel.yaml.YAML()
with open("data/users.yaml", "r") as f:
  desired_users = yaml.load(f.read())
leafs = nr.filter(role="leaf")
# we call manage_users passing the users we loaded from the yaml file
r = leafs.run(task=manage_users,desired_users=desired_users)
print_result(r)
