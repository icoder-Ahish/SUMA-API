# SUMA-API-CALL


# Requirements
## The following libraries are required to run the application:

    Streamlit
    Pandas
    Altair
    xmlrpc.client
    ssl
  
# Usage  
##  Import the required libraries:

    import streamlit as st
    import pandas as pd
    import altair as alt
    from xmlrpc.client import ServerProxy
    import ssl
  
## Set the URL, login and password of the Suse Maneger Server:  

    MANAGER_URL = "https://10.0.0.20/rpc/api"
    MANAGER_LOGIN = "sumaadmin"
    MANAGER_PASSWORD = "exadmin"

## Create an SSL context and a ServerProxy object for the Suse Maneger Server:

    context = ssl._create_unverified_context()
    client = ServerProxy(MANAGER_URL, context=context)

## Log in to the Suse Maneger Server and get an authentication key:

    key = client.auth.login(MANAGER_LOGIN, MANAGER_PASSWORD)
  
## Retrieve a list of active systems and their patch counts:  

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

## Display the number of active systems:

    st.write(f"Number of active systems: {len(activesystems)}")

## Create Altair visualizations for the patch count by system:

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

## Display the Altair visualizations using Streamlit:

    st.altair_chart(chart, use_container_width=True)
    st.altair_chart(pie_chart, use_container_width=True)
    st.altair_chart(line_chart, use_container_width=True)

## Log out of the Suse Maneger Server:

    client.auth.logout(key)
    
## Run Your Application

    streamlit run file_name.py

