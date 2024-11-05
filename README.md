# Inferencia de Haplotipos mediante Modelos SAT

## Descripción: 

Este repositorio contiene la implementación de encodings propuestos para el problema de inferencia de haplotipos, donde el objetivo es deducir las combinaciones de alelos en cromosomas homólogos a partir de datos de genotipos.

El problema se formula como un problema de satisfacibilidad booleana (SAT), buscando un conjunto mínimo de haplotipos que explique los genotipos dados mediante una combinación de restricciones lógicas. Se utilizan las formulaciones propuestas que denominaremos "algoritmo original" y "algoritmo optimizado", basadas en el artículo de Lynce y Marques-Silva [1].

## Estructura del Repositorio

- **experiments**: Archivos bash para generar instancias y correr experimentos.
  - **results**: 
    - `f1`: Resultados del algoritmo original.
    - `f2`: Resultados del algoritmo optimizado.
- **instances**: Archivos `.txt` con cada instancia; el nombre sigue el formato `ms_<num_haplotipos>_<num_sitios>`.
- **results**: Archivos `.csv` con resultados y notebooks con análisis de los mismos.
- **src**: Código fuente.
  - `f1.py`: Código del algoritmo original.
  - `f2.py`: Código del algoritmo optimizado.
    

## Instalación

1. Clona el repositorio.
2. Navega al directorio del repositorio.
3. Instala las dependencias con:

   ```bash
   pip install -r requirements.txt
   ```

Además, se puede utilizar el generador de instancias. Si deseas crear nuevas instancias, se describe y proporciona el enlace a continuación.


## Generación instancias:

Para generar muestras que sirvan como instancias para el modelo SAT en el problema de inferencia de haplotipos, se utiliza "ms", un programa que genera muestras permitiendo definir parámetros que simulen polimorfismos en diferentes configuraciones poblacionales [2].

- Código fuente: [ms](https://uchicago.app.box.com/s/l3e5uf13tikfjm7e1il1eujitlsjdx13)


# Uso

Se incluye un Makefile para la generación de experimentos. Puedes utilizar los siguientes comandos:

- Para generar instancias: 

    ```bash
    make generate_instances
    ```

 - Para ejecutar los experimentos: 

    ```bash
    make run_experiments
    ```

 - Para limpiar los resultados y las instancias generadas:

    ```bash
    make clean
    ```

Para correr sobre instancias individuales, ejecuta:

 ```bash
   python src/f1.py ruta/instancia  # Para el algoritmo original
   python src/f2.py ruta/instancia  # Para el algoritmo optimizado
   ```


## Referencias

[1] Lynce, I., & Marques-Silva, J. (2006). SAT in Bioinformatics: Making the Case with Haplotype Inference. In Lecture notes in computer science (pp. 136–141). https://doi.org/10.1007/11814948_16

[2] Hudson, R. R. (2002) Generating samples under a Wright-Fisher neutral
model of genetic variation. Bioinformatics 18: 337-338.