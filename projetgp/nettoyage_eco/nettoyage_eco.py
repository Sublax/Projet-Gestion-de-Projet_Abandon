import pandas as pd

# Charger le fichier CSV
df = pd.read_csv('nettoyage_eco/dataeco.csv')

# 1. Remplacer les valeurs vides ("") par NaN
df = df.replace("", pd.NA)

# 2. Vérifier quelles colonnes existent dans le DataFrame
print("Colonnes disponibles dans le DataFrame :", df.columns)

# 3. Définir les colonnes que vous souhaitez convertir en numériques (si elles existent)
colonnes_numeriques = ['AMA exchange rate', 'IMF based exchange rate', 'Population', 'Per capita GNI', 
                       'Agriculture', 'Household_Consumption', 'GNI_USD', 'GDP']

# Filtrer uniquement les colonnes qui existent dans le DataFrame
colonnes_existantes = [col for col in colonnes_numeriques if col in df.columns]  # Utiliser 'if' au lieu de 'si'

# 4. Convertir uniquement les colonnes existantes en numériques
df[colonnes_existantes] = df[colonnes_existantes].apply(pd.to_numeric, errors='coerce')

# 5. Supprimer les colonnes avec trop de NaN (plus de 50%)
df = df.dropna(thresh=len(df)*0.5, axis=1)

colonnes_a_supprimer = [' Changes in inventories ', '"Mining, Manufacturing, Utilities (ISIC C-E)"']
df = df.drop(columns=colonnes_a_supprimer, errors='ignore')

# 6. Renommer les colonnes pour simplifier les noms longs
df = df.rename(columns={
    'Agriculture, hunting, forestry, fishing (ISIC A-B)': 'Agriculture',
    'Wholesale, retail trade, restaurants and hotels (ISIC G-H)': 'Trade_Restaurants_Hotels',
    'Transport, storage and communication (ISIC I)': 'Transport_Communication',
    'Mining, Manufacturing, Utilities (ISIC C-E)': 'Mining_Manufacturing_Utilities',
    'Household consumption expenditure (including Non-profit institutions serving households)': 'Household_Consumption',
    'Gross National Income(GNI) in USD': 'GNI_USD',
    'Gross Domestic Product (GDP)': 'GDP'
})
# 7. Enregistrer le DataFrame nettoyé dans un nouveau fichier CSV
df.to_csv('dataeco_cleaned.csv', index=False)

print("Nettoyage de la base de données terminé et enregistré sous 'dataeco_cleaned.csv'")
