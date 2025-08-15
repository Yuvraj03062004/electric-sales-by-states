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

