import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------
# PAGE CONFIGURATION
# --------------------------
st.set_page_config(
    page_title="Electric Vehicle Sales - State Wise",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------
# LOAD DATA
# --------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("electric_sales.csv")
    return df

data = load_data()

# --------------------------
# CUSTOM CSS
# --------------------------
st.markdown("""
    <style>
    /* Sidebar title */
    [data-testid=stSidebar] h2 {
        color: #1565C0;
    }
    /* Sidebar dropdown styling */
    div[data-baseweb="select"] div {
        background-color: #1565C0 !important;
        color: white !important;
    }
    /* Selected filter tags */
    div[data-baseweb="tag"] {
        background-color: #1565C0 !important;
        color: white !important;
        border-radius: 5px !important;
        padding: 2px 5px !important;
    }
    /* KPI styling */
    .metric-card {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0px 1px 3px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# --------------------------
# SIDEBAR FILTERS
# --------------------------
st.sidebar.header("Filters")
year_options = sorted(data["Year"].unique())
state_options = sorted(data["State"].unique())

selected_year = st.sidebar.multiselect("Select Year", year_options, default=year_options)
selected_state = st.sidebar.multiselect("Select State", state_options, default=state_options)

# --------------------------
# DATA FILTERING
# --------------------------
filtered_df = data[
    (data["Year"].isin(selected_year)) &
    (data["State"].isin(selected_state))
]

# --------------------------
# KPI METRICS
# --------------------------
total_sales = int(filtered_df["EV_Sales"].sum())
top_state = filtered_df.groupby("State")["EV_Sales"].sum().idxmax()
top_state_sales = int(filtered_df.groupby("State")["EV_Sales"].sum().max())

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"<div class='metric-card'><h4>Total EV Sales</h4><h2>{total_sales:,}</h2></div>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<div class='metric-card'><h4>Top State</h4><h2>{top_state}</h2></div>", unsafe_allow_html=True)
with col3:
    st.markdown(f"<div class='metric-card'><h4>Top State Sales</h4><h2>{top_state_sales:,}</h2></div>", unsafe_allow_html=True)

# --------------------------
# CHARTS
# --------------------------

# Map Chart
map_fig = px.choropleth(
    filtered_df.groupby("State", as_index=False)["EV_Sales"].sum(),
    locations="State",
    locationmode="india states",
    color="EV_Sales",
    color_continuous_scale="Blues",
    title="State-wise EV Sales"
)
map_fig.update_geos(fitbounds="locations", visible=False)

# Bar Chart
bar_fig = px.bar(
    filtered_df.groupby("State", as_index=False)["EV_Sales"].sum().sort_values("EV_Sales", ascending=False),
    x="State", y="EV_Sales",
    title="EV Sales by State",
    color="EV_Sales",
    color_continuous_scale="Blues"
)

# Line Chart (Trend over time)
trend_fig = px.line(
    filtered_df.groupby(["Year", "Month_Name"], as_index=False)["EV_Sales"].sum(),
    x="Month_Name", y="EV_Sales", color="Year",
    title="Monthly EV Sales Trend"
)

# --------------------------
# DISPLAY CHARTS
# --------------------------
left_col, right_col = st.columns(2)
left_col.plotly_chart(map_fig, use_container_width=True)
right_col.plotly_chart(bar_fig, use_container_width=True)

st.plotly_chart(trend_fig, use_container_width=True)






