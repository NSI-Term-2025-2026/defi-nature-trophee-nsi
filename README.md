# 🐾 Défi Nature — Projet NSI

Défi Nature est une recréation en Python d’un jeu de cartes inspiré de « Défis Nature », réalisée dans le cadre de la spécialité NSI en Terminale.
Le projet propose un moteur de jeu séparé de l’interface, un mode graphique avec Pygame, plusieurs robots avec des stratégies différentes, ainsi qu’un module de simulations statistiques pour comparer les IA.

## Pour commencer

Ce projet permet de :
- jouer à deux joueurs ;
- jouer contre un robot ;
- découvrir des animaux et leurs caractéristiques ;
- comparer plusieurs stratégies grâce à des simulations automatiques.

L’objectif est de montrer des compétences en programmation, en algorithmique, en structuration d’un projet et en expérimentation.

### Pré-requis

Ce qu’il est requis pour commencer avec ce projet :
- Python 3.11 ou supérieur
- pip
- pygame
- numpy

### Installation
#### Option 1
Les étapes pour jouer au jeu :
1. Installer la dernière release du projet:  `https://github.com/NSI-Term-2025-2026/defi-nature-trophee-nsi/releases`

2. Lancer le `.exe`

#### Option 2
Les étapes pour installer le programme :

1. Cloner le dépôt :
git clone `https://github.com/NSI-Term-2025-2026/defi-nature-trophee-nsi.git`

2. Se placer dans le dossier du projet :
`cd defi-nature-trophee-nsi`

3. Installer les dépendances :
`pip install -r requirements.txt`



## Démarrage

### Lancer le jeu en mode graphique
`python sources/main.py play`

### Lancer le module de simulations statistiques
`python sources/main.py stats`

### Lancer les tests
`python tests/test_projet.py`

## Fabriqué avec

- Python
- Pygame
- NumPy
- CSV pour les données
- Google Drive et GitHub pour l’organisation du projet
- Spyder / Visual Studio Code

## Versions

- Premier Jeu uniquement en console
- Ajout de l'interface pyagme
- Ajout du module stats pour comparer des robots entre eux
- Mise en commun des trois
- Plein de petites nouvelles versions avec des ajouts au fur et a mesure. (sons , menu deroulant Pygame ...)
- Notre projet à présent
  
## Auteurs

- Antonin
- Alexi
- Léo

## License

Ce projet est sous licence MIT - voir le fichier `LICENSE.txt` pour plus d’informations.
