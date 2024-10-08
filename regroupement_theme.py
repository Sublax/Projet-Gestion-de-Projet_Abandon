from data.Economy.clean_data import result_economy
from data.Transport.clean_data import result_transport
from data.Agroalimentaire.clean_data import result_agro
import pandas as pd
import numpy as np

df_merge = result_economy.merge(result_transport,how="left",on="Code")
df_merge = pd.DataFrame(df_merge)

#On remplace les valeurs autres que 2020 par NaN pour éviter les répétitions
df_merge.loc[df_merge["Year_x"] != 2020,'Proportion of population that has convenient access to public transport'] = np.nan
df_merge2 = df_merge.merge(result_agro,how="left",left_on=["Code","Year_x"],right_on=["Country Code","Year"])
df_merge2.drop(["Country Name_x","Country Code_x","Entity_y","Year_y","Country Name_y","Country Code_y","Year"],axis=1,inplace=True)
df_merge2.to_csv("result.csv")
