import json
import requests
import pandas as pd

def data_caller(url, headers):
    response = requests.get(url, headers)
    return response

def get_json(url):
    r = requests.get(url)
    return r.json()

def dim_table():
    # create the dim table
    dim_json = []
    regiones = get_json('http://www.servelelecciones.cl/data/elecciones_constitucion/filters/regiones/all.json')
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
                                row = {
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
                                    'mesa_name': mesa['d'],
                                }
                                dim_json.append(row)
    return dim_json

def dim_geo_servel():
    dim_json = []
    # create the dimension table for 
    regiones = get_json('http://www.servelelecciones.cl/data/elecciones_constitucion/filters/regiones/all.json')
    for region in regiones:
        provincias = get_json('http://www.servelelecciones.cl/data/elecciones_constitucion/filters/provincias/byregion/{}.json'.format(region['c']))
        for provincia in provincias:
            comunas = get_json('http://www.servelelecciones.cl/data/elecciones_constitucion/filters/comunas/byprovincia/{}.json'.format(provincia['c']))
            for comuna in comunas:
                row = {
                    'region_id': region['c'],
                    'region_name': region['d'],
                    'provincia_id': provincia['c'],
                    'provincia_name': provincia['d'],
                    'comuna_id': comuna['c'],
                    'comuna_name': comuna['d']
                }
                dim_json.append(row)
    return dim_json

def dict_results(data, name, optionA, optionB):
    dict = {
        '{}_{}'.format(name, optionA): data['data'][0]['c'],
        '{}_{}'.format(name, optionB): data['data'][1]['c'],
        '{}_nulos'.format(name): data['resumen'][1]['c'],
        '{}_blancos'.format(name): data['resumen'][2]['c'],
        '{}_total'.format(name): data['resumen'][3]['c'],
        '{}_validos'.format(name): data['resumen'][0]['c']
    }
    return dict

def read_data_all(dimensions, save_json=False, save_csv=False, filename=None):
    for row in data:
        # votacion de constitucion
        constitucion_json = get_json('http://www.servelelecciones.cl/data/elecciones_constitucion/computomesas/{}.json'.format(row['mesa_id']))
        constitucion = dict_results(constitucion_json, 'constitucion', 'apruebo', 'rechazo')
        
        # votacion de tipo de organo
        convencion_json = get_json('http://www.servelelecciones.cl/data/elecciones_convencion/computomesas/{}.json'.format(row['mesa_id']))
        convencion = dict_results(convencion_json, 'convencion', 'mixta', 'constitucional')
        row.update(constitucion)
        row.update(convencion)
        print('** REGION: {} COMUNA: {} MESA: {} ** DATOS DESCARGADOS **'.format(row['region_name'], row['comuna_name'], row['mesa_name']))

    df = pd.DataFrame(data)
    if (save_json):
        df.to_json('{}.json'.format(filename), orient='records')
    if (save_csv):
        df.to_csv('{}.csv'.format(filename), index=False)
    
    return df

with open('dim_electorales.json') as json_file:
    dimensions = json.load(json_file)

print(dimensions)
print('*** PLEBICITO 2020 DESCARGADO ***')