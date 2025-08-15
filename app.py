import streamlit as st
import pandas as pd
import plotly.express as px
import requests

st.set_page_config(page_title="⚡ Electric Vehicle Sales Dashboard", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("electric_sales.csv")
    df['State'] = df['State'].str.strip()
    return df

df = load_data()

# Sidebar filter
states = st.sidebar.multiselect("Select States", options=df["State"].unique(), default=df["State"].unique())
df_filtered = df[df["State"].isin(states)]

# KPIs
total_sales = df_filtered["EV_Sales"].sum()
top_state = df_filtered.groupby("State")["EV_Sales"].sum().idxmax()

col1, col2 = st.columns(2)
col1.metric("Total EV Sales", f"{total_sales:,}")
col2.metric("Top State", top_state)

# Map
geojson_url = "https://raw.githubusercontent.com/geohacker/india/master/state/india_telengana.json"
geojson_data = requests.get(geojson_url).json()

fig_map = px.choropleth(
    df_filtered,
    geojson=geojson_data,
    featureidkey="properties.NAME_1",
    locations="State",
    color="EV_Sales",
    hover_name="State",
    color_continuous_scale="Viridis",
    title="State-wise EV Sales"
)
fig_map.update_geos(fitbounds="locations", visible=False)
st.plotly_chart(fig_map, use_container_width=True)



