from pprint import pprint
from xmlrpc.client import ServerProxy
import ssl

manager_url = "https://10.0.0.20/rpc/api"
manager_login = "sumaadmin"
manager_password = "exadmin"

# you might need to set to other options depending on your
# server ssl configuartion and your local ssl configuration
context = ssl._create_unverified_context()
client = ServerProxy(manager_url, context=context)
key = client.auth.login(manager_login, manager_password)
# pprint(key)

# print(client.user.list_users(key))
# pprint(client.system.monitoring.listEndpoints(key, [1000010027]))
# pprint(client.system.monitoring.listEndpoints(key, [1000010027, 1000010008, 1000010012]))
# pprint(client.system.listInstalledPackages(key, 1000010027))

# system_name = 'sle-12sp5' # replace with the name of the system you want to retrieve the ID for
# system_id = client.system.getId(key, system_name)
#
# # print the system ID
# print(system_id)
#
# pprint(client.system.getRelevantPatches(key, system_id))
# print(system['name'], patches)
#
# pprint(client.Errata.Bugzillafixes(key, "suse-12-sp5-2019-2781"))
swchannels = client.channel.listVendorChannels(key)
print("Print VendorChannels")
pprint(swchannels)
#
# pprint(type(swchannels))
# print(len(swchannels))
#
# swchannels_labels = []
# for i in range(len(swchannels)):
# #print(swchannels[i]['label'])
#     swchannels_labels.append(swchannels[i]['label'])
#     pprint(len(client.channel.software.listErrata(key, swchannels[i]['label'])))
#
# # pprint(swchannels_labels)
#
client.auth.logout(key)

