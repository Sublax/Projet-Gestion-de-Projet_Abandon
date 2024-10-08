

import pandas as pd
import matplotlib.pyplot as plt
import country_converter as coco
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

countries_path = os.path.join(current_dir, '..', 'countries.csv')
agro_path = os.path.join(current_dir,'..','Agroalimentaire','global-food-prices.csv')

df = pd.read_csv(countries_path)
agro = pd.read_csv(agro_path)


def perf_coco(df2):
    """
    Fonction perf_coco -
    Paramètre : 
    - df2 : colonne de nom de pays à valeur unique

    Sortie : Comparaison entre aucun changement, coco_convert en name short et coco_convert en ISO2
    """
    print("===== Performance sans changement : ======")
    set_pays = set(df["Name"])
    set_df2 = set(df2)
    valeurs_communes = set_pays.intersection(set_df2)
    print(f"Valeur communes : {len(valeurs_communes)}/{len(df2)}")

    print("===== Performance short name pays : ======")
    set_df2 = set(coco.convert(names=df2,to='name_short'))
    valeurs_communes = set_pays.intersection(set_df2)
    print(f"Valeur communes : {len(valeurs_communes)}/{len(df2)}")

    print("===== Performance code pays : ======")
    set_pays = set(df["Code"])
    set_df2 = set(coco.convert(names=df2,to='ISO2'))
    valeurs_communes = set_pays.intersection(set_df2)
    print(f"Valeur communes : {len(valeurs_communes)}/{len(df2)}")



pays_agro = pd.unique(agro["adm0_name"])
perf_coco(pays_agro)


eco_path = os.path.join(current_dir, 'global_gdp.csv')
wage_path = os.path.join(current_dir, 'minimum_wage.csv')

eco = pd.read_csv(eco_path)
lst = pd.unique(eco["Entity"])
perf_coco(lst)

wage = pd.read_csv(wage_path)
perf_coco(wage["country"])


# +
## On voit qu'il y le plus de ressemblance grâce à ISO2, on utilisera
## cette standardisation pour la suite.

def standardisation(col):
    """
    Fonction qui prend en paramètre une colonne nom et la transforme en norme ISO2 
    """
    cc = coco.CountryConverter()
    col = cc.convert(col,to = 'ISO3')
    return col


# -

wage["country"] = standardisation(wage["country"])

result = pd.merge(eco,wage,left_on="Code", right_on="country", how="left")
result

## ================= Unemployment table =================
unemployment_path = os.path.join(current_dir, 'Unemployment.csv')

unemployment = pd.read_csv(unemployment_path)
#On supprime les lignes vide de Country code qui sont 1) des données non pratiquables 2) la source des données
unemployment = unemployment[unemployment['Country Code'].notna()]
#Et on supprime les colonnes Series et Series Code qui sont inutiles pour l'avenir
unemployment = unemployment.drop(['Series','Series Code'], axis=1)


# +
#On fait en sorte que les années soient par colonne pour standardiser les df.
UN_rate = unemployment.melt(id_vars=["Country","Country Code"],
                  var_name="Year",
                  value_name="UnemploymentRate")

year = UN_rate["Year"]
# -

#On standardise la colonne année.
UN_rate["Year"] = UN_rate["Year"].str.slice(0,4)

#On change le type de Year pour correspondre à la colonne dans result
UN_rate["Year"] = UN_rate["Year"].astype('int')

result = result.merge(UN_rate,how="left", left_on=["Code","Year"], right_on=["Country Code","Year"])

result[result["Entity"] == "France"]
result = result.drop(columns=["Country","Country Code","country"])
result.to_csv("result.csv",index=False)



arrival_path = os.path.join(current_dir, 'arrivaltourists.csv')

df_arrival = pd.read_csv(arrival_path)
#On supprime les lignes vide de Country code qui sont 1) des données non pratiquables 2) la source des données
df_arrival = df_arrival[df_arrival['Country Code'].notna()]
#Et on supprime les colonnes Series et Series Code qui sont inutiles pour l'avenir
df_arrival = df_arrival.drop(['Series Name','Series Code'], axis=1)


# +
df_arrival = df_arrival.melt(id_vars=["Country Name","Country Code"],
                  var_name="Year",
                  value_name="Arrival")
# -

df_arrival["Year"] = df_arrival["Year"].str.slice(0,4)
#On change le type de Year pour correspondre à la colonne dans result
df_arrival["Year"] = df_arrival["Year"].astype('int')


# =====================================================
# ================= Electricity table =================
# =====================================================
elect_path = os.path.join(current_dir, 'access_elect.csv')
elect = pd.read_csv(elect_path, encoding="ISO-8859-1")

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


elect = clean_dataworld(elect,"AcessToElectricity")
result = result.merge(elect,how="left", left_on=["Code","Year"], right_on=["Country Code","Year"])

# ================================================================
# ================= Primary ClassEnrolment table =================
# ================================================================
class_path = os.path.join(current_dir, 'PrimaryClassEnrollment.csv')
classenrollment = pd.read_csv(class_path, encoding="ISO-8859-1")

classenrollment = clean_dataworld(classenrollment,"PrimaryClassEnrollment(%)")
result = result.merge(classenrollment,how="left", left_on=["Code","Year"], right_on=["Country Code","Year"])


# ================================================================
# ================= Secoundary ClassEnrolment table ==============
# ================================================================
class2_path = os.path.join(current_dir, 'SecondaryClassEnrollment.csv')
#Pas de gâchis de variable :
classenrollment = pd.read_csv(class2_path, encoding="ISO-8859-1")

classenrollment = clean_dataworld(classenrollment,"SecondaryClassEnrollment(%)")
result = result.merge(classenrollment,how="left", left_on=["Code","Year"], right_on=["Country Code","Year"])

#===========================
# Résultat
#===========================
result_economy = result.drop(columns=["Country Name_x","Country Code_x","Country Name_y","Country Code_y","Country Name","Country Code"])
result_economy.replace("..","",inplace=True)
result_economy.to_csv("result_eco.csv")