#!/bin/bash

# Directorios de instancias y resultados
INSTANCE_DIR=$1
RESULTS_DIR=$2
SCRIPT_DIR=$3

mkdir -p "$RESULTS_DIR/f1"
mkdir -p "$RESULTS_DIR/f2"

for instance in "$INSTANCE_DIR"/*.txt; do
    if [ ! -e "$instance" ]; then
        echo "No se encontraron archivos de instancia en $INSTANCE_DIR"
        exit 1
    fi

    # Nombre del archivo de instancia
    instance_name=$(basename "$instance")

    # Nombre del archivo de salida para el algoritmo original
    result_file_f1="${RESULTS_DIR}/f1/${instance_name}"

    # Ejecuta el solver para f1 con un límite de tiempo de 10 minutos
    timeout 1m python "$SCRIPT_DIR/f1.py" "$instance" > "$result_file_f1"
    
    # Verifica si el comando fue interrumpido por el timeout
    if [ $? -eq 124 ]; then
        echo "TIMEOUT" >> "$result_file_f1"
    fi

    # Nombre del archivo de salida para el algoritmo optimizado
    result_file_f2="${RESULTS_DIR}/f2/${instance_name}"

    # Ejecuta el solver para f2 con un límite de tiempo de 10 minutos
    timeout 1m python "$SCRIPT_DIR/f2.py" "$instance" > "$result_file_f2"

    # Verifica si el comando fue interrumpido por el timeout
    if [ $? -eq 124 ]; then
        echo "TIMEOUT" >> "$result_file_f2"
    fi
done
