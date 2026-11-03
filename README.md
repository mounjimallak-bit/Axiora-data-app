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
reaches a polygon in the shapefiles. It exits with code 1 while errors remain.

Corrected after the first run:

- Map joins sent Inezgane-Aït Melloul to a name absent from the shapefile, so the
  prefecture never appeared on any province map; one spelling of Chtouka-Aït Baha
  was missing from the population module's mapping, so it vanished from the 2018
  administrative-division map. The four modules now share one mapping table, and
  the script fails if any province name in the data does not reach a polygon.
- Several part-of-whole charts counted the total as a part: the households pie
  chart included the Souss-Massa row (always 50 % of the pie), and the sector and
  employment-status charts offered "Total" as a branch or status. A pie chart of
  employment rates (which do not add up) was removed.
- The Souss-Massa row of the 2016 to 2018 population estimates had 2016 and 2017
  swapped (and urban and rural swapped), and a digit error in 2018 urban. Rebuilt
  from the province rows, which are internally consistent.
- RGPH 2004 urban population of Chtouka-Aït Baha read 239,694, more than the
  province's municipalities plus every commune that has an urban centre (140,562
  in the HCP commune sheets). With 39,694 the provinces add up exactly to the
  regional figure. No HCP sheet gives the urban figure directly, so 39,694 is
  inferred.
- Unemployed aged 35-44, regional row: 12,984 corrected to 12,048 (urban + rural,
  and consistent with the row total).
- Commune poverty map: the "(AC)" centres were drawn on their commune's polygon,
  giving two values per polygon. They are now excluded from the map. Missing
  2004 and 2007 rates for these centres had been typed as 0; they are now empty.
- The commune map's middle KPI was labelled "Moyenne Régionale"; it is an
  unweighted mean of commune rates and is now labelled as such.
- The assistant prompt said the data were in thousands; most values are raw counts.

Re-entered from the HCP publications of the Souss-Massa regional directorate
(hcp.ma/region-agadir), after which every table passes:

- Poverty and vulnerability rates by commune, 2004, 2007 and 2014, checked
  column by column against the HCP sheets "Evolution des indicateurs de pauvreté
  2004, 2007 et 2014" for each province. Taroudannt's 2004 vulnerability column had
  lost one value near the end of the list (91 values for 92 rows). Drargua's poverty
  rates were shifted by one year: the app showed 26.2 % for 2014, the HCP figure is
  8.86 % (2004: 28.4 %, 2007: 11 %). Two Tata vulnerability values were corrected,
  and Inezgane-Aït Melloul, which had no commune data, was added.
- 2017 tourist arrivals and nights by nationality: re-entered from the 2017
  regional statistical yearbook (table Tourisme 3). The re-entered table adds up:
  every regional subtotal (Europe, North America, Arab countries, other) equals
  the sum of its countries, and international plus national equals the total.
- Primary school pupils by grade: the old table held only the girls' rows, with
  some cells shifted, and labelled them as teachers; the 2018 table was a copy of
  2017. Both years were re-entered from the 2017 and 2018 yearbooks (table
  Enseignement 11, public primary, all pupils), and the regional totals match the
  published ones.
- Teaching staff by sex, 2018: the women's column was shifted by one province.
  Re-entered from the 2018 yearbook (table Enseignement 7).

Not yet checked: the PDF report generator, which works on an uploaded file.

## Notes and Limitations

- The interface language is **French**, matching the source data.
- Projections use linear regression only; they extrapolate observed trends and
  should not be read as forecasts accounting for structural change.
- Indicator coverage depends on what HCP publishes; some series are available for
  a limited number of years.

---

## Author

**Malak Mounji**
Data & AI Engineering student, ENSA Agadir, Morocco

[GitHub](https://github.com/mounjimallak-bit) ·
[LinkedIn](https://www.linkedin.com/in/malakmounji/)
