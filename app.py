import pandas as pd
import plotly.express as px
import json
import requests

# Data load
df = pd.read_csv("electric_sales.csv")

# India ka GeoJSON load (public source)
geojson_url = "https://raw.githubusercontent.com/geohacker/india/master/state/india_telengana.json"
geojson_data = requests.get(geojson_url).json()

# Column check
df['State'] = df['State'].str.strip()  # extra spaces remove

# Choropleth Map
fig_map = px.choropleth(
    df,
    geojson=geojson_data,
    featureidkey="properties.NAME_1",  # GeoJSON me state ka naam yahan hota hai
    locations="State",
    color="EV_Sales",
    hover_name="State",
    color_continuous_scale="Viridis",
    title="State-wise EV Sales in India"
)

fig_map.update_geos(fitbounds="locations", visible=False)

# Agar Streamlit me use karna ho
# import streamlit as st
# st.plotly_chart(fig_map)


