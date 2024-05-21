import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
import seaborn as sns
import matplotlib.pyplot as plt
import os

import statsmodels.graphics.utils     as     utils
from statsmodels.graphics.factorplots import interaction_plot
from   statsmodels.compat.python      import lrange
from   statsmodels.graphics.plottools import rainbow
from   scipy.stats import norm
from   scipy.stats import sem

# Configurer la page
st.set_page_config(page_title="Tableau de bord GoldenLine", layout="wide")
st.markdown("<h1 style='text-align: center; color: #5A5E6B;'>Tableau de bord GoldenLine</h1>", unsafe_allow_html=True)

# Définir les identifiants de connexion par défaut
DEFAULT_USERNAME = "admin"
DEFAULT_PASSWORD = "1234"

# Fonction de vérification des identifiants
def check_credentials(username, password):
    return username == DEFAULT_USERNAME and password == DEFAULT_PASSWORD

# Interface de connexion
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:

    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    username = st.text_input("Identifiant", key="username", help="Entrez votre identifiant", placeholder="Identifiant", max_chars=50).strip()
    password = st.text_input("Mot de passe", type="password", key="password", help="Entrez votre mot de passe", placeholder="Mot de passe", max_chars=50).strip()
    if st.button("Se connecter", key="login_button"):
        if check_credentials(username, password):
            st.session_state.logged_in = True
            st.experimental_rerun()
        else:
            st.error("Identifiant ou mot de passe incorrect")
    st.markdown('</div>', unsafe_allow_html=True)
else:
    # Chargement des données
    conn = sqlite3.connect('my_database.db')   
    # Lire les données de la table "complete" depuis SQLite
    complete = pd.read_sql('SELECT * FROM complete', conn)

    # Conversion de la colonne 'DATE' en datetime
    complete['DATE'] = pd.to_datetime(complete['DATE'])

    # Création de melted_db
    melted_db = pd.melt(complete, id_vars=['DATE', 'COLLECTE', 'ID', 'CSP', 'ENFANTS', 'PRIX'], var_name='SECTEUR', value_name='DEPENSE')
    melted_db = melted_db.sort_values(by=['COLLECTE']).reset_index(drop=True)

    # Dates par défaut
    start_date = pd.to_datetime('2023-01-01')
    end_date = pd.to_datetime('2023-12-31')

    # Sélection des dates avec Streamlit
    st.sidebar.header("Filtrer par date")
    start_date_picker2 = st.sidebar.date_input('Date de début', value=start_date)
    end_date_picker2 = st.sidebar.date_input('Date de fin', value=end_date)

    # Bouton pour générer la base de données filtrée
    generate_button2 = st.sidebar.button('Générer')

    if generate_button2:
        selected_start = pd.to_datetime(start_date_picker2)
        selected_end = pd.to_datetime(end_date_picker2)
        
        # Filtrer les DataFrames pour la plage de dates sélectionnée
        selected_compl = complete[(complete['DATE'] >= selected_start) & (complete['DATE'] <= selected_end)]
        selected_melt = melted_db[(melted_db['DATE'] >= selected_start) & (melted_db['DATE'] <= selected_end)]

        # Layout en deux colonnes
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("Dépenses par catégorie socioprofessionnelle")
            st.write(selected_melt)

            # Create a histogram plot
            fig1, ax1 = plt.subplots(figsize=(10, 6))
            sns.histplot(x=selected_melt['DEPENSE'], hue=selected_melt['SECTEUR'], kde=True, multiple='stack', binwidth=5, shrink=1, ax=ax1)
            ax1.set_title('Répartition des dépenses par secteur')
            ax1.set_xlabel('Dépenses')
            ax1.set_ylabel('Fréquence')

            # Display the histogram in Streamlit
            st.pyplot(fig1)
    
        with col2:
            st.write("Distribution de la dépense en fonction de la CSP et du secteur d'activité")
            st.write(selected_compl)

            # Create a interaction plot
            fig, ax = plt.subplots(figsize=(10, 6))
            interaction_plot(x = melted_db['CSP'], trace = melted_db['SECTEUR'], response = melted_db['DEPENSE'], ms = 10, ax = ax)
            plt.title("Distribution de la dépense en fonction de la CSP et du secteur d'activité de GoldenLine")
            plt.xticks(rotation = 45)
            plt.xlabel('Catégorie socioprofessionnelle (CSP)', fontsize = 12)
            plt.ylabel('Montant moyen dépensé par achat par segment (en €)', fontsize = 12)

            # Display the histogram in Streamlit
            st.pyplot(fig)


