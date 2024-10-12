#=============================
# Importations libraries
#=============================
import pandas as pd
import matplotlib.pyplot as plt
import country_converter as coco
import os
import sys

#=============================
# Importations csv
#=============================
current_dir = os.path.dirname(os.path.abspath(__file__))


eco_path = os.path.join(current_dir, 'global_gdp.csv')
wage_path = os.path.join(current_dir, 'minimum_wage.csv')

countries_path = os.path.join(current_dir, '..', 'countries.csv')
agro_path = os.path.join(current_dir,'..','Agroalimentaire','global-food-prices.csv')

countries = pd.read_csv(countries_path)
agro = pd.read_csv(agro_path)

arrival_path = os.path.join(current_dir, 'arrivaltourists.csv')
df_arrival = pd.read_csv(arrival_path)

elect_path = os.path.join(current_dir, 'access_elect.csv')
elect = pd.read_csv(elect_path, encoding="ISO-8859-1")


class_path = os.path.join(current_dir, 'PrimaryClassEnrollment.csv')
classenrollment = pd.read_csv(class_path, encoding="ISO-8859-1")

class2_path = os.path.join(current_dir, 'SecondaryClassEnrollment.csv')


#=============================
# Fonctions + test
#=============================
def perf_coco(df2):
    """
    Fonction perf_coco -
    Paramètre : 
    - df2 : colonne de nom de pays à valeur unique

    Sortie : Comparaison entre aucun changement, coco_convert en name short et coco_convert en ISO2
    """
    print("===== Performance sans changement : ======")
    set_pays = set(countries["Name"])
    set_df2 = set(df2)
    valeurs_communes = set_pays.intersection(set_df2)
    print(f"Valeur communes : {len(valeurs_communes)}/{len(df2)}")

    print("===== Performance short name pays : ======")
    set_df2 = set(coco.convert(names=df2,to='name_short'))
    valeurs_communes = set_pays.intersection(set_df2)
    print(f"Valeur communes : {len(valeurs_communes)}/{len(df2)}")



pays_agro = pd.unique(agro["adm0_name"])
perf_coco(pays_agro)

eco = pd.read_csv(eco_path)
lst = pd.unique(eco["Entity"])
perf_coco(lst)

wage = pd.read_csv(wage_path)
perf_coco(wage["country"])

# +
## On voit qu'il y le plus de ressemblance grâce à ISO2, on utilisera
## cette standardisation pour la suite.
## ------
## UPDATE OCTOBRE: Néanmoins, pour la standardisation de TOUTES les tables de chacun des membres du groupe
## On utilisera le short name, pour avoir un affichage clair des noms des pays sur le site.

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


#=============================
# Traitements
#=============================
wage = standardisation(wage,'country')

#result = pd.merge(eco,wage,left_on="Code", right_on="country", how="left")
result = eco.merge(wage,left_on="Entity",right_on="country",how="left")


# =====================================================
# ================= Arrival table =================
# =====================================================
#On supprime les lignes vide de Country code qui sont 1) des données non pratiquables 2) la source des données
df_arrival = df_arrival[df_arrival['Country Code'].notna()]
#Et on supprime les colonnes Series et Series Code qui sont inutiles pour l'avenir
df_arrival = df_arrival.drop(['Series Name','Series Code'], axis=1)


# On retourne le df pour avoir des années sur une seule colonne
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
#On utilise la fonction clean data world pour avoir un df standardisé
elect = clean_dataworld(elect,"AcessToElectricity")
result = result.merge(elect,how="left", left_on=["Code","Year"], right_on=["Country Code","Year"])

# ================================================================
# ================= Primary ClassEnrolment table =================
# ================================================================
#On utilise la fonction clean data world pour avoir un df standardisé
classenrollment = clean_dataworld(classenrollment,"PrimaryClassEnrollment(%)")
result = result.merge(classenrollment,how="left", left_on=["Code","Year"], right_on=["Country Code","Year"])


# ================================================================
# ================= Secoundary ClassEnrolment table ==============
# ================================================================
#Pas de gâchis de variable :
classenrollment = pd.read_csv(class2_path, encoding="ISO-8859-1")

classenrollment = clean_dataworld(classenrollment,"SecondaryClassEnrollment(%)")
result = result.merge(classenrollment,how="left", left_on=["Code","Year"], right_on=["Country Code","Year"])




#===========================
# Résultats
#===========================
result_economy = result.drop(columns=["Country Name_x","Country Code_x","Country Name_y","Country Code_y","Country Name","Country Code"])
result_economy.replace("..","",inplace=True)

    #==========================
    # Resultats Education
    #==========================
result_education = result_economy[["Entity","Year","PrimaryClassEnrollment(%)","SecondaryClassEnrollment(%)"]]
result_education = result_education.dropna(subset=["PrimaryClassEnrollment(%)", "SecondaryClassEnrollment(%)"])
#On standardise les noms des pays : 
result_education = standardisation(result_education, "Entity")

#On remplace les noms des pays par l'id : 
result_education = result_education.merge(countries,left_on="Entity", right_on="Name",how="left")
result_education = result_education.drop(["Name","Entity"],axis=1).rename(columns={'id':'pays_id'})

#On exporte en csv : 
result_education.to_csv("result_educ.csv", index_label="id_educ")

#==========================
# Resultats Economy
#==========================
#On supprime les deux dernières colonnes qui sont Primary et Secondary Class Enrollment
result_economy = result_economy.iloc[:, :-2]

#Puis on supprime les colonnes Code
result_economy.drop(["Code","country"],axis=1, inplace=True)

#On standardise le nom des pays : 
result_economy = standardisation(result_economy,"Entity")

#Enfin on remplace les noms des pays par l'id : 
result_economy = result_economy.merge(countries,left_on="Entity", right_on="Name",how="left")
result_economy = result_economy.drop(["Name","Entity"],axis=1).rename(columns={'id':'pays_id'})

#On exporte en csv : 
result_economy.to_csv("result_eco.csv", index_label="id_eco")