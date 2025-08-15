import streamlit as st
import pandas as pd
import plotly.express as px

# Page Config
st.set_page_config(page_title="Electric Sales by States", page_icon="⚡", layout="wide")

# Title
st.title("⚡ Electric Vehicle Sales Dashboard (State-wise)")

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("electric_sales.csv")  # Agar file Excel hai to read_excel use karo
    return df

df = load_data()

# Sidebar Filters
st.sidebar.header("Filters")
states = st.sidebar.multiselect("Select States", options=df["State"].unique(), default=df["State"].unique())
years = st.sidebar.multiselect("Select Years", options=df["Year"].unique(), default=df["Year"].unique())

# Filter Data
df_filtered = df[(df["State"].isin(states)) & (df["Year"].isin(years))]

# KPIs
total_sales = df_filtered["EV_Sales"].sum()
top_state = df_filtered.groupby("State")["EV_Sales"].sum().idxmax()
st.metric("Total EV Sales", f"{total_sales:,}")
st.metric("Top State", top_state)

# Map
fig_map = px.choropleth(df_filtered,
                        locations="State",
                        locationmode="geojson-id",
                        color="Sales",
                        hover_name="State",
                        title="State-wise EV Sales")
st.plotly_chart(fig_map, use_container_width=True)

# Bar Chart
fig_bar = px.bar(df_filtered.groupby("State")["EV_Sales"].sum().reset_index(),
                 x="State", y="EV_Sales", title="EV Sales by State")
st.plotly_chart(fig_bar, use_container_width=True)

# Line Chart (Trend)
fig_line = px.line(df_filtered.groupby("Year")["EV_Sales"].sum().reset_index(),
                   x="Year", y="EV_Sales", title="EV Sales Over Time")
st.plotly_chart(fig_line, use_container_width=True)

# Show Data
st.dataframe(df_filtered)


