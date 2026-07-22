# pages/03_demand.py — demand story

import streamlit as st
import plotly.express as px
import sys, os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import load_data, sidebar_filters

# Load data + shared sidebar
df, p95 = load_data()
filtered = sidebar_filters(df, p95)

st.title("Where is guest demand strongest?")
st.caption("Demand is estimated using reviews per month.")

# -----------------------------
# Persisted widget
# -----------------------------
room_types = sorted(filtered["room_type"].unique())

if "sel_room" not in st.session_state:
    st.session_state.sel_room = room_types[0]

st.session_state.sel_room = st.session_state.sel_room

if st.session_state.sel_room not in room_types:
    st.session_state.sel_room = room_types[0]

st.selectbox(
    "Choose Room Type",
    room_types,
    key="sel_room"
)

room = st.session_state.sel_room
room_df = filtered[filtered["room_type"] == room]

# -----------------------------
# KPI Row
# -----------------------------
k1, k2, k3 = st.columns(3)

k1.metric(
    "Listings",
    f"{len(room_df):,}"
)

k2.metric(
    "Median Reviews/Month",
    f"{room_df['reviews_per_month'].median():.1f}",
    f"{room_df['reviews_per_month'].median()-filtered['reviews_per_month'].median():+.1f}"
)

k3.metric(
    "Median Price",
    f"£{room_df['price'].median():.0f}"
)

st.divider()

# Highlight colour:
# Blue = selected room type, Grey = all other room types
plot_df = filtered.copy()

plot_df["highlight"] = plot_df["room_type"].apply(
    lambda x: room if x == room else "Other"
)

fig = px.scatter(
    plot_df,
    x="price",
    y="reviews_per_month",
    color="highlight",
    hover_name="neighbourhood",
    title=f"Demand for {room}",
    labels={
        "price": "Nightly Price (£)",
        "reviews_per_month": "Reviews per Month"
    },
    color_discrete_map={
        room: "#2E75B6",
        "Other": "#AAAAAA"
    }
)

fig.update_layout(
    plot_bgcolor="white",
    paper_bgcolor="white",
    font=dict(
        family="Arial",
        size=12
    )
)

st.plotly_chart(
    fig,
    use_container_width=True
)