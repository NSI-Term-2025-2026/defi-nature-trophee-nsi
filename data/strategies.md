
# Stratégies des bots (jeu + mode statistiques)

Objectif : expliquer simplement les stratégies utilisées dans `sources/cerveau.py` et `sources/stats.py`, avec un ordre de grandeur de leur coût de calcul.

## Notation de complexité (ordre de grandeur)

On utilise les notations suivantes :

- `H` = nombre de cartes dans l'historique déjà observé
- `E` = nombre d'essais Monte Carlo (`essais`)
- `T` = nombre de manches simulées dans un rollout Monte Carlo
- Le nombre de caractéristiques est fixe (3 : poids, longueur, longévité), donc traité comme une constante.

Quand on écrit `O(H)` ou `O(E*T)`, c'est un ordre de grandeur pour comparer les stratégies entre elles.

---

## 1) Stratégies naïves

### 1.1 `Random`

**Principe**
- Le bot choisit au hasard une caractéristique parmi `poids`, `longueur`, `longevite`.

**Informations utilisées**
- Aucune information de contexte.

**Complexité (par décision)**
- **Temps : `O(1)`**
- **Mémoire : `O(1)`**

**Usage**
- Baseline minimale pour savoir si une autre stratégie est réellement meilleure que le hasard.

---

### 1.2 `FirstStat(poids)`

**Principe**
- Le bot joue toujours la même caractéristique (actuellement `poids`).

**Informations utilisées**
- Aucune.

**Complexité (par décision)**
- **Temps : `O(1)`**
- **Mémoire : `O(1)`**

**Usage**
- Baseline déterministe, utile pour détecter si une caractéristique est structurellement avantagée.

---

## 2) Stratégies adaptatives basées sur l'historique

### 2.1 `MedianRatio(hist)`

**Principe**
- Le bot regarde sa carte courante.
- Il calcule la médiane de chaque caractéristique sur les cartes déjà jouées (historique).
- Il choisit la caractéristique qui maximise le ratio :
  - `valeur_carte / mediane_historique`

**Informations utilisées**
- Historique des cartes vues dans la partie.

**Complexité (par décision)**
- **Temps : `O(H)`** (construction des listes + calcul des médianes)
- **Mémoire : `O(H)`** (listes temporaires)

**Points forts**
- S'adapte progressivement à la partie.
- Plus robuste aux valeurs extrêmes que la moyenne.

**Limites**
- Dépend de la qualité de l'historique (faible au début de partie).

---

### 2.2 `MeanRatio(hist)`

**Principe**
- Même idée que la médiane, mais avec la moyenne.
- Choix via le meilleur ratio :
  - `valeur_carte / moyenne_historique`

**Informations utilisées**
- Historique local des cartes jouées.

**Complexité (par décision)**
- **Temps : `O(H)`**
- **Mémoire : `O(H)`**

**Points forts**
- Simple et souvent efficace.

**Limites**
- Plus sensible aux valeurs extrêmes que `MedianRatio(hist)`.

---

## 3) Stratégies "triche" (borne haute théorique)

### 3.1 `CheatAbsolute(see both)`

**Principe**
- Le bot connaît sa carte **et** la carte adverse courante.
- Il choisit immédiatement une caractéristique gagnante si possible.

**Informations utilisées**
- Information parfaite sur le duel courant.

**Complexité (par décision)**
- **Temps : `O(1)`**
- **Mémoire : `O(1)`**

**Usage**
- Sert de référence de performance maximale (non réaliste en jeu normal).

---

### 3.2 `CheatMedianAllCards(median global)`

**Principe**
- Le bot connaît toute la distribution globale (`LISTE_ANIMAUX`).
- Il calcule des médianes sur l'ensemble des cartes du jeu puis choisit le meilleur ratio.

**Informations utilisées**
- Données globales complètes du deck.

**Complexité (par décision)**
- **Temps : `O(N)`**, avec `N` = nombre total de cartes (petit et fixe ici)
- **Mémoire : `O(N)`**

**Usage**
- Borne intermédiaire entre une IA réaliste et la triche absolue.

---

## 4) Stratégies Monte Carlo (simulation)

### 4.1 `MonteCarlo_random`

**Principe**
- Pour chaque caractéristique candidate, on :
  1. clone l'état courant,
  2. joue cette caractéristique,
  3. simule la suite de la partie avec des choix aléatoires,
  4. compte les victoires.
- On garde la caractéristique avec le plus de victoires simulées.

**Informations utilisées**
- État courant complet de la partie.

**Complexité (par décision)**
- **Temps : `O(E * T)`** (à constante près des 3 caractéristiques)
- **Mémoire : `O(T)`** par simulation (ordre de grandeur)

**Points forts**
- Méthode probabiliste solide.
- Peut dépasser des heuristiques simples.

**Limites**
- Coûteuse en temps de calcul.
- Sensible au nombre d'essais `E`.

---

### 4.2 `MonteCarlo_median`

**Principe**
- Même base que `MonteCarlo_random`.
- Pendant les rollouts, les décisions simulées utilisent la stratégie médiane au lieu du pur hasard.

**Informations utilisées**
- État courant + historique dans les simulations.

**Complexité (par décision)**
- **Temps : `O(E * T * C_hist)`** avec un coût historique `C_hist` proche de `O(H)` dans les calculs médiane.
- En pratique : plus lent que `MonteCarlo_random`.

**Points forts**
- Simulations plus "intelligentes" que le hasard pur.

**Limites**
- Très coûteuse si on augmente `E`.

---

## Hiérarchie globale (du plus simple au plus coûteux)

1. `Random` / `FirstStat(poids)`
2. `CheatAbsolute(see both)` (simple mais irréaliste)
3. `MedianRatio(hist)` / `MeanRatio(hist)`
4. `CheatMedianAllCards(median global)`
5. `MonteCarlo_random`
6. `MonteCarlo_median`

