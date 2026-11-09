"""HCP tables for the Souss-Massa region, entered from the publications of the
HCP regional directorate (hcp.ma/region-agadir).

Each table is stored column by column, labels and values aligned by position.
Missing figures are None. SOURCES gives the publication of every table;
validate_data.py checks shapes, totals, missing values and territorial names.
"""

ASR = "HCP, Annuaire statistique régional Souss-Massa"

SOURCES = {
    "pauvrete": "HCP Souss-Massa, Évolution des indicateurs de pauvreté 2004, 2007 et 2014 (une fiche par province ou préfecture)",
    "population/division_administrative": f"{ASR} 2017 et 2018, chapitre Population",
    "population/population_legale": f"{ASR} 2017, Population, tableau 2 (RGPH 2004 et 2014)",
    "population/estimations_population_milieu": f"{ASR} 2017 et 2018, Population, tableau 3",
    "population/evolution_population_age": f"{ASR} 2017 et 2018, Population, tableau 4",
    "population/estimation_nombre_menages": f"{ASR} 2017 (2014) et 2018 (2018), Population",
    "marche_du_travail/activite_par_age_milieu": "HCP, Enquête nationale sur l'emploi 2017 à 2020, résultats régionaux",
    "marche_du_travail/taux_activite_instruction": "HCP, Enquête nationale sur l'emploi 2017 à 2020, résultats régionaux",
    "marche_du_travail/taux_emploi_sexe_milieu": "HCP, Enquête nationale sur l'emploi 2017 à 2020, résultats régionaux",
    "marche_du_travail/taux_chomage_par_province": f"{ASR} 2016, Emploi, tableau 2 (ENE 2016)",
    "marche_du_travail/population_chomage_age_milieu": f"{ASR} 2016, Emploi, tableau 3 (ENE 2016)",
    "marche_du_travail/taux_chomage_diplome_milieu": f"{ASR} 2016, Emploi (ENE 2016)",
    "marche_du_travail/population_active_occupee_age": f"{ASR} 2016, Emploi (ENE 2016)",
    "marche_du_travail/population_active_occupee_sexe": f"{ASR} 2016, Emploi (ENE 2016)",
    "marche_du_travail/population_active_occupee_secteurs": f"{ASR} 2016, Emploi (ENE 2016)",
    "marche_du_travail/population_active_occupee_statut": f"{ASR} 2016, Emploi (ENE 2016)",
    "habitat": f"{ASR} 2017, Habitat, tableaux 1 à 4",
    "finance": f"{ASR} 2017, chapitres Finances et Économie",
    "enseignement/nouveaux_inscrits_annee_1": f"{ASR} 2017 et 2018, Enseignement, tableau 6",
    "enseignement/personnel_enseignant_sexe": f"{ASR} 2017 et 2018, Enseignement, tableau 7",
    "enseignement/eleves_primaire_public_par_niveau": f"{ASR} 2017 et 2018, Enseignement, tableau 11",
    "sante": f"{ASR} 2017, Santé, tableaux 1 et 2",
    "tourisme": f"{ASR} 2017, Tourisme, tableau 3",
    "énergie": f"{ASR} 2017 et 2018, Énergie et Mines, tableaux 2, 5 et 6",
}

# Published figures that do not add up, and the value used here:
#   marche_du_travail/population_chomage_age_milieu, Région, 35-44 ans: the 2016 yearbook prints
#   12 984; its urban and rural parts (9 538 + 2 510) and the row total both give 12 048.
#   population/population_legale, Chtouka-Aït Baha, urbain 2004: 39 694, the value with which the
#   provinces add up to the published regional total (no HCP sheet gives this figure directly).

hcp_data = {
    "pauvrete": {
        "Chtouka- Ait Baha": {
            "Commune": ["Ait Baha (M)", "Biougra (M)", "Ait Mzal", "Ait Ouadrim", "Aouguenz", "Hilala", "Ida-Ougnidif", "Sidi Abdallah El Bouchouari", "Tanalt", "Targua-Ntouchka", "Tassegdelt", "Tizi Ntakoucht", "Ait Milk", "Belfaa", "Belfaa Centre (AC)", "Inchaden", "Massa", "Massa centre (AC)", "Sidi Ouassay", "Ait Amira", "Ait Amira centre (AC)", "Imi-Mqourn", "Ouad Essafa", "Sidi Bibi", "Sidi Bibi centre (AC)", "Sidi Boushab", "Province de Chtouka-Ait Baha Urbain", "Province de Chtouka-Ait Baha Rural", "Province de Chtouka-Ait Baha Ensemble"],
            "Taux de pauvreté 2004": [8.1, 9.0, 23.8, 31.0, 29.7, 27.4, 17.3, 30.3, 13.7, 16.2, 44.7, 9.3, 21.9, 17.4, None, 17.3, 17.5, 5.4, 9.8, 13.9, None, 23.6, 14.4, 13.1, None, 27.3, 8.1, 18.5, 17.1],
            "Taux de pauvreté 2007": [2.8, 6.5, 12.8, 19.3, 16.8, 13.2, 5.8, 17.0, 8.5, 20.0, 16.3, 14.6, 11.3, 5.6, None, 5.8, 4.0, 11.5, 4.3, 5.4, None, 15.4, 6.1, 4.1, None, 15.1, 7.2, 8.5, 8.4],
            "Taux de pauvreté 2014": [11.27, 1.02, 7.44, 13.16, 10.24, 11.42, 6.44, 15.83, 3.73, 17.35, 8.68, 8.41, 5.75, 2.27, 1.55, 1.78, 2.45, 8.48, 1.68, 1.38, 0.85, 14.69, 4.29, 2.69, 0.55, 7.25, 2.13, 4.92, 4.07],
            "Taux de vulnérabilité 2004": [11.3, 12.4, 23.9, 25.6, 24.9, 25.2, 20.9, 25.8, 18.6, 21.3, 25.6, 14.8, 23.3, 21.5, None, 21.1, 20.7, 8.4, 14.3, 19.0, None, 25.0, 19.6, 18.0, None, 25.5, 11.4, 21.0, 19.7],
            "Taux de vulnérabilité 2007": [14.7, 20.6, 20.5, 24.4, 18.9, 25.0, 11.2, 24.8, 14.1, 27.3, 23.0, 20.8, 19.4, 17.1, None, 15.8, 11.0, 36.5, 9.8, 17.8, None, 23.7, 16.3, 11.2, None, 24.9, 23.5, 17.7, 18.5],
            "Taux de vulnérabilité 2014": [22.06, 7.9, 20.98, 25.51, 23.44, 27.44, 20.22, 28.86, 12.96, 30.59, 21.45, 20.64, 18.13, 9.47, 10.01, 7.48, 10.12, 17.95, 7.47, 6.75, 8.12, 29.11, 14.67, 10.71, 5.51, 20.37, 9.57, 14.16, 12.76]
        },
        "Tiznit": {
            "Commune": ["Tafraout (M)", "Tiznit (M)", "Ait Issafen", "Anzi", "Arbaa Ait Ahmed", "Ida Ou Gougmar", "Sidi Ahmed Ou Moussa", "Tafraout El Mouloud", "Tighmi", "Tizoughrane", "Tnine Aday", "Afella Ighir", "Ait Ouafqa", "Ammelne", "Irigh N'Tahala", "Tarsouat", "Tassrirt", "Arbaa Rasmouka", "Arbaa Sahel", "Bounaamane", "El Maader El Kabir", "Ouijjane", "Reggada", "Sidi Bouabdelli", "Tnine Aglou", "Province de Tiznit Urbain", "Province de Tiznit Rural", "Province de Tiznit Ensemble"],
            "Taux de pauvreté 2004": [5.1, 3.2, 27.0, 32.4, 33.4, 27.7, 27.5, 17.3, 22.2, 20.7, 17.5, 19.2, 29.0, 20.4, 23.2, 29.9, 23.6, 17.6, 24.6, 17.7, 14.9, 15.2, 15.6, 31.3, 14.3, 3.5, 25.5, 20.1],
            "Taux de pauvreté 2007": [3.3, 2.5, 16.9, 14.5, 16.7, 19.4, 11.8, 16.1, 14.5, 14.3, 14.4, 9.6, 15.4, 8.9, 8.2, 9.9, 9.3, 9.6, 12.1, 13.8, 7.4, 10.3, 9.2, 19.4, 6.0, 3.1, 15.8, 12.7],
            "Taux de pauvreté 2014": [4.89, 2.19, 10.32, 10.91, 18.06, 11.87, 7.45, 14.55, 12.03, 9.65, 12.41, 7.65, 5.01, 6.5, 8.98, 6.57, 3.02, 6.52, 3.2, 11.22, 3.66, 5.65, 7.21, 18.08, 3.09, 2.4, 8.53, 6.13],
            "Taux de vulnérabilité 2004": [7.8, 4.9, 24.5, 26.1, 25.4, 24.7, 23.4, 20.6, 23.4, 22.8, 20.6, 21.0, 24.2, 21.6, 23.9, 23.8, 22.4, 21.3, 24.7, 21.3, 19.4, 19.2, 19.4, 25.6, 18.1, 5.3, 23.2, 18.9],
            "Taux de vulnérabilité 2007": [13.0, 10.5, 19.1, 20.2, 20.9, 25.4, 19.2, 19.0, 18.4, 18.7, 14.2, 13.0, 20.7, 11.4, 14.5, 13.8, 13.3, 17.1, 17.1, 23.1, 12.8, 14.2, 14.4, 24.1, 9.8, 11.6, 21.1, 18.8],
            "Taux de vulnérabilité 2014": [10.84, 8.84, 24.16, 22.32, 29.59, 25.66, 20.75, 23.94, 24.47, 21.64, 25.39, 19.14, 15.24, 17.8, 22.22, 18.29, 12.0, 19.86, 13.23, 25.55, 14.14, 17.58, 18.37, 31.19, 12.5, 8.99, 20.25, 15.84]
        },
        "Tata": {
            "Commune": ["Akka (M)", "Fam El Hisn (M)", "Foum Zguid (M)", "Tata (M)", "Ait Ouabelli", "Kasbat Sidi Abdellah Ben M'Barek", "Tamanarte", "Tizounine", "Aguinane", "Akka-Ighane", "Allougoum", "Ibn Yacoub", "Tissint", "Tlite", "Adis", "Issafen", "Oum El Guerdane", "Tagmout", "Tigzmerte", "Tizaghte", "Province de Tata Urbain", "Province de Tata Rural", "Province de Tata Ensemble"],
            "Taux de pauvreté 2004": [38.03, 15.95, 16.74, 21.83, 27.7, 34.31, 22.27, 17.05, 13.82, 36.3, 40.31, 19.04, 27.4, 38.09, 8.67, 18.62, 18.04, 22.13, 10.83, 20.64, 22.2, 25.6, 24.5],
            "Taux de pauvreté 2007": [16.2, 6.6, 12.3, 11.7, 20.9, 32.6, 11.1, 14.5, 14.9, 20.3, 38.7, 14.0, 28.8, 33.8, 12.7, 9.2, 14.1, 11.1, 9.3, 16.8, 11.8, 21.1, 18.2],
            "Taux de pauvreté 2014": [21.27, 11.48, 14.62, 4.06, 16.85, 25.21, 9.66, 16.38, 17.72, 33.08, 37.21, 22.02, 21.85, 25.09, 12.84, 18.21, 10.69, 15.34, 7.36, 11.92, 10.15, 20.38, 17.01],
            "Taux de vulnérabilité 2004": [22.76, 19.26, 18.18, 19.99, 24.04, 27.2, 21.92, 22.62, 18.21, 25.17, 24.1, 20.85, 25.42, 26.32, 13.4, 19.66, 21.34, 23.31, 14.86, 22.4, 19.9, 22.5, 21.7],
            "Taux de vulnérabilité 2007": [37.9, 31.1, 56.4, 33.8, 29.4, 29.3, 21.7, 24.0, 24.5, 24.7, 24.5, 26.2, 24.5, 26.8, 18.2, 17.0, 19.8, 21.7, 13.1, 25.1, 39.8, 23.4, 28.5],
            "Taux de vulnérabilité 2014": [29.05, 20.59, 24.31, 16.51, 32.62, 31.49, 22.43, 27.9, 28.77, 32.73, 31.12, 40.17, 29.8, 32.7, 35.22, 28.4, 22.66, 26.26, 23.15, 25.22, 20.77, 29.56, 26.67]
        },
        "Taroudannt": {
            "Commune": ["Ait Iaaza (M)", "Aoulouz (M)", "El Guerdane (M)", "Irherm (M)", "Oulad Berhil (M)", "Oulad Teima (M)", "Taliouine (M)", "Taroudannt (M)", "Adar", "Ait Abdallah", "Amalou", "Azaghar N'Irs", "Imaouen", "Imi N'Tayart", "Nihit", "Oualqadi", "Sidi Boaal", "Sidi Mzal", "Tabia", "Tataoute", "Tindine", "Tisfane", "Toufelaazt", "Toumliline", "Arazane", "El Faid", "Ida Ou Gailal", "Ida-Ougoummad", "Igli", "Igoudar Mnabha", "Lamhara", "Oulad Aissa", "Ouneine", "Sidi Abdellah Ou Said", "Sidi Ouaaziz", "Tafingoult", "Talgjount", "Tigouga", "Tinzart", "Tizi N'Test", "Toughmart", "Ahl Ramel", "Argana", "Assads", "Bigoudine", "Eddir", "El Koudia El Beida", "Imilmaiss", "Issen", "Lagfifat", "Lakhnafif", "Lamhadi", "Machraa El Ain", "Sidi Ahmed Ou Amar", "Sidi Boumoussa", "Sidi Moussa Lhamri", "Talmakante", "Tidsi-Nissendalene", "Agadir Melloul", "Ahl Tifnoute", "Askaouen", "Assaisse", "Assaki", "Azrar", "Iguidi", "Sidi Hsaine", "Taouyalte", "Tassousfi", "Tizgzaouine", "Toubkal", "Zagmouzen", "Ouzioua", "Tisrasse", "Ahmar Laglalcha", "Ait Igas", "Ait Makhlouf", "Bounrar", "Freija", "Ida Ou Moumen", "Imoulass", "Lamnizla", "Sidi Ahmed Ou Abdallah", "Sidi Borja", "Sidi Dahmane", "Tafraouten", "Tamaloukte", "Tazemmourt", "Tiout", "Zaouia Sidi Tahar", "Province de Taroudannt Urbain", "Province de Taroudannt Rural", "Province de Taroudannt Ensemble"],
            "Taux de pauvreté 2004": [12.0, 26.4, 5.4, 22.8, 10.4, 6.3, 40.3, 5.8, 37.4, 18.8, 31.3, 28.1, 30.4, 18.6, 47.2, 38.9, 34.7, 30.3, 29.7, 22.1, 22.2, 32.9, 35.7, 39.5, 33.0, 40.8, 40.5, 31.1, 17.8, 23.1, 25.6, 18.7, 35.9, 36.0, 37.8, 17.6, 38.4, 34.2, 25.1, 36.9, 43.9, 5.7, 32.8, 40.0, 39.3, 31.0, 8.3, 44.2, 20.9, 16.0, 16.0, 14.8, 10.7, 13.3, 16.9, 20.7, 39.1, 22.4, 34.6, 21.5, 20.0, 22.6, 32.6, 39.5, 33.2, 31.7, 33.2, 18.7, 35.1, 36.3, 27.9, 36.3, 36.4, 23.5, 25.6, 38.2, 25.2, 18.8, 28.1, 30.9, 26.5, 51.2, 20.5, 20.8, 48.6, 38.2, 24.2, 25.7, 19.7, 8.5, 27.0, 22.6],
            "Taux de pauvreté 2007": [10.4, 13.5, 6.7, 14.0, 12.3, 3.8, 17.6, 2.2, 17.1, 11.0, 18.0, 19.8, 20.5, 9.1, 22.2, 15.7, 20.0, 14.4, 18.7, 16.8, 20.0, 21.6, 16.9, 20.4, 15.6, 21.5, 17.0, 18.4, 11.7, 10.4, 21.3, 8.5, 13.5, 24.6, 14.0, 12.3, 16.3, 21.9, 13.9, 17.2, 23.5, 6.9, 18.3, 17.4, 21.0, 19.8, 10.1, 30.8, 9.4, 11.1, 5.1, 9.1, 4.8, 7.7, 4.5, 12.5, 15.4, 15.6, 23.4, 29.5, 24.1, 20.4, 19.7, 21.5, 32.0, 23.5, 23.7, 15.0, 17.1, 29.8, 31.2, 19.1, 20.3, 10.5, 12.0, 16.2, 18.6, 10.2, 10.8, 12.3, 14.5, 19.4, 8.0, 9.6, 20.1, 14.6, 9.8, 11.1, 7.8, 5.3, 15.7, 13.2],
            "Taux de pauvreté 2014": [4.2, 21.04, 3.93, 24.64, 11.16, 4.16, 16.38, 2.37, 12.66, 8.49, 11.04, 13.37, 16.56, 4.48, 6.8, 8.98, 9.68, 6.64, 17.31, 10.33, 19.05, 17.01, 30.61, 15.97, 18.64, 17.59, 21.34, 14.47, 5.59, 5.3, 5.76, 2.98, 14.36, 13.13, 11.89, 15.92, 24.9, 21.65, 6.81, 28.78, 17.09, 4.89, 21.5, 16.37, 27.92, 13.68, 5.11, 15.89, 11.97, 6.89, 5.41, 5.94, 4.64, 6.5, 5.79, 11.55, 13.11, 15.77, 26.11, 9.32, 10.23, 7.08, 11.95, 17.09, 11.94, 4.09, 14.94, 7.72, 7.76, 10.93, 17.47, 22.99, 24.61, 6.75, 10.71, 11.46, 10.79, 6.78, 10.29, 12.54, 13.21, 16.43, 6.98, 6.12, 11.65, 12.64, 7.56, 15.65, 5.36, 6.02, 11.17, 9.65],
            "Taux de vulnérabilité 2004": [15.5, 26.0, 8.9, 19.6, 14.1, 9.6, 20.9, 8.5, 25.8, 20.7, 26.0, 24.5, 25.7, 21.3, 23.2, 25.8, 26.0, 26.0, 25.5, 24.8, 25.6, 25.6, 26.9, 24.8, 26.7, 26.6, 27.1, 26.2, 22.3, 25.8, 26.1, 22.8, 27.6, 28.0, 27.6, 22.1, 27.0, 28.0, 26.8, 27.3, 25.2, 10.1, 25.8, 26.7, 25.7, 27.5, 13.8, 26.5, 25.1, 21.8, 21.1, 20.5, 16.3, 19.3, 20.5, 24.7, 26.1, 25.0, 26.2, 24.3, 23.5, 24.6, 27.1, 27.2, 27.6, 26.0, 27.9, 22.3, 26.0, 26.9, 26.4, 26.2, 27.1, 25.5, 27.0, 27.1, 26.4, 23.7, 27.1, 25.9, 24.7, 24.5, 24.2, 23.3, 24.5, 25.9, 25.9, 25.3, 24.3, 10.8, 24.3, 21.1],
            "Taux de vulnérabilité 2007": [31.9, 23.7, 24.3, 42.2, 35.9, 18.5, 36.8, 11.8, 24.7, 17.3, 27.4, 27.0, 25.7, 21.2, 23.8, 21.5, 24.3, 18.6, 30.0, 27.0, 26.9, 26.4, 27.4, 27.3, 22.8, 25.7, 23.6, 21.4, 19.4, 18.1, 24.7, 15.5, 24.9, 28.5, 20.8, 20.8, 22.2, 30.3, 21.7, 26.6, 25.8, 14.3, 24.4, 25.4, 25.9, 28.0, 17.2, 31.2, 19.3, 18.7, 12.1, 15.7, 11.9, 14.7, 13.0, 19.2, 25.5, 21.6, 28.3, 31.1, 30.2, 25.6, 24.8, 29.6, 29.2, 24.2, 28.7, 24.5, 26.1, 29.5, 28.9, 27.9, 27.4, 18.0, 22.7, 27.6, 27.7, 20.6, 20.4, 23.3, 16.9, 25.6, 19.2, 19.9, 27.6, 21.7, 18.7, 18.7, 16.3, 20.1, 22.5, 21.9],
            "Taux de vulnérabilité 2014": [13.2, 26.04, 15.18, 26.57, 19.85, 13.89, 22.88, 9.85, 25.01, 21.61, 23.79, 26.01, 27.84, 14.01, 17.49, 21.98, 22.51, 20.33, 23.87, 25.56, 30.92, 27.38, 32.18, 27.42, 28.55, 30.06, 30.38, 28.09, 15.53, 16.92, 16.51, 10.9, 29.08, 25.08, 26.68, 28.06, 35.35, 33.19, 19.19, 37.57, 29.23, 15.87, 31.65, 28.54, 32.34, 26.1, 14.42, 30.96, 24.21, 17.6, 15.56, 17.05, 14.61, 17.32, 16.24, 22.77, 29.05, 30.31, 32.24, 20.01, 22.37, 16.58, 22.54, 31.22, 24.23, 14.32, 28.87, 20.83, 20.86, 24.04, 29.78, 31.49, 33.52, 17.99, 21.81, 26.03, 26.18, 17.93, 23.85, 27.9, 28.09, 30.64, 18.92, 17.97, 24.97, 25.83, 19.29, 29.7, 15.91, 14.43, 22.64, 20.21]
        },
        "Agadir-Ida -Ou-Tanane": {
            "Commune": ["Agadir (M)", "Amskroud", "Drargua", "Drargua centre (AC)", "Idmine", "Aourir", "Aourir centre (AC)", "Aqsri", "Aziar", "Imouzzer", "Imsouane", "Tadrart", "Taghazout", "Tamri", "Tiqqi", "Préfecture d'Agadir-Idaoutanane Urbain", "Préfecture d'Agadir-Idaoutanane Rural", "Préfecture d'Agadir-Idaoutanane Ensemble"],
            "Taux de pauvreté 2004": [3.7, 23.0, 28.4, 11.7, 18.8, 14.6, 15.2, 29.8, 15.6, 28.3, 28.3, 21.4, 10.2, 25.5, 28.0, 4.7, 24.4, 8.9],
            "Taux de pauvreté 2007": [1.5, 12.6, 11.0, 0.5, 13.6, 6.5, 8.2, 14.9, 19.9, 15.4, 11.7, 17.8, 10.3, 15.1, 17.3, 1.9, 13.5, 4.3],
            "Taux de pauvreté 2014": [0.39, 10.09, 8.86, 6.84, 6.91, 6.83, 4.64, 4.3, 9.76, 13.16, 4.9, 9.7, 5.9, 5.41, 17.02, 1.33, 8.53, 2.44],
            "Taux de vulnérabilité 2004": [5.8, 25.1, 26.2, 15.7, 24.1, 17.5, 17.0, 26.4, 21.5, 25.9, 26.4, 25.5, 15.8, 25.2, 26.1, 6.8, 24.6, 10.6],
            "Taux de vulnérabilité 2007": [7.8, 20.5, 21.4, 5.3, 24.6, 10.0, 30.4, 22.7, 28.4, 25.4, 20.6, 28.1, 20.4, 24.4, 29.8, 8.9, 23.0, 11.9],
            "Taux de vulnérabilité 2014": [3.1, 22.98, 21.76, 12.98, 20.34, 19.31, 13.15, 14.98, 23.04, 26.55, 16.01, 24.25, 16.51, 15.56, 31.41, 4.78, 20.75, 7.24]
        },
        "Inezgane-Ait Melloul": {
            "Commune": ["Ait Melloul (M)", "Dcheira El Jihadia (M)", "Inezgane (M)", "Lqliaa (M)", "Oulad Dahou", "Temsia", "Temsia centre (AC)", "Préfecture d'Inezgane-Ait Melloul Urbain", "Préfecture d'Inezgane-Ait Melloul Rural", "Préfecture d'Inezgane-Ait Melloul Ensemble"],
            "Taux de pauvreté 2004": [9.0, 4.9, 8.0, 19.2, 20.5, 22.0, 13.8, 8.6, 20.7, 9.6],
            "Taux de pauvreté 2007": [2.4, 0.6, 3.5, 10.4, 13.3, 10.9, 6.9, 2.9, 11.7, 3.6],
            "Taux de pauvreté 2014": [1.54, 0.28, 1.56, 4.34, 5.29, 7.58, 6.48, 2.01, 6.37, 2.23],
            "Taux de vulnérabilité 2004": [12.5, 7.2, 11.7, 21.9, 23.9, 23.4, 17.7, 11.9, 23.2, 12.8],
            "Taux de vulnérabilité 2007": [12.0, 3.3, 15.6, 16.6, 17.3, 14.3, 24.7, 12.7, 16.1, 12.9],
            "Taux de vulnérabilité 2014": [8.15, 3.17, 9.56, 12.52, 16.08, 19.81, 13.43, 8.52, 17.83, 8.99]
        }
    },
    "population": {
        "division_administrative": {
            "2017": {
                "Province": ["Agadir Ida Outanane", "Inezgane-Aït Melloul", "Chtouka-Aït Baha", "Taroudant", "Tiznit", "Tata"],
                "Urbaines": [1, 4, 2, 8, 2, 4],
                "Rurales": [12, 2, 20, 81, 23, 16],
                "Total Communes": [13, 6, 22, 89, 25, 20],
                "Cercles": [1, 1, 3, 5, 3, 3]
            },
            "2018": {
                "Province": ["Agadir Ida Outanane", "Inezgane Ait Melloul", "Chtouka Ait Baha", "Taroudant", "Tiznit", "Tata"],
                "Urbaines": [1, 4, 2, 8, 2, 4],
                "Rurales": [12, 2, 20, 81, 23, 16],
                "Total Communes": [13, 6, 22, 89, 25, 20],
                "Cercles": [2, 1, 3, 5, 3, 3]
            }
        },
        "population_legale": {
            "Provinces": ["Agadir Ida Outanane", "Inezgane-Aït Melloul", "Chtouka-Aït Baha", "Taroudant", "Tiznit", "Tata", "Souss-Massa"],
            "RGPH 2004 – Urbain": [384987, 385612, 39694, 186471, 58613, 39060, 1094437],
            "RGPH 2004 – Total": [487954, 419614, 297245, 780661, 217050, 121618, 2324142],
            "RGPH 2014 – Urbain": [508155, 513706, 113531, 248640, 81044, 40820, 1505896],
            "RGPH 2014 – Total": [600599, 541118, 371102, 838820, 207367, 117841, 2676847]
        },
        "estimations_population_milieu": {
            "Provinces": ["Agadir Ida Outanane", "Inezgane Aït Melloul", "Chtouka Aït Baha", "Taroudant", "Tata", "Tiznit", "Souss-Massa"],
            "2016 – Urbain": [535653, 539975, 125818, 260214, 41417, 85357, 1588434],
            "2016 – Rural": [89307, 27595, 258625, 582540, 74937, 119786, 1152790],
            "2016 – Total": [624960, 567570, 384443, 842754, 116354, 205143, 2741224],
            "2017 – Urbain": [551240, 554820, 133050, 266730, 41740, 87800, 1635380],
            "2017 – Rural": [87650, 27710, 259260, 578550, 73840, 116380, 1143390],
            "2017 – Total": [638890, 582530, 392310, 845280, 115580, 204180, 2778770],
            "2018 – Urbain": [567055, 569865, 140642, 273306, 42054, 90276, 1683198],
            "2018 – Rural": [86032, 27806, 259843, 574518, 72752, 113055, 1134006],
            "2018 – Total": [653087, 597671, 400485, 847824, 114806, 203331, 2817204]
        },
        "evolution_population_age": {
            "Groupe d’âge": ["0-4 ans", "5-9 ans", "10-14 ans", "15-19 ans", "20-24 ans", "25-29 ans", "30-34 ans", "35-39 ans", "40-44 ans", "45-49 ans", "50-54 ans", "55-59 ans", "60-64 ans", "65-69 ans", "70-74 ans", "75 ans et plus"],
            "2014 – Total": [266719, 244243, 242784, 231381, 233398, 219021, 211861, 194920, 181003, 149184, 135266, 100538, 86390, 54314, 47437, 71021],
            "2014 – Urbain": [149168, 134967, 130734, 127775, 139186, 131404, 126351, 114419, 106312, 87638, 78159, 55289, 43871, 24887, 20294, 26996],
            "2015 – Total": [263138, 247901, 242734, 231611, 233812, 222918, 214974, 199205, 185359, 152807, 137225, 105990, 90497, 59470, 47632, 69467],
            "2015 – Urbain": [149649, 138729, 132105, 129081, 141790, 137016, 130846, 118877, 109996, 90813, 80386, 59238, 47178, 28191, 20930, 27605],
            "2016 – Total": [258157, 253372, 242142, 232771, 232916, 227545, 217486, 204001, 188828, 158186, 137230, 112736, 93026, 66982, 46275, 69567],
            "2016 – Urbain": [149559, 143496, 133406, 130898, 143058, 143200, 135045, 123916, 113221, 94976, 81590, 63808, 49834, 32671, 20995, 28757],
            "2017 – Total": [251508, 260478, 241642, 234430, 231315, 232285, 219789, 209018, 191816, 164604, 136342, 119808, 94854, 75625, 44596, 70660],
            "2017 – Urbain": [148717, 149207, 134900, 132997, 143466, 149466, 139213, 129315, 116261, 99741, 82305, 68537, 52201, 37806, 20992, 30256],
            "2018 – Total": [243065, 268885, 242011, 235893, 229909, 236252, 222462, 213797, 194959, 170950, 136065, 125881, 97256, 83719, 44246, 71850],
            "2018 – Urbain": [147017, 155706, 136914, 134973, 143762, 155097, 143758, 134723, 119555, 104482, 83315, 72781, 54832, 42848, 21651, 31786]
        },
        "estimation_nombre_menages": {
            "2014": {
                "Provinces": ["Agadir Ida Outanane", "Inezgane", "Chtouka-Aït Baha", "Taroudant", "Tata", "Tiznit", "Souss-Massa"],
                "Total": [154203, 133941, 94633, 177278, 22697, 52349, 635101],
                "Rural": [19644, 6255, 63090, 117574, 14286, 30421, 251270],
                "Urbain": [134559, 127686, 31543, 59704, 8411, 21928, 383831]
            },
            "2018": {
                "Provinces": ["Agadir Ida Outanane", "Inezgane", "Chtouka-Aït Baha", "Taroudant", "Tata", "Tiznit", "Souss-Massa"],
                "Total": [163283, 142549, 99852, 180895, 22675, 52671, 661925],
                "Rural": [19223, 6381, 64281, 117445, 14002, 29186, 250518],
                "Urbain": [144060, 136168, 35571, 63450, 8673, 23485, 411407]
            }
        }
    },
    "marche_du_travail": {
        "activite_par_age_milieu": {
            "Âge": ["15-24", "25-34", "35-44", "45 et plus", "Total"],
            "2017-Urbain": [16.4, 55.8, 56.3, 39.8, 41.8],
            "2017-Rural": [18.5, 54.5, 61.2, 46.9, 45.7],
            "2018-Urbain": [19.3, 53.3, 56.1, 39.7, 41.6],
            "2018-Rural": [25.4, 54.5, 60.4, 45.7, 45],
            "2019-Urbain": [19.4, 56.5, 57.1, 39, 42.6],
            "2019-Rural": [22, 53.6, 59.9, 43.3, 43.5],
            "2020-Urbain": [16.4, 55.7, 57.2, 38, 41.5],
            "2020-Rural": [18.5, 52.7, 56.9, 42.2, 41.6]
        },
        "taux_activite_instruction": {
            "Niveau": ["Sans diplôme", "Avec diplôme", "Sans diplôme", "Avec diplôme", "Sans diplôme", "Avec diplôme"],
            "Milieu": ["Urbain", "Urbain", "Rural", "Rural", "Total", "Total"],
            "2017": [38.4, 45.2, 48, 39.6, 43.2, 43.7],
            "2018": [38, 45, 46.8, 40.5, 42.3, 43.8],
            "2019": [37.6, 47.1, 44.4, 41.3, 40.9, 45.6],
            "2020": [36.1, 46.2, 42.7, 38.8, 39.3, 44.3]
        },
        "taux_emploi_sexe_milieu": {
            "Sexe": ["Hommes", "Femmes", "Hommes", "Femmes", "Hommes", "Femmes"],
            "Milieu": ["Urbain", "Urbain", "Rural", "Rural", "Total", "Total"],
            "2017": [61.6, 12.5, 63.9, 26.0, 62.5, 18.2],
            "2018": [61.2, 12.3, 62.7, 25.0, 61.7, 17.5],
            "2019": [61.3, 13.5, 63.7, 21.0, 62.2, 16.6],
            "2020": [59.7, 11.9, 62.1, 18.1, 60.6, 14.4]
        },
        "taux_chomage_par_province": {
            "Province": ["Agadir Ida Outanane", "Inezgane Ait Melloul", "Taroudannt", "Région"],
            "Taux_Activité_Urbain": [41.6, 42.2, 43.9, 41.5],
            "Taux_Chômage_Urbain": [16.7, 11.8, 13.8, 13.9],
            "Taux_Activité_Rural": [50.5, 47.0, 57.8, 52.1],
            "Taux_Chômage_Rural": [3.3, 14.5, 3.8, 4.7],
            "Taux_Activité_Total": [45.4, 42.5, 54.1, 46.6],
            "Taux_Chômage_Total": [10.4, 12.0, 5.9, 9.0]
        },
        "population_chomage_age_milieu": {
            "Milieu": ["Région", "Urbain Région", "Rural Région", "Maroc", "Urbain Maroc", "Rural Maroc"],
            "15-24": [26013, 16908, 9105, 392146, 283177, 108969],
            "25-34": [37556, 27910, 9646, 480693, 403509, 77184],
            "35-44": [12048, 9538, 2510, 135407, 113254, 22153],
            "45+": [8794, 6604, 2190, 97318, 79023, 18295],
            "Total": [84411, 60960, 23451, 1105564, 878963, 226601]
        },
        "taux_chomage_diplome_milieu": {
            "Milieu": ["Région", "Urbain Région", "Rural Région", "Maroc", "Urbain Maroc", "Rural Maroc"],
            "Sans diplôme": [3.9, 7.3, 2.2, 3.8, 6.5, 2.2],
            "Niveau moyenne": [13.1, 16.5, 8.5, 14.3, 17.2, 8.5],
            "Niveau supérieur": [23.7, 21.9, 34.0, 21.9, 21.1, 33.3],
            "Total": [9.0, 13.9, 4.7, 9.4, 13.9, 4.2]
        },
        "population_active_occupee_age": {
            "Âge": ["15-24", "25-34", "35-44", "45 et plus", "Total"],
            "Région-Urbain": [28537, 122684, 107949, 117604, 376774],
            "Région-Rural": [74003, 144680, 101353, 159340, 479376],
            "Région-Total": [102540, 267364, 209302, 276944, 856150],
            "Maroc-Urbain": [406879, 1607948, 1576580, 1836830, 5428237],
            "Maroc-Rural": [944659, 1475434, 1088876, 1704415, 5213384],
            "Maroc-Total": [1351538, 3083382, 2665456, 3541245, 10641621]
        },
        "population_active_occupee_sexe": {
            "Milieu": ["Région", "Urbain Région", "Rural Région", "Maroc", "Urbain Maroc", "Rural Maroc"],
            "Masculin": [610608, 314710, 295898, 7884294, 4386974, 3497320],
            "Féminin": [245542, 62064, 183478, 2757327, 1041263, 1716064],
            "Total": [856150, 376774, 479376, 10641621, 5428237, 5213384]
        },
        "population_active_occupee_secteurs": {
            "Milieu": ["Région", "Urbain Région", "Rural Région", "Maroc", "Urbain Maroc", "Rural Maroc"],
            "Forêt et pêche / Agriculture": [382657, 36085, 346572, 4042943, 244731, 3798212],
            "Industrie et commerce": [70488, 52390, 18098, 1199134, 980432, 218702],
            "B.T.P": [86324, 45408, 40916, 1042110, 610666, 431444],
            "Services": [315362, 241572, 73790, 4344867, 3580980, 763887],
            "Autres": [1319, 1319, 0, 12567, 11428, 1139],
            "Total": [856150, 376774, 479376, 10641621, 5428237, 5213384]
        },
        "population_active_occupee_statut": {
            "Statut": ["Salariés", "Auto-emploi", "Emploi non rémunéré", "Autres", "Total"],
            "Urbain": [251639, 111477, 12802, 856, 376774],
            "Rural": [167635, 167668, 143696, 377, 479376],
            "Total": [419274, 279145, 156498, 1233, 856150]
        }
    },
    "habitat": {
        "operations_achevees": {
            "Province": ["Agadir Ida Outanane", "Inezgane Ait Melloul", "Chtouka Ait Baha", "Taroudant", "Tiznit", "Tata", "Total"],
            "Nbre d'unités": [9439, 1063, 295, 261, 4279, None, 15337],
            "Superficie (En Ha)": [283, 35, 427, 1, 986, None, 1732],
            "Lotissements": [589, 100, 0, 0, 0, None, 689],
            "Logements (recasement)": [0, 0, 0, 0, 0, None, 0],
            "Restructuration": [7063, 0, 295, 0, 4213, None, 11571],
            "Lots de terrain": [21, 737, 0, 0, 0, None, 758],
            "Logements (autres unités)": [1693, 216, 0, 261, 62, None, 2232],
            "Activités et Zones Industrielles": [73, 10, 0, 0, 4, None, 87],
            "Cout en Millions de DH": [588, 285, 2, 36, 60, None, 971]
        },
        "operations_lancement": {
            "Province": ["Agadir Ida Outanane", "Inezgane Ait Melloul", "Chtouka Ait Baha", "Total"],
            "Nbre d'unités": [9817, 583, 2469, 12869],
            "Superficie (En Ha)": [334, 2, 383, 719],
            "Lotissements": [0, 0, 0, 0],
            "Logements (recasement)": [0, 0, 0, 0],
            "Restructuration": [7395, 0, 2469, 9864],
            "Lots de terrain": [0, 0, 0, 0],
            "Logements (autres unités)": [679, 533, 0, 1212],
            "Activités et Zones Industrielles": [1743, 50, 0, 1793],
            "Cout en Millions de DH": [385, 104, 25, 514]
        },
        "operations_execution": {
            "Province": ["Agadir Ida Outanane", "Inezgane Ait Melloul", "Chtouka Ait Baha", "Taroudant", "Tiznit", "Tata"],
            "Nbre d'unités": [6662, 3283, 5841, 2050, 797, None],
            "Superficie (En Ha)": [60, 42, 330, 143, 64, None],
            "Lotissements": [985, 744, 24, 0, 0, None],
            "Logements (recasement)": [0, 0, 210, 0, 0, None],
            "Restructuration": [500, 0, 150, 0, 672, None],
            "Lots de terrain": [25, 994, 4800, 850, 0, None],
            "Logements (autres unités)": [4416, 1228, 100, 96, 111, None],
            "Activités et Zones Industrielles": [736, 317, 557, 1104, 14, None],
            "Cout en Millions de DH": [2121, 517, 973, 475, 38, None]
        },
        "operations_etude": {
            "Province": ["Agadir Ida Outanane", "Inezgane Ait Melloul", "Chtouka Ait Baha", "Taroudant", "Tiznit", "Tata", "Total"],
            "Nbre d'unités": [29568, 722, 457, 400, 300, None, 31447],
            "Superficie (En Ha)": [1019, 3, 4, 6, 1, None, 1033],
            "Lotissements": [0, 0, 0, 0, 0, None, 0],
            "Logements (recasement)": [0, 0, 0, 400, 0, None, 400],
            "Restructuration": [0, 0, 0, 0, 0, None, 0],
            "Lots de terrain": [25204, 0, 117, 0, 0, None, 25321],
            "Logements (autres unités)": [4364, 500, 340, 0, 300, None, 5504],
            "Activités et Zones Industrielles": [0, 222, 0, 0, 0, None, 222],
            "Cout en Millions de DH": [5815, 110, 77, 40, 55, None, 6097]
        }
    },
    "finance": {
        "depots_credits_banques": {
            "Province": ["Agadir Ida Outanane", "Inezgane Ait Melloul", "Chtouka Ait Baha", "Taroudant", "Tiznit", "Tata"],
            "Montant des dépôts (en milliers)": [25599795, 9560580, 2488070, 5962524, 5697437, 254432],
            "Montant des crédits (en milliers)": [20526240, 3666514, 482351, 3747507, 1140457, 134904]
        },
        "projets_investissement_2017": {
            "Provinces": ["Agadir Ida Outanane", "Inezgane Ait Melloul", "Chtouka Ait Baha", "Taroudant", "Tiznit", "Tata", "Total"],
            "Emplois à créer": [9083, 384, 1023, 896, 896, 512, 12793],
            "Montant d'investissement (millions de DH)": [11113, 780, 4641, 579, 590, 256, 17960],
            "Nombre de projets": [134, 23, 6, 17, 15, 17, 213]
        },
        "ventilation_sectorielle_projets": {
            "Secteur d’Activité": ["Tourisme", "Services", "Commerce", "BTP", "Mines", "Industrie", "Artisanat"],
            "Investissement (millions de DH)": [6714, 5285, 519, 4561, 167, 711, 4],
            "Emplois à créer": [4941, 3082, 230, 1361, 104, 949, 2]
        },
        "evolution_entreprises_creees": {
            "Année": ["2017", "2016", "2015"],
            "Nombre d’emplois ": [3549, 2718, 4293],
            "Montant d’investissement (Mdhs) ": [360, 323, 562],
            "Nombre de projets ": [684, 572, 1087]
        },
        "repartition_entreprises_secteur": {
            "Secteur d’Activité": ["Tourisme", "Services", "Commerce", "BTP", "Mines", "Agriculture et pêche", "Industrie"],
            "Nbre d’entreprises créées (%)": [1, 40, 37, 17, 1, 5, 1],
            "Montant d’investissement (%)": [2, 36, 28, 22, 2, 9, 1]
        },
        "pib_secteurs": {
            "Secteurs ": ["Primaire ", "Secondaire ", "Tertiaire "],
            "Souss Massa 2015": [12036, 13460, 31522],
            "Souss Massa 2016": [13864, 12832, 33163],
            "Maroc 2015": [124759, 257796, 491424],
            "Maroc 2016": [121556, 263384, 509991]
        }
    },
    "enseignement": {
        "nouveaux_inscrits_annee_1": {
            "2017": {
                "Province": ["Agadir Ida Outanane", "Inezgane Aït Melloul", "Chtouka Aït Baha", "Taroudant", "Tiznit", "Tata", "Région Souss-Massa"],
                "Garçons 2017": [6237, 6043, 4605, 9112, 1886, 1190, 29073],
                "Filles 2017": [5950, 5750, 4383, 8784, 1758, 1178, 27803],
                "Total 2017": [12187, 11793, 8988, 17896, 3644, 2368, 56876]
            },
            "2018": {
                "Province": ["Agadir Ida Outanane", "Inezgane Aït Melloul", "Chtouka Aït Baha", "Taroudant", "Tiznit", "Tata", "Région Souss-Massa"],
                "Garçons 2018": [6233, 6236, 4961, 9248, 1923, 1288, 29889],
                "Filles 2018": [6187, 6016, 4666, 8826, 1905, 1152, 28752],
                "Total 2018": [12420, 12252, 9627, 18074, 3826, 2440, 58639]
            }
        },
        "personnel_enseignant_sexe": {
            "2017": {
                "Province": ["Agadir Ida Outanane", "Inezgane Ait Melloul", "Chtouka Ait Baha", "Taroudant", "Tiznit", "Tata", "Total"],
                "Hommes 2017": [769, 773, 1303, 3185, 837, 509, 7376],
                "Femmes 2017": [1022, 874, 619, 2073, 385, 310, 5283],
                "Total 2017": [1791, 1647, 1922, 5258, 1222, 819, 12659]
            },
            "2018": {
                "Province": ["Agadir Idaoutanane", "Inezgane Ait Melloul", "Chtouka Ait Baha", "Taroudant", "Tiznit", "Tata", "Total région Souss-Massa"],
                "Hommes 2018": [816, 830, 1334, 3048, 890, 494, 7412],
                "Femmes 2018": [1101, 942, 728, 2137, 411, 339, 5658],
                "Total 2018": [1917, 1772, 2062, 5185, 1301, 833, 13070]
            }
        },
        "eleves_primaire_public_par_niveau": {
            "2017": {
                "Province": ["Agadir Ida Outanane", "Inezgane Aït Melloul", "Chtouka Aït Baha", "Taroudant", "Tiznit", "Tata", "Total"],
                "1ère": [9290, 9732, 9671, 21207, 3463, 2767, 56130],
                "2ème": [8712, 9524, 8985, 19593, 3375, 2627, 52816],
                "3ème": [8906, 9350, 8778, 19727, 3342, 2607, 52710],
                "4ème": [8642, 9281, 8394, 18295, 3339, 2432, 50383],
                "5ème": [8205, 9180, 7836, 17911, 3176, 2439, 48747],
                "6ème": [9456, 9857, 8144, 17800, 3471, 2531, 51259],
                "Total": [53211, 56924, 51808, 114533, 20166, 15403, 312045]
            },
            "2018": {
                "Province": ["Agadir Idaoutanane", "Inezgane Ait Melloul", "Chtouka Ait Baha", "Taroudant", "Tiznit", "Tata", "Total Région Souss-Massa"],
                "1ère": [9311, 9828, 10013, 20369, 3535, 2779, 55835],
                "2ème": [9025, 9743, 9436, 19931, 3390, 2569, 54094],
                "3ème": [8923, 9623, 9163, 19811, 3298, 2647, 53465],
                "4ème": [8931, 9534, 8661, 19014, 3324, 2523, 51987],
                "5ème": [8673, 9232, 8322, 17986, 3291, 2377, 49881],
                "6ème": [8826, 10737, 8245, 18006, 3337, 2408, 51559],
                "Total": [53689, 58697, 53840, 115117, 20175, 15303, 316821]
            }
        }
    },
    "sante": {
        "infrastructure_sante_publique_2017": {
            "Province": ["Agadir Ida Outanane", "Inezgane Ait Melloul", "Chtouka Ait Baha", "Taroudant", "Tiznit", "Tata", "Total"],
            "Hôpitaux généraux": [1, 1, 1, 2, 1, 1, 7],
            "Hôpitaux spécialisés": [1, 0, 0, 0, 1, 0, 2],
            "Centres de santé urbains avec lits d'accouchement": [3, 3, 1, 6, 1, 3, 17],
            "Centres de santé urbains sans lits d'accouchement": [10, 11, 1, 6, 2, 3, 33],
            "Dispensaires ruraux": [14, 4, 13, 28, 29, 13, 101],
            "Centres de santé ruraux sans lits d'accouchement": [4, 1, 9, 61, 11, 8, 94],
            "Centres de santé ruraux avec lits d'accouchement": [4, 1, 11, 19, 12, 8, 55]
        },
        "lits_hopitaux_publics_2017": {
            "Province": ["Agadir Ida Outanane", "Inezgane Ait Melloul", "Chtouka Ait Baha", "Taroudant", "Tiznit", "Tata", "Total"],
            "Hôpitaux généraux": [500, 310, 60, 310, 230, 58, 1468],
            "Hôpitaux spécialisés": [30, 0, 0, 0, 40, 0, 70],
            "Total": [530, 310, 60, 310, 270, 58, 1538]
        }
    },
    "tourisme": {
        "arrivées_touristes_2017": {
            "Nationalite": ["TOTAL", "T.INTERNATIONA", "Europe", "France", "Espagne", "Royaume-Uni", "Allemagne", "Italie", "Scandinavie", "Autriche", "Portugal", "Hollande", "Belgique", "Suisse", "C.E.I", "Hongrie", "Russie", "Pologne", "Amérique du Nord", "U.S.A", "Canada", "Pays Arabes", "Maghreb", "Moyen Orient", "Autres Pays", "Japon", "Chine", "Afrique", "M.R.E", "Autres", "T.NATIONAL"],
            "Tiznit-Arrivees": [8368, 2917, 2400, 875, 321, 107, 475, 187, 64, 20, 80, 106, 69, 63, 4, 14, 0, 15, 92, 76, 16, 54, 20, 34, 371, 4, 0, 56, 6, 305, 5451],
            "Tiznit-Nuitees": [12653, 4368, 3505, 1330, 480, 177, 633, 279, 104, 25, 95, 178, 91, 75, 4, 15, 0, 19, 172, 145, 27, 91, 21, 70, 600, 4, 0, 87, 6, 503, 8285],
            "Taroudant-Arrivees": [956, 638, 359, 67, 15, 47, 79, 23, 72, 2, 1, 11, 16, 25, 0, 0, 0, 1, 45, 21, 24, 4, 0, 4, 230, 0, 0, 0, 79, 151, 318],
            "Taroudant-Nuitees": [1090, 720, 410, 82, 16, 52, 91, 31, 79, 2, 1, 11, 17, 27, 0, 0, 0, 1, 49, 23, 26, 4, 0, 4, 257, 0, 0, 0, 92, 165, 370],
            "Inezgane-Arrivees": [10849, 4719, 3975, 2150, 100, 280, 391, 97, 84, 28, 21, 247, 415, 86, 0, 21, 16, 39, 71, 50, 21, 217, 125, 92, 456, 19, 0, 179, 62, 196, 6130],
            "Inezgane-Nuitees": [37346, 21888, 20183, 11107, 207, 1333, 2550, 289, 452, 126, 72, 1187, 1989, 546, 0, 141, 63, 121, 172, 107, 65, 670, 431, 239, 863, 67, 0, 302, 88, 406, 15458],
            "Chtouka-Arrivees": [922, 188, 177, 45, 19, 37, 49, 1, 2, 7, 0, 10, 4, 1, 0, 0, 0, 2, 0, 0, 0, 5, 0, 5, 6, 2, 0, 0, 0, 4, 734],
            "Chtouka-Nuitees": [1012, 205, 194, 50, 20, 41, 54, 1, 2, 8, 0, 11, 4, 1, 0, 0, 0, 2, 0, 0, 0, 5, 0, 5, 6, 2, 0, 0, 0, 4, 807],
            "Agadir-Arrivees": [1033358, 630112, 499157, 147101, 12438, 89951, 121932, 6413, 13447, 1613, 5658, 13441, 29860, 5533, 4, 748, 16941, 34077, 9698, 5969, 3729, 55819, 11555, 44264, 65438, 610, 115, 2046, 499, 62168, 403246],
            "Agadir-Nuitees": [5451124, 4150081, 3613061, 1029468, 47783, 659470, 1010038, 32764, 83142, 10592, 35432, 89983, 267188, 35669, 17, 3156, 134363, 173996, 39904, 22852, 17052, 240791, 54113, 186678, 256325, 1640, 268, 9573, 1628, 243216, 1301043],
            "Tata-Arrivees": [13299, 11062, 9135, 3451, 1332, 302, 1200, 650, 382, 218, 259, 310, 515, 349, 0, 2, 103, 62, 1406, 1033, 373, 189, 53, 136, 332, 25, 0, 13, 4, 290, 2237],
            "Tata-Nuitees": [16958, 13759, 11400, 4242, 1603, 394, 1477, 839, 516, 266, 375, 387, 622, 442, 0, 2, 122, 113, 1618, 1148, 470, 316, 103, 213, 425, 36, 0, 25, 15, 349, 3199],
            "TOTAL-Arrivees": [1067752, 649636, 515203, 153689, 14225, 90724, 124126, 7371, 14051, 1888, 6019, 14125, 30879, 6057, 8, 785, 17060, 34196, 11312, 7149, 4163, 56288, 11753, 44535, 66833, 660, 115, 2294, 650, 63114, 418116],
            "TOTAL-Nuitees": [5520183, 4191021, 3648753, 1046279, 50109, 661467, 1014843, 34203, 84295, 11019, 35975, 91757, 269911, 36760, 21, 3314, 134548, 174252, 41915, 24275, 17640, 241877, 54668, 187209, 258476, 1749, 268, 9987, 1829, 244643, 1329162]
        }
    },
    "énergie": {
        "2017": {
            "nombre_consommateurs_par_type_tension": {
                "Agadir Ida Outanane": {
                    "Basse tension": 227754,
                    "Moyenne tension": 539,
                    "Haute tension": 0,
                    "Total": 228293
                },
                "Inezgane Aït Melloul": {
                    "Basse tension": 147745,
                    "Moyenne tension": 450,
                    "Haute tension": 0,
                    "Total": 148195
                },
                "Chtouka Aït Baha": {
                    "Basse tension": 101735,
                    "Moyenne tension": 1268,
                    "Haute tension": 1,
                    "Total": 103004
                },
                "Taroudant": {
                    "Basse tension": 202408,
                    "Moyenne tension": 2621,
                    "Haute tension": 0,
                    "Total": 205029
                },
                "Tiznit": {
                    "Basse tension": 81344,
                    "Moyenne tension": 167,
                    "Haute tension": 1,
                    "Total": 81512
                },
                "Tata": {
                    "Basse tension": 31825,
                    "Moyenne tension": 122,
                    "Haute tension": 1,
                    "Total": 31948
                },
                "Total": {
                    "Basse tension": 792811,
                    "Moyenne tension": 5167,
                    "Haute tension": 3,
                    "Total": 797981
                }
            },
            "evolution_production_thermique": {
                "Turbines à gaz - Agadir": {
                    "2016": 0.6,
                    "2015": 0.5,
                    "2014": 1.9
                },
                "Total des Turbines à gaz au Maroc": {
                    "2016": 673.2,
                    "2015": 361.6,
                    "2014": 840.3
                },
                "Total de la production thermique au Maroc": {
                    "2016": 25652.3,
                    "2015": 25047.9,
                    "2014": 23987.7
                }
            },
            "consommation_produits_petroliers": {
                "Agadir Ida Outanane": {
                    "Propane (tonne)": 211,
                    "Butane (tonne)": 49518,
                    "Essence super S+O (m³)": 25506,
                    "Gasoil 50 (m³)": 90110
                },
                "Inezgane Aït Melloul": {
                    "Propane (tonne)": 273,
                    "Butane (tonne)": 37174,
                    "Essence super S+O (m³)": 12472,
                    "Gasoil 50 (m³)": 90743
                },
                "Chtouka Aït Baha": {
                    "Propane (tonne)": 75,
                    "Butane (tonne)": 110111,
                    "Essence super S+O (m³)": 6706,
                    "Gasoil 50 (m³)": 76424
                },
                "Taroudant": {
                    "Propane (tonne)": 31,
                    "Butane (tonne)": 52840,
                    "Essence super S+O (m³)": 7109,
                    "Gasoil 50 (m³)": 103302
                },
                "Tiznit": {
                    "Propane (tonne)": 34,
                    "Butane (tonne)": 35176,
                    "Essence super S+O (m³)": 7227,
                    "Gasoil 50 (m³)": 43771
                },
                "Tata": {
                    "Propane (tonne)": None,
                    "Butane (tonne)": None,
                    "Essence super S+O (m³)": None,
                    "Gasoil 50 (m³)": None
                },
                "Total": {
                    "Propane (tonne)": 624,
                    "Butane (tonne)": 284819,
                    "Essence super S+O (m³)": 59020,
                    "Gasoil 50 (m³)": 404350
                }
            }
        },
        "2018": {
            "nombre_consommateurs_par_type_tension": {
                "Agadir Ida Outanane": {
                    "Basse tension": 239768,
                    "Moyenne tension": 553,
                    "Haute tension": 0,
                    "Total": 240321
                },
                "Inezgane Ait Melloul": {
                    "Basse tension": 155613,
                    "Moyenne tension": 455,
                    "Haute tension": 0,
                    "Total": 156068
                },
                "Chtouka Ait Baha": {
                    "Basse tension": 109854,
                    "Moyenne tension": 1309,
                    "Haute tension": 1,
                    "Total": 111164
                },
                "Taroudant": {
                    "Basse tension": 208631,
                    "Moyenne tension": 2674,
                    "Haute tension": 0,
                    "Total": 211305
                },
                "Tiznit": {
                    "Basse tension": 83470,
                    "Moyenne tension": 166,
                    "Haute tension": 1,
                    "Total": 83637
                },
                "Tata": {
                    "Basse tension": 32677,
                    "Moyenne tension": 124,
                    "Haute tension": 1,
                    "Total": 32802
                },
                "Total": {
                    "Basse tension": 830013,
                    "Moyenne tension": 5281,
                    "Haute tension": 3,
                    "Total": 835297
                }
            },
            "evolution_production_thermique": {
                "Turbines à gaz - Agadir": {
                    "2017": 0.1,
                    "2016": 0.6,
                    "2015": 0.5
                },
                "Total des turbines à gaz au Maroc": {
                    "2017": 427.4,
                    "2016": 673.2,
                    "2015": 361.6
                },
                "Total de la production thermique au Maroc": {
                    "2017": 26484.4,
                    "2016": 25652.0,
                    "2015": 25047.9
                }
            },
            "consommation_produits_petroliers": {
                "Agadir Ida Outanane": {
                    "Propane (tonne)": 217,
                    "Butane (tonne)": 51003,
                    "Essence super S+O (m³)": 26271,
                    "Gasoil 50 (m³)": 92813
                },
                "Inezgane Ait Melloul": {
                    "Propane (tonne)": 281,
                    "Butane (tonne)": 38289,
                    "Essence super S+O (m³)": 12846,
                    "Gasoil 50 (m³)": 93465
                },
                "Chtouka Ait Baha": {
                    "Propane (tonne)": 77,
                    "Butane (tonne)": 113414,
                    "Essence super S+O (m³)": 6907,
                    "Gasoil 50 (m³)": 78718
                },
                "Taroudant": {
                    "Propane (tonne)": 32,
                    "Butane (tonne)": 54425,
                    "Essence super S+O (m³)": 7322,
                    "Gasoil 50 (m³)": 106401
                },
                "Tiznit": {
                    "Propane (tonne)": 35,
                    "Butane (tonne)": 36231,
                    "Essence super S+O (m³)": 7444,
                    "Gasoil 50 (m³)": 45084
                }
            }
        }
    }
}
