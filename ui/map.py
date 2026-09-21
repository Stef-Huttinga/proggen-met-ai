from datetime import datetime

import pandas as pd
import plotly.express as px
import streamlit as st


def render_powerplant_map(powerplants: pd.DataFrame) -> None:
    available_techs = sorted(
        powerplants.dropna(subset=["DateIn", "lat", "lon"])["Fueltype"].unique()
    )
    default_tech_index = (
        available_techs.index("Natural Gas") if "Natural Gas" in available_techs else 0
    )
    min_year = int(powerplants["DateIn"].dropna().min())
    max_year = int(powerplants["DateIn"].dropna().max())
    current_year = min(datetime.now().year, max_year)

    with st.sidebar:
        st.title("Data Science for Energy System Modelling")
        st.caption("Explore the power-plant dataset by technology and commissioning year.")
        technology = st.selectbox(
            "Select a technology",
            available_techs,
            index=default_tech_index,
        )
        start_year, end_year = st.slider(
            "Range of commissioning years",
            min_year,
            max_year,
            (min_year, current_year),
            step=1,
            help="Pick years!",
        )

    filtered = powerplants[
        (powerplants["Fueltype"] == technology)
        & powerplants["DateIn"].between(start_year, end_year)
    ].dropna(subset=["lat", "lon"])

    if filtered.empty:
        st.error("Sorry, no power plants to display!")
        return

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
        hover_data=["Name", "Fueltype", "Technology", "Capacity", "Efficiency", "DateIn"],
        range_color=(min_year, max_year),
    )
    st.plotly_chart(fig, width="stretch")
