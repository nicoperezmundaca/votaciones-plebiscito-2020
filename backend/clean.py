import json
import requests
import pandas as pd

def df_from_json(file):
  with open(file) as json_file:
    data = json.load(json_file)
  df = pd.DataFrame(data)
  return df

def df_from_csv(file):
  df = pd.read_csv(file)
  return df

def save_csv(df, filename):
  df.to_csv(filename, index=False)

def save_json(df, filename, orient='records'):
  df.to_json(filename, orient=orient)

df = df_from_json('resultados.json')
df_dim = df_from_csv('dim_geo.csv')

df = df.fillna(0)
df = df.merge(df_dim[['provincia_id', 'provincia_name', 'comuna_id']], on='comuna_id')
df = df[['region_id', 'region_name', 'provincia_id', 'provincia_name', 'comuna_id', 'comuna_name', 'circ_senatorial_id', 'circ_senatorial_name', 'distrito_id', 'distrito_name', 'circ_electoral_id', 'circ_electoral_name', 'local_id', 'local_name', 'mesa_id', 'mesa_name', 'constitucion_apruebo', 'constitucion_rechazo', 'constitucion_nulos', 'constitucion_blancos', 'constitucion_total', 'constitucion_validos', 'convencion_mixta', 'convencion_constitucional', 'convencion_nulos', 'convencion_blancos', 'convencion_total', 'convencion_validos']]

save_csv(df, 'data/plebicito_2020_clean_data.csv')
save_json(df, 'plebicito_2020_clean_data.json')

print('*** Plebicito 2020 Data Clean ***')