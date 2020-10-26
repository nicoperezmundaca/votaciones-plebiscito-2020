import json
import requests
import pandas as pd


def data_caller(url, headers):
    response = requests.get(url, headers)
    return response


def get_json(url):
    r = requests.get(url)
    return r.json()

def dim_geo_servel(regiones):
	data = []
	for region in regiones:
		provincias = get_json('http://www.servelelecciones.cl/data/elecciones_constitucion/filters/provincias/byregion/{}.json'.format(region['c']))
		for provincia in provincias:
			comunas = get_json('http://www.servelelecciones.cl/data/elecciones_constitucion/filters/comunas/byprovincia/{}.json'.format(provincia['c']))
			for comuna in comunas:
				data.append({
					'region_id': region['c'],
					'region_name': region['d'],
					'provincia_id': provincia['c'],
					'provincia_name': provincia['d'],
					'comuna_id': comuna['c'],
					'comuna_name': comuna['d'],
				})
	df = pd.DataFrame(data)
	return df

def dim_mesas_servel(regiones):
    data = []
    for region in regiones:
        circs_senatorial = get_json('http://www.servelelecciones.cl/data/elecciones_constitucion/filters/circ_senatorial/byregion/{}.json'.format(region['c']))
        for circ_senatorial in circs_senatorial:
            distritos = get_json('http://www.servelelecciones.cl/data/elecciones_constitucion/filters/distritos/bycirc_senatorial/{}.json'.format(circ_senatorial['c']))
            for distrito in distritos:
                comunas = get_json('http://www.servelelecciones.cl/data/elecciones_constitucion/filters/comunas/bydistrito/{}.json'.format(distrito['c']))
                for comuna in comunas:
                    circs_electoral = get_json('http://www.servelelecciones.cl/data/elecciones_constitucion/filters/circ_electoral/bycomuna/{}.json'.format(comuna['c']))
                    for circ_electoral in circs_electoral:
                        locales = get_json('http://www.servelelecciones.cl/data/elecciones_constitucion/filters/locales/bycirc_electoral/{}.json'.format(circ_electoral['c']))
                        for local in locales:
                            mesas = get_json('http://www.servelelecciones.cl/data/elecciones_constitucion/filters/mesas/bylocales/{}.json'.format(local['c']))
                            for mesa in mesas:
                                data.append({
                                    'region_id': region['c'],
                                    'region_name': region['d'],
                                    'circ_senatorial_id': circ_senatorial['c'],
                                    'circ_senatorial_name': circ_senatorial['d'],
                                    'distrito_id': distrito['c'],
                                    'distrito_name': distrito['d'],
                                    'comuna_id': comuna['c'],
                                    'comuna_name': comuna['d'],
                                    'circ_electoral_id': circ_electoral['c'],
                                    'circ_electoral_name': circ_electoral['d'],
                                    'local_id': local['c'],
                                    'local_name': local['d'],
                                    'mesa_id': mesa['c'],
                                    'mesa_name': mesa['d']
                                })
    df = pd.DataFrame(data)
    return df

# get all regiones on the database
regiones = get_json('http://www.servelelecciones.cl/data/elecciones_constitucion/filters/regiones/all.json')

# get geo division from servel
df_geo = dim_geo_servel(regiones)
print(df_geo)

df_mesas = dim_mesas_servel(regiones)
print(df_mesas)