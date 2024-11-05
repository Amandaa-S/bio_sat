
def read_instance(filename):
    """
    Lee una instancia desde un archivo y extrae la información de haplotipos y genotipos.

    Entrada:
    - filename (str): Nombre del archivo que contiene la instancia de haplotipos.

    Salida:
    - n_hap (int): Número de haplotipos.
    - m (int): Número de sitios polimórficos (largo de cada haplotipo).
    - haplotypes (list of lists): Lista de haplotipos, donde cada haplotipo es una lista de enteros (0 o 1) de longitud m.
    - genotypes (list of lists): Lista de genotipos, donde cada genotipo es una lista de enteros (0, 1, o 2) de longitud m.
    """

    haplotypes = []
    genotypes = []

    #Abrir archivo
    with open(filename, "r") as file:
        lines = file.readlines()
    
        for i in range(len(lines)):
            lines[i] = lines[i].strip()
            if "ms" in lines[i]:
                #Cantidad de haplotipos en la muestra
                n_hap = int(lines[i].split()[1])
            if "segsites" in lines[i]:
                # Cantidad de sitios polimorficos
                m = int(lines[i].split()[1])
            if "positions" in lines[i]:
                break
        
        # Lee cada haplotipo
        for j in range(n_hap):
            hapl = list(map(int, lines[i+j+1].strip()))
            assert len(hapl) == m #verifica que la longitud del haplotipo sea igual a la cantidad de sitios polimorficos
            haplotypes.append(hapl)
            
        # Verifica que la cantidad de haplotipos sea correcta
        assert len(haplotypes) == n_hap

    # Generar genotipos
    genotypes = generar_genotipo(n_hap, m, haplotypes)

    #Verificar que la cantidad de genotipos sea igual a la mitad de la cantidad de haplotipos
    assert len(genotypes) == n_hap // 2    
    
    return n_hap, m, haplotypes, genotypes


def generar_genotipo(n_hap, m, haplotypes):
    """
    Genera una lista de genotipos a partir de una lista de haplotipos.

    Entrada:
    - n_hap (int): Número de haplotipos.
    - m (int): Número de sitios polimórficos.
    - haplotypes (list of lists): Lista de haplotipos, donde cada haplotipo es una lista de enteros (0 o 1) de longitud m.

    Salida:
    - genotypes (list of lists): Lista de genotipos, se obtiene a partir de pares de haplotipos,
    donde cada genotipo es una lista de enteros (0, 1, o 2) de longitud m
    """

    genotypes = []

    #Verifica que la cantidad de haplotipos sea par, ya que se generan los genotipos de dos en dos
    assert n_hap % 2 == 0

    #Recorrer los pares de haplotipos para generar los genotipos
    for i in range(0, n_hap, 2): 
        genotype = [] 
        hap1 = haplotypes[i]
        hap2 = haplotypes[i + 1]
        
        # Revisa cada sitio dentro de los haplotipos, si son distintos toma valor 2, si son iguales toma el valor del sitio
        for k in range(m):
            site1 = hap1[k]
            site2 = hap2[k]
            
            if site1 == site2:
                # Homocigoto: 0 o 1
                assert site1 == 0 or site1 == 1
                genotype.append(site1)  
            else:
                # Heterocigoto
                genotype.append(2)        
       
        #Verifica que el genotipo tenga la misma longitud que la cantidad de sitios polimorficos
        assert len(genotype) == m
        genotypes.append(genotype) 
    
    #Verifica que la cantidad de genotipos sea igual a la mitad de la cantidad de haplotipos
    assert len(genotypes) == n_hap // 2
    return genotypes


def verify_sol(haplotypes_par, genotypes):
    """
    Verifica que cada par de haplotipos explica correctamente su genotipo correspondiente.

    Entrada:
    - haplotypes_par (list of tuples): Lista de pares de haplotipos (tuplas de listas) que explican los genotipos. 
    - genotypes (list of lists): Lista de genotipos objetivo, donde cada genotipo es una lista de enteros (0, 1 o 2) de longitud m.

    Salida:
    - bool: True si todos los pares de haplotipos explican correctamente sus genotipos, `False` en caso contrario.
    """


    for i, (hap1, hap2) in enumerate(haplotypes_par):
        genotype = genotypes[i]
        
        # Verificar que el par de haplotipos explica correctamente el genotipo
        for j, m in enumerate(genotype):
            if m == 0:
                # Ambos haplotipos deben ser 0 en este sitio
                if not (hap1[j] == 0 and hap2[j] == 0):
                    return False
            elif m == 1:
                # Ambos haplotipos deben ser 1 en este sitio
                if not (hap1[j] == 1 and hap2[j] == 1):
                    return False
            elif m == 2:
                # Los haplotipos deben ser opuestos en este sitio
                if hap1[j] == hap2[j]:
                    return False

    return True
