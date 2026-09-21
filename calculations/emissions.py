from dataclasses import dataclass

import pandas as pd


EMISSIONS_COLUMN = "EstimatedAnnualCO2_tonnes"


@dataclass(frozen=True)
class EmissionsOverview:
    total_emissions: float
    country_emissions: pd.DataFrame
    fuel_emissions: pd.DataFrame
    country_fuel_emissions: pd.DataFrame


def summarize_emissions(co2_emissions: pd.DataFrame, top_country_count: int = 15) -> EmissionsOverview:
    country_emissions = (
        co2_emissions.groupby("Country", as_index=False)[EMISSIONS_COLUMN]
        .sum()
        .sort_values(EMISSIONS_COLUMN, ascending=False)
    )
    fuel_emissions = (
        co2_emissions.groupby("Fueltype", as_index=False)[EMISSIONS_COLUMN]
        .sum()
        .sort_values(EMISSIONS_COLUMN, ascending=False)
    )
    top_countries = country_emissions.head(top_country_count)["Country"]
    country_fuel_emissions = (
        co2_emissions.groupby(["Country", "Fueltype"], as_index=False)[EMISSIONS_COLUMN]
        .sum()
    )
    country_fuel_emissions = country_fuel_emissions[
        country_fuel_emissions["Country"].isin(top_countries)
    ]

    return EmissionsOverview(
        total_emissions=co2_emissions[EMISSIONS_COLUMN].sum(),
        country_emissions=country_emissions,
        fuel_emissions=fuel_emissions,
        country_fuel_emissions=country_fuel_emissions,
    )
