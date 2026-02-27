# 🐾 Défi Nature — Projet NSI (Terminale)
## Recréation du jeu de société avec IA et analyse expérimentale

---

## 📌 Présentation

Ce dépôt contient une **recréation numérique du jeu de société _Défi Nature_**, développée en **Python**, avec une interface graphique réalisée en **Pygame**.

Le projet ne se limite pas à une simple adaptation visuelle :  
il intègre :

- 🎮 Une interface interactive complète  
- 🧠 Plusieurs stratégies de robots (IA)  
- 📊 Un module de simulations statistiques  
- 🧱 Une architecture modulaire (moteur indépendant de l’interface)  

L’objectif est de reproduire fidèlement le jeu tout en explorant la **prise de décision algorithmique**.

---

## 🎴 Règles du jeu

Chaque carte représente un animal avec trois caractéristiques :

- **Poids**
- **Longueur**
- **Longévité**

### Déroulement d’une manche

1. Les cartes sont mélangées et distribuées équitablement.  
2. Le joueur actif révèle sa carte visible (dernière carte du tas).  
3. Il choisit une caractéristique.  
4. Les valeurs sont comparées.  
5. La valeur **strictement supérieure** gagne la manche.  
6. En cas d’égalité, le joueur actif perd.  
7. Le gagnant récupère la carte adverse.  
8. Les cartes sont réinsérées aléatoirement dans le tas.  
9. La partie se termine lorsqu’un joueur n’a plus de cartes.  

⚠️ La règle d’égalité rend le choix stratégique plus risqué.

---

## 🚀 Fonctionnalités principales

### 🎮 Gameplay

- Modes disponibles :
  - Joueur vs Joueur  
  - Joueur vs Robot  
- Interface complète :
  - Affichage des cartes  
  - Animation de fin de manche  
  - Historique des manches  
  - Menu hamburger (Rejouer / Options / Règles / À propos / Quitter)  
- Sons (clics, victoire)  
- Options (volume, affichage debug)

---

## 🧠 Intelligence Artificielle

Plusieurs niveaux d’intelligence sont implémentés afin de comparer différentes approches algorithmiques.

### 🔹 Stratégies naïves

- Choix aléatoire  
- Toujours la même caractéristique  

### 🔹 Stratégies heuristiques

- Comparaison à la moyenne  
- Comparaison à la médiane  
- Analyse de l’historique des cartes jouées  

### 🔹 Approches probabilistes

- Estimation des chances de victoire  
- Simulation de fins de partie  
- Méthodes de type Monte Carlo  

🎯 L’intérêt principal du projet réside dans la **comparaison expérimentale entre ces stratégies**.

---

## 📊 Module statistique

Le fichier `stats.py` permet :

- De comparer automatiquement deux stratégies  
- De lancer des centaines / milliers de parties  
- D’obtenir :
  - Winrate (% de victoire)  
  - Nombre moyen de manches  
  - Comparaison vitesse / efficacité  
- D’utiliser des **seeds fixes** pour garantir la reproductibilité  
- D’enregistrer les résultats dans `data/results.txt`  

Cette séparation permet de faire des simulations **sans dépendre de Pygame**.

---

## 🧩 Architecture du projet

Le projet est organisé selon une séparation claire des responsabilités :

- `cerveau.py` → moteur du jeu (règles, classes, IA)  
- `game_pygame.py` → interface graphique uniquement  
- `stats.py` → simulations statistiques  
- `main.py` → point d’entrée  
- `data/animaux.csv` → base de données des cartes  

Cette organisation permet :

- Des tests indépendants de l’interface  
- Une maintenance plus simple  
- Une meilleure lisibilité du code  

---

## 📂 Structure du projet

```text
defi_nature_trophee_nsi/
│
├── main.py
├── cerveau.py
├── game_pygame.py
├── stats.py
├── requirements.txt
│
├── data/
│   ├── animaux.csv
│   └── results.txt
│
├── assets/
│   ├── images/animaux/
│   └── sounds/
│
└── strategies/
    └── strategies.txt
```

## 🎮 Jouer au jeu

Si tu veux jouer à **Défi Nature** sans installer Python ni cloner le dépôt :

1. Va sur la page des **Releases** du projet (onglet *Releases* en haut du dépôt GitHub).  
2. Télécharge le fichier **exécutable Windows (`.exe`)** correspondant à la dernière version publiée.  
   - Par exemple : `DefiNature-v1.0.0.exe`
3. Place ce fichier `.exe` dans un dossier avec les dossiers `assets/` et `data/` si ceux-ci sont fournis séparément dans l’archive de la release.
4. Double-clique sur l’exécutable pour lancer le jeu directement sur ton ordinateur — il n’est **pas nécessaire d’installer Python** ni de taper des commandes dans un terminal.

👉 Tu peux aussi ajouter un lien direct vers la dernière release dans le README, par exemple :

```markdown
https://github.com/NSI-Term-2025-2026/defi-nature-trophee-nsi/releases/latest
