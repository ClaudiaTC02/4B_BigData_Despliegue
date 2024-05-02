<h3 align = "center"> Proyecto Despliegue - Big Data </h3>

---
<p align = "center"> Este proyecto consiste en un conjunto de scripts diseñados para recopilar datos financieros de diversas acciones de la bolsa de valores. Estos datos incluyen el nombre de la acción, la última cotización, el máximo y mínimo de la sesión, y la fecha y hora de la recopilación.
    <br>
</p>

## 📝 Tabla de contenido

- [Estructura del proyecto](#structure)
- [Recopilando datos](#extract_data)

## ⚒️ Estructura del Proyecto <a name = "structure"> </a>

El proyecto se organiza de la siguiente manera:

- **src**: Contiene el código fuente del proyecto.
  - **extract**: Directorio que contiene los scripts de extracción de datos.
  - **datos**: Directorio donde se almacenan los datos recopilados.


## 🏁 Extrayendo datos <a name = "extract_data"> </a>

El script `dataExtraction.sh` se encarga de ejecutar el script de scraping automáticamente cada hora durante el horario comercial (de 9:30 a 18:30 de lunes a viernes). Los datos recopilados se guardan en el directorio `datos` y al finalizar el día se subirá al directorio HDFS `proyecto_despliegue/datos`.

El nombre de los archivos es la fecha en formato DD-MM-YYYY y se recopilan cada hora.

### Requisitos previos

Qué necesita para instalar el software y cómo instalarlo.
Lo que se debe instalar para hacer funcionar este proyecto es una máquina Linux con Apache Hadoop con HDFS configurado.

Además, deberá instalar selenium ejecutando en su terminal el siguiente comando:

```
pip install selenium
```

### Uso del script

Para poner el script en funcionamiento, deberá seguir los siguientes pasos:

1. Iniciar el servicio HDFS

```
start-dfs.sh
```

2. Acceder a la carpeta extract del repositorio previamente clonado

```
cd 4B_BigData_Despliegue/src/extract/
```

1. Dar permisos de ejecución a los siguientes ficheros

```
chmod +x dataExtraction.sh
```
```
chmod +x scraper.py
```
```
chmod +x geckodriver
```

4. Ejecutar el fichero

```
sh dataExtraction.sh
```