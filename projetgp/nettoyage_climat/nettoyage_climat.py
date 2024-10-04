import pandas as pd

# 1. Charger les données climatiques
df_climat = pd.read_csv("nettoyage_climat\daily_weather_data.csv")

# 2. Supprimer les colonnes 'Latitude' et 'Longitude'
df_climat = df_climat.drop(columns=['Latitude', 'Longitude'])

# 3. Convertir la colonne 'date' en format datetime pour faciliter le travail avec les dates
df_climat['date'] = pd.to_datetime(df_climat['date'], format='%d-%m-%Y')

# 4. Créer une fonction pour définir les saisons basées sur les dates en France
def determiner_saison(date):
    jour_annee = date.timetuple().tm_yday
    if jour_annee >= 80 and jour_annee < 172:
        return 'Printemps'
    elif jour_annee >= 172 and jour_annee < 264:
        return 'Été'
    elif jour_annee >= 264 and jour_annee < 355:
        return 'Automne'
    else:
        return 'Hiver'

# 5. Appliquer la fonction pour créer une nouvelle colonne 'saison'
df_climat['saison'] = df_climat['date'].apply(determiner_saison)

# 6. Extraire l'année pour chaque ligne
df_climat['année'] = df_climat['date'].dt.year

# 7. Calculer les moyennes de la température minimale, maximale et moyenne par saison, par pays et par année
moyennes_saison_pays = df_climat.groupby(['année', 'country', 'saison']).agg({
    'tmin': 'mean',  # Moyenne de la température minimale
    'tmax': 'mean',  # Moyenne de la température maximale
    'tavg': 'mean'   # Moyenne de la température moyenne
}).reset_index()

# 8. Réorganiser le tableau pour avoir une ligne par année et pays, avec des colonnes pour chaque saison
moyennes_pivot = moyennes_saison_pays.pivot_table(index=['année', 'country'], columns='saison', 
                                                  values=['tmin', 'tmax', 'tavg'], aggfunc='mean')

# 9. Aplatir les colonnes après le pivot et renommer les colonnes pour inclure la saison dans le nom
moyennes_pivot.columns = [f'{saison}_{col}' for col, saison in moyennes_pivot.columns]
moyennes_pivot = moyennes_pivot.reset_index()

# 10. Sauvegarder le DataFrame final dans un fichier CSV
moyennes_pivot.to_csv('moyennes_temperatures_saisons_pays_final.csv', index=False)

print("Calcul des moyennes saisonnières terminé et enregistré dans 'moyennes_temperatures_saisons_pays_final.csv'")
