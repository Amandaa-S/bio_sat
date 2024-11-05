
from utils import *
from pysat.formula import CNF
from pysat.solvers import Solver
from pysat.card import CardEnc, EncType
import sys


def encode(genotypes, n, m):
    """
    Codifica los genotipos en una fórmula CNF.

    Entrada:
    - genotypes (list of lists): Lista de listas, donde cada lista representa un genotipo de tamaño m.
    - n (int): Número de haplotipos (candidatos).
    - m (int): Número de sitios polimórficos.

    Salida:
    - cnf: Un objeto CNF que representa las restricciones del problema.
    """

    cnf = CNF()

    # Crea variables para haplotipos h_kj: variable sitio j del haplotipo k cant
    haplotype_vars = [[(k * m) + j + 1 for j in range(m)] for k in range(n)]

    # Crea variables selectoras s_ki^a y s_ki^b: selecciona haplotipo k para genotipo i
    selector_a = [[(n * m) + (i * n) + k + 1 for k in range(n)] for i in range(len(genotypes))]
    selector_b = [[(n * m) + (i * n) + n + k + 1 for k in range(n)] for i in range(len(genotypes))]

    #h_kj son n*m variables
    assert len(haplotype_vars) == n
    assert len(haplotype_vars[0]) == m

    #s_ki^a y s_ki^b son num_genotipos*n variables cada uno
    assert len(selector_a) == len(genotypes) == len(selector_b)
    assert len(selector_a[0]) == len(selector_b[0]) == n

    # Restricciones
    # Por cada genotipo
    for i, genotype in enumerate(genotypes): 

        # Selección única: exactamente 1 haplotipo para selector_a y selector_b
        cnf.extend(CardEnc.equals(selector_a[i], bound=1, encoding=EncType.pairwise, top_id=cnf.nv))  
        cnf.extend(CardEnc.equals(selector_b[i], bound=1, encoding=EncType.pairwise, top_id=cnf.nv))

        # Por cada sitio polimorfico
        for j in range(m):
            if genotype[j] == 0:
                #Para k = 1, .. n ((neg h_kj or neg s_ki^a) and (neg h_kj or neg s_ki^b))
                for k in range(n):
                    cnf.append([-haplotype_vars[k][j], -selector_a[i][k]])
                    cnf.append([-haplotype_vars[k][j], -selector_b[i][k]])
                
            elif genotype[j] == 1:
                #Para k = 1, .. n ((h_kj or neg s_ki^a) and (h_kj or neg s_ki^b))
                for k in range(n):
                    cnf.append([haplotype_vars[k][j], -selector_a[i][k]])
                    cnf.append([haplotype_vars[k][j], -selector_b[i][k]])
            else:
                # Se crean g_ij^a y g_ij^b
                g_a = (2 * n * m) + i * m + j * 2 + cnf.nv + 1  
                g_b = g_a + 1
                
                # Deben tener valores opuestos: (neg g_ij^a or neg g_ij^b) and (g_ij^a or g_ij^b)
                cnf.append([-g_a, -g_b])
                cnf.append([g_a, g_b])
                
                # Restringir la asignación de valores en función de g_ij^a y g_ij^b
                for k in range(n):
                    cnf.append([haplotype_vars[k][j], -g_a, -selector_a[i][k]])  
                    cnf.append([-haplotype_vars[k][j], g_a, -selector_a[i][k]])  
                    cnf.append([haplotype_vars[k][j], -g_b, -selector_b[i][k]])  
                    cnf.append([-haplotype_vars[k][j], g_b, -selector_b[i][k]]) 


    return cnf


def decode_from_model(model, genotypes, n, m):
    """
    Decodifica el modelo resultante en haplotipos y pares de haplotipos.

    Entrada:
    - model: Modelo resultante del solver, que contiene la asignación de variables.
    - genotypes (list of lists): Lista de listas, donde cada lista representa un genotipo de tamaño m.
    - n: Número de haplotipos (candidatos).
    - m: Número de sitios polimórficos.

    Salida:
    - haplotypes (list of lists): Lista de haplotipos
    - par_haplotypes: Lista de pares de haplotipos que explican cada genotipo.
    """

    # Encuentra lista de haplotipos seleccionados
    haplotypes = []
    for k in range(n):
        haplotype = [0] * m
        for j in range(m):
            if (k * m) + j + 1 in model:
                haplotype[j] = 1
        haplotypes.append(haplotype)

    # Decodificar los selectores
    selector_a = [[(n * m) + (i * n) + k + 1 for k in range(n)] for i in range(len(genotypes))]
    selector_b = [[(n * m) + (i * n) + n + k + 1 for k in range(n)] for i in range(len(genotypes))]

    # Encuentra par de haplotipos que explican cada genotipo
    par_haplotypes = []

    for i in range(len(genotypes)):
        haplotype_a, haplotype_b = None, None

        # Buscar el haplotipo seleccionado para selector_a
        for k in range(n):
            if selector_a[i][k] in model:
                haplotype_a = haplotypes[k]
                break

        # Buscar el haplotipo seleccionado para selector_b
        for k in range(n):
            if selector_b[i][k] in model:
                haplotype_b = haplotypes[k]
                break

        # Agregar el par de haplotipos que explican el genotipo i
        if haplotype_a is not None and haplotype_b is not None:
            par_haplotypes.append((haplotype_a, haplotype_b))
    return haplotypes, par_haplotypes

def solve(instance):
    """
    Resuelve la instancia.

    Entrada:
    - instance: Ruta al archivo de instancia que contiene haplotipos y genotipos.

    Salida:
    - Imprime un resumen de la instancia y la solución encontrada
    - Imprime tiempo de ejecución y estadísticas del CNF (cantidad de cláusulas y restricciones)
    """

    # Leer instancia
    print("Instancia: " , instance)
    n_hap, m, haplotypes, genotypes = read_instance(instance)

    #Mostrar información de la instancia
    print("# Parámetros de la instancia")
    print("Número de haplotipos:", n_hap)
    print("Número de genotipos:", n_hap // 2)
    print("Cantidad de sitios polimórficos:", m)
    print("Haplotipos:")
    for hap in haplotypes:
        print(hap)
    print("Genotipos:")
    for geno in genotypes:
        print(geno)
    
    #Algoritmo: utiliza upper y lower bound para encontrar el número de haplotipos que explican los genotipos
    lb = 1
    ub = n_hap

    solution_found = False
    print("Solving...")

    # Variables para estadísticas finales
    tiempos = [] #lista de tiempos de ejecución
    clauses = [] #lista de cantidad de cláusulas
    variables = [] #lista de cantidad de variables

    while lb <= ub:
        #Probar con r = (lb + ub) // 2 haplotipos
        r = (lb + ub) // 2

        # Encode
        cnf = encode(genotypes, r, m)

        # Restricción de cardinalidad para limitar el número de haplotipos candidatos
        haplotype_candidates = [i + 1 for i in range(r)]
        cnf.extend(CardEnc.atmost(haplotype_candidates, r, encoding=EncType.pairwise, top_id=cnf.nv))

        # Solver
        with Solver(bootstrap_with=cnf, use_timer=True) as solver:
            if solver.solve():
                model = solver.get_model()
                sol_hap, par_hap = decode_from_model(model, genotypes, r, m)

                # Verificar la solución
                if verify_sol(par_hap, genotypes):
                    solution_found = True
                    print(f"Solución válida encontrada para r={r} haplotipos")
                    print("Haplotipos inferidos:")
                    for hap in sol_hap:
                        print(hap)
    
                    ub = r - 1  # Intentar con menos haplotipos
                else:
                    lb = r + 1  # Incrementar límite inferior
            else:
                lb = r + 1  # Incrementar límite inferior
            tiempos.append(solver.time())
            clauses.append(len(cnf.clauses))
            variables.append(cnf.nv)
    if solution_found:
        print("######")        
        #nombre instancia, si encuentra solución o no: 1 o 0, numero genotipos, cantidad de sitios polimórficos, r, tiempo total, cantidad de clausulas, cantidad de variables
        print(instance, 1, n_hap // 2, m, len(sol_hap), sum(tiempos), sum(clauses), sum(variables), sep=",")

    elif not solution_found:
        print("######")        
        print(instance, 0, n_hap // 2, m, 0, sum(tiempos), sum(clauses), sum(variables), sep=",")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(1)
    
    instance = sys.argv[1]
    solve(instance)