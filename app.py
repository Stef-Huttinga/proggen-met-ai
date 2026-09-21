# SPDX-FileCopyrightText: 2023 Fabian Neumann (TU Berlin), 2023
#
# SPDX-License-Identifier: MIT

import streamlit as st

from data_io.data import load_co2_emissions, load_powerplants
from calculations.emissions import summarize_emissions
from ui.map import render_powerplant_map
from ui.overview import render_emissions_overview

st.set_page_config(page_title="Power Plants", layout="wide")
st.title("Power Plants in Europe")


powerplants = load_powerplants()
co2_emissions = load_co2_emissions()

render_emissions_overview(summarize_emissions(co2_emissions))
render_powerplant_map(powerplants)
