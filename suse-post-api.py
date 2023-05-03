import streamlit as st
from xmlrpc.client import ServerProxy
import ssl
import pprint

MANAGER_URL = "https://10.0.0.20/rpc/api"
MANAGER_LOGIN = "sumaadmin"
MANAGER_PASSWORD = "exadmin"

context = ssl._create_unverified_context()
client = ServerProxy(MANAGER_URL, context=context)
key = client.auth.login(MANAGER_LOGIN, MANAGER_PASSWORD)

activesystems = client.system.listActiveSystems(key)

# for i in range(len(activesystems)):
#     pprint.pprint(activesystems[i]['id'])

patches = []
patches_id_list = []
for i in range(len(activesystems)):
    patches.append(client.system.getRelevantErrata(key, activesystems[i]['id']))

key = 'id'

for dictionary_list in patches:
    for dictionary in dictionary_list:
        for k, v in dictionary.items():
            if k == key:
                patches_id_list.append(v)

print("Printing Patch Id")
print(patches_id_list)
# pprint.pprint(patches)

# print(len(patches))
#
# for i in range(len(patches)):
#     pprint.pprint(patches[i]['id'])

# end = 15000
# for i in range(0, end):
#     patches = client.system.getRelevantErrata(key, activesystems[i]['id'])
#     print(patches)

# client.auth.logout(key)
