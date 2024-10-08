import pandas as pd
import matplotlib.pyplot as plt
import country_converter as coco
import os
import numpy as np

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

df = pd.read_csv(countries_path)
df_cooking= pd.read_csv(cooking_path)


result = clean_dataworld(df_cooking,"CleanFuelAndCookingEquipment")


# ================================================================
# ================= Cost of Healthy food table ==============
# ================================================================
healthy_path = os.path.join(current_dir, 'CostHealthyFood.csv')
#Pas de gâchis de variable :
healthy = pd.read_csv(healthy_path, encoding="ISO-8859-1")
healthy.drop(["Classification Name","Classification Code","Country Name","Time Code"], axis=1, inplace=True)
healthy.replace("",np.nan,inplace=True)
healthy.dropna(inplace=True)
healthy["Time"] = healthy["Time"].astype('int')
result = result.merge(healthy,how="left", left_on=["Country Code","Year"], right_on=["Country Code","Time"])


#===========================
# Résultat
#===========================
result_agro = result.drop("Time",axis=1)
result_agro.replace("..","",inplace=True)
result_agro.to_csv("result_agro.csv")