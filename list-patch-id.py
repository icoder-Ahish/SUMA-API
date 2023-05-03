import streamlit as st
from xmlrpc.client import ServerProxy
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

# Create the Streamlit form
with st.form(key='apply_patch_form'):
    system_name = st.selectbox('Select system', options=system_names)
    submit_button = st.form_submit_button(label='Show patches')

if submit_button:
    system_id = [system['id'] for system in activesystems if system['name'] == system_name][0]
    patches = client.system.getRelevantErrata(key, system_id)
    patch_ids = [patch['id'] for patch in patches]
    st.write(f"Patch IDs for {system_name}: {patch_ids}")

client.auth.logout(key)
