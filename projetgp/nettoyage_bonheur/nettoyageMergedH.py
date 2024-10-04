import pandas as pd

# Charger le fichier CSV
df = pd.read_csv('bonheur_combined_cleaned2.csv')

# Remplacer les valeurs vides ("") par NaN
df = df.replace("", pd.NA)

# Unifier les colonnes "Happiness Rank", "Happiness.Rank" et "Overall rank"
df['Happiness Rank'] = df['Happiness Rank'].combine_first(df['Happiness.Rank'])
df['Happiness Rank'] = df['Happiness Rank'].combine_first(df['Overall rank'])

# Unifier les colonnes "Happiness Score" et "Happiness.Score"
df['Happiness Score'] = df['Happiness Score'].combine_first(df['Happiness.Score'])

# Unifier les colonnes "Health (Life Expectancy)" et "Health..Life.Expectancy."
df['Health (Life Expectancy)'] = df['Health (Life Expectancy)'].combine_first(df['Health..Life.Expectancy.'])

# Unifier les colonnes "Trust (Government Corruption)", "Trust..Government.Corruption." et "Perceptions of corruption"
df['Trust (Government Corruption)'] = df['Trust (Government Corruption)'].combine_first(df['Trust..Government.Corruption.'])
df['Trust (Government Corruption)'] = df['Trust (Government Corruption)'].combine_first(df['Perceptions of corruption'])

# Unifier les colonnes "Economy (GDP per Capita)" et "GDP per capita"
df['Economy (GDP per Capita)'] = df['Economy (GDP per Capita)'].combine_first(df['GDP per capita'])
df['Economy (GDP per Capita)'] = df['Economy (GDP per Capita)'].combine_first(df['Economy..GDP.per.Capita.'])

# Supprimer les colonnes dupliquées
df = df.drop(columns=[
    'Happiness.Rank', 'Overall rank', 'Happiness.Score', 'Health..Life.Expectancy.', 
    'Trust..Government.Corruption.', 'Perceptions of corruption', 'GDP per capita','Economy..GDP.per.Capita.',"Region"
])

# Supprimer les colonnes non nécessaires, y compris "Social support"
columns_to_drop = ['Family', 'Standard Error', 'Freedom', 'Dystopia Residual', 'Lower Confidence Interval',
                   'Upper Confidence Interval', 'Whisker.high', 'Whisker.low', 'Dystopia.Residual', 'Social support']
df = df.drop(columns=columns_to_drop, errors='ignore')  # Supprimer les colonnes

# Supprimer les colonnes avec des valeurs vides (NaN)
df = df.dropna(axis=1, how='all')

# Sauvegarder le DataFrame final dans un nouveau fichier CSV
cols = list(df.columns)
cols.insert(1, cols.pop(cols.index('Year')))  # Déplacer 'Year' à la deuxième position
df = df[cols]
df = df.sort_values(by='Country')  # Trier les données par ordre alphabétique des pays
df.to_csv('bonheur_combined_cleaned_final.csv', index=False)

print("Colonnes unifiées, colonnes supplémentaires supprimées, et données enregistrées sous 'bonheur_combined_cleaned_final.csv'")