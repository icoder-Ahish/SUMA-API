import streamlit as st
import pandas as pd
import altair as alt
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

for i in range(len(activesystems)):
    system_names.append(activesystems[i]['name'])
    patch_counts.append(len(client.system.getRelevantErrata(key, activesystems[i]['id'])))

data = pd.DataFrame({
    'System Name': system_names,
    'Patch Count': patch_counts
})

st.write(f"Number of active systems: {len(activesystems)}")

st.write('Patch Count by System')
chart = alt.Chart(data).mark_bar().encode(
    x=alt.X('System Name', axis=alt.Axis(labelAngle=0)),
    y='Patch Count'
)
line_chart = alt.Chart(data).mark_line().encode(
    x='System Name',
    y='Patch Count'
)


pie_chart = alt.Chart(data).mark_arc().encode(
    color='System Name',
    theta='Patch Count'
)

st.altair_chart(chart, use_container_width=True)
st.altair_chart(pie_chart, use_container_width=True)
st.altair_chart(line_chart, use_container_width=True)
client.auth.logout(key)
