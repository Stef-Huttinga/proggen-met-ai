import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import pandas as pd

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


def render_emissions_explorer(co2_emissions: pd.DataFrame) -> None:
    st.subheader("Explore emissions")
    plants_tab, mix_tab, relationships_tab, scenario_tab = st.tabs(
        ["Power plants", "Energy mix", "Relationships", "Scenario"]
    )

    with plants_tab:
        top_plants = co2_emissions.nlargest(20, EMISSIONS_COLUMN).sort_values(EMISSIONS_COLUMN)
        fig = px.bar(
            top_plants,
            x=EMISSIONS_COLUMN,
            y="Name",
            color="Fueltype",
            orientation="h",
            hover_data=["Country", "Capacity"],
            labels={EMISSIONS_COLUMN: "tonnes CO₂/year", "Name": "Plant", "Fueltype": "Fuel"},
            title="20 highest-emitting power plants",
        )
        fig.update_layout(height=700, yaxis={"categoryorder": "array", "categoryarray": top_plants["Name"].tolist()})
        st.plotly_chart(fig, width="stretch")

    with mix_tab:
        mode = st.radio("Show", ["Annual emissions", "Share within country"], horizontal=True)
        country_totals = co2_emissions.groupby("Country")[EMISSIONS_COLUMN].sum().nlargest(15)
        mix = co2_emissions[co2_emissions["Country"].isin(country_totals.index)].pivot_table(
            index="Country", columns="Fueltype", values=EMISSIONS_COLUMN, aggfunc="sum", fill_value=0
        ).reindex(country_totals.index)
        mix = mix.loc[:, mix.sum(axis=0) > 0]
        if mode == "Share within country":
            mix = mix.div(mix.sum(axis=1).replace(0, float("nan")), axis=0).fillna(0) * 100
        fig = px.imshow(
            mix,
            aspect="auto",
            color_continuous_scale="YlOrRd",
            labels={"x": "Fuel", "y": "Country", "color": "% of country" if mode == "Share within country" else "t CO₂/year"},
            title="Emissions by country and fuel",
        )
        fig.update_layout(height=650, xaxis_tickangle=-35)
        st.plotly_chart(fig, width="stretch")

    with relationships_tab:
        countries = sorted(co2_emissions["Country"].dropna().unique())
        country_col, fuel_col = st.columns(2)
        with country_col:
            country = st.selectbox("Country", ["All countries", *countries])
        with fuel_col:
            fuels = sorted(co2_emissions.loc[co2_emissions[EMISSIONS_COLUMN] > 0, "Fueltype"].dropna().unique())
            fuel = st.selectbox("Fuel", ["All fuels", *fuels])
        visible = co2_emissions if country == "All countries" else co2_emissions[co2_emissions["Country"] == country]
        if fuel != "All fuels":
            visible = visible[visible["Fueltype"] == fuel]
        visible = visible[(visible["Capacity"] > 0) & (visible[EMISSIONS_COLUMN] > 0)]
        fig = px.scatter(
            visible,
            x="Capacity",
            y=EMISSIONS_COLUMN,
            color="Fueltype",
            hover_name="Name",
            hover_data=["Country"],
            opacity=0.55,
            render_mode="webgl",
            labels={"Capacity": "Installed capacity (MW)", EMISSIONS_COLUMN: "tonnes CO₂/year", "Fueltype": "Fuel"},
            title="Capacity versus annual emissions per plant",
        )
        fig.update_layout(height=600)
        st.plotly_chart(fig, width="stretch")
        st.caption("Only plants with positive capacity and estimated operational emissions are shown.")

    with scenario_tab:
        st.caption("Illustrative phase-out of annual operational emissions; replacement generation is not modelled.")
        fuel_totals = co2_emissions.groupby("Fueltype")[EMISSIONS_COLUMN].sum().sort_values(ascending=False)
        selected_fuels = st.multiselect(
            "Fuels to phase out", fuel_totals[fuel_totals > 0].index.tolist(),
            default=[fuel for fuel in ("Hard Coal", "Lignite") if fuel in fuel_totals.index],
        )
        phase_out = st.slider("Phase-out percentage", 0, 100, 50, format="%d%%")
        baseline = co2_emissions[EMISSIONS_COLUMN].sum()
        reductions = fuel_totals.reindex(selected_fuels).fillna(0) * phase_out / 100
        scenario = baseline - reductions.sum()
        fig = go.Figure(go.Waterfall(
            x=["Current", *reductions.index.tolist(), "Scenario"],
            y=[baseline, *(-reductions).tolist(), scenario],
            measure=["absolute", *(["relative"] * len(reductions)), "total"],
            connector={"line": {"color": "#8b969b"}},
            decreasing={"marker": {"color": "#168574"}},
            totals={"marker": {"color": "#244a61"}},
            hovertemplate="%{x}: %{y:,.0f} t CO₂/year<extra></extra>",
        ))
        fig.update_layout(title="From current emissions to scenario", yaxis_title="tonnes CO₂/year", height=520)
        st.plotly_chart(fig, width="stretch")
        st.metric("Estimated scenario emissions", f"{scenario:,.0f} t CO₂/year", f"{-reductions.sum():,.0f} t CO₂/year", delta_color="inverse")
