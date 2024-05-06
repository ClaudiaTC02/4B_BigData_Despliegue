
directorio_script=$(dirname "$0")
directorio_datos="../$directorio_script/datos"

read -p "Introduce la fecha inicial: " fecha_inicial

fecha_inicial_unix=$(date -d "$(echo "$fecha_inicial" | awk -F '-' '{print $3"-"$2"-"$1}')" +%s)

fecha_final=$(date -d "@$((fecha_inicial_unix + 30 * 24 * 60 * 60))" "+%d-%m-%Y")
fecha_final_unix=$(date -d "@$((fecha_inicial_unix + 30 * 24 * 60 * 60))" "+%s")

archivo_mensual="Mes_${fecha_inicial}_${fecha_final}.csv"

ls "../$directorio_script/datos/" | while read -r archivo; do

    # Obteniendo la fecha del archivo
    fecha_archivo=$(echo "$archivo" | awk -F "." '{print $1}')
    fecha_archivo_unix=$(date -d "$(echo "$fecha_archivo" | awk -F '-' '{print $3"-"$2"-"$1}')" +%s)

    # Comprobando si se encuentra dentro del rango 1 semana
    if [ "$fecha_archivo_unix" -ge "$fecha_inicial_unix" ] && [ "$fecha_archivo_unix" -le "$fecha_final_unix" ]; then
	
	# si el archivo no existe crearlo
	if [ ! -f "$directorio_script/archivos/$archivo_mensual" ]; then
	    > "$directorio_script/archivos/$archivo_mensual"
	fi
		# Agregar la fecha a cada línea del archivo actual y concatenar
        while IFS= read -r linea; do
            echo "$linea,$fecha_archivo" >> "$directorio_datos/$archivo_mensual"
        done < "$directorio_datos/$archivo"
	
    fi
    

done

archivo_mapreducer="$directorio_script/ejercicio5.py"

python "$archivo_mapreducer" "$directorio_datos/$archivo_mensual" 


rm "$directorio_datos/$archivo_mensual"
