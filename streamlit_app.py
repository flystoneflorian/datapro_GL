# streamlit_app.py
import streamlit as st # type: ignore
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from statsmodels.graphics.factorplots import interaction_plot
from app_functions import check_credentials, load_data, create_melted_db

# Configurer la page
st.set_page_config(page_title="Tableau de bord GoldenLine", layout="wide")
st.markdown("<h1 style='text-align: center; color: #5A5E6B;'>Tableau de bord GoldenLine</h1>", unsafe_allow_html=True)

# Interface de connexion
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    username = st.text_input("Identifiant", key="username")
    password = st.text_input("Mot de passe", type="password", key="password")
    if st.button("Se connecter"):
        if check_credentials(username, password):
            st.session_state.logged_in = True
            st.experimental_rerun()
        else:
            st.error("Identifiant ou mot de passe incorrect")
else:
    # Chargement des données
    complete = load_data()

    # Création de melted_db
    melted_db = create_melted_db(complete)

    # Dates par défaut
    start_date = pd.to_datetime('2020-01-01')
    end_date = pd.to_datetime('today').normalize()

    # Sélection des dates 
    st.sidebar.header("Filtrer par date")
    start_date_picker2 = st.sidebar.date_input('Date de début', value=start_date)
    end_date_picker2 = st.sidebar.date_input('Date de fin', value=end_date)

    # Bouton pour générer la base de données filtrée
    generate_button2 = st.sidebar.button('Générer')

    #Séléction de lignes pour extraction .csv
    st.sidebar.header("extraction de lignes en CSV")
    total_lines = complete.shape[0]
    st.sidebar.write(f"nombre total de lignes : {total_lines}")

    # Saisie des numéros de lignes de début et de fin
    start_line = st.sidebar.number_input("Numero de ligne de début", min_value=1, max_value=total_lines, value=1)
    end_line = st.sidebar.number_input("Numéro de ligne de fin", min_value=1, max_value=total_lines, value=total_lines)

    # Bouton pour générer le CSV
    if st.sidebar.button("Extraire .csv"):
        if start_line > end_line:
            st.sidebar.error("Le numéro de ligne de début doit être inférieur ou égal au numéro de ligne de fin.")
        else:
            extracted_df = complete.iloc[start_line-1:end_line]
            csv = extracted_df.to_csv(index=False)
            st.sidebar.download_button(label="Télécharger le CSV", data=csv, file_name="extracted_lines.csv", mime="text/csv")

    if generate_button2:
        selected_start = pd.to_datetime(start_date_picker2)
        selected_end = pd.to_datetime(end_date_picker2)
        selected_compl = complete[(complete['DATE'] >= selected_start) & (complete['DATE'] <= selected_end)]
        selected_melt = melted_db[(melted_db['DATE'] >= selected_start) & (melted_db['DATE'] <= selected_end)]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("Dépenses par catégorie socioprofessionnelle")
            st.write(selected_compl)
            fig1, ax1 = plt.subplots(figsize=(10, 6))
            sns.histplot(x=selected_melt['DEPENSE'], hue=selected_melt['SECTEUR'], kde=True, multiple='stack', binwidth=5, shrink=1, ax=ax1)
            ax1.set_title('Répartition des dépenses par secteur')
            ax1.set_xlabel('Dépenses')
            ax1.set_ylabel('Fréquence')
            st.pyplot(fig1)
    
        with col2:
            st.write("Distribution de la dépense en fonction de la CSP et du secteur d'activité")
            st.write(selected_melt)
            fig, ax = plt.subplots(figsize=(10, 6))
            interaction_plot(x = melted_db['CSP'], trace = melted_db['SECTEUR'], response = melted_db['DEPENSE'], ms = 10, ax = ax)
            plt.title("Distribution de la dépense en fonction de la CSP et du secteur d'activité de GoldenLine")
            plt.xticks(rotation = 45)
            plt.xlabel('Catégorie socioprofessionnelle (CSP)', fontsize = 12)
            plt.ylabel('Montant moyen dépensé par achat par segment (en €)', fontsize = 12)
            st.pyplot(fig)





