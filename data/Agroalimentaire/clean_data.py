#=============================
# Importations libraries
#=============================
import pandas as pd
import country_converter as coco
import os
import numpy as np

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


def clean_dataworld(df,ValueName):
    """
    Fonction qui sert à standardiser les données venant de dataworld
    Paramètres : 
    df : tableau de données
    ValueName : nom de la colonne utilitaire

    Retourne :
    Un df standardisé.
    """
    df = df[df['Country Code'].notna()]
    df = df.drop(['Series Name','Series Code'], axis=1)
    df = df.melt(id_vars=["Country Name","Country Code"],
                  var_name="Year",
                  value_name=ValueName)
    df["Year"] = df["Year"].str.slice(0,4)
    df["Year"] = df["Year"].astype('int')
    return df


# ====================================================================================
# ================= Accessibility to proper fuel and cooking equipments ==============
# ====================================================================================

current_dir = os.path.dirname(os.path.abspath(__file__))
countries_path = os.path.join(current_dir, '..', 'countries.csv')
cooking_path = os.path.join(current_dir,'Cooking.csv')

countries = pd.read_csv(countries_path)
df_cooking= pd.read_csv(cooking_path)


result = clean_dataworld(df_cooking,"CleanFuelAndCookingEquipment")


# ================================================================
# ================= Cost of Healthy food table ==============
# ================================================================
healthy_path = os.path.join(current_dir, 'CostHealthyFood.csv')
#Pas de gâchis de variable :
healthy = pd.read_csv(healthy_path, encoding="ISO-8859-1")
#On supprime les colonnes inutiles (là c'est une classification)
healthy.drop(["Classification Name","Classification Code","Country Name","Time Code"], axis=1, inplace=True)
healthy.replace("",np.nan,inplace=True)
#On supprime les NaN qui étaient avant des valeurs vides
healthy.dropna(inplace=True)
#On met les années en int
healthy["Time"] = healthy["Time"].astype('int')
result = result.merge(healthy,how="left", left_on=["Country Code","Year"], right_on=["Country Code","Time"])


#===========================
# Résultat
#===========================
#On supprime la colonne Time
result_agro = result.drop("Time",axis=1)
#On remplace les ".."
result_agro.replace("..","",inplace=True)
result_agro.drop("Country Code",axis=1, inplace=True)
#On standardise les noms des pays : 
result_agro = standardisation(result_agro,"Country Name")

#Enfin, on remplace les noms des pays par leur id dans la table country :
result_agro = result_agro.merge(countries,left_on="Country Name", right_on="Name",how="left")
result_agro = result_agro.drop(["Name","Country Name"],axis=1).rename(columns={'id':'pays_id'})
result_agro.to_csv("result_agro.csv",index_label="id_agro")
