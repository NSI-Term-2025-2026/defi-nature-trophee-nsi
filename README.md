# 🐾 Défi Nature — Projet NSI (Terminale)

Recréation du jeu de cartes **Défis Nature** en Python, avec :
- un moteur de jeu indépendant,
- une interface Pygame jouable,
- des robots de difficulté variable,
- un mode de simulations statistiques.

---

## 1) Vision du projet

Ce projet a été construit pour combiner **jeu**, **algorithmique** et **démarche expérimentale**.

Concrètement, il permet de :
- jouer une partie complète (Joueur vs Joueur ou Joueur vs Robot),
- apprendre des informations sur les animaux via un onglet dédié,
- comparer des stratégies d'IA sur un grand nombre de parties,
- exporter les résultats pour les analyser.

Le code est pensé pour rester lisible en Terminale NSI :
- séparation claire entre logique et interface,
- nomenclature simple,
- commentaires et fonctions explicites.

---

## 2) Règles du jeu implémentées

Chaque carte contient 3 caractéristiques :
- **poids**,
- **longueur**,
- **longévité**.

Déroulement d'une manche :
1. Le joueur actif choisit une caractéristique.
2. Les deux cartes visibles sont comparées.
3. La valeur strictement la plus grande gagne.
4. En cas d'égalité, le joueur actif perd (règle volontaire).
5. Les cartes sont réinsérées aléatoirement dans la pile du gagnant.

Fin de partie :
- dès qu'un joueur n'a plus de carte.

---

## 3) Fonctionnalités complètes

### Gameplay / interface
- Écran d'accueil avec saisie du prénom.
- Choix du mode :
  - **Joueur vs Joueur**,
  - **Joueur vs Robot**.
- Interface Pygame avec :
  - boutons de caractéristiques,
  - historique des dernières manches,
  - écran de victoire,
  - sons (clic + victoire),
  - menu latéral (rejouer, options, règles, animaux, robots, à propos, quitter).

### Options et accessibilité
- Réglage du volume.
- Choix du robot utilisé en mode Joueur vs Robot.
- Option debug pour afficher/masquer la carte adverse.
- UI adaptée à un usage pédagogique (contrastes, zones lisibles, textes explicites).

### Dimension éducative
- Onglet **Animaux** :
  - image,
  - caractéristiques,
  - descriptif,
  - navigation précédent/suivant.
- Données centralisées dans `data/animaux.csv`.

### IA et stratégies
- Robot aléatoire.
- Robot heuristique basé sur l'historique (médiane / moyenne).
- Robots Monte Carlo (rollouts simulés).
- Stratégies de référence/triche pour comparer les performances en stats.

### Simulations statistiques
- Comparaison systématique de stratégies.
- Winrate, intervalle de confiance (Wilson), nombre moyen de manches.
- Comparaisons symétrisées A/B et B/A pour réduire les biais d'ordre.
- Répétitions et export CSV dans `data/results.csv`.

---

## 4) Architecture du dépôt

```text
defi-nature-trophee-nsi/
├── sources/
│   ├── main.py          # point d'entrée (play/stats)
│   ├── cerveau.py       # moteur, modèles, IA, chargement CSV
│   ├── game_pygame.py   # interface graphique Pygame
│   └── stats.py         # simulations, comparaisons, export CSV
├── data/
│   ├── animaux.csv      # données cartes + descriptif
│   └── results.csv      # sorties du mode stats
├── assets/
│   ├── images/animaux/
│   └── sounds/
├── docs/
│   ├── index.html       # site de présentation
│   └── css/styles.css
├── dossier/
│   └── presentation.md  # dossier de participation
├── strategies.md        # synthèse des stratégies IA
└── requirements.txt
```

---

## 5) Installation et exécution locale

## Prérequis
- Python 3.11+ recommandé
- dépendances du projet

```bash
pip install -r requirements.txt
```

## Lancer le jeu (Pygame)
```bash
python sources/main.py play
```

## Lancer les simulations statistiques
```bash
python sources/main.py stats
```

---

## 6) Fichiers importants à lire en priorité

- `sources/main.py` : démarrage des modes.
- `sources/cerveau.py` : règles du jeu, classes, IA, chargement des données.
- `sources/game_pygame.py` : interactions utilisateur et rendu.
- `sources/stats.py` : cadre expérimental complet.
- `strategies.md` : explication des bots et ordre de grandeur des coûts.

---

## 7) Documentation web et dossier NSI

- Site de présentation : `docs/index.html`
- Dossier de participation : `dossier/presentation.md`

---

## 8) Dépôt GitHub

Remplacer ce lien si besoin selon votre organisation de classe :
- https://github.com/NSI-Term-2025-2026/defi-nature-trophee-nsi



---

## 9) État participation Trophées NSI

- `dossier/presentation.md` : prêt et synchronisé avec l'état du projet.
- architecture du dépôt : cohérente (code, données, assets, docs séparés).
- vidéo de présentation : non incluse pour l'instant.
