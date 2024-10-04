import pandas as pd

# Définir la liste des fichiers CSV
files = [
    'C:/Users/maxim/Documents/projetgp/nettoyage_tourisme/international-tourist-trips2013.csv',
    'C:/Users/maxim/Documents/projetgp/nettoyage_tourisme/international-tourist-trips2014.csv',
    'C:/Users/maxim/Documents/projetgp/nettoyage_tourisme/international-tourist-trips2015.csv',
    'C:/Users/maxim/Documents/projetgp/nettoyage_tourisme/international-tourist-trips2016.csv',
    'C:/Users/maxim/Documents/projetgp/nettoyage_tourisme/international-tourist-trips2017.csv',
    'C:/Users/maxim/Documents/projetgp/nettoyage_tourisme/international-tourist-trips2018.csv',
    'C:/Users/maxim/Documents/projetgp/nettoyage_tourisme/international-tourist-trips2019.csv',
    'C:/Users/maxim/Documents/projetgp/nettoyage_tourisme/international-tourist-trips2020.csv',
    'C:/Users/maxim/Documents/projetgp/nettoyage_tourisme/international-tourist-trips2021.csv',
    'C:/Users/maxim/Documents/projetgp/nettoyage_tourisme/international-tourist-trips2022.csv'
]

# Années correspondantes à chaque fichier
years = ['2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022']

# Liste pour stocker les DataFrames
yearly_data = []

# Charger et traiter chaque fichier CSV par morceaux pour économiser de la mémoire
for i, file in enumerate(files):
    chunk_list = []  # Liste pour stocker les morceaux de chaque fichier
    
    # Lire le fichier par morceaux (chunks)
    for chunk in pd.read_csv(file, chunksize=10000, dtype={'Country Code': 'category', 'Country': 'category'}):
        chunk_list.append(chunk)

    # Combiner les morceaux dans un DataFrame
    df = pd.concat(chunk_list)
    
    # Renommer les colonnes pour unifier les noms
    df = df.rename(columns={
        'Entity': 'Country',  # Unifions 'Entity' en 'Country'
        'Code': 'Country Code',  # Unifions 'Code' en 'Country Code'
        'Inbound arrivals of tourists': f'Inbound arrivals of tourists_{years[i]}'  # Ajouter le suffixe de l'année
    })
    
    # Supprimer la colonne 'Year' si elle existe
    if 'Year' in df.columns:
        df = df.drop(columns=['Year'])
    
    # Ajouter le DataFrame à la liste
    yearly_data.append(df)

# Fusionner tous les DataFrames sur la colonne 'Country' en utilisant une jointure externe (outer join)
combined_df = yearly_data[0]
for df in yearly_data[1:]:
    combined_df = pd.merge(combined_df, df, on=['Country', 'Country Code'], how='outer')

# Utiliser melt pour convertir le DataFrame large en format long
long_df = pd.melt(
    combined_df,
    id_vars=['Country', 'Country Code'],  # Colonnes qui ne seront pas fondues
    var_name='Year',                      # Nouvelle colonne pour l'année
    value_name='Inbound Arrivals'         # Nouvelle colonne pour les arrivées de touristes
)

# Nettoyer la colonne 'Year' pour ne contenir que l'année (supprimer le préfixe)
long_df['Year'] = long_df['Year'].str.extract(r'(\d{4})')

# Sauvegarder le DataFrame transformé au format long dans un fichier CSV
long_df.to_csv('tourist_data_long_format.csv', index=False)

print("Les données ont été transformées et enregistrées sous le nom 'tourist_data_long_format.csv'")