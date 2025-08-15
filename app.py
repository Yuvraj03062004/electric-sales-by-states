import pandas as pd
import plotly.express as px
import requests

# Data load
df = pd.read_csv("electric_sales.csv")

# Extra spaces remove
df['State'] = df['State'].str.strip()

# India ka GeoJSON load
geojson_url = "https://raw.githubusercontent.com/geohacker/india/master/state/india_states.geojson"
geojson_data = requests.get(geojson_url).json()

# Choropleth Map
fig_map = px.choropleth(
    df,
    geojson=geojson_data,
    featureidkey="properties.state",  # GeoJSON me state ka naam ka key
    locations="State",
    color="EV_Sales",
    hover_name="State",
    color_continuous_scale="Viridis",
    title="State-wise EV Sales in India"
)

fig_map.update_geos(fitbounds="locations", visible=False)

# Agar Streamlit me
# import streamlit as st
# st.plotly_chart(fig_map)

