import plotly.express as px
import streamlit as st

from calculations.emissions import EMISSIONS_COLUMN, EmissionsOverview


def render_emissions_overview(emissions: EmissionsOverview) -> None:
    st.subheader("Estimated annual CO₂ emissions")
    st.caption(
        "Estimates use installed capacity, an assumed capacity factor and direct operational emission factors."
    )
    st.metric("Total estimated emissions", f"{emissions.total_emissions:,.0f} t CO₂/year")

    chart_col, fuel_col = st.columns(2)
    with chart_col:
        country_fig = px.bar(
            emissions.country_emissions.head(15),
            x=EMISSIONS_COLUMN,
            y="Country",
            orientation="h",
            title="Estimated emissions by country",
            labels={EMISSIONS_COLUMN: "tonnes CO₂/year"},
        )
        country_fig.update_layout(yaxis={"categoryorder": "total ascending"})
        st.plotly_chart(country_fig, width="stretch")

    with fuel_col:
        fuel_fig = px.bar(
            emissions.fuel_emissions,
            x="Fueltype",
            y=EMISSIONS_COLUMN,
            title="Estimated emissions by fuel",
            labels={EMISSIONS_COLUMN: "tonnes CO₂/year"},
        )
        st.plotly_chart(fuel_fig, width="stretch")

    country_fuel_fig = px.bar(
        emissions.country_fuel_emissions,
        x=EMISSIONS_COLUMN,
        y="Country",
        color="Fueltype",
        orientation="h",
        title="CO₂ by country and fuel",
        labels={EMISSIONS_COLUMN: "tonnes CO₂/year", "Fueltype": "fuel"},
        category_orders={
            "Country": emissions.country_emissions.head(15)["Country"].iloc[::-1].tolist()
        },
    )
    country_fuel_fig.update_layout(
        barmode="stack",
        height=600,
        legend={
            "orientation": "h",
            "title_text": "Fuel",
            "x": 0,
            "xanchor": "left",
            "y": -0.35,
            "yanchor": "top",
        },
        margin={"b": 150},
    )
    st.plotly_chart(country_fuel_fig, width="stretch")
