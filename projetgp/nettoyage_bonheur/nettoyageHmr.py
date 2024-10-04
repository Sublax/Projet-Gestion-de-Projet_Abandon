import pandas as pd

# Définir les chemins des fichiers CSV
files = [
    'nettoyage_bonheur/2015h.csv',
    'nettoyage_bonheur/2016h.csv',
    'nettoyage_bonheur/2017h.csv',
    'nettoyage_bonheur/2018h.csv',
    'nettoyage_bonheur/2019h.csv'
]

# Années correspondantes à chaque fichier
years = ['2015', '2016', '2017', '2018', '2019']

# Liste pour stocker les DataFrames
dataframes = []

# Fonction pour renommer les colonnes de manière uniforme
def rename_columns(df, year):
    # Unifier les noms des colonnes qui signifient la même chose
    df = df.rename(columns={
        'Country or region': 'Country',
        'Happiness Score': 'Happiness Score',
        'Score': 'Happiness Score',  # Unifier les deux noms pour la note de bonheur
        'Happiness Rank': 'Happiness Rank',
        'Economy (GDP per Capita)': 'Economy (GDP per Capita)',
        'Health (Life Expectancy)': 'Health (Life Expectancy)',
        'Healthy life expectancy': 'Health (Life Expectancy)',  # Unifier les noms relatifs à la santé
        'Freedom to make life choices': 'Freedom',
        'Trust (Government Corruption)': 'Trust (Government Corruption)',
        'Perception of corruption': 'Trust (Government Corruption)',  # Unifier les noms pour la corruption
        'Generosity': 'Generosity',
        'Dystopia Residual': 'Dystopia Residual',
        'Family': 'Family'
    })
    # Ajouter la colonne de l'année
    df['Year'] = year
    return df

# Charger et traiter chaque fichier CSV
for i, file in enumerate(files):
    df = pd.read_csv(file)
    df = rename_columns(df, years[i])
    
    # S'assurer que toutes les colonnes existent, même avec des valeurs NaN
    expected_columns = [
        'Country', 'Happiness Rank', 'Happiness Score', 'Economy (GDP per Capita)',
        'Family', 'Health (Life Expectancy)', 'Freedom', 'Trust (Government Corruption)',
        'Generosity', 'Dystopia Residual', 'Year'
    ]
    for col in expected_columns:
        if col not in df.columns:
            df[col] = pd.NA  # Remplir les colonnes manquantes avec NaN
    
    dataframes.append(df)

# Concaténer tous les DataFrames en un seul DataFrame
combined_df = pd.concat(dataframes, ignore_index=True)

# Enregistrer le DataFrame combiné au format CSV
combined_df.to_csv('bonheur_combined_cleaned2.csv', index=False)

print("Données combinées et enregistrées sous 'bonheur_combined_cleaned.csv'")