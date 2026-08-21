# Axiora Data — Socio-Economic Analytics Platform for Morocco

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
| **Type** | Personal project |
| **Author** | Malak Mounji — Data & AI Engineering student, ENSA Agadir |
| **Data source** | HCP Morocco — public open data (RGPH 2014 and related surveys) |
| **Status** | Deployed and publicly accessible |

---

## Overview

Public statistical data in Morocco is published mainly as spreadsheets, which
makes comparison across regions and over time slow and error-prone. Axiora Data
loads these tables, harmonises them, and exposes them through a single interface
where an indicator can be explored on a map, compared between provinces and
projected forward.

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

- **Report generator** — builds a structured PDF report from an uploaded dataset,
  including descriptive statistics, ranking tables and generated charts.
- **Axiora assistant** — a conversational module built on the Google Gemini API
  that answers natural-language questions about the loaded indicators.

---

## Features

### Interactive visualisation

- Choropleth maps at regional (**ADM2**) and provincial (**ADM3**) level, rendered
  with GeoPandas and Plotly
- Comparative charts across territories and time periods
- Filtering by year, region and indicator

### Trend projection

Linear regression (`scikit-learn`) is used to extrapolate indicator trends over
time and produce simple forward projections. The intent is to make direction and
magnitude of change readable, not to build a predictive model — the projections
are descriptive extrapolations of historical series.

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
├── hcpdata.py                      # HCP datasets and data preparation
├── requirements.txt
│
├── assets/
│   ├── logo.png
│   └── photo.png
│
├── mar_admbnda_adm2_hcp_20230925/  # Regional boundaries (shapefile)
└── mar_admbnda_adm3_hcp_20230925/  # Provincial boundaries (shapefile)
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

## Notes and Limitations

- The interface language is **French**, matching the source data.
- Projections use linear regression only; they extrapolate observed trends and
  should not be read as forecasts accounting for structural change.
- Indicator coverage depends on what HCP publishes; some series are available for
  a limited number of years.

---

## Author

**Malak Mounji**
Data & AI Engineering student — ENSA Agadir, Morocco

[GitHub](https://github.com/mounjimallak-bit) ·
[LinkedIn](https://www.linkedin.com/in/malakmounji/)
