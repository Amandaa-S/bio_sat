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
                for k in range(n):
                    cnf.append([-haplotype_vars[k][j], -selector_a[i][k]])
                    cnf.append([-haplotype_vars[k][j], -selector_b[i][k]])
            elif genotype[j] == 1:
                for k in range(n):
                    cnf.append([haplotype_vars[k][j], -selector_a[i][k]])
                    cnf.append([haplotype_vars[k][j], -selector_b[i][k]])
            else:
                t = (2 * n * m) + i * m + j + 1 + cnf.nv
                cnf.append([-t, -haplotype_vars[0][j], -selector_a[i][0]])
                cnf.append([t, haplotype_vars[0][j], selector_a[i][0]])
    return cnf

def decode_from_model(model, genotypes, num_haplotypes, num_sitios):
    """
    Decodifica el modelo resultante en haplotipos y pares de haplotipos.

    Entrada:
    - model: Modelo resultante del solver, que contiene la asignación de variables.
    - genotypes (list of lists): Lista de listas, donde cada lista representa un genotipo de tamaño m.
    - num_haplotipos (int): Número de haplotipos (candidatos).
    - num_sitios (int): Número de sitios polimórficos.

    Salida:
    - haplotypes (list of lists): Lista de haplotipos.
    - par_haplotipos: Lista de pares de haplotipos que explican cada genotipo.
    """

    haplotypes = []
    for k in range(num_haplotypes):
        haplotype = [0] * num_sitios
        for j in range(num_sitios):
            if (k + 1) * (j + 1) in model:
                haplotype[j] = 1
        haplotypes.append(haplotype)

    selector_a = [[(num_haplotypes + 1) * i + k + 1 for k in range(num_haplotypes)] for i in range(len(genotypes))]
    selector_b = [[(num_haplotypes + 1) * i + num_haplotypes + k + 1 for k in range(num_haplotypes)] for i in range(len(genotypes))]

    haplotypes_par = []

    for i in range(len(genotypes)):
        haplotype_a, haplotype_b = None, None

        for k in range(num_haplotypes):
            if selector_a[i][k] in model:
                haplotype_a = haplotypes[k]
                break

        for k in range(num_haplotypes):
            if selector_b[i][k] in model:
                haplotype_b = haplotypes[k]
                break

        if haplotype_a is not None and haplotype_b is not None:
            haplotypes_par.append((haplotype_a, haplotype_b))
    return haplotypes, haplotypes_par

def solve(instance):
    """
    Resuelve la instancia.

    Entrada:
    - instance: Ruta al archivo de instancia que contiene haplotipos y genotipos.

    Salida:
    - Imprime un resumen de la instancia y la solución encontrada.
    - Imprime tiempo de ejecución y estadísticas del CNF (cantidad de cláusulas y restricciones).
    """
    print("Instancia: ", instance)

    n_hap, m, haplotypes, genotypes = read_instance(instance)

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
    
    lb = 1
    ub = n_hap

    solution_found = False
    print("Solving...")

    tiempos = []
    clauses = []
    variables = []

    while lb <= ub:
        r = (lb + ub) // 2

        # Encode utilizando la nueva formulación
        cnf = encode(genotypes, r, m)

        haplotype_candidates = [i + 1 for i in range(r)]
        cnf.extend(CardEnc.atmost(haplotype_candidates, r, encoding=EncType.pairwise, top_id=cnf.nv))

        with Solver(bootstrap_with=cnf, use_timer=True) as solver:
            if solver.solve():
                model = solver.get_model()
                sol_hap, par_hap = decode_from_model(model, genotypes, r, m)

                if verify_sol(par_hap, genotypes):
                    solution_found = True
                    print(f"Solución válida encontrada para r={r} haplotipos")
                    print("Haplotipos inferidos:")
                    for hap in sol_hap:
                        print(hap)
    
                    ub = r - 1
                else:
                    lb = r + 1
            else:
                lb = r + 1
            tiempos.append(solver.time())
            clauses.append(len(cnf.clauses))
            variables.append(cnf.nv)

    if solution_found:
        print("######")
        print(instance, 1, n_hap // 2, m, len(sol_hap), sum(tiempos), sum(clauses), sum(variables), sep=",")
    else:
        print("######")
        print(instance, 0, n_hap // 2, m, 0, sum(tiempos), sum(clauses), sum(variables), sep=",")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(1)
    
    instance = sys.argv[1]
    solve(instance)

