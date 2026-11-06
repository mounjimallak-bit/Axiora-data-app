# Axiora Data: Socio-Economic Analytics Platform for Morocco

An interactive **Streamlit** application for exploring, visualising and reporting on
Moroccan socio-economic indicators published by the **HCP** (Haut-Commissariat au
Plan, Morocco's national statistics institute).

The platform turns official statistical tables into interactive dashboards,
choropleth maps, trend projections and automatically generated PDF reports.

**Live application:** https://axiora-data.streamlit.app/

---

## Project Context

| | |
|---|---|
| **Type** | Personal project, extends my HCP internship work (2025) |
| **Author** | Malak Mounji, Data & AI Engineering student, ENSA Agadir |
| **Data source** | HCP Morocco, public open data (RGPH 2014 and related surveys) |
| **Status** | Deployed and publicly accessible |

---

## Overview

Public statistical data in Morocco is published mainly as spreadsheets, which
makes comparison across regions and over time slow and error-prone. For Axiora Data
I transcribed a set of these tables (Souss-Massa region) by hand into Python
dictionaries, and the app exposes them through a single interface where an
indicator can be explored on a map, compared between provinces and projected
forward. There is no automated import from HCP files, so the data is only as good
as the transcription; `validate_data.py` exists to check it (see Data checks below).

The application covers **six thematic domains**, plus two cross-cutting modules:

### Thematic modules

| Module | Content |
|---|---|
| **Population** | Demographic structure, urban/rural distribution, growth by province |
| **Labour market** | Activity, employment and unemployment indicators |
| **Housing** | Housing conditions and equipment |
| **Finance** | Household financial indicators |
| **Education** | Schooling and literacy indicators |
| **Poverty** | Poverty and vulnerability rates by territory |

### Cross-cutting modules

- **Report generator:** builds a structured PDF report from an uploaded dataset,
  including descriptive statistics, ranking tables and generated charts.
- **Axiora assistant:** a conversational module built on the Google Gemini API
  that answers natural-language questions about the loaded indicators.

---

## Features

### Interactive visualisation

- Choropleth maps at provincial (**ADM2**) and commune (**ADM3**) level, rendered
  with GeoPandas and Plotly
- Comparative charts across territories and time periods
- Filtering by year, province and indicator

### Trend projection

Linear regression (`scikit-learn`) is used to extrapolate indicator trends over
time and produce simple forward projections. The intent is to make direction and
magnitude of change readable, not to build a predictive model. Each line is fitted on the
full observed series, with no held-out evaluation: the projections are descriptive
extrapolations of short historical series.

### Automatic PDF reporting

The report generator accepts a user-supplied dataset and produces a formatted PDF
containing:

- a generated table of contents
- descriptive statistics for numeric columns
- top / bottom ranking tables
- group summary tables
- charts exported as images and embedded in the document

Built with `fpdf` and a custom `PDF` class handling headers, footers and TOC entries.

### Conversational assistant

A question-answering module built on `gemini-2.5-flash`. The API key is read from
Streamlit secrets and is never stored in the repository.

---

## Tech Stack

| Layer | Technology |
|---|---|
| **Interface** | Streamlit |
| **Data processing** | pandas, NumPy |
| **Visualisation** | Plotly, Matplotlib |
| **Geospatial** | GeoPandas |
| **Modelling** | scikit-learn (`LinearRegression`) |
| **Reporting** | fpdf, Kaleido (static chart export) |
| **LLM** | Google Generative AI (Gemini) |

---

## Repository Structure

```
Axiora-data-app/
│
├── app.py                          # Streamlit application (all modules)
├── hcpdata.py                      # HCP tables transcribed by hand (also the assistant's context)
├── validate_data.py                # consistency checks on the transcribed tables
├── analyse_pauvrete.py             # reproduces the poverty analysis of the case study
├── requirements.txt
│
├── assets/
│   ├── logo.png
│   └── photo.png
│
├── mar_admbnda_adm2_hcp_20230925/  # Province and prefecture boundaries (shapefile)
└── mar_admbnda_adm3_hcp_20230925/  # Commune boundaries (shapefile)
```

### About the shapefiles

The two `mar_admbnda_*` directories contain the official administrative boundary
shapefiles for Morocco. They are **required**: `app.py` loads them through
GeoPandas to render every choropleth map. Removing them disables all
cartographic features.

---

## Running Locally

### 1. Clone and install

```bash
git clone https://github.com/mounjimallak-bit/Axiora-data-app.git
cd Axiora-data-app
pip install -r requirements.txt
```

### 2. Configure the API key

The conversational assistant requires a Google Gemini API key. Create
`.streamlit/secrets.toml`:

```toml
GEMINI_API_KEY = "your_api_key_here"
```

This file is git-ignored. All other modules work without it.

### 3. Run

```bash
streamlit run app.py
```

The application opens at `http://localhost:8501`.

---


## Data checks

```bash
python validate_data.py
```

The script parses the tables in `hcpdata.py` and `app.py` without running the app
and checks that every column of a table has the same length, that totals match
their parts (Urbain + Rural, Hommes + Femmes, regional row vs provinces), that no
rate is a missing value typed as 0, and that every province and commune name
reaches a polygon in the shapefiles. It exits with code 1 while errors remain;
on the current data it reports no errors across 93 tables.

## Poverty analysis (case study)

```bash
python analyse_pauvrete.py --figures
```

Reproduces every number of the poverty analysis in the portfolio case study
(distributions, sign test, Wilcoxon test, bootstrap interval, results by territory)
from `hcpdata.py`, and writes the two box plots to `figures/`.

## Data provenance

The tables are transcribed from the public statistical publications of the HCP
Souss-Massa regional directorate (hcp.ma/region-agadir): the *Annuaire
statistique régional* for 2017 and 2018, the commune poverty sheets *Evolution
des indicateurs de pauvreté 2004, 2007 et 2014*, and the RGPH 2014 results. Most
numeric tables were cross-checked value by value against their source
publication. The three labour-market tables for 2017–2020 were taken from the
regional results of the ENE survey and were not checked cell by cell against a
single published table. The internal totals (province rows against the regional
row, Urbain + Rural, subtotals against their parts) are enforced by
`validate_data.py`.

Two points are documented rather than checked automatically:

- The RGPH 2004 urban population of Chtouka-Aït Baha is not given directly in any
  HCP sheet. It is set to 39,694, the value for which the province figures add up
  exactly to the published regional total; this is an inference, not a published
  figure.
- On the commune poverty map, the central KPI is the unweighted mean of commune
  rates (not a population-weighted regional rate) and is labelled as such.

The PDF report generator operates on a file the user uploads, so its output
depends on that file; it drops aggregate rows ("Total", "Région", "Ensemble")
before ranking or summing, and `validate_data.py` does not inspect uploaded files.

## Notes and Limitations

- The interface language is **French**, matching the source data.
- Projections use linear regression only; they extrapolate observed trends and
  should not be read as forecasts accounting for structural change.
- The 2004, 2007 and 2014 poverty rates come from three separate HCP poverty
  maps; their comparability over time has not been checked against the HCP
  methodology notes.
- Indicator coverage depends on what HCP publishes; some series are available for
  a limited number of years.

---

## Author

**Malak Mounji**
Data & AI Engineering student, ENSA Agadir, Morocco

[GitHub](https://github.com/mounjimallak-bit) ·
[LinkedIn](https://www.linkedin.com/in/malakmounji/)
