import requests
from requests.auth import HTTPBasicAuth
import pandas as pd
import timeit
from datetime import datetime, timedelta
import config
import os
import errno

date = datetime.now()
semana_pasada = date - timedelta(weeks=1)
fechafin = date.strftime('%Y-%m-%d 00:00')
fechaini = semana_pasada.strftime('%Y-%m-%d 00:00')
ouput = config.path_ouputs + date.strftime('%Y%m%d_%H.%M.%S\\')

try:
    os.makedirs(ouput)
except OSError as e:
    if e.errno != errno.EEXIST:
        print('El directorio %s ya existe se sobreescribiran los Archivos en el.' % ouput)
    else:
        print('La creación del directorio %s falló.' % ouput)
        raise SystemExit(e)
else:
    print('Se ha creado el directorio: %s' % ouput)

api_server = 'https://redmet.icc.org.gt/ws/'
url_estaciones = 'redmet/estaciones'
url_lecturas = 'redmet/estaciones/lecturas'

auth = HTTPBasicAuth(config.user, config.password)

headers = {
    'Content-Type': 'application/json', 
    'Accept':'application/json', 
    }

parametros = {
    'fechaini': fechaini,
    'fechafin': fechafin,
    'tipo': 'fecha',
    'estacionids[]': []
}

## Consultar informacion de estaciones

try:
    response = requests.get( api_server + url_estaciones, headers=headers, auth=auth)
except requests.exceptions.HTTPError as errh:
    print ("Error Http durante consulta estaciones:",errh)
    raise SystemExit(errh)
except requests.exceptions.ConnectionError as errc:
    print ("Error de conexion durante consulta estaciones:",errc)
    raise SystemExit(errc)
except requests.exceptions.Timeout as errt:
    print ("Error de tiempo de espera durante consulta estaciones:",errt)
    raise SystemExit(errt)
except requests.exceptions.RequestException as err:
    print ("OOps: algo salio mal durante consulta estaciones",err)
    raise SystemExit(err)

estaciones = response.json()['estaciones']

## filtrar Ids de estaciones con informacion
estaciones_con_datos = [x['estacionid'] for x in estaciones if x['redmet'] == 1]
parametros['estacionids[]'] = estaciones_con_datos

## Fechas de consulta
print('\nPor defecto se extraeran los datos de una semana atras, es decir entre las fechas:')
print('Fecha de inicio: ', fechaini)
print('Fecha final: ', fechafin)
print('Si desea cambiar alguna de estas fechas podrar hacerlo acontinuacion respetando el formato yyyy-mm-dd hh:mm,')
print('si NO desea cambiar las fechas solo precione ENTER cuando el sistema solicite la fecha.')

fechaini = input('Ingrese la fecha de inicio (yyyy-mm-dd hh:mm): ')
fechafin = input('Ingrese la fecha final (yyyy-mm-dd hh:mm): ')

if fechaini:
    parametros['fechaini'] = fechaini
if fechafin:
    parametros['fechafin'] = fechafin

start = timeit.default_timer()

print('\nExtrayendo datos entre las fechas %s y %s' % (parametros['fechaini'] ,parametros['fechafin']))
## Consultar lecturas

try:
    response1 =  requests.get(api_server + url_lecturas, headers=headers, auth=auth, params=parametros)
except requests.exceptions.HTTPError as errh:
    print ("Error Http durante extraccion de lo datos: ",errh)
    raise SystemExit(errh)
except requests.exceptions.ConnectionError as errc:
    print ("Error de conexion durante extraccion de lo datos: ",errc)
    raise SystemExit(errc)
except requests.exceptions.Timeout as errt:
    print ("Error de tiempo de espera durante extraccion de lo datos: ",errt)
    raise SystemExit(errt)
except requests.exceptions.RequestException as err:
    print ("OOps: algo salio mal durante extraccion de lo datos: ",err)
    raise SystemExit(err)

try:
    
    datos = response1.json()

    ## Organizar datos para cada estacion
    for dato in datos:
        df = pd.DataFrame(datos[dato])
        estacion = [x for x in estaciones if x['estacionid'] == int(dato)][0]
        
        df['codigo'] = estacion['codigo']
        df['finca'] = estacion['finca']
        df['latitud'] = estacion['latitud']
        df['longitud'] = estacion['longitud']
        df['pais'] = estacion['pais']['nombre']

        df.to_csv(ouput + 'Estacion-'+ estacion['finca'] +'.csv', index=False)
except e:
    print('Error guardando los datos ', e)
    raise SystemExit(e)
else:
    print('Datos extraidos')

stop = timeit.default_timer()

print('Tiempo de consulta: ', stop - start) 