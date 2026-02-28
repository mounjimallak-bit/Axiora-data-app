from sklearn.linear_model import LinearRegression
from PIL import Image
import base64
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import google.generativeai as genai
import json
from hcpdata import hcp_data
from fpdf import FPDF
from datetime import datetime
import os
import geopandas as gpd
import os
import plotly.io as pio


# --- Configuration page ---
st.set_page_config(
    page_title="Axiora Data",
    page_icon="assets/logo.png",
    layout="wide"
)


# --- Fonction pour convertir une image en base64 ---
def image_to_base64(image_path):
    with open(image_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


# --- CSS sidebar ---
st.markdown("""
<style>
section[data-testid="stSidebar"] {
    background-color: #1E293B; /* bleu foncé */
    color: white;
    padding: 15px;F
}
.stButton>button {
    background-color: transparent;
    border: none;
    padding: 4px 0;
    text-align: left;
    color: white;
    font-size: 12px;        /* texte plus petit */
    font-weight: 400;
    cursor: pointer;
}
.stButton>button:hover {
    color: #e6ecf2;
    text-decoration: underline;
    background-color: transparent;
}
section[data-testid="stSidebar"] * {
    color: white !important;
    font-size: 12px !important;
}
</style>
""", unsafe_allow_html=True)
st.markdown("""
<style>
/* Header principal */
h1 {
    font-family: 'Cinzel', cursive;
    color: #E5E7EB;
    margin: 0 0 20px 0;
    font-size: 48px; 
    font-weight: 900; 
    text-align: center; /* centré horizontalement */
}

/* Texte secondaire */
.subtitle-text {
    font-family: 'Dancing Script', cursive;
    color: #3f3f54;
    font-size: 22px;
    text-align: center;
    margin-bottom: 40px;
}

/* Cards */
.card {
    background: linear-gradient(135deg, #1E293B, #374151);
    border-radius: 15px;
    padding: 15px;
    text-align: center;
    box-shadow: 0px 4px 8px rgba(0,0,0,0.3);
    color: white;
    margin-bottom: 10px;
    margin-left: auto;
    margin-right: auto; /* centre horizontalement */
}
.card p {
    font-size: 24px;
    font-weight: bold;
    margin: 5px 0;
}
.card h3 {
    font-size: 14px;
    margin: 5px 0;
    color: #E5E7EB;
}
.arrow-up { color: #a6c69f; font-size: 14px; }
.arrow-down { color: #b52b2b; font-size: 14px; }
.arrow-stable { color: #e0e060; font-size: 14px; }

/* Titre style pillule */
.title-pill {
    display: inline-flex; 
    align-items: center; 
    background-color:  #a3a8ad;
    color: #ffffff; 
    padding: 12px 24px;   
    border-radius: 30px; 
    font-size: 28px;      
    font-weight: 500; 
    white-space: nowrap; 
    line-height: 1.2; 
    text-align:center;
    margin-left: auto;
    margin-right: auto; /* centre horizontalement */
}

/* Supprime padding horizontal pour titre pleine largeur */
div[data-testid="stAppViewContainer"] > div:first-child {
    padding-left: 0px;
    padding-right: 0px;
}

/* Responsive */
@media (max-width: 768px) {
    .card p { font-size: 20px; }
    .title-pill { font-size: 22px; padding: 10px 20px; }
}
</style>
""", unsafe_allow_html=True)

# --- Session state ---
if "page" not in st.session_state:
    st.session_state.page = "Accueil"
if "indices_open" not in st.session_state:
    st.session_state.indices_open = False


# --- Fonctions ---
def go_to(page_name):
    st.session_state.page = page_name
    st.session_state.indices_open = False  # referme après clic sous-menu


def toggle_indices():
    st.session_state.indices_open = not st.session_state.indices_open


# --- Sidebar ---
logo_base64 = image_to_base64("assets/logo.png")
st.sidebar.markdown(f'''
<div style="display:flex; align-items:center; padding:10px; margin-bottom:20px;">
    <img src="data:image/png;base64,{logo_base64}" style="height:28px; margin-right:8px;">
    <h3 style="margin:0; font-size:14px;">Axiora Data</h3>
</div>
''', unsafe_allow_html=True)
st.sidebar.markdown('<h4 style="color:white; margin-top:0; margin-bottom:10px;">Menu Principal</h4>',
                    unsafe_allow_html=True)  # --- Menu principal ---
if st.sidebar.button("▶ Accueil"):
    go_to("Accueil")

# --- Indices accordéon ---
label = "▼ Exploration des Indices" if st.session_state.indices_open else "▶ Exploration des Indices"
st.sidebar.button(label, key="indices_toggle", on_click=toggle_indices)

if st.session_state.indices_open:
    if st.sidebar.button("Population"):
        go_to("Population")
    if st.sidebar.button("Marche de Travail"):
        go_to("Marche de Travail")
    if st.sidebar.button("Habitat"):
        go_to("Habitat")
    if st.sidebar.button("Finance"):
        go_to("Finance")
    if st.sidebar.button("Enseignement"):
        go_to("Enseignement")
    if st.sidebar.button("pauvrete"):
        go_to("pauvrete")


if st.sidebar.button("▶ Generateur Rapport & statistiques"):
    go_to("Generateur Rapport & statistiques")
if st.sidebar.button("▶ assistant axiora data "):
    go_to("assistant axiora data")
if st.sidebar.button("▶ Aide & contact"):
    go_to("Aide & contact")

# --- Routing ---
if st.session_state.page == "Population":
    st.markdown("<br>", unsafe_allow_html=True)

    st.set_page_config(layout="wide")

    st.markdown("""
    <style>
    .block-container {
        padding: 0;
        margin: 0;
        max-width: 100%;
    }

    .full-width-bar {
        width: 100%;
        background-color: #1E293B;
        padding: 15px 20px;  /* réduit les paddings */
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-sizing: border-box;
    }

    .bar-logo {
        font-family: 'Playfair Display', serif;
        color: white;
        font-size: 24px;   /* légèrement réduit */
        font-weight: 900;
    }

    .bar-menu {
        display: flex;
        gap: 10px;           /* réduit l’espace entre liens */
        max-width: 70%;       /* limite la largeur du menu pour éviter le dépassement */
        overflow-x: auto;     /* permet le défilement si écran trop petit */
    }

    .bar-menu a {
        color: white;
        text-decoration: none;
        font-size: 14px;      /* réduit la taille du texte */
        font-weight: 600;
        white-space: nowrap;  /* empêche le texte de passer à la ligne */
    }

    .bar-menu a:hover {
        color: #60A5FA;
    }

    .bar-menu .button {
        background-color: #3b82f6;
        padding: 5px 10px;
        border-radius: 6px;
        font-size: 14px;
        font-weight: 600;
    }

    .bar-menu .button:hover {
        background-color: #2563eb;
    }
    </style>

    <div class="full-width-bar">
        <div class="bar-logo">Axiora Data</div>
        <div class="bar-menu">
            <a href="#">App Marketing Agency</a>
            <a href="#">ASO Agency</a>
            <a href="#">Glossary</a>
            <a href="#">Data</a>
            <a href="#">ASO Tools</a>
            <a href="#" class="button">Read Blog</a>
        </div>
    </div>

    <div style="height: 60px;"></div>
    """, unsafe_allow_html=True)

    ###

    # --- CSS pour checkboxes bleu-gris ---
    st.markdown("""
    <style>
    /* Contour de la case */
    div.stCheckbox div[role="checkbox"] {
        border: 2px solid #3e5c76 !important;
        border-radius: 4px;
    }

    /* Coche à l’intérieur */
    div.stCheckbox input:checked + div svg {
        stroke: #1c354f !important;
    }

    /* Texte du label */
    div.stCheckbox label span {
        color: #1c354f !important;
        font-weight: 500;
    }
    </style>
    """, unsafe_allow_html=True)

    # --- Données ---

    # --- Données par année ---
    data_2017 = {
        "Province": ["Agadir Ida Outanane", "Inezgane-Aït Melloul", "Chtouka-Aït Baha", "Taroudant", "Tiznit", "Tata"],
        "Urbaines": [1, 2, 2, 8, 2, 4],
        "Rurales": [11, 4, 20, 81, 23, 16],
        "Total Communes": [12, 6, 22, 89, 25, 20],
        "Cercles": [1, 1, 2, 5, 3, 3]
    }

    data_2018 = {
        "Province": ["Agadir Ida Outanane", "Inezgane Ait Melloul", "Chtouka Ait Baha", "Taroudant", "Tiznit", "Tata"],
        "Urbaines": [1, 4, 2, 8, 2, 4],
        "Rurales": [12, 2, 20, 81, 23, 16],
        "Total Communes": [13, 6, 22, 89, 25, 20],
        "Cercles": [2, 1, 3, 5, 3, 3]
    }

    # --- Choix de l'année ---
    st.markdown("""
        <h4 style=' color: #85919e;margin-left: 110px;'>
                       1 – Division administrative de la région
        </h4>
        """, unsafe_allow_html=True)
    st.markdown("<br><br>", unsafe_allow_html=True)
    # --- Création de la mise en page 3 colonnes ---
    col11, col22, col33 = st.columns([0.1, 1, 0.1])
    with col22:
        col1, col2, col3 = st.columns([1, 2, 1])

        # --- Colonne 1 : choix utilisateur ---
        with col1:

            year_options = ["2017", "2018"]
            selected_year = st.selectbox("Choisir l'année", year_options)

            # --- Charger le DataFrame correspondant ---
            if selected_year == "2017":
                df = pd.DataFrame(data_2017)
            else:
                df = pd.DataFrame(data_2018)

            graph_options = ["Courbes multiples", "Barres groupées", "Scatter multi-dimension"]
            graph_type = st.selectbox("Type de graphique", graph_options, index=0)

            st.markdown("<h9 style='color:#3e5c76;'>Sélectionnez les indicateurs à afficher</h9>",
                        unsafe_allow_html=True)
            show_urbaines = st.checkbox("Urbaines", True, key="chec1")
            show_rurales = st.checkbox("Rurales", True, key="chec2")
            show_total = st.checkbox("Total Communes", True, key="chec3")
            show_cercles = st.checkbox("Cercles", True, key="chec4")

        # --- Construire liste des colonnes à afficher ---
        columns_to_plot = []
        if show_urbaines: columns_to_plot.append("Urbaines")
        if show_rurales: columns_to_plot.append("Rurales")
        if show_total: columns_to_plot.append("Total Communes")
        if show_cercles: columns_to_plot.append("Cercles")

        # --- Colonne 2 : graphique ---
        with col2:
            if not columns_to_plot:
                st.warning("⚠ Veuillez sélectionner au moins un indicateur !")
            else:
                if graph_type == "Barres groupées":
                    colors = ["#a83232", "#8799ad", "#a19d37", "#c1cddf"]
                    fig = px.bar(df, x="Province", y=columns_to_plot, barmode="group",
                                 color_discrete_sequence=colors[:len(columns_to_plot)])
                    st.plotly_chart(fig, use_container_width=True)
                elif graph_type == "Courbes multiples":
                    colors = ["#1c354f", "#a19d37", "#a83232", "#8799ad"]
                    fig = px.line(df, x="Province", y=columns_to_plot, markers=True,
                                  color_discrete_sequence=colors[:len(columns_to_plot)])
                    st.plotly_chart(fig, use_container_width=True)
                elif graph_type == "Scatter multi-dimension":
                    x_col = "Total Communes" if "Total Communes" in columns_to_plot else columns_to_plot[0]
                    y_col = "Cercles" if "Cercles" in columns_to_plot else columns_to_plot[0]
                    size_col = "Rurales" if "Rurales" in columns_to_plot else columns_to_plot[0]
                    color_col = "Urbaines" if "Urbaines" in columns_to_plot else columns_to_plot[0]
                    fig = px.scatter(df, x=x_col, y=y_col, size=size_col, color=color_col,
                                     text="Province",
                                     color_continuous_scale=px.colors.sequential.Blues)
                    fig.update_traces(textposition="top center")
                    st.plotly_chart(fig, use_container_width=True)

        # --- Colonne 3 : aperçu du tableau brut ---
        with col3:
            st.markdown("<br><br>", unsafe_allow_html=True)
            st.dataframe(df, use_container_width=True)

        ####### pree tab 1

        st.markdown("""
        <div style='
            background-color: #aab5bf;
            border-radius: 12px;
            padding: 8px 16px;
            text-align: center;
            color: white;
            font-weight: bold;
            font-size: 18px;
            display: inline-block;
        '>
            Analyse Comparative et Évolution des Données
        </div>
        """, unsafe_allow_html=True)

        df_2017 = pd.DataFrame(data_2017)
        df_2018 = pd.DataFrame(data_2018)

        # ================== Préparation ==================
        df = df_2017.rename(columns={"Urbaines": "2017-Urbaines", "Rurales": "2017-Rurales",
                                     "Total Communes": "2017-Total Communes", "Cercles": "2017-Cercles"})
        df["2018-Urbaines"] = df_2018["Urbaines"]
        df["2018-Rurales"] = df_2018["Rurales"]
        df["2018-Total Communes"] = df_2018["Total Communes"]
        df["2018-Cercles"] = df_2018["Cercles"]

        # ================== Streamlit ==================
        col1, col2, col3 = st.columns([1.5, 3, 1])

        # --- Col1 : texte explicatif ---
        with col1:
            st.markdown("<br><br><br><br>", unsafe_allow_html=True)
            st.markdown("""
            Comparaison des communes et cercles entre 2017 et 2018 pour chaque province. 

            """)
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("""

                        Les changements sont plus visibles sur les communes urbaines et le nombre de cercles.
                        """)

        # --- Col3 : options ---
        with col3:
            st.markdown("<br><br><br>", unsafe_allow_html=True)
            indicators = ["Total Communes", "Urbaines", "Rurales", "Cercles"]
            selected_indicator = st.selectbox(
                "Indicateur", indicators, index=0, key="indicator_communes"
            )
            graph_options = ["Bar Plot comparatif", "Évolution", "Variation %", "Prévision"]
            graph_type = st.selectbox(
                "Graphique", graph_options, index=0, key="graph_type_communes"  # Évolution par défaut
            )

        # --- Col2 : graphique ---
        with col2:
            years = [2017, 2018]
            cols = [f"{year}-{selected_indicator}" for year in years]

            if graph_type == "Bar Plot comparatif":
                col_y1, col_y2 = cols[0], cols[1]
                fig = px.bar(
                    df, x="Province", y=[col_y1, col_y2], barmode="group",
                    color_discrete_sequence=["#e3e3a1", "#8d93a8"]
                )

            elif graph_type == "Évolution":
                df_melt = df.melt(
                    id_vars="Province", value_vars=cols,
                    var_name="Année", value_name=selected_indicator
                )
                df_melt["Année"] = df_melt["Année"].str.extract(r"(\d{4})").astype(int)
                fig = px.line(
                    df_melt, x="Année", y=selected_indicator, color="Province",
                    markers=True, color_discrete_sequence=px.colors.qualitative.Set2
                )

            elif graph_type == "Variation %":
                col_y1, col_y2 = cols[0], cols[1]
                df["Variation %"] = ((df[col_y2] - df[col_y1]) / df[col_y1] * 100).round(2)
                fig = px.bar(
                    df, x="Province", y="Variation %", color="Variation %",
                    color_continuous_scale=["#758a72", "#7a3d2c", "#abb1d6", "#dede85"]
                )

            elif graph_type == "Prévision":
                df_melt = df.melt(
                    id_vars="Province", value_vars=cols,
                    var_name="Année", value_name=selected_indicator
                )
                df_melt["Année"] = df_melt["Année"].str.extract(r"(\d{4})").astype(int)

                predictions = []
                for prov in df["Province"]:
                    sub = df_melt[df_melt["Province"] == prov]
                    X = sub["Année"].values.reshape(-1, 1)
                    y = sub[selected_indicator].values
                    model = LinearRegression().fit(X, y)
                    future_years = np.array([2019, 2020, 2021]).reshape(-1, 1)
                    y_pred = model.predict(future_years)
                    for yr, val in zip([2019, 2020, 2021], y_pred):
                        predictions.append({"Province": prov, "Année": yr, selected_indicator: val})

                df_pred = pd.DataFrame(predictions)
                df_all = pd.concat([df_melt, df_pred])
                fig = px.line(
                    df_all, x="Année", y=selected_indicator, color="Province",
                    markers=True, color_discrete_sequence=px.colors.qualitative.Set2
                )

            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        ################# taaaaab 22222
        st.markdown("""
               <h4 style=' color: #85919e;margin-left: 0px;'>
                              2 – Population légale selon provinces et préfectures						
               </h4>
               """, unsafe_allow_html=True)
        st.markdown("<br><br>", unsafe_allow_html=True)

        data = {
            "Provinces": [
                "Agadir Ida Outanane", "Inezgane-Aït Melloul", "Chtouka-Aït Baha",
                "Taroudant", "Tiznit", "Tata", "Souss-Massa"
            ],
            "RGPH 2004 – Urbain": [384987, 385612, 239694, 186471, 58613, 39060, 1094437],
            "RGPH 2004 – Total": [487954, 419614, 297245, 780661, 217050, 121618, 2324142],
            "RGPH 2014 – Urbain": [508155, 513706, 113531, 248640, 81044, 40820, 1505896],
            "RGPH 2014 – Total": [600599, 541118, 371102, 838820, 207367, 117841, 2676847],
        }

        df = pd.DataFrame(data)
        col1, col2, col3 = st.columns([2, 1, 1])  # 1 : Graphique, 2 : tableau, 3 : choix

        # --- Colonne 3 : choix utilisateur ---
        with col3:
            st.markdown("<br><br>", unsafe_allow_html=True)
            graph_options = ["Area Miroir", "Line Plot", "Heatmap", "Bar Plot"]
            graph_type = st.selectbox("Type de graphique", graph_options, index=0)

            st.markdown("<h5 style='color:#3e5c76;'>Sélectionnez les indicateurs à afficher</h5>",
                        unsafe_allow_html=True)
            show_urbaines = st.checkbox("Urbaines 2004/2014", True, key="chec5")
            show_total = st.checkbox("Total 2004/2014", True, key="chec6")

        # --- Construire liste des colonnes à afficher ---
        columns_to_plot = []
        if show_urbaines: columns_to_plot.append("Urbain")
        if show_total: columns_to_plot.append("Total")

        # --- Colonne 1 : graphique ---
        with col1:
            if not columns_to_plot:
                st.warning("⚠ Veuillez sélectionner au moins un indicateur !")
            else:
                if graph_type == "Area Miroir":
                    fig = go.Figure()
                    # Total d'abord, Urbain après pour visibilité
                    if "Total" in columns_to_plot:
                        fig.add_trace(go.Scatter(
                            x=df["Provinces"],
                            y=df["RGPH 2004 – Total"],
                            fill='tozeroy', mode='none', name="2004 Total", fillcolor='#b36b6b'
                        ))
                        fig.add_trace(go.Scatter(
                            x=df["Provinces"],
                            y=[-val for val in df["RGPH 2014 – Total"]],
                            fill='tozeroy', mode='none', name="2014 Total", fillcolor='#802828'
                        ))
                    if "Urbain" in columns_to_plot:
                        fig.add_trace(go.Scatter(
                            x=df["Provinces"],
                            y=df["RGPH 2004 – Urbain"],
                            fill='tozeroy', mode='none', name="2004 Urbain", fillcolor='#7ea6c2'
                        ))
                        fig.add_trace(go.Scatter(
                            x=df["Provinces"],
                            y=[-val for val in df["RGPH 2014 – Urbain"]],
                            fill='tozeroy', mode='none', name="2014 Urbain", fillcolor='#5a7b8c'
                        ))
                    fig.update_layout(
                        yaxis=dict(
                            tickvals=[-3000000, -2000000, -1000000, 0, 1000000, 2000000, 3000000],
                            ticktext=[3_000_000, 2_000_000, 1_000_000, 0, 1_000_000, 2_000_000, 3_000_000],
                            title="Population"
                        ),
                        xaxis=dict(title="Provinces", tickfont=dict(size=8)),
                        template="plotly_white"
                    )
                    st.plotly_chart(fig, use_container_width=True)

                elif graph_type == "Line Plot":
                    colors = ["#7ea6c2", "#5a7b8c", "#b36b6b", "#802828"]
                    fig = px.line(df, x="Provinces", y=[col for col in df.columns if "Urbain" in col or "Total" in col],
                                  markers=True, color_discrete_sequence=colors)
                    st.plotly_chart(fig, use_container_width=True)

                elif graph_type == "Heatmap":
                    heat_data = df[[col for col in df.columns if "Urbain" in col or "Total" in col]]
                    fig = px.imshow(heat_data.T, x=df["Provinces"], y=heat_data.columns,
                                    color_continuous_scale='blues')
                    st.plotly_chart(fig, use_container_width=True)

                elif graph_type == "Bar Plot":
                    colors = ["#7ea6c2", "#5a7b8c", "#b36b6b", "#802828"]
                    fig = px.bar(df, x="Provinces", y=[col for col in df.columns if "Urbain" in col or "Total" in col],
                                 barmode="group", color_discrete_sequence=colors)
                    st.plotly_chart(fig, use_container_width=True)

        # --- Colonne 2 : aperçu du tableau brut ---
        with col2:
            st.markdown("<br><br>", unsafe_allow_html=True)

            st.dataframe(df, use_container_width=True)
        #############previsualisation tab 2

        st.markdown("""
                <div style='
                    background-color: #aab5bf;
                    border-radius: 12px;
                    padding: 8px 16px;
                    text-align: center;
                    color: white;
                    font-weight: bold;
                    font-size: 18px;
                    display: inline-block;
                '>
                    Analyse Comparative et Évolution des Données
                </div>
                """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1.5, 3, 1])

        # --- Col1 : texte explicatif ---
        with col1:
            st.markdown("<br><br><br><br><br>", unsafe_allow_html=True)
            st.markdown("""
            Entre 2004 et 2014, la population des provinces a globalement augmenté .

            """)
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("""

                       Une croissance plus marquée en milieu urbain.
                       """)

        # --- Col3 : options ---
        with col3:
            st.markdown("<br><br><br>", unsafe_allow_html=True)
            indicators = ["Total", "Urbain"]
            selected_indicator = st.selectbox(
                "Indicateur", indicators, index=1, key="indicator_rgph"
            )
            graph_options = ["Bar Plot comparatif", "Évolution", "Variation %", "Prévision"]
            graph_type = st.selectbox(
                "Graphique", graph_options, index=3, key="graph_type_rgph"  # Évolution par défaut
            )

        # --- Col2 : graphique ---
        with col2:
            years = [2004, 2014]
            cols = [f"RGPH {year} – {selected_indicator}" for year in years]

            if graph_type == "Bar Plot comparatif":
                col_y1, col_y2 = cols[0], cols[1]
                fig = px.bar(
                    df, x="Provinces", y=[col_y1, col_y2], barmode="group",
                    color_discrete_sequence=["#1c354f", "#7a3d2c"]
                )

            elif graph_type == "Évolution":
                df_melt = df.melt(
                    id_vars="Provinces", value_vars=cols,
                    var_name="Année", value_name="Population"
                )
                df_melt["Année"] = df_melt["Année"].str.extract(r"(\d{4})").astype(int)
                fig = px.line(
                    df_melt, x="Année", y="Population", color="Provinces",
                    markers=True, color_discrete_sequence=px.colors.qualitative.Set2
                )

            elif graph_type == "Variation %":
                col_y1, col_y2 = cols[0], cols[1]
                df["Variation %"] = ((df[col_y2] - df[col_y1]) / df[col_y1] * 100).round(2)
                fig = px.bar(
                    df, x="Provinces", y="Variation %", color="Variation %",
                    color_continuous_scale=["#758a72", "#7a3d2c", "#abb1d6", "#dede85"]
                )

            elif graph_type == "Prévision":
                df_melt = df.melt(
                    id_vars="Provinces", value_vars=cols,
                    var_name="Année", value_name="Population"
                )
                df_melt["Année"] = df_melt["Année"].str.extract(r"(\d{4})").astype(int)

                predictions = []
                for prov in df["Provinces"]:
                    sub = df_melt[df_melt["Provinces"] == prov]
                    X = sub["Année"].values.reshape(-1, 1)
                    y = sub["Population"].values
                    model = LinearRegression().fit(X, y)
                    future_years = np.array([2015, 2016, 2017, 2018, 2019]).reshape(-1, 1)
                    y_pred = model.predict(future_years)
                    for yr, val in zip([2015, 2016, 2017, 2018, 2019], y_pred):
                        predictions.append({"Provinces": prov, "Année": yr, "Population": val})

                df_pred = pd.DataFrame(predictions)
                df_all = pd.concat([df_melt, df_pred])
                fig = px.line(
                    df_all, x="Année", y="Population", color="Provinces",
                    markers=True, color_discrete_sequence=px.colors.qualitative.Set2
                )

            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

            #####tab3
        st.markdown("""
                      <h4 style=' color: #85919e;margin-left: 0px;'>
                                    3 – Estimations de la population selon le milieu de résidence														
                      </h4>
                      """, unsafe_allow_html=True)

        # --- Données 2016–2018 ---
        data = {
            "Provinces": [
                "Agadir Ida Outanane", "Inezgane Aït Melloul", "Chtouka Aït Baha",
                "Taroudant", "Tata", "Tiznit", "Souss-Massa"
            ],
            "2016 – Urbain": [535653, 539975, 125818, 260214, 41417, 85357, 1143390],
            "2016 – Rural": [89307, 27595, 258625, 582540, 74937, 119786, 1635380],
            "2016 – Total": [624960, 567570, 384443, 842754, 116354, 205143, 2778770],

            "2017 – Urbain": [551240, 554820, 133050, 266730, 41740, 87800, 1152790],
            "2017 – Rural": [87650, 27710, 259260, 578550, 73840, 116380, 1588434],
            "2017 – Total": [638890, 582530, 392310, 845280, 115580, 204180, 2741224],

            "2018 – Urbain": [567055, 569865, 140642, 273306, 42054, 90276, 1168198],
            "2018 – Rural": [86032, 27806, 259843, 574518, 72752, 113055, 1134006],
            "2018 – Total": [653087, 597671, 400485, 847824, 114806, 203331, 2817204],
        }
        df = pd.DataFrame(data)

        # --- Palette perso ---
        custom_colors = ["#1c354f", "#4d0f14", "#758a72"]

        # --- Layout colonnes ---
        col1, col2, col3 = st.columns([1, 2, 1])

        # --- Colonne 1 : choix utilisateur ---
        with col1:
            year_options = ["2016", "2017", "2018"]
            selected_year = st.selectbox("Choisir l'année", year_options)
            graph_options = ["scatter chart", "Line Plot", "Bar Plot"]
            graph_type = st.selectbox("Type de graphique", graph_options, index=2)

            show_urbain = st.checkbox("Urbain", True, key="chec7")
            show_rural = st.checkbox("Rural", True, key="chec8")
            show_total = st.checkbox("Total", True, key="chec9")

        # --- Colonnes à afficher selon sélection ---
        columns_to_plot = []
        if show_urbain:
            columns_to_plot.append(f"{selected_year} – Urbain")
        if show_rural:
            columns_to_plot.append(f"{selected_year} – Rural")
        if show_total:
            columns_to_plot.append(f"{selected_year} – Total")

        # --- Colonne 2 : tableau + graphique ---
        with col2:
            if not columns_to_plot:
                st.warning("⚠ Veuillez sélectionner au moins un indicateur !")
            else:
                # --- Graphiques ---
                if graph_type == "Line Plot":
                    fig = px.line(
                        df, x="Provinces", y=columns_to_plot, markers=True,
                        color_discrete_sequence=custom_colors
                    )
                    st.plotly_chart(fig, use_container_width=True)

                elif graph_type == "scatter chart":
                    if len(columns_to_plot) >= 2:
                        x_col = columns_to_plot[0]
                        y_col = columns_to_plot[1]
                    else:
                        # si un seul indicateur choisi → x = Provinces, y = colonne
                        x_col = "Provinces"
                        y_col = columns_to_plot[0]

                    fig = px.scatter(
                        df, x=x_col, y=y_col, text="Provinces",
                        size_max=20, color_discrete_sequence=custom_colors
                    )
                    fig.update_traces(textposition="top center")
                    st.plotly_chart(fig, use_container_width=True)

                else:  # Bar Plot
                    fig = px.bar(
                        df, x="Provinces", y=columns_to_plot, barmode="group",
                        color_discrete_sequence=custom_colors
                    )
                    st.plotly_chart(fig, use_container_width=True)

        # --- Colonne 3 : tableau ---
        with col3:
            st.dataframe(df[["Provinces"] + columns_to_plot], use_container_width=True)
        ######prevision tab 3

        st.markdown("""
                <div style='
                    background-color: #aab5bf;
                    border-radius: 12px;
                    padding: 8px 16px;
                    text-align: center;
                    color: white;
                    font-weight: bold;
                    font-size: 18px;
                    display: inline-block;
                '>
                    Analyse Comparative et Évolution des Données
                </div>
                """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1.5, 3, 1])

        # --- Col1 : texte explicatif ---
        with col1:
            st.markdown("<br><br><br><br><br>", unsafe_allow_html=True)
            st.markdown("""
            Entre 2016 et 2018, la population progresse dans la plupart des provinces, 

            """)
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("""

                        Une dynamique plus marquée en milieu urbain que rural.
                        """)

        # --- Col3 : options ---
        with col3:
            st.markdown("<br><br><br>", unsafe_allow_html=True)
            indicators = ["Total", "Urbain", "Rural"]
            selected_indicator = st.selectbox(
                "Indicateur", indicators, index=0, key="indicator_province"
            )
            graph_options = ["Bar Plot comparatif", "Évolution", "Variation %", "Prévision"]
            graph_type = st.selectbox(
                "Graphique", graph_options, index=1, key="graph_type_province"  # Prévision par défaut
            )

        # --- Col2 : graphique ---
        with col2:
            years = [2016, 2017, 2018]
            cols = [f"{year} – {selected_indicator}" for year in years]

            if graph_type == "Bar Plot comparatif":
                year1, year2 = st.select_slider(
                    "Comparer", options=years, value=(2016, 2018), key="compare_years_province"
                )
                col_y1, col_y2 = f"{year1} – {selected_indicator}", f"{year2} – {selected_indicator}"
                fig = px.bar(
                    df, x="Provinces", y=[col_y1, col_y2], barmode="group",
                    color_discrete_sequence=["#1c354f", "#7a3d2c"]
                )

            elif graph_type == "Évolution":
                df_melt = df.melt(
                    id_vars="Provinces", value_vars=cols,
                    var_name="Année", value_name="Population"
                )
                df_melt["Année"] = df_melt["Année"].str.extract(r"(\d{4})").astype(int)
                fig = px.line(
                    df_melt, x="Année", y="Population", color="Provinces",
                    markers=True, color_discrete_sequence=px.colors.qualitative.Set2
                )

            elif graph_type == "Variation %":
                year1, year2 = st.select_slider(
                    "Comparer", options=years, value=(2016, 2018), key="compare_variation_province"
                )
                col_y1, col_y2 = f"{year1} – {selected_indicator}", f"{year2} – {selected_indicator}"
                df["Variation %"] = ((df[col_y2] - df[col_y1]) / df[col_y1] * 100).round(2)
                fig = px.bar(
                    df, x="Provinces", y="Variation %", color="Variation %",
                    color_continuous_scale=["#758a72", "#7a3d2c", "#abb1d6", "#dede85"]
                )

            elif graph_type == "Prévision":
                df_melt = df.melt(
                    id_vars="Provinces", value_vars=cols,
                    var_name="Année", value_name="Population"
                )
                df_melt["Année"] = df_melt["Année"].str.extract(r"(\d{4})").astype(int)

                predictions = []
                for prov in df["Provinces"]:
                    sub = df_melt[df_melt["Provinces"] == prov]
                    X = sub["Année"].values.reshape(-1, 1)
                    y = sub["Population"].values
                    model = LinearRegression().fit(X, y)
                    future_years = np.array([2019, 2020, 2021]).reshape(-1, 1)
                    y_pred = model.predict(future_years)
                    for yr, val in zip([2019, 2020, 2021], y_pred):
                        predictions.append({"Provinces": prov, "Année": yr, "Population": val})

                df_pred = pd.DataFrame(predictions)
                df_all = pd.concat([df_melt, df_pred])
                fig = px.line(
                    df_all, x="Année", y="Population", color="Provinces",
                    markers=True, color_discrete_sequence=px.colors.qualitative.Set2
                )

            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

        #########tab4
        st.markdown("""
                              <h4 style=' color: #85919e;margin-left: 0px;'>
                                            4 – Évolution de la population selon les groupes d’âges et le milieu																						
                              </h4>
                              """, unsafe_allow_html=True)

        # --- Données âge 2014–2018 ---
        data = {
            "Groupe d’âge": [
                "0-4 ans", "5-9 ans", "10-14 ans", "15-19 ans", "20-24 ans",
                "25-29 ans", "30-34 ans", "35-39 ans", "40-44 ans", "45-49 ans",
                "50-54 ans", "55-59 ans", "60-64 ans", "65-69 ans", "70-74 ans", "75 ans et plus"
            ],
            "2014 – Total": [266719, 244243, 242784, 231381, 233398, 219021, 211861, 194902, 181003, 149184, 135266,
                             100538, 86390, 54314, 47437, 71021],
            "2014 – Urbain": [149168, 134967, 130734, 127775, 139186, 131404, 126351, 114419, 106312, 87638, 78159,
                              55289, 43871, 24887, 20294, 26996],

            "2015 – Total": [263138, 247901, 242734, 231611, 233812, 222918, 214974, 199205, 185359, 152807, 137225,
                             105990, 90497, 59470, 47632, 69467],
            "2015 – Urbain": [149649, 138729, 132105, 129081, 141790, 137016, 130846, 118877, 109996, 90813, 80386,
                              59238, 47178, 28191, 20930, 27605],

            "2016 – Total": [258157, 253372, 242142, 232771, 232916, 227545, 217486, 204001, 188828, 158186, 137230,
                             112736, 93026, 66982, 46275, 69567],
            "2016 – Urbain": [149559, 143496, 133406, 130898, 143058, 143200, 135045, 123961, 113221, 94976, 81590,
                              63808, 49834, 32671, 20995, 28757],

            "2017 – Total": [251508, 260478, 241642, 234430, 231315, 232285, 219789, 209018, 191816, 164604, 136342,
                             119808, 94854, 75625, 44596, 70660],
            "2017 – Urbain": [148717, 149207, 134900, 132997, 143466, 149466, 139213, 129315, 116261, 99741, 82305,
                              68537, 52201, 37806, 20992, 30256],

            "2018 – Total": [243065, 268885, 242011, 235893, 229909, 236252, 222462, 213797, 194959, 170950, 136065,
                             125881, 97256, 83719, 44246, 71850],
            "2018 – Urbain": [147017, 155706, 136914, 134973, 143762, 155097, 143758, 134723, 119555, 104482, 83315,
                              72781, 54832, 42848, 21651, 31786],
        }

        df = pd.DataFrame(data)

        # --- Trois colonnes de la page ---
        col1, col2, col3 = st.columns([2, 1, 1])  # Graphique, tableau, choix

        # --- Colonne 3 : choix utilisateur ---
        with col3:
            st.markdown("<br><br>", unsafe_allow_html=True)

            graph_options = ["Scatter (par défaut)", "Line Plot", "Bar Plot"]
            graph_type = st.selectbox("Type de graphique", graph_options, index=0, key="graph_type_ages")

            st.markdown("<h7 style='color:#3e5c76;'>Sélectionnez l'année et le milieu</h7>", unsafe_allow_html=True)
            annee = st.selectbox("Année :", ["2014", "2015", "2016", "2017", "2018"], index=0, key="annee_ages")

            # ✅ Ajout de clés uniques pour éviter bug Streamlit
            show_urbain = st.checkbox("Urbain", True, key="urbain_ages", )
            show_total = st.checkbox("Total", True, key="total_ages")

        # --- Construire liste des colonnes à afficher ---
        columns_to_plot = []
        if show_total: columns_to_plot.append(f"{annee} – Total")
        if show_urbain: columns_to_plot.append(f"{annee} – Urbain")

        # --- Palette douce ---
        soft_colors = ["#91a6a6", "#a3c1ad", "#f3d1b0", "#f0a6a6", "#b0c4de", "#c2b280",
                       "#d4a6c8", "#c8e0f0", "#f0c8c0", "#a6b0c8", "#d1c2a3", "#b0d1c8",
                       "#c8b0d4", "#e0c8c8", "#d4f0c8", "#f0e0c8"]

        # --- Colonne 1 : graphique ---
        with col1:
            if not columns_to_plot:
                st.warning("⚠ Veuillez sélectionner au moins un indicateur !")
            else:
                if graph_type == "Bar Plot":
                    fig = px.bar(df, x="Groupe d’âge", y=columns_to_plot, barmode="group",
                                 color_discrete_sequence=soft_colors)
                    st.plotly_chart(fig, use_container_width=True)

                elif graph_type == "Line Plot":
                    fig = px.line(df, x="Groupe d’âge", y=columns_to_plot, markers=True,
                                  color_discrete_sequence=soft_colors)
                    st.plotly_chart(fig, use_container_width=True)

                else:  # Scatter par défaut
                    if len(columns_to_plot) >= 2:
                        x_col, y_col = columns_to_plot[0], columns_to_plot[1]
                    else:
                        x_col, y_col = "Groupe d’âge", columns_to_plot[0]

                    fig = px.scatter(df, x=x_col, y=y_col, text="Groupe d’âge",
                                     size_max=20, color_discrete_sequence=["#1f77b4"])
                    fig.update_traces(textposition="top center")
                    st.plotly_chart(fig, use_container_width=True)

        # --- Colonne 2 : tableau ---
        with col2:
            st.markdown("<br><br>", unsafe_allow_html=True)
            st.dataframe(df[["Groupe d’âge"] + columns_to_plot], use_container_width=True)
        ####### comparaison tab 4

        st.markdown("""
                <div style='
                    background-color: #aab5bf;
                    border-radius: 12px;
                    padding: 8px 16px;
                    text-align: center;
                    color: white;
                    font-weight: bold;
                    font-size: 18px;
                    display: inline-block;
                '>
                    Analyse Comparative et Évolution des Données
                </div>
                """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1.5, 3, 1])

        # --- Col1 : texte explicatif ---
        with col1:
            st.markdown("<br><br><br><br>", unsafe_allow_html=True)
            st.markdown("""
            Entre 2014 et 2018, les effectifs évoluent différemment selon les groupes d’âge, 

            """)
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("""
                        Une baisse chez les plus jeunes et une hausse dans certaines tranches urbaines.
                        """)

        # --- Col3 : options ---
        with col3:
            st.markdown("<br><br><br>", unsafe_allow_html=True)
            indicators = ["Total", "Urbain"]
            selected_indicator = st.selectbox("Indicateur", indicators, index=0)
            graph_options = ["Bar Plot comparatif", "Évolution", "Variation %", "Prévision"]
            graph_type = st.selectbox("Graphique", graph_options, index=3)  # Prévision par défaut

        # --- Col2 : graphique ---
        with col2:
            # Colonnes disponibles
            years = [2014, 2015, 2016, 2017, 2018]
            cols = [f"{year} – {selected_indicator}" for year in years]

            if graph_type == "Bar Plot comparatif":
                year1, year2 = st.select_slider("Comparer", options=years, value=(2014, 2018))
                col_y1, col_y2 = f"{year1} – {selected_indicator}", f"{year2} – {selected_indicator}"
                fig = px.bar(df, x="Groupe d’âge", y=[col_y1, col_y2], barmode="group",
                             color_discrete_sequence=["#1c354f", "#7a3d2c"])

            elif graph_type == "Évolution":
                df_melt = df.melt(id_vars="Groupe d’âge", value_vars=cols,
                                  var_name="Année", value_name="Population")
                df_melt["Année"] = df_melt["Année"].str.extract(r"(\d{4})").astype(int)
                fig = px.line(df_melt, x="Année", y="Population", color="Groupe d’âge",
                              markers=True, color_discrete_sequence=px.colors.qualitative.Set2)

            elif graph_type == "Variation %":
                year1, year2 = st.select_slider("Comparer", options=years, value=(2014, 2018))
                col_y1, col_y2 = f"{year1} – {selected_indicator}", f"{year2} – {selected_indicator}"
                df["Variation %"] = ((df[col_y2] - df[col_y1]) / df[col_y1] * 100).round(2)
                fig = px.bar(df, x="Groupe d’âge", y="Variation %", color="Variation %",
                             color_continuous_scale=["#758a72", "#7a3d2c", "#abb1d6", "#dede85"])

            elif graph_type == "Prévision":
                df_melt = df.melt(id_vars="Groupe d’âge", value_vars=cols,
                                  var_name="Année", value_name="Population")
                df_melt["Année"] = df_melt["Année"].str.extract(r"(\d{4})").astype(int)

                predictions = []
                for group in df["Groupe d’âge"]:
                    sub = df_melt[df_melt["Groupe d’âge"] == group]
                    X = sub["Année"].values.reshape(-1, 1)
                    y = sub["Population"].values
                    model = LinearRegression().fit(X, y)
                    future_years = np.array([2019, 2020, 2021]).reshape(-1, 1)
                    y_pred = model.predict(future_years)
                    for yr, val in zip([2019, 2020, 2021], y_pred):
                        predictions.append({"Groupe d’âge": group, "Année": yr, "Population": val})

                df_pred = pd.DataFrame(predictions)
                df_all = pd.concat([df_melt, df_pred])
                fig = px.line(df_all, x="Année", y="Population", color="Groupe d’âge", markers=True,
                              color_discrete_sequence=px.colors.qualitative.Set2)

            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

        ############# tab 5
        st.markdown("""
                                      <h4 style=' color: #85919e;margin-left: 0px;'>
                                                   5 – Estimation du nombre de ménages selon le milieu de résidence								 </h4>
                                      """, unsafe_allow_html=True)

        # ================== Données 2014 ==================
        data_2014 = {
            "Provinces": [
                "Agadir Ida Outanane", "Inezgane", "Chtouka-Aït Baha",
                "Taroudant", "Tata", "Tiznit", "Souss-Massa"
            ],
            "Total": [154203, 133941, 94633, 177278, 22697, 52349, 635101],
            "Rural": [19644, 6255, 63090, 117574, 14286, 30421, 251270],
            "Urbain": [134559, 127686, 31543, 59704, 8411, 21928, 383831],
        }
        df_2014 = pd.DataFrame(data_2014)

        # ================== Données 2018 ==================
        data_2018 = {
            "Provinces": [
                "Agadir Ida Outanane", "Inezgane", "Chtouka-Aït Baha",
                "Taroudant", "Tata", "Tiznit", "Souss-Massa"
            ],
            "Total": [163283, 142549, 99852, 180895, 22675, 52671, 661925],
            "Rural": [19223, 6381, 64281, 117445, 14002, 29186, 250518],
            "Urbain": [144060, 136168, 35571, 63450, 8673, 23485, 411407],
        }
        df_2018 = pd.DataFrame(data_2018)

        # ================== Trois colonnes ==================
        col1, col2, col3 = st.columns([2, 1, 1])  # Graphique, tableau, choix

        # ================== Colonne 3 : choix utilisateur ==================
        with col3:
            st.markdown("<br><br>", unsafe_allow_html=True)

            # Sélecteur année avec clé unique
            year_options = ["2014", "2018"]
            selected_year = st.selectbox("Choisir l'année", year_options, key="select_year_1")

            # Sélecteur graphique avec clé unique (Pie Chart par défaut)
            graph_options = ["Pie Chart", "Bar Plot", "Line Plot", "Heatmap"]
            graph_type = st.selectbox("Type de graphique", graph_options, index=0, key="graph_type_1")

            st.markdown("<h7 style='color:#3e5c76;'>Sélectionnez les indicateurs</h7>", unsafe_allow_html=True)
            show_total = st.checkbox("Total", True, key="total_1")
            show_rural = st.checkbox("Rural", True, key="rural_1")
            show_urbain = st.checkbox("Urbain", True, key="urbain_1")

        # ================== Sélection de l'année ==================
        if selected_year == "2014":
            df = df_2014
        else:
            df = df_2018

        # ================== Colonnes à afficher ==================
        columns_to_plot = []
        if show_total: columns_to_plot.append("Total")
        if show_rural: columns_to_plot.append("Rural")
        if show_urbain: columns_to_plot.append("Urbain")

        # ================== Palette personnalisée ==================
        custom_colors = [
            "#48516e", "#1f232e", "#754837",
            "#5c1313", "#4a491e", "#464047", "#687d6c"
        ]

        # ================== Colonne 1 : graphique ==================
        with col1:
            if not columns_to_plot:
                st.warning("⚠ Veuillez sélectionner au moins un indicateur !")
            else:
                if graph_type == "Pie Chart":
                    fig = go.Figure()
                    for idx, col in enumerate(columns_to_plot):
                        fig.add_trace(go.Pie(
                            labels=df["Provinces"],
                            values=df[col],
                            name=col,
                            hole=0.3,
                            textinfo='label+percent',
                            marker=dict(colors=custom_colors)
                        ))
                    st.plotly_chart(fig, use_container_width=True)

                elif graph_type == "Bar Plot":
                    fig = px.bar(
                        df, x="Provinces", y=columns_to_plot, barmode="group",
                        color_discrete_sequence=custom_colors
                    )
                    st.plotly_chart(fig, use_container_width=True)

                elif graph_type == "Line Plot":
                    fig = px.line(
                        df, x="Provinces", y=columns_to_plot, markers=True,
                        color_discrete_sequence=custom_colors
                    )
                    st.plotly_chart(fig, use_container_width=True)

                elif graph_type == "Heatmap":
                    heat_data = df[columns_to_plot]
                    fig = px.imshow(
                        heat_data.T, x=df["Provinces"], y=columns_to_plot,
                        color_continuous_scale=custom_colors
                    )
                    st.plotly_chart(fig, use_container_width=True)

        # ================== Colonne 2 : tableau ==================
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<br><br>", unsafe_allow_html=True)
            st.dataframe(df[["Provinces"] + columns_to_plot], use_container_width=True)

        ########## prediction tab5

        st.markdown("""
                <div style='
                    background-color: #aab5bf;
                    border-radius: 12px;
                    padding: 8px 16px;
                    text-align: center;
                    color: white;
                    font-weight: bold;
                    font-size: 18px;
                    display: inline-block;
                '>
                    Analyse Comparative et Évolution des Données
                </div>
                """, unsafe_allow_html=True)

        # --- Col2 : sous-colonnes pour graphique et options ---
        df = df_2014.rename(columns={"Total": "2014-Total", "Rural": "2014-Rural", "Urbain": "2014-Urbain"})
        df["2018-Total"] = df_2018["Total"]
        df["2018-Rural"] = df_2018["Rural"]
        df["2018-Urbain"] = df_2018["Urbain"]

        # Colonnes principales
        col1, col2, col3 = st.columns([1.5, 3, 1])

        # --- Col1 : texte explicatif ---
        with col1:
            st.markdown("<br><br><br><br>", unsafe_allow_html=True)
            st.markdown("""
           Entre 2014 et 2018, la population a globalement progressé, avec une hausse plus marquée en milieu urbain. 

            """)
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("""Les provinces affichent toutefois des rythmes de croissance différents """)

        # --- Col3 : options ---
        with col3:
            st.markdown("<br><br>", unsafe_allow_html=True)
            indicators = ["Total", "Urbain", "Rural"]
            selected_indicator = st.selectbox("Indicateur", indicators, index=0)
            graph_options = ["Bar Plot comparatif", "Scatter 2014 vs 2018", "Variation %", "Prévision"]
            graph_type = st.selectbox("Graphique", graph_options, index=2)

        # --- Col2 : graphique ---
        with col2:
            col_2014 = f"2014-{selected_indicator}"
            col_2018 = f"2018-{selected_indicator}"

            if graph_type == "Bar Plot comparatif":
                fig = px.bar(df, x="Provinces", y=[col_2014, col_2018], barmode="group",
                             color_discrete_sequence=["#1c354f", "#4d0f14"])
            elif graph_type == "Scatter 2014 vs 2018":
                fig = px.scatter(df, x=col_2014, y=col_2018, text="Provinces", size=col_2018,
                                 color_discrete_sequence=["#758a72"])
                fig.update_traces(textposition="top center")
            elif graph_type == "Variation %":
                df["Variation %"] = ((df[col_2018] - df[col_2014]) / df[col_2014] * 100).round(2)
                fig = px.bar(
                    df,
                    x="Provinces",
                    y="Variation %",
                    color="Variation %",
                    color_continuous_scale=["#758a72", "#7a3d2c", "#abb1d6", "#dede85"]
                )


            elif graph_type == "Prévision":
                years = np.array([2014, 2018]).reshape(-1, 1)
                future_years = np.array([2019, 2020, 2021]).reshape(-1, 1)
                predictions = {}
                for i, row in df.iterrows():
                    y = np.array([row[col_2014], row[col_2018]])
                    model = LinearRegression().fit(years, y)
                    y_pred = model.predict(future_years)
                    predictions[row["Provinces"]] = y_pred
                df_pred = pd.DataFrame(predictions, index=[2019, 2020, 2021])
                df_pred.reset_index(inplace=True)
                df_pred_melt = df_pred.melt(id_vars="index", var_name="Province", value_name="Population")
                fig = px.line(df_pred_melt, x="index", y="Population", color="Province", markers=True,
                              color_discrete_sequence=px.colors.qualitative.Set2)

            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.write("")
        import streamlit as st
        import pandas as pd
        import geopandas as gpd
        import plotly.express as px

        # --- CONFIGURATION DE LA PAGE ---
        st.set_page_config(page_title="Axioradata - Dashboard Démographique", layout="wide")

        # --- STYLE CSS ---
        st.markdown("""
        <style>
            h1 {
                color: #000033;
            }
            .kpi-banner {
                background-color: #000033;
                color: white;
                padding: 1rem;
                border-radius: 0.5rem;
                display: flex;
                justify-content: space-between;
                align-items: center;
                flex-wrap: wrap;
                margin-bottom: 1rem;
            }
            .kpi-box {
                text-align: center;
                flex-grow: 1;
            }
            .kpi-box.min { order: 1; }
            .kpi-box.max { order: 2; }
            .kpi-box.total { order: 3; }
            .kpi-label {
                font-size: 0.9em;
                opacity: 0.8;
                display: block;
            }
            .kpi-value {
                font-size: 1.3em;
                font-weight: bold;
                display: block;
            }
        </style>
        """, unsafe_allow_html=True)

        # --- DONNÉES ---
        population_data = {
            "division_administrative": {
                "2017": {
                    "Province": ["Agadir Ida Outanane", "Inezgane-Aït Melloul", "Chtouka-Aït Baha", "Taroudant",
                                 "Tiznit",
                                 "Tata"],
                    "Urbaines": [1, 2, 2, 8, 2, 4], "Rurales": [11, 4, 20, 81, 23, 16],
                    "Total Communes": [12, 6, 22, 89, 25, 20], "Cercles": [1, 1, 2, 5, 3, 3]
                },
                "2018": {
                    "Province": ["Agadir Ida Outanane", "Inezgane Ait Melloul", "Chtouka Ait Baha", "Taroudant",
                                 "Tiznit",
                                 "Tata"],
                    "Urbaines": [1, 4, 2, 8, 2, 4], "Rurales": [12, 2, 20, 81, 23, 16],
                    "Total Communes": [13, 6, 22, 89, 25, 20], "Cercles": [2, 1, 3, 5, 3, 3]
                }
            },
            "population_legale": {
                "Provinces": ["Agadir Ida Outanane", "Inezgane-Aït Melloul", "Chtouka-Aït Baha", "Taroudant", "Tiznit",
                              "Tata",
                              "Souss-Massa"],
                "RGPH 2004 – Urbain": [384987, 385612, 239694, 186471, 58613, 39060, 1094437],
                "RGPH 2004 – Total": [487954, 419614, 297245, 780661, 217050, 121618, 2324142],
                "RGPH 2014 – Urbain": [508155, 513706, 113531, 248640, 81044, 40820, 1505896],
                "RGPH 2014 – Total": [600599, 541118, 371102, 838820, 207367, 117841, 2676847],
            },
            "estimations_population_milieu": {
                "Provinces": ["Agadir Ida Outanane", "Inezgane Aït Melloul", "Chtouka Aït Baha", "Taroudant", "Tata",
                              "Tiznit",
                              "Souss-Massa"],
                "2016 – Urbain": [535653, 539975, 125818, 260214, 41417, 85357, 1143390],
                "2016 – Rural": [89307, 27595, 258625, 582540, 74937, 119786, 1635380],
                "2016 – Total": [624960, 567570, 384443, 842754, 116354, 205143, 2778770],
                "2017 – Urbain": [551240, 554820, 133050, 266730, 41740, 87800, 1152790],
                "2017 – Rural": [87650, 27710, 259260, 578550, 73840, 116380, 1588434],
                "2017 – Total": [638890, 582530, 392310, 845280, 115580, 204180, 2741224],
                "2018 – Urbain": [567055, 569865, 140642, 273306, 42054, 90276, 1168198],
                "2018 – Rural": [86032, 27806, 259843, 574518, 72752, 113055, 1134006],
                "2018 – Total": [653087, 597671, 400485, 847824, 114806, 203331, 2817204],
            },
            "estimation_nombre_menages": {
                "2014": {
                    "Provinces": ["Agadir Ida Outanane", "Inezgane", "Chtouka-Aït Baha", "Taroudant", "Tata", "Tiznit",
                                  "Souss-Massa"], "Total": [154203, 133941, 94633, 177278, 22697, 52349, 635101],
                    "Rural": [19644, 6255, 63090, 117574, 14286, 30421, 251270],
                    "Urbain": [134559, 127686, 31543, 59704, 8411, 21928, 383831]},
                "2018": {
                    "Provinces": ["Agadir Ida Outanane", "Inezgane", "Chtouka-Aït Baha", "Taroudant", "Tata", "Tiznit",
                                  "Souss-Massa"], "Total": [163283, 142549, 99852, 180895, 22675, 52671, 661925],
                    "Rural": [19223, 6381, 64281, 117445, 14002, 29186, 250518],
                    "Urbain": [144060, 136168, 35571, 63450, 8673, 23485, 411407]}
            }
        }


        # --- FONCTIONS ---
        @st.cache_data
        def load_shapefile(path):
            try:
                return gpd.read_file(path)
            except Exception as e:
                st.error(f"Erreur chargement shapefile : {e}");
                return None


        @st.cache_data
        def process_all_data(data):
            records = []
            for year, df_data in data['division_administrative'].items():
                df = pd.DataFrame(df_data).melt(id_vars='Province', var_name='Indicateur', value_name='Valeur')
                df['Thème'] = 'Division Administrative';
                df['Année'] = year
                records.append(df)
            df_pl = pd.DataFrame(data['population_legale']).melt(id_vars='Provinces', var_name='Indicateur_original',
                                                                 value_name='Valeur')
            df_pl[['Année', 'Indicateur']] = df_pl['Indicateur_original'].str.split(' – ', expand=True)
            df_pl['Année'] = df_pl['Année'].str.replace('RGPH ', '');
            df_pl['Thème'] = 'Population Légale (RGPH)'
            records.append(
                df_pl[['Provinces', 'Valeur', 'Année', 'Indicateur', 'Thème']].rename(
                    columns={'Provinces': 'Province'}))
            df_ep = pd.DataFrame(data['estimations_population_milieu']).melt(id_vars='Provinces',
                                                                             var_name='Indicateur_original',
                                                                             value_name='Valeur')
            df_ep[['Année', 'Indicateur']] = df_ep['Indicateur_original'].str.split(' – ', expand=True)
            df_ep['Thème'] = 'Estimations de Population'
            records.append(
                df_ep[['Provinces', 'Valeur', 'Année', 'Indicateur', 'Thème']].rename(
                    columns={'Provinces': 'Province'}))
            for year, df_data in data['estimation_nombre_menages'].items():
                df = pd.DataFrame(df_data).melt(id_vars='Provinces', var_name='Indicateur', value_name='Valeur')
                df['Thème'] = 'Nombre de Ménages';
                df['Année'] = year
                records.append(df.rename(columns={'Provinces': 'Province'}))
            final_df = pd.concat(records, ignore_index=True)
            final_df = final_df[final_df['Province'] != 'Souss-Massa'].copy()
            final_df['Valeur'] = pd.to_numeric(final_df['Valeur'], errors='coerce')
            final_df.dropna(subset=['Valeur'], inplace=True)
            return final_df


        # --- AFFICHAGE ---
        st.markdown(
            '<h5 style="background-color:#c9cad1; color:#494c63; display:inline-block; padding:8px 15px; border-radius:15px;">Dashboard Démographique - Région Souss-Massa</h5>',
            unsafe_allow_html=True)
        df_complet = process_all_data(population_data)
        st.write("")

        # --- DONNÉES ET BANDEAU KPI ---
        # Le code pour calculer les KPIs est placé ici pour être accessible globalement
        # mais les filtres qui en dépendent sont déplacés plus bas.
        df_theme_temp = df_complet[df_complet['Thème'] == df_complet['Thème'].unique()[0]]
        df_indicateur_temp = df_theme_temp[df_theme_temp['Indicateur'] == df_theme_temp['Indicateur'].unique()[0]]
        annee_choisie_temp = sorted(df_indicateur_temp['Année'].unique(), reverse=True)[0]
        df_filtre = df_indicateur_temp[df_indicateur_temp['Année'] == annee_choisie_temp]

        if not df_filtre.empty:
            total_regional = f"{df_filtre['Valeur'].sum():,.0f}".replace(',', ' ')
            max_province = df_filtre.loc[df_filtre['Valeur'].idxmax()]
            min_province = df_filtre.loc[df_filtre['Valeur'].idxmin()]
            max_val = f"{max_province['Valeur']:,.0f}".replace(',', ' ')
            min_val = f"{min_province['Valeur']:,.0f}".replace(',', ' ')

            st.markdown(f"""
            <div class="kpi-banner">
                <div class="kpi-box min">
                    <span class="kpi-label">Min: {min_province['Province']}</span>
                    <span class="kpi-value">{min_val}</span>
                </div>
                <div class="kpi-box max">
                    <span class="kpi-label">Max: {max_province['Province']}</span>
                    <span class="kpi-value">{max_val}</span>
                </div>
                <div class="kpi-box total">
                    <span class="kpi-label">Total Régional</span>
                    <span class="kpi-value">{total_regional}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("Aucune donnée initiale disponible.")
            st.stop()

        # --- CARTE ET GRAPHIQUE ---
        shapefile_path = "mar_admbnda_adm2_hcp_20230925/mar_admbnda_adm2_hcp_20230925.shp"
        gdf_provinces = load_shapefile(shapefile_path)
        if gdf_provinces is not None:
            province_name_mapping = {
                'Agadir Ida Outanane': 'Agadir Ida Ou Tanane', 'Chtouka-Aït Baha': 'Chtouka- Ait Baha',
                'Inezgane-Aït Melloul': 'Inezgane-Ait Melloul', 'Taroudant': 'Taroudannt',
                'Inezgane Aït Melloul': 'Inezgane-Ait Melloul', 'Chtouka Aït Baha': 'Chtouka- Ait Baha',
                'Inezgane Ait Melloul': 'Inezgane-Ait Melloul', 'Inezgane': 'Inezgane-Ait Melloul'
            }
            df_filtre.loc[:, 'Province_corrige'] = df_filtre['Province'].replace(province_name_mapping)
            merged_gdf = gdf_provinces.merge(df_filtre, left_on='ADM2_FR', right_on='Province_corrige', how='inner')

            if not merged_gdf.empty:
                col1_viz, col2_viz = st.columns((2, 1))
                with col1_viz:
                    fig_map = px.choropleth_mapbox(merged_gdf, geojson=merged_gdf.geometry, locations=merged_gdf.index,
                                                   color="Valeur", hover_name="Province",
                                                   color_continuous_scale="YlGnBu",
                                                   mapbox_style="open-street-map", center={"lat": 30.0, "lon": -8.5},
                                                   zoom=6,
                                                   opacity=0.8,
                                                   labels={'Valeur': 'Valeur sélectionnée'})
                    fig_map.update_traces(marker_line_width=1.5, marker_line_color='white')
                    fig_map.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
                    st.plotly_chart(fig_map, use_container_width=True)
                with col2_viz:
                    df_sorted = merged_gdf.sort_values(by="Valeur", ascending=True)
                    fig_bar = px.bar(df_sorted, x="Valeur", y='Province', orientation='h', text_auto='.2s',
                                     color="Valeur", color_continuous_scale="YlGnBu",
                                     labels={'Valeur': 'Valeur sélectionnée'})
                    fig_bar.update_layout(showlegend=False)
                    st.plotly_chart(fig_bar, use_container_width=True)
            else:
                st.warning("Aucune donnée correspondante n'a pu être fusionnée avec la carte.")
        else:
            st.error("Données géographiques non chargées.")

        col1_filter, col2_filter, col3_filter = st.columns(3)
        with col1_filter:
            theme_choisi = st.selectbox("1. Choisissez un thème :", df_complet['Thème'].unique())
        df_theme = df_complet[df_complet['Thème'] == theme_choisi]
        with col2_filter:
            indicateur_choisi = st.selectbox("2. Choisissez un indicateur :", df_theme['Indicateur'].unique())
        df_indicateur = df_theme[df_theme['Indicateur'] == indicateur_choisi]
        with col3_filter:
            annee_choisie = st.selectbox("3. Choisissez une année :",
                                         sorted(df_indicateur['Année'].unique(), reverse=True))

        st.write("")
        st.markdown("<br>", unsafe_allow_html=True)




elif st.session_state.page == "Marche de Travail":
    st.markdown("<br>", unsafe_allow_html=True)

    st.set_page_config(layout="wide")

    st.markdown("""
        <style>
        .block-container {
            padding: 0;
            margin: 0;
            max-width: 100%;
        }

        .full-width-bar {
            width: 100%;
            background-color: #1E293B;
            padding: 15px 20px;  /* réduit les paddings */
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-sizing: border-box;
        }

        .bar-logo {
            font-family: 'Playfair Display', serif;
            color: white;
            font-size: 24px;   /* légèrement réduit */
            font-weight: 900;
        }

        .bar-menu {
            display: flex;
            gap: 10px;           /* réduit l’espace entre liens */
            max-width: 70%;       /* limite la largeur du menu pour éviter le dépassement */
            overflow-x: auto;     /* permet le défilement si écran trop petit */
        }

        .bar-menu a {
            color: white;
            text-decoration: none;
            font-size: 14px;      /* réduit la taille du texte */
            font-weight: 600;
            white-space: nowrap;  /* empêche le texte de passer à la ligne */
        }

        .bar-menu a:hover {
            color: #60A5FA;
        }

        .bar-menu .button {
            background-color: #3b82f6;
            padding: 5px 10px;
            border-radius: 6px;
            font-size: 14px;
            font-weight: 600;
        }

        .bar-menu .button:hover {
            background-color: #2563eb;
        }
        </style>

        <div class="full-width-bar">
            <div class="bar-logo">Axiora Data</div>
            <div class="bar-menu">
                <a href="#">App Marketing Agency</a>
                <a href="#">ASO Agency</a>
                <a href="#">Glossary</a>
                <a href="#">Data</a>
                <a href="#">ASO Tools</a>
                <a href="#" class="button">Read Blog</a>
            </div>
        </div>

        <div style="height: 60px;"></div>
        """, unsafe_allow_html=True)

    col11, col22, col33 = st.columns([0.1, 1, 0.1])
    with col22:
        st.markdown("""
                                          <h4 style=' color: #85919e;margin-left: 0px;'>
                                                       1. Activité par âge et milieu (2017–2020) </h4>
                                          """, unsafe_allow_html=True)
        data = {
            "Âge": ["15-24", "25-34", "35-44", "45 et plus", "Total"],
            "2017-Urbain": [16.4, 55.8, 56.3, 39.8, 41.8],
            "2017-Rural": [18.5, 54.5, 61.2, 46.9, 45.7],
            "2018-Urbain": [19.3, 53.3, 56.1, 39.7, 41.6],
            "2018-Rural": [25.4, 54.5, 60.4, 45.7, 45],
            "2019-Urbain": [19.4, 56.5, 57.1, 39, 42.6],
            "2019-Rural": [22, 53.6, 59.9, 43.3, 43.5],
            "2020-Urbain": [16.4, 55.7, 57.2, 38, 41.5],
            "2020-Rural": [18.5, 52.7, 56.9, 42.2, 41.6]
        }
        df = pd.DataFrame(data)

        # ================== Première ligne : Visualisation individuelle ==================

        col1, col2, col3 = st.columns([1, 2, 1])

        # --- Colonne 1 : choix utilisateur ---
        with col1:
            st.markdown("<br><br><br>", unsafe_allow_html=True)
            annees_disponibles = [2017, 2018, 2019, 2020]
            annee_select = st.selectbox("Sélectionner une année", annees_disponibles)
            show_urbain = st.checkbox("Urbain", True, key="urbain_vis3")
            show_rural = st.checkbox("Rural", True, key="rural_vis4")
            graph_options_vis = ["Line Plot", "Area Miroir", "Heatmap"]
            graph_type_vis = st.selectbox("Type de graphique", graph_options_vis, key="graph_vis3")

        # --- Colonne 2 : graphique ---
        with col2:

            cols_to_plot = []
            if show_urbain: cols_to_plot.append(f"{annee_select}-Urbain")
            if show_rural: cols_to_plot.append(f"{annee_select}-Rural")

            if cols_to_plot:
                if graph_type_vis == "Line Plot":
                    fig = px.line(df, x="Âge", y=cols_to_plot, markers=True)
                    st.plotly_chart(fig, use_container_width=True)
                elif graph_type_vis == "Area Miroir":
                    fig = go.Figure()
                    for col in cols_to_plot:
                        sign = 1 if "Urbain" in col else -1
                        fig.add_trace(go.Scatter(
                            x=df["Âge"], y=sign * df[col], fill='tozeroy', mode='none', name=col
                        ))
                    fig.update_layout(yaxis=dict(title="Valeur"), xaxis=dict(title="Âge"), template="plotly_white")
                    st.plotly_chart(fig, use_container_width=True)
                elif graph_type_vis == "Heatmap":
                    fig = px.imshow(df[cols_to_plot].T, x=df["Âge"], y=cols_to_plot, color_continuous_scale='Blues')
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("⚠ Veuillez sélectionner au moins un indicateur !")

        # --- Colonne 3 : tableau ---
        with col3:
            st.markdown("<br><br><br><br>", unsafe_allow_html=True)

            st.dataframe(df, use_container_width=True)

        # ================== Deuxième ligne : Comparaison multi-années ==================
        st.markdown("""
               <div style='background-color: #aab5bf; border-radius: 12px; padding: 8px 16px;
                text-align: center; color: white; font-weight: bold; font-size: 18px; display: inline-block;'>
                   Analyse Comparative et Évolution des Données
               </div>
               """, unsafe_allow_html=True)
        col1c, col2c, col3c = st.columns([1, 1.5, 2])

        # --- Colonne 1 : petit test comparatif ---
        with col1c:
            st.markdown("<br><br>", unsafe_allow_html=True)
            st.markdown("""
            - 15-24 ans : baisse, surtout rural.  

            - 25-34 ans : stable urbain, légère baisse rural.  

            - 35-44 ans : élevé, rural diminue.  

            - 45 ans et plus : baisse rural.  

            - Taux global : légère baisse.  
            """)

        # --- Colonne 2 : options utilisateur ---
        with col2c:
            st.markdown("<br><br><br>", unsafe_allow_html=True)

            annees_select = st.multiselect("Sélectionner les années à comparer", annees_disponibles,
                                           default=[2017, 2018])
            show_urbain_comp = st.checkbox("Urbain", True, key="urbain_comp4")
            show_rural_comp = st.checkbox("Rural", True, key="rural_comp4")
            graph_options_comp = ["Bar Plot comparatif", "Évolution", "Variation %", "Prévision"]
            graph_type_comp = st.selectbox("Type de graphique comparatif", graph_options_comp, key="graph_comp4")

        # --- Colonne 3 : graphique ---
        with col3c:
            cols_to_plot_comp = []
            if show_urbain_comp: cols_to_plot_comp.append("Urbain")
            if show_rural_comp: cols_to_plot_comp.append("Rural")

            if cols_to_plot_comp and annees_select:
                # Préparation des données pour comparaison
                cols_full = [f"{annee}-{col}" for annee in annees_select for col in cols_to_plot_comp]
                df_melted = df.melt(id_vars=["Âge"], value_vars=cols_full, var_name="Année", value_name="Valeur")
                df_melted["Année"] = df_melted["Année"].str.extract(r"(\d{4})").astype(int)

                if graph_type_comp == "Bar Plot comparatif":
                    fig = px.bar(df_melted, x="Âge", y="Valeur", color="Année", barmode="group")
                    st.plotly_chart(fig, use_container_width=True)

                elif graph_type_comp == "Évolution":
                    fig = px.line(df_melted, x="Âge", y="Valeur", color="Année", markers=True)
                    st.plotly_chart(fig, use_container_width=True)

                elif graph_type_comp == "Variation %":
                    annee1, annee2 = min(annees_select), max(annees_select)
                    for col in cols_to_plot_comp:
                        df[f"Var% {col}"] = ((df[f"{annee2}-{col}"] - df[f"{annee1}-{col}"]) / df[
                            f"{annee1}-{col}"]) * 100
                    df_var_melted = df.melt(id_vars=["Âge"], value_vars=[f"Var% {col}" for col in cols_to_plot_comp],
                                            var_name="Année", value_name="Valeur")
                    fig = px.bar(df_var_melted, x="Âge", y="Valeur", color="Année")
                    st.plotly_chart(fig, use_container_width=True)

                elif graph_type_comp == "Prévision":
                    st.write("Prévision basée sur régression linéaire pour les années à venir")
                    future_years = np.arange(min(annees_select), max(annees_select) + 5, 1).reshape(-1, 1)
                    for col in cols_to_plot_comp:
                        y = df[[f"{annee}-{col}" for annee in annees_select]].values.T
                        model = LinearRegression().fit(np.array(annees_select).reshape(-1, 1), y)
                        y_pred = model.predict(future_years)
                        for idx, col_val in enumerate(cols_to_plot_comp):
                            st.line_chart(
                                pd.DataFrame({f"{col_val} prévision": y_pred[:, idx]}, index=future_years.flatten()))
            else:
                st.warning("⚠ Veuillez sélectionner au moins un indicateur et une année !")
        ###################taaaabbb22
        st.markdown("""
        <h4 style='color: #85919e;margin-left: 0px;'>
        2-Évolution du taux d'activité par niveau d'instruction et milieu (2017–2020)
        </h4>
        """, unsafe_allow_html=True)

        # ================== Données ==================
        data_evolution = {
            "Niveau": ["Sans diplôme", "Avec diplôme", "Sans diplôme", "Avec diplôme", "Sans diplôme", "Avec diplôme"],
            "Milieu": ["Urbain", "Urbain", "Rural", "Rural", "Total", "Total"],
            "2017": [38.4, 45.2, 48, 39.6, 43.2, 43.7],
            "2018": [38, 45, 46.8, 40.5, 42.3, 43.8],
            "2019": [37.6, 47.1, 44.4, 41.3, 40.9, 45.6],
            "2020": [36.1, 46.2, 42.7, 38.8, 39.3, 44.3]
        }
        df = pd.DataFrame(data_evolution)

        # -------------------- Conversion colonnes en string --------------------
        annees_disponibles = [2017, 2018, 2019, 2020]
        df.columns = df.columns.map(str)
        annees_disponibles_str = [str(a) for a in annees_disponibles]

        # ================== Première ligne : Visualisation individuelle ==================
        col1, col2, col3 = st.columns([1, 3, 1])

        # --- Colonne 1 : sélection utilisateur ---
        with col1:
            st.markdown("<br><br>", unsafe_allow_html=True)
            annee_select = st.selectbox("Sélectionner une année", annees_disponibles_str, key="annee_vis1")
            show_urbain = st.checkbox("Urbain", True, key="urbain_vis7")
            show_rural = st.checkbox("Rural", True, key="rural_vis8")
            show_total = st.checkbox("Total", True, key="total_vis9")
            graph_options_vis = ["Bar Empilée", "Line Plot", "Area Miroir", "Radar Chart"]
            graph_type_vis = st.selectbox("Type de graphique", graph_options_vis, key="graph_vis4", index=1)

        # --- Colonne 2 : graphique ---
        with col2:
            cols_to_plot = []
            if show_urbain: cols_to_plot.append("Urbain")
            if show_rural: cols_to_plot.append("Rural")
            if show_total: cols_to_plot.append("Total")

            if cols_to_plot:
                df_plot = pd.DataFrame()
                for milieu in cols_to_plot:
                    df_subset = df[df["Milieu"] == milieu].melt(
                        id_vars=["Niveau", "Milieu"],
                        value_vars=annees_disponibles_str,
                        var_name="Année",
                        value_name="Valeur"
                    )
                    df_plot = pd.concat([df_plot, df_subset], ignore_index=True)

                # -------------------- Graphiques --------------------
                if graph_type_vis == "Bar Empilée":
                    fig = px.bar(
                        df_plot, x="Niveau", y="Valeur", color="Année", barmode="group",
                        facet_col="Milieu", text="Valeur",
                        color_discrete_sequence=["#556270", "#4ECDC4", "#C7F464", "#FF6B6B"]
                    )
                    fig.update_traces(textposition="outside", marker_line_color='black', marker_line_width=1.5)
                    fig.update_layout(title="Taux d'activité par niveau et milieu", title_x=0.5,
                                      template="plotly_white")
                    st.plotly_chart(fig, use_container_width=True)

                elif graph_type_vis == "Line Plot":
                    fig = px.line(
                        df_plot, x="Niveau", y="Valeur", color="Année", markers=True, line_dash="Milieu",
                        color_discrete_sequence=["#556270", "#4ECDC4", "#C7F464", "#FF6B6B"]
                    )
                    fig.update_traces(marker=dict(size=10, line=dict(width=2, color='DarkSlateGrey')))
                    fig.update_layout(title="Évolution du taux d'activité par niveau et milieu", title_x=0.5,
                                      template="plotly_white")
                    st.plotly_chart(fig, use_container_width=True)

                elif graph_type_vis == "Area Miroir":
                    fig = go.Figure()
                    for col in df_plot["Milieu"].unique():
                        df_temp = df_plot[df_plot["Milieu"] == col]
                        sign = 1 if col != "Rural" else -1
                        fig.add_trace(go.Scatter(
                            x=df_temp["Niveau"], y=sign * df_temp["Valeur"], fill='tozeroy', mode='lines+markers',
                            name=col
                        ))
                    fig.update_layout(title="Graphique Area Miroir par milieu", title_x=0.5, template="plotly_white")
                    st.plotly_chart(fig, use_container_width=True)

                elif graph_type_vis == "Radar Chart":
                    fig = px.line_polar(df_plot, r="Valeur", theta="Niveau", color="Milieu", line_close=True,
                                        markers=True)
                    fig.update_layout(title="Radar Chart du taux d'activité", title_x=0.5, template="plotly_white")
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("⚠ Veuillez sélectionner au moins un milieu !")

        # --- Colonne 3 : tableau ---
        with col3:
            st.markdown("<br><br><br>", unsafe_allow_html=True)
            st.dataframe(df, use_container_width=True)

        # ================== Deuxième ligne : Comparaison multi-années ==================
        st.markdown("""
        <div style='background-color: #aab5bf; border-radius: 12px; padding: 8px 16px;
         text-align: center; color: white; font-weight: bold; font-size: 18px; display: inline-block;'>
            Analyse Comparative et Évolution des Données
        </div>
        """, unsafe_allow_html=True)

        col1c, col2c, col3c = st.columns([1, 1, 3])

        with col1c:
            st.markdown("<br><br><br>", unsafe_allow_html=True)
            st.markdown("""
            - Le tableau montre l’évolution du taux d’activité (15 ans et plus) entre 2017 et 2020.  
            - Les personnes diplômées sont plus actives.  

            - Le milieu rural connaît une légère baisse.  
            - Le taux global diminue légèrement.  
            """)

        with col2c:
            st.markdown("<br><br><br>", unsafe_allow_html=True)
            annees_select = st.multiselect("Sélectionner années à comparer", annees_disponibles_str,
                                           default=annees_disponibles_str, key="annees_comp")
            show_urbain_comp = st.checkbox("Urbain", True, key="urbain_comp5")
            show_rural_comp = st.checkbox("Rural", True, key="rural_comp5")
            show_total_comp = st.checkbox("Total", True, key="total_comp5")
            graph_options_comp = ["Slope Chart", "Waterfall", "Bar Comparatif"]
            graph_type_comp = st.selectbox("Type de graphique comparatif", graph_options_comp, key="graph_comp1",
                                           index=2)

        with col3c:
            cols_to_plot_comp = []
            if show_urbain_comp: cols_to_plot_comp.append("Urbain")
            if show_rural_comp: cols_to_plot_comp.append("Rural")
            if show_total_comp: cols_to_plot_comp.append("Total")

            if cols_to_plot_comp and annees_select:
                df_melted = pd.DataFrame()
                for col in cols_to_plot_comp:
                    df_sub = df[df["Milieu"] == col].melt(id_vars=["Niveau"], value_vars=annees_select,
                                                          var_name="Année", value_name="Valeur")
                    df_sub["Milieu"] = col
                    df_melted = pd.concat([df_melted, df_sub], ignore_index=True)

                if graph_type_comp == "Slope Chart":
                    fig = px.line(df_melted, x="Année", y="Valeur", color="Niveau", line_group="Milieu", markers=True)
                    fig.update_layout(template="plotly_white", title="Slope Chart : évolution multi-années")
                    st.plotly_chart(fig, use_container_width=True)

                elif graph_type_comp == "Waterfall":
                    df_waterfall = df_melted[df_melted["Milieu"] == cols_to_plot_comp[0]].sort_values("Année")
                    fig = go.Figure(go.Waterfall(
                        name="Taux activité",
                        orientation="v",
                        measure=["relative"] * (len(df_waterfall) - 1) + ["total"],
                        x=df_waterfall["Année"],
                        y=df_waterfall["Valeur"]
                    ))
                    fig.update_layout(template="plotly_white", title="Waterfall Chart")
                    st.plotly_chart(fig, use_container_width=True)

                elif graph_type_comp == "Bar Comparatif":
                    fig = px.bar(df_melted, x="Niveau", y="Valeur", color="Année", barmode="group", facet_col="Milieu",
                                 color_discrete_sequence=["#556270", "#4ECDC4", "#C7F464", "#66352b"])
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("⚠ Veuillez sélectionner au moins un milieu et une année !")

        ################# tab 3

        # ================== Titre ==================
        st.markdown("""
        <h4 style='color: #85919e;margin-left: 0px;'>
        3-Évolution du taux d'emploi par sexe et milieu (2017–2020)
        </h4>
        """, unsafe_allow_html=True)

        # ================== Données ==================
        data_emploi = {
            "Sexe": ["Hommes", "Femmes", "Hommes", "Femmes", "Hommes", "Femmes"],
            "Milieu": ["Urbain", "Urbain", "Rural", "Rural", "Total", "Total"],
            "2017": [61.6, 12.5, 63.9, 26.0, 62.5, 18.2],
            "2018": [61.2, 12.3, 62.7, 25.0, 61.7, 17.5],
            "2019": [61.3, 13.5, 63.7, 21.0, 62.2, 16.6],
            "2020": [59.7, 11.9, 62.1, 18.1, 60.6, 14.4]
        }
        df_emploi = pd.DataFrame(data_emploi)

        # Colonnes en string
        annees_dispo_emploi = [2017, 2018, 2019, 2020]
        df_emploi.columns = df_emploi.columns.map(str)
        annees_dispo_emploi_str = [str(a) for a in annees_dispo_emploi]

        # ================== Première ligne : Visualisation individuelle ==================
        col1e, col2e, col3e = st.columns([1, 3, 1])

        # --- Colonne 1 : sélection utilisateur ---
        with col1e:
            st.markdown("<br><br>", unsafe_allow_html=True)
            annee_select_emploi = st.selectbox("Sélectionner une année", annees_dispo_emploi_str, key="annee_emp1")
            show_urbain_emp = st.checkbox("Urbain", True, key="urbain_emp1")
            show_rural_emp = st.checkbox("Rural", True, key="rural_emp1")
            show_total_emp = st.checkbox("Total", True, key="total_emp1")
            graph_options_emp = ["Bar Groupé", "Line Plot", "Area Chart", "Pie Chart"]
            graph_type_emp = st.selectbox("Type de graphique", graph_options_emp, key="graph_emp1", index=1)

        # --- Colonne 2 : graphique ---
        with col2e:
            cols_to_plot_emp = []
            if show_urbain_emp: cols_to_plot_emp.append("Urbain")
            if show_rural_emp: cols_to_plot_emp.append("Rural")
            if show_total_emp: cols_to_plot_emp.append("Total")

            if cols_to_plot_emp:
                df_plot_emp = pd.DataFrame()
                for milieu in cols_to_plot_emp:
                    df_subset_emp = df_emploi[df_emploi["Milieu"] == milieu].melt(
                        id_vars=["Sexe", "Milieu"],
                        value_vars=annees_dispo_emploi_str,
                        var_name="Année",
                        value_name="Valeur"
                    )
                    df_plot_emp = pd.concat([df_plot_emp, df_subset_emp], ignore_index=True)

                # -------------------- Graphiques --------------------
                if graph_type_emp == "Bar Groupé":
                    fig = px.bar(
                        df_plot_emp, x="Sexe", y="Valeur", color="Année", barmode="group",
                        facet_col="Milieu", text="Valeur"
                    )
                    fig.update_traces(textposition="outside")

                    st.plotly_chart(fig, use_container_width=True)

                elif graph_type_emp == "Line Plot":
                    fig = px.line(
                        df_plot_emp, x="Sexe", y="Valeur", color="Année", markers=True, line_dash="Milieu"
                    )
                    fig.update_traces(marker=dict(size=9))

                    st.plotly_chart(fig, use_container_width=True)

                elif graph_type_emp == "Area Chart":
                    fig = px.area(
                        df_plot_emp, x="Année", y="Valeur", color="Sexe", facet_col="Milieu", line_group="Milieu"
                    )

                    st.plotly_chart(fig, use_container_width=True)

                elif graph_type_emp == "Pie Chart":
                    df_pie = df_plot_emp[df_plot_emp["Année"] == annee_select_emploi]
                    fig = px.pie(df_pie, names="Sexe", values="Valeur", color="Milieu")
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("⚠ Veuillez sélectionner au moins un milieu !")

        # --- Colonne 3 : tableau ---
        with col3e:
            st.markdown("<br><br><br>", unsafe_allow_html=True)
            st.dataframe(df_emploi, use_container_width=True)

        # ================== Deuxième ligne : Comparaison multi-années ==================
        st.markdown("""
        <div style='background-color: #aab5bf; border-radius: 12px; padding: 8px 16px;
         text-align: center; color: white; font-weight: bold; font-size: 18px; display: inline-block;'>
           Analyse Comparative et Évolution des Données
        </div>
        """, unsafe_allow_html=True)

        col1ce, col2ce, col3ce = st.columns([1, 1, 3])

        with col1ce:
            st.markdown("<br><br><br><br><br>", unsafe_allow_html=True)
            st.markdown("""
            - Les hommes ont toujours un taux plus élevé.  
            - Les femmes en rural reculent fortement.  
            - Globalement, baisse entre 2017 et 2020.  
            """)

        with col2ce:
            st.markdown("<br><br><br>", unsafe_allow_html=True)
            annees_select_emp = st.multiselect("Sélectionner années à comparer", annees_dispo_emploi_str,
                                               default=annees_dispo_emploi_str, key="annees_emp")
            show_urbain_comp_emp = st.checkbox("Urbain", True, key="urbain_comp_emp")
            show_rural_comp_emp = st.checkbox("Rural", True, key="rural_comp_emp")
            show_total_comp_emp = st.checkbox("Total", True, key="total_comp_emp")
            graph_options_comp_emp = ["Slope Chart", "Bar Comparatif", "Heatmap"]
            graph_type_comp_emp = st.selectbox("Type de graphique comparatif", graph_options_comp_emp,
                                               key="graph_comp_emp", index=2)

        with col3ce:
            cols_to_plot_comp_emp = []
            if show_urbain_comp_emp: cols_to_plot_comp_emp.append("Urbain")
            if show_rural_comp_emp: cols_to_plot_comp_emp.append("Rural")
            if show_total_comp_emp: cols_to_plot_comp_emp.append("Total")

            if cols_to_plot_comp_emp and annees_select_emp:
                df_melted_emp = pd.DataFrame()
                for col in cols_to_plot_comp_emp:
                    df_sub_emp = df_emploi[df_emploi["Milieu"] == col].melt(id_vars=["Sexe"],
                                                                            value_vars=annees_select_emp,
                                                                            var_name="Année", value_name="Valeur")
                    df_sub_emp["Milieu"] = col
                    df_melted_emp = pd.concat([df_melted_emp, df_sub_emp], ignore_index=True)

                if graph_type_comp_emp == "Slope Chart":
                    fig = px.line(df_melted_emp, x="Année", y="Valeur", color="Sexe", line_group="Milieu", markers=True)
                    fig.update_layout(template="plotly_white", title="Slope Chart : évolution multi-années")
                    st.plotly_chart(fig, use_container_width=True)

                elif graph_type_comp_emp == "Bar Comparatif":
                    fig = px.bar(df_melted_emp, x="Sexe", y="Valeur", color="Année", barmode="group",
                                 facet_col="Milieu")
                    st.plotly_chart(fig, use_container_width=True)

                elif graph_type_comp_emp == "Heatmap":
                    df_heat = df_melted_emp.pivot_table(index="Sexe", columns="Année", values="Valeur", aggfunc="mean")
                    fig = px.imshow(df_heat, text_auto=True, aspect="auto", color_continuous_scale="Blues")

                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("⚠ Veuillez sélectionner au moins un milieu et une année !")
        ########## taaaaaaaaaaaaaab 4

        # ================== TITRE ==================
        st.markdown("""
        <h4 style='color: #85919e;margin-left: 0px;'>
        4-Taux d'activité et de chômage par province/préfecture (2016)
        </h4>
        """, unsafe_allow_html=True)

        # ================== Données ==================
        data_indicateurs = {
            "Province": ["Agadir Ida Outanane", "Inezgane Ait Melloul", "Taroudannt", "Région"],
            "Taux_Activité_Urbain": [41.6, 42.2, 43.9, 41.5],
            "Taux_Chômage_Urbain": [16.7, 11.8, 13.8, 13.9],
            "Taux_Activité_Rural": [50.5, 47.0, 57.8, 52.1],
            "Taux_Chômage_Rural": [3.3, 14.5, 3.8, 4.7],
            "Taux_Activité_Total": [45.4, 42.5, 54.1, 46.6],
            "Taux_Chômage_Total": [10.4, 12.0, 5.9, 9.0]
        }
        df_ind = pd.DataFrame(data_indicateurs)

        # ================== Palette harmonieuse ==================
        custom_palette = [
            "#1f77b4",  # bleu
            "#2ca02c",  # vert
            "#ff7f0e",  # orange
            "#17becf",  # turquoise
            "#9467bd",  # violet doux
            "#8c564b",  # brun clair
            "#e377c2",  # rose
            "#7f7f7f"  # gris
        ]

        # ================== Première ligne : Visualisation individuelle ==================
        col1i, col2i, col3i = st.columns([1, 3, 1])

        with col1i:
            st.markdown("<br><br>", unsafe_allow_html=True)
            indicateur_select = st.selectbox("Choisir un indicateur",
                                             ["Taux_Activité", "Taux_Chômage"],
                                             key="indicateur_select")
            milieu_options = ["Urbain", "Rural", "Total"]
            milieux_select = st.multiselect("Sélectionner milieux", milieu_options, default=milieu_options)
            graph_options_ind = ["Barres", "Radar", "Scatter", "Treemap"]
            graph_type_ind = st.selectbox("Type de graphique", graph_options_ind, key="graph_ind", index=1)

        with col2i:
            if milieux_select:
                df_plot_ind = pd.DataFrame()
                for milieu in milieux_select:
                    col_name = f"{indicateur_select}_{milieu}"
                    df_temp = df_ind[["Province", col_name]].rename(columns={col_name: "Valeur"})
                    df_temp["Milieu"] = milieu
                    df_temp["Indicateur"] = indicateur_select
                    df_plot_ind = pd.concat([df_plot_ind, df_temp], ignore_index=True)

                if graph_type_ind == "Barres":
                    fig = px.bar(df_plot_ind, x="Province", y="Valeur", color="Milieu", barmode="group",
                                 text="Valeur", color_discrete_sequence=custom_palette)
                    fig.update_traces(textposition="outside")
                    st.plotly_chart(fig, use_container_width=True)

                elif graph_type_ind == "Radar":
                    fig = px.line_polar(df_plot_ind, r="Valeur", theta="Province", color="Milieu",
                                        line_close=True, markers=True, color_discrete_sequence=custom_palette)
                    st.plotly_chart(fig, use_container_width=True)

                elif graph_type_ind == "Scatter":
                    fig = px.scatter(df_plot_ind, x="Province", y="Valeur", color="Milieu", size="Valeur",
                                     symbol="Milieu", color_discrete_sequence=custom_palette)
                    st.plotly_chart(fig, use_container_width=True)

                elif graph_type_ind == "Treemap":
                    fig = px.treemap(df_plot_ind, path=["Milieu", "Province"], values="Valeur", color="Valeur",
                                     color_continuous_scale="Tealrose")
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("⚠ Veuillez sélectionner au moins un milieu !")

        with col3i:
            st.markdown("<br><br><br>", unsafe_allow_html=True)
            st.dataframe(df_ind, use_container_width=True)

        # ================== Deuxième ligne : Comparaison multi-indicateurs ==================
        st.markdown("""
        <div style='background-color: #aab5bf; border-radius: 12px; padding: 8px 16px;
         text-align: center; color: white; font-weight: bold; font-size: 18px; display: inline-block;'>
        Analyse Comparative et Évolution des Données (2016)
        </div>
        """, unsafe_allow_html=True)

        col1ci, col2ci, col3ci = st.columns([1, 1, 3])

        with col1ci:
            st.markdown("<br><br><br><br><br>", unsafe_allow_html=True)
            st.markdown("""
            - Activité plus forte en rural.  
            - Chômage beaucoup plus élevé en urbain.  
            - Taroudannt affiche le meilleur taux d’activité.  
            """)

        with col2ci:
            st.markdown("<br><br><br>", unsafe_allow_html=True)
            indicateurs_multi = st.multiselect("Choisir indicateurs à comparer",
                                               ["Taux_Activité", "Taux_Chômage"],
                                               default=["Taux_Activité", "Taux_Chômage"])
            milieux_multi = st.multiselect("Choisir milieux", milieu_options, default=milieu_options,
                                           key="milieux_multi")
            graph_options_comp_ind = ["Grouped Bar", "Heatmap", "Boxplot"]
            graph_type_comp_ind = st.selectbox("Type de graphique comparatif", graph_options_comp_ind,
                                               key="graph_comp_ind", index=1)

        with col3ci:
            if indicateurs_multi and milieux_multi:
                df_melted_ind = pd.DataFrame()
                for ind in indicateurs_multi:
                    for milieu in milieux_multi:
                        col_name = f"{ind}_{milieu}"
                        df_temp = df_ind[["Province", col_name]].rename(columns={col_name: "Valeur"})
                        df_temp["Milieu"] = milieu
                        df_temp["Indicateur"] = ind
                        df_melted_ind = pd.concat([df_melted_ind, df_temp], ignore_index=True)

                if graph_type_comp_ind == "Grouped Bar":
                    fig = px.bar(df_melted_ind, x="Province", y="Valeur", color="Indicateur", barmode="group",
                                 facet_col="Milieu", color_discrete_sequence=custom_palette)
                    st.plotly_chart(fig, use_container_width=True)

                elif graph_type_comp_ind == "Heatmap":
                    df_heat = df_melted_ind.pivot_table(index="Province", columns=["Indicateur", "Milieu"],
                                                        values="Valeur")
                    fig = px.imshow(df_heat, text_auto=True, aspect="auto", color_continuous_scale="Viridis")
                    st.plotly_chart(fig, use_container_width=True)

                elif graph_type_comp_ind == "Boxplot":
                    fig = px.box(df_melted_ind, x="Indicateur", y="Valeur", color="Milieu",
                                 points="all", color_discrete_sequence=custom_palette)
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("⚠ Veuillez sélectionner au moins un milieu et un indicateur !")
        # taaaaaaaaaaaaaaaaaab 5

        # ================== TITRE ==================
        st.markdown("""
        <h4 style='color: #85919e;margin-left: 0px;'>
        5-Population active en chômage par âge et milieu de résidence
        </h4>
        """, unsafe_allow_html=True)

        # ================== Données ==================
        data_chomage = {
            "Milieu": ["Région", "Urbain Région", "Rural Région", "Maroc", "Urbain Maroc", "Rural Maroc"],
            "15-24": [26013, 16908, 9105, 392146, 283177, 108969],
            "25-34": [37556, 27910, 9646, 480693, 403509, 77184],
            "35-44": [12984, 9538, 2510, 135407, 113254, 22153],
            "45+": [8794, 6604, 2190, 97318, 79023, 18295],
            "Total": [84411, 60960, 23451, 1105564, 878963, 226601]
        }

        df_chomage = pd.DataFrame(data_chomage)

        # ================== Palette harmonieuse ==================
        custom_palette = ["#4E79A7", "#F28E2B", "#E15759", "#76B7B2", "#59A14F", "#EDC948"]

        # ================== Première ligne : Visualisation individuelle ==================
        col1i, col2i, col3i = st.columns([1, 3, 1])

        with col1i:
            st.markdown("<br><br>", unsafe_allow_html=True)
            age_select = st.selectbox("Choisir une tranche d'âge", ["15-24", "25-34", "35-44", "45+", "Total"])
            milieux_select = st.multiselect("Sélectionner milieux", df_chomage["Milieu"].unique(),
                                            default=df_chomage["Milieu"].unique())
            graph_options = ["Barres", "Radar", "Scatter", "Treemap"]
            graph_type = st.selectbox("Type de graphique", graph_options, index=3)

        with col2i:
            if milieux_select:
                df_plot = pd.DataFrame()
                for milieu in milieux_select:
                    df_temp = df_chomage[df_chomage["Milieu"] == milieu][["Milieu", age_select]].rename(
                        columns={age_select: "Valeur"})
                    df_temp["Milieu"] = milieu
                    df_plot = pd.concat([df_plot, df_temp], ignore_index=True)

                if graph_type == "Barres":
                    fig = px.bar(df_plot, x="Milieu", y="Valeur", color="Milieu", text="Valeur",
                                 color_discrete_sequence=custom_palette)
                    fig.update_traces(textposition="outside")
                    st.plotly_chart(fig, use_container_width=True)

                elif graph_type == "Radar":
                    fig = px.line_polar(df_plot, r="Valeur", theta="Milieu", line_close=True, markers=True,
                                        color="Milieu", color_discrete_sequence=custom_palette)
                    st.plotly_chart(fig, use_container_width=True)

                elif graph_type == "Scatter":
                    fig = px.scatter(df_plot, x="Milieu", y="Valeur", size="Valeur", color="Milieu",
                                     symbol="Milieu", color_discrete_sequence=custom_palette)
                    st.plotly_chart(fig, use_container_width=True)

                elif graph_type == "Treemap":
                    fig = px.treemap(df_plot, path=["Milieu"], values="Valeur", color="Valeur",
                                     color_continuous_scale="Tealrose")
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("⚠ Veuillez sélectionner au moins un milieu !")

        with col3i:
            st.markdown("<br><br><br>", unsafe_allow_html=True)
            st.dataframe(df_chomage, use_container_width=True)

        # ================== Deuxième ligne : Comparaison multi-indicateurs ==================
        st.markdown("""
        <div style='background-color: #aab5bf; border-radius: 12px; padding: 8px 16px;
         text-align: center; color: white; font-weight: bold; font-size: 18px; display: inline-block;'>
        Analyse Comparative des populations en chômage par âge et milieu
        </div>
        """, unsafe_allow_html=True)

        col1c, col2c, col3c = st.columns([1, 1, 3])

        with col1c:
            st.markdown("<br><br><br><br><br><br>", unsafe_allow_html=True)
            st.markdown("""
            - Les jeunes (15-24 ans) représentent une forte proportion du chômage.  


            - Le milieu urbain a globalement plus de chômeurs que le rural.  


            - La population totale du Maroc dépasse largement celle de la région.  
            """)

        with col2c:
            st.markdown("<br><br><br>", unsafe_allow_html=True)
            ages_multi = st.multiselect("Choisir tranches d'âge à comparer",
                                        ["15-24", "25-34", "35-44", "45+", "Total"],
                                        default=["15-24", "25-34", "35-44", "45+", "Total"])
            milieux_multi = st.multiselect("Choisir milieux", df_chomage["Milieu"].unique(),
                                           default=df_chomage["Milieu"].unique(),
                                           key="milieux_multio")
            graph_options_comp = ["Grouped Bar", "Heatmap", "Boxplot"]
            graph_type_comp = st.selectbox("Type de graphique comparatif", graph_options_comp, index=2)

        with col3c:
            if ages_multi and milieux_multi:
                df_melted = pd.DataFrame()
                for age in ages_multi:
                    for milieu in milieux_multi:
                        df_temp = df_chomage[df_chomage["Milieu"] == milieu][["Milieu", age]].rename(
                            columns={age: "Valeur"})
                        df_temp["Âge"] = age
                        df_temp["Milieu"] = milieu
                        df_melted = pd.concat([df_melted, df_temp], ignore_index=True)

                if graph_type_comp == "Grouped Bar":
                    fig = px.bar(df_melted, x="Âge", y="Valeur", color="Milieu", barmode="group",
                                 color_discrete_sequence=custom_palette)
                    st.plotly_chart(fig, use_container_width=True)

                elif graph_type_comp == "Heatmap":
                    df_heat = df_melted.pivot_table(index="Milieu", columns="Âge", values="Valeur")
                    fig = px.imshow(df_heat, text_auto=True, aspect="auto", color_continuous_scale="Viridis")
                    st.plotly_chart(fig, use_container_width=True)

                elif graph_type_comp == "Boxplot":
                    fig = px.box(df_melted, x="Âge", y="Valeur", color="Milieu", points="all",
                                 color_discrete_sequence=custom_palette)
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("⚠ Veuillez sélectionner au moins un milieu et une tranche d'âge !")

        ############taaaaaaaaab 6

        st.markdown("""
        <style>
        /* Multiselect et selectbox */
        div.stMultiSelect > div:first-child, div.stSelectbox > div:first-child {
            background-color: #e8f0f5;
            border-radius: 6px;
        }
        div.stMultiSelect div.css-1cpxqw2, div.stSelectbox div.css-1cpxqw2 {
            color: #4E79A7;
            font-weight: bold;
        }
        /* Checkbox */
        div.stCheckbox > div {
            color: #4E79A7;
        }
        </style>
        """, unsafe_allow_html=True)

        # ================== TITRE ==================
        st.markdown("""
        <h4 style='color: #85919e;margin-left: 0px;'>
        6-Taux de chômage selon le niveau du diplôme et le milieu de résidence (2016)
        </h4>
        """, unsafe_allow_html=True)

        # ================== Données ==================
        data_diplome = {
            "Milieu": ["Région", "Urbain Région", "Rural Région", "Maroc", "Urbain Maroc", "Rural Maroc"],
            "Sans diplôme": [3.9, 7.3, 2.2, 3.8, 6.5, 2.2],
            "Niveau moyenne": [13.1, 16.5, 8.5, 14.3, 17.2, 8.5],
            "Niveau supérieur": [23.7, 21.9, 34.0, 21.9, 21.1, 33.3],
            "Total": [9.0, 13.9, 4.7, 9.4, 13.9, 4.2]
        }

        df_diplome = pd.DataFrame(data_diplome)

        # ================== Palette harmonieuse ==================
        custom_palette = ["#1b1b42", "#b89c5c", "#5e0711", "#79947a", "#c99fc0", "#a7b8b6"]

        # ================== Première ligne : Visualisation individuelle ==================
        col1i, col2i, col3i = st.columns([1, 3, 1])

        with col1i:
            st.markdown("<br><br>", unsafe_allow_html=True)
            niveau_select = st.selectbox("Choisir un niveau de diplôme",
                                         ["Sans diplôme", "Niveau moyenne", "Niveau supérieur", "Total"])
            milieux_select = st.multiselect("Sélectionner milieux", df_diplome["Milieu"].unique(),
                                            default=df_diplome["Milieu"].unique(), key="1")
            graph_options = ["Barres", "Radar", "Scatter", "Treemap", "Funnel"]
            graph_type = st.selectbox("Type de graphique", graph_options, index=4)

        with col2i:
            if milieux_select:
                df_plot = pd.DataFrame()
                for milieu in milieux_select:
                    df_temp = df_diplome[df_diplome["Milieu"] == milieu][["Milieu", niveau_select]].rename(
                        columns={niveau_select: "Valeur"})
                    df_temp["Milieu"] = milieu
                    df_plot = pd.concat([df_plot, df_temp], ignore_index=True)

                if graph_type == "Barres":
                    fig = px.bar(df_plot, x="Milieu", y="Valeur", color="Milieu", text="Valeur",
                                 color_discrete_sequence=custom_palette)
                    fig.update_traces(textposition="outside")
                    st.plotly_chart(fig, use_container_width=True)

                elif graph_type == "Radar":
                    fig = px.line_polar(df_plot, r="Valeur", theta="Milieu", line_close=True, markers=True,
                                        color="Milieu", color_discrete_sequence=custom_palette)
                    st.plotly_chart(fig, use_container_width=True)

                elif graph_type == "Scatter":
                    fig = px.scatter(df_plot, x="Milieu", y="Valeur", size="Valeur", color="Milieu",
                                     symbol="Milieu", color_discrete_sequence=custom_palette)
                    st.plotly_chart(fig, use_container_width=True)

                elif graph_type == "Treemap":
                    fig = px.treemap(df_plot, path=["Milieu"], values="Valeur", color="Valeur",
                                     color_continuous_scale="Tealrose")
                    st.plotly_chart(fig, use_container_width=True)

                elif graph_type == "Funnel":
                    fig = px.funnel(df_plot, x="Milieu", y="Valeur", color="Milieu",
                                    color_discrete_sequence=custom_palette)
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("⚠ Veuillez sélectionner au moins un milieu !")

        with col3i:
            st.markdown("<br><br><br>", unsafe_allow_html=True)
            st.dataframe(df_diplome, use_container_width=True)

        # ================== Deuxième ligne : Comparaison multi-niveaux ==================
        st.markdown("""
        <div style='background-color: #aab5bf; border-radius: 12px; padding: 8px 16px;
         text-align: center; color: white; font-weight: bold; font-size: 18px; display: inline-block;'>
        Analyse Comparative du chômage par niveau de diplôme et milieu
        </div>
        """, unsafe_allow_html=True)

        col1c, col2c, col3c = st.columns([1, 1, 3])

        with col1c:
            st.markdown("<br><br><br><br><br><br>", unsafe_allow_html=True)
            st.markdown("""
            - Le chômage augmente avec le niveau du diplôme en région rurale. 


            - Urbain a un chômage globalement plus élevé que rural.  


            - La population totale du Maroc présente un taux intermédiaire.  
            """)

        with col2c:
            st.markdown("<br><br><br>", unsafe_allow_html=True)
            niveaux_multi = st.multiselect("Choisir niveaux à comparer",
                                           ["Sans diplôme", "Niveau moyenne", "Niveau supérieur", "Total"],
                                           default=["Sans diplôme", "Niveau moyenne", "Niveau supérieur", "Total"],
                                           key="2")
            milieux_multi = st.multiselect("Choisir milieux", df_diplome["Milieu"].unique(),
                                           default=df_diplome["Milieu"].unique(),
                                           key="milieux_multip")
            graph_options_comp = ["Grouped Bar", "Heatmap", "Boxplot", "Funnel"]
            graph_type_comp = st.selectbox("Type de graphique comparatif", graph_options_comp, index=3)

        with col3c:
            st.markdown("<br><br>", unsafe_allow_html=True)
            if niveaux_multi and milieux_multi:
                df_melted = pd.DataFrame()
                for niveau in niveaux_multi:
                    for milieu in milieux_multi:
                        df_temp = df_diplome[df_diplome["Milieu"] == milieu][["Milieu", niveau]].rename(
                            columns={niveau: "Valeur"})
                        df_temp["Niveau"] = niveau
                        df_temp["Milieu"] = milieu
                        df_melted = pd.concat([df_melted, df_temp], ignore_index=True)

                if graph_type_comp == "Grouped Bar":
                    fig = px.bar(df_melted, x="Niveau", y="Valeur", color="Milieu", barmode="group",
                                 color_discrete_sequence=custom_palette)
                    st.plotly_chart(fig, use_container_width=True)

                elif graph_type_comp == "Heatmap":
                    df_heat = df_melted.pivot_table(index="Milieu", columns="Niveau", values="Valeur")
                    fig = px.imshow(df_heat, text_auto=True, aspect="auto", color_continuous_scale="Viridis")
                    st.plotly_chart(fig, use_container_width=True)

                elif graph_type_comp == "Boxplot":
                    fig = px.box(df_melted, x="Niveau", y="Valeur", color="Milieu", points="all",
                                 color_discrete_sequence=custom_palette)
                    st.plotly_chart(fig, use_container_width=True)

                elif graph_type_comp == "Funnel":
                    fig = px.funnel(df_melted, x="Niveau", y="Valeur", color="Milieu",
                                    color_discrete_sequence=custom_palette)
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("⚠ Veuillez sélectionner au moins un milieu et un niveau !")

        ########################## taaaaaaaab 7

        # ================== STYLE ==================
        st.markdown("""
        <style>
        /* Checkbox custom */
        div.stCheckbox > label {
            color: #4E79A7 !important;
            font-weight: bold;
        }
        </style>
        """, unsafe_allow_html=True)

        # ================== TITRE ==================
        st.markdown("""
        <h4 style='color: #85919e;margin-left: 0px;'>
        7 - Population active occupée selon l’âge et le milieu de résidence
        </h4>
        """, unsafe_allow_html=True)

        # ================== Données ==================
        data_age = {
            "Âge": ["15-24", "25-34", "35-44", "45 et plus", "Total"],
            "Région-Urbain": [28537, 122684, 107949, 117604, 376774],
            "Région-Rural": [74003, 144680, 101353, 159340, 479376],
            "Région-Total": [102540, 267364, 209302, 276944, 856150],
            "Maroc-Urbain": [406879, 1607948, 1576580, 1836830, 5428237],
            "Maroc-Rural": [944659, 1475434, 1088876, 1704415, 5213384],
            "Maroc-Total": [1351538, 3083382, 2665456, 3541245, 10641621]
        }
        df_age = pd.DataFrame(data_age)

        # ================== Palette ==================
        custom_palette = ["#1b1b42", "#b89c5c", "#5e0711", "#79947a", "#c99fc0", "#a7b8b6"]

        # ================== Première ligne ==================
        col1a, col2a, col3a = st.columns([1, 3, 1])

        with col1a:
            st.markdown("<br><br>", unsafe_allow_html=True)
            age_select = st.selectbox("Choisir une tranche d’âge",
                                      df_age["Âge"].unique(), key="age_select_6")

            st.write("### Sélectionner milieux")
            milieux_select = []
            for milieu in df_age.columns[1:]:
                if st.checkbox(milieu, value=True, key=f"milieux_select_{milieu}"):
                    milieux_select.append(milieu)

            graph_options = ["Barres", "Lignes", "Radar", "Scatter", "Aires"]
            graph_type = st.selectbox("Type de graphique", graph_options, index=4, key="graph_type_6")

        with col2a:
            st.markdown("<br><br><br>", unsafe_allow_html=True)
            if milieux_select:
                df_plot = pd.DataFrame()
                for milieu in milieux_select:
                    valeur = df_age[df_age["Âge"] == age_select][milieu].values[0]
                    df_plot = pd.concat([df_plot, pd.DataFrame({"Milieu": [milieu], "Valeur": [valeur]})],
                                        ignore_index=True)

                if graph_type == "Barres":
                    fig = px.bar(df_plot, x="Milieu", y="Valeur", color="Milieu", text="Valeur",
                                 color_discrete_sequence=custom_palette)
                    fig.update_traces(textposition="outside")

                elif graph_type == "Lignes":
                    fig = px.line(df_plot, x="Milieu", y="Valeur", color="Milieu", markers=True,
                                  color_discrete_sequence=custom_palette)

                elif graph_type == "Radar":
                    fig = px.line_polar(df_plot, r="Valeur", theta="Milieu", line_close=True, markers=True,
                                        color="Milieu", color_discrete_sequence=custom_palette)

                elif graph_type == "Scatter":
                    fig = px.scatter(df_plot, x="Milieu", y="Valeur", size="Valeur", color="Milieu",
                                     symbol="Milieu", color_discrete_sequence=custom_palette)

                elif graph_type == "Aires":
                    fig = px.area(df_plot, x="Milieu", y="Valeur", color="Milieu",
                                  color_discrete_sequence=custom_palette)

                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("⚠ Veuillez sélectionner au moins un milieu !")

        with col3a:
            st.markdown("<br><br><br><br><br><br>", unsafe_allow_html=True)
            st.dataframe(df_age, use_container_width=True)

        # ================== Deuxième ligne ==================
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div style='background-color: #aab5bf; border-radius: 12px; padding: 8px 16px;
         text-align: center; color: white; font-weight: bold; font-size: 18px; display: inline-block;'>
        Analyse Comparative par âge et milieu
        </div>
        """, unsafe_allow_html=True)

        col1b, col2b, col3b = st.columns([1, 1, 3])

        with col1b:
            st.markdown("<br><br><br><br><br><br><br>", unsafe_allow_html=True)
            st.markdown("""
            - En zone **urbaine**, la concentration est plus forte sur les 25-34 ans. 

            """)
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("""

                        - En zone **rurale**, le poids des 45 ans et + est plus marqué.  

                        """)
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("""

                        - La répartition nationale suit une logique mixte.  
                        """)

        with col2b:
            st.markdown("<br><br>", unsafe_allow_html=True)

            st.write("### Choisir tranches d’âge à comparer")
            ages_multi = []
            for age in df_age["Âge"].unique():
                if st.checkbox(age, value=True, key=f"ages_multi_{age}"):
                    ages_multi.append(age)

            st.write("### Choisir milieux")
            milieux_multi = []
            for milieu in df_age.columns[1:]:
                if st.checkbox(milieu, value=True, key=f"milieux_multi2_{milieu}"):
                    milieux_multi.append(milieu)

            graph_options_comp = ["Grouped Bar", "Heatmap", "Boxplot", "Lignes"]
            graph_type_comp = st.selectbox("Type de graphique comparatif", graph_options_comp, index=0,
                                           key="graph_type_comp_6")

        with col3b:
            st.markdown("<br><br><br><br>", unsafe_allow_html=True)
            if ages_multi and milieux_multi:
                df_melted = pd.DataFrame()
                for age in ages_multi:
                    for milieu in milieux_multi:
                        valeur = df_age[df_age["Âge"] == age][milieu].values[0]
                        df_melted = pd.concat(
                            [df_melted, pd.DataFrame({"Âge": [age], "Milieu": [milieu], "Valeur": [valeur]})],
                            ignore_index=True)

                if graph_type_comp == "Grouped Bar":
                    fig = px.bar(df_melted, x="Âge", y="Valeur", color="Milieu", barmode="group",
                                 color_discrete_sequence=custom_palette)

                elif graph_type_comp == "Heatmap":
                    df_heat = df_melted.pivot_table(index="Milieu", columns="Âge", values="Valeur")
                    fig = px.imshow(df_heat, text_auto=True, aspect="auto", color_continuous_scale="Viridis")

                elif graph_type_comp == "Boxplot":
                    fig = px.box(df_melted, x="Âge", y="Valeur", color="Milieu", points="all",
                                 color_discrete_sequence=custom_palette)

                elif graph_type_comp == "Lignes":
                    fig = px.line(df_melted, x="Âge", y="Valeur", color="Milieu", markers=True,
                                  color_discrete_sequence=custom_palette)

                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("⚠ Veuillez sélectionner au moins un milieu et un âge !")

                ###################### taaaab 8
        import streamlit as st
        import pandas as pd
        import plotly.express as px

        # ================== STYLE ==================
        st.markdown("""
        <style>
        div.stCheckbox > label {
            color: #4E79A7 !important;
            font-weight: bold;
        }
        </style>
        """, unsafe_allow_html=True)

        # ================== TITRE ==================
        st.markdown("""
        <h4 style='color: #85919e;margin-left: 0px;'>
        8- Population active occupée selon le sexe et le milieu de résidence (2016)
        </h4>
        """, unsafe_allow_html=True)

        # ================== Données ==================
        data_sexe = {
            "Milieu": ["Région", "Urbain", "Rural", "Maroc", "Urbain", "Rural"],
            "Masculin": [610608, 314710, 295898, 7884294, 4386974, 3497320],
            "Féminin": [245542, 62064, 183478, 2757327, 1041263, 1716064],
            "Total": [856150, 376774, 479376, 10641621, 5428237, 5213384]
        }
        df_sexe = pd.DataFrame(data_sexe)

        # ================== Palette ==================
        custom_palette = ["#A3C1AD", "#F6C3B7", "#F7E3AF", "#C1D3E0", "#D6A3C1", "#E0D3B8"]

        # ================== Première ligne ==================
        col1a, col2a, col3a = st.columns([1, 3, 1])

        with col1a:
            st.markdown("<br><br>", unsafe_allow_html=True)

            milieu_select = st.selectbox("Choisir un milieu de résidence",
                                         df_sexe["Milieu"].unique(), key="milieu_select_7")

            st.write("### Sélectionner catégories")
            categories_select = []
            for col in ["Masculin", "Féminin", "Total"]:
                if st.checkbox(col, value=True, key=f"categories_select_{col}"):
                    categories_select.append(col)

            graph_options = ["Barres", "Lignes", "Radar", "Scatter", "Aires"]
            graph_type = st.selectbox("Type de graphique", graph_options, index=2, key="graph_type_7")

        with col2a:
            if categories_select:
                df_plot = pd.DataFrame()
                for cat in categories_select:
                    valeur = df_sexe[df_sexe["Milieu"] == milieu_select][cat].values[0]
                    df_plot = pd.concat([df_plot, pd.DataFrame({"Catégorie": [cat], "Valeur": [valeur]})],
                                        ignore_index=True)

                if graph_type == "Barres":
                    fig = px.bar(df_plot, x="Catégorie", y="Valeur", color="Catégorie", text="Valeur",
                                 color_discrete_sequence=custom_palette)
                    fig.update_traces(textposition="outside")

                elif graph_type == "Lignes":
                    fig = px.line(df_plot, x="Catégorie", y="Valeur", color="Catégorie", markers=True,
                                  color_discrete_sequence=custom_palette)

                elif graph_type == "Radar":
                    fig = px.line_polar(df_plot, r="Valeur", theta="Catégorie", line_close=True, markers=True,
                                        color="Catégorie", color_discrete_sequence=custom_palette)

                elif graph_type == "Scatter":
                    fig = px.scatter(df_plot, x="Catégorie", y="Valeur", size="Valeur", color="Catégorie",
                                     symbol="Catégorie", color_discrete_sequence=custom_palette)

                elif graph_type == "Aires":
                    fig = px.area(df_plot, x="Catégorie", y="Valeur", color="Catégorie",
                                  color_discrete_sequence=custom_palette)

                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("⚠ Veuillez sélectionner au moins une catégorie !")

        with col3a:
            st.markdown("<br><br><br>", unsafe_allow_html=True)
            st.dataframe(df_sexe, use_container_width=True)

        # ================== Deuxième ligne ==================
        st.markdown("""
        <div style='background-color: #aab5bf; border-radius: 12px; padding: 8px 16px;
         text-align: center; color: white; font-weight: bold; font-size: 18px; display: inline-block;'>
        Analyse Comparative par sexe et milieu
        </div>
        """, unsafe_allow_html=True)

        col1b, col2b, col3b = st.columns([1, 1, 3])

        with col1b:
            st.markdown("<br><br><br><br><br>", unsafe_allow_html=True)
            st.markdown("""
            - Les hommes dominent largement la population active.  

            """)
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("""

                        - Les femmes sont proportionnellement plus présentes en **rural** que dans les villes.  

                        """)
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("""

                        - La structure nationale est marquée par une forte disparité de genre.  
                        """)

        with col2b:
            st.markdown("<br><br>", unsafe_allow_html=True)

            st.write("### Choisir milieux")
            milieux_multi = []
            for milieu in df_sexe["Milieu"].unique():
                if st.checkbox(milieu, value=True, key=f"milieux_multi3_{milieu}"):
                    milieux_multi.append(milieu)

            st.write("### Choisir catégories")
            categories_multi = []
            for col in ["Masculin", "Féminin", "Total"]:
                if st.checkbox(col, value=True, key=f"categories_multi_{col}"):
                    categories_multi.append(col)

            graph_options_comp = ["Grouped Bar", "Heatmap", "Boxplot", "Lignes"]
            graph_type_comp = st.selectbox("Type de graphique comparatif", graph_options_comp, index=0,
                                           key="graph_type_comp_7")

        with col3b:
            st.markdown("<br><br>", unsafe_allow_html=True)
            if milieux_multi and categories_multi:
                df_melted = pd.DataFrame()
                for milieu in milieux_multi:
                    for cat in categories_multi:
                        valeur = df_sexe[df_sexe["Milieu"] == milieu][cat].values[0]
                        df_melted = pd.concat(
                            [df_melted, pd.DataFrame({"Milieu": [milieu], "Catégorie": [cat], "Valeur": [valeur]})],
                            ignore_index=True)

                if graph_type_comp == "Grouped Bar":
                    fig = px.bar(df_melted, x="Milieu", y="Valeur", color="Catégorie", barmode="group",
                                 color_discrete_sequence=custom_palette)

                elif graph_type_comp == "Heatmap":
                    df_heat = df_melted.pivot_table(index="Catégorie", columns="Milieu", values="Valeur")
                    fig = px.imshow(df_heat, text_auto=True, aspect="auto", color_continuous_scale="Viridis")

                elif graph_type_comp == "Boxplot":
                    fig = px.box(df_melted, x="Milieu", y="Valeur", color="Catégorie", points="all",
                                 color_discrete_sequence=custom_palette)

                elif graph_type_comp == "Lignes":
                    fig = px.line(df_melted, x="Milieu", y="Valeur", color="Catégorie", markers=True,
                                  color_discrete_sequence=custom_palette)

                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("⚠ Veuillez sélectionner au moins un milieu et une catégorie !")

                ################### tab 9

        # ================== STYLE ==================
        st.markdown("""
        <style>
        div.stCheckbox > label {
            color: #4E79A7 !important;
            font-weight: bold;
        }
        </style>
        """, unsafe_allow_html=True)

        # ================== TITRE ==================
        st.markdown("""
        <h4 style='color: #85919e;margin-left: 0px;'>
        9 - Population active occupée selon les branches d’activité économique et le milieu de résidence (2016)
        </h4>
        """, unsafe_allow_html=True)

        # ================== Données ==================
        data_secteurs = {
            "Milieu": ["Région", "Urbain", "Rural", "Maroc", "Urbain", "Rural"],
            "Forêt et pêche / Agriculture": [382657, 36085, 346572, 4042943, 244731, 3798212],
            "Industrie et commerce": [70488, 52390, 18098, 1199134, 980432, 218702],
            "B.T.P": [86324, 45408, 40916, 1042110, 610666, 431444],
            "Services": [315362, 241572, 73790, 4344867, 3580980, 763887],
            "Autres": [1319, 1319, 0, 12567, 11428, 1139],
            "Total": [856150, 376774, 479376, 10641621, 5428237, 5213384]
        }
        df_secteurs = pd.DataFrame(data_secteurs)

        # ================== Palette ==================
        custom_palette = px.colors.qualitative.Set2

        # ================== Première ligne ==================
        col1a, col2a, col3a = st.columns([1, 3, 1])

        with col1a:
            st.markdown("<br><br>", unsafe_allow_html=True)

            milieu_select = st.selectbox("Choisir un milieu de résidence",
                                         df_secteurs["Milieu"].unique(), key="milieu_select_8")

            st.write("### Sélectionner branches")
            branches_select = []
            for col in ["Forêt et pêche / Agriculture", "Industrie et commerce", "B.T.P", "Services", "Autres",
                        "Total"]:
                if st.checkbox(col, value=True, key=f"branches_select_{col}"):
                    branches_select.append(col)

            graph_options = ["Pie", "Treemap", "Sunburst", "Funnel", "Barres Horizontales"]
            graph_type = st.selectbox("Type de graphique", graph_options, index=3, key="graph_type_8")

        with col2a:
            st.markdown("<br><br><br>", unsafe_allow_html=True)

            if branches_select:
                df_plot = pd.DataFrame()
                for br in branches_select:
                    valeur = df_secteurs[df_secteurs["Milieu"] == milieu_select][br].values[0]
                    df_plot = pd.concat([df_plot, pd.DataFrame({"Branche": [br], "Valeur": [valeur]})],
                                        ignore_index=True)

                if graph_type == "Pie":
                    custom_palette = ["#A3C1AD", "#F6C3B7", "#F7E3AF", "#C1D3E0", "#D6A3C1", "#E0D3B8"]

                    # Exemple dans le graphique : Pie
                    fig = px.pie(df_plot, names="Branche", values="Valeur", color="Branche",
                                 color_discrete_sequence=custom_palette)

                elif graph_type == "Treemap":
                    fig = px.treemap(df_plot, path=["Branche"], values="Valeur", color="Branche",
                                     color_discrete_sequence=custom_palette)

                elif graph_type == "Sunburst":
                    fig = px.sunburst(df_plot, path=["Branche"], values="Valeur", color="Branche",
                                      color_discrete_sequence=custom_palette)

                elif graph_type == "Funnel":

                    custom_palette = ["#A3C1AD", "#F6C3B7", "#F7E3AF", "#C1D3E0", "#D6A3C1", "#E0D3B8"]

                    # Exemple dans le graphique : Pie
                    fig = px.funnel(df_plot, x="Valeur", y="Branche", color="Branche",
                                    color_discrete_sequence=custom_palette)

                elif graph_type == "Barres Horizontales":
                    fig = px.bar(df_plot, x="Valeur", y="Branche", orientation="h", color="Branche",
                                 text="Valeur", color_discrete_sequence=custom_palette)
                    fig.update_traces(textposition="outside")

                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("⚠ Veuillez sélectionner au moins une branche !")

        with col3a:
            st.markdown("<br><br><br><br><br><br>", unsafe_allow_html=True)
            st.dataframe(df_secteurs, use_container_width=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ================== Deuxième ligne ==================
        st.markdown("""
        <div style='background-color: #aab5bf; border-radius: 12px; padding: 8px 16px;
         text-align: center; color: white; font-weight: bold; font-size: 18px; display: inline-block;'>
        Analyse Comparative par branches d’activité et milieu
        </div>
        """, unsafe_allow_html=True)

        col1b, col2b, col3b = st.columns([1, 1, 3])

        with col1b:
            st.markdown("<br><br><br><br><br>", unsafe_allow_html=True)
            st.markdown("""
            - **Agriculture** domine largement en zone rurale.  

            """)
            st.markdown("<br><br>", unsafe_allow_html=True)
            st.markdown("""

                        - En **urbain**, les **services** prennent la première place.  
                        """)
            st.markdown("<br><br>", unsafe_allow_html=True)
            st.markdown("""
                        - La structure nationale révèle une forte dualité **rural agricole** vs **urbain tertiaire**.  
                        """)

        with col2b:
            st.markdown("<br><br>", unsafe_allow_html=True)

            st.write("### Choisir milieux")
            milieux_multi = []
            for milieu in df_secteurs["Milieu"].unique():
                if st.checkbox(milieu, value=True, key=f"milieux_multi12_{milieu}"):
                    milieux_multi.append(milieu)

            st.write("### Choisir branches")
            branches_multi = []
            for col in ["Forêt et pêche / Agriculture", "Industrie et commerce", "B.T.P", "Services", "Autres",
                        "Total"]:
                if st.checkbox(col, value=True, key=f"branches_multi_{col}"):
                    branches_multi.append(col)

            graph_options_comp = ["Stacked Bar", "Line Area", "Strip", "Density Heatmap"]
            graph_type_comp = st.selectbox("Type de graphique comparatif", graph_options_comp, index=0,
                                           key="graph_type_comp_8")

        with col3b:
            st.markdown("<br><br><br><br><br>", unsafe_allow_html=True)
            if milieux_multi and branches_multi:
                df_melted = pd.DataFrame()
                for milieu in milieux_multi:
                    for br in branches_multi:
                        valeur = df_secteurs[df_secteurs["Milieu"] == milieu][br].values[0]
                        df_melted = pd.concat(
                            [df_melted, pd.DataFrame({"Milieu": [milieu], "Branche": [br], "Valeur": [valeur]})],
                            ignore_index=True)

                if graph_type_comp == "Stacked Bar":
                    custom_palette = ["#A3C1AD", "#F6C3B7", "#F7E3AF", "#C1D3E0", "#D6A3C1", "#E0D3B8"]

                    # Exemple dans le graphique : Pie
                    fig = px.bar(df_plot, x="Branche", y="Valeur", color="Branche",
                                 text="Valeur", color_discrete_sequence=custom_palette)
                    fig.update_traces(textposition="outside")


                elif graph_type_comp == "Line Area":
                    fig = px.area(df_melted, x="Milieu", y="Valeur", color="Branche",
                                  color_discrete_sequence=custom_palette, groupnorm=None)

                elif graph_type_comp == "Strip":
                    fig = px.strip(df_melted, x="Milieu", y="Valeur", color="Branche",
                                   color_discrete_sequence=custom_palette)

                elif graph_type_comp == "Density Heatmap":
                    fig = px.density_heatmap(df_melted, x="Milieu", y="Branche", z="Valeur",
                                             color_continuous_scale="Viridis", text_auto=True)

                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("⚠ Veuillez sélectionner au moins un milieu et une branche !")

        ############33taaaab ffin

        import streamlit as st
        import pandas as pd
        import plotly.express as px

        # ================== STYLE ==================
        st.markdown("""
        <style>
        div.stCheckbox > label {
            color: #4E79A7 !important;
            font-weight: bold;
        }
        </style>
        """, unsafe_allow_html=True)

        # ================== TITRE ==================
        st.markdown("""
        <h4 style='color: #85919e;margin-left: 0px;'>
        10 - Population active occupée de la région selon le statut professionnel et le milieu de résidence (2016)
        </h4>
        """, unsafe_allow_html=True)

        # ================== Données ==================
        data_statut = {
            "Statut": ["Salariés", "Auto-emploi", "Emploi non rémunéré", "Autres", "Total"],
            "Urbain": [251639, 111477, 12802, 856, 376774],
            "Rural": [167635, 167668, 143696, 377, 479376],
            "Total": [419274, 279145, 156498, 1233, 856150]
        }
        df_statut = pd.DataFrame(data_statut)

        # ================== Palette pastel ==================
        custom_palette = ["#A3C1AD", "#F6C3B7", "#F7E3AF", "#C1D3E0", "#D6A3C1"]

        # ================== Première ligne ==================
        col1a, col2a, col3a = st.columns([1, 3, 1])

        with col1a:
            st.markdown("<br><br>", unsafe_allow_html=True)

            milieu_select = st.selectbox("Choisir un milieu de résidence",
                                         ["Urbain", "Rural", "Total"], key="milieu_select_98")

            st.write("### Sélectionner statut professionnel")
            statut_select = []
            for statut in df_statut["Statut"]:
                if st.checkbox(statut, value=True, key=f"statut_select1_{statut}"):
                    statut_select.append(statut)

            graph_options = ["Pie", "Treemap", "Sunburst", "Funnel", "Barres Horizontales"]
            graph_type = st.selectbox("Type de graphique", graph_options, index=0, key="graph_type_9")

        with col2a:
            if statut_select:
                df_plot = pd.DataFrame()
                for statut in statut_select:
                    valeur = df_statut[df_statut["Statut"] == statut][milieu_select].values[0]
                    df_plot = pd.concat([df_plot, pd.DataFrame({"Statut": [statut], "Valeur": [valeur]})],
                                        ignore_index=True)

                if graph_type == "Pie":
                    fig = px.pie(df_plot, names="Statut", values="Valeur", color="Statut",
                                 color_discrete_sequence=custom_palette)

                elif graph_type == "Treemap":
                    fig = px.treemap(df_plot, path=["Statut"], values="Valeur", color="Statut",
                                     color_discrete_sequence=custom_palette)

                elif graph_type == "Sunburst":
                    fig = px.sunburst(df_plot, path=["Statut"], values="Valeur", color="Statut",
                                      color_discrete_sequence=custom_palette)

                elif graph_type == "Funnel":
                    fig = px.funnel(df_plot, x="Valeur", y="Statut", color="Statut",
                                    color_discrete_sequence=custom_palette)

                elif graph_type == "Barres Horizontales":
                    fig = px.bar(df_plot, x="Valeur", y="Statut", orientation="h", color="Statut",
                                 text="Valeur", color_discrete_sequence=custom_palette)
                    fig.update_traces(textposition="outside")

                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("⚠ Veuillez sélectionner au moins un statut professionnel !")

        with col3a:
            st.markdown("<br><br><br>", unsafe_allow_html=True)
            st.dataframe(df_statut, use_container_width=True)

        # ================== Deuxième ligne ==================
        st.markdown("""
        <div style='background-color: #aab5bf; border-radius: 12px; padding: 8px 16px;
         text-align: center; color: white; font-weight: bold; font-size: 18px; display: inline-block;'>
        Analyse Comparative par statut professionnel et milieu
        </div>
        """, unsafe_allow_html=True)

        col1b, col2b, col3b = st.columns([1, 1, 3])

        with col1b:
            st.markdown("<br><br><br><br><br>", unsafe_allow_html=True)
            st.markdown("""
            - Les **salariés** sont majoritaires en zone urbaine.  
            - L'**auto-emploi** est plus présent en zone rurale.  
            - Les **emplois non rémunérés** concernent surtout le rural.  
            """)

        with col2b:
            st.markdown("<br><br>", unsafe_allow_html=True)

            st.write("### Choisir milieux")
            milieux_multi = []
            for milieu in ["Urbain", "Rural", "Total"]:
                if st.checkbox(milieu, value=True, key=f"milieux_multi1_{milieu}"):
                    milieux_multi.append(milieu)

            st.write("### Choisir statuts")
            statut_multi = []
            for statut in df_statut["Statut"]:
                if st.checkbox(statut, value=True, key=f"statut_multi2_{statut}"):
                    statut_multi.append(statut)

            graph_options_comp = ["Stacked Bar", "Line Area", "Strip", "Density Heatmap"]
            graph_type_comp = st.selectbox("Type de graphique comparatif", graph_options_comp, index=0,
                                           key="graph_type_comp_9")

        with col3b:
            st.markdown("<br><br>", unsafe_allow_html=True)
            if milieux_multi and statut_multi:
                df_melted = pd.DataFrame()
                for milieu in milieux_multi:
                    for statut in statut_multi:
                        valeur = df_statut[df_statut["Statut"] == statut][milieu].values[0]
                        df_melted = pd.concat(
                            [df_melted, pd.DataFrame({"Milieu": [milieu], "Statut": [statut], "Valeur": [valeur]})],
                            ignore_index=True)

                if graph_type_comp == "Stacked Bar":
                    fig = px.bar(df_melted, x="Milieu", y="Valeur", color="Statut", barmode="stack",
                                 color_discrete_sequence=custom_palette)

                elif graph_type_comp == "Line Area":
                    fig = px.area(df_melted, x="Milieu", y="Valeur", color="Statut",
                                  color_discrete_sequence=custom_palette)

                elif graph_type_comp == "Strip":
                    fig = px.strip(df_melted, x="Milieu", y="Valeur", color="Statut",
                                   color_discrete_sequence=custom_palette)

                elif graph_type_comp == "Density Heatmap":
                    fig = px.density_heatmap(df_melted, x="Milieu", y="Statut", z="Valeur",
                                             color_continuous_scale="Viridis", text_auto=True)

                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("⚠ Veuillez sélectionner au moins un milieu et un statut !")

        ##########33taaaaaaab 10 fffffinnn

        st.markdown("""
        <style>
        div.stCheckbox > label {
            color: #4E79A7 !important;
            font-weight: bold;
        }
        </style>
        """, unsafe_allow_html=True)

        # ================== TITRE ==================
        st.markdown("""
        <h4 style='color: #85919e;margin-left: 0px;'>
        10 - Population active occupée de la région selon le statut professionnel et le milieu de résidence (2016)
        </h4>
        """, unsafe_allow_html=True)

        # ================== Données ==================
        data_statut = {
            "Statut": ["Salariés", "Auto-emploi", "Emploi non rémunéré", "Autres", "Total"],
            "Urbain": [251639, 111477, 12802, 856, 376774],
            "Rural": [167635, 167668, 143696, 377, 479376],
            "Total": [419274, 279145, 156498, 1233, 856150]
        }
        df_statut = pd.DataFrame(data_statut)

        # ================== Palette pastel ==================
        custom_palette = ["#c9b8b5", "#62647a", "#7c8f83", "#806f82", "#9cadad"]

        # ================== Première ligne ==================
        col1a, col2a, col3a = st.columns([1, 3, 1])

        with col1a:
            st.markdown("<br><br>", unsafe_allow_html=True)

            milieu_select = st.selectbox("Choisir un milieu de résidence",
                                         ["Urbain", "Rural", "Total"], key="milieu_select_99")

            st.write("### Sélectionner statut professionnel")
            statut_select = []
            for statut in df_statut["Statut"]:
                if st.checkbox(statut, value=True, key=f"statut_select2_{statut}"):
                    statut_select.append(statut)

            graph_options = ["Pie", "Treemap", "Sunburst", "Funnel", "Barres Horizontales"]
            graph_type = st.selectbox("Type de graphique", graph_options, index=0, key="graph_type1_9")

        with col2a:
            st.markdown("<br><br><br>", unsafe_allow_html=True)

            if statut_select:
                df_plot = pd.DataFrame()
                for statut in statut_select:
                    valeur = df_statut[df_statut["Statut"] == statut][milieu_select].values[0]
                    df_plot = pd.concat([df_plot, pd.DataFrame({"Statut": [statut], "Valeur": [valeur]})],
                                        ignore_index=True)

                if graph_type == "Pie":
                    fig = px.pie(df_plot, names="Statut", values="Valeur", color="Statut",
                                 color_discrete_sequence=custom_palette)

                elif graph_type == "Treemap":
                    fig = px.treemap(df_plot, path=["Statut"], values="Valeur", color="Statut",
                                     color_discrete_sequence=custom_palette)

                elif graph_type == "Sunburst":
                    fig = px.sunburst(df_plot, path=["Statut"], values="Valeur", color="Statut",
                                      color_discrete_sequence=custom_palette)

                elif graph_type == "Funnel":
                    fig = px.funnel(df_plot, x="Valeur", y="Statut", color="Statut",
                                    color_discrete_sequence=custom_palette)

                elif graph_type == "Barres Horizontales":
                    fig = px.bar(df_plot, x="Valeur", y="Statut", orientation="h", color="Statut",
                                 text="Valeur", color_discrete_sequence=custom_palette)
                    fig.update_traces(textposition="outside")

                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("⚠ Veuillez sélectionner au moins un statut professionnel !")

        with col3a:
            st.markdown("<br><br><br><br><br><br>", unsafe_allow_html=True)
            st.dataframe(df_statut, use_container_width=True)

        # ================== Deuxième ligne ==================
        st.markdown("""
        <div style='background-color: #aab5bf; border-radius: 12px; padding: 8px 16px;
         text-align: center; color: white; font-weight: bold; font-size: 18px; display: inline-block;'>
        Analyse Comparative par statut professionnel et milieu
        </div>
        """, unsafe_allow_html=True)

        col1b, col2b, col3b = st.columns([1, 1, 3])

        with col1b:
            st.markdown("<br><br><br><br><br>", unsafe_allow_html=True)
            st.markdown("""
            - Les **salariés** sont majoritaires en zone urbaine.  

            """)
            st.markdown("<br><br>", unsafe_allow_html=True)
            st.markdown("""

                       - L'**auto-emploi** est plus présent en zone rurale.  

                       """)
            st.markdown("<br><br>", unsafe_allow_html=True)
            st.markdown("""

                       - Les **emplois non rémunérés** concernent surtout le rural.  
                       """)

        with col2b:
            st.markdown("<br><br>", unsafe_allow_html=True)

            st.write("### Choisir milieux")
            milieux_multi = []
            for milieu in ["Urbain", "Rural", "Total"]:
                if st.checkbox(milieu, value=True, key=f"milieux_multi2_{milieu}"):
                    milieux_multi.append(milieu)

            st.write("### Choisir statuts")
            statut_multi = []
            for statut in df_statut["Statut"]:
                if st.checkbox(statut, value=True, key=f"statut_multi1_{statut}"):
                    statut_multi.append(statut)

            graph_options_comp = ["Stacked Bar", "Line Area", "Strip", "Density Heatmap"]
            graph_type_comp = st.selectbox("Type de graphique comparatif", graph_options_comp, index=0,
                                           key="graph_type2_comp_9")

        with col3b:
            st.markdown("<br><br>", unsafe_allow_html=True)
            if milieux_multi and statut_multi:
                df_melted = pd.DataFrame()
                for milieu in milieux_multi:
                    for statut in statut_multi:
                        valeur = df_statut[df_statut["Statut"] == statut][milieu].values[0]
                        df_melted = pd.concat(
                            [df_melted, pd.DataFrame({"Milieu": [milieu], "Statut": [statut], "Valeur": [valeur]})],
                            ignore_index=True)

                if graph_type_comp == "Stacked Bar":
                    fig = px.bar(df_melted, x="Milieu", y="Valeur", color="Statut", barmode="stack",
                                 color_discrete_sequence=custom_palette)

                elif graph_type_comp == "Line Area":
                    fig = px.area(df_melted, x="Milieu", y="Valeur", color="Statut",
                                  color_discrete_sequence=custom_palette)

                elif graph_type_comp == "Strip":
                    fig = px.strip(df_melted, x="Milieu", y="Valeur", color="Statut",
                                   color_discrete_sequence=custom_palette)

                elif graph_type_comp == "Density Heatmap":
                    fig = px.density_heatmap(df_melted, x="Milieu", y="Statut", z="Valeur",
                                             color_continuous_scale="Viridis", text_auto=True)

                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("⚠ Veuillez sélectionner au moins un milieu et un statut !")









elif st.session_state.page == "Habitat":
    st.markdown("<br>", unsafe_allow_html=True)

    st.set_page_config(layout="wide")

    st.markdown("""
        <style>
        .block-container {
            padding: 0;
            margin: 0;
            max-width: 100%;
        }

        .full-width-bar {
            width: 100%;
            background-color: #1E293B;
            padding: 15px 20px;  /* réduit les paddings */
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-sizing: border-box;
        }

        .bar-logo {
            font-family: 'Playfair Display', serif;
            color: white;
            font-size: 24px;   /* légèrement réduit */
            font-weight: 900;
        }

        .bar-menu {
            display: flex;
            gap: 10px;           /* réduit l’espace entre liens */
            max-width: 70%;       /* limite la largeur du menu pour éviter le dépassement */
            overflow-x: auto;     /* permet le défilement si écran trop petit */
        }

        .bar-menu a {
            color: white;
            text-decoration: none;
            font-size: 14px;      /* réduit la taille du texte */
            font-weight: 600;
            white-space: nowrap;  /* empêche le texte de passer à la ligne */
        }

        .bar-menu a:hover {
            color: #60A5FA;
        }

        .bar-menu .button {
            background-color: #3b82f6;
            padding: 5px 10px;
            border-radius: 6px;
            font-size: 14px;
            font-weight: 600;
        }

        .bar-menu .button:hover {
            background-color: #2563eb;
        }
        </style>

        <div class="full-width-bar">
            <div class="bar-logo">Axiora Data</div>
            <div class="bar-menu">
                <a href="#">App Marketing Agency</a>
                <a href="#">ASO Agency</a>
                <a href="#">Glossary</a>
                <a href="#">Data</a>
                <a href="#">ASO Tools</a>
                <a href="#" class="button">Read Blog</a>
            </div>
        </div>

        <div style="height: 60px;"></div>
        """, unsafe_allow_html=True)
    col11, col22, col33 = st.columns([0.1, 1, 0.1])
    with col22:

        # ================== STYLE ==================
        st.markdown("""
        <style>
        div.stMultiSelect > div:first-child, div.stSelectbox > div:first-child {
            background-color: #e8f0f5;
            border-radius: 6px;
            height: 30px;
            font-size: 14px;
        }
        div.stMultiSelect div.css-1cpxqw2, div.stSelectbox div.css-1cpxqw2 {
            color: #4E79A7;
            font-weight: bold;
        }
        </style>
        """, unsafe_allow_html=True)

        # ================== PALETTE ==================
        custom_palette = ["#7DA186", "#D6A19B", "#D6C189", "#9EB6C1", "#B68DA3", "#B8B198"]

        # ================== TITRE ==================
        st.markdown("<h4 style='color: #85919e;'>1-Opérations achevées par province</h4>", unsafe_allow_html=True)

        # ================== DONNÉES ==================
        data_ops = {
            "Province": ["Agadir Ida Outanane", "Inezgane Ait Melloul", "Chtouka Ait Baha",
                         "Taroudant", "Tiznit", "Tata", "Total"],
            "Nbre d'unités": [9439, 1063, 295, 261, 4279, None, 15337],
            "Superficie (En Ha)": [283, 35, 427, 1, 986, None, 1732],
            "Lotissements": [589, 100, 0, 0, 0, None, 689],
            "Logements": [0, 0, 0, 0, 0, None, 0],
            "Restructuration": [7063, 0, 295, 0, 4213, None, 11571],
            "قطع أرضية Lots de terrain": [21, 737, 0, 0, 0, None, 758],
            "Logements_2": [1693, 216, 0, 261, 62, None, 2232],
            "Activités et Zones Industrielles": [73, 10, 0, 0, 4, None, 87],
            "Cout en Millions de DH": [588, 285, 2, 36, 60, None, 971]
        }

        df_ops = pd.DataFrame(data_ops)

        # ================== Sélection multiselect compacte ==================
        col1, col2, col3 = st.columns([1, 5, 1])

        with col1:
            province_select = st.multiselect("Choisir provinces", df_ops["Province"].dropna().tolist(),
                                             default=df_ops["Province"].dropna().tolist(), key="province_ops")
            colonnes_select = st.multiselect("Choisir colonnes", df_ops.columns[1:].tolist(),
                                             default=df_ops.columns[1:].tolist(), key="colonnes_ops")
            graph_type = st.selectbox("Type de graphique", ["Barres", "Pie", "Treemap", "Funnel"], index=0,
                                      key="graph_ops")

        with col2:
            st.markdown("<br><br>", unsafe_allow_html=True)
            if province_select and colonnes_select:
                df_plot = pd.DataFrame({"Catégorie": [], "Valeur": []})
                for prov in province_select:
                    for col in colonnes_select:
                        val = df_ops[df_ops["Province"] == prov][col].values[0]
                        if isinstance(val, (int, float)):
                            df_plot = pd.concat(
                                [df_plot, pd.DataFrame({"Catégorie": [f"{prov}-{col}"], "Valeur": [val]})],
                                ignore_index=True)

                if graph_type == "Barres":
                    fig = px.bar(df_plot, x="Catégorie", y="Valeur", color="Catégorie",
                                 text="Valeur", color_discrete_sequence=custom_palette)
                    fig.update_traces(textposition="outside")
                elif graph_type == "Pie":
                    fig = px.pie(df_plot, names="Catégorie", values="Valeur", color="Catégorie",
                                 color_discrete_sequence=custom_palette)
                elif graph_type == "Treemap":
                    fig = px.treemap(df_plot, path=["Catégorie"], values="Valeur", color="Catégorie",
                                     color_discrete_sequence=custom_palette)
                elif graph_type == "Funnel":
                    fig = px.funnel(df_plot, x="Valeur", y="Catégorie", color="Catégorie",
                                    color_discrete_sequence=custom_palette)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("⚠ Veuillez sélectionner au moins une province et une colonne !")

        with col3:
            st.markdown("<br><br><br><br>", unsafe_allow_html=True)
            st.dataframe(df_ops, use_container_width=True)
        st.markdown("<br>", unsafe_allow_html=True)
        # ================== Deuxième partie : Comparaison multi-provinces ==================

        # ================== STYLE ==================
        st.markdown("""
        <style>
        div.stMultiSelect > div:first-child, div.stSelectbox > div:first-child {
            background-color: #e8f0f5;
            border-radius: 6px;
            height: 30px;
            font-size: 14px;
        }
        div.stMultiSelect div.css-1cpxqw2, div.stSelectbox div.css-1cpxqw2 {
            color: #4E79A7;
            font-weight: bold;
        }
        </style>
        """, unsafe_allow_html=True)

        # ================== PALETTE ==================
        custom_palette = ["#7DA186", "#D6A19B", "#D6C189", "#9EB6C1", "#B68DA3", "#B8B198"]

        # ================== TITRE ==================
        st.markdown("<h4 style='color: #85919e;'>2-Opérations en cours de lancement par province</h4>",
                    unsafe_allow_html=True)

        # ================== DONNÉES ==================
        data_ops_lancement = {
            "Province": ["Agadir Ida Outanane", "Inezgane Ait Melloul", "Chtouka Ait Baha", "Total"],
            "Nbre d'unités": [9817, 583, 2469, 12869],
            "Superficie (En Ha)": [334, 2, 383, 719],
            "Lotissements": [0, 0, 0, 0],
            "Logements": [0, 0, 0, 0],
            "Restructuration": [7395, 0, 2469, 9864],
            "قطع أرضية Lots de terrain": [0, 0, 0, 0],
            "Logements_2": [679, 533, 0, 1212],
            "Activités et Zones Industrielles": [1743, 50, 0, 1793],
            "Cout en Millions de DH": [385, 104, 25, 514]
        }

        df_ops_lancement = pd.DataFrame(data_ops_lancement)

        # ================== Sélection multiselect compacte ==================
        col1, col2, col3 = st.columns([1, 4, 1])

        with col1:
            province_select = st.multiselect("Choisir provinces", df_ops_lancement["Province"].dropna().tolist(),
                                             default=df_ops_lancement["Province"].dropna().tolist(),
                                             key="province_lancement")
            colonnes_select = st.multiselect("Choisir colonnes", df_ops_lancement.columns[1:].tolist(),
                                             default=df_ops_lancement.columns[1:].tolist(), key="colonnes_lancement")
            graph_type = st.selectbox("Type de graphique", ["Barres", "Pie", "Treemap", "Funnel"], index=3,
                                      key="graph_lancement")

        with col2:
            if province_select and colonnes_select:
                df_plot = pd.DataFrame({"Catégorie": [], "Valeur": []})
                for prov in province_select:
                    for col in colonnes_select:
                        val = df_ops_lancement[df_ops_lancement["Province"] == prov][col].values[0]
                        # Vérification que la valeur est numérique
                        if val is not None and str(val).replace('.', '', 1).isdigit():
                            df_plot = pd.concat(
                                [df_plot, pd.DataFrame({"Catégorie": [f"{prov}-{col}"], "Valeur": [float(val)]})],
                                ignore_index=True)

                if df_plot.empty:
                    st.warning("⚠ Aucune donnée valide à afficher pour la sélection actuelle.")
                else:
                    if graph_type == "Barres":
                        fig = px.bar(df_plot, x="Catégorie", y="Valeur", color="Catégorie",
                                     text="Valeur", color_discrete_sequence=custom_palette)
                        fig.update_traces(textposition="outside")
                    elif graph_type == "Pie":
                        fig = px.pie(df_plot, names="Catégorie", values="Valeur", color="Catégorie",
                                     color_discrete_sequence=custom_palette)
                    elif graph_type == "Treemap":
                        fig = px.treemap(df_plot, path=["Catégorie"], values="Valeur", color="Catégorie",
                                         color_discrete_sequence=custom_palette)
                    elif graph_type == "Funnel":
                        fig = px.funnel(df_plot, x="Valeur", y="Catégorie", color="Catégorie",
                                        color_discrete_sequence=custom_palette)
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("⚠ Veuillez sélectionner au moins une province et une colonne !")

        with col3:
            st.markdown("<br><br><br><br><br>", unsafe_allow_html=True)

            st.dataframe(df_ops_lancement, use_container_width=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ================== Deuxième partie : Comparaison multi-provinces ==================

        # ================== STYLE ==================

        ###################3333 taaaaaab 3

        st.markdown("""
                               <style>
                               div.stMultiSelect > div:first-child, div.stSelectbox > div:first-child {
                                   background-color: #e8f0f5;
                                   border-radius: 6px;
                                   height: 30px;
                                   font-size: 14px;
                               }
                               div.stMultiSelect div.css-1cpxqw2, div.stSelectbox div.css-1cpxqw2 {
                                   color: #4E79A7;
                                   font-weight: bold;
                               }
                               </style>
                               """, unsafe_allow_html=True)

        # ================== PALETTE ==================
        custom_palette = ["#7DA186", "#D6A19B", "#D6C189", "#9EB6C1", "#B68DA3", "#B8B198"]

        # ================== TITRE ==================
        st.markdown("<h4 style='color: #85919e;'>3-Opérations en cours d'exécution par province</h4>",
                    unsafe_allow_html=True)
        # Palette personnalisée pastel un peu plus sombre
        custom_palette = ["#5B5EA6", "#9E7B4C", "#B7415E", "#6B8E23", "#C49BBB", "#88B0AC"]

        # --- Données d'exemple pour opérations en cours d'exécution ---
        # Remplace df_ops_execution par ton vrai DataFrame
        df_ops_execution = pd.DataFrame({
            "Province": ["Agadir Ida Outanane", "Inezgane Ait Melloul", "Chtouka Ait Baha", "Taroudant", "Tiznit",
                         "Tata"],
            "Nbre d'unités": [6662, 3283, 5841, 2050, 797, None],
            "Superficie (En Ha)": [60, 42, 330, 143, 64, None],
            "Lotissements": [985, 744, 24, 0, 0, None],
            "Logements": [0, 0, 210, 0, 0, None],
            "Restructuration": [500, 0, 150, 0, 672, None],
            "قطع أرضية Lots de terrain": [25, 994, 4800, 850, 0, None],
            "Logements 2": [4416, 1228, 100, 96, 111, None],
            "Activités et Zones Industrielles": [736, 317, 557, 1104, 14, None],
            "Cout en Millions de DH": [2121, 517, 973, 475, 38, None]
        })

        # ================== Visualisation individuelle ==================
        col1, col2, col3 = st.columns([1, 3, 1])

        with col1:
            province_select = st.multiselect(
                "Choisir provinces", df_ops_execution["Province"].dropna().tolist(),
                default=df_ops_execution["Province"].dropna().tolist(), key="province_execution"
            )
            colonnes_select = st.multiselect(
                "Choisir colonnes",
                df_ops_execution.columns[1:].tolist(),
                default=df_ops_execution.columns[1:].tolist(),
                key="colonnes_execution"
            )

            graph_type = st.selectbox(
                "Type de graphique", ["Sunburst", "Funnel Area", "Polar (Radar)", "Barres empilées"],
                index=2, key="graph_execution"
            )

        with col2:
            st.markdown("<br><br>", unsafe_allow_html=True)
            if province_select and colonnes_select:
                df_plot = pd.DataFrame({"Catégorie": [], "Valeur": []})
                for prov in province_select:
                    for col in colonnes_select:
                        val = df_ops_execution[df_ops_execution["Province"] == prov][col].values[0]
                        if val is not None and str(val).replace('.', '', 1).isdigit():
                            df_plot = pd.concat(
                                [df_plot, pd.DataFrame({"Catégorie": [f"{prov}-{col}"], "Valeur": [float(val)]})],
                                ignore_index=True
                            )
                if not df_plot.empty:
                    if graph_type == "Sunburst":
                        fig = px.sunburst(df_plot, path=["Catégorie"], values="Valeur", color="Catégorie",
                                          color_discrete_sequence=custom_palette)
                    elif graph_type == "Funnel Area":
                        fig = px.funnel_area(df_plot, names="Catégorie", values="Valeur", color="Catégorie",
                                             color_discrete_sequence=custom_palette)
                    elif graph_type == "Polar (Radar)":
                        fig = px.line_polar(df_plot, r="Valeur", theta="Catégorie", line_close=True, markers=True,
                                            color="Catégorie", color_discrete_sequence=custom_palette)
                    elif graph_type == "Barres empilées":
                        fig = px.bar(df_plot, x="Catégorie", y="Valeur", color="Catégorie", text="Valeur",
                                     color_discrete_sequence=custom_palette)
                        fig.update_traces(textposition="outside")
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("⚠ Aucune donnée valide à afficher.")
            else:
                st.warning("⚠ Sélectionner au moins une province et une colonne !")

        with col3:
            st.markdown("<br><br><br><br>", unsafe_allow_html=True)
            st.dataframe(df_ops_execution, use_container_width=True)

        # ================== Comparaison multi-provinces ==================
        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("""
        <style>
        div.stMultiSelect > div:first-child, div.stSelectbox > div:first-child {
            background-color: #e8f0f5;
            border-radius: 6px;
            height: 30px;
            font-size: 14px;
        }
        div.stMultiSelect div.css-1cpxqw2, div.stSelectbox div.css-1cpxqw2 {
            color: #4E79A7;
            font-weight: bold;
        }
        </style>
        """, unsafe_allow_html=True)

        # ================== PALETTE ==================
        custom_palette = ["#7DA186", "#D6A19B", "#D6C189", "#9EB6C1", "#B68DA3", "#B8B198"]

        # ================== TITRE ==================
        st.markdown("<h4 style='color: #85919e;'>4-Opérations en cours d'étude par province</h4>",
                    unsafe_allow_html=True)

        # ================== DONNÉES ==================
        data_ops_etude = {
            "Province": ["Agadir Ida Outanane", "Inezgane Ait Melloul", "Chtouka Ait Baha",
                         "Taroudant", "Tiznit", "Tata", "Total"],
            "Nbre d'unités": [29568, 722, 457, 400, 300, None, 31447],
            "Superficie (En Ha)": [1019, 3, 4, 6, 1, None, 1033],
            "Lotissements": [0, 0, 0, 0, 0, None, 0],
            "Logements": [0, 0, 0, 0, 0, None, 400],
            "Restructuration": [0, 0, 0, 400, 0, None, 0],
            "قطع أرضية Lots de terrain": [25204, 0, 117, 0, 300, None, 25321],
            "Logements_2": [4364, 500, 340, 0, 0, None, 5504],
            "Activités et Zones Industrielles": [0, 222, 0, 0, 0, None, 222],
            "Cout en Millions de DH": [5815, 110, 77, 40, 55, None, 6097]
        }

        df_ops_etude = pd.DataFrame(data_ops_etude)

        # ================== PREMIÈRE LIGNE : Sélection et graphique ==================
        col1a, col2a, col3a = st.columns([1, 3, 1])

        with col1a:
            st.markdown("<br><br>", unsafe_allow_html=True)
            province_select = st.multiselect("Choisir provinces", df_ops_etude["Province"].dropna().tolist(),
                                             default=df_ops_etude["Province"].dropna().tolist(), key="province_etude")
            colonnes_select = st.multiselect("Choisir colonnes", df_ops_etude.columns[1:].tolist(),
                                             default=df_ops_etude.columns[1:].tolist(), key="colonnes_etude")
            graph_type = st.selectbox("Type de graphique",
                                      ["Sunburst", "Funnel Area", "Polar (Radar)", "Barres empilées"], index=1,
                                      key="graph_etude")

        with col2a:
            st.markdown("<br><br><br>", unsafe_allow_html=True)
            if province_select and colonnes_select:
                df_plot = pd.DataFrame({"Catégorie": [], "Valeur": []})
                for prov in province_select:
                    for col in colonnes_select:
                        val = df_ops_etude[df_ops_etude["Province"] == prov][col].values[0]
                        if val is not None and str(val).replace('.', '', 1).isdigit():
                            df_plot = pd.concat(
                                [df_plot, pd.DataFrame({"Catégorie": [f"{prov}-{col}"], "Valeur": [float(val)]})],
                                ignore_index=True)

                if df_plot.empty:
                    st.warning("⚠ Aucune donnée valide à afficher pour la sélection actuelle.")
                else:
                    if graph_type == "Sunburst":
                        fig = px.sunburst(df_plot, path=["Catégorie"], values="Valeur", color="Catégorie",
                                          color_discrete_sequence=custom_palette)
                    elif graph_type == "Funnel Area":
                        fig = px.funnel_area(df_plot, names="Catégorie", values="Valeur", color="Catégorie",
                                             color_discrete_sequence=custom_palette)
                    elif graph_type == "Polar (Radar)":
                        fig = px.line_polar(df_plot, r="Valeur", theta="Catégorie", line_close=True, markers=True,
                                            color="Catégorie", color_discrete_sequence=custom_palette)
                    elif graph_type == "Barres empilées":
                        fig = px.bar(df_plot, x="Catégorie", y="Valeur", color="Catégorie", text="Valeur",
                                     color_discrete_sequence=custom_palette)
                        fig.update_traces(textposition="outside")
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("⚠ Veuillez sélectionner au moins une province et une colonne !")

        with col3a:
            st.markdown("<br><br><br><br><br>", unsafe_allow_html=True)
            st.dataframe(df_ops_etude, use_container_width=True)

        st.markdown("<br>", unsafe_allow_html=True)
        import streamlit as st
        import pandas as pd
        import geopandas as gpd
        import plotly.express as px

        # --- CONFIGURATION DE LA PAGE ---
        st.set_page_config(page_title="Axioradata - Dashboard Habitat", layout="wide")

        # --- STYLE CSS (Pour la bannière des KPIs) ---
        st.markdown("""
        <style>
            .kpi-banner {
                background-color: #2b2b45;
                padding: 1.5rem;
                border-radius: 0.5rem;
                display: flex;
                justify-content: space-around;
                align-items: center;
                flex-wrap: wrap;
                margin-bottom: 2rem;
            }
            .kpi-box {
                text-align: center;
                flex-grow: 1;
                padding: 1rem;
            }
            .kpi-label {
                font-size: 0.9em;
                color: #ffffff;
                opacity: 0.8;
                display: block;
                margin-bottom: 0.25rem;
            }
            .kpi-value {
                font-size: 2em;
                font-weight: bold;
                color: #ffffff;
                display: block;
            }
            .kpi-subvalue {
                font-size: 0.8em;
                color: #ffffff;
                opacity: 0.9;
            }
        </style>
        """, unsafe_allow_html=True)

        # --- DONNÉES HABITAT ---
        habitat_data = {
            "Opérations achevées": {
                "Province": ["Agadir Ida Outanane", "Inezgane Ait Melloul", "Chtouka Ait Baha", "Taroudant", "Tiznit",
                             "Tata",
                             "Total"],
                "Nbre d'unités": [9439, 1063, 295, 261, 4279, None, 15337],
                "Superficie (En Ha)": [283, 35, 427, 1, 986, None, 1732],
                "Lotissements": [589, 100, 0, 0, 0, None, 689],
                "Logements": [0, 0, 0, 0, 0, None, 0],
                "Restructuration": [7063, 0, 295, 0, 4213, None, 11571],
                "Lots de terrain": [21, 737, 0, 0, 0, None, 758],
                "Logements_2": [1693, 216, 0, 261, 62, None, 2232],
                "Activités et Zones Industrielles": [73, 10, 0, 0, 4, None, 87],
                "Cout en Millions de DH": [588, 285, 2, 36, 60, None, 971]
            },
            "Opérations en lancement": {
                "Province": ["Agadir Ida Outanane", "Inezgane Ait Melloul", "Chtouka Ait Baha", "Total"],
                "Nbre d'unités": [9817, 583, 2469, 12869],
                "Superficie (En Ha)": [334, 2, 383, 719],
                "Lotissements": [0, 0, 0, 0],
                "Logements": [0, 0, 0, 0],
                "Restructuration": [7395, 0, 2469, 9864],
                "Lots de terrain": [0, 0, 0, 0],
                "Logements_2": [679, 533, 0, 1212],
                "Activités et Zones Industrielles": [1743, 50, 0, 1793],
                "Cout en Millions de DH": [385, 104, 25, 514]
            },
            "Opérations en exécution": {
                "Province": ["Agadir Ida Outanane", "Inezgane Ait Melloul", "Chtouka Ait Baha", "Taroudant", "Tiznit",
                             "Tata"],
                "Nbre d'unités": [6662, 3283, 5841, 2050, 797, None],
                "Superficie (En Ha)": [60, 42, 330, 143, 64, None],
                "Lotissements": [985, 744, 24, 0, 0, None],
                "Logements": [0, 0, 210, 0, 0, None],
                "Restructuration": [500, 0, 150, 0, 672, None],
                "Lots de terrain": [25, 994, 4800, 850, 0, None],
                "Logements_2": [4416, 1228, 100, 96, 111, None],
                "Activités et Zones Industrielles": [736, 317, 557, 1104, 14, None],
                "Cout en Millions de DH": [2121, 517, 973, 475, 38, None]
            },
            "Opérations en étude": {
                "Province": ["Agadir Ida Outanane", "Inezgane Ait Melloul", "Chtouka Ait Baha", "Taroudant", "Tiznit",
                             "Tata",
                             "Total"],
                "Nbre d'unités": [29568, 722, 457, 400, 300, None, 31447],
                "Superficie (En Ha)": [1019, 3, 4, 6, 1, None, 1033],
                "Lotissements": [0, 0, 0, 0, 0, None, 0],
                "Logements": [0, 0, 0, 0, 0, None, 400],
                "Restructuration": [0, 0, 0, 400, 0, None, 0],
                "Lots de terrain": [25204, 0, 117, 0, 300, None, 25321],
                "Logements_2": [4364, 500, 340, 0, 0, None, 5504],
                "Activités et Zones Industrielles": [0, 222, 0, 0, 0, None, 222],
                "Cout en Millions de DH": [5815, 110, 77, 40, 55, None, 6097]
            }
        }


        # --- FONCTIONS ---
        @st.cache_data
        def load_shapefile(path):
            try:
                return gpd.read_file(path)
            except Exception as e:
                st.error(f"Erreur lors du chargement du fichier {path} : {e}")
                return None


        @st.cache_data
        def process_habitat_data(data):
            """Transforme les données d'habitat en un seul DataFrame propre."""
            all_records = []
            for status, status_data in data.items():
                df = pd.DataFrame(status_data)
                df_melted = df.melt(id_vars=["Province"], var_name="Indicateur", value_name="Valeur")
                df_melted["Statut"] = status
                all_records.append(df_melted)

            final_df = pd.concat(all_records, ignore_index=True)
            final_df = final_df[final_df['Province'] != 'Total'].copy()
            final_df['Valeur'] = pd.to_numeric(final_df['Valeur'], errors='coerce')
            final_df.dropna(subset=['Valeur'], inplace=True)
            return final_df


        # --- TITRE ---
        st.markdown(
            "<h3 style='text-align: center; color:#8e8e9e;'>Analyse du Secteur de l'Habitat (Souss-Massa)</h3>",
            unsafe_allow_html=True)
        st.write("")

        # --- CHARGEMENT ET PRÉPARATION DES DONNÉES ---
        df_habitat = process_habitat_data(habitat_data)
        # Utiliser le fichier simplifié si vous l'avez créé, sinon le fichier original
        shapefile_path = "mar_admbnda_adm2_hcp_20230925/mar_admbnda_adm2_hcp_20230925.shp"
        gdf_provinces = load_shapefile(shapefile_path)

        # --- FILTRES ---
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            statut_choisi = st.selectbox("1. Choisissez un statut d'opération :", df_habitat['Statut'].unique())
        with col_f2:
            df_statut = df_habitat[df_habitat['Statut'] == statut_choisi]
            indicateur_choisi = st.selectbox("2. Choisissez un indicateur :", df_statut['Indicateur'].unique())

        df_filtre = df_statut[df_statut['Indicateur'] == indicateur_choisi]

        # --- BANNIÈRE KPI ---
        if not df_filtre.empty:
            total_val = df_filtre['Valeur'].sum()
            min_val = df_filtre['Valeur'].min()
            max_val = df_filtre['Valeur'].max()

            min_province = df_filtre.loc[df_filtre['Valeur'].idxmin()]
            max_province = df_filtre.loc[df_filtre['Valeur'].idxmax()]

            st.markdown(f"""
            <div class="kpi-banner">
                <div class="kpi-box">
                    <span class="kpi-label">Minimum</span>
                    <span class="kpi-value">{min_val:,.0f}</span>
                    <span class="kpi-subvalue">{min_province['Province']}</span>
                </div>
                <div class="kpi-box">
                    <span class="kpi-label">Total Régional</span>
                    <span class="kpi-value">{total_val:,.0f}</span>
                    <span class="kpi-subvalue">{indicateur_choisi}</span>
                </div>
                <div class="kpi-box">
                    <span class="kpi-label">Maximum</span>
                    <span class="kpi-value">{max_val:,.0f}</span>
                    <span class="kpi-subvalue">{max_province['Province']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("Aucune donnée disponible pour cette sélection.")

        # --- CARTE ET GRAPHIQUE ---
        if gdf_provinces is not None and not df_filtre.empty:
            province_name_mapping = {
                'Agadir Ida Outanane': 'Agadir Ida Ou Tanane', 'Chtouka Ait Baha': 'Chtouka- Ait Baha',
                'Inezgane Ait Melloul': 'Inezgane-Ait Melloul', 'Taroudant': 'Taroudannt'
            }
            df_filtre['join_key'] = df_filtre['Province'].replace(province_name_mapping)
            gdf_provinces['join_key'] = gdf_provinces['ADM2_FR']

            gdf_merged = gdf_provinces.merge(df_filtre, on='join_key', how='inner')

            if not gdf_merged.empty:
                col1, col2 = st.columns([3, 2])
                with col1:
                    fig_map = px.choropleth_mapbox(
                        gdf_merged,
                        geojson=gdf_merged.geometry,
                        locations=gdf_merged.index,
                        color="Valeur",
                        hover_name="Province",
                        hover_data={"Valeur": ':,.0f'},
                        mapbox_style="open-street-map",  # <-- MODIFIÉ ICI
                        center={"lat": 30.2, "lon": -9.0},
                        zoom=6.5,
                        opacity=0.75,
                        color_continuous_scale="Plasma"
                    )
                    fig_map.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, height=600)
                    st.plotly_chart(fig_map, use_container_width=True)

                with col2:
                    df_sorted = gdf_merged.sort_values(by="Valeur", ascending=False)
                    fig_bar = px.bar(
                        df_sorted,
                        x="Valeur",
                        y='Province',
                        orientation='h',
                        text_auto=',.0f',
                        color="Valeur",
                        color_continuous_scale="Plasma"
                    )
                    fig_bar.update_layout(
                        yaxis={'categoryorder': 'total ascending'},
                        margin={"r": 0, "t": 30, "l": 0, "b": 0},
                        height=600,
                        showlegend=False,
                        xaxis_title=indicateur_choisi,
                        yaxis_title=""
                    )
                    fig_bar.update_traces(textposition='outside')
                    st.plotly_chart(fig_bar, use_container_width=True)
            else:
                st.warning("Impossible de faire correspondre les données de l'habitat avec les données géographiques.")
        else:
            st.error("Données géographiques non chargées ou aucune donnée à afficher pour les filtres sélectionnés.")

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)




elif st.session_state.page == "Finance":
    st.markdown("<br>", unsafe_allow_html=True)

    st.set_page_config(layout="wide")

    st.markdown("""
        <style>
        .block-container {
            padding: 0;
            margin: 0;
            max-width: 100%;
        }

        .full-width-bar {
            width: 100%;
            background-color: #1E293B;
            padding: 15px 20px;  /* réduit les paddings */
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-sizing: border-box;
        }

        .bar-logo {
            font-family: 'Playfair Display', serif;
            color: white;
            font-size: 24px;   /* légèrement réduit */
            font-weight: 900;
        }

        .bar-menu {
            display: flex;
            gap: 10px;           /* réduit l’espace entre liens */
            max-width: 70%;       /* limite la largeur du menu pour éviter le dépassement */
            overflow-x: auto;     /* permet le défilement si écran trop petit */
        }

        .bar-menu a {
            color: white;
            text-decoration: none;
            font-size: 14px;      /* réduit la taille du texte */
            font-weight: 600;
            white-space: nowrap;  /* empêche le texte de passer à la ligne */
        }

        .bar-menu a:hover {
            color: #60A5FA;
        }

        .bar-menu .button {
            background-color: #3b82f6;
            padding: 5px 10px;
            border-radius: 6px;
            font-size: 14px;
            font-weight: 600;
        }

        .bar-menu .button:hover {
            background-color: #2563eb;
        }
        </style>

        <div class="full-width-bar">
            <div class="bar-logo">Axiora Data</div>
            <div class="bar-menu">
                <a href="#">App Marketing Agency</a>
                <a href="#">ASO Agency</a>
                <a href="#">Glossary</a>
                <a href="#">Data</a>
                <a href="#">ASO Tools</a>
                <a href="#" class="button">Read Blog</a>
            </div>
        </div>

        <div style="height: 60px;"></div>
        """, unsafe_allow_html=True)

    col11, col22, col33 = st.columns([0.1, 1, 0.1])
    with col22:

        # ================== STYLE ==================
        st.markdown("""
        <style>
        div.stMultiSelect > div:first-child, div.stSelectbox > div:first-child {
            background-color: #e8f0f5;
            border-radius: 6px;
            height: 30px;
            font-size: 14px;
        }
        div.stMultiSelect div.css-1cpxqw2, div.stSelectbox div.css-1cpxqw2 {
            color: #4E79A7;
            font-weight: bold;
        }
        </style>
        """, unsafe_allow_html=True)

        # ================== DONNÉES ==================
        data_banques = {
            "Province": ["Agadir Ida Outanane", "Inezgane Ait Melloul", "Chtouka Ait Baha",
                         "Taroudant", "Tiznit", "Tata"],
            "Montant des dépôts (en milliers)": [25599795, 9560580, 2488070, 5962524, 5697437, 254432],
            "Montant des crédits (en milliers)": [20526240, 3666514, 482351, 3747507, 1140457, 134904
                                                  ]
        }

        df_banques = pd.DataFrame(data_banques)

        # ================== PALETTE ==================

        st.markdown("<h4 style='color: #607080;'>1-Dépôts et crédits des différentes banques par province</h4>",
                    unsafe_allow_html=True)
        # ================== INTERFACE ==================
        # Palette pastel bleu et violet
        custom_palette = ["#a3c4f3", "#c9b3f3"]

        col1a, col2a, col3a = st.columns([1, 3, 1])

        with col1a:
            st.markdown("<br><br>", unsafe_allow_html=True)
            province_select = st.multiselect(
                "Choisir provinces",
                df_banques["Province"].tolist(),
                default=df_banques["Province"].tolist(),
                key="province_banques"
            )
            colonnes_select = st.multiselect(
                "Choisir colonnes",
                df_banques.columns[1:].tolist(),
                default=df_banques.columns[1:].tolist(),
                key="colonnes_banques"
            )
            graph_type = st.selectbox(
                "Type de graphique",
                ["Barres empilées", "Bar Groupé", "Treemap", "Pie Chart", "Sunburst", "Polar (Radar)"],
                index=1,
                key="graph_banques"
            )

        with col2a:
            st.markdown("<br><br><br>", unsafe_allow_html=True)
            if province_select and colonnes_select:
                df_plot = df_banques[df_banques["Province"].isin(province_select)][["Province"] + colonnes_select]
                df_long = df_plot.melt(id_vars="Province", var_name="Colonne", value_name="Valeur")
                df_long = df_long[pd.to_numeric(df_long["Valeur"], errors='coerce').notnull()]
                df_long["Valeur"] = df_long["Valeur"].astype(float)

                if df_long.empty:
                    st.warning("⚠ Aucune donnée valide à afficher pour la sélection actuelle.")
                else:
                    if graph_type == "Sunburst":
                        fig = px.sunburst(df_long, path=["Province", "Colonne"], values="Valeur",
                                          color="Colonne", color_discrete_sequence=custom_palette)
                        fig.update_traces(textinfo="none")
                    elif graph_type == "Treemap":
                        fig = px.treemap(df_long, path=["Province", "Colonne"], values="Valeur",
                                         color="Colonne", color_discrete_sequence=custom_palette)
                        fig.update_traces(textinfo="none")
                    elif graph_type == "Pie Chart":
                        fig = px.pie(df_long, names="Colonne", values="Valeur",
                                     color="Colonne", color_discrete_sequence=custom_palette)
                        fig.update_traces(textinfo="none")
                    elif graph_type == "Polar (Radar)":
                        fig = px.line_polar(df_long, r="Valeur", theta="Colonne", line_close=True, markers=True,
                                            color="Colonne", color_discrete_sequence=custom_palette)
                    elif graph_type == "Barres empilées":
                        fig = px.bar(df_long, x="Province", y="Valeur", color="Colonne",
                                     barmode="stack", color_discrete_sequence=custom_palette)
                    elif graph_type == "Bar Groupé":
                        fig = px.bar(df_long, x="Province", y="Valeur", color="Colonne",
                                     barmode="group", color_discrete_sequence=custom_palette)

                    fig.update_layout(
                        font=dict(family="Arial", size=12, color="#000000"),
                        height=400,
                        width=1000,
                        showlegend=True,
                        xaxis_title=None,
                        yaxis_title=None,
                        xaxis=dict(showticklabels=True),
                        yaxis=dict(showticklabels=True),
                        margin=dict(l=20, r=20, t=20, b=20)
                    )

                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("⚠ Veuillez sélectionner au moins une province et une colonne !")

        with col3a:
            st.markdown("<br><br><br><br><br>", unsafe_allow_html=True)
            st.dataframe(df_banques, use_container_width=True)

        #############tab 2

        # ================== DONNÉES ==================
        data_projets = {
            "Provinces": [
                "Agadir Ida Outanane", "Inezgane Ait Melloul", "Chtouka Ait Baha",
                "Taroudant", "Tiznit", "Tata", "Total"
            ],
            "Emplois à créer": [9083, 384, 1023, 896, 896, 512, 12793],
            "Montant d'investissement (millions de DH)": [11113, 780, 4641, 579, 590, 256, 17960],
            "Nombre de projets": [134, 23, 6, 17, 15, 17, 213]
        }

        df_projets = pd.DataFrame(data_projets)

        # ================== PALETTE PASTEL ==================
        custom_palette_pastel = ["#7f7e91", "#7f917e", "#556967"]  # pastel bleu, violet et vert doux

        # ================== INTERFACE ==================
        st.markdown("<h4 style='color: #607080;'>2-Répartition des projets d'investissement 2017</h4>",
                    unsafe_allow_html=True)

        col1b, col2b, col3b = st.columns([1, 1, 3])

        with col1b:
            st.markdown("<br><br>", unsafe_allow_html=True)
            province_select_proj = st.multiselect(
                "Choisir provinces",
                df_projets["Provinces"].tolist(),
                default=df_projets["Provinces"].tolist(),
                key="province_projets"
            )
            colonnes_select_proj = st.multiselect(
                "Choisir colonnes",
                df_projets.columns[1:].tolist(),
                default=df_projets.columns[1:].tolist(),
                key="colonnes_projets"
            )
            graph_type_proj = st.selectbox(
                "Type de graphique",
                ["Barres empilées", "Bar Groupé", "Treemap", "Pie Chart", "Sunburst", "Polar (Radar)", "Line Chart",
                 "Area Chart"],
                index=7,
                key="graph_projets"
            )

        with col3b:
            st.markdown("<br><br><br>", unsafe_allow_html=True)
            if province_select_proj and colonnes_select_proj:
                # Filtrer selon la sélection
                df_plot_proj = df_projets[df_projets["Provinces"].isin(province_select_proj)][
                    ["Provinces"] + colonnes_select_proj]

                # Transformation en format long pour Plotly
                df_long_proj = df_plot_proj.melt(id_vars="Provinces", var_name="Colonne", value_name="Valeur")
                df_long_proj = df_long_proj[pd.to_numeric(df_long_proj["Valeur"], errors='coerce').notnull()]
                df_long_proj["Valeur"] = df_long_proj["Valeur"].astype(float)

                if df_long_proj.empty:
                    st.warning("⚠ Aucune donnée valide à afficher pour la sélection actuelle.")
                else:
                    if graph_type_proj == "Sunburst":
                        fig = px.sunburst(df_long_proj, path=["Provinces", "Colonne"], values="Valeur",
                                          color="Colonne", color_discrete_sequence=custom_palette_pastel)
                        fig.update_traces(textinfo="none")
                    elif graph_type_proj == "Treemap":
                        fig = px.treemap(df_long_proj, path=["Provinces", "Colonne"], values="Valeur",
                                         color="Colonne", color_discrete_sequence=custom_palette_pastel)
                        fig.update_traces(textinfo="none")
                    elif graph_type_proj == "Pie Chart":
                        fig = px.pie(df_long_proj, names="Colonne", values="Valeur",
                                     color="Colonne", color_discrete_sequence=custom_palette_pastel)
                        fig.update_traces(textinfo="none")
                    elif graph_type_proj == "Polar (Radar)":
                        fig = px.line_polar(df_long_proj, r="Valeur", theta="Colonne", line_close=True, markers=True,
                                            color="Colonne", color_discrete_sequence=custom_palette_pastel)
                    elif graph_type_proj == "Barres empilées":
                        fig = px.bar(df_long_proj, x="Provinces", y="Valeur", color="Colonne",
                                     barmode="stack", color_discrete_sequence=custom_palette_pastel)
                    elif graph_type_proj == "Bar Groupé":
                        fig = px.bar(df_long_proj, x="Provinces", y="Valeur", color="Colonne",
                                     barmode="group", color_discrete_sequence=custom_palette_pastel)
                    elif graph_type_proj == "Line Chart":
                        fig = px.line(df_long_proj, x="Provinces", y="Valeur", color="Colonne",
                                      markers=True, color_discrete_sequence=custom_palette_pastel)
                    elif graph_type_proj == "Area Chart":
                        fig = px.area(df_long_proj, x="Provinces", y="Valeur", color="Colonne",
                                      color_discrete_sequence=custom_palette_pastel)

                    fig.update_layout(
                        font=dict(family="Arial", size=12, color="#000000"),
                        height=400,
                        width=1000,
                        showlegend=True,
                        xaxis_title=None,
                        yaxis_title=None,
                        xaxis=dict(showticklabels=True),
                        yaxis=dict(showticklabels=True),
                        margin=dict(l=20, r=20, t=20, b=20)
                    )

                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("⚠ Veuillez sélectionner au moins une province et une colonne !")

        with col2b:
            st.markdown("<br><br><br><br><br>", unsafe_allow_html=True)
            st.dataframe(df_projets, use_container_width=True)

            ########## taaaaaaaab 3
        data_sectoriel = {
            "Secteur d’Activité": ["Tourisme", "Services", "Commerce", "BTP", "Mines", "Industrie", "Artisanat"],
            "Investissement (millions de DH)": [6714, 5285, 519, 4561, 167, 711, 4],
            "Emplois à créer": [4941, 3082, 230, 1361, 104, 949, 2]
        }

        df_sectoriel = pd.DataFrame(data_sectoriel)

        # ================== PALETTE PASTEL ==================
        custom_palette_sectoriel = ["#556967", "#556957", "#8c997d", "#31314d", "#d4cb87", "#96726c", "#f3b3c9"]
        st.markdown("<br><br>", unsafe_allow_html=True)

        # ================== INTERFACE ==================
        st.markdown("<h4 style='color: #607080;'>3-Ventilation sectorielle des projets d’investissement</h4>",
                    unsafe_allow_html=True)

        col1s, col2s, col3s = st.columns([1, 3, 1])

        with col1s:
            st.markdown("<br><br>", unsafe_allow_html=True)
            indicateurs_select = st.multiselect(
                "Choisir les indicateurs à afficher",
                df_sectoriel.columns[1:].tolist(),
                default=df_sectoriel.columns[1:].tolist(),
                key="indicateurs_sectoriel"
            )
            st.markdown("<h6>Sélectionner les secteurs à afficher :</h6>", unsafe_allow_html=True)
            # --- Checkboxes pour chaque secteur ---
            secteurs_select = []
            for secteur in df_sectoriel["Secteur d’Activité"]:
                if st.checkbox(secteur, True, key=f"secteur_{secteur}"):
                    secteurs_select.append(secteur)

            graph_type_sectoriel = st.selectbox(
                "Type de graphique",
                ["Barres groupées", "Barres empilées", "Courbes multiples", "Scatter multi-dimension", "Pie Chart",
                 "Treemap"],
                index=5,
                key="graph_sectoriel"
            )

        with col2s:
            st.markdown("<br><br><br>", unsafe_allow_html=True)
            if not indicateurs_select:
                st.warning("⚠ Veuillez sélectionner au moins un indicateur !")
            else:
                if graph_type_sectoriel == "Barres groupées":
                    fig = px.bar(df_sectoriel, x="Secteur d’Activité", y=indicateurs_select,
                                 barmode="group",
                                 color_discrete_sequence=custom_palette_sectoriel[:len(indicateurs_select)])
                    st.plotly_chart(fig, use_container_width=True)
                elif graph_type_sectoriel == "Barres empilées":
                    fig = px.bar(df_sectoriel, x="Secteur d’Activité", y=indicateurs_select,
                                 barmode="stack",
                                 color_discrete_sequence=custom_palette_sectoriel[:len(indicateurs_select)])
                    st.plotly_chart(fig, use_container_width=True)
                elif graph_type_sectoriel == "Courbes multiples":
                    fig = px.line(df_sectoriel, x="Secteur d’Activité", y=indicateurs_select, markers=True,
                                  color_discrete_sequence=custom_palette_sectoriel[:len(indicateurs_select)])
                    st.plotly_chart(fig, use_container_width=True)
                elif graph_type_sectoriel == "Scatter multi-dimension":
                    x_col = indicateurs_select[0] if len(indicateurs_select) > 0 else indicateurs_select[0]
                    y_col = indicateurs_select[1] if len(indicateurs_select) > 1 else indicateurs_select[0]
                    size_col = indicateurs_select[1] if len(indicateurs_select) > 1 else indicateurs_select[0]
                    color_col = indicateurs_select[0]
                    fig = px.scatter(df_sectoriel, x=x_col, y=y_col, size=size_col, color=color_col,
                                     text="Secteur d’Activité",
                                     color_discrete_sequence=custom_palette_sectoriel)
                    fig.update_traces(textposition="top center")
                    st.plotly_chart(fig, use_container_width=True)
                elif graph_type_sectoriel == "Pie Chart":
                    if len(indicateurs_select) > 0:
                        fig = px.pie(df_sectoriel, names="Secteur d’Activité", values=indicateurs_select[0],
                                     color_discrete_sequence=custom_palette_sectoriel)
                        st.plotly_chart(fig, use_container_width=True)
                elif graph_type_sectoriel == "Treemap":
                    if len(indicateurs_select) > 0:
                        fig = px.treemap(df_sectoriel, path=["Secteur d’Activité"], values=indicateurs_select[0],
                                         color="Secteur d’Activité",
                                         color_discrete_sequence=custom_palette_sectoriel)
                        st.plotly_chart(fig, use_container_width=True)

        with col3s:
            st.markdown("<br><br><br><br><br>", unsafe_allow_html=True)
            st.dataframe(df_sectoriel, use_container_width=True)

        ######################## taaaaaaaaabbbb 4

        data_entreprises = {
            "Année": ["2017", "2016", "2015"],
            "Nombre d’emplois ": [3549, 2718, 1087],
            "Montant d’investissement (Mdhs) ": [360, 323, 4293],
            "Nombre de projets ": [684, 572, 562]
        }

        df_entreprises = pd.DataFrame(data_entreprises)

        # ================== PALETTE PASTEL ==================

        custom_palette_entreprises = ["#556967", "#556957", "#8c997d", "#31314d", "#d4cb87", "#96726c", "#f3b3c9"]

        st.markdown("<br><br>", unsafe_allow_html=True)

        # ================== INTERFACE ==================
        st.markdown("<h4 style='color: #607080;'>4-Évolution des entreprises créées dans la région</h4>",
                    unsafe_allow_html=True)

        col1e, col2e, col3e = st.columns([3, 1, 1])

        with col2e:
            st.markdown("<br><br>", unsafe_allow_html=True)

            # --- Choix des indicateurs ---
            indicateurs_select = st.multiselect(
                "Choisir les indicateurs à afficher",
                df_entreprises.columns[1:].tolist(),
                default=df_entreprises.columns[1:].tolist(),
                key="indicateurs_entreprises"
            )

            # --- Choix du type de graphique ---
            graph_type_entreprises = st.selectbox(
                "Type de graphique",
                ["Barres groupées", "Barres empilées", "Courbes multiples", "Scatter multi-dimension", "Pie Chart",
                 "Treemap"],
                index=2,
                key="graph_entreprises"
            )

        with col1e:

            if not indicateurs_select:
                st.warning("⚠ Veuillez sélectionner au moins un indicateur !")
            else:
                if graph_type_entreprises == "Barres groupées":
                    fig = px.bar(df_entreprises, x="Année", y=indicateurs_select,
                                 barmode="group",
                                 color_discrete_sequence=custom_palette_entreprises[:len(indicateurs_select)])
                    st.plotly_chart(fig, use_container_width=True)

                elif graph_type_entreprises == "Barres empilées":
                    fig = px.bar(df_entreprises, x="Année", y=indicateurs_select,
                                 barmode="stack",
                                 color_discrete_sequence=custom_palette_entreprises[:len(indicateurs_select)])
                    st.plotly_chart(fig, use_container_width=True)

                elif graph_type_entreprises == "Courbes multiples":
                    fig = px.line(df_entreprises, x="Année", y=indicateurs_select, markers=True,
                                  color_discrete_sequence=custom_palette_entreprises[:len(indicateurs_select)])
                    st.plotly_chart(fig, use_container_width=True)

                elif graph_type_entreprises == "Scatter multi-dimension":
                    x_col = indicateurs_select[0]
                    y_col = indicateurs_select[1] if len(indicateurs_select) > 1 else indicateurs_select[0]
                    size_col = indicateurs_select[1] if len(indicateurs_select) > 1 else indicateurs_select[0]
                    color_col = indicateurs_select[0]
                    fig = px.scatter(df_entreprises, x=x_col, y=y_col, size=size_col, color=color_col,
                                     text="Année",
                                     color_discrete_sequence=custom_palette_entreprises)
                    fig.update_traces(textposition="top center")
                    st.plotly_chart(fig, use_container_width=True)

                elif graph_type_entreprises == "Pie Chart":
                    if len(indicateurs_select) > 0:
                        fig = px.pie(df_entreprises, names="Année", values=indicateurs_select[0],
                                     color_discrete_sequence=custom_palette_entreprises)
                        st.plotly_chart(fig, use_container_width=True)

                elif graph_type_entreprises == "Treemap":
                    if len(indicateurs_select) > 0:
                        fig = px.treemap(df_entreprises, path=["Année"], values=indicateurs_select[0],
                                         color="Année",
                                         color_discrete_sequence=custom_palette_entreprises)
                        st.plotly_chart(fig, use_container_width=True)

        with col3e:
            st.markdown("<br><br><br><br><br>", unsafe_allow_html=True)
            st.dataframe(df_entreprises, use_container_width=True)

            ############ taaaaab 5

        data_secteurs = {
            "Secteur d’Activité": [
                "Tourisme", "Services", "Commerce", "BTP",
                "Mines", "Agriculture et pêche", "Industrie"
            ],
            "Nbre d’entreprises créées (%)": [1, 40, 37, 17, 1, 5, 1],
            "Montant d’investissement (%)": [2, 36, 28, 22, 2, 9, 1],

        }
        df_secteurs = pd.DataFrame(data_secteurs)

        # Palette personnalisée
        custom_palette_secteurs = ["#556967", "#556957", "#8c997d", "#31314d", "#d4cb87", "#96726c", "#f3b3c9"]

        # ================== TITRE ==================
        st.markdown(
            "<h4 style='color: #607080;'>5- Répartition des créations d’entreprises par secteur d’activité</h4>",
            unsafe_allow_html=True)

        # ================== LAYOUT ==================
        col1s, col2s, col3s = st.columns([1, 1, 3])

        with col1s:
            st.markdown("<br><br>", unsafe_allow_html=True)

            # --- Checkbox pour les colonnes (indicateurs) ---
            colonnes_disponibles = df_secteurs.columns[1:3].tolist()
            indicateurs_select_secteurs = []
            st.markdown("**Choisir les indicateurs à afficher :**")
            for col in colonnes_disponibles:
                if st.checkbox(col, value=True, key=f"check_{col}"):
                    indicateurs_select_secteurs.append(col)

            # --- Checkbox pour les secteurs (lignes) ---
            secteurs_disponibles = df_secteurs["Secteur d’Activité"].tolist()
            secteurs_selectionnes = []
            st.markdown("**Choisir les secteurs à afficher :**")
            for sec in secteurs_disponibles:
                if st.checkbox(sec, value=True, key=f"check_{sec}"):
                    secteurs_selectionnes.append(sec)

            # --- Filtrage du dataframe en fonction des choix ---
            df_filtered = df_secteurs[df_secteurs["Secteur d’Activité"].isin(secteurs_selectionnes)]

            # --- Choix du type de graphique ---
            graph_type_secteurs = st.selectbox(
                "Type de graphique",
                ["Barres groupées", "Barres empilées", "Courbes multiples", "Scatter multi-dimension", "Pie Chart",
                 "Treemap"],
                index=0,
                key="graph_secteurs"
            )

        with col3s:
            st.markdown("<br><br><br><br>", unsafe_allow_html=True)
            if not indicateurs_select_secteurs:
                st.warning("⚠ Veuillez sélectionner au moins un indicateur !")
            else:
                if graph_type_secteurs == "Barres groupées":
                    fig = px.bar(df_secteurs, x="Secteur d’Activité", y=indicateurs_select_secteurs,
                                 barmode="group",
                                 color_discrete_sequence=custom_palette_secteurs[:len(indicateurs_select_secteurs)])
                    st.plotly_chart(fig, use_container_width=True)

                elif graph_type_secteurs == "Barres empilées":
                    fig = px.bar(df_secteurs, x="Secteur d’Activité", y=indicateurs_select_secteurs,
                                 barmode="stack",
                                 color_discrete_sequence=custom_palette_secteurs[:len(indicateurs_select_secteurs)])
                    st.plotly_chart(fig, use_container_width=True)

                elif graph_type_secteurs == "Courbes multiples":
                    fig = px.line(df_secteurs, x="Secteur d’Activité", y=indicateurs_select_secteurs, markers=True,
                                  color_discrete_sequence=custom_palette_secteurs[:len(indicateurs_select_secteurs)])
                    st.plotly_chart(fig, use_container_width=True)

                elif graph_type_secteurs == "Scatter multi-dimension":
                    x_col = indicateurs_select_secteurs[0]
                    y_col = indicateurs_select_secteurs[1] if len(indicateurs_select_secteurs) > 1 else \
                        indicateurs_select_secteurs[0]
                    fig = px.scatter(df_secteurs, x=x_col, y=y_col, size=y_col, color="Secteur d’Activité",
                                     text="Secteur d’Activité",
                                     color_discrete_sequence=custom_palette_secteurs)
                    fig.update_traces(textposition="top center")
                    st.plotly_chart(fig, use_container_width=True)

                elif graph_type_secteurs == "Pie Chart":
                    if len(indicateurs_select_secteurs) == 1:
                        fig = px.pie(df_secteurs, names="Secteur d’Activité", values=indicateurs_select_secteurs[0],
                                     color_discrete_sequence=custom_palette_secteurs)
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.warning("⚠ Sélectionnez un seul indicateur pour le camembert.")

                elif graph_type_secteurs == "Treemap":
                    if len(indicateurs_select_secteurs) == 1:
                        fig = px.treemap(df_secteurs, path=["Secteur d’Activité"],
                                         values=indicateurs_select_secteurs[0],
                                         color="Secteur d’Activité",
                                         color_discrete_sequence=custom_palette_secteurs)
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.warning("⚠ Sélectionnez un seul indicateur pour la treemap.")

        with col2s:
            st.markdown("<br><br><br><br><br><br>", unsafe_allow_html=True)
            st.dataframe(df_secteurs, use_container_width=True)

            ######## taaaaaaaaaaaaab 6
        # ================== DATA ==================

        # Palette pastel
        custom_palette_pib = ["#556967", "#556957", "#8c997d", "#31314d", "#d4cb87", "#96726c", "#f3b3c9"]

        # ================== DATA ==================
        data_pib = {
            "Secteurs ": ["Primaire ", "Secondaire ", "Tertiaire "],
            "Souss Massa 2015": [12036, 13460, 31522],
            "Souss Massa 2016": [13864, 12832, 33163],
            "Maroc 2015": [124759, 257796, 491424],
            "Maroc 2016": [121556, 263384, 509991]
        }

        df_pib = pd.DataFrame(data_pib)

        # ============ CORRIGER LES NOMS DE COLONNES ============
        df_pib.columns = df_pib.columns.str.strip()  # Supprime les espaces en début/fin
        # df_pib.columns: ['Secteurs', 'Souss Massa 2015', 'Souss Massa 2016', 'Maroc 2015', 'Maroc 2016']
        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("<h4 style='color: #607080;'>6- PIB selon les secteurs d'activité</h4>", unsafe_allow_html=True)

        col1p, col2p, col3p = st.columns([1, 3, 1])

        # ================== COLONNE 1 : OPTIONS ==================
        with col1p:
            st.markdown("<br><br>", unsafe_allow_html=True)

            # --- Checkbox pour les colonnes (indicateurs/années) ---
            colonnes_disponibles = df_pib.columns[1:].tolist()
            indicateurs_select_pib = []
            st.markdown("**Choisir les indicateurs (années/zones) :**")
            for col in colonnes_disponibles:
                if st.checkbox(col, value=True, key=f"check_{col}_pib"):
                    indicateurs_select_pib.append(col)

            # --- Checkbox pour les secteurs (lignes) ---
            secteurs_disponibles = df_pib["Secteurs"].tolist()
            secteurs_selectionnes = []
            st.markdown("**Choisir les secteurs à afficher :**")
            for sec in secteurs_disponibles:
                if st.checkbox(sec, value=True, key=f"check_{sec}_pib"):
                    secteurs_selectionnes.append(sec)

            # --- Filtrage du dataframe ---
            df_filtered = df_pib[df_pib["Secteurs"].isin(secteurs_selectionnes)]

            # --- Choix du type de graphique ---
            graph_type_pib = st.selectbox(
                "Type de graphique",
                [
                    "Barres groupées",
                    "Barres empilées",
                    "Courbes multiples",
                    "Scatter multi-dimension",
                    "Pie Chart",
                    "Treemap",
                    "Radar Chart",
                    "Heatmap"
                ],
                index=7,
                key="graph_pib"
            )

        # ================== COLONNE 2 : GRAPHIQUE ==================
        with col2p:
            st.markdown("<br><br>", unsafe_allow_html=True)

            if not indicateurs_select_pib:
                st.warning("⚠ Veuillez sélectionner au moins un indicateur !")
            else:
                if graph_type_pib == "Barres groupées":
                    fig = px.bar(df_filtered, x="Secteurs", y=indicateurs_select_pib,
                                 barmode="group",
                                 color_discrete_sequence=custom_palette_pib[:len(indicateurs_select_pib)])
                    st.plotly_chart(fig, use_container_width=True)

                elif graph_type_pib == "Barres empilées":
                    fig = px.bar(df_filtered, x="Secteurs", y=indicateurs_select_pib,
                                 barmode="stack",
                                 color_discrete_sequence=custom_palette_pib[:len(indicateurs_select_pib)])
                    st.plotly_chart(fig, use_container_width=True)

                elif graph_type_pib == "Courbes multiples":
                    fig = px.line(df_filtered, x="Secteurs", y=indicateurs_select_pib, markers=True,
                                  color_discrete_sequence=custom_palette_pib[:len(indicateurs_select_pib)])
                    st.plotly_chart(fig, use_container_width=True)

                elif graph_type_pib == "Scatter multi-dimension":
                    if len(indicateurs_select_pib) >= 2:
                        x_col = indicateurs_select_pib[0]
                        y_col = indicateurs_select_pib[1]
                        fig = px.scatter(df_filtered, x=x_col, y=y_col, size=y_col, color="Secteurs",
                                         text="Secteurs",
                                         color_discrete_sequence=custom_palette_pib)
                        fig.update_traces(textposition="top center")
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.warning("⚠ Sélectionnez au moins deux indicateurs pour ce graphique.")

                elif graph_type_pib == "Pie Chart":
                    if len(indicateurs_select_pib) == 1:
                        fig = px.pie(df_filtered, names="Secteurs", values=indicateurs_select_pib[0],
                                     color_discrete_sequence=custom_palette_pib)
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.warning("⚠ Sélectionnez un seul indicateur pour le camembert.")

                elif graph_type_pib == "Treemap":
                    if len(indicateurs_select_pib) == 1:
                        fig = px.treemap(df_filtered, path=["Secteurs"],
                                         values=indicateurs_select_pib[0],
                                         color="Secteurs",
                                         color_discrete_sequence=custom_palette_pib)
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.warning("⚠ Sélectionnez un seul indicateur pour la treemap.")

                elif graph_type_pib == "Radar Chart":
                    if len(indicateurs_select_pib) > 0:
                        fig = px.line_polar(df_filtered, r=indicateurs_select_pib, theta="Secteurs",
                                            line_close=True,
                                            color_discrete_sequence=custom_palette_pib[:len(indicateurs_select_pib)])
                        st.plotly_chart(fig, use_container_width=True)

                elif graph_type_pib == "Heatmap":
                    df_heatmap = df_filtered.set_index("Secteurs")[indicateurs_select_pib]
                    fig = px.imshow(df_heatmap, text_auto=True, aspect="auto",
                                    color_continuous_scale="YlGnBu")
                    st.plotly_chart(fig, use_container_width=True)

        # ================== COLONNE 3 : TABLEAU ==================
        with col3p:
            st.markdown("<br><br><br><br><br>", unsafe_allow_html=True)
            st.dataframe(df_pib, use_container_width=True)

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("""
        <style>
            h1 {
                color: #000033;
            }
            .kpi-banner {
                background-color: #000033;
                color: white;
                padding: 1rem;
                border-radius: 0.5rem;
                display: flex;
                justify-content: space-between;
                align-items: center;
                flex-wrap: wrap;
                margin-bottom: 1rem;
            }
            .kpi-box {
                text-align: center;
                flex-grow: 1;
            }
            .kpi-box.min { order: 1; }
            .kpi-box.max { order: 2; }
            .kpi-box.total { order: 3; }
            .kpi-label {
                font-size: 0.9em;
                opacity: 0.8;
                display: block;
            }
            .kpi-value {
                font-size: 1.3em;
                font-weight: bold;
                display: block;
            }
        </style>
        """, unsafe_allow_html=True)

        # --- DONNÉES ---
        finance_data = {
            "depots_credits_banques": {
                "Province": ["Agadir Ida Outanane", "Inezgane Ait Melloul", "Chtouka Ait Baha",
                             "Taroudant", "Tiznit", "Tata"],
                "Montant des dépôts (en milliers)": [25599795, 9560580, 2488070, 5962524, 5697437, 254432],
                "Montant des crédits (en milliers)": [20526240, 3666514, 482351, 3747507, 1140457, 134904]
            },
            "projets_investissement_2017": {
                "Provinces": [
                    "Agadir Ida Outanane", "Inezgane Ait Melloul", "Chtouka Ait Baha",
                    "Taroudant", "Tiznit", "Tata"
                ],
                "Emplois à créer": [9083, 384, 1023, 896, 896, 512],
                "Montant d'investissement (millions de DH)": [11113, 780, 4641, 579, 590, 256],
                "Nombre de projets": [134, 23, 6, 17, 15, 17]
            }
        }


        # --- FONCTIONS ---
        @st.cache_data
        def load_shapefile(path):
            try:
                # Cette fonction nécessite que 'gpd' (GeoPandas) soit défini.
                return gpd.read_file(path)
            except Exception as e:
                st.error(f"Erreur lors du chargement du fichier shapefile : {e}")
                return None


        @st.cache_data
        def process_finance_data(data):
            # Unifier toutes les données financières en un seul DataFrame
            df_dc = pd.DataFrame(data["depots_credits_banques"])
            df_dc_melted = df_dc.melt(id_vars="Province", var_name="Indicateur", value_name="Valeur")
            df_dc_melted["Thème"] = "Activité Bancaire"

            df_pi = pd.DataFrame(data["projets_investissement_2017"])
            df_pi.rename(columns={"Provinces": "Province"}, inplace=True)
            df_pi_melted = df_pi.melt(id_vars="Province", var_name="Indicateur", value_name="Valeur")
            df_pi_melted["Thème"] = "Projets d'Investissement (2017)"

            final_df = pd.concat([df_dc_melted, df_pi_melted], ignore_index=True)
            return final_df


        # --- AFFICHAGE ---
        st.markdown(
            '<h5 style="background-color:#c9cad1; color:#494c63; display:inline-block; padding:8px 15px; border-radius:15px;">Dashboard Financier - Région Souss-Massa</h5>',
            unsafe_allow_html=True)
        df_complet = process_finance_data(finance_data)
        st.write("")

        # --- FILTRES (placés logiquement avant l'affichage mais affichés en bas) ---
        col1_filter, col2_filter = st.columns(2)
        with col1_filter:
            theme_choisi = st.selectbox("1. Choisissez un thème :", df_complet['Thème'].unique())
        df_theme = df_complet[df_complet['Thème'] == theme_choisi]
        with col2_filter:
            indicateur_choisi = st.selectbox("2. Choisissez un indicateur :", df_theme['Indicateur'].unique())
        df_filtre = df_theme[df_theme['Indicateur'] == indicateur_choisi]

        # --- BANDEAU KPI ---
        if not df_filtre.empty:
            total_regional = f"{df_filtre['Valeur'].sum():,.0f}".replace(',', ' ')
            max_province = df_filtre.loc[df_filtre['Valeur'].idxmax()]
            min_province = df_filtre.loc[df_filtre['Valeur'].idxmin()]
            max_val = f"{max_province['Valeur']:,.0f}".replace(',', ' ')
            min_val = f"{min_province['Valeur']:,.0f}".replace(',', ' ')

            st.markdown(f"""
            <div class="kpi-banner">
                <div class="kpi-box min">
                    <span class="kpi-label">Min: {min_province['Province']}</span>
                    <span class="kpi-value">{min_val}</span>
                </div>
                <div class="kpi-box max">
                    <span class="kpi-label">Max: {max_province['Province']}</span>
                    <span class="kpi-value">{max_val}</span>
                </div>
                <div class="kpi-box total">
                    <span class="kpi-label">Total Régional</span>
                    <span class="kpi-value">{total_regional}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("Aucune donnée disponible pour la sélection actuelle.")
            st.stop()

        # --- CARTE ET GRAPHIQUE ---
        shapefile_path = "mar_admbnda_adm2_hcp_20230925/mar_admbnda_adm2_hcp_20230925.shp"
        gdf_provinces = load_shapefile(shapefile_path)

        if gdf_provinces is not None:
            province_name_mapping = {
                'Agadir Ida Outanane': 'Agadir Ida Ou Tanane', 'Chtouka Ait Baha': 'Chtouka- Ait Baha',
                'Inezgane Ait Melloul': 'Inezgane-Ait Melloul', 'Taroudant': 'Taroudannt'
            }
            # Utiliser .loc pour éviter le SettingWithCopyWarning
            df_filtre.loc[:, 'Province_corrige'] = df_filtre['Province'].replace(province_name_mapping)
            merged_gdf = gdf_provinces.merge(df_filtre, left_on='ADM2_FR', right_on='Province_corrige', how='inner')

            if not merged_gdf.empty:
                col1_viz, col2_viz = st.columns((2, 1))
                with col1_viz:
                    fig_map = px.choropleth_mapbox(merged_gdf, geojson=merged_gdf.geometry, locations=merged_gdf.index,
                                                   color="Valeur", hover_name="Province",
                                                   color_continuous_scale="YlGnBu",
                                                   mapbox_style="open-street-map", center={"lat": 30.0, "lon": -8.5},
                                                   zoom=6,
                                                   opacity=0.8,
                                                   labels={'Valeur': indicateur_choisi})
                    fig_map.update_traces(marker_line_width=1.5, marker_line_color='white')
                    fig_map.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
                    st.plotly_chart(fig_map, use_container_width=True)
                with col2_viz:
                    df_sorted = merged_gdf.sort_values(by="Valeur", ascending=True)
                    fig_bar = px.bar(df_sorted, x="Valeur", y='Province', orientation='h', text_auto='.2s',
                                     color="Valeur", color_continuous_scale="YlGnBu",
                                     labels={'Valeur': indicateur_choisi})
                    fig_bar.update_layout(showlegend=False, yaxis_title=None)
                    st.plotly_chart(fig_bar, use_container_width=True)
            else:
                st.warning("Aucune donnée correspondante n'a pu être fusionnée avec la carte.")
        else:
            # Le message "Données géographiques non chargées." est déjà géré par la fonction load_shapefile
            pass

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

elif st.session_state.page == "Enseignement":
    st.markdown("<br>", unsafe_allow_html=True)

    st.set_page_config(layout="wide")

    st.markdown("""
        <style>
        .block-container {
            padding: 0;
            margin: 0;
            max-width: 100%;
        }

        .full-width-bar {
            width: 100%;
            background-color: #1E293B;
            padding: 15px 20px;  /* réduit les paddings */
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-sizing: border-box;
        }

        .bar-logo {
            font-family: 'Playfair Display', serif;
            color: white;
            font-size: 24px;   /* légèrement réduit */
            font-weight: 900;
        }

        .bar-menu {
            display: flex;
            gap: 10px;           /* réduit l’espace entre liens */
            max-width: 70%;       /* limite la largeur du menu pour éviter le dépassement */
            overflow-x: auto;     /* permet le défilement si écran trop petit */
        }

        .bar-menu a {
            color: white;
            text-decoration: none;
            font-size: 14px;      /* réduit la taille du texte */
            font-weight: 600;
            white-space: nowrap;  /* empêche le texte de passer à la ligne */
        }

        .bar-menu a:hover {
            color: #60A5FA;
        }

        .bar-menu .button {
            background-color: #3b82f6;
            padding: 5px 10px;
            border-radius: 6px;
            font-size: 14px;
            font-weight: 600;
        }

        .bar-menu .button:hover {
            background-color: #2563eb;
        }
        </style>

        <div class="full-width-bar">
            <div class="bar-logo">Axiora Data</div>
            <div class="bar-menu">
                <a href="#">App Marketing Agency</a>
                <a href="#">ASO Agency</a>
                <a href="#">Glossary</a>
                <a href="#">Data</a>
                <a href="#">ASO Tools</a>
                <a href="#" class="button">Read Blog</a>
            </div>
        </div>

        <div style="height: 60px;"></div>
        """, unsafe_allow_html=True)
    col11, col22, col33 = st.columns([0.1, 1, 0.1])
    with col22:
        data_2017 = {
            "Province": ["Agadir Ida Outanane", "Inezgane Aït Melloul", "Chtouka Aït Baha", "Taroudant", "Tiznit",
                         "Tata", "Région Souss-Massa"],
            "Garçons 2017": [6237, 6043, 4605, 9112, 1886, 1190, 29073],
            "Filles 2017": [5950, 5750, 4383, 8784, 1758, 1178, 27803],
            "Total 2017": [12187, 11793, 8988, 17896, 3644, 2368, 56876]
        }

        data_2018 = {
            "Province": ["Agadir Ida Outanane", "Inezgane Aït Melloul", "Chtouka Aït Baha", "Taroudant", "Tiznit",
                         "Tata", "Région Souss-Massa"],
            "Garçons 2018": [6233, 6236, 4961, 9248, 1923, 1288, 29889],
            "Filles 2018": [6187, 6016, 4666, 8826, 1905, 1152, 28752],
            "Total 2018": [12420, 12252, 9627, 18074, 3826, 2440, 58639]
        }

        df_2017 = pd.DataFrame(data_2017)
        df_2018 = pd.DataFrame(data_2018)

        # Fusion des 2 années
        df_all = pd.merge(df_2017, df_2018, on="Province")

        # ================== Interface ==================

        # --- VISUALISATION ---
        st.markdown(
            "<h4 style='color: #85919e;'>1-Nouveaux inscrits en 1ʳᵉ année selon le sexe, le milieu et les provinces/préfectures</h4>",
            unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 3, 1])

        with col1:
            year = st.radio("Choisir une année :", ["2017", "2018"], index=1, key="radio_year_2")

            show_boys = st.checkbox("Afficher Garçons", True, key="chk1")
            show_girls = st.checkbox("Afficher Filles", True, key="chk2")
            show_total = st.checkbox("Afficher Total", True, key="chk3")

            # --- nouveau : choix du type de graphe ---
            graph_type_viz = st.selectbox("Type de graphique", ["Barre", "Ligne", "Aire", "Nuage de points"], index=2)

        with col2:
            if year == "2017":
                df_plot = df_2017.copy()
                cols = []
                if show_boys: cols.append("Garçons 2017")
                if show_girls: cols.append("Filles 2017")
                if show_total: cols.append("Total 2017")
            else:
                df_plot = df_2018.copy()
                cols = []
                if show_boys: cols.append("Garçons 2018")
                if show_girls: cols.append("Filles 2018")
                if show_total: cols.append("Total 2018")

            if cols:
                df_melted = df_plot.melt(id_vars="Province", value_vars=cols, var_name="Catégorie", value_name="Valeur")

                # Choix dynamique du graphique
                if graph_type_viz == "Barre":
                    fig = px.bar(df_melted, x="Province", y="Valeur", color="Catégorie", barmode="group",
                                 color_discrete_sequence=["#5c5470", "#6a7b76", "#8d99ae"])
                elif graph_type_viz == "Ligne":
                    fig = px.line(df_melted, x="Province", y="Valeur", color="Catégorie", markers=True,
                                  color_discrete_sequence=["#5c5470", "#6a7b76", "#8d99ae"])
                elif graph_type_viz == "Aire":
                    fig = px.area(df_melted, x="Province", y="Valeur", color="Catégorie",
                                  color_discrete_sequence=["#5c5470", "#6a7b76", "#8d99ae"])
                elif graph_type_viz == "Nuage de points":
                    fig = px.scatter(df_melted, x="Province", y="Valeur", color="Catégorie", size="Valeur",
                                     color_discrete_sequence=["#5c5470", "#6a7b76", "#8d99ae"])

                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Veuillez sélectionner au moins un indicateur.")

        with col3:
            st.dataframe(df_plot)

        # --- COMPARAISON ---
        st.markdown("""
                <div style='background-color: #aab5bf; border-radius: 12px; padding: 8px 16px;
                 text-align: center; color: white; font-weight: bold; font-size: 18px; display: inline-block;'>
                Analyse Comparative par statut professionnel et milieu
                </div>
                """, unsafe_allow_html=True)
        col1c, col2c, col3c = st.columns([1, 1, 3])

        with col1c:
            st.markdown("<br><br>", unsafe_allow_html=True)
            st.markdown("""En comparant 2017 et 2018, on observe une progression générale des effectifs scolaires.""")
            st.markdown("<br><br>", unsafe_allow_html=True)
            st.markdown("""Une légère hausse du total régional.""")
            st.markdown("<br><br>", unsafe_allow_html=True)
            st.markdown("""Les écarts entre garçons et filles restent faibles.""")

        with col2c:
            st.markdown("<br><br>", unsafe_allow_html=True)

            compare_boys = st.checkbox("Comparer Garçons", True, key="comp_boys")
            compare_girls = st.checkbox("Comparer Filles", True, key="comp_girls")
            compare_total = st.checkbox("Comparer Total", True, key="comp_total")

            # --- nouveau : choix type de graphe comparaison ---
            graph_type_comp = st.selectbox("Type de graphique comparatif",
                                           ["Barre", "Ligne", "Aire", "Nuage de points"], index=0)

        with col3c:
            df_compare = df_all.copy()
            cols_compare = []
            if compare_boys: cols_compare += ["Garçons 2017", "Garçons 2018"]
            if compare_girls: cols_compare += ["Filles 2017", "Filles 2018"]
            if compare_total: cols_compare += ["Total 2017", "Total 2018"]

            if cols_compare:
                df_melted = df_compare.melt(id_vars="Province", value_vars=cols_compare, var_name="Catégorie",
                                            value_name="Valeur")

                if graph_type_comp == "Barre":
                    fig2 = px.bar(df_melted, x="Province", y="Valeur", color="Catégorie", barmode="group",
                                  color_discrete_sequence=["#3a506b", "#5c677d", "#9a8c98", "#8d99ae", "#6d6875",
                                                           "#4a4e69"])
                elif graph_type_comp == "Ligne":
                    fig2 = px.line(df_melted, x="Province", y="Valeur", color="Catégorie", markers=True,
                                   color_discrete_sequence=["#3a506b", "#5c677d", "#9a8c98", "#8d99ae", "#6d6875",
                                                            "#4a4e69"])
                elif graph_type_comp == "Aire":
                    fig2 = px.area(df_melted, x="Province", y="Valeur", color="Catégorie",
                                   color_discrete_sequence=["#3a506b", "#5c677d", "#9a8c98", "#8d99ae", "#6d6875",
                                                            "#4a4e69"])
                elif graph_type_comp == "Nuage de points":
                    fig2 = px.scatter(df_melted, x="Province", y="Valeur", color="Catégorie", size="Valeur",
                                      color_discrete_sequence=["#3a506b", "#5c677d", "#9a8c98", "#8d99ae", "#6d6875",
                                                               "#4a4e69"])

                st.plotly_chart(fig2, use_container_width=True)
            else:
                st.info("Veuillez sélectionner au moins un indicateur.")

        ####### taaaaaaaab 2
        import streamlit as st
        import pandas as pd
        import plotly.express as px

        # ================== Données ==================
        data_2017 = {
            "Province": ["Agadir Ida Outanane", "Inezgane Ait Melloul", "Chtouka Ait Baha",
                         "Taroudant", "Tiznit", "Tata", "Total"],
            "Garçons 2017": [769, 773, 1303, 3185, 837, 509, 7376],
            "Filles 2017": [1022, 874, 619, 2073, 385, 310, 5283],
            "Total 2017": [1791, 1647, 1922, 5258, 1222, 819, 12659]
        }

        data_2018 = {
            "Province": ["Agadir Ida Outanane", "Inezgane Ait Melloul", "Chtouka Ait Baha",
                         "Taroudant", "Tiznit", "Tata", "Total région Souss-Massa"],
            "Garçons 2018": [816, 830, 1334, 3048, 890, 494, 7412],
            "Filles 2018": [942, 728, 1772, 5185, 1301, 833, 5658],
            "Total 2018": [1758, 1558, 3106, 8233, 2191, 1327, 13070]
        }

        df_2017 = pd.DataFrame(data_2017)
        df_2018 = pd.DataFrame(data_2018)

        # Fusion des 2 années
        df_all = pd.merge(df_2017, df_2018, on="Province")

        # ================== Interface ==================

        # --- VISUALISATION ---
        st.markdown(
            "<h4 style='color: #607080;'>2-Personnel enseignant exerçant en classe selon le sexe et les provinces/préfectures								</h4>",
            unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 3, 1])

        with col1:
            st.markdown("<br><br><br>", unsafe_allow_html=True)
            year = st.radio("Choisir une année :", ["2017", "2018"], index=1, key="radio_year_1")

            show_boys = st.checkbox("Afficher Garçons", True, key="chk11")
            show_girls = st.checkbox("Afficher Filles", True, key="chk12")
            show_total = st.checkbox("Afficher Total", True, key="chk13")

            # --- nouveau : choix du type de graphe ---
            graph_type_viz = st.selectbox("Type de graphique", ["Barre", "Ligne", "Aire", "Nuage de points"], index=1)

        with col2:
            if year == "2017":
                df_plot = df_2017.copy()
                cols = []
                if show_boys: cols.append("Garçons 2017")
                if show_girls: cols.append("Filles 2017")
                if show_total: cols.append("Total 2017")
            else:
                df_plot = df_2018.copy()
                cols = []
                if show_boys: cols.append("Garçons 2018")
                if show_girls: cols.append("Filles 2018")
                if show_total: cols.append("Total 2018")

            if cols:
                df_melted = df_plot.melt(id_vars="Province", value_vars=cols, var_name="Catégorie", value_name="Valeur")

                palette_viz = ["#778da9", "#9ab87a", "#e5989b"]  # pastel plus doux

                if graph_type_viz == "Barre":
                    fig = px.bar(df_melted, x="Province", y="Valeur", color="Catégorie", barmode="group",
                                 color_discrete_sequence=palette_viz)
                elif graph_type_viz == "Ligne":
                    fig = px.line(df_melted, x="Province", y="Valeur", color="Catégorie", markers=True,
                                  color_discrete_sequence=palette_viz)
                elif graph_type_viz == "Aire":
                    fig = px.area(df_melted, x="Province", y="Valeur", color="Catégorie",
                                  color_discrete_sequence=palette_viz)
                elif graph_type_viz == "Nuage de points":
                    fig = px.scatter(df_melted, x="Province", y="Valeur", color="Catégorie", size="Valeur",
                                     color_discrete_sequence=palette_viz)

                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Veuillez sélectionner au moins un indicateur.")

        with col3:
            st.markdown("<br><br><br>", unsafe_allow_html=True)
            st.dataframe(df_plot)

        # --- COMPARAISON ---
        st.markdown("""
                        <div style='background-color: #aab5bf; border-radius: 12px; padding: 8px 16px;
                         text-align: center; color: white; font-weight: bold; font-size: 18px; display: inline-block;'>
                        Analyse Comparative par statut professionnel et milieu
                        </div>
                        """, unsafe_allow_html=True)

        col1c, col2c, col3c = st.columns([1, 1, 3])

        with col1c:
            st.markdown("<br><br>", unsafe_allow_html=True)
            st.markdown("""On observe une évolution positive des effectifs entre 2017 et 2018.""")
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("""Le total régional augmente légèrement.""")
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("""Les écarts entre garçons et filles persistent mais restent modérés.""")

        with col2c:
            st.markdown("<br><br><br><br><br>", unsafe_allow_html=True)

            compare_boys = st.checkbox("Comparer Garçons", True, key="comp_boys1")
            compare_girls = st.checkbox("Comparer Filles", True, key="comp_girls2")
            compare_total = st.checkbox("Comparer Total", True, key="comp_total3")

            # --- nouveau : choix type de graphe comparaison ---
            graph_type_comp = st.selectbox("Type de graphique comparatif",
                                           ["Barre", "Ligne", "Aire", "Nuage de points"], index=3)

        with col3c:
            df_compare = df_all.copy()
            cols_compare = []
            if compare_boys: cols_compare += ["Garçons 2017", "Garçons 2018"]
            if compare_girls: cols_compare += ["Filles 2017", "Filles 2018"]
            if compare_total: cols_compare += ["Total 2017", "Total 2018"]

            if cols_compare:
                df_melted = df_compare.melt(id_vars="Province", value_vars=cols_compare, var_name="Catégorie",
                                            value_name="Valeur")

                palette_comp = ["#4d908e", "#577590", "#f4a261", "#e76f51", "#90be6d", "#f94144"]

                if graph_type_comp == "Barre":
                    fig2 = px.bar(df_melted, x="Province", y="Valeur", color="Catégorie", barmode="group",
                                  color_discrete_sequence=palette_comp)
                elif graph_type_comp == "Ligne":
                    fig2 = px.line(df_melted, x="Province", y="Valeur", color="Catégorie", markers=True,
                                   color_discrete_sequence=palette_comp)
                elif graph_type_comp == "Aire":
                    fig2 = px.area(df_melted, x="Province", y="Valeur", color="Catégorie",
                                   color_discrete_sequence=palette_comp)
                elif graph_type_comp == "Nuage de points":
                    fig2 = px.scatter(df_melted, x="Province", y="Valeur", color="Catégorie", size="Valeur",
                                      color_discrete_sequence=palette_comp)

                st.plotly_chart(fig2, use_container_width=True)
            else:
                st.info("Veuillez sélectionner au moins un indicateur.")

        data_2017 = {
            "Province": ["Agadir Ida Outanane", "Inezgane Aït Melloul", "Chtouka Aït Baha",
                         "Taroudant", "Tiznit", "Tata", "Total"],
            "1ère": [4492, 4443, 3987, 8280, 1607, 1516, 23925],
            "2ème": [4191, 4399, 3751, 7239, 1178, 1147, 22005],
            "3ème": [4283, 4399, 3987, 8611, 1147, 1134, 23561],
            "4ème": [4204, 4147, 4147, 8985, 1232, 1209, 24924],
            "5ème": [3932, 3754, 3754, 8144, 1134, 1134, 29852],
            "6ème": [4433, 4515, 4515, 9856, 1339, 1339, 25097],
            "Total": [25535, 27293, 24547, 51083, 6637, 7479, 161718]
        }

        data_2018 = {
            "Province": ["Agadir Idaoutanane", "Inezgane Ait Melloul", "Chtouka Ait Baha",
                         "Taroudant", "Tiznit", "Tata", "Total Région Souss-Massa"],
            "1ère": [4117, 8157, 8964, 8838, 3168, 2426, 35670],
            "2ème": [4049, 8171, 8907, 8514, 3097, 2343, 35081],
            "3ème": [3952, 7993, 8828, 8239, 3073, 2357, 34742],
            "4ème": [4022, 8123, 8746, 7943, 3115, 2313, 35362],
            "5ème": [4037, 8013, 8558, 7730, 3127, 2190, 33655],
            "6ème": [3800, 7649, 8566, 7241, 2971, 2215, 32442],
            "Total": [23977, 48106, 52569, 48505, 18551, 13844, 207952]
        }

        df_2017 = pd.DataFrame(data_2017)
        df_2018 = pd.DataFrame(data_2018)

        # Fusion des deux années
        df_all = pd.merge(df_2017, df_2018, left_on="Province", right_on="Province", suffixes=("_2017", "_2018"))

        # ================== Interface ==================

        st.markdown("<h4 style='color: #607080;'>3-Personnel enseignant par classe et province</h4>",
                    unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 3, 1])
        with col1:
            year = st.radio("Choisir une année :", ["2017", "2018"], index=1, key="radio_year3")
            show_cols = st.multiselect("Afficher classes:",
                                       options=df_2017.columns[1:],
                                       default=list(df_2017.columns[1:]),  # tout sélectionné par défaut
                                       key="multi_cols3")
            graph_type_viz = st.selectbox("Type de graphique",
                                          ["Barre", "Ligne", "Aire", "Radar", "Nuage de points", "Box"], index=3,
                                          key="graph_viz3")

        with col2:
            df_plot = df_2017.copy() if year == "2017" else df_2018.copy()
            cols = [c for c in df_plot.columns if c in show_cols]

            if cols:
                df_melted = df_plot.melt(id_vars="Province", value_vars=cols, var_name="Classe", value_name="Effectifs")
                # Palette pastel douce
                palette_viz = ["#9cadad", "#9dad9c", "#9f9cad", "#ac9cad", "#e8e5ba", "#946363", "#bfd6b0"]

                if graph_type_viz == "Barre":
                    fig = px.bar(df_melted, x="Province", y="Effectifs", color="Classe", barmode="group",
                                 color_discrete_sequence=palette_viz)
                elif graph_type_viz == "Ligne":
                    fig = px.line(df_melted, x="Province", y="Effectifs", color="Classe", markers=True,
                                  color_discrete_sequence=palette_viz)
                elif graph_type_viz == "Aire":
                    fig = px.area(df_melted, x="Province", y="Effectifs", color="Classe",
                                  color_discrete_sequence=palette_viz)
                elif graph_type_viz == "Radar":
                    fig = px.line_polar(df_melted, r="Effectifs", theta="Classe", color="Province", line_close=True,
                                        color_discrete_sequence=palette_viz)
                elif graph_type_viz == "Nuage de points":
                    fig = px.scatter(df_melted, x="Province", y="Effectifs", color="Classe", size="Effectifs",
                                     color_discrete_sequence=palette_viz)
                elif graph_type_viz == "Box":
                    fig = px.box(df_melted, x="Classe", y="Effectifs", color="Classe",
                                 color_discrete_sequence=palette_viz)

                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Veuillez sélectionner au moins une classe.")

        with col3:
            st.dataframe(df_plot)

        # --- Comparaison ---

        st.markdown("""
                        <div style='background-color: #aab5bf; border-radius: 12px; padding: 8px 16px;
                         text-align: center; color: white; font-weight: bold; font-size: 18px; display: inline-block;'>
                        Analyse Comparative par statut professionnel et milieu
                        </div>
                        """, unsafe_allow_html=True)

        col1c, col2c, col3c = st.columns([1, 1, 3])

        with col1c:
            st.markdown("<br><br><br><br>", unsafe_allow_html=True)
            st.markdown("Évolution globale des effectifs par province entre 2017 et 2018.")
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("Comparaison des classes et du total.")

        with col2c:
            st.markdown("<br><br><br>", unsafe_allow_html=True)

            compare_cols = st.multiselect("Colonnes à comparer:", options=df_2017.columns[1:],
                                          default=list(df_2017.columns[1:]), key="compare_cols3")
            graph_type_comp = st.selectbox("Type de graphique comparatif",
                                           ["Barre", "Ligne", "Aire", "Radar", "Nuage de points", "Box"], index=5,
                                           key="graph_comp3")
        with col3c:
            if compare_cols:
                cols_compare = []
                for c in compare_cols:
                    cols_compare += [f"{c}_2017", f"{c}_2018"]

                df_melted_comp = df_all.melt(id_vars="Province", value_vars=cols_compare,
                                             var_name="Classe_Annee", value_name="Effectifs")

                # Palette pastel douce
                palette_comp = ["#9cadad", "#9dad9c", "#9f9cad", "#ac9cad", "#e8e5ba", "#946363", "#bfd6b0"]

                if graph_type_comp == "Barre":
                    fig2 = px.bar(df_melted_comp, x="Province", y="Effectifs", color="Classe_Annee",
                                  barmode="group", color_discrete_sequence=palette_comp)
                elif graph_type_comp == "Ligne":
                    fig2 = px.line(df_melted_comp, x="Province", y="Effectifs", color="Classe_Annee",
                                   markers=True, color_discrete_sequence=palette_comp)
                elif graph_type_comp == "Aire":
                    fig2 = px.area(df_melted_comp, x="Province", y="Effectifs", color="Classe_Annee",
                                   color_discrete_sequence=palette_comp)
                elif graph_type_comp == "Radar":
                    # Pour éviter trop de séries, on peut limiter aux 2 premières colonnes
                    sample_df = df_melted_comp[df_melted_comp['Classe_Annee'].isin(cols_compare[:2])]
                    fig2 = px.line_polar(sample_df, r="Effectifs", theta="Classe_Annee", color="Province",
                                         line_close=True, color_discrete_sequence=palette_comp)
                elif graph_type_comp == "Nuage de points":
                    fig2 = px.scatter(df_melted_comp, x="Province", y="Effectifs", color="Classe_Annee",
                                      size="Effectifs", color_discrete_sequence=palette_comp)
                elif graph_type_comp == "Box":
                    fig2 = px.box(df_melted_comp, x="Classe_Annee", y="Effectifs", color="Classe_Annee",
                                  color_discrete_sequence=palette_comp)

                st.plotly_chart(fig2, use_container_width=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        # --- CONFIGURATION DE LA PAGE ---
        import streamlit as st
        import pandas as pd
        import geopandas as gpd
        import plotly.express as px
        import numpy as np
        import random
        from shapely.geometry import Point  # <-- LIGNE AJOUTÉE POUR CORRIGER L'ERREUR

        # --- CONFIGURATION DE LA PAGE ---
        st.set_page_config(page_title="Axioradata - Dashboard Enseignement", layout="wide")

        # --- STYLE CSS ---
        st.markdown("""
        <style>
            .kpi-banner {
                background-color: #2f2f4d; /* Couleur de fond sombre */
                padding: 1.5rem;
                border-radius: 0.5rem;
                display: flex;
                justify-content: space-around;
                align-items: center;
                flex-wrap: wrap;
                margin-bottom: 2rem;
            }
            .kpi-box { text-align: center; flex-grow: 1; padding: 1rem; }
            .kpi-label { font-size: 0.9em; color: #ffffff; opacity: 0.8; display: block; margin-bottom: 0.25rem; }
            .kpi-value { font-size: 2em; font-weight: bold; color: #ffffff; display: block; }
            .kpi-subvalue { font-size: 0.8em; color: #ffffff; opacity: 0.9; }
        </style>
        """, unsafe_allow_html=True)

        # --- DONNÉES ENSEIGNEMENT ---
        enseignement_data = {
            "Nouveaux inscrits (1ère année)": {
                "2017": {"Province": ["Agadir Ida Outanane", "Inezgane Aït Melloul", "Chtouka Aït Baha", "Taroudant",
                                      "Tiznit", "Tata", "Région Souss-Massa"],
                         "Garçons": [6237, 6043, 4605, 9112, 1886, 1190, 29073],
                         "Filles": [5950, 5750, 4383, 8784, 1758, 1178, 27803],
                         "Total": [12187, 11793, 8988, 17896, 3644, 2368, 56876]},
                "2018": {"Province": ["Agadir Ida Outanane", "Inezgane Aït Melloul", "Chtouka Aït Baha", "Taroudant",
                                      "Tiznit", "Tata", "Région Souss-Massa"],
                         "Garçons": [6233, 6236, 4961, 9248, 1923, 1288, 29889],
                         "Filles": [6187, 6016, 4666, 8826, 1905, 1152, 28752],
                         "Total": [12420, 12252, 9627, 18074, 3826, 2440, 58639]}
            },
            "Personnel enseignant par sexe": {
                "2017": {"Province": ["Agadir Ida Outanane", "Inezgane Ait Melloul", "Chtouka Ait Baha", "Taroudant",
                                      "Tiznit", "Tata", "Total"], "Hommes": [769, 773, 1303, 3185, 837, 509, 7376],
                         "Femmes": [1022, 874, 619, 2073, 385, 310, 5283],
                         "Total": [1791, 1647, 1922, 5258, 1222, 819, 12659]},
                "2018": {"Province": ["Agadir Idaoutanane", "Inezgane Ait Melloul", "Chtouka Ait Baha", "Taroudant",
                                      "Tiznit", "Tata", "Total région Souss-Massa"],
                         "Hommes": [816, 830, 1334, 3048, 890, 494, 7412],
                         "Femmes": [942, 728, 1772, 5185, 1301, 833, 5658],
                         "Total": [1758, 1558, 3106, 8233, 2191, 1327, 13070]}
            },
            "Élèves par classe": {
                "2017": {"Province": ["Agadir Ida Outanane", "Inezgane Aït Melloul", "Chtouka Aït Baha", "Taroudant",
                                      "Tiznit", "Tata", "Total"], "1ère": [4492, 4443, 3987, 8280, 1607, 1516, 23925],
                         "2ème": [4191, 4399, 3751, 7239, 1178, 1147, 22005],
                         "3ème": [4283, 4399, 3987, 8611, 1147, 1134, 23561],
                         "4ème": [4204, 4147, 4147, 8985, 1232, 1209, 24924],
                         "5ème": [3932, 3754, 3754, 8144, 1134, 1134, 29852],
                         "6ème": [4433, 4515, 4515, 9856, 1339, 1339, 25097],
                         "Total": [25535, 27293, 24547, 51083, 6637, 7479, 161718]},
                "2018": {"Province": ["Agadir Idaoutanane", "Inezgane Ait Melloul", "Chtouka Ait Baha", "Taroudant",
                                      "Tiznit", "Tata", "Total Région Souss-Massa"],
                         "1ère": [4492, 4443, 3987, 8280, 1607, 1516, 23925],
                         "2ème": [4191, 4399, 3751, 7239, 1178, 1147, 22005],
                         "3ème": [4283, 4399, 3987, 8611, 1147, 1134, 23561],
                         "4ème": [4204, 4147, 4147, 8985, 1232, 1209, 24924],
                         "5ème": [3932, 3754, 3754, 8144, 1134, 1134, 29852],
                         "6ème": [4433, 4515, 4515, 9856, 1339, 1339, 25097],
                         "Total": [25535, 27293, 24547, 51083, 6637, 7479, 161718]}
            }
        }


        # --- FONCTIONS ---
        @st.cache_data
        def load_shapefile(path):
            try:
                return gpd.read_file(path)
            except Exception as e:
                st.error(f"Erreur de chargement du fichier {path} : {e}"); return None


        @st.cache_data
        def process_data(data):
            province_data = []
            for theme, theme_data in data.items():
                if "Évolution" not in theme:
                    for year, year_data in theme_data.items():
                        df = pd.DataFrame(year_data)
                        df.columns = [col.replace('Garçons', 'Hommes').replace('Filles', 'Femmes') for col in
                                      df.columns]
                        df_melted = df.melt(id_vars=["Province"], var_name="Indicateur", value_name="Valeur")
                        df_melted["Thème"] = theme;
                        df_melted["Année"] = year
                        province_data.append(df_melted)

            df_province = pd.concat(province_data, ignore_index=True)
            df_province = df_province[~df_province['Province'].str.contains("Région|Total", regex=True)].copy()
            df_province['Valeur'] = pd.to_numeric(df_province['Valeur'], errors='coerce').dropna()
            return df_province


        def generate_random_points_in_polygon(polygon, num_points):
            points = []
            minx, miny, maxx, maxy = polygon.bounds
            if polygon.geom_type == 'MultiPolygon':
                largest_polygon = max(polygon.geoms, key=lambda p: p.area)
            else:
                largest_polygon = polygon

            attempts = 0
            max_attempts = num_points * 100
            while len(points) < num_points and attempts < max_attempts:
                random_point = Point(random.uniform(minx, maxx), random.uniform(miny, maxy))
                if largest_polygon.contains(random_point):
                    points.append({'lon': random_point.x, 'lat': random_point.y})
                attempts += 1
            return points


        # --- TITRE ---
        st.markdown(
            "<h3 style='text-align: center; color: #000033;'>Analyse du Secteur de l'Enseignement (Souss-Massa)</h3>",
            unsafe_allow_html=True)

        # --- CHARGEMENT ET PRÉPARATION ---
        df_provinces = process_data(enseignement_data)
        shapefile_path = "mar_admbnda_adm2_hcp_20230925/mar_admbnda_adm2_hcp_20230925.shp"
        gdf_provinces = load_shapefile(shapefile_path)

        # --- FILTRES ---
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            theme_choisi = st.selectbox("1. Choisissez un thème :", df_provinces['Thème'].unique())
        df_theme = df_provinces[df_provinces['Thème'] == theme_choisi]
        with col_f2:
            annee_choisie = st.selectbox("2. Choisissez une année :", df_theme['Année'].unique())
        df_annee = df_theme[df_theme['Année'] == annee_choisie]

        themes_genres = ["Nouveaux inscrits (1ère année)", "Personnel enseignant par sexe"]
        is_gendered_theme = theme_choisi in themes_genres

        if not is_gendered_theme:
            indicateur_choisi = st.selectbox("3. Choisissez un indicateur :", df_annee['Indicateur'].unique())
            df_filtre = df_annee[df_annee['Indicateur'] == indicateur_choisi]
        else:
            df_filtre = df_annee[df_annee['Indicateur'].isin(['Hommes', 'Femmes'])]

        # --- BANNIÈRE KPI ---
        if not df_filtre.empty:
            total_val = df_filtre['Valeur'].sum()
            st.markdown(f"""
            <div class="kpi-banner">
                <div class="kpi-box"><span class="kpi-label">Total pour la sélection</span><span class="kpi-value">{int(total_val):,}</span><span class="kpi-subvalue">{theme_choisi} ({annee_choisie})</span></div>
            </div>""", unsafe_allow_html=True)

        # --- CARTE ET GRAPHIQUE ---
        if gdf_provinces is not None and not df_filtre.empty:
            province_name_mapping = {'Agadir Ida Outanane': 'Agadir Ida Ou Tanane',
                                     'Chtouka Aït Baha': 'Chtouka- Ait Baha',
                                     'Inezgane Aït Melloul': 'Inezgane-Ait Melloul', 'Taroudant': 'Taroudannt',
                                     'Agadir Idaoutanane': 'Agadir Ida Ou Tanane',
                                     'Inezgane Ait Melloul': 'Inezgane-Ait Melloul',
                                     'Chtouka Ait Baha': 'Chtouka- Ait Baha'}
            df_filtre['join_key'] = df_filtre['Province'].replace(province_name_mapping)
            gdf_provinces['join_key'] = gdf_provinces['ADM2_FR']
            gdf_merged = gdf_provinces.merge(df_filtre, on='join_key', how='inner')

            if not gdf_merged.empty:
                col1, col2 = st.columns([3, 2])
                with col1:


                    MAP_STYLE = "open-street-map"

                    if is_gendered_theme:
                        all_generated_points = []
                        POINTS_SCALE_FACTOR = 40

                        for _, row in gdf_merged.iterrows():
                            num_dots = int(row['Valeur'] / POINTS_SCALE_FACTOR)
                            num_dots = min(num_dots, 700)

                            points_coords = generate_random_points_in_polygon(row['geometry'], num_dots)
                            for p in points_coords:
                                p['Indicateur'] = row['Indicateur']
                                p['Province'] = row['Province']
                                all_generated_points.append(p)

                        df_points = pd.DataFrame(all_generated_points)

                        if not df_points.empty:
                            fig_map = px.scatter_mapbox(
                                df_points, lat="lat", lon="lon",
                                color="Indicateur",
                                hover_name="Province",
                                mapbox_style=MAP_STYLE,
                                center={"lat": 30.2, "lon": -9.0}, zoom=6.5,
                                color_discrete_map={"Hommes": "#4d4d66", "Femmes": "#c478b4"}
                            )
                            fig_map.update_traces(marker=dict(size=6, opacity=0.7))
                        else:
                            fig_map = px.choropleth_mapbox(gdf_merged, geojson=gdf_merged.geometry,
                                                           locations=gdf_merged.index, color_continuous_scale="Blues",
                                                           mapbox_style=MAP_STYLE, center={"lat": 30.2, "lon": -9.0},
                                                           zoom=6.5)
                            st.warning("Pas assez de données pour générer des points dispersés.")

                    else:
                        fig_map = px.choropleth_mapbox(gdf_merged, geojson=gdf_merged.geometry,
                                                       locations=gdf_merged.index, color="Valeur",
                                                       hover_name="Province", mapbox_style=MAP_STYLE,
                                                       center={"lat": 30.2, "lon": -9.0}, zoom=6.5,
                                                       color_continuous_scale="Blues")

                    fig_map.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, height=600, legend_title_text='')
                    st.plotly_chart(fig_map, use_container_width=True)

                with col2:

                    if is_gendered_theme:
                        fig_bar = px.bar(gdf_merged.sort_values("Valeur", ascending=False),
                                         x="Valeur", y="Province",
                                         color="Indicateur",
                                         orientation='h', barmode="group",
                                         color_discrete_map={"Hommes": "#4d4d66", "Femmes": "#c478b4"}
                                         )
                        fig_bar.update_layout(yaxis={'categoryorder': 'total ascending'})
                    else:
                        fig_bar = px.bar(gdf_merged.sort_values("Valeur", ascending=True), x="Valeur", y='Province',
                                         orientation='h', color="Valeur", color_continuous_scale="Blues")

                    fig_bar.update_layout(margin={"r": 0, "t": 30, "l": 0, "b": 0}, height=600, showlegend=True,
                                          yaxis_title="", xaxis_title=f"Effectif ({annee_choisie})",
                                          legend_title_text='')
                    st.plotly_chart(fig_bar, use_container_width=True)

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)


elif st.session_state.page == "pauvrete":
    st.markdown("<br>", unsafe_allow_html=True)

    st.set_page_config(layout="wide")

    st.markdown("""
        <style>
        .block-container {
            padding: 0;
            margin: 0;
            max-width: 100%;
        }

        .full-width-bar {
            width: 100%;
            background-color: #1E293B;
            padding: 15px 20px;  /* réduit les paddings */
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-sizing: border-box;
        }

        .bar-logo {
            font-family: 'Playfair Display', serif;
            color: white;
            font-size: 24px;   /* légèrement réduit */
            font-weight: 900;
        }

        .bar-menu {
            display: flex;
            gap: 10px;           /* réduit l’espace entre liens */
            max-width: 70%;       /* limite la largeur du menu pour éviter le dépassement */
            overflow-x: auto;     /* permet le défilement si écran trop petit */
        }

        .bar-menu a {
            color: white;
            text-decoration: none;
            font-size: 14px;      /* réduit la taille du texte */
            font-weight: 600;
            white-space: nowrap;  /* empêche le texte de passer à la ligne */
        }

        .bar-menu a:hover {
            color: #60A5FA;
        }

        .bar-menu .button {
            background-color: #3b82f6;
            padding: 5px 10px;
            border-radius: 6px;
            font-size: 14px;
            font-weight: 600;
        }

        .bar-menu .button:hover {
            background-color: #2563eb;
        }
        </style>

        <div class="full-width-bar">
            <div class="bar-logo">Axiora Data</div>
            <div class="bar-menu">
                <a href="#">App Marketing Agency</a>
                <a href="#">ASO Agency</a>
                <a href="#">Glossary</a>
                <a href="#">Data</a>
                <a href="#">ASO Tools</a>
                <a href="#" class="button">Read Blog</a>
            </div>
        </div>

        <div style="height: 60px;"></div>
        """, unsafe_allow_html=True)
    col11, col22, col33 = st.columns([0.1, 1, 0.1])
    with col22:
        import streamlit as st
        import pandas as pd
        import geopandas as gpd
        import plotly.express as px

        # --- CONFIGURATION DE LA PAGE ---
        st.set_page_config(page_title="Axioradata - Dashboard Pauvreté", layout="wide")

        # --- STYLE CSS (Pour la bannière des KPIs) ---
        st.markdown("""
        <style>
            .kpi-banner {
                background-color: #2b2b45;
                padding: 1.5rem;
                border-radius: 0.5rem;
                display: flex;
                justify-content: space-around;
                align-items: center;
                flex-wrap: wrap;
                margin-bottom: 2rem;
            }
            .kpi-box {
                text-align: center;
                flex-grow: 1;
                padding: 1rem;
            }
            .kpi-label {
                font-size: 0.9em;
                color: #ffffff;
                opacity: 0.8;
                display: block;
                margin-bottom: 0.25rem;
            }
            .kpi-value {
                font-size: 2em;
                font-weight: bold;
                color: #ffffff;
                display: block;
            }
            .kpi-subvalue {
                font-size: 0.8em;
                color: #ffffff;
                opacity: 0.9;
            }
        </style>
        """, unsafe_allow_html=True)

        # --- DONNÉES ---
        pauvrete_data = {
            "Chtouka- Ait Baha": {
                "Commune": ["Ait Baha (M)", "Biougra (M)", "Ait Mzal", "Ait Ouadrim", "Aouguenz", "Hilala",
                            "Ida-Ougnidif",
                            "Sidi Abdallah El Bouchouari", "Tanalt", "Targua-Ntouchka", "Tassegdelt", "Tizi Ntakoucht",
                            "Ait Milk", "Belfaa", "Belfaa Centre (AC)", "Inchaden", "Massa", "Massa centre (AC)",
                            "Sidi Ouassay", "Ait Amira", "Ait Amira centre (AC)", "Imi-Mqourn", "Ouad Essafa",
                            "Sidi Bibi",
                            "Sidi Bibi centre (AC)", "Sidi Boushab", "Province de Chtouka-Ait Baha Urbain",
                            "Province de Chtouka-Ait Baha Rural", "Province de Chtouka-Ait Baha Ensemble"],
                "Taux de pauvreté 2014": [11.27, 1.02, 7.44, 13.16, 10.24, 11.42, 6.44, 15.83, 3.73, 17.35, 8.68, 8.41,
                                          5.75,
                                          2.27, 1.55, 1.78, 2.45, 8.48, 1.68, 1.38, 0.85, 14.69, 4.29, 2.69, 0.55, 7.25,
                                          2.13,
                                          4.92, 4.07],
                "Taux de vulnérabilité 2014": [22.06, 7.9, 20.98, 25.51, 23.44, 27.44, 20.22, 28.86, 12.96, 30.59,
                                               21.45, 20.64,
                                               18.13, 9.47, 10.01, 7.48, 10.12, 17.95, 7.47, 6.75, 8.12, 29.11, 14.67,
                                               10.71,
                                               5.51, 20.37, 9.57, 14.16, 12.76]
            },
            "Tiznit": {
                "Commune": ["Tafraout (M)", "Tiznit (M)", "Ait Issafen", "Anzi", "Arbaa Ait Ahmed", "Ida Ou Gougmar",
                            "Sidi Ahmed Ou Moussa", "Tafraout El Mouloud", "Tighmi", "Tizoughrane", "Tnine Aday",
                            "Afella Ighir", "Ait Ouafqa", "Ammelne", "Irigh N'Tahala", "Tarsouat", "Tassrirt",
                            "Arbaa Rasmouka",
                            "Arbaa Sahel", "Bounaamane", "El Maader El Kabir", "Ouijjane", "Reggada", "Sidi Bouabdelli",
                            "Tnine Aglou", "Province de Tiznit Urbain", "Province de Tiznit Rural",
                            "Province de Tiznit Ensemble"],
                "Taux de pauvreté 2014": [4.89, 2.19, 10.32, 10.91, 18.06, 11.87, 7.45, 14.55, 12.03, 9.65, 12.41, 7.65,
                                          5.01,
                                          6.5, 8.98, 6.57, 3.02, 6.52, 3.2, 11.22, 3.66, 5.65, 7.21, 18.08, 3.09, 2.4,
                                          8.53,
                                          6.13],
                "Taux de vulnérabilité 2014": [10.84, 8.84, 24.16, 22.32, 29.59, 25.66, 20.75, 23.94, 24.47, 21.64,
                                               25.39,
                                               19.14, 15.24, 17.8, 22.22, 18.29, 12.0, 19.86, 13.23, 25.55, 14.14,
                                               17.58, 18.37,
                                               31.19, 12.5, 8.99, 20.25, 15.84]
            },
            "Tata": {
                "Commune": ["Akka (M)", "Fam El Hisn (M)", "Foum Zguid (M)", "Tata (M)", "Ait Ouabelli",
                            "Kasbat Sidi Abdellah Ben M'Barek", "Tamanarte", "Tizounine", "Aguinane", "Akka-Ighane",
                            "Allougoum", "Ibn Yacoub", "Tissint", "Tlite", "Adis", "Issafen", "Oum El Guerdane",
                            "Tagmout",
                            "Tigzmerte", "Tizaghte", "Province de Tata Urbain", "Province de Tata Rural",
                            "Province de Tata Ensemble"],
                "Taux de pauvreté 2014": [21.27, 11.48, 14.62, 4.06, 16.85, 25.21, 9.66, 16.38, 17.72, 33.08, 37.21,
                                          22.02,
                                          21.85, 25.09, 12.84, 18.21, 10.69, 15.34, 7.36, 11.92, 10.15, 20.38, 17.01],
                "Taux de vulnérabilité 2014": [29.05, 20.59, 24.31, 16.51, 32.62, 31.49, 22.43, 27.9, 28.77, 32.73,
                                               31.12,
                                               40.17, 29.8, 32.7, 35.22, 28.4, 22.66, 26.26, 23.15, 25.22, 20.77, 29.56,
                                               26.67]
            },
            "Taroudannt": {
                "Commune": ["Ait Iaaza (M)", "Aoulouz (M)", "El Guerdane (M)", "Irherm (M)", "Oulad Berhil (M)",
                            "Oulad Teima (M)", "Taliouine (M)", "Taroudannt (M)", "Adar", "Ait Abdallah", "Amalou",
                            "Azaghar N'Irs", "Imaouen", "Imi N'Tayart", "Nihit", "Oualqadi", "Sidi Boaal", "Sidi Mzal",
                            "Tabia",
                            "Tataoute", "Tindine", "Tisfane", "Toufelaazt", "Toumliline", "Arazane", "El Faid",
                            "Ida Ou Gailal",
                            "Ida-Ougoummad", "Igli", "Igoudar Mnabha", "Lamhara", "Oulad Aissa", "Ouneine",
                            "Sidi Abdellah Ou Said", "Sidi Ouaaziz", "Tafingoult", "Talgjount", "Tigouga", "Tinzart",
                            "Tizi N'Test", "Toughmart", "Ahl Ramel", "Argana", "Assads", "Bigoudine", "Eddir",
                            "El Koudia El Beida", "Imilmaiss", "Issen", "Lagfifat", "Lakhnafif", "Lamhadi",
                            "Machraa El Ain",
                            "Sidi Ahmed Ou Amar", "Sidi Boumoussa", "Sidi Moussa Lhamri", "Talmakante",
                            "Tidsi-Nissendalene",
                            "Agadir Melloul", "Ahl Tifnoute", "Askaouen", "Assaisse", "Assaki", "Azrar", "Iguidi",
                            "Sidi Hsaine", "Taouyalte", "Tassousfi", "Tizgzaouine", "Toubkal", "Zagmouzen", "Ouzioua",
                            "Tisrasse", "Ahmar Laglalcha", "Ait Igas", "Ait Makhlouf", "Bounrar", "Freija",
                            "Ida Ou Moumen",
                            "Imoulass", "Lamnizla", "Sidi Ahmed Ou Abdallah", "Sidi Borja", "Sidi Dahmane",
                            "Tafraouten",
                            "Tamaloukte", "Tazemmourt", "Tiout", "Zaouia Sidi Tahar", "Province de Taroudannt Urbain",
                            "Province de Taroudannt Rural", "Province de Taroudannt Ensemble"],
                "Taux de pauvreté 2014": [4.2, 21.04, 3.93, 24.64, 11.16, 4.16, 16.38, 2.37, 12.66, 8.49, 11.04, 13.37,
                                          16.56,
                                          4.48, 6.8, 8.98, 9.68, 6.64, 17.31, 10.33, 19.05, 17.01, 30.61, 15.97, 18.64,
                                          17.59,
                                          21.34, 14.47, 5.59, 5.3, 5.76, 2.98, 14.36, 13.13, 11.89, 15.92, 24.9, 21.65,
                                          6.81,
                                          28.78, 17.09, 4.89, 21.5, 16.37, 27.92, 13.68, 5.11, 15.89, 11.97, 6.89, 5.41,
                                          5.94,
                                          4.64, 6.5, 5.79, 11.55, 13.11, 15.77, 26.11, 9.32, 10.23, 7.08, 11.95, 17.09,
                                          11.94,
                                          4.09, 14.94, 7.72, 7.76, 10.93, 17.47, 22.99, 24.61, 6.75, 10.71, 11.46,
                                          10.79, 6.78,
                                          10.29, 12.54, 13.21, 16.43, 6.98, 6.12, 11.65, 12.64, 7.56, 15.65, 5.36, 6.02,
                                          11.17,
                                          9.65],
                "Taux de vulnérabilité 2014": [13.2, 26.04, 15.18, 26.57, 19.85, 13.89, 22.88, 9.85, 25.01, 21.61,
                                               23.79, 26.01,
                                               27.84, 14.01, 17.49, 21.98, 22.51, 20.33, 23.87, 25.56, 30.92, 27.38,
                                               32.18,
                                               27.42, 28.55, 30.06, 30.38, 28.09, 15.53, 16.92, 16.51, 10.9, 29.08,
                                               25.08,
                                               26.68, 28.06, 35.35, 33.19, 19.19, 37.57, 29.23, 15.87, 31.65, 28.54,
                                               32.34,
                                               26.1, 14.42, 30.96, 24.21, 17.6, 15.56, 17.05, 14.61, 17.32, 16.24,
                                               22.77, 29.05,
                                               30.31, 32.24, 20.01, 22.37, 16.58, 22.54, 31.22, 24.23, 14.32, 28.87,
                                               20.83,
                                               20.86, 24.04, 29.78, 31.49, 33.52, 17.99, 21.81, 26.03, 26.18, 17.93,
                                               23.85,
                                               27.9, 28.09, 30.64, 18.92, 17.97, 24.97, 25.83, 19.29, 29.7, 15.91,
                                               14.43, 22.64,
                                               20.21]
            },
            "Agadir-Ida -Ou-Tanane": {
                "Commune": ["Agadir (M)", "Amskroud", "Drargua", "Drargua centre (AC)", "Idmine", "Aourir",
                            "Aourir centre (AC)", "Aqsri", "Aziar", "Imouzzer", "Imsouane", "Tadrart", "Taghazout",
                            "Tamri",
                            "Tiqqi", "Préfecture d'Agadir-Idaoutanane Urbain", "Préfecture d'Agadir-Idaoutanane Rural",
                            "Préfecture d'Agadir-Idaoutanane Ensemble"],
                "Taux de pauvreté 2014": [0.39, 10.09, 26.2, 6.84, 6.91, 6.83, 4.64, 4.3, 9.76, 13.16, 4.9, 9.7, 5.9,
                                          5.41,
                                          17.02, 1.33, 8.53, 2.44],
                "Taux de vulnérabilité 2014": [3.1, 22.98, 21.76, 12.98, 20.34, 19.31, 13.15, 14.98, 23.04, 26.55,
                                               16.01, 24.25,
                                               16.51, 15.56, 31.41, 4.78, 20.75, 7.24]
            }
        }


        # --- FONCTIONS ---
        @st.cache_data
        def load_shapefile(path):
            try:
                return gpd.read_file(path)
            except Exception as e:
                st.error(f"Erreur lors du chargement du fichier {path} : {e}")
                return None


        def nettoyer_nom(nom):
            if isinstance(nom, str):
                return nom.lower().replace('(m)', '').replace('(ac)', '').replace('-', ' ').replace("'", ' ').strip()
            return nom


        # --- TITRE ---
        st.markdown(
            "<h3 style='text-align: center; color: #9292a8;'>Analyse de la Pauvreté par Commune (Souss-Massa, 2014)</h3>",
            unsafe_allow_html=True)
        st.write("")

        # --- FILTRES ---
        indicateur_choisi = st.selectbox(
            "Choisissez un indicateur à visualiser :",
            ["Taux de pauvreté 2014", "Taux de vulnérabilité 2014"],
            label_visibility="collapsed"
        )
        st.write("")

        # --- PRÉPARATION DES DONNÉES ---
        liste_df = []
        for province, data in pauvrete_data.items():
            df_temp = pd.DataFrame(data)
            df_temp["Province"] = province
            df_temp = df_temp[~df_temp["Commune"].str.contains("Province de")]
            liste_df.append(df_temp)

        df_stats = pd.concat(liste_df, ignore_index=True)

        # --- CHARGEMENT ET FUSION ---
        shapefile_path = "mar_admbnda_adm3_hcp_20230925/mar_admbnda_adm3_hcp_20230925.shp"
        gdf_communes = load_shapefile(shapefile_path)

        if gdf_communes is not None:
            df_stats['join_key'] = df_stats['Commune'].apply(nettoyer_nom)
            gdf_communes['join_key'] = gdf_communes['ADM3_FR'].apply(nettoyer_nom)

            commune_name_mapping = {
                "belfaa centre": "belfaa", "massa centre": "massa", "ait amira centre": "ait amira",
                "sidi bibi centre": "sidi bibi", "drargua centre": "drarga", "aourir centre": "aourir",
                "aqsri": "aqesri"
            }
            df_stats['join_key'] = df_stats['join_key'].replace(commune_name_mapping)
            gdf_merged = gdf_communes.merge(df_stats, on='join_key', how='inner')

            # --- BANNIÈRE KPI ---
            if not gdf_merged.empty:
                valeurs = gdf_merged[indicateur_choisi]
                min_val = valeurs.min()
                max_val = valeurs.max()
                moy_val = valeurs.mean()

                min_commune = gdf_merged.loc[valeurs.idxmin()]
                max_commune = gdf_merged.loc[valeurs.idxmax()]

                st.markdown(f"""
                <div class="kpi-banner">
                    <div class="kpi-box">
                        <span class="kpi-label">Taux le plus bas</span>
                        <span class="kpi-value">{min_val:.1f}%</span>
                        <span class="kpi-subvalue">{min_commune['Commune']}</span>
                    </div>
                    <div class="kpi-box">
                        <span class="kpi-label">Moyenne Régionale</span>
                        <span class="kpi-value">{moy_val:.1f}%</span>
                        <span class="kpi-subvalue">Sur toutes les communes analysées</span>
                    </div>
                    <div class="kpi-box">
                        <span class="kpi-label">Taux le plus élevé</span>
                        <span class="kpi-value">{max_val:.1f}%</span>
                        <span class="kpi-subvalue">{max_commune['Commune']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                st.markdown("---")

                # --- CARTE ET GRAPHIQUE ---
                col1, col2 = st.columns([3, 2])

                with col1:
                    fig_map = px.choropleth_mapbox(
                        gdf_merged,
                        geojson=gdf_merged.geometry,
                        locations=gdf_merged.index,
                        color=indicateur_choisi,
                        hover_name="Commune",
                        hover_data={"Province": True, indicateur_choisi: ':.2f'},
                        mapbox_style="open-street-map",  # <-- MODIFIÉ ICI pour une carte plus détaillée
                        center={"lat": 30.2, "lon": -9.0},
                        zoom=6.5,
                        opacity=0.75,  # Un peu plus transparent pour mieux voir la carte en dessous
                        color_continuous_scale="YlOrRd"
                    )
                    fig_map.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, height=600)
                    st.plotly_chart(fig_map, use_container_width=True)

                with col2:
                    df_sorted = gdf_merged.sort_values(by=indicateur_choisi, ascending=False)
                    fig_bar = px.bar(
                        df_sorted.head(25),
                        x=indicateur_choisi,
                        y='Commune',
                        orientation='h',
                        text_auto='.1f',
                        color=indicateur_choisi,
                        color_continuous_scale="YlOrRd"
                    )
                    fig_bar.update_layout(
                        yaxis={'categoryorder': 'total ascending'},
                        margin={"r": 0, "t": 30, "l": 0, "b": 0},
                        height=600,
                        showlegend=False,
                        xaxis_title=indicateur_choisi,
                        yaxis_title=""
                    )
                    fig_bar.update_traces(texttemplate='%{x:.1f}%', textposition='outside')
                    st.plotly_chart(fig_bar, use_container_width=True)

            else:
                st.warning(
                    "Aucune donnée géographique n'a pu être fusionnée avec les statistiques. Vérifiez les noms des communes.")

        else:
            st.warning("Impossible de charger le shapefile. Vérifiez le chemin et réessayez.")
################ taaaaaaaabbbb 3


elif st.session_state.page == "Generateur Rapport & statistiques":
    # =========================================================
    # GÉNÉRATEUR UNIVERSEL DE RAPPORTS PDF (PRO)
    # - Pas de prévision (uniquement analyse + comparaison + conclusion)
    # - Table des matières professionnelle (avec numéros de pages)
    # - Graphiques exportés via Matplotlib (stable sur Streamlit Cloud)
    # - Fonctionne avec n'importe quel Excel (mapping colonnes génériques)
    # =========================================================

    import os
    import re
    import numpy as np
    import pandas as pd
    import streamlit as st
    import plotly.express as px
    import matplotlib.pyplot as plt

    from fpdf import FPDF
    from datetime import datetime

    # -------------------------
    # UI HEADER
    # -------------------------
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
        <style>
        .block-container { padding: 0; margin: 0; max-width: 100%; }
        .full-width-bar{
            width:100%; background:#1E293B; padding:14px 18px;
            display:flex; justify-content:space-between; align-items:center; box-sizing:border-box;
        }
        .bar-logo{ font-family:'Playfair Display',serif; color:white; font-size:22px; font-weight:900; }
        .bar-tag{ color:#CBD5E1; font-size:13px; font-weight:600; }

        [data-testid="stExpander"] summary {
            background-color:#1E293B !important; color:white !important; border-radius:6px;
        }
        [data-testid="stExpander"] .streamlit-expanderContent{
            background:#FFFFFF; border:1px solid #E6EAF1; border-top:none;
            border-radius:0 0 6px 6px; padding-top:16px;
        }
        </style>

        <div class="full-width-bar">
            <div>
              <div class="bar-logo">Axiora Data</div>
              <div class="bar-tag">Générateur de rapports PDF (analyse + comparaison + conclusion)</div>
            </div>
        </div>
        <div style="height: 14px;"></div>
    """, unsafe_allow_html=True)

    col11, col22, col33 = st.columns([0.12, 1, 0.12])
    with col22:

        # =========================================================
        # HELPERS (génériques)
        # =========================================================
        def safe_filename(s: str) -> str:
            s = (s or "").strip().lower()
            s = re.sub(r"[^a-z0-9_\-]+", "_", s)
            s = re.sub(r"_+", "_", s).strip("_")
            return s or "rapport"

        def prepare_generic_data(df, group_idx, item_idx, value_idx):
            """
            Retour: df_clean avec colonnes Group, Item, Value
            - Group : catégorie (ex: région, segment, produit, type...)
            - Item  : élément (optionnel)
            - Value : numérique
            """
            cols = [group_idx, value_idx] if item_idx is None else [group_idx, item_idx, value_idx]
            df_selected = df.iloc[:, cols].copy()

            if item_idx is None:
                df_selected.columns = ["Group", "Value"]
                df_selected["Item"] = df_selected["Group"].astype(str)
            else:
                df_selected.columns = ["Group", "Item", "Value"]

            df_selected["Group"] = df_selected["Group"].astype(str).str.strip()
            df_selected["Item"] = df_selected["Item"].astype(str).str.strip()
            df_selected["Value"] = pd.to_numeric(df_selected["Value"], errors="coerce")

            df_selected = df_selected.dropna(subset=["Group", "Item", "Value"])

            # filtrage générique des totaux
            summary_keywords = ["total", "ensemble", "all", "sum", "moyenne", "average", "subtotal"]
            mask_summary = df_selected["Item"].str.lower().str.contains("|".join(summary_keywords), na=False)
            df_selected = df_selected[~mask_summary].copy()

            return df_selected

        def fmt_num(x):
            try:
                x = float(x)
                if abs(x) >= 1000:
                    return f"{x:,.2f}".replace(",", " ")
                return f"{x:.2f}"
            except:
                return str(x)

        def describe_table_str(series: pd.Series) -> str:
            d = series.describe()
            lines = []
            for k in ["count", "mean", "std", "min", "25%", "50%", "75%", "max"]:
                if k in d.index:
                    lines.append(f"{k:>6} : {fmt_num(d[k])}")
            return "\n".join(lines)

        def group_summary_table(df_clean: pd.DataFrame) -> pd.DataFrame:
            g = (
                df_clean.groupby("Group")["Value"]
                .agg(["count", "mean", "min", "max"])
                .sort_values("mean", ascending=False)
                .reset_index()
            )
            g["mean"] = g["mean"].round(2)
            g["min"] = g["min"].round(2)
            g["max"] = g["max"].round(2)
            return g

        def top_items_table(df_clean: pd.DataFrame, top_n=10) -> pd.DataFrame:
            t = df_clean.sort_values("Value", ascending=False).head(top_n).copy()
            t["Value"] = t["Value"].round(2)
            return t[["Group", "Item", "Value"]]

        def bottom_items_table(df_clean: pd.DataFrame, bottom_n=10) -> pd.DataFrame:
            b = df_clean.sort_values("Value", ascending=True).head(bottom_n).copy()
            b["Value"] = b["Value"].round(2)
            return b[["Group", "Item", "Value"]]

        # =========================================================
        # CHARTS (Matplotlib -> PNG stable)
        # =========================================================
        def save_chart_top_items(df_clean: pd.DataFrame, out_path: str, top_n=20):
            df_plot = df_clean.sort_values("Value", ascending=False).head(int(top_n)).copy()
            if df_plot.empty:
                return None

            labels = [f"{it} ({gr})" for gr, it in zip(df_plot["Group"], df_plot["Item"])]

            plt.figure(figsize=(12, 6))
            plt.bar(range(len(df_plot)), df_plot["Value"].values)
            plt.xticks(range(len(df_plot)), labels, rotation=65, ha="right", fontsize=8)
            plt.title(f"Top {top_n} items (Value)")
            plt.tight_layout()

            os.makedirs(os.path.dirname(out_path), exist_ok=True)
            plt.savefig(out_path, dpi=200)
            plt.close()
            return out_path

        def save_chart_group_means(df_clean: pd.DataFrame, out_path: str, top_g=15):
            df_g = group_summary_table(df_clean).head(int(top_g))
            if df_g.empty:
                return None

            plt.figure(figsize=(10.5, 5.5))
            plt.barh(df_g["Group"], df_g["mean"].values)
            plt.gca().invert_yaxis()
            plt.title(f"Moyenne par groupe (Top {top_g})")
            plt.xlabel("Moyenne (Value)")
            plt.tight_layout()

            os.makedirs(os.path.dirname(out_path), exist_ok=True)
            plt.savefig(out_path, dpi=200)
            plt.close()
            return out_path

        # =========================================================
        # PDF CLASS (TOC avec numéros de page)
        # =========================================================
        class PDF(FPDF):
            def __init__(self):
                super().__init__()
                self.toc = []  # [{"title":..., "page":...}]
                self.set_auto_page_break(auto=True, margin=14)

            def header(self):
                self.set_font("Helvetica", "B", 10)
                self.set_text_color(80, 80, 80)
                self.cell(0, 8, getattr(self, "title", ""), 0, 1, "R")
                self.ln(1)
                self.set_text_color(0, 0, 0)

            def footer(self):
                self.set_y(-14)
                self.set_font("Helvetica", "I", 8)
                self.set_text_color(120, 120, 120)
                self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")
                self.set_text_color(0, 0, 0)

            def safe(self, s):
                return (s or "").encode("latin-1", "replace").decode("latin-1")

            def h1(self, text):
                self.set_font("Helvetica", "B", 16)
                self.multi_cell(0, 8, self.safe(text))
                self.ln(1)

            def h2(self, text):
                self.set_font("Helvetica", "B", 12)
                self.multi_cell(0, 6.5, self.safe(text))
                self.ln(1)

            def p(self, text):
                self.set_font("Helvetica", "", 11)
                self.multi_cell(0, 6, self.safe(text))
                self.ln(1)

            def bullets(self, items):
                self.set_font("Helvetica", "", 11)
                for it in items:
                    self.multi_cell(0, 6, self.safe(f"• {it}"))
                self.ln(1)

            def codeblock(self, text):
                self.set_font("Courier", "", 8)
                text = self.safe(text)
                self.multi_cell(0, 4.5, text)
                self.set_font("Helvetica", "", 11)
                self.ln(1)

            def add_image(self, path, width=180):
                if path and os.path.exists(path):
                    self.image(path, w=width)
                    self.ln(4)

            def add_toc_entry(self, title):
                self.toc.append({"title": title, "page": self.page_no()})

        def df_to_text_table(df: pd.DataFrame, max_rows=40) -> str:
            df2 = df.copy()
            if len(df2) > max_rows:
                df2 = df2.head(max_rows)
            return df2.to_string(index=False)

        # =========================================================
        # REPORT CONTENT (structure pro)
        # =========================================================
        def build_report_sections(df_clean, objective, top_n_items=10, top_n_chart=20, top_g_chart=15):
            # Stats globales
            n_rows = len(df_clean)
            n_groups = df_clean["Group"].nunique()
            n_items = df_clean["Item"].nunique()

            max_row = df_clean.loc[df_clean["Value"].idxmax()]
            min_row = df_clean.loc[df_clean["Value"].idxmin()]
            mean_val = float(df_clean["Value"].mean())
            std_val = float(df_clean["Value"].std()) if n_rows > 1 else 0.0

            # Tables
            group_tab = group_summary_table(df_clean)
            top_tab = top_items_table(df_clean, top_n=top_n_items)
            bottom_tab = bottom_items_table(df_clean, bottom_n=top_n_items)

            # Insights simples (génériques)
            gap = float(max_row["Value"] - min_row["Value"])
            dispersion = "faible" if std_val < (0.1 * abs(mean_val) + 1e-9) else "marquée"
            best_group = group_tab.iloc[0]["Group"] if not group_tab.empty else "N/A"

            executive_summary = (
                f"Objectif : {objective}\n"
                f"Données analysées : {n_rows} lignes, {n_groups} groupes, {n_items} items.\n"
                f"Max : {max_row['Item']} ({max_row['Group']}) = {fmt_num(max_row['Value'])} | "
                f"Min : {min_row['Item']} ({min_row['Group']}) = {fmt_num(min_row['Value'])}\n"
                f"Moyenne : {fmt_num(mean_val)} | Écart-type : {fmt_num(std_val)} | Écart max-min : {fmt_num(gap)}\n"
                f"Groupe le plus performant (moyenne) : {best_group}"
            )

            sections = [
                {
                    "title": "1. Contexte & Objectif",
                    "body": (
                        "Ce rapport est généré automatiquement à partir d’un fichier Excel fourni par l’utilisateur. "
                        "Le contenu est construit dynamiquement selon les colonnes sélectionnées (Groupe / Élément / Valeur)."
                    ),
                    "bullets": [
                        f"Objectif : {objective}",
                        "Approche : nettoyage + statistiques descriptives + comparaisons",
                        "Sorties : tableaux synthèse + graphiques + conclusion"
                    ],
                },
                {
                    "title": "2. Données & Nettoyage",
                    "body": (
                        "Le pipeline standardise les colonnes en (Group, Item, Value). "
                        "La colonne Value est convertie en numérique et les lignes non exploitables sont supprimées. "
                        "Les lignes de type total/ensemble (si présentes) sont ignorées."
                    ),
                    "bullets": [
                        f"Lignes conservées : {n_rows}",
                        f"Groupes uniques : {n_groups}",
                        f"Items uniques : {n_items}",
                    ],
                },
                {
                    "title": "3. Analyse Descriptive",
                    "body": "Statistiques de base calculées sur la colonne Value :",
                    "table": describe_table_str(df_clean["Value"]),
                },
                {
                    "title": "4. Comparaison entre groupes",
                    "body": (
                        "Synthèse par groupe : nombre d’observations, moyenne, min et max. "
                        "Cette section sert à comparer rapidement les catégories (Group) sur l’indicateur (Value)."
                    ),
                    "table": df_to_text_table(group_tab, max_rows=40),
                },
                {
                    "title": "5. Items extrêmes (Top / Bottom)",
                    "body": (
                        "Liste des items les plus élevés et les plus faibles. "
                        "Utile pour identifier rapidement les zones/segments/produits dominants ou en retard."
                    ),
                    "bullets": [
                        "Top : items à forte valeur (priorités / points forts).",
                        "Bottom : items à faible valeur (zones à investiguer / points faibles)."
                    ],
                    "table": "TOP (valeurs les plus élevées)\n"
                             + df_to_text_table(top_tab, max_rows=top_n_items)
                             + "\n\nBOTTOM (valeurs les plus faibles)\n"
                             + df_to_text_table(bottom_tab, max_rows=top_n_items),
                },
                {
                    "title": "6. Synthèse & Conclusion",
                    "body": (
                        "Conclusion basée sur les constats descriptifs et comparatifs. "
                        "Elle indique où se situent les écarts et comment exploiter ces résultats."
                    ),
                    "bullets": [
                        f"Hétérogénéité : dispersion {dispersion} (écart-type vs moyenne).",
                        f"Écart max-min : {fmt_num(gap)} → amplitude des différences à expliquer.",
                        f"Groupe leader (moyenne) : {best_group} → benchmark.",
                        "Recommandation : compléter avec des variables explicatives (contexte, ressources, profils) pour interpréter les écarts.",
                    ],
                },
            ]

            # Graphiques à intégrer au PDF (paths calculés ailleurs)
            charts_meta = {
                "top_items_chart_n": int(top_n_chart),
                "top_groups_chart_n": int(top_g_chart),
                "executive_summary": executive_summary
            }
            return sections, charts_meta

        # =========================================================
        # PDF REPORT CREATION (TOC avec pages)
        # =========================================================
        def create_pdf_report(report_title, author, organization, objective, df_clean, charts_paths, sections, executive_summary):
            """
            charts_paths = {"top_items": "...png", "group_means": "...png"}
            """
            pdf = PDF()
            pdf.title = report_title

            # --- Cover ---
            pdf.add_page()
            pdf.set_font("Helvetica", "B", 26)
            pdf.multi_cell(0, 12, pdf.safe(report_title), 0, "C")
            pdf.ln(6)

            pdf.set_font("Helvetica", "", 13)
            pdf.multi_cell(0, 7, pdf.safe(f"Auteur : {author}"), 0, "C")
            pdf.multi_cell(0, 7, pdf.safe(f"Organisation : {organization}"), 0, "C")
            pdf.multi_cell(0, 7, pdf.safe(f"Date : {datetime.now().strftime('%d/%m/%Y')}"), 0, "C")
            pdf.ln(10)

            pdf.h2("Executive Summary")
            pdf.codeblock(executive_summary)

            # --- Table des matières placeholder ---
            pdf.add_page()
            toc_page = pdf.page_no()
            pdf.h1("Table des matières")
            pdf.p("Génération en cours...")

            # --- Content sections ---
            for sec in sections:
                pdf.add_page()
                pdf.add_toc_entry(sec["title"])

                pdf.h1(sec["title"])
                if sec.get("body"):
                    pdf.p(sec["body"])
                if sec.get("bullets"):
                    pdf.bullets(sec["bullets"])
                if sec.get("table"):
                    pdf.h2("Table / Résultats")
                    pdf.codeblock(sec["table"])

                # Insertion de figures dans les sections pertinentes (propre)
                if sec["title"].startswith("4.") and charts_paths.get("group_means"):
                    pdf.h2("Figure — Moyennes par groupe")
                    pdf.add_image(charts_paths["group_means"], width=180)

                if sec["title"].startswith("5.") and charts_paths.get("top_items"):
                    pdf.h2("Figure — Top items")
                    pdf.add_image(charts_paths["top_items"], width=180)

            # --- Rebuild TOC with page numbers ---
            # Sauvegarde le contenu actuel dans une string, puis on re-génère proprement
            # Astuce FPDF: on ne peut pas modifier une page déjà écrite facilement,
            # donc on régénère un 2e PDF final avec TOC correcte.
            final_pdf = PDF()
            final_pdf.title = report_title

            # Cover
            final_pdf.add_page()
            final_pdf.set_font("Helvetica", "B", 26)
            final_pdf.multi_cell(0, 12, final_pdf.safe(report_title), 0, "C")
            final_pdf.ln(6)

            final_pdf.set_font("Helvetica", "", 13)
            final_pdf.multi_cell(0, 7, final_pdf.safe(f"Auteur : {author}"), 0, "C")
            final_pdf.multi_cell(0, 7, final_pdf.safe(f"Organisation : {organization}"), 0, "C")
            final_pdf.multi_cell(0, 7, final_pdf.safe(f"Date : {datetime.now().strftime('%d/%m/%Y')}"), 0, "C")
            final_pdf.ln(10)

            final_pdf.h2("Executive Summary")
            final_pdf.codeblock(executive_summary)

            # TOC correct
            final_pdf.add_page()
            final_pdf.h1("Table des matières")

            final_pdf.set_font("Helvetica", "", 11)
            for entry in pdf.toc:
                # format: Title .......... page
                title = entry["title"]
                page = entry["page"]  # pages in pdf (cover + toc placeholder + content)
                # On doit recalculer car final_pdf a 2 pages (cover+toc) avant contenu,
                # alors que pdf avait cover + toc placeholder = 2 pages aussi. Même offset => OK.
                dots = "." * max(2, 70 - len(title))
                final_pdf.cell(0, 7, final_pdf.safe(f"{title} {dots} {page}"), 0, 1)

            # Content sections (replay)
            for sec in sections:
                final_pdf.add_page()
                final_pdf.h1(sec["title"])

                if sec.get("body"):
                    final_pdf.p(sec["body"])
                if sec.get("bullets"):
                    final_pdf.bullets(sec["bullets"])
                if sec.get("table"):
                    final_pdf.h2("Table / Résultats")
                    final_pdf.codeblock(sec["table"])

                if sec["title"].startswith("4.") and charts_paths.get("group_means"):
                    final_pdf.h2("Figure — Moyennes par groupe")
                    final_pdf.add_image(charts_paths["group_means"], width=180)

                if sec["title"].startswith("5.") and charts_paths.get("top_items"):
                    final_pdf.h2("Figure — Top items")
                    final_pdf.add_image(charts_paths["top_items"], width=180)

            return final_pdf.output(dest="S").encode("latin-1")

        # =========================================================
        # UI
        # =========================================================
        st.markdown("<h4 style='text-align:center;'>Générateur de Rapport Universel</h4>", unsafe_allow_html=True)

        with st.expander("Étape 1 : Informations du rapport", expanded=True):
            c1, c2 = st.columns(2)
            with c1:
                report_title = st.text_input("Titre du rapport", "Analyse de Données")
                author_name = st.text_input("Auteur(s)", "Généré automatiquement")
            with c2:
                organization = st.text_input("Organisation", "")
                objective = st.text_area("Objectif de l'étude", "Analyser la répartition d'un indicateur clé.")

        with st.expander("Étape 2 : Charger le fichier + mapping des colonnes", expanded=True):
            uploaded_file = st.file_uploader("Chargez votre fichier Excel", type=["xlsx"], label_visibility="collapsed")

            df_raw = None
            group_idx = item_idx = value_idx = None

            if uploaded_file is not None:
                df_raw = pd.read_excel(uploaded_file, header=None)
                st.markdown("**Aperçu (5 lignes) :**")
                st.dataframe(df_raw.head(5), use_container_width=True)

                col_options = [f"Colonne {i}" for i in range(len(df_raw.columns))]
                m1, m2, m3 = st.columns(3)

                with m1:
                    group_col = st.selectbox("Colonne Groupe (catégorie)", col_options, index=0)
                with m2:
                    item_col = st.selectbox("Colonne Élément (optionnelle)", ["Aucune"] + col_options, index=0)
                with m3:
                    value_col = st.selectbox("Colonne Valeur (numérique)", col_options, index=1 if len(col_options) > 1 else 0)

                group_idx = col_options.index(group_col)
                value_idx = col_options.index(value_col)
                item_idx = None if item_col == "Aucune" else col_options.index(item_col)

        with st.expander("Étape 3 : Générer le PDF (analyse uniquement)", expanded=True):
            if df_raw is None:
                st.info("Veuillez charger un fichier Excel pour activer la génération du rapport.")
            else:
                top_n_items = st.slider("Top / Bottom (table)", 5, 30, 10, step=1)
                top_n_chart = st.slider("Top N (graphique items)", 10, 50, 20, step=5)
                top_g_chart = st.slider("Top groupes (graphique moyennes)", 5, 30, 15, step=5)

                if st.button("Créer le PDF", type="primary", use_container_width=True):
                    with st.spinner("Nettoyage, analyse, comparaison et génération du PDF..."):

                        df_clean = prepare_generic_data(df_raw, group_idx, item_idx, value_idx)

                        if df_clean.empty:
                            st.error("Impossible d'analyser : vérifiez vos colonnes (valeur numérique requise).")
                        else:
                            # Aperçu UI
                            st.success("Données nettoyées (aperçu) :")
                            st.dataframe(df_clean.head(10), use_container_width=True)

                            # Graph UI (Plotly)
                            fig_ui = px.bar(
                                df_clean.sort_values("Value", ascending=False).head(int(top_n_chart)),
                                x="Item",
                                y="Value",
                                color="Group",
                                title=f"Top {top_n_chart} items (Value)"
                            )
                            st.plotly_chart(fig_ui, use_container_width=True)

                            # Export charts for PDF
                            os.makedirs("temp_plots", exist_ok=True)
                            p_top_items = save_chart_top_items(df_clean, "temp_plots/top_items.png", top_n=top_n_chart)
                            p_group_means = save_chart_group_means(df_clean, "temp_plots/group_means.png", top_g=top_g_chart)

                            sections, meta = build_report_sections(
                                df_clean=df_clean,
                                objective=objective,
                                top_n_items=top_n_items,
                                top_n_chart=top_n_chart,
                                top_g_chart=top_g_chart
                            )

                            charts_paths = {"top_items": p_top_items, "group_means": p_group_means}

                            pdf_bytes = create_pdf_report(
                                report_title=report_title,
                                author=author_name,
                                organization=organization,
                                objective=objective,
                                df_clean=df_clean,
                                charts_paths=charts_paths,
                                sections=sections,
                                executive_summary=meta["executive_summary"]
                            )

                            st.session_state.pdf_bytes = pdf_bytes
                            st.session_state.report_title = report_title
                            st.success("PDF généré avec succès !")

        # Download
        if "pdf_bytes" in st.session_state:
            fname = safe_filename(st.session_state.get("report_title", "rapport"))
            ts = datetime.now().strftime("%Y%m%d_%H%M")
            st.download_button(
                label="⬇ Télécharger le Rapport PDF",
                data=st.session_state.pdf_bytes,
                file_name=f"{fname}_{ts}.pdf",
                mime="application/pdf",
                use_container_width=True
            )


















































elif st.session_state.page == "assistant axiora data":
    st.markdown("<br>", unsafe_allow_html=True)

    st.set_page_config(layout="wide")

    st.markdown("""
        <style>
        .block-container {
            padding: 0;
            margin: 0;
            max-width: 100%;
        }

        .full-width-bar {
            width: 100%;
            background-color: #1E293B;
            padding: 15px 20px;  /* réduit les paddings */
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-sizing: border-box;
        }

        .bar-logo {
            font-family: 'Playfair Display', serif;
            color: white;
            font-size: 24px;   /* légèrement réduit */
            font-weight: 900;
        }

        .bar-menu {
            display: flex;
            gap: 10px;           /* réduit l’espace entre liens */
            max-width: 70%;       /* limite la largeur du menu pour éviter le dépassement */
            overflow-x: auto;     /* permet le défilement si écran trop petit */
        }

        .bar-menu a {
            color: white;
            text-decoration: none;
            font-size: 14px;      /* réduit la taille du texte */
            font-weight: 600;
            white-space: nowrap;  /* empêche le texte de passer à la ligne */
        }

        .bar-menu a:hover {
            color: #60A5FA;
        }

        .bar-menu .button {
            background-color: #3b82f6;
            padding: 5px 10px;
            border-radius: 6px;
            font-size: 14px;
            font-weight: 600;
        }

        .bar-menu .button:hover {
            background-color: #2563eb;
        }
        </style>

        <div class="full-width-bar">
            <div class="bar-logo">Axiora Data</div>
            <div class="bar-menu">
                <a href="#">App Marketing Agency</a>
                <a href="#">ASO Agency</a>
                <a href="#">Glossary</a>
                <a href="#">Data</a>
                <a href="#">ASO Tools</a>
                <a href="#" class="button">Read Blog</a>
            </div>
        </div>

        <div style="height: 60px;"></div>
        """, unsafe_allow_html=True)

    # ====== CONFIGURATION GEMINI ======
    col11, col22, col33 = st.columns([0.1, 1, 0.1])
    with col22:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-2.5-flash')

        # Passer en mode large (full width)
        st.set_page_config(layout="wide")

        # ====== FONCTION : RÉPONSE IA ======
        if "messages" not in st.session_state:
            st.session_state.messages = []
        if "pinned" not in st.session_state:
            st.session_state.pinned = []
        if "open_menu" not in st.session_state:
            st.session_state.open_menu = None


        # ====== Fonction : Réponse IA ======
        def response_to_query(query: str) -> str:
            hcp_definition = "Le HCP (Haut-Commissariat au Plan) est l'institution nationale chargée de la production, de l'analyse et de la diffusion des statistiques officielles au Maroc. Il joue un rôle crucial dans la planification économique et sociale en fournissant des données fiables sur des sujets tels que la population, l'emploi, l'économie, et le niveau de vie."

            data_json = json.dumps(hcp_data, indent=2, ensure_ascii=False)
            prompt = f"""
                    Tu es un assistant expert en données statistiques du HCP.

                    Si la question concerne la définition ou le rôle du HCP, réponds avec la définition suivante :
                    "{hcp_definition}"

                    Si la question porte sur des données chiffrées, réponds UNIQUEMENT à partir des données suivantes (en milliers sauf mention contraire).
                    Données HCP :
                    {data_json}

                    Si la question est hors de ces deux contextes, réponds que tu ne peux répondre qu'avec les données fournies.

                    Question : {query}
                    """
            try:
                # L'appel à generate_content gérera automatiquement l'appel à l'outil si nécessaire
                resp = model.generate_content(prompt)
                return resp.text
            except Exception as e:
                # Gérer les erreurs, par exemple si l'outil n'a pas pu être utilisé
                return f"Désolé, une erreur est survenue lors de la recherche. Erreur: {e}"


        # ====== CSS ======
        st.markdown("""
            <style>
            .user-msg {
                text-align: right;
                background-color: #919b9c;
                padding: 10px 15px;
                border-radius: 12px;
                max-width: 70%;
                margin: 5px 0 5px auto;
            }
            .assistant-msg {
                text-align: left;
                background-color: #E5E7EB;
                padding: 10px 15px;
                border-radius: 12px;
                max-width: 70%;
                margin: 5px 0;
            }
            .sidebar {
                border-left: 1px solid #E5E7EB;
                padding-left: 15px;
                height: 100vh;
            }
            .sidebar-item {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 6px 0;
                font-size: 14px;
            }
            .sidebar-item:hover {
                background-color: #F9FAFB;
                border-radius: 6px;
            }
            .dots-btn {
                background: none;
                border: none;
                font-size: 16px;
                cursor: pointer;
            }
            .menu-box {
                background-color: #FFF;
                border: 1px solid #E5E7EB;
                border-radius: 6px;
                padding: 5px;
                font-size: 13px;
                position: relative;
                z-index: 10;
            }
            .menu-item {
                padding: 4px 6px;
                cursor: pointer;
            }
            .menu-item:hover {
                background-color: #F3F4F6;
                border-radius: 4px;
            }
            </style>
            """, unsafe_allow_html=True)

        # ====== Layout ======

        if len(st.session_state.messages) == 0:
            st.markdown("""
                    <div style="
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 60vh;
                        font-size: 22px;
                        color: #4B5563;
                        text-align: center;
                    ">
                        <b>Qu’est-ce qui vous intéresse à savoir à propos de HCP ?</b>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            for i, m in enumerate(st.session_state.messages):
                role_class = "user-msg" if m["role"] == "user" else "assistant-msg"
                st.markdown(f"<div class='{role_class}'>{m['content']}</div>", unsafe_allow_html=True)

        with st.container():
            user_query = st.chat_input("Posez votre question sur les données HCP :")
            if user_query:
                st.session_state.messages.append({"role": "user", "content": user_query})
                with st.spinner("Recherche dans les données..."):
                    ai_response = response_to_query(user_query)
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
                st.rerun()





elif st.session_state.page == "Aide & contact":
    st.markdown("<br>", unsafe_allow_html=True)

    st.set_page_config(layout="wide")

    st.markdown("""
        <style>
        .block-container {
            padding: 0;
            margin: 0;
            max-width: 100%;
        }

        .full-width-bar {
            width: 100%;
            background-color: #1E293B;
            padding: 15px 20px;  /* réduit les paddings */
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-sizing: border-box;
        }

        .bar-logo {
            font-family: 'Playfair Display', serif;
            color: white;
            font-size: 24px;   /* légèrement réduit */
            font-weight: 900;
        }

        .bar-menu {
            display: flex;
            gap: 10px;           /* réduit l’espace entre liens */
            max-width: 70%;       /* limite la largeur du menu pour éviter le dépassement */
            overflow-x: auto;     /* permet le défilement si écran trop petit */
        }

        .bar-menu a {
            color: white;
            text-decoration: none;
            font-size: 14px;      /* réduit la taille du texte */
            font-weight: 600;
            white-space: nowrap;  /* empêche le texte de passer à la ligne */
        }

        .bar-menu a:hover {
            color: #60A5FA;
        }

        .bar-menu .button {
            background-color: #3b82f6;
            padding: 5px 10px;
            border-radius: 6px;
            font-size: 14px;
            font-weight: 600;
        }

        .bar-menu .button:hover {
            background-color: #2563eb;
        }
        </style>

        <div class="full-width-bar">
            <div class="bar-logo">Axiora Data</div>
            <div class="bar-menu">
                <a href="#">App Marketing Agency</a>
                <a href="#">ASO Agency</a>
                <a href="#">Glossary</a>
                <a href="#">Data</a>
                <a href="#">ASO Tools</a>
                <a href="#" class="button">Read Blog</a>
            </div>
        </div>

        <div style="height: 60px;"></div>
        """, unsafe_allow_html=True)



    col11, col22, col33 = st.columns([0.1, 1, 0.1])
    with col22:
        import streamlit as st

        st.markdown("""
        <style>
            /* --- VARIABLES DE COULEUR --- */
            :root {
                --fond-principal: #FFFFFF;
                --texte-principal: #0E1117;
                --texte-secondaire: #555555;
                --bleu-accent: #0068C9;
                --bleu-hover: #0055A4;
                --fond-bulle-arrondie: #303242; /* Nouvelle couleur de fond pour les bulles */
                --texte-bulle: #FFFFFF; /* Texte blanc pour les bulles */
            }

            /* --- STYLE GÉNÉRAL --- */
            .stApp {
                background-color: var(--fond-principal);
            }

            /* --- DIMINUTION DE LA TAILLE DES POLICES --- */
            /* Titres principaux */
            .st-emotion-cache-10trblm { /* st.header */
                font-size: 1.5em;
            }
            .st-emotion-cache-1outpf7 { /* st.subheader */
                font-size: 1.15em;
            }

            /* Paragraphes et labels de formulaire */
            .stMarkdown p, .stTextInput label, .stTextArea label, .stButton > button {
                font-size: 0.9rem;
            }

            /* Champs de saisie */
            .stTextInput > div > div > input,
            .stTextArea > div > div > textarea {
                font-size: 0.9rem;
            }
            /* Correction de la couleur des labels dans la bulle */
            .bulle-arrondie label {
                color: var(--texte-bulle) !important;
            }

            /* --- AUTRES STYLES --- */
            /* Titres */
            h3, h4 {
                color: var(--texte-principal) !important;
                font-weight: 600;
            }

            /* Style des bulles avec fond arrondi */
            .bulle-arrondie {
                background-color: var(--fond-bulle-arrondie);
                color: var(--texte-bulle);
                padding: 20px;
                border-radius: 15px; /* Pour les extrémités arrondies */
                margin-bottom: 20px;
                display: flex;
                flex-direction: column;
            }
            /* Assurer que les colonnes ont la même hauteur */
            .st-emotion-cache-pk-0 {
                display: flex;
            }
            .st-emotion-cache-1c7y3x2, .st-emotion-cache-q8s10s {
                height: 100%;
            }

            .bulle-arrondie h3, .bulle-arrondie h1, .bulle-arrondie p, .bulle-arrondie strong, .bulle-arrondie b {
                color: var(--texte-bulle) !important; /* S'assurer que tout le texte est blanc */
            }
            .bulle-arrondie input, .bulle-arrondie textarea {
                background-color: #404252 !important; /* Couleur de fond des champs de saisie */
                color: var(--texte-bulle) !important;
                border: 1px solid #55586B !important;
            }
            .bulle-arrondie button {
                background-color: var(--bleu-accent);
                color: #FFFFFF;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
            }
            .bulle-arrondie .st-emotion-cache-5rimss p {
                color: #FFFFFF !important;
            }

            /* Pied de page */
            .footer {
                text-align: center;
                padding-top: 40px;
                color: var(--texte-secondaire);
                font-size: 0.8rem;
            }
        </style>
        """, unsafe_allow_html=True)

        # --- HEADER ---
        st.markdown('<div class="bulle-arrondie">', unsafe_allow_html=True)
        st.header("Aide & Contact")
        st.markdown('</div>', unsafe_allow_html=True)
        st.write("---")

        # --- SECTIONS DE CONTENU EN COLONNES ---
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            <div class="bulle-arrondie">
                <h3>Notre Mission</h3>
                <p>
                Notre mission chez <strong>Axioradata</strong> est de rendre les données socio-économiques du Maroc accessibles et compréhensibles. Nous transformons les informations complexes du <strong>(HCP)</strong> en visualisations claires pour aider les décideurs et chercheurs  à explorer les dynamiques de notre pays.
                </p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div class="bulle-arrondie">
                <h3>Comment Utiliser Nos Dashboards</h3>
                <p>
                1. <strong>Choisissez un secteur</strong> dans le menu principal.<br>
                2. <strong>Utilisez les filtres</strong> (année, région, indicateur) pour affiner votre recherche.<br>
                3. <strong>Interagissez avec la carte</strong> en survolant les provinces pour obtenir des détails instantanés.<br>
                </p>
            </div>
            """, unsafe_allow_html=True)

        st.write("---")

        # --- SECTION CONTACT ---
        st.markdown('<div class="bulle-arrondie">', unsafe_allow_html=True)
        st.subheader("Contactez-nous")
        with st.form("contact_form", clear_on_submit=True):
            st.write(
                "<b>Une question ? Une suggestion ?</b><br>Remplissez le formulaire ci-dessous et nous vous répondrons dans les plus brefs délais.",
                unsafe_allow_html=True)

            name = st.text_input("Votre Nom", placeholder="Jean Dupont")
            email = st.text_input("Votre Email", placeholder="jean.dupont@email.com")
            subject = st.text_input("Sujet")
            message = st.text_area("Votre Message", height=120)

            submitted = st.form_submit_button("Envoyer le Message")

            if submitted:
                st.success("Merci ! Votre message a bien été envoyé.")
        st.markdown('</div>', unsafe_allow_html=True)

        # --- PIED DE PAGE ---
        st.markdown("""
        <div class="footer">
            <p>&copy; 2025 Axioradata. Tous droits réservés.</p>
            <p>Données fournies par le <strong>Haut-Commissariat au Plan (HCP)</strong> du Maroc.</p>
        </div>
        """, unsafe_allow_html=True)

else:
    st.markdown("<br>", unsafe_allow_html=True)

    st.set_page_config(layout="wide")

    st.markdown("""
        <style>
        .block-container {
            padding: 0;
            margin: 0;
            max-width: 100%;
        }

        .full-width-bar {
            width: 100%;
            background-color: #1E293B;
            padding: 15px 20px;  /* réduit les paddings */
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-sizing: border-box;
        }

        .bar-logo {
            font-family: 'Playfair Display', serif;
            color: white;
            font-size: 24px;   /* légèrement réduit */
            font-weight: 900;
        }

        .bar-menu {
            display: flex;
            gap: 10px;           /* réduit l’espace entre liens */
            max-width: 70%;       /* limite la largeur du menu pour éviter le dépassement */
            overflow-x: auto;     /* permet le défilement si écran trop petit */
        }

        .bar-menu a {
            color: white;
            text-decoration: none;
            font-size: 14px;      /* réduit la taille du texte */
            font-weight: 600;
            white-space: nowrap;  /* empêche le texte de passer à la ligne */
        }

        .bar-menu a:hover {
            color: #60A5FA;
        }

        .bar-menu .button {
            background-color: #3b82f6;
            padding: 5px 10px;
            border-radius: 6px;
            font-size: 14px;
            font-weight: 600;
        }

        .bar-menu .button:hover {
            background-color: #2563eb;
        }
        </style>

        <div class="full-width-bar">
            <div class="bar-logo">Axiora Data</div>
            <div class="bar-menu">
                <a href="#">App Marketing Agency</a>
                <a href="#">ASO Agency</a>
                <a href="#">Glossary</a>
                <a href="#">Data</a>
                <a href="#">ASO Tools</a>
                <a href="#" class="button">Read Blog</a>
            </div>
        </div>

        <div style="height: 60px;"></div>
        """, unsafe_allow_html=True)

    col_1, col_2, col_3 = st.columns([0.1, 1, 0.1])
    with col_2:

        new_image_path = r"assets/photo.png"
        hcp_image = Image.open(new_image_path)

        # --- Colonnes texte + image ---
        col_text, col_image = st.columns([1, 1])

        with col_text:
            st.markdown("""
                <div style="
                    display: flex;
                    flex-direction: column;
                    justify-content: center;   
                    height: 100%;              
                    color: #a3a8ad;
                    padding: 20px;
                    font-size: 24px;  /* réduit de 30px à 24px */
                    line-height: 1.6;   
                    text-align: justify;
                ">
                Boostez vos analyses avec la plateforme #1
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            st.markdown('<div class="title-pill">Expert en données socio-économiques</div>', unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            st.markdown("""
            <div style="
                display: flex;
                flex-direction: column;
                justify-content: center;   
                height: 100%;              
                color: black;
                padding: 20px;
                font-size: 16px;  /* réduit de 20px à 16px */
                line-height: 1.6;   
                text-align: justify;
            ">
            Axiora Data est une plateforme avancée d’analyse et de visualisation de données socio-économiques, spécialisée dans l’exploitation des statistiques officielles fournies par le Haut-Commissariat au Plan (HCP).<br><br> 
            Elle permet de collecter, traiter et interpréter les données relatives à divers indicateurs nationaux et régionaux tels que la pauvreté, le chômage, l’emploi, le niveau de vie, les prix ou la démographie.<br><br> 
            Grâce à des cartes interactives et des graphiques dynamiques, Axiora Data transforme les données brutes en informations claires, visuelles et exploitables, offrant aux utilisateurs une compréhension approfondie des tendances socio-économiques du Maroc.
            </div>
            """, unsafe_allow_html=True)

        with col_image:
            st.image(hcp_image, caption="Illustration d'information", use_container_width=True)

        st.markdown("<br><br>", unsafe_allow_html=True)

        ######### les 4 indice #######
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown('''
            <div class="card">
                <p style="font-size:20px;">3 020 431+</p>  <!-- réduit de 24px à 20px -->
                <h3 style="font-size:12px;">Utilisateurs</h3>  <!-- réduit de 14px à 12px -->
                <div class="arrow-up" style="font-size:12px;">&#9650; 5% ce mois</div>
            </div>
            ''', unsafe_allow_html=True)

        with col2:
            st.markdown('''
            <div class="card">
                <p style="font-size:20px;">350+</p>
                <h3 style="font-size:12px;">Données</h3>
                <div class="arrow-stable" style="font-size:12px;">&#9650;&#9660; stable</div>
            </div>
            ''', unsafe_allow_html=True)

        with col3:
            st.markdown('''
            <div class="card region">
                <p style="font-size:20px;">12</p>
                <h3 style="font-size:12px;">Régions</h3>
                <div class="arrow-down" style="font-size:12px;">&#9660; 1 depuis 2024</div>
            </div>
            ''', unsafe_allow_html=True)

        with col4:
            st.markdown('''
            <div class="card">
                <p style="font-size:20px;">6+</p>
                <h3 style="font-size:12px;">Indicateurs</h3>
                <div class="arrow-up" style="font-size:12px;">&#9650; 2 nouveaux</div>
            </div>
            ''', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        ########## les etape de hcp ########
        st.markdown("""
            <style>
                body {
                    background-color: #f5f8fe;
                    margin: 0;
                    padding: 0;
                }
                .hcp-band {
                    background-color: #e6ecf2;  /* Même couleur pour le titre et les étapes */
                    padding: 30px 0;  /* padding vertical seulement */
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    gap: 30px;
                    width: 100vw;  /* pleine largeur de la fenêtre */
                    margin-left: calc(-50vw + 50%); /* aligne le div avec le bord gauche */
                }
                .steps-container {
    display: flex;
    justify-content: center;  /* centre les étapes */
    gap: 40px;                 /* espace entre chaque étape */
    max-width: 1200px;         /* largeur max du contenu pour laisser des marges */
    margin: 0 auto;            /* centre le conteneur dans le fond gris */
    flex-wrap: nowrap;          /* empêche le passage à la ligne */
}
.step-item {
    text-align: center;
    padding: 15px 20px;
    flex: 1;  /* chaque étape prend un espace égal */
    max-width: 250px; /* limite la largeur de chaque étape */
}
                .step-number {
                    background-color: #1E293B;  /* Cercle bleu foncé */
                    color: white;
                    font-weight: bold;
                    border-radius: 50%;
                    width: 55px;
                    height: 55px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    margin: 0 auto 15px auto;
                    font-size: 18px;
                }
                .step-title {
                    font-weight: bold;
                    font-size: 16px;
                    margin-bottom: 5px;
                }
                .step-desc {
                    font-size: 14px;
                    color: #111;
                }
                .hcp-title {
                    font-size: 22px;
                    font-weight: bold;
                    color: #111;
                    text-align: center;
                }
                .hcp-subtitle {
                    font-size: 16px;
                    color: #111;
                    text-align: center;
                }
            </style>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="hcp-band">
            <div class="hcp-title">Workflow de traitement des données HCP</div>
            <div class="hcp-subtitle">Étapes de traitement des données HCP garantissant qualité et conformité.</div>
            <div class="steps-container">
                <div class="step-item">
                    <div class="step-number">1</div>
                    <div class="step-title">Collecte des données</div>
                    <div class="step-desc">Rassembler les données brutes HCP provenant de toutes les sources : enquêtes, logs et bases externes.</div>
                </div>
                <div class="step-item">
                    <div class="step-number">2</div>
                    <div class="step-title">Nettoyage des données</div>
                    <div class="step-desc">Supprimer les doublons, gérer les valeurs manquantes et standardiser les formats pour plus de cohérence.</div>
                </div>
                <div class="step-item">
                    <div class="step-number">3</div>
                    <div class="step-title">Analyse des données</div>
                    <div class="step-desc">Appliquer des méthodes statistiques et analytiques pour extraire des insights et tendances.</div>
                </div>
                <div class="step-item">
                    <div class="step-number">4</div>
                    <div class="step-title">Rapports & visualisation</div>
                    <div class="step-desc">Générer des rapports et tableaux de bord pour la prise de décision et le suivi de conformité.</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        ###############les indices ############

        st.markdown("""
        <div style="
            display: flex;
            justify-content: center;
            margin-top: 10px;
            margin-bottom: 10px;
        ">
            <div style="
                background-color: #a3a8ad;
                color: #ffffff;
                padding: 5px 12px;  
                border-radius: 40px; 
                font-size: 14px;    
                font-weight: 500;
                white-space: nowrap;
                line-height: 1.2;
                text-align: center;
            ">
                nos services
            </div>
        </div>
        """, unsafe_allow_html=True)

        # --- Titres et description plus petits ---
        st.markdown("""
        <div style="text-align:center; margin:20px 0;">
            <div style="color:#1E293B; font-size:20px; font-weight:800; font-family:'Playfair Display', serif; margin-bottom:8px;">
               Solutions complètes de données socio-économiques
            </div>
            <div style="color:#1E293B; font-size:14px; font-weight:500; font-family:'Roboto', sans-serif; max-width:700px; margin:0 auto; line-height:1.4;">
                Des services statistiques stratégiques, fiables et intégrés, conçus pour fournir des insights clairs sur les réalités sociales et économiques du Maroc
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # --- Données indices HCP ---
        indices = [
            ("Population",
             "Population totale et démographie : répartition par âge, sexe, densité, taux de croissance et migrations internes et internationales."),
            ("Santé",
             "Santé : taux de mortalité, espérance de vie, couverture médicale, accès aux hôpitaux et suivi des maladies chroniques et épidémiques."),
            ("Tourisme",
             "Tourisme : flux touristique national et international, fréquentation par région, revenus générés, et impact sur l’économie locale."),
            ("Enseignement",
             "Enseignement : taux de scolarisation, accès à l’éducation primaire, secondaire et universitaire, alphabétisation, et qualité des infrastructures."),
            ("Habitat",
             "Habitat : types de logement, conditions de vie, accès à l’eau, à l’électricité et à l’assainissement, urbanisation et logement social."),
            ("Finance",
             "Finance : revenus moyens, répartition des richesses, épargne, accès au crédit, investissements et indicateurs économiques régionaux."),
            ("Pauvreté",
             "Pauvreté : pourcentage de ménages vivant sous le seuil de pauvreté, disparités régionales, et suivi des programmes d’aide sociale."),
            ("Prix",
             "Prix : évolution des prix des biens et services, inflation, comparaison régionale, et impact sur le pouvoir d’achat des ménages."),
            ("Marché du travail",
             "Marché du travail : taux d’emploi, chômage, répartition sectorielle, salaires moyens, et insertion des jeunes et des diplômés.")
        ]

        # --- CSS pour les cartes plus petites ---
        st.markdown("""
        <style>
        .card {
            background-color: #1E293B;  
            border-radius: 12px;
            padding: 15px;
            text-align: center;
            box-shadow: 0 3px 8px rgba(0,0,0,0.1);
            margin-bottom: 15px;
            transition: transform 0.2s;
            color: #ffffff;
        }
        .card:hover { transform: translateY(-3px); }
        .card h3 { font-size: 16px; margin: 8px 0 4px 0; color: #a3a8ad; }
        .card p { font-size: 12px; color: #ffffff; text-align: center; }
        </style>
        """, unsafe_allow_html=True)

        # --- Affichage des cartes centrées avec gestion dynamique ---
        col_1, col_2, col_3 = st.columns([0.1, 1, 0.1])
        with col_2:
            chunk_size = 3  # nombre de cartes par ligne
            for i in range(0, len(indices), chunk_size):
                chunk = indices[i:i + chunk_size]
                cols = st.columns(len(chunk))  # crée exactement le nombre de colonnes nécessaire
                for col, (titre, desc) in zip(cols, chunk):
                    with col:
                        st.markdown(f'''
                            <div class="card">
                                <h3>{titre}</h3>
                                <p>{desc}</p>
                            </div>
                        ''', unsafe_allow_html=True)

        st.markdown("<br><br>", unsafe_allow_html=True)

        ############## question & reponces #############

        # --- Titre principal ---
        st.markdown("""
        <div style="
            display: flex;
            justify-content: center;
            margin-top: 20px;
            margin-bottom: 20px;
        ">
            <div style="
                background-color:#1E293B ;
                color: #ffffff;
                padding: 8px 16px;
                border-radius: 50px;          
                font-size: 27px;               
                font-weight: 700;
                white-space: nowrap;
                line-height: 1.2;
                text-align: center;
            ">
                Questions fréquentes sur Axiora & HCP
            </div>
        </div>
        """, unsafe_allow_html=True)

        # --- Sous-titre réduit ---
        st.markdown(
            "<h5 style='text-align:center;color:#1E293B; font-size:14px;'>Obtenez des réponses aux questions les plus courantes sur l'analyse et le traitement des données HCP avec Axiora.</h5>",
            unsafe_allow_html=True)
        col1, col2, col3 = st.columns([0.2, 1, 0.2])
        with col2:
            # --- Colonnes pour centrer le contenu ---
            # --- Données FAQ ---
            faq_data = [
                {
                    "question": "Qu'est-ce qu'Axiora Data ?",
                    "answer": "Axiora est une plateforme qui permet d'analyser et de traiter les données HCP et de les visualiser à l'aide de graphiques et cartes interactives."
                },
                {
                    "question": "Comment Axiora aide-t-il à traiter les données HCP ?",
                    "answer": "Axiora permet de nettoyer, organiser et analyser les données HCP, générer des insights et créer des visualisations claires pour la prise de décision."
                },
                {
                    "question": "Puis-je créer des graphiques personnalisés avec Axiora ?",
                    "answer": "Oui, Axiora offre des options pour créer des graphiques personnalisés afin de mieux représenter vos données et tendances HCP."
                },
                {
                    "question": "Axiora garantit-il la sécurité des données HCP ?",
                    "answer": "Oui, la plateforme respecte les normes de sécurité et confidentialité pour protéger toutes les données HCP traitées."
                }
            ]

            # --- CSS pour personnaliser les expanders ---
            st.markdown("""
            <style>
            /* Question (titre de l'expander) */
            div[data-testid="stExpander"] > div:first-child {
                font-size: 20px;
                font-weight: bold;
            }

            /* Réponse */
            div[data-testid="stExpander"] > div:nth-child(2) {
                font-size: 16px;
            }

            /* Ajouter un + à droite */
            div[data-testid="stExpander"] > div:first-child::after {
                content: "+";
                float: right;
                font-size: 20px;
                font-weight: bold;
                margin-left: 10px;
            }

            /* Optionnel : changer couleur du + lorsqu'on ouvre */
            div[data-testid="stExpander"][aria-expanded="true"] > div:first-child::after {
                content: "-";
                color: #0073e6; /* bleu */
            }
            </style>
            """, unsafe_allow_html=True)

            # --- Affichage des FAQ ---
            for faq in faq_data:
                with st.expander(faq["question"]):
                    st.write(faq["answer"])

            st.markdown("<br><br>", unsafe_allow_html=True)

            ############# finnnnn#############
            st.markdown("""
            <style>
            .footer {
                width: 100vw;
                background-color: #1E293B;
                color: #e6ecf2;
                padding: 40px 0;
                font-size: 14px;
                line-height: 1.6;
                border-top: 1px solid #ccc;
                position: relative;
                left: -328px;  /* fond bleu reste inchangé */
            }

            .footer-container {
                width: 1200px;
                display: flex;
                flex-wrap: nowrap;

                justify-content: flex-start;
                position: relative;
                left: 70px;  /* texte principal reste décalé de 7 cm à droite */
            }

            .footer-column {
                flex: 1;
                min-width: 220px;
                margin: 10px 20px;
            }

            .footer h4 {
                margin-bottom: 10px;
                border-bottom: 1px solid #99999933;
                padding-bottom: 5px;
                color: #e6ecf2;
            }

            .footer a {
                color: #e6ecf2;
                text-decoration: none;
            }

            .footer a:hover {
                text-decoration: underline;
            }

            .footer p {
                color: #e6ecf2;
                margin: 4px 0;
            }

            .social-icons img {
                width: 22px;
                margin-right: 10px;
                filter: brightness(0) invert(1);
            }

            .footer-bottom {
                width: 1200px;
                margin-top: 15px;
                color: #e6ecf2;
                font-size: 13px;
                position: relative;
                left: 15.5cm;  /* avancé de 1,5 cm à droite depuis 14 cm */
            }
            </style>

            <div class="footer">
                <div class="footer-container">
                    <div class="footer-column">
                        <h4>Axiora Data</h4>
                        <p>Axiora est une plateforme qui permet d'analyser et de traiter les données HCP, et de les visualiser via des graphiques et cartes interactives.</p>
                        <div class="social-icons">
                            <a href="#"><img src="https://img.icons8.com/ios-filled/50/000000/facebook-new.png"/></a>
                            <a href="#"><img src="https://img.icons8.com/ios-filled/50/000000/twitter.png"/></a>
                            <a href="#"><img src="https://img.icons8.com/ios-filled/50/000000/instagram-new.png"/></a>
                        </div>
                    </div>
                    <div class="footer-column">
                        <h4>Informations</h4>
                        <p><a href="#">Statistiques HCP</a></p>
                        <p><a href="#">Applications Populaires</a></p>
                        <p><a href="#">Revenus et Utilisateurs</a></p>
                        <p><a href="#">Tendances Santé</a></p>
                    </div>
                    <div class="footer-column">
                        <h4>Outils Populaires</h4>
                        <p><a href="#">Générateur de Noms</a></p>
                        <p><a href="#">Analyse de Données HCP</a></p>
                        <p><a href="#">Visualisation de Données</a></p>
                    </div>
                    <div class="footer-column">
                        <h4>Contactez-nous</h4>
                        <p><a href="#">À propos</a></p>
                        <p><a href="#">Politique de Confidentialité</a></p>
                        <p>Besoin d'aide ou une question ?</p>
                        <p>Téléphone : +212 600000000</p>
                        <p>Email : contact@axioradata.com</p>
                    </div>
                </div>
                <div class="footer-bottom">&copy; 2025 - Axiora Data</div>
            </div>

            """, unsafe_allow_html=True)





