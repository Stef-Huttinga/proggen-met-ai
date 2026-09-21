from pathlib import Path

import pandas as pd
import streamlit as st


DATA_DIRECTORY = Path(__file__).resolve().parents[1]


@st.cache_data
def load_powerplants() -> pd.DataFrame:
    return pd.read_csv(DATA_DIRECTORY / "powerplants.csv", index_col=0)


@st.cache_data
def load_co2_emissions() -> pd.DataFrame:
    return pd.read_csv(DATA_DIRECTORY / "co2_emissions.csv")
