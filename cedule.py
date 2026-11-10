import random

# =====================================
# 1. DONNEES DU PROBLEME
# =====================================

puissances = [20, 15, 35, 40, 15, 15, 10]
demande = [80, 90, 65, 70]

puissance_totale = sum(puissances)

# Genes autorises pour chaque unite
genes_2_periodes = ["1100", "0110", "0011"]
genes_1_periode = ["1000", "0100", "0010", "0001"]


# =====================================
# 2. CREATION D'UN INDIVIDU
# =====================================

def creer_individu():

    individu = []

    for i in range(7):

        if i < 2:
            gene = random.choice(genes_2_periodes)
        else:
            gene = random.choice(genes_1_periode)

        individu.append(gene)

    return individu


# =====================================
# 3. CREATION DE LA POPULATION
# =====================================

def creer_population(taille):

    population = []

    for i in range(taille):
        population.append(creer_individu())

    return population


# =====================================
# 4. CALCUL DES RESERVES
# =====================================

def calculer_reserves(individu):

    reserves = []

    for periode in range(4):

        puissance_maintenance = 0

        for unite in range(7):

            if individu[unite][periode] == "1":
                puissance_maintenance += puissances[unite]

        puissance_disponible = (
                puissance_totale - puissance_maintenance
        )

        reserve = puissance_disponible - demande[periode]

        reserves.append(reserve)

    return reserves


# =====================================
# 5. CALCUL DE LA FITNESS
# =====================================

def fitness(individu):

    reserves = calculer_reserves(individu)

    # Le planning doit respecter toutes les demandes
    if min(reserves) <= 0:
        return 0

    # On maximise la reserve minimale
    return min(reserves)


# =====================================
# 6. SELECTION PAR LOTERIE
# =====================================

def selection_loterie(population):

    fitnesses = [fitness(ind) for ind in population]

    total = sum(fitnesses)

    # Si toutes les fitness sont nulles,
    # on choisit un individu au hasard
    if total == 0:
        return random.choice(population).copy()

    tirage = random.uniform(0, total)

    cumul = 0

    for i in range(len(population)):

        cumul += fitnesses[i]

        if tirage <= cumul:
            return population[i].copy()

    return population[-1].copy()


# =====================================
# 7. CROISEMENT
# =====================================

def croisement(parent1, parent2, pc=0.8):

    enfant1 = parent1.copy()
    enfant2 = parent2.copy()

    if random.random() < pc:

        # Coupure entre deux blocs de genes
        point = random.randint(1, 6)

        enfant1 = parent1[:point] + parent2[point:]
        enfant2 = parent2[:point] + parent1[point:]

    return enfant1, enfant2


# =====================================
# 8. MUTATION PAR INVERSION
# =====================================

def mutation_inversion(individu, pm=0.1):

    individu = individu.copy()

    for i in range(7):

        if random.random() < pm:

            # Inversion de l'ordre des 4 bits du gene
            individu[i] = individu[i][::-1]

    return individu


# =====================================
# 9. ALGORITHME GENETIQUE
# =====================================

def algorithme_genetique():

    taille_population = 20
    nombre_generations = 100

    # Initialisation
    population = creer_population(taille_population)

    meilleur_global = None
    meilleure_fitness = -1

    for generation in range(nombre_generations):

        # Evaluation de la population
        for individu in population:

            score = fitness(individu)

            if score > meilleure_fitness:

                meilleure_fitness = score
                meilleur_global = individu.copy()

        # Nouvelle population
        nouvelle_population = []

        # Elitisme : garder le meilleur individu
        nouvelle_population.append(meilleur_global.copy())

        while len(nouvelle_population) < taille_population:

            # Selection des parents par loterie
            parent1 = selection_loterie(population)
            parent2 = selection_loterie(population)

            # Croisement
            enfant1, enfant2 = croisement(parent1, parent2)

            # Mutation par inversion
            enfant1 = mutation_inversion(enfant1)
            enfant2 = mutation_inversion(enfant2)

            nouvelle_population.append(enfant1)

            if len(nouvelle_population) < taille_population:
                nouvelle_population.append(enfant2)

        # Remplacement de l'ancienne population
        population = nouvelle_population

    # Affichage du meilleur resultat
    print("\nMEILLEUR PLANNING TROUVE")
    print("-------------------------")

    for i in range(7):
        print("Unite", i + 1, ":", meilleur_global[i])

    reserves = calculer_reserves(meilleur_global)

    print("\nReserves par periode :", reserves)
    print("Fitness :", meilleure_fitness, "MW")


# =====================================
# 10. EXECUTION
# =====================================

algorithme_genetique()
