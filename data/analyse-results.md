# Analyse des résultats du module stats

## 1. Cadre de lecture statistique

Le fichier contient deux types de sorties :

- `simple` : une expérience unique par match-up (wins, winrate, IC95, durée moyenne),
- `repetitions` : une synthèse sur plusieurs expériences (moyenne, écart-type, min, max).

Pour interpréter correctement :

1. les lignes `simple` donnent une photographie ponctuelle ;
2. les lignes `repetitions` donnent la stabilité inter-runs ;
3. une conclusion forte doit s’appuyer en priorité sur les répétitions quand elles existent.

---

## 2. Lecture globale des forces relatives

### Niveau 1 — très forte

- `CheatAbsolute(see both)`

### Niveau 2 — fortes stratégies informées

- `MonteCarlo_median`
- `CheatMedianAllCards(median global)`
- `MedianRatio(hist)`
- `MonteCarlo_random`
- `MeanRatio(hist)`

### Niveau 3 — faibles

- `FirstStat(poids)`
- `Random`

---

## 3. Résultats robustes sur les baselines

## 3.1 `Random` et `FirstStat(poids)` sont équivalentes

- `Random` vs `FirstStat(poids)` : **49.7% vs 50.3%**
- IC95 (Interval de confiance à 95%)de A : **[46.61 ; 52.79]**

Lecture statistique : aucune différence significative détectable.

## 3.2 Les stratégies informées dominent `Random`

Contre `Random`, taux de victoire du bot informé :

- `MedianRatio(hist)` : **93.0%**
- `MeanRatio(hist)` : **90.6%**
- `MonteCarlo_random` : **90.2%**
- `MonteCarlo_median` : **92.1%**
- `CheatMedianAllCards` : **94.4%**
- `CheatAbsolute` : **98.7%**

Conclusion : le choix de caractéristique structure fortement l’issue du jeu.

## 3.3 Les mêmes tendances face à `FirstStat(poids)`

- `MedianRatio(hist)` : **90.0%**
- `MeanRatio(hist)` : **90.0%**
- `MonteCarlo_random` : **88.3%**
- `MonteCarlo_median` : **89.5%**
- `CheatMedianAllCards` : **90.7%**
- `CheatAbsolute` : **97.6%**

Les stratégies fixes sont donc de bonnes références, mais pas compétitives.

---

## 4. Comparaisons entre stratégies avancées

## 4.1 `MedianRatio(hist)` vs `MeanRatio(hist)`

Répétitions retenues :

- `MedianRatio(hist)` vs `MeanRatio(hist)` (1200 games, 10 reps) :
  - moyenne A = **55.28%**,
  - écart-type = **1.10**,
  - min/max = **53.67 / 57.63**.

Interprétation : `MedianRatio(hist)` domine `MeanRatio(hist)` de façon régulière sur ce protocole.

## 4.2 `MeanRatio(hist)` vs `MonteCarlo_random`

- `MeanRatio(hist)` vs `MonteCarlo_random` : **50.0% vs 50.0%**

Interprétation : pas d’avantage net du Monte Carlo random dans ce duel.

## 4.3 `MedianRatio(hist)` vs `MonteCarlo_random`

Répétitions retenues :

- (500 games, 5 reps) moyenne A = **55.27%**,
- écart-type = **1.33**,
- min/max = **53.26 / 56.60**.

Interprétation : sur ce protocole, `MedianRatio(hist)` garde un avantage mesurable contre `MonteCarlo_random`.

## 4.4 `MonteCarlo_median` vs heuristiques historiques

- `MeanRatio(hist)` vs `MonteCarlo_median` (200 games, 5 reps) :
  - moyenne A = **41.63%** (donc B ≈ **58.37%**).
- `MedianRatio(hist)` vs `MonteCarlo_median` (200 games, 5 reps) :
  - moyenne A = **45.67%** (donc B ≈ **54.33%**).

Conclusion : `MonteCarlo_median` est la stratégie non-triche la plus performante dans ces confrontations directes.

---

## 5. Cas limite supérieur : `CheatAbsolute`

- vs `Random` : **98.7%**
- vs `FirstStat(poids)` : **97.6%**
- vs `MeanRatio(hist)` : **83.9%**
- vs `MedianRatio(hist)` : **80.17%**

Interprétation : la vision de la carte adverse constitue une borne supérieure très éloignée des bots réalistes.

---

## 6. Synthèse des répétitions (tous match-ups)

- `MedianRatio` vs `MeanRatio` (1200, 10 reps) : **55.28 ± 1.10**.
- `MedianRatio` vs `MonteCarlo_random` (500, 5 reps) : **55.27 ± 1.33**.
- `MedianRatio` vs `MonteCarlo_median` (200, 5 reps) : **45.67 ± 3.44**.
- `MedianRatio` vs `CheatAbsolute` (400, 6 reps) : **19.83 ± 0.60**.
- `MedianRatio` vs `CheatMedianAllCards` (500, 5 reps) : **43.87 ± 1.75**.
- `MeanRatio` vs `CheatMedianAllCards` (500, 5 reps) : **38.14 ± 1.36**.
- `MeanRatio` vs `MonteCarlo_median` (200, 5 reps) : **41.63 ± 1.98**.

Lecture :

- `MonteCarlo_median` et `CheatMedianAllCards` dominent les heuristiques historiques,
- `CheatAbsolute` reste hors catégorie,
- `MedianRatio` garde un avantage stable sur `MeanRatio` dans le protocole long.

---

## 7. Analyse des durées de partie

Sur l’ensemble des statistiques disponibles (`simple` et `repetitions`) :

- bornes observées : environ **36** à **67** manches en moyenne,
- extrême bas : `Random` vs `CheatAbsolute` (**36.305**),
- extrême haut : `MedianRatio` vs `CheatAbsolute` (**66.913**),
- confrontations de bots forts : souvent entre **55** et **64** manches.

Interprétation :

- les match-ups très asymétriques contre baseline faible sont souvent plus courts,
- les confrontations entre bots forts produisent davantage de manches,
- la réinsertion aléatoire maintient une inertie qui peut allonger la partie même avec un bot supérieur.

---

## 8. Conclusions robustes vs points sensibles

## Conclusions robustes

- `Random` et `FirstStat(poids)` sont faibles et quasi équivalentes.
- Les stratégies informées dominent massivement les stratégies simple et aléatoires.
- `CheatAbsolute` domine toutes les autres stratégies.
- `MonteCarlo_median` surclasse `MeanRatio(hist)` et bat aussi `MedianRatio(hist)` sur les répétitions retenues.
- `CheatMedianAllCards` bat `MedianRatio(hist)` et `MeanRatio(hist)`.

## Points sensibles

- La hiérarchie fine des bots forts doit être confirmée par un protocole strictement unique sur tous les match-ups (même seed).

---

## 9. Classement opérationnel (objectif : choix d’un bot de jeu)

Mode de jeu considéré comme triche , n'ets donc pas implémenté dans le jeu pour jouer contre les utilisateurs. *

1. `CheatAbsolute(see both)` *
2. `MonteCarlo_median`
3. `CheatMedianAllCards(median global)` *
4. `MedianRatio(hist)`
5. `MeanRatio(hist)`
6. `MonteCarlo_random`
7. `FirstStat(poids)`
8. `Random`

---

## 10. Point statistique central : pourquoi `MedianRatio(hist)` bat `MeanRatio(hist)`

Le résultat principal entre heuristiques historiques est :

- `MedianRatio(hist)` vs `MeanRatio(hist)` = **55.28%** (10 répétitions),
- dispersion faible (**σ = 1.10**),
- intervalle empirique serré (**53.67 – 57.63**).

Raisons probables :

1. **Robustesse aux extrêmes** : la médiane est moins sensible aux cartes atypiques que la moyenne ;
2. **Décision plus stable** : la règle médiane varie moins d’une manche à l’autre, donc moins d’oscillation stratégique ;
3. **Distribution hétérogène des cartes** : si certaines caractéristiques ont des queues lourdes, la moyenne peut être tirée vers des valeurs peu représentatives ;


En pratique :

- si l’objectif est un bot rapide, lisible et solide sans Monte Carlo, `MedianRatio(hist)` est un meilleur choix que `MeanRatio(hist)` dans ces données.

- en utilisant Monte Carlo, le meilleur bot est `MonteCarlo_median`, il demande une plus grande capacité de calcul mais celle-ci est negligeable et n'influence pas l'experience utilisateur lors des parties.