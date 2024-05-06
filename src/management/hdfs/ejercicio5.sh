
directorio_script=$(dirname "$0")
directorio_datos_local="../../$directorio_script/datos"
directorio_datos="proyecto_despliegue/datos"

read -p "Introduce la fecha inicial: " fecha_inicial

fecha_inicial_unix=$(date -d "$(echo "$fecha_inicial" | awk -F '-' '{print $3"-"$2"-"$1}')" +%s)

fecha_final=$(date -d "@$((fecha_inicial_unix + 30 * 24 * 60 * 60))" "+%d-%m-%Y")
fecha_final_unix=$(date -d "@$((fecha_inicial_unix + 30 * 24 * 60 * 60))" "+%s")

archivo_mensual="Mes_${fecha_inicial}_${fecha_final}.csv"

hdfs dfs -ls "$directorio_datos" | while read -r archivo; do

    # Obteniendo la fecha del archivo
    fecha_archivo=$(echo "$archivo" | awk '{print $8}' | awk -F "/" '{print $3}' | awk -F "." '{print $1}')
    fecha_archivo_unix=$(date -d "$(echo "$fecha_archivo" | awk -F '-' '{print $3"-"$2"-"$1}')" +%s)

    # Comprobando si se encuentra dentro del rango 1 semana
    if [ "$fecha_archivo_unix" -ge "$fecha_inicial_unix" ] && [ "$fecha_archivo_unix" -le "$fecha_final_unix" ]; then
	
	# si el archivo no existe crearlo
	if [ ! -f "$directorio_datos_local/$archivo_mensual" ]; then
	    > "$directorio_datos_local/$archivo_mensual"
	fi

	# Agregar la fecha a cada línea del archivo actual y concatenar
	hdfs dfs -cat "$directorio_datos/$fecha_archivo.csv" | while IFS= read -r linea; do
            echo "$linea,$fecha_archivo" >> "$directorio_datos_local/$archivo_mensual"
        done
	
    fi
    

done

# Subir archivo HDFS
hdfs dfs -put "$directorio_datos_local/$archivo_mensual" "$directorio_datos/$archivo_mensual"

# Eliminar el archivo
rm "$directorio_datos_local/$archivo_mensual"

archivo_mapreducer="../$directorio_script/ejercicio5.py"

python "$archivo_mapreducer" -r hadoop "hdfs:///user/alumno/$directorio_datos/$archivo_mensual"

hdfs dfs -rm "$directorio_datos/$archivo_semanal"
