import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# your existing code
from pprint import pprint
from xmlrpc.client import ServerProxy
import ssl

MANAGER_URL = "https://10.0.0.20/rpc/api"
MANAGER_LOGIN = "sumaadmin"
MANAGER_PASSWORD = "exadmin"

# You might need to set to other options depending on your
# server SSL configuartion and your local SSL configuration
context = ssl._create_unverified_context()
client = ServerProxy(MANAGER_URL, context=context)
key = client.auth.login(MANAGER_LOGIN, MANAGER_PASSWORD)

activesystems = client.system.listActiveSystems(key)

system_name = []
patches = []

for i in range(len(activesystems)):
    system_name.append(activesystems[i]['name'])
    patches.append(len(client.system.getRelevantErrata(key, activesystems[i]['id'])))

client.auth.logout(key)

# create a pandas dataframe from the system_name and patches lists
data = {'system_name': system_name, 'patches': patches}
df = pd.DataFrame(data)

# create a line chart using matplotlib
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(df['system_name'], df['patches'])
ax.set_title('Number of Patches per System')
ax.set_xlabel('System Name')
ax.set_ylabel('Number of Patches')
ax.tick_params(axis='x', rotation=90)

# display the chart using streamlit
st.pyplot(fig)