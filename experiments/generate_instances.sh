#!/bin/bash

# Experimentos número de genotipos y sitios polimórficos
START_GENOTYPES=2
END_GENOTYPES=100  
START_SITES=2      
END_SITES=20     

# Crea el directorio para guardar las instancias si no existe
dir_generator=$1
dir_instances=$2


mkdir -p "$dir_instances"

# Generar instancias: ../msdir/ms <num_genotipos> 1 -s <num_sites>
for (( num_genotipos=START_GENOTYPES; num_genotipos<=END_GENOTYPES; num_genotipos+=2 ))
do
    for (( num_sites=START_SITES; num_sites<=END_SITES; num_sites++ ))
    do
        INSTANCE_FILE="${dir_instances}/ms_${num_genotipos}_${num_sites}.txt"
        "$dir_generator" "$num_genotipos" 1 -s "$num_sites" > "$INSTANCE_FILE"
    done
done

echo "Todas las instancias han sido generadas."


