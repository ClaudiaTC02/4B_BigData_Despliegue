
directorio_script=$(dirname "$0")

directorio_datos="../$directorio_script/datos"

read -p "Introduce la fecha inicial: " fecha_inicial
read -p "Introduce la fecha final: " fecha_final
read -p "Introduce el nombre de una acción: " nombre_accion

fecha_inicial_unix=$(date -d "$(echo "$fecha_inicial" | awk -F '-' '{print $3"-"$2"-"$1}')" +%s)

fecha_final_unix=$(date -d "$(echo "$fecha_final" | awk -F '-' '{print $3"-"$2"-"$1}')" +%s)

archivo_semanal="Ejercicio3_${fecha_inicial}_${fecha_final}.csv"

ls "../$directorio_script/datos/" | while read -r archivo; do

    # Obteniendo la fecha del archivo
    fecha_archivo=$(echo "$archivo" | awk -F "." '{print $1}')
    fecha_archivo_unix=$(date -d "$(echo "$fecha_archivo" | awk -F '-' '{print $3"-"$2"-"$1}')" +%s)

    # Comprobando si se encuentra dentro del rango
    if [ "$fecha_archivo_unix" -ge "$fecha_inicial_unix" ] && [ "$fecha_archivo_unix" -le "$fecha_final_unix" ]; then
	
	# si el archivo no existe crearlo
	if [ ! -f "$directorio_datos/$archivo_semanal" ]; then
	    > "$directorio_datos/$archivo_semanal"
	fi
	
        cat "$directorio_datos/$archivo" >> "$directorio_datos/$archivo_semanal"
    fi
    

done

archivo_mapreducer="$directorio_script/ejercicio3.py"

python "$archivo_mapreducer" "$directorio_datos/$archivo_semanal" --accion "$nombre_accion"

# Eliminar el archivo
rm "$directorio_datos/$archivo_semanal"
