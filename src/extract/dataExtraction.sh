
directorio_script=$(dirname "$0")

while true; do
    
    hora_actual=$(date +"%H%M")

    # formato de la fecha DD-MM-YYYY
    fecha_actual=$(date +"%d-%m-%Y")

    dia_semana=$(date +"%u")

    # Directorio donde se guardará el archivo de datos
    directorio_datos="$directorio_script/../datos"

    # Crear el directorio de datos si no existe
    mkdir -p "$directorio_datos"

    archivo_datos="${fecha_actual}.csv"

    # Hora en el que funcionará el script: de 9:30 a 18:30 de lunes a viernes

    if [ "$hora_actual" -ge "0930" ] && [ "$hora_actual" -le "1830" ] && [ "$dia_semana" -ge 1 ] && [ "$dia_semana" -le 5 ]; then

	# Si el archivo no existe, crearlo
	if [ ! -f "$directorio_datos/$archivo_datos" ]; then
	    echo "Hola"
	    > "$directorio_datos/$archivo_datos"
	    chmod +w "$directorio_datos/$archivo_datos"
	fi
    
	python "$directorio_script/scraper.py" | awk -F "," -v hora="$hora_actual" '{print $1 "," $2 "," $6 "," $7 "," substr(hora, 1, 2) ":" substr(hora, 3, 2)}' >> "$directorio_datos/$archivo_datos"
    
    fi


    # Dormir 1 h
    sleep 3600
done
