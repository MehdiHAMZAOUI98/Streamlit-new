import streamlit as st
from streamlit_folium import folium_static
import pandas as pd
import altair as alt
import geopandas as gpd
import matplotlib.pyplot as plt
import plotly.express as px
import folium
import json
import requests
import numpy as np
import plotly.graph_objects as go
import seaborn as sns
import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart





# Chemins vers les fichiers csv
path_app = "prixloyerAPP.csv"
path_app12 = "prixloyerAPP12.csv"
path_app3 = "prixloyerAPP3.csv"
path_maison = "prixloyerMAISON.csv"

# Lire les fichiers csv en utilisant l'encodage Windows-1252 et en spécifiant les points-virgules comme séparateur de champ
df_app = pd.read_csv(path_app, encoding='Windows-1252', delimiter=';', decimal=',')
df_app12 = pd.read_csv(path_app12, encoding='Windows-1252', delimiter=';', decimal=',')
df_app3 = pd.read_csv(path_app3, encoding='Windows-1252', delimiter=';', decimal=',')
df_maison = pd.read_csv(path_maison, encoding='Windows-1252', delimiter=';', decimal=',')

# Lien vers LinkedIn
linkedin_url = 'https://www.linkedin.com/in/mehdi-raphael-h-415a03204/'

# Lien vers GitHub
github_url = 'https://github.com/MehdiH98'

# Afficher la photo
st.sidebar.image('Mehdilegrand.jpg', width=150)


# Afficher les liens dans une colonne sur le côté gauche
st.sidebar.markdown('### Liens utiles')
st.sidebar.markdown(f'- [LinkedIn]({linkedin_url})')
st.sidebar.markdown(f'- [GitHub]({github_url})')



# Calculer la moyenne du loyer pour chaque type de logement
loyer_app = df_app['loypredm2'].mean()
loyer_maison = df_maison['loypredm2'].mean()
loyer_app12 = df_app12['loypredm2'].mean()
loyer_app3 = df_app3['loypredm2'].mean()

# Créer un dataframe avec les moyennes pour chaque type de logement
df = pd.DataFrame({
    'Type de logement': ['Appartements', 'Maisons', 'Appartements de APP12', 'Appartements de APP3'],
    'Moyenne du loyer (€/m2)': [loyer_app, loyer_maison, loyer_app12, loyer_app3]
})

# Créer la barre de navigation
menu = ['Général', 'Données' , 'Appartement', 'Maison', 'Appartement type T1-T2', 'Appartement type T3 et plus']
page = st.sidebar.selectbox('Navigation', menu)

# Afficher la page sélectionnée
container = st.container()

# Définir les informations de connexion au serveur de messagerie
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = "your-email@example.com"
SMTP_PASSWORD = "your-password"
SENDER_EMAIL = "your-email@example.com"
RECEIVER_EMAIL = "your-email@example.com"

# Fonction pour envoyer un e-mail
def send_email(subject, message):
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())

# Afficher la page de commentaires dans la sidebar
st.sidebar.header("Commentaires")
comment = st.sidebar.text_area("Laissez votre commentaire ici")

# Ajouter un composant de notation en étoiles
rating = st.sidebar.slider("Votre satisfaction", min_value=0, max_value=5, value=0, step=1)

if st.sidebar.button("Envoyer le commentaire"):
    if comment:
        message = f"Commentaire : {comment}\nSatisfaction : {rating} étoile(s)"
        send_email("Nouveau commentaire", message)
        st.sidebar.success("Le commentaire a été envoyé avec succès !")
    else:
        st.sidebar.warning("Veuillez saisir un commentaire avant de l'envoyer.")
        


# Afficher l'histogramme avec Altair dans l'onglet "Général"

if page == 'Général':
    with container:
        st.markdown("<h2><strong>Contexte du projet</strong></h2>", unsafe_allow_html=True)
        st.write("La connaissance du niveau des loyers est importante pour garantir le bon fonctionnement du marché locatif et la conduite des politiques nationales et locales de l’habitat. La Direction Générale de l’Aménagement, du Logement et de la Nature (DGALN) a lancé en 2018 le projet de « carte des loyers » en s’associant d’une part à une équipe de recherche en économie d’Agrosup Dijon et de l’Institut national de la recherche en agronomique (INRAE), et d’autre part à SeLoger et leboncoin. En 2020, le projet a été repris par l’Agence Nationale pour l’Information sur le Logement (ANIL), qui a publié en 2022 une nouvelle version de la carte. Ce partenariat innovant a permis de reconstituer une base de données avec plus de 7 millions d’annonces locatives. A partir de ces données, l’équipe de recherche et l’ANIL ont développé une méthodologie d’estimation d’indicateurs, à l’échelle communale, du loyer (charges comprises) par m² pour les appartements et maisons. Ces indicateurs expérimentaux sont mis en ligne afin d’être utilisables par tous : services de l’Etat, collectivités territoriales, professionnels de l’immobiliers, particuliers bailleurs et locataires. A partir de 2022, les cartes sont actualisées et publiées tous les ans par l’ANIL. Ce projet fournit une information complémentaire à celle offerte par les Observatoires Locaux des Loyers (OLL), déployés depuis 2013 et renforcés depuis 2018 par la loi Elan. Aujourd’hui, ce réseau associatif d’une trentaine d’OLL publie chaque année des informations précises sur les loyers pratiqués dans une cinquantaine d’agglomérations françaises.")

        st.markdown("<br/><br/><br/>", unsafe_allow_html=True)

        st.markdown("<h2>Présentation du jeu de données</h2>", unsafe_allow_html=True)
        st.write("Les données diffusées sont des indicateurs de loyers d’annonces, à l’échelle de la commune. Le champ couvert est la France entière, hors Mayotte. La géographie des communes est celle en vigueur au 1er janvier 2022.")
        st.write("Les indicateurs de loyers sont calculés grâce à l’utilisation des données d’annonces parues sur les plateformes de leboncoin et du Groupe SeLoger sur la période -2018 - 2022.")
        st.write("Les indicateurs de loyers sont fournis charges comprises pour des biens types loués vides et mis en location au 3ème trimestre 2022 avec les caractéristiques de référence suivantes :")
        st.write("- Pour un appartement (toutes typologies confondues) : surface de 52 m² et surface moyenne par pièce de 22,2 m²")
        st.write("- Pour appartement type T1-T2 : surface de 37 m² et surface moyenne par pièce de 22,9 m²")
        st.write("- Pour appartement type T3 et plus : surface de 72 m² et surface moyenne par pièce de 21,2 m²")
        st.write("- Pour une maison : surface de 92 m² et surface moyenne par pièce de 22,3 m²")

        st.markdown("<br/><br/><br/>", unsafe_allow_html=True)

        # Afficher l'histogramme avec Altair
        chart = alt.Chart(df).mark_bar(width=20, size=40).encode(
            x=alt.X('Type de logement', axis=alt.Axis(labels=False, ticks=False)),
            y=alt.Y('Moyenne du loyer (€/m2)', scale=alt.Scale(domain=(0, 15))),
            color=alt.Color('Type de logement', legend=alt.Legend(title="Type de logement"), scale=alt.Scale(scheme='category10')),
            tooltip=['Type de logement', 'Moyenne du loyer (€/m2)']
        ).properties(
            title="Moyenne du loyer par type de logement",
            width=500,
            height=300
        )

        st.altair_chart(chart, use_container_width=True)





    

elif page == 'Données':
    with container:

        def afficher_tableau(code_variable, description, modalites):
            data = {
                'Code Variable': code_variable,
                'Description': description,
                'Modalités/Interprétation': modalites
            }
            df = pd.DataFrame(data)
            st.table(df)

        code_variable = ["id_zone", "INSEE_C", "LIBGEO", "EPCI", "DEP", "REG", "loypredm2", "lwr.IPm2", "upr.IPm2", "TYPPRED", "nbobs_com", "nbobs_mail", "R2_adj"]
        description = ["Identifiant maille", "Code INSEE de la commune", "Nom de la commune", "Siren de l’EPCI", "Code du département", "Code de la région", "Indicateur de loyer en €/m2", "Respectivement borne basse et supérieure de l’intervalle de prédiction à 95% (€/m2)", "L’intervalle de prédiction est une plage de loyers par m².", "Niveau de la prédiction", "Nombre d’observations dans la commune", "Nombre d’observations dans la maille", "Coefficient de détermination ajusté du modèle hédonique servant à l’estimation de l’indicateur de loyer"]
        modalites = ["Identification de la maille utilisée pour l’estimation de l’indicateur", "Géographie au 1er janvier 2022", "", "", "", "", "Loyer d’annonces, charges comprises pour un bien de référence non meublé, pour une annonce mise en ligne au T3 2022", "L’intervalle de prédiction est une plage de loyers par m². La probabilité que l’indicateur de loyers soit réellement compris dans cet intervalle est de 95%. Plus l’intervalle est faible, plus l’indicateur est fiable.", "L’intervalle de prédiction est une plage de loyers par m². La probabilité que l’indicateur de loyers soit réellement compris dans cet intervalle est de 95%. Plus l’intervalle est faible, plus l’indicateur est fiable.", "« Commune » : indicateur de loyer prédit au niveau de la commune (>= 100 observations dans la commune) ou arrondissement pour Paris-Lyon-Marseille\n« epci » : indicateur de loyer prédit au niveau de l'EPCI (>=100 observations dans l'EPCI)\n« maile » : indicateur de loyer prédit au niveau d'une maille (<100 observation)", "Un nombre d’observations inférieur à 30 indique une fiabilité faible de l’indicateur de loyer.", "Un nombre d’observations inférieur à 30 indique une fiabilité faible de l’indicateur de loyer.", "Le coefficient de détermination est d’autant plus élevé que la valeur de l’indicateur est proche des loyers observés dans les annonces.\nLe R², compris entre 0 et 1, est jugé bon quand sa valeur est supérieure à 0,5"]

        st.title("Tableau des variables")

        afficher_tableau(code_variable, description, modalites)

        # Contenu de la page de données
        st.write("Prix des loyers pour un appartement (toutes typologies confondues) :")
        st.write(df_app)

        st.write("Prix des loyers pour un appartement type T1-T2 :")
        st.write(df_app12)

        st.write("Prix des loyers pour un appartement type T3 et plus :")
        st.write(df_app3)

        st.write("Prix des loyers pour une maison :")
        st.write(df_maison)

elif page == 'Appartement':
    with container:


        # Catégorisation de la fiabilité basée sur nbobs_com
        conditions = [
            (df_app['nbobs_com'] >= 100),  # Très fiable
            (df_app['nbobs_com'] >= 50) & (df_app['nbobs_com'] < 100),  # Fiable
            (df_app['nbobs_com'] >= 10) & (df_app['nbobs_com'] < 50),  # Moyennement fiable
            (df_app['nbobs_com'] < 10)  # Peu fiable
        ]

        # Étiquettes correspondantes aux catégories de fiabilité
        labels = ['Très fiable', 'Fiable', 'Moyennement fiable', 'Peu fiable']

        # Ajouter une colonne pour la catégorie de fiabilité basée sur nbobs_com
        df_app['Fiabilite_nbobs_com'] = np.select(conditions, labels, default='Non disponible')

        # Créer un tableau de répartition des communes en fonction du nombre d'observations basé sur nbobs_com
        repartition_observations_nbobs_com = df_app.groupby('Fiabilite_nbobs_com')['nbobs_com'].count().reset_index()

        # Renommer les colonnes du tableau
        repartition_observations_nbobs_com.columns = ['Fiabilité (nbobs_com)', 'Nombre de Communes']

    

        # Définir les couleurs en fonction de la fiabilité
        colors = ['rgb(0, 100, 0)', 'rgb(0, 255, 0)', 'rgb(255, 165, 0)', 'rgb(255, 0, 0)']

        # Créer un histogramme de répartition des communes en fonction de la fiabilité basée sur nbobs_com
        fig = go.Figure(data=[go.Bar(x=repartition_observations_nbobs_com['Fiabilité (nbobs_com)'],
                                    y=repartition_observations_nbobs_com['Nombre de Communes'],
                                    marker=dict(color=colors))])

        # Ajouter un titre à l'histogramme
        fig.update_layout(title_text='Analyse de la fiabilité des indicateurs de loyer basée sur le nombre d’observations dans la commune (nbobs_com)')



        # Afficher l'histogramme
        st.plotly_chart(fig, use_container_width=True)



        # Charger le fichier GeoJSON des régions
        geojson_url = 'https://france-geojson.gregoiredavid.fr/repo/regions.geojson'

        # Créer une carte interactive avec Plotly Express
        fig = px.choropleth_mapbox(df_app, geojson=geojson_url, color="loypredm2",
                           locations="REG", featureidkey="properties.code",
                           center={"lat": 46.2276, "lon": 2.2137}, zoom=5,
                           mapbox_style="carto-positron",
                           color_continuous_scale="Reds")

        # Ajouter un titre au graphique
        fig.update_layout(title_text="Carte des prix des loyers par région")

        # Afficher la carte
        st.plotly_chart(fig, use_container_width=True)


        # Charger le fichier GeoJSON des départements
        geojson_url = 'https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/departements.geojson'

        # Créer une carte interactive avec Plotly Express
        fig = px.choropleth_mapbox(df_app, geojson=geojson_url, color="loypredm2",
                                   locations="DEP", featureidkey="properties.code",
                                   center={"lat": 46.2276, "lon": 2.2137}, zoom=5,
                                   mapbox_style="carto-positron",
                                   color_continuous_scale="Blues")
        
        # Ajouter un titre au graphique
        fig.update_layout(title_text="Carte des prix des loyers par département")

        # Afficher la carte
        st.plotly_chart(fig, use_container_width=True)


        # Charger le fichier GeoJSON des arrondissements
        geojson_url = 'https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/communes-avec-outre-mer.geojson'

        # Créer une carte interactive avec Plotly Express
        fig = px.choropleth_mapbox(df_app, geojson=geojson_url, color="loypredm2",
                                   locations="INSEE_C", featureidkey="properties.code",
                                   center={"lat": 46.2276, "lon": 2.2137}, zoom=5,
                                   mapbox_style="carto-positron",
                                   color_continuous_scale="Greens")
        
        # Ajouter un titre au graphique
        fig.update_layout(title_text="Carte des prix des loyers par commune")

        # Afficher la carte
        st.plotly_chart(fig, use_container_width=True)

        
        # Sélectionner les variables pertinentes pour l'analyse de corrélation
        variables = ["loypredm2", "lwr.IPm2", "upr.IPm2", "TYPPRED", "nbobs_com", "nbobs_mail", "R2_adj"]

        # Lire le fichier CSV en utilisant l'encodage Windows-1252 et en spécifiant les points-virgules comme séparateur de champ
        df_app = pd.read_csv(path_app, encoding='Windows-1252', delimiter=';', decimal=',')

        # Sélectionner les colonnes pertinentes pour l'analyse de corrélation
        data_app = df_app[variables]

        # Calculer la matrice de corrélation
        correlation_matrix = data_app.corr()

        # Créer une copie de la matrice de corrélation pour la mise en couleur
        correlation_colors = correlation_matrix.copy()

        # Remplacer les valeurs de corrélation égales à 1 par np.nan
        correlation_colors = correlation_colors.mask(correlation_colors == 1)

        # Définir les limites de la plage de couleurs en fonction des valeurs minimale et maximale de la matrice de corrélation (en excluant la valeur 1)
        vmin = correlation_matrix[correlation_matrix != 1].min().min()
        vmax = correlation_matrix[correlation_matrix != 1].max().max()

        # Afficher la matrice de graphiques de nuages de points avec mise en couleur et barre de nuance
        fig, ax = plt.subplots()
        ax = sns.heatmap(correlation_colors, annot=True, cmap="RdYlGn", linewidths=0.5, ax=ax, cbar=True, vmin=vmin, vmax=vmax)

        # Inverser l'ordre des noms de variables et les placer en haut
        ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
        ax.set_yticklabels(ax.get_yticklabels(), rotation=0, va="center")

        # Ajouter un titre à l'axe des graphiques
        ax.set_title("Analyse de la corrélation entre les variables")

        st.pyplot(fig)

        # Lire le fichier CSV en utilisant l'encodage Windows-1252 et en spécifiant les points-virgules comme séparateur de champ
        df_app = pd.read_csv(path_app, encoding='Windows-1252', delimiter=';', decimal=',')


        # Afficher l'histogramme des indicateurs de loyer
        plt.figure(figsize=(10, 6))
        sns.histplot(data=df_app, x="loypredm2", kde=True)
        plt.xlabel("Indicateur de loyer (€/m2)")
        plt.ylabel("Nombre d'observations")
        plt.title("Distribution des indicateurs de loyer")
        st.pyplot(plt)

        # Afficher les statistiques descriptives des indicateurs de loyer
        st.write(df_app["loypredm2"].describe())

        # Obtenir la valeur du coefficient de détermination ajusté (R2 ajusté)
        r2_adj = df_app['R2_adj'].iloc[0]

        # Définir le style CSS pour le carré
        square_style = "border: 2px solid black; padding: 10px; display: inline-block;"

        # Définir le style CSS pour la taille de police et le relief
        font_style = "font-size: 20px; text-shadow: 1px 1px 1px #888888;"

        # Afficher le R2 ajusté dans un carré avec une taille de police plus grande et un léger relief
        st.markdown(f'<div style="{square_style} {font_style}">R2 ajusté : {r2_adj:.2f}</div>', unsafe_allow_html=True)

elif page == 'Maison':
    with container:

        # Catégorisation de la fiabilité basée sur nbobs_com
        conditions = [
            (df_maison['nbobs_com'] >= 100),  # Très fiable
            (df_maison['nbobs_com'] >= 50) & (df_maison['nbobs_com'] < 100),  # Fiable
            (df_maison['nbobs_com'] >= 10) & (df_maison['nbobs_com'] < 50),  # Moyennement fiable
            (df_maison['nbobs_com'] < 10)  # Peu fiable
        ]

        # Étiquettes correspondantes aux catégories de fiabilité
        labels = ['Très fiable', 'Fiable', 'Moyennement fiable', 'Peu fiable']

        # Ajouter une colonne pour la catégorie de fiabilité basée sur nbobs_com
        df_maison['Fiabilite_nbobs_com'] = np.select(conditions, labels, default='Non disponible')

        # Créer un tableau de répartition des communes en fonction du nombre d'observations basé sur nbobs_com
        repartition_observations_nbobs_com = df_maison.groupby('Fiabilite_nbobs_com')['nbobs_com'].count().reset_index()

        # Renommer les colonnes du tableau
        repartition_observations_nbobs_com.columns = ['Fiabilité (nbobs_com)', 'Nombre de Communes']

    

        # Définir les couleurs en fonction de la fiabilité
        colors = ['rgb(0, 100, 0)', 'rgb(0, 255, 0)', 'rgb(255, 165, 0)', 'rgb(255, 0, 0)']

        # Créer un histogramme de répartition des communes en fonction de la fiabilité basée sur nbobs_com
        fig = go.Figure(data=[go.Bar(x=repartition_observations_nbobs_com['Fiabilité (nbobs_com)'],
                                    y=repartition_observations_nbobs_com['Nombre de Communes'],
                                    marker=dict(color=colors))])

        # Ajouter un titre à l'histogramme
        fig.update_layout(title_text='Analyse de la fiabilité des indicateurs de loyer basée sur le nombre d’observations dans la commune (nbobs_com)')



        # Afficher l'histogramme
        st.plotly_chart(fig, use_container_width=True)


        # Charger le fichier GeoJSON des régions
        geojson_url = 'https://france-geojson.gregoiredavid.fr/repo/regions.geojson'

        # Créer une carte interactive avec Plotly Express
        fig = px.choropleth_mapbox(df_maison, geojson=geojson_url, color="loypredm2",
                           locations="REG", featureidkey="properties.code",
                           center={"lat": 46.2276, "lon": 2.2137}, zoom=5,
                           mapbox_style="carto-positron",
                           color_continuous_scale="Reds")
        
        # Ajouter un titre au graphique
        fig.update_layout(title_text="Carte des prix des loyers par région")

        # Afficher la carte
        st.plotly_chart(fig, use_container_width=True)


        # Charger le fichier GeoJSON des départements
        geojson_url = 'https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/departements.geojson'

        # Créer une carte interactive avec Plotly Express
        fig = px.choropleth_mapbox(df_maison, geojson=geojson_url, color="loypredm2",
                                   locations="DEP", featureidkey="properties.code",
                                   center={"lat": 46.2276, "lon": 2.2137}, zoom=5,
                                   mapbox_style="carto-positron",
                                   color_continuous_scale="Blues")
        
        # Ajouter un titre au graphique
        fig.update_layout(title_text="Carte des prix des loyers par département")

        # Afficher la carte
        st.plotly_chart(fig, use_container_width=True)

        # Charger le fichier GeoJSON des arrondissements
        geojson_url = 'https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/communes-avec-outre-mer.geojson'

        # Créer une carte interactive avec Plotly Express
        fig = px.choropleth_mapbox(df_maison, geojson=geojson_url, color="loypredm2",
                                   locations="INSEE_C", featureidkey="properties.code",
                                   center={"lat": 46.2276, "lon": 2.2137}, zoom=5,
                                   mapbox_style="carto-positron",
                                   color_continuous_scale="Greens")
        
        # Ajouter un titre au graphique
        fig.update_layout(title_text="Carte des prix des loyers par commune")

        # Afficher la carte
        st.plotly_chart(fig, use_container_width=True)

        # Ajouter un titre au graphique
        fig.update_layout(title_text="Analyse de la corrélation entre les variables")

        # Sélectionner les variables pertinentes pour l'analyse de corrélation
        variables = ["loypredm2", "lwr.IPm2", "upr.IPm2", "TYPPRED", "nbobs_com", "nbobs_mail", "R2_adj"]

        # Lire le fichier CSV en utilisant l'encodage Windows-1252 et en spécifiant les points-virgules comme séparateur de champ
        df_maison = pd.read_csv(path_maison, encoding='Windows-1252', delimiter=';', decimal=',')

        # Sélectionner les colonnes pertinentes pour l'analyse de corrélation
        data_maison = df_maison[variables]

        # Calculer la matrice de corrélation
        correlation_matrix = data_maison.corr()

        # Créer une copie de la matrice de corrélation pour la mise en couleur
        correlation_colors = correlation_matrix.copy()

        # Remplacer les valeurs de corrélation égales à 1 par np.nan
        correlation_colors = correlation_colors.mask(correlation_colors == 1)

        # Définir les limites de la plage de couleurs en fonction des valeurs minimale et maximale de la matrice de corrélation (en excluant la valeur 1)
        vmin = correlation_matrix[correlation_matrix != 1].min().min()
        vmax = correlation_matrix[correlation_matrix != 1].max().max()

        # Afficher la matrice de graphiques de nuages de points avec mise en couleur et barre de nuance
        fig, ax = plt.subplots()
        ax = sns.heatmap(correlation_colors, annot=True, cmap="RdYlGn", linewidths=0.5, ax=ax, cbar=True, vmin=vmin, vmax=vmax)

        # Inverser l'ordre des noms de variables et les placer en haut
        ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
        ax.set_yticklabels(ax.get_yticklabels(), rotation=0, va="center")

        # Ajouter un titre à l'axe des graphiques
        ax.set_title("Analyse de la corrélation entre les variables")

        st.pyplot(fig)


        # Lire le fichier CSV en utilisant l'encodage Windows-1252 et en spécifiant les points-virgules comme séparateur de champ
        df_maison = pd.read_csv(path_app, encoding='Windows-1252', delimiter=';', decimal=',')


        # Afficher l'histogramme des indicateurs de loyer
        plt.figure(figsize=(10, 6))
        sns.histplot(data=df_maison, x="loypredm2", kde=True)
        plt.xlabel("Indicateur de loyer (€/m2)")
        plt.ylabel("Nombre d'observations")
        plt.title("Distribution des indicateurs de loyer")
        st.pyplot(plt)

        # Afficher les statistiques descriptives des indicateurs de loyer
        st.write(df_maison["loypredm2"].describe())

        # Obtenir la valeur du coefficient de détermination ajusté (R2 ajusté)
        r2_adj = df_maison['R2_adj'].iloc[0]

        # Définir le style CSS pour le carré
        square_style = "border: 2px solid black; padding: 10px; display: inline-block;"

        # Définir le style CSS pour la taille de police et le relief
        font_style = "font-size: 20px; text-shadow: 1px 1px 1px #888888;"

        # Afficher le R2 ajusté dans un carré avec une taille de police plus grande et un léger relief
        st.markdown(f'<div style="{square_style} {font_style}">R2 ajusté : {r2_adj:.2f}</div>', unsafe_allow_html=True)

        

elif page == 'Appartement type T1-T2':
    with container:


        # Catégorisation de la fiabilité basée sur nbobs_com
        conditions = [
            (df_app12['nbobs_com'] >= 100),  # Très fiable
            (df_app12['nbobs_com'] >= 50) & (df_app12['nbobs_com'] < 100),  # Fiable
            (df_app12['nbobs_com'] >= 10) & (df_app12['nbobs_com'] < 50),  # Moyennement fiable
            (df_app12['nbobs_com'] < 10)  # Peu fiable
        ]

        # Étiquettes correspondantes aux catégories de fiabilité
        labels = ['Très fiable', 'Fiable', 'Moyennement fiable', 'Peu fiable']

        # Ajouter une colonne pour la catégorie de fiabilité basée sur nbobs_com
        df_app12['Fiabilite_nbobs_com'] = np.select(conditions, labels, default='Non disponible')

        # Créer un tableau de répartition des communes en fonction du nombre d'observations basé sur nbobs_com
        repartition_observations_nbobs_com = df_app12.groupby('Fiabilite_nbobs_com')['nbobs_com'].count().reset_index()

        # Renommer les colonnes du tableau
        repartition_observations_nbobs_com.columns = ['Fiabilité (nbobs_com)', 'Nombre de Communes']

    

        # Définir les couleurs en fonction de la fiabilité
        colors = ['rgb(0, 100, 0)', 'rgb(0, 255, 0)', 'rgb(255, 165, 0)', 'rgb(255, 0, 0)']

        # Créer un histogramme de répartition des communes en fonction de la fiabilité basée sur nbobs_com
        fig = go.Figure(data=[go.Bar(x=repartition_observations_nbobs_com['Fiabilité (nbobs_com)'],
                                    y=repartition_observations_nbobs_com['Nombre de Communes'],
                                    marker=dict(color=colors))])

        # Ajouter un titre à l'histogramme
        fig.update_layout(title_text='Analyse de la fiabilité des indicateurs de loyer basée sur le nombre d’observations dans la commune (nbobs_com)')



        # Afficher l'histogramme
        st.plotly_chart(fig, use_container_width=True)        


        # Charger le fichier GeoJSON des régions
        geojson_url = 'https://france-geojson.gregoiredavid.fr/repo/regions.geojson'

        # Créer une carte interactive avec Plotly Express
        fig = px.choropleth_mapbox(df_app12, geojson=geojson_url, color="loypredm2",
                           locations="REG", featureidkey="properties.code",
                           center={"lat": 46.2276, "lon": 2.2137}, zoom=5,
                           mapbox_style="carto-positron",
                           color_continuous_scale="Reds")
        
        # Ajouter un titre au graphique
        fig.update_layout(title_text="Carte des prix des loyers par région")
        
        # Afficher la carte
        st.plotly_chart(fig, use_container_width=True)


        # Charger le fichier GeoJSON des départements
        geojson_url = 'https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/departements.geojson'

        # Créer une carte interactive avec Plotly Express
        fig = px.choropleth_mapbox(df_app12, geojson=geojson_url, color="loypredm2",
                                   locations="DEP", featureidkey="properties.code",
                                   center={"lat": 46.2276, "lon": 2.2137}, zoom=5,
                                   mapbox_style="carto-positron",
                                   color_continuous_scale="Blues")
        
        # Ajouter un titre au graphique
        fig.update_layout(title_text="Carte des prix des loyers par département")
        
        # Afficher la carte
        st.plotly_chart(fig, use_container_width=True)


        # Charger le fichier GeoJSON des arrondissements
        geojson_url = 'https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/communes-avec-outre-mer.geojson'

        # Créer une carte interactive avec Plotly Express
        fig = px.choropleth_mapbox(df_app12, geojson=geojson_url, color="loypredm2",
                                   locations="INSEE_C", featureidkey="properties.code",
                                   center={"lat": 46.2276, "lon": 2.2137}, zoom=5,
                                   mapbox_style="carto-positron",
                                   color_continuous_scale="Greens")
        
        # Ajouter un titre au graphique
        fig.update_layout(title_text="Carte des prix des loyers par commune")

        # Afficher la carte
        st.plotly_chart(fig, use_container_width=True)
        

        # Sélectionner les variables pertinentes pour l'analyse de corrélation
        variables = ["loypredm2", "lwr.IPm2", "upr.IPm2", "TYPPRED", "nbobs_com", "nbobs_mail", "R2_adj"]

        # Lire le fichier CSV en utilisant l'encodage Windows-1252 et en spécifiant les points-virgules comme séparateur de champ
        df_app12 = pd.read_csv(path_app12, encoding='Windows-1252', delimiter=';', decimal=',')

        # Sélectionner les colonnes pertinentes pour l'analyse de corrélation
        data_app12 = df_app12[variables]

        # Calculer la matrice de corrélation
        correlation_matrix = data_app12.corr()

        # Créer une copie de la matrice de corrélation pour la mise en couleur
        correlation_colors = correlation_matrix.copy()

        # Remplacer les valeurs de corrélation égales à 1 par np.nan
        correlation_colors = correlation_colors.mask(correlation_colors == 1)

        # Définir les limites de la plage de couleurs en fonction des valeurs minimale et maximale de la matrice de corrélation (en excluant la valeur 1)
        vmin = correlation_matrix[correlation_matrix != 1].min().min()
        vmax = correlation_matrix[correlation_matrix != 1].max().max()

        # Afficher la matrice de graphiques de nuages de points avec mise en couleur et barre de nuance
        fig, ax = plt.subplots()
        ax = sns.heatmap(correlation_colors, annot=True, cmap="RdYlGn", linewidths=0.5, ax=ax, cbar=True, vmin=vmin, vmax=vmax)

        # Inverser l'ordre des noms de variables et les placer en haut
        ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
        ax.set_yticklabels(ax.get_yticklabels(), rotation=0, va="center")

        # Ajouter un titre à l'axe des graphiques
        ax.set_title("Analyse de la corrélation entre les variables")

        st.pyplot(fig)


        # Lire le fichier CSV en utilisant l'encodage Windows-1252 et en spécifiant les points-virgules comme séparateur de champ
        df_app12 = pd.read_csv(path_app12, encoding='Windows-1252', delimiter=';', decimal=',')


        # Afficher l'histogramme des indicateurs de loyer
        plt.figure(figsize=(10, 6))
        sns.histplot(data=df_app12, x="loypredm2", kde=True)
        plt.xlabel("Indicateur de loyer (€/m2)")
        plt.ylabel("Nombre d'observations")
        plt.title("Distribution des indicateurs de loyer")
        st.pyplot(plt)

        # Afficher les statistiques descriptives des indicateurs de loyer
        st.write(df_app12["loypredm2"].describe())

        # Lire le fichier CSV en utilisant l'encodage Windows-1252 et en spécifiant les points-virgules comme séparateur de champ
        df_app12 = pd.read_csv(path_app12, encoding='Windows-1252', delimiter=';', decimal=',')


        # Boxplot des indicateurs de loyer prédits par niveau de prédiction
        plt.figure(figsize=(10, 6))
        sns.boxplot(data=df_app12, x="TYPPRED", y="loypredm2")
        plt.xlabel("Niveau de prédiction")
        plt.ylabel("Indicateur de loyer (€/m2)")
        plt.title("Comparaison des indicateurs de loyer prédits")
        st.pyplot(plt)

        # Statistiques descriptives des indicateurs de loyer prédits par niveau de prédiction
        st.write(df_app12.groupby("TYPPRED")["loypredm2"].describe())

        # Charger le fichier CSV en utilisant l'encodage Windows-1252 et en spécifiant les points-virgules comme séparateur de champ
        df_app12 = pd.read_csv(path_app12, encoding='Windows-1252', delimiter=';', decimal=',')

        # Obtenir la valeur du coefficient de détermination ajusté (R2 ajusté)
        r2_adj = df_app12['R2_adj'].iloc[0]

        # Définir le style CSS pour le carré
        square_style = "border: 2px solid black; padding: 10px; display: inline-block;"

        # Définir le style CSS pour la taille de police et le relief
        font_style = "font-size: 20px; text-shadow: 1px 1px 1px #888888;"

        # Afficher le R2 ajusté dans un carré avec une taille de police plus grande et un léger relief
        st.markdown(f'<div style="{square_style} {font_style}">R2 ajusté : {r2_adj:.2f}</div>', unsafe_allow_html=True)


elif page == 'Appartement type T3 et plus':
    with container:

        # Catégorisation de la fiabilité basée sur nbobs_com
        conditions = [
            (df_app3['nbobs_com'] >= 100),  # Très fiable
            (df_app3['nbobs_com'] >= 50) & (df_app3['nbobs_com'] < 100),  # Fiable
            (df_app3['nbobs_com'] >= 10) & (df_app3['nbobs_com'] < 50),  # Moyennement fiable
            (df_app3['nbobs_com'] < 10)  # Peu fiable
        ]

        # Étiquettes correspondantes aux catégories de fiabilité
        labels = ['Très fiable', 'Fiable', 'Moyennement fiable', 'Peu fiable']

        # Ajouter une colonne pour la catégorie de fiabilité basée sur nbobs_com
        df_app3['Fiabilite_nbobs_com'] = np.select(conditions, labels, default='Non disponible')

        # Créer un tableau de répartition des communes en fonction du nombre d'observations basé sur nbobs_com
        repartition_observations_nbobs_com = df_app3.groupby('Fiabilite_nbobs_com')['nbobs_com'].count().reset_index()

        # Renommer les colonnes du tableau
        repartition_observations_nbobs_com.columns = ['Fiabilité (nbobs_com)', 'Nombre de Communes']

    

        # Définir les couleurs en fonction de la fiabilité
        colors = ['rgb(0, 100, 0)', 'rgb(0, 255, 0)', 'rgb(255, 165, 0)', 'rgb(255, 0, 0)']

        # Créer un histogramme de répartition des communes en fonction de la fiabilité basée sur nbobs_com
        fig = go.Figure(data=[go.Bar(x=repartition_observations_nbobs_com['Fiabilité (nbobs_com)'],
                                    y=repartition_observations_nbobs_com['Nombre de Communes'],
                                    marker=dict(color=colors))])

        # Ajouter un titre à l'histogramme
        fig.update_layout(title_text='Analyse de la fiabilité des indicateurs de loyer basée sur le nombre d’observations dans la commune (nbobs_com)')



        # Afficher l'histogramme
        st.plotly_chart(fig, use_container_width=True)


        # Charger le fichier GeoJSON des régions
        geojson_url = 'https://france-geojson.gregoiredavid.fr/repo/regions.geojson'

        # Créer une carte interactive avec Plotly Express
        fig = px.choropleth_mapbox(df_app3, geojson=geojson_url, color="loypredm2",
                           locations="REG", featureidkey="properties.code",
                           center={"lat": 46.2276, "lon": 2.2137}, zoom=5,
                           mapbox_style="carto-positron",
                           color_continuous_scale="Reds")
        
        # Ajouter un titre au graphique
        fig.update_layout(title_text="Carte des prix des loyers par région")

        # Afficher la carte
        st.plotly_chart(fig, use_container_width=True)


        # Charger le fichier GeoJSON des départements
        geojson_url = 'https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/departements.geojson'

        # Créer une carte interactive avec Plotly Express
        fig = px.choropleth_mapbox(df_app3, geojson=geojson_url, color="loypredm2",
                                   locations="DEP", featureidkey="properties.code",
                                   center={"lat": 46.2276, "lon": 2.2137}, zoom=5,
                                   mapbox_style="carto-positron",
                                   color_continuous_scale="Blues")

        # Ajouter un titre au graphique
        fig.update_layout(title_text="Carte des prix des loyers par département")

        # Afficher la carte
        st.plotly_chart(fig, use_container_width=True)
        

        # Charger le fichier GeoJSON des arrondissements
        geojson_url = 'https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/communes-avec-outre-mer.geojson'

        # Créer une carte interactive avec Plotly Express
        fig = px.choropleth_mapbox(df_app3, geojson=geojson_url, color="loypredm2",
                                   locations="INSEE_C", featureidkey="properties.code",
                                   center={"lat": 46.2276, "lon": 2.2137}, zoom=5,
                                   mapbox_style="carto-positron",
                                   color_continuous_scale="Greens")
        
        # Ajouter un titre au graphique
        fig.update_layout(title_text="Carte des prix des loyers par commune")

        # Afficher la carte
        st.plotly_chart(fig, use_container_width=True)



        # Sélectionner les variables pertinentes pour l'analyse de corrélation
        variables = ["loypredm2", "lwr.IPm2", "upr.IPm2", "TYPPRED", "nbobs_com", "nbobs_mail", "R2_adj"]

        # Lire le fichier CSV en utilisant l'encodage Windows-1252 et en spécifiant les points-virgules comme séparateur de champ
        df_app3 = pd.read_csv(path_app3, encoding='Windows-1252', delimiter=';', decimal=',')

        # Sélectionner les colonnes pertinentes pour l'analyse de corrélation
        data_app3 = df_app3[variables]

        # Calculer la matrice de corrélation
        correlation_matrix = data_app3.corr()

        # Créer une copie de la matrice de corrélation pour la mise en couleur
        correlation_colors = correlation_matrix.copy()

        # Remplacer les valeurs de corrélation égales à 1 par np.nan
        correlation_colors = correlation_colors.mask(correlation_colors == 1)

        # Définir les limites de la plage de couleurs en fonction des valeurs minimale et maximale de la matrice de corrélation (en excluant la valeur 1)
        vmin = correlation_matrix[correlation_matrix != 1].min().min()
        vmax = correlation_matrix[correlation_matrix != 1].max().max()

        # Afficher la matrice de graphiques de nuages de points avec mise en couleur et barre de nuance
        fig, ax = plt.subplots()
        ax = sns.heatmap(correlation_colors, annot=True, cmap="RdYlGn", linewidths=0.5, ax=ax, cbar=True, vmin=vmin, vmax=vmax)

        # Inverser l'ordre des noms de variables et les placer en haut
        ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
        ax.set_yticklabels(ax.get_yticklabels(), rotation=0, va="center")

        # Ajouter un titre à l'axe des graphiques
        ax.set_title("Analyse de la corrélation entre les variables")

        st.pyplot(fig)

        # Lire le fichier CSV en utilisant l'encodage Windows-1252 et en spécifiant les points-virgules comme séparateur de champ
        df_app3 = pd.read_csv(path_app12, encoding='Windows-1252', delimiter=';', decimal=',')


        # Afficher l'histogramme des indicateurs de loyer
        plt.figure(figsize=(10, 6))
        sns.histplot(data=df_app3, x="loypredm2", kde=True)
        plt.xlabel("Indicateur de loyer (€/m2)")
        plt.ylabel("Nombre d'observations")
        plt.title("Distribution des indicateurs de loyer")
        st.pyplot(plt)

        # Afficher les statistiques descriptives des indicateurs de loyer
        st.write(df_app3["loypredm2"].describe())

        # Obtenir la valeur du coefficient de détermination ajusté (R2 ajusté)
        r2_adj = df_app3['R2_adj'].iloc[0]

        # Définir le style CSS pour le carré
        square_style = "border: 2px solid black; padding: 10px; display: inline-block;"

        # Définir le style CSS pour la taille de police et le relief
        font_style = "font-size: 20px; text-shadow: 1px 1px 1px #888888;"

        # Afficher le R2 ajusté dans un carré avec une taille de police plus grande et un léger relief
        st.markdown(f'<div style="{square_style} {font_style}">R2 ajusté : {r2_adj:.2f}</div>', unsafe_allow_html=True)

pip install pipreqs
pipreqs --encoding=utf8