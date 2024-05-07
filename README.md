<h3 align = "center"> Proyecto Despliegue - Big Data </h3>

---
<p align = "center"> Este proyecto consiste en un conjunto de scripts diseñados para recopilar datos financieros de diversas acciones de la bolsa de valores y posteriormente obtener información acerca de ellos. 
Estos datos incluyen el nombre de la acción, la última cotización, el máximo y mínimo de la sesión, y la fecha y hora de la recopilación.
<br>
</p>

## 📝 Tabla de contenido

- [Estructura del proyecto](#structure)
- [Recopilando datos](#extract_data)
- [Gestionando datos](#manage_data)
- [Autores](#authors)

## ⚒️ Estructura del Proyecto <a name = "structure"> </a>

El proyecto se organiza de la siguiente manera en local:

- **src**: Contiene el código fuente del proyecto.
  - **extract**: Directorio que contiene los scripts de extracción de datos.
  - **datos**: Directorio donde se almacenan los datos recopilados.
  - **management**: Directorio donde se almacenan los scripts para procesar los datos de forma local.
    - **hdfs**: Directorio donde se almacenan los scripts usando HDFS.

Los archivos que se almacenan en datos tienen la forma de `DD-MM-YYYY.csv` donde sus campos son en orden de izquierda a derecha:
- Nombre de la Acción
- Última cotización
- Máximo de la sesión
- Mínimo de la sesión
- Hora

El archivo que se encuentra en src con nombre `informacion_empresas.csv` sus campos de izquierda a derecha son:
- Nombre de la empresa
- Fecha de fundación
- Tipo de empresa
- Número de empleados
- Beneficio neto
- Ciudad donde tienen la sede central

En HDFS el proyecto tiene la siguiente forma:

- **proyecto_despliegue**: Contiene los archivos necesarios para su ejecución en hdfs.
  - **datos**: Directorio donde se almacenan los datos recopilados al terminar el día.


## 📂 Extrayendo datos <a name = "extract_data"> </a>

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

3. Dar permisos de ejecución a los siguientes ficheros

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

## 📊 Gestionando datos <a name = "manage_data"> </a>

El la carpeta `management` están todo lo archivos relacionados con la gestión de los `datos` junto a un archivo `.sh` encargado de la mecanización de procesos.

### Descipción de los script

- `Ejercicio 1`: Genera un lista semanal donde se indica (`Nombre de la acción`, (`valor inicial de cotización`, `valor final de cotización`, `mínimo`, `máximo`))

- `Ejercicio 2`: Genera un lista mensual donde se indica (`Nombre de la acción`, (`valor inicial de cotización`, `valor final de cotización`, `mínimo`, `máximo`))

- `Ejercicio 3`: Dado el nombre de una acción y un rango ded fechas, obtiene (`Acción`, (`valor mínimo de cotización`, `valor máximo de cotización`, `porcentaje de decremento desde el valor inicial hasta el mínimo`, `porcentaje de incremento desde el valor inicial hasta el máximo`))

- `Ejercicio 4`: Dado el nombre de una acción se obtiene (`Acción`, (`valor mínimo mensual`, `valor máximo mensual`, `valor mínimo semanal`, `valor máximo semanal`, `valor mínimo de la última hora`, `valor máximo de la última hora`))

- `Ejercicio 5`: Muestra las 5 acciones que más han subido en la última semana y último mes: (`Semana/Mes`, (`Nombre de la acción`, `diferencia de la acción (precio final-precio inicial)`))

- `Ejercicio 6`: Muestra las 5 acciones que más han bajado en la última semana y último mes: (`Semana/Mes`, (`Nombre de la acción`, `diferencia de la acción (precio final-precio inicial)`))

- `Ejercicio 7`: Dado un porcentaje y un rango de fechas obtiene las acciones que han tenido un incremento de ese porcentaje durante ese periodo (`Acción`, (`Porcentaje de incremento del precio de la acción`, `Porcentaje introducido`))

- `Extra 1`: Ranking de las acciones con mayor ratio entre la última cotización y el beneficio económico de esa empresa, sirve para saber si una acción está sobrevalorada (`Posición del ranking`, (`Nombre de la acción`, `Ratio`))

- `Extra 2`: Muestra el tipo de empresa que tiende a tener acciones más altas (`Tipo de empresa`, `Cotización media de ese tipo de empresa`)

- `Extra 3`: Muestra la acción de las empresa fundada antes de los 2000 que tiene el menor porcentaje de incremento de cotización en un día (`Nombre de la Acción`, `Porcentaje de incremento de cotización`)

### Requisitos previos <a name = "previous_steps_manage"> </a>

Si se van a ejecutar de forma local puede omitir este apartado y pasar al funcionamiento local, sin embargo para HDFS será necesario ejecutar el servicio de HDFS y YARN.

```
start-dfs.sh
```

```
start-yarn.sh
```

### Funcionamiento en su máquina local

1. Situarse en el `directorio management`

```
cd src/management
```

2. Para ejecutar los scripts del ejercicio 1 al ejercicio 7

```
sh ejercicioX.sh
```
Donde X es el número del 1 al 7

3. Para ejecutar los scripts extra 

```
python extraX.py ../informacion_empresas.csv ../datos/DD-MM-YYYY.csv 
```
Donde `X` es el número del 1 al 3 y `DD-MM-YYY` es el formato del archivo diario que quiera consultar

### Funcionamiento en HDFS

Para esta parte es necesario haber ejecutado los comandos que aparecen en [`Requisitos previos`](#previous_steps_manage)

1. Subir a HDFS el archivo con la información de las empresas situado en `src`

```
cd src/
```

```
hdfs dfs -put informacion_empresas.csv proyecto_despliegue
```

2. Situarse en el directorio `hdfs`

```
cd src/management/hdfs
```

3. Para ejecutar los scripts del ejercicio 1 al ejercicio 7

```
sh ejercicioX.sh
```
Donde `X` es el número del 1 al 7

4. Para ejecutar los scripts extra 

```
python extraX.py -r hadoop hdfs:///user/alumno/proyecto_despliegue/informacion_empresas.csv hdfs:///user/alumno/proyecto_despliegue/datos/DD-MM-YYYY.csv
```
Y si quiere que la información se guarde en un archivo puede añadirle esto:

```
--output-dir proyecto_despliegue/extraX
```

Donde `X`es el número del 1 al 3 y `DD-MM-YYY` es el formato del archivo diario que quiera consultar


## ✒️ Autores <a name = "authors"> </a>

* **Claudia Torres** - [ClaudiaTC02](https://github.com/ClaudiaTC02)
* **Jordi Doménech** - [Jordi272](https://github.com/Jordi272)
