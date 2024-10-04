import pandas as pd
import pycountry 

# 1. Charger les jeux de données
religion = pd.read_csv('religion.csv')
migrant = pd.read_csv('migrant-stock-total.csv')
life_expectancy = pd.read_csv('life-expectancy.csv')

def normalize_country_name(country_name):
    try:
        # Recherche du pays dans la base de pycountry
        return pycountry.countries.lookup(country_name).name
    except LookupError:
        return country_name 
    

religion['Entity'] = religion['Entity'].apply(normalize_country_name)
migrant['Entity'] = migrant['Entity'].apply(normalize_country_name)
life_expectancy['Entity'] = life_expectancy['Entity'].apply(normalize_country_name)


# 2. Nettoyage du jeu de données religion.csv
# On garde uniquement les colonnes 'Entitym', 'Code', 'Yearm', et 'Importance'
religion_cleaned = religion[['Entity', 'Code', 'Year', "Importance"]]

# Convertir la colonne 'Importance' en entier (integer)
religion_cleaned['Importance'] = religion_cleaned['Importance'].astype(int)

# 3. Nettoyage du jeu de données migrant.csv
# Supprimer les lignes où la colonne 'CODE' a des valeurs manquantes
migrant_cleaned = migrant.dropna(subset=['Code'])

# 4. Nettoyage du jeu de données life-expectancy.csv
# Supprimer les lignes où la colonne 'CODE' a des valeurs manquantes
life_expectancy_cleaned = life_expectancy.dropna(subset=['Code'])

life_expectancy_cleaned.to_csv("life_expectancy_filtres.csv", index = False)
migrant_cleaned.to_csv("migrant_filtres.csv", index = False)
religion_cleaned.to_csv("religion_filtres.csv", index = False)
# 5. Fusionner les trois jeux de données sur la colonne 'Entitym' (ou 'Code' si elle correspond à l'identifiant pays)
#merged_data = pd.merge(religion_cleaned, migrant_cleaned, on=['Entity', 'Code'], how='inner')
#merged_data = pd.merge(merged_data, life_expectancy_cleaned, on=['Entitym', 'Code'], how='inner')

# 6. Exporter les données fusionnées
#merged_data.to_csv('cleaned_merged_data.csv', index=False)

#print("Le nettoyage et la fusion des données sont terminés.")


merged_data = pd.merge(religion_cleaned, migrant_cleaned, on=['Entity', 'Code','Year'], how='outer', suffixes=('_religion', '_migrant'))
merged_data = pd.merge(merged_data, life_expectancy_cleaned, on=['Entity','Code','Year'], how='outer', suffixes=('', '_life_expectancy'))

# 8. Exporter les données fusionnées avec toutes les années
merged_data.to_csv('cleaned_merged_data.csv', index=False)

print("Le nettoyage, la fusion avec toutes les années sont terminés.")
merged_data = pd.merge(religion_cleaned, migrant_cleaned, on=['Entity', 'Code'], how='inner')
merged_data = pd.merge(merged_data, life_expectancy_cleaned, on=['Entity', 'Code'], how='inner')
# 8. Exporter les données fusionnées
merged_data.to_csv("donnees_combinees.csv", index = False)