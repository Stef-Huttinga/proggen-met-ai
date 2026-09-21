# Power Plants in Europe

Een interactieve Streamlit-app voor het verkennen van Europese energiecentrales en
geschatte jaarlijkse operationele CO₂-uitstoot.

De app gebruikt data uit het `powerplantmatching`-project en toont centrales op een
kaart, met filters voor brandstoftype en ingebruiknamejaar.

## Installatie

Installeer [uv](https://docs.astral.sh/uv/) en maak de omgeving aan:

```sh
uv sync
```

De runtime gebruikt alleen de meegeleverde CSV-bestanden en heeft geen netwerkverbinding
nodig om de app te starten.

## Starten

```sh
uv run streamlit run app.py
```

## Databestanden

- `powerplants.csv` bevat de eigenschappen, locaties en metadata van centrales.
- `co2_emissions.csv` bevat per centrale de geschatte jaarlijkse CO₂-uitstoot.

Beide bestanden gebruiken dezelfde unieke `id`. De uitstootschatting is gebaseerd op
geïnstalleerd vermogen, een capaciteitsfactor en een directe emissiefactor.

## Projectstructuur

```text
app.py              Streamlit-applicatie
co2_emissions.csv   CO₂-schattingen per centrale
powerplants.csv     Centrale- en locatiegegevens
pyproject.toml      Projectmetadata en afhankelijkheden
```

Meer informatie over Streamlit staat in de
[officiële documentatie](https://docs.streamlit.io/).
