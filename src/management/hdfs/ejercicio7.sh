
directorio_script=$(dirname "$0")

directorio_datos_local="../../$directorio_script/datos"

directorio_datos="proyecto_despliegue/datos"

read -p "Introduce la fecha inicial: " fecha_inicial
read -p "Introduce la fecha final: " fecha_final
read -p "Introduce un porcentaje: " porcentaje

fecha_inicial_unix=$(date -d "$(echo "$fecha_inicial" | awk -F '-' '{print $3"-"$2"-"$1}')" +%s)

fecha_final_unix=$(date -d "$(echo "$fecha_final" | awk -F '-' '{print $3"-"$2"-"$1}')" +%s)

archivo_semanal="Ejercicio7_${fecha_inicial}_${fecha_final}.csv"

hdfs dfs -ls "$directorio_datos" | while read -r archivo; do

    # Obteniendo la fecha del archivo
    fecha_archivo=$(echo "$archivo" | awk '{print $8}' | awk -F "/" '{print $3}' | awk -F "." '{print $1}')
    fecha_archivo_unix=$(date -d "$(echo "$fecha_archivo" | awk -F '-' '{print $3"-"$2"-"$1}')" +%s)

    # Comprobando si se encuentra dentro del rango
    if [ "$fecha_archivo_unix" -ge "$fecha_inicial_unix" ] && [ "$fecha_archivo_unix" -le "$fecha_final_unix" ]; then
	
	# si el archivo no existe crearlo
	hdfs dfs -cat "$directorio_datos/$fecha_archivo.csv" | while IFS= read -r linea; do
            echo "$linea,$fecha_archivo" >> "$directorio_datos_local/$archivo_semanal"
        done
	
    fi
    

done

# Subir archivo HDFS
hdfs dfs -put "$directorio_datos_local/$archivo_semanal" "$directorio_datos/$archivo_semanal"

# Eliminar el archivo
rm "$directorio_datos_local/$archivo_semanal"

archivo_mapreducer="../$directorio_script/ejercicio7.py"

python "$archivo_mapreducer" -r hadoop "hdfs:///user/alumno/$directorio_datos/$archivo_semanal" --porcentaje "$porcentaje"  

hdfs dfs -rm "$directorio_datos/$archivo_semanal"

