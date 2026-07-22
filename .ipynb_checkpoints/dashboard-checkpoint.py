import streamlit as st
import pandas as pd
import plotly.express as px

# Page Configuration
st.set_page_config(page_title="FIFA World Cup Dashboard", layout="wide")

# Title
st.title("⚽ FIFA World Cup Match Analysis Dashboard")

# Load Dataset
df = pd.read_csv("fifa_wc_mens_match_dataset_1970_2022.csv")

# Show Dataset
st.subheader("Dataset Preview")
st.dataframe(df.head())

# Summary Metrics
st.subheader("Project Summary")

col1, col2, col3 = st.columns(3)

col1.metric("Total Matches", len(df))
col2.metric("Teams", df["team_name"].nunique())
col3.metric("Tournaments", df["tournament_name"].nunique())