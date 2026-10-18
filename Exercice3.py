import random
import math
X = 1000
distances = [
    [0, 14, 15, X, X, X, X, 17],
    [14, 0, 13, 14, 20, X, X, 21],
    [15, 13, 0, 11, 21, 17, 9, 9],
    [X, 14, 11, 0, 11, 10, 8, 20],
    [X, 20, 21, 11, 0, 15, 18, X],
    [X, X, 17, 10, 15, 0, 9, X],
    [X, X, 9, 8, 18, 9, 0, 13],
    [17, 21, 9, 20, X, X, 13, 0],
]
 
 
def calculer_distance(solution):
    distance = 0
    for i in range(len(solution) - 1):
        distance += distances[solution[i]][solution[i + 1]]
    distance += distances[solution[-1]][solution[0]]    # retour à la ville de départ
    return distance
 
 
def afficher(solution):
    # les villes sont numérotées à partir de 1 dans l'énoncé
    return "-".join(str(v + 1) for v in solution + [solution[0]])
 
 
# ---------- Question 1 : Recherche Tabou ----------
def generer_voisins(solution):
    # échange de 2 villes (la ville 1 reste au début)
    voisins = []
    for i in range(1, len(solution)):
        for j in range(i + 1, len(solution)):
            voisin = solution[:]
            voisin[i], voisin[j] = voisin[j], voisin[i]
            voisins.append(voisin)
    return voisins
 
 
def tabou_pvc(taille_tabou, max_iter):
    solution = [0, 1, 2, 3, 4, 5, 6, 7]       # solution initiale 1-2-3-4-5-6-7-8-1
    best_solution = solution
    best_distance = calculer_distance(solution)
    tabu_list = []
    print("Départ :", afficher(solution), "distance =", best_distance)
 
    for it in range(1, max_iter + 1):
        voisins = [v for v in generer_voisins(solution) if v not in tabu_list]
        if not voisins:
            break
        solution = min(voisins, key=calculer_distance)
        tabu_list.append(solution)
        if len(tabu_list) > taille_tabou:
            tabu_list.pop(0)
        if calculer_distance(solution) < best_distance:
            best_solution = solution
            best_distance = calculer_distance(solution)
        print("it", it, ":", afficher(solution), "distance =", calculer_distance(solution))
    return best_solution, best_distance
 
 
print("\n===== EXERCICE 3 - Q1 : TABOU =====")
sol, dist = tabou_pvc(taille_tabou=50, max_iter=20)
print("Meilleure solution :", afficher(sol), "distance =", dist)
 
 
# ---------- Question 2 : Recuit Simulé (5 itérations) ----------
def recuit_simule(T0, details=False, max_iter=5, alpha=0.9):
    solution = [0, 1, 2, 3, 4, 5, 6, 7]
    distance = calculer_distance(solution)
    best_solution = solution
    best_distance = distance
    T = T0
 
    for it in range(1, max_iter + 1):
        # voisin : on inverse une partie de la tournée (2-opt)
        i, j = sorted(random.sample(range(1, 8), 2))
        voisin = solution[:i] + solution[i:j + 1][::-1] + solution[j + 1:]
        dist_voisin = calculer_distance(voisin)
        delta = dist_voisin - distance
 
        # on accepte si meilleur, sinon avec la probabilité exp(-delta/T)
        if delta < 0 or random.random() < math.exp(-delta / T):
            solution = voisin
            distance = dist_voisin
            if distance < best_distance:
                best_solution = solution
                best_distance = distance
        if details:
            print("it", it, "| T =", round(T, 1), "|", afficher(solution), "| distance =", distance)
        T = T * alpha                          # refroidissement
    return best_solution, best_distance
 
 
print("\n===== EXERCICE 3 - Q2 : RECUIT SIMULE (T0 = 20) =====")
random.seed(1)
sol, dist = recuit_simule(T0=20, details=True)
print("Meilleure solution :", afficher(sol), "| distance =", dist)
random.seed(1)
sol, dist = recuit_simule(T0=100, details=True)
print("Meilleure solution :", afficher(sol), "| distance =", dist)
 
print("\n===== Variation de la température T0 (100 essais chacune) =====")
for T0 in [1, 5, 10, 20, 50, 100]:
    resultats = []
    for essai in range(100):
        sol, dist = recuit_simule(T0)
        resultats.append(dist)
    moyenne = sum(resultats) / len(resultats)
    print("T0 =", T0, "| moyenne =", round(moyenne, 1), "| minimum =", min(resultats))
