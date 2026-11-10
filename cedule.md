# Planification de la maintenance par algorithme génétique

Ce projet utilise un **algorithme génétique** (écrit en Python, sans bibliothèque externe) pour planifier la maintenance de 7 unités de production d'électricité sur 4 périodes, tout en gardant une réserve de puissance maximale.

## Le problème

Une centrale compte 7 unités de production. Chaque unité doit être mise en maintenance pendant une ou deux périodes. Pendant la maintenance, sa puissance n'est plus disponible. Le but est de choisir un planning qui **maximise la réserve minimale** sur l'ensemble des périodes, en couvrant toujours la demande.

### Données

| Unité | 1  | 2  | 3  | 4  | 5  | 6  | 7  |
|-------|----|----|----|----|----|----|----|
| Puissance (MW) | 20 | 15 | 35 | 40 | 15 | 15 | 10 |

- Puissance totale : **150 MW**
- Demande par période : **80, 90, 65, 70 MW**

### Contraintes de maintenance

- Les unités 1 et 2 sont en maintenance pendant **2 périodes consécutives**.
- Les unités 3 à 7 sont en maintenance pendant **1 seule période**.

## Représentation (codage)

Chaque unité est codée par un gène de 4 bits, un bit par période (`1` = en maintenance, `0` = en service). Un individu (un planning complet) est une liste de 7 gènes.

| Type d'unité | Gènes autorisés |
|--------------|-----------------|
| Unités 1 et 2 (2 périodes) | `1100`, `0110`, `0011` |
| Unités 3 à 7 (1 période) | `1000`, `0100`, `0010`, `0001` |

Exemple d'individu : `["1100", "0011", "0100", "0010", "1000", "0001", "0100"]`

## Fonctionnement de l'algorithme

1. **Population initiale** : 20 individus générés aléatoirement.
2. **Réserve** : pour chaque période, `réserve = puissance totale − puissance en maintenance − demande`.
3. **Fitness** : la réserve minimale sur les 4 périodes. Si elle est ≤ 0, le planning est invalide et la fitness vaut 0.
4. **Sélection par loterie** (roulette) : la probabilité de choisir un individu est proportionnelle à sa fitness.
5. **Croisement** à un point (probabilité `pc = 0.8`), avec une coupure entre deux gènes, ce qui garde les gènes valides.
6. **Mutation par inversion** (probabilité `pm = 0.1` par gène) : inverse l'ordre des 4 bits d'un gène (par ex. `1100` devient `0011`). Les gènes restent toujours valides.
7. **Élitisme** : le meilleur individu trouvé est conservé à chaque génération.
8. **Arrêt** après 100 générations.

## Paramètres

| Paramètre | Valeur |
|-----------|--------|
| Taille de la population | 20 |
| Nombre de générations | 100 |
| Probabilité de croisement (`pc`) | 0.8 |
| Probabilité de mutation (`pm`) | 0.1 |

Ces valeurs se modifient dans la fonction `algorithme_genetique()` et dans les arguments par défaut de `croisement()` et `mutation_inversion()`.

## Utilisation

Prérequis : Python 3 (uniquement le module standard `random`).

```bash
python nom_du_fichier.py
```

## Exemple de sortie

```
MEILLEUR PLANNING TROUVE
-------------------------
Unite 1 : 1100
Unite 2 : 0011
Unite 3 : 0010
Unite 4 : 0100
Unite 5 : 0001
Unite 6 : 1000
Unite 7 : 0100

Reserves par periode : [...]
Fitness : ... MW
```

Le résultat varie d'une exécution à l'autre, car l'algorithme est stochastique.

## Structure du code

| Fonction | Rôle |
|----------|------|
| `creer_individu()` / `creer_population()` | Génèrent la population initiale |
| `calculer_reserves()` | Calcule la réserve de chaque période |
| `fitness()` | Évalue la qualité d'un planning |
| `selection_loterie()` | Sélection des parents par roulette |
| `croisement()` | Croisement à un point |
| `mutation_inversion()` | Mutation par inversion des bits d'un gène |
| `algorithme_genetique()` | Boucle principale et affichage du résultat |

## Pistes d'amélioration

- Ajouter un critère d'arrêt basé sur la stagnation de la fitness.
- Tester d'autres opérateurs (sélection par tournoi, croisement à deux points).
- Tracer l'évolution de la fitness au fil des générations.
- Fixer la graine aléatoire (`random.seed`) pour des résultats reproductibles.
