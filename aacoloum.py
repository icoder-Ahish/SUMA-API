import streamlit as st
from xmlrpc.client import ServerProxy
import pprint
import ssl
import array

MANAGER_URL = "https://10.0.0.20/rpc/api"
MANAGER_LOGIN = "sumaadmin"
MANAGER_PASSWORD = "exadmin"

context = ssl._create_unverified_context()
client = ServerProxy(MANAGER_URL, context=context)
key = client.auth.login(MANAGER_LOGIN, MANAGER_PASSWORD)

# Get list of active systems for the selectbox
activesystems = client.system.listActiveSystems(key)

system_names = [system['name'] for system in activesystems]

for i in range(len(activesystems)):
    patchs = client.system.getRelevantErrata(key, activesystems[i]['id'])
    # pprint(patchs)

# Create the Streamlit form
with st.form(key='apply_patch_form'):
    patch_name = st.text_input('Enter patch name')
    system_name = st.selectbox('Select system', options=system_names)
    submit_button = st.form_submit_button(label='Apply patch')

#############################
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
myarray = array.array('i',patches_id_list)

#######################################
# Create the Streamlit form
# with st.form(key='list_patch_form'):
#     system_name = st.selectbox('Select system', options=system_names)
#     submit_button1 = st.form_submit_button(label='Show patches')
#
# if submit_button1:
#     system_id = [system['id'] for system in activesystems if system['name'] == system_name][0]
#     patches = client.system.getRelevantErrata(key, system_id)
#     patch_ids = [patch['id'] for patch in patches]
#     st.write(f"Patch IDs for {system_name}: {patch_ids}")
#######################################
# Apply the patch when the submit button is clicked
if submit_button:
    system_id = [system['id'] for system in activesystems if system['name'] == system_name][0]
    # patch_id = client.errata.listErrata(key, patch_name, system_id, 'all', 1)[0]['id']
    client.system.scheduleApplyErrata(key, patches_id_list, [system_id])
    st.success(f"Patch {patch_name} has been scheduled for the system {system_name}")

# client.auth.logout(key)
