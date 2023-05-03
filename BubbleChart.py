import streamlit as st
import pandas as pd
import altair as alt
from pprint import pprint
from xmlrpc.client import ServerProxy
import ssl

MANAGER_URL = "https://10.0.0.20/rpc/api"
MANAGER_LOGIN = "sumaadmin"
MANAGER_PASSWORD = "exadmin"

context = ssl._create_unverified_context()
client = ServerProxy(MANAGER_URL, context=context)
key = client.auth.login(MANAGER_LOGIN, MANAGER_PASSWORD)

activesystems = client.system.listActiveSystems(key)

system_names = []
patch_counts = []
cpu_counts = []
memory_counts = []

for i in range(len(activesystems)):
    system_names.append(activesystems[i]['name'])
    patch_counts.append(len(client.system.getRelevantErrata(key, activesystems[i]['id'])))
    cpu_counts.append(client.system.getCpu(key, activesystems[i]['id']))
    memory_counts.append(client.system.getMemory(key, activesystems[i]['id']))

data = pd.DataFrame({
    'System Name': system_names,
    'Patch Count': patch_counts,
    'CPU Count': cpu_counts,
    'Memory Count': memory_counts
})

st.write(f"Number of active systems: {len(activesystems)}")

# Scatter plot
st.write('Patch Count vs. CPU Count')
chart_scatter = alt.Chart(data).mark_circle().encode(
    x='Patch Count',
    y='CPU Count',
    tooltip=['System Name', 'Patch Count', 'CPU Count']
).interactive()
st.altair_chart(chart_scatter, use_container_width=True)

# Bubble chart
st.write('Patch Count vs. CPU Count vs. Memory Count')
chart_bubble = alt.Chart(data).mark_circle().encode(
    x='Patch Count',
    y='CPU Count',
    size='Memory Count',
    color='Patch Count',
    tooltip=['System Name', 'Patch Count', 'CPU Count', 'Memory Count']
).interactive()
st.altair_chart(chart_bubble, use_container_width=True)

client.auth.logout(key)
