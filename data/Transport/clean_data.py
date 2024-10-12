#=============================
# Importations libraries
#=============================
import pandas as pd
import country_converter as coco
import os

#=============================
# Importations csv
#=============================
current_dir = os.path.dirname(os.path.abspath(__file__))
countries_path = os.path.join(current_dir, '..', 'countries.csv')
public_transport_path = os.path.join(current_dir,'public_transport.csv')
countries = pd.read_csv(countries_path)
result_transport = pd.read_csv(public_transport_path)


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
# Traitements
#=============================
# On supprime la colonne Code : 
result_transport = result_transport.drop("Code",axis=1)

#On standardise le nom des pays : 
result_transport = standardisation(result_transport,"Entity")
#Enfin, on remplace les noms des pays par leur id dans la table country :
result_transport = result_transport.merge(countries,left_on="Entity", right_on="Name",how="left")
result_transport = result_transport.drop(["Name","Entity"],axis=1).rename(columns={'id':'pays_id'})
#=============================
# Résultat
#=============================
result_transport.to_csv("result_transport.csv", index_label="id_transport")