#!/bin/bash

# Directorios
RESULTS_DIR=$1
OUTPUT_CSV_DIR=$2

# Archivos de salida
OUTPUT_CSV_F1="$OUTPUT_CSV_DIR/resultados_f1.csv"
OUTPUT_CSV_F2="$OUTPUT_CSV_DIR/resultados_f2.csv"

echo "instance,solved,num_genotipos,num_sitios,solucion,time,num_clausulas,num_variables" > "$OUTPUT_CSV_F1"
echo "instance,solved,num_genotipos,num_sitios,solucion,time,num_clausulas,num_variables" > "$OUTPUT_CSV_F2"

process_results() {
    local dir=$1
    local output_csv=$2
    for result_file in "$dir"/*.txt; do
        # Verifica si hay archivos en el directorio
        if [ ! -e "$result_file" ]; then
            echo "No se encontraron archivos en $dir"
            continue
        fi
        
        # Lee el archivo y busca líneas que contienen "######" (indica que hay solución)
        local found_solution=0
        while IFS= read -r line; do
            if [[ "$line" == "######" ]]; then
                read -r solution_line 
                IFS=',' read -r instance solved num_genotipos num_sitios solucion time num_clausulas num_variables <<< "$solution_line"
                
                # Solo agrega al si se encontró una solución (solved == 1)
                if [[ "$solved" -eq 1 ]]; then
                    echo "$instance,$solved,$num_genotipos,$num_sitios,$solucion,$time,$num_clausulas,$num_variables" >> "$output_csv"
                    found_solution=1
                fi
            fi
        done < "$result_file"

        # Verifica si el archivo contiene "TIMEOUT" al final
        if [[ $(tail -n 1 "$result_file") == "TIMEOUT" ]]; then
            # Si hay un timeout, se registra como no resuelto
            echo "$instance,0,$num_genotipos,$num_sitios,N/A,time,$num_clausulas,$num_variables" >> "$output_csv"
        fi
    done
}

process_results "$RESULTS_DIR/f1" "$OUTPUT_CSV_F1"
process_results "$RESULTS_DIR/f2" "$OUTPUT_CSV_F2"
