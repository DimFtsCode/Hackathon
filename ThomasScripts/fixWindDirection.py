import pandas as pd

# Read the existing CSV files as Dataframes.
df_Aigeirouses = pd.read_csv('C:/Users/thoma/Documents/Hackathon/DimiScripts/Datasets/Aigeirouses_weather_data.csv')
df_Anthousa = pd.read_csv('C:/Users/thoma/Documents/Hackathon/DimiScripts/Datasets/Anthousa_weather_data.csv')
df_Dioni = pd.read_csv('C:/Users/thoma/Documents/Hackathon/DimiScripts/Datasets/Dioni_weather_data.csv')
df_Ekali = pd.read_csv('C:/Users/thoma/Documents/Hackathon/DimiScripts/Datasets/Ekali_weather_data.csv')
df_Grammatiko = pd.read_csv('C:/Users/thoma/Documents/Hackathon/DimiScripts/Datasets/Grammatiko_weather_data.csv')
df_Kallitechnoupoli = pd.read_csv('C:/Users/thoma/Documents/Hackathon/DimiScripts/Datasets/Kallitechnoupoli_weather_data.csv')
df_Kato_Soulion = pd.read_csv('C:/Users/thoma/Documents/Hackathon/DimiScripts/Datasets/Kato Soulion_weather_data.csv')
df_Kifisia = pd.read_csv('C:/Users/thoma/Documents/Hackathon/DimiScripts/Datasets/Kifisia_weather_data.csv')
df_Marathonas = pd.read_csv('C:/Users/thoma/Documents/Hackathon/DimiScripts/Datasets/Marathonas_weather_data.csv')
df_Melissia = pd.read_csv('C:/Users/thoma/Documents/Hackathon/DimiScripts/Datasets/Melissia_weather_data.csv')
df_Nea_Erythraia = pd.read_csv('C:/Users/thoma/Documents/Hackathon/DimiScripts/Datasets/Nea Erythraia_weather_data.csv')
df_Ntaou_Penteli = pd.read_csv('C:/Users/thoma/Documents/Hackathon/DimiScripts/Datasets/Ntaou Penteli_weather_data.csv')
df_Ntrafi = pd.read_csv('C:/Users/thoma/Documents/Hackathon/DimiScripts/Datasets/Ntrafi_weather_data.csv')
df_Rapentosa = pd.read_csv('C:/Users/thoma/Documents/Hackathon/DimiScripts/Datasets/Rapentosa_weather_data.csv')
df_Rodopoli = pd.read_csv('C:/Users/thoma/Documents/Hackathon/DimiScripts/Datasets/Rodopoli_weather_data.csv')
df_Vothon = pd.read_csv('C:/Users/thoma/Documents/Hackathon/DimiScripts/Datasets/Vothon_weather_data.csv')
df_Vrilissia = pd.read_csv('C:/Users/thoma/Documents/Hackathon/DimiScripts/Datasets/Vrilissia_weather_data.csv')

# Static Wind Translation.
wind_translation = [("N", 360), ("S", 180), ("E", 90), ("W", 270), 
                    ("NW", 315), ("NE", 45), ("SE", 135), ("SW", 225),
                    ("WNW", 315), ("WSW", 45), ("NNW", 335), ("NNE", 25),
                    ("ENE", 65), ("ESE", 115), ("SSE", 155), ("SSW", 205)]

#Reset Indexes for all Dataframes.
df_aigeirouses = df_Aigeirouses.reset_index()
df_anthousa = df_Anthousa.reset_index()
df_dioni = df_Dioni.reset_index()
df_Ekali = df_Ekali.reset_index()
df_Grammatiko = df_Grammatiko.reset_index()
df_Kallitechnoupoli = df_Kallitechnoupoli.reset_index()
df_Kato_Soulion = df_Kato_Soulion.reset_index()
df_Kifisia = df_Kifisia.reset_index()
df_Marathonas = df_Marathonas.reset_index()
df_Melissia = df_Melissia.reset_index()
df_Nea_Erythraia = df_Nea_Erythraia.reset_index()
df_Ntaou_Penteli = df_Ntaou_Penteli.reset_index()
df_Ntrafi = df_Ntrafi.reset_index()
df_Rapentosa = df_Rapentosa.reset_index()
df_Rodopoli = df_Rodopoli.reset_index()
df_Vothon = df_Vothon.reset_index()
df_Vrilissia = df_Vrilissia.reset_index()

# For each tuple in wind_translation, parse all dataset files and replace the existing value with the correct value.
for val in wind_translation:
    df_Aigeirouses.replace(val[0], val[1], inplace=True)
    df_Anthousa.replace(val[0], val[1], inplace=True)
    df_Dioni.replace(val[0], val[1], inplace=True)
    df_Ekali.replace(val[0], val[1], inplace=True)
    df_Grammatiko.replace(val[0], val[1], inplace=True)
    df_Kallitechnoupoli.replace(val[0], val[1], inplace=True)
    df_Kato_Soulion.replace(val[0], val[1], inplace=True)
    df_Kifisia.replace(val[0], val[1], inplace=True)
    df_Marathonas.replace(val[0], val[1], inplace=True)
    df_Melissia.replace(val[0], val[1], inplace=True)
    df_Nea_Erythraia.replace(val[0], val[1], inplace=True)
    df_Ntaou_Penteli.replace(val[0], val[1], inplace=True)
    df_Ntrafi.replace(val[0], val[1], inplace=True)
    df_Rapentosa.replace(val[0], val[1], inplace=True)
    df_Rodopoli.replace(val[0], val[1], inplace=True)
    df_Vothon.replace(val[0], val[1], inplace=True)
    df_Vrilissia.replace(val[0], val[1], inplace=True)
    
#print(df)
# df.replace("SSW", 205, inplace=True)
# print(df)

# Write the results to new CSV files. 
df_Aigeirouses.to_csv("C:/Users/thoma/Documents/Hackathon/ThomasScripts/aigeirouses_fixed.csv")
df_Anthousa.to_csv("C:/Users/thoma/Documents/Hackathon/ThomasScripts/anthousa_fixed.csv")
df_Dioni.to_csv("C:/Users/thoma/Documents/Hackathon/ThomasScripts/dioni_fixed.csv")
df_Ekali.to_csv("C:/Users/thoma/Documents/Hackathon/ThomasScripts/ekali_fixed.csv")
df_Grammatiko.to_csv("C:/Users/thoma/Documents/Hackathon/ThomasScripts/grammatiko_fixed.csv")
df_Kallitechnoupoli.to_csv("C:/Users/thoma/Documents/Hackathon/ThomasScripts/kallitechnoupoli_fixed.csv")
df_Kato_Soulion.to_csv("C:/Users/thoma/Documents/Hackathon/ThomasScripts/kato_soulion_fixed.csv")
df_Kifisia.to_csv("C:/Users/thoma/Documents/Hackathon/ThomasScripts/kifisia_fixed.csv")
df_Marathonas.to_csv("C:/Users/thoma/Documents/Hackathon/ThomasScripts/marathonas_fixed.csv")
df_Melissia.to_csv("C:/Users/thoma/Documents/Hackathon/ThomasScripts/melissia_fixed.csv")
df_Nea_Erythraia.to_csv("C:/Users/thoma/Documents/Hackathon/ThomasScripts/nea_erythraia_fixed.csv")
df_Ntaou_Penteli.to_csv("C:/Users/thoma/Documents/Hackathon/ThomasScripts/ntaou_penteli_fixed.csv")
df_Ntrafi.to_csv("C:/Users/thoma/Documents/Hackathon/ThomasScripts/ntrafi_fixed.csv")
df_Rapentosa.to_csv("C:/Users/thoma/Documents/Hackathon/ThomasScripts/rapentosa_fixed.csv")
df_Rodopoli.to_csv("C:/Users/thoma/Documents/Hackathon/ThomasScripts/rodopoli_fixed.csv")
df_Vothon.to_csv("C:/Users/thoma/Documents/Hackathon/ThomasScripts/vothon_fixed.csv")
df_Vrilissia.to_csv("C:/Users/thoma/Documents/Hackathon/ThomasScripts/vrilissia_fixed.csv")

print("task finished")
