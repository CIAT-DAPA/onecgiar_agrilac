# Script ICC

Este script fue diseñado para descargar información de la red de estaciones meteorológicas del **Instituto Privado de Investigación sobre Cambio Climático** (ICC) a través de su API y esta desarrollado en Python y utiliza las librerias

    pandas
    requests
    timeit
    datetime
    errno

## Configuración

En el archivo config.py se encuentran las variables necesario para el funcionamiento del script, estas se deberan configurar antes de ejecutar el script por primera vez

|Nombre Variable | Descripción                             |
|----------------|-----------------------------------------|
| path_ouputs    | Directorio donde se almacenarán los archivos csv generados durante la consulta. Ejemplo `D:\\api_ICC\\datos_estaciones\\`|
| user           | Nombre de usuario registrado la pagina del  ICC      |
| password       | Contraseña correspondiente al usuario                |

    Nota: utilizar las mismas credenciales que se utilizan para ingresar al portal del ICC (https://redmet.icc.org.gt/)

## Ejecutar script

Para ejecutar el script debe abrir una consola de comando desde la carpeta donde estan almacenados los archivos main.py y config.py, en la consola debera correr el comando 

	python main.py

Seguido a esto se generara la carpeta donde se almacenaran los archivos csv, el script esta programado para consultar los datos de la ultima semana pero  el sistema le preguntara si desea cambiar las fechas de la consulta las cuales son:

    Fecha de inicio
    Fecha final

Recordar que estas fechas deben cumplir con el formato `yyyy-mm-dd hh:mm`, si NO desea cambiar las fechas por defecto solo debe precionar ENTER al momento de que se le soliciten las fechas. si todos los datos estan correctos el sistema realizara la consulta y creara los archivos correspondientes.

Ejemplo de una ejecucion exitosa:

    > python main.py

    Se ha creado el directorio: D:\api ICC\datos_estaciones\20220922_11.33.55\

    Por defecto se extraeran los datos de una semana atras, es decir entre las fechas:
    Fecha de inicio:  2022-09-15 00:00
    Fecha final:  2022-09-22 00:00
    Si desea cambiar alguna de estas fechas podrar hacerlo acontinuacion respetando el formato yyyy-mm-dd hh:mm,
    si NO desea cambiar las fechas solo precione ENTER cuando el sistema solicite la fecha.
    Ingrese la fecha de inicio (yyyy-mm-dd hh:mm): 
    Ingrese la fecha final (yyyy-mm-dd hh:mm): 

    Extrayendo datos entre las fechas 2022-09-15 00:00 y 2022-09-22 00:00
    Datos extraidos
    Tiempo de consulta:  9.37557699996978

# Datos extraídos

## carpetas y archivos

Al extraer los datos se genera una carpeta en el directorio configurado en el archivo config.py esta carpeta tendrá por nombre la fecha y hora en la que se realizo la extraccion de los datos por ejemplo `20220922_14.05.46` donde 20220922 corresponde a la fecha y 14.05.46 a la hora.

Dentro de la carpeta generada se almacenará un archivo csv por cada estación encontrada, estos archivos tendran como nombre 'Estacion-<nombre_estacion>' por ejemplo `Estacion-Alamo`

## Estructura de los datos

|  Nombre dato      | Descripción                   |
|-------------------|-------------------------------|
|estacionid         |Id de la estación              |
|fecha              ||
|temperatura        ||
|radiacion          ||
|humedad_relativa   ||
|precipitacion      ||
|velocidad_viento   ||
|presion_atmosferica||
|mojadura           ||
|direccion_viento   ||
|created_at         ||
|updated_at         ||
|codigo             |Codigo de la estación           |
|eto                ||
|finca              |Nombre de la estación           |
|latitud            |Latitud de la estación          |
|longitud           |Longitud de la estación         |
|pais               |Pais donde se ubica la estación |	
