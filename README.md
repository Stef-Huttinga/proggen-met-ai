# Streamlit Tutorial with `powerplantmatching` Data

This tutorial builds a minimal interactive dashboard
using [`streamlit`](https://streamlit.io/), [`plotly`](https://plotly.com/python/) and
the bundled dataset from [`powerplantmatching`](https://github.com/PyPSA/powerplantmatching).

## Installation

Install `uv`, then create the project environment and lock dependencies:

```sh
uv sync
```

The shell already provides the `UV_INDEX_ARTIFACTORY_USERNAME` and
`UV_INDEX_ARTIFACTORY_PASSWORD` variables used by `uv` when an Artifactory
index is configured for this project.

The app reads `powerplants.csv` from the repository, so it does not need a
network connection to load the data at runtime.

## Run Locally

In terminal, run:

```sh
uv run streamlit run app.py
```

## Files

```
├── requirements.txt      pip packages
├── powerplants.csv       local power-plant dataset
├── .streamlit            
│   └── config.toml       streamlit configuration file
├── app.py                streamlit app
├── LICENSE
└── README.md
```


## Learn More about Streamlit

To deepen your understanding of Streamlit, check out these resources:

- [Streamlit Official Documentation](https://docs.streamlit.io/)
- [Streamlit Tutorials on YouTube](https://youtube.com/playlist?list=PLgkF0qak9G4-TC9_tKW1V4GRcJ9cdmnlx&si=qbE4JUDV3iS8ksp1)
- [Streamlit Youtube channel for more](https://www.youtube.com/@streamlitofficial)
