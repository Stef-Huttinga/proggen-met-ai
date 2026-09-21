# SPDX-FileCopyrightText: 2023 Fabian Neumann (TU Berlin), 2023
#
# SPDX-License-Identifier: MIT

from datetime import datetime
from pathlib import Path

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Power Plants", layout="wide")
st.title("Power Plants in Europe")


@st.cache_data
def load_powerplants():
    data_path = Path(__file__).with_name("powerplants.csv")
    return pd.read_csv(data_path, index_col=0)

ppl = load_powerplants()

# Only keep technologies that have valid commissioning dates and coordinates
available_techs = sorted(
    ppl.dropna(subset=["DateIn", "lat", "lon"])["Fueltype"].unique()
)
default_tech_index = (
    available_techs.index("Natural Gas") if "Natural Gas" in available_techs else 0
)

min_year = int(ppl["DateIn"].dropna().min())
max_year = int(ppl["DateIn"].dropna().max())
current_year = min(datetime.now().year, max_year)

with st.sidebar:
    st.title("Data Science for Energy System Modelling")
    st.caption("Explore the power-plant dataset by technology and commissioning year.")

    tech = st.selectbox(
        "Select a technology",
        available_techs,
        index=default_tech_index,
    )

    start, end = st.slider(
        "Range of commissioning years",
        min_year,
        max_year,
        (min_year, current_year),
        step=1,
        help="Pick years!",
    )

filtered = ppl[
    (ppl["Fueltype"] == tech)
    & ppl["DateIn"].between(start, end)
].dropna(subset=["lat", "lon"])

if not filtered.empty:
    hover_data = ["Name", "Fueltype", "Technology", "Capacity", "Efficiency", "DateIn"]
    fig = px.scatter_map(
        filtered,
        lat="lat",
        lon="lon",
        map_style="carto-positron",
        color="DateIn",
        size="Capacity",
        zoom=5.5,
        center={"lat": 52.1326, "lon": 5.2913},
        height=700,
        hover_name="Name",
        hover_data=hover_data,
        range_color=(min_year, max_year),
    )
    st.plotly_chart(fig, width="stretch")

else:
    st.error("Sorry, no power plants to display!")
