#=============================
# Importations libraries
#=============================
import pandas as pd
import country_converter as coco
import os

#=============================
# Fonctions
#=============================
def standardisation(df,nom_col):
    """
    Fonction qui prend en paramètre le df et la colonne nom et la transforme en norme name_short (nom complet)
    puis supprime les lignes not found 
    """
    cc = coco.CountryConverter()
    df[nom_col] = cc.convert(df[nom_col],to = 'name_short')
    df = df[~df[nom_col].str.contains("not found")]
    return df



#=============================
# Importations csv
#=============================
current_dir = os.path.dirname(os.path.abspath(__file__))
countries_path = os.path.join(current_dir, 'countries.csv')
df = pd.read_csv(countries_path)



#=============================
# Traitement et résultat
#=============================
df.drop("Code",inplace=True, axis=1)
df = standardisation(df,"Name")
#Seulement 1 pays est retiré par la standardisation.
df.to_csv("./data/countries.csv",index_label="id_country")
