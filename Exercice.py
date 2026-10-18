import random
import math
 

couts = [[5, 3, 4],     # D1 -> M1, M2, M3
         [6, 7, 2]]     # D2 -> M1, M2, M3
offre = [8, 9]          # containers dans D1 et D2
demande = [4, 5, 8]     # demandes de M1, M2, M3
 
 
def cout_total(d1):
    # d1 = quantités envoyées par D1 ; D2 envoie le reste (demande - d1)
    d2 = [demande[j] - d1[j] for j in range(3)]
    total = 0
    for j in range(3):
        total += couts[0][j] * d1[j] + couts[1][j] * d2[j]
    return total
 
 
def est_valide(d1):
    # aucune quantité négative et on ne dépasse pas la demande
    for j in range(3):
        if d1[j] < 0 or d1[j] > demande[j]:
            return False
    return True
 
 
def generer_voisins_transport(d1):
    # on déplace 1 container d'un magasin j vers un magasin k
    voisins = []
    for j in range(3):
        for k in range(3):
            if j != k:
                voisin = d1[:]
                voisin[j] -= 1
                voisin[k] += 1
                if est_valide(voisin):
                    voisins.append(voisin)
    return voisins
 
 
def tabou_transport(taille_tabou, max_iter):
    solution = [4, 4, 0]                      # solution initiale (D1 envoie 4, 4, 0)
    best_solution = solution
    best_cout = cout_total(solution)
    tabu_list = []
    print("Départ :", solution, "coût =", best_cout)
 
    for it in range(1, max_iter + 1):
        # voisins non tabous
        voisins = [v for v in generer_voisins_transport(solution) if v not in tabu_list]
        if not voisins:
            break
        # on prend le meilleur voisin
        solution = min(voisins, key=cout_total)
        tabu_list.append(solution)
        if len(tabu_list) > taille_tabou:
            tabu_list.pop(0)
        if cout_total(solution) < best_cout:
            best_solution = solution
            best_cout = cout_total(solution)
        print("it", it, ":", solution, "coût =", cout_total(solution))
    return best_solution, best_cout
 
 
print("===== EXERCICE 2 =====")
sol, cout = tabou_transport(taille_tabou=3, max_iter=6)
print("D1 envoie :", sol)
print("D2 envoie :", [demande[j] - sol[j] for j in range(3)])
print("Coût minimal trouvé :", cout)
