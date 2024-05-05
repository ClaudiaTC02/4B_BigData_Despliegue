
directorio_script=$(dirname "$0")

directorio_datos_local="../../$directorio_script/datos"

directorio_datos="proyecto_despliegue/datos"

fecha_actual=$(date +"%s")

fecha_mes=$(date +%s --date='-1 month')

read -p "Introduce el nombre de una acción: " nombre_accion

archivo_mes="Ejercicio4_${fecha_mes}.csv"

hdfs dfs -ls "$directorio_datos" | while read -r archivo; do

    # Obteniendo la fecha del archivo
    fecha_archivo=$(echo "$archivo" | awk '{print $8}' | awk -F "/" '{print $3}' | awk -F "." '{print $1}')
    fecha_archivo_unix=$(date -d "$(echo "$fecha_archivo" | awk -F '-' '{print $3"-"$2"-"$1}')" +%s)

    # Comprobando si se encuentra dentro del rango
    if [ "$fecha_archivo_unix" -ge "$fecha_mes" ] && [ "$fecha_archivo_unix" -le "$fecha_actual" ]; then

	# si el archivo no existe crearlo
	if [ ! -f "$directorio_datos_local/$archivo_mes" ]; then
	    > "$directorio_datos_local/$archivo_mes"
	fi

	# Agregar la fecha a cada línea del archivo actual y concatenar
	hdfs dfs -cat "$directorio_datos/$fecha_archivo.csv" | while IFS= read -r linea; do
            echo "$linea,$fecha_archivo" >> "$directorio_datos_local/$archivo_mes"
        done
    fi
    

done

# Subir archivo HDFS
hdfs dfs -put "$directorio_datos_local/$archivo_mes" "$directorio_datos/$archivo_mes"

# Eliminar el archivo
rm "$directorio_datos_local/$archivo_mes"


archivo_mapreducer="../$directorio_script/ejercicio4.py"

python "$archivo_mapreducer" -r hadoop "hdfs:///user/alumno/$directorio_datos/$archivo_mes" --accion "$nombre_accion"

hdfs dfs -rm "$directorio_datos/$archivo_mes"

