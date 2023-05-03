import streamlit as st
from xmlrpc.client import ServerProxy
import pprint
import ssl

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

# Apply the patch when the submit button is clicked
if submit_button:
    system_id = [system['id'] for system in activesystems if system['name'] == system_name][0]
    patch_id = client.errata.listErrata(key, patch_name, system_id, 'all', 1)[0]['id']
    client.system.scheduleApplyErrata(key, patch_id, [system_id])
    st.success(f"Patch {patch_name} has been scheduled for the system {system_name}")
