# Heur_MetaHeur
# TD2 – Transport et Voyageur de Commerce

Résolution de deux problèmes d'optimisation en Python avec la **Recherche Tabou** et le **Recuit Simulé**.

## Exercice 2 : problème de transport

Deux dépôts contiennent 8 et 9 containers. Trois magasins demandent 4, 5 et 8 containers. L'objectif est de minimiser le coût total de transport.

| | M1 | M2 | M3 | Dépôt |
|---|---|---|---|---|
| D1 | 5 | 3 | 4 | 8 |
| D2 | 6 | 7 | 2 | 9 |

**Modèle :** minimiser Σ cᵢⱼ · xᵢⱼ, avec Σⱼ xᵢⱼ = offreᵢ, Σᵢ xᵢⱼ = demandeⱼ et xᵢⱼ entier.

**Méthode (tabou) :**
- Une solution est la ligne de D1 ; D2 envoie le reste.
- Départ : `[4, 4, 0]` (coût 55).
- Voisin : déplacer 1 container d'un magasin à un autre.

**Résultat :** D1 envoie (3, 5, 0) et D2 envoie (1, 0, 8), soit un **coût minimal de 52**.
<img width="1601" height="270" alt="image" src="https://github.com/user-attachments/assets/b42bce42-f272-445c-ac70-862d5171378f" />

---

## Exercice 3 : voyageur de commerce (8 villes)

Les liaisons « - » de l'énoncé valent 1000 dans le programme. La matrice est symétrique.

### Q1 : Recherche Tabou

- Départ : 1-2-3-4-5-6-7-8-1 (distance 103)
- Voisin : échange de deux villes
- Liste tabou : 50 solutions, 20 itérations

**Résultat :** 1-2-4-5-6-7-3-8-1, **distance 98** (optimum).

### Q2 : Recuit Simulé

- 5 itérations, T ← 0,9 × T
- Voisin : inversion d'une partie de la tournée (2-opt)
- Une solution moins bonne est acceptée avec la probabilité exp(−Δ/T)
- Test de T₀ = 1, 5, 10, 20, 50, 100 (100 essais chacune)

| T₀ | Moyenne | Minimum |
|---|---|---|
| 1 | 103,0 | 103 |
| 5 | 103,0 | 102 |
| 10 | 103,0 | 103 |
| 20 | 102,9 | 98 |
| 50 | 102,9 | 100 |
| 100 | 102,9 | 98 |

**Conclusion :** avec seulement 5 itérations, la température change peu le résultat. Le tabou est beaucoup plus efficace ici.

---

## Remarques

- Le recuit simulé est aléatoire : les valeurs peuvent varier légèrement d'une exécution à l'autre.
- Une liste tabou trop courte (par exemple 5) fait tourner la recherche en rond autour de 103.
