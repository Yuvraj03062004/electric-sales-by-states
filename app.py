import streamlit as st
import pandas as pd
import plotly.express as px

# Page config
st.set_page_config(page_title="EV Sales Dashboard", layout="wide")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("electric_sales.csv")  # <-- apna CSV name check kar lo
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("Filters")
year_filter = st.sidebar.multiselect("Select Year", sorted(df["Year"].unique()))
state_filter = st.sidebar.multiselect("Select State", sorted(df["State"].unique()))

df_filtered = df.copy()
if year_filter:
    df_filtered = df_filtered[df_filtered["Year"].isin(year_filter)]
if state_filter:
    df_filtered = df_filtered[df_filtered["State"].isin(state_filter)]

# KPI Calculations
total_sales = df_filtered["EV_Sales"].sum()
top_state = df_filtered.groupby("State")["EV_Sales"].sum().idxmax()
growth = ((df_filtered["EV_Sales"].sum() - df["EV_Sales"].sum()) / df["EV_Sales"].sum()) * 100

# KPI Cards
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Total EV Sales", value=f"{total_sales:,.0f}")
with col2:
    st.metric(label="Top State", value=top_state)
with col3:
    st.metric(label="Growth %", value=f"{growth:.2f}%")

# Charts Row 1
col4, col5 = st.columns(2)
with col4:
    sales_trend = df_filtered.groupby("Year")["EV_Sales"].sum().reset_index()
    fig_trend = px.line(sales_trend, x="Year", y="EV_Sales", title="Sales Trend Over Years", markers=True)
    st.plotly_chart(fig_trend, use_container_width=True)

with col5:
    category_data = df_filtered.groupby("Vehicle_Category")["EV_Sales"].sum().reset_index()
    fig_pie = px.pie(category_data, names="Vehicle_Category", values="EV_Sales", title="Sales by Vehicle Category")
    st.plotly_chart(fig_pie, use_container_width=True)

# Footer
st.markdown("---")
st.caption("Electric Vehicle Sales Dashboard - Created by [Your Name]")



