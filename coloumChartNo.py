from xmlrpc.client import ServerProxy
import ssl
import streamlit as st

MANAGER_URL = "https://10.0.0.20/rpc/api"
MANAGER_LOGIN = "sumaadmin"
MANAGER_PASSWORD = "exadmin"

# You might need to set to other options depending on your
# server SSL configuartion and your local SSL configuration
context = ssl._create_unverified_context()
client = ServerProxy(MANAGER_URL, context=context)
key = client.auth.login(MANAGER_LOGIN, MANAGER_PASSWORD)

activesystems = client.system.listActiveSystems(key)

st.header("Active Systems and Relevant Errata")

st.write(f"Number of active systems: {len(activesystems)}")

for i in range(len(activesystems)):
    system_name = activesystems[i]['name']
    patches = len(client.system.getRelevantErrata(key, activesystems[i]['id']))
    st.subheader(system_name)
    st.write(f"Number of relevant errata: {patches}")
    st.bar_chart({system_name: patches})

client.auth.logout(key)