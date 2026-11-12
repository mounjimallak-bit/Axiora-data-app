# Axiora Data

[![checks](https://github.com/mounjimallak-bit/Axiora-data-app/actions/workflows/checks.yml/badge.svg)](https://github.com/mounjimallak-bit/Axiora-data-app/actions/workflows/checks.yml)

A validated dataset of official statistics for the Souss-Massa region of Morocco, a reproducible
descriptive analysis of poverty change between 2004 and 2014, and an interactive application for
exploring the data.

**Live application:** https://axiora-data.streamlit.app/
**Case study:** https://mounjimallak-bit.github.io/Portfolio/post/axiora/

| | |
|---|---|
| **Author** | Malak Mounji, Data Science, Big Data and AI engineering student, ENSA Agadir |
| **Context** | Personal project extending an internship at the HCP regional directorate for Souss-Massa (2025) |
| **Data** | Publications of the Haut-Commissariat au Plan (HCP), Morocco's national statistics institute |
| **Language of the interface** | French, as in the source publications |

---

## Overview

The HCP publishes regional statistics mainly as PDF yearbooks and spreadsheets, which makes
comparisons across years and territories slow and error-prone. This project:

1. **transcribes 48 HCP tables** on the Souss-Massa region into a single Python module (`hcpdata.py`):
   29 broken down by province, prefecture or commune and 19 at regional level or partial, drawn from
   the 2016–2018 regional yearbooks, the ENE 2017–2020 results and the 2004/2007/2014 poverty sheets,
   each with the publication it comes from;
2. **validates them automatically** (`validate_data.py`), with a test suite showing that typical
   transcription errors are detected (`test_validate_data.py`);
3. **answers a descriptive research question** with a reproducible script (`analyse_pauvrete.py`):
   *did poverty decline uniformly across the communes of Souss-Massa between 2004 and 2014, and
   where did it decline least?*;
4. **makes the data explorable** in a Streamlit application with maps, charts, a PDF report
   generator and a question-answering assistant.

---

## Data

| Source (HCP, Souss-Massa regional directorate) | Years | Used for |
|---|---|---|
| *Annuaire statistique régional* | 2016, 2017, 2018 | population, labour market (ENE 2016), housing, finance, education, health, tourism, energy |
| Legal population (RGPH), from the 2017 yearbook | 2004, 2014 | population by province |
| National employment survey (ENE), regional results | 2017–2020 | activity and employment rates |
| *Evolution des indicateurs de pauvreté* (one sheet per province or prefecture) | 2004, 2007, 2014 | poverty and vulnerability rates by commune |
| HCP administrative boundaries (ADM2, ADM3) | 2023 edition | provincial and commune maps |

The regional yearbooks can be downloaded from the HCP Souss-Massa website, https://www.hcp.ma/region-agadir/.

The source of every table is recorded in `SOURCES` in `hcpdata.py`, and each page of the
application states its own. The tables cover nine themes; the application's dashboards present
six of them (population, labour market, housing, finance, education, poverty), and the assistant
can answer questions on all nine.

---

## Methods

### Data validation

`validate_data.py` reads the tables as literals, without running the application, and checks that:

- the columns of each table have the same length;
- totals equal the sum of their parts, exactly for counts (urban + rural, men + women, provinces
  against the regional row, communes of each province against its total);
- every table that the application repeats from `hcpdata.py` has the same values as its source
  table, the copy being identified from its structure and year;
- every province and commune used in a map reaches exactly one polygon of the official boundary
  files, inside its own province (a commune name alone is not unique in Morocco);
- zeros in rate columns are reported for review, since a zero rate often stands for a missing value.

On the current data the script reports no errors. `test_validate_data.py` introduces six typical
errors one at a time in a copy of the data (a total off by one, a regional population off by
0.75 %, a 2018 table filled with the 2017 figures, among others) and checks that each is reported.

These checks establish internal consistency. Agreement with the publications was established by
comparing the tables with the yearbooks and poverty sheets.

### Poverty analysis

`analyse_pauvrete.py` describes the change in poverty rates between 2004, 2007 and 2014 at two levels:

- **geographic units**: the 179 communes and urban centres with a rate in all three years, each
  counted once (median, quartiles, interquartile range, unit-level change);
- **territories**: the population-weighted rate that the HCP publishes for each province or
  prefecture (its *Ensemble* row).

The two levels answer different questions (how local rates changed, and how poverty changed for
the population of each territory) and can rank the territories differently. No hypothesis test or
confidence interval is computed: the 179 units are the complete set of units with published rates,
not a random sample, and neighbouring units are not independent.

---

## Reproducing the results

```bash
git clone https://github.com/mounjimallak-bit/Axiora-data-app.git
cd Axiora-data-app
pip install -r requirements.txt

python validate_data.py            # data checks (exit code 1 if an error is found)
python test_validate_data.py       # tests of the checks
python test_app_pages.py           # every page of the app runs without an exception
python analyse_pauvrete.py --figures   # every number of the case study, and its two box plots
streamlit run app.py               # the application, at http://localhost:8501
```

Tested with Python 3.13 and streamlit 1.66.1, pandas 3.1.1, numpy 2.5.4, plotly 5.24.1,
geopandas 1.2.0, google-generativeai 0.8.6, fpdf 1.7.2, matplotlib 3.11.2, openpyxl 3.1.5,
Pillow 13.0.0.

The assistant needs a Google Gemini API key in `.streamlit/secrets.toml` (not versioned):

```toml
GEMINI_API_KEY = "your_api_key_here"
```

All other modules work without it.

---

## The application

| Module | Content |
|---|---|
| **Population** | Administrative division, legal population (RGPH 2004, 2014), estimates by setting, age structure, households |
| **Labour market** | Activity, employment and unemployment by age, sex, education, sector and status |
| **Housing** | Housing development operations by province (completed, launched, in progress, planned) |
| **Finance** | Bank deposits and credit, investment projects, companies created, GDP by sector |
| **Education** | First-year enrolment, teaching staff by sex, public primary pupils by grade |
| **Poverty** | Poverty and vulnerability rates by commune, 2014, on the commune map |

- **Maps.** Choropleth maps at provincial (ADM2) and commune (ADM3) level, built with GeoPandas and
  Plotly, and a dot map of enrolment and teaching staff by sex (one dot for 40 people, placed at
  random inside the province).
- **Charts.** Rows that add up territories ("Souss-Massa", "Total", "Ensemble") stay in the tables
  but are removed from the charts, so that a total is never compared with the territories it adds
  up. Shares in pie charts and percentage charts always refer to the published total, including
  when some categories are hidden.
- **Report generator.** Builds a descriptive PDF report (summary statistics, group comparison,
  extreme values, charts) from an Excel file uploaded by the user, reads numbers written in French
  or English format, and drops aggregate rows. Uploads are limited to 10 MB.
- **Assistant.** Answers questions in natural language with `gemini-2.5-flash`. Each call sends the
  tables of `hcpdata.py` and their sources as system instructions, with a low temperature (0.2) and
  the last six exchanges; it is limited to 6 questions per minute per session and 500 characters
  per question. Its answers are generated by the model and are not verified automatically against
  the tables. The application uses the `google-generativeai` SDK; Google recommends `google-genai`
  for new projects.

---

## Notes on sources

- **Unemployed aged 35–44, region, 2016.** The 2016 yearbook prints 12,984; the value used, 12,048,
  is the sum of its urban and rural parts (9,538 + 2,510) and the one consistent with the published
  total (84,411).
- **Two published totals that differ from the sum of their parts**, kept as published: first-year
  enrolment in Tiznit, 2018 (1,923 + 1,905 = 3,828 against a total of 3,826), and the Total row of
  the 2017 investment projects table (off by one in three columns).
- **ENE 2017 to 2020.** The 2019 and 2020 values match the HCP's published ENE indicators, except
  the rates for people with a diploma, which the HCP publishes split into two levels. For 2017, the
  activity rates by setting match the 2017 yearbook (Emploi, table 9), and the regional employment
  rates by sex and activity rates by diploma match the 2018 yearbook (Emploi, tables 4 and 7, which
  reprint ENE 2017). For 2018, the activity rates by setting are those of the 2018 yearbook (Emploi,
  table 9: 41.3 % urban, 46.0 % rural). The other 2017 and 2018 values could not be matched to a
  published table.
- **Tourist arrivals, 2017.** The yearbook gives the six provinces and prefectures only; the regional
  total columns are computed here as their sum. This table is used by the assistant only.

The application states each of these points under the table concerned.

---

## Limitations

- The tables are transcribed by hand; there is no automated import from HCP files.
- The 2004, 2007 and 2014 poverty rates come from three separate HCP poverty maps, whose
  comparability over time has not been established from the HCP methodology notes.
- Below the territory level, only unweighted statistics are possible, because the poverty sheets
  give no commune populations.
- Maps of counts show absolute values, which grow with the size of the province; comparing
  intensities would require dividing by the population.
- The analysis covers Souss-Massa only and is descriptive: it does not identify the causes of the
  territorial differences.
- Code organisation `app.py` (about 7,400 lines) holds every page in one file, with each page's tables copied inline next to its charts; `validate_data.py` checks every copy value by value against `hcpdata.py`. A modular layout (configuration, shared chart and map components, a PDF service, an assistant service, one module per page) is planned. It must keep the validator's contract, since the validator reads the application's tables as literals rather than running the app.

---

## Repository structure

```
Axiora-data-app/
├── app.py                          # Streamlit application
├── hcpdata.py                      # the 48 HCP tables and their sources
├── validate_data.py                # data checks
├── test_validate_data.py           # tests of the data checks
├── analyse_pauvrete.py             # poverty analysis of the case study
├── requirements.txt
├── .streamlit/config.toml          # upload size limit
├── assets/                         # logo and illustration
├── mar_admbnda_adm2_hcp_20230925/  # province and prefecture boundaries (shapefile)
└── mar_admbnda_adm3_hcp_20230925/  # commune boundaries (shapefile)
```

---

## Author

**Malak Mounji**, Data Science, Big Data and AI engineering student, ENSA Agadir, Morocco ·
[GitHub](https://github.com/mounjimallak-bit) · [LinkedIn](https://www.linkedin.com/in/malakmounji/)
