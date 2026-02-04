# -*- coding: utf-8 -*-
from random import randint, choice, shuffle
import numpy

# ---------- Classe Animaux ----------
class Animaux:
    def __init__(self, Nom: str, Poids: float, Longueur: float, Longevite: float):
        self.nom = Nom
        self.poids = Poids
        self.longueur = Longueur
        self.longevite = Longevite
        
    def __repr__(self):
        return f"{self.nom} pèse {self.poids} kg, sa longueur est de {self.longueur} m, sa longevité est de {self.longevite} ans."


# ---------- Classe Joueur ----------
class Joueur:
    def __init__(self, Nom_joueur: str, Points: int, Cartes_en_main: list = None, is_robot: bool = False):
        self.nom = Nom_joueur
        self.pts = Points
        self.carte_en_main = Cartes_en_main if Cartes_en_main is not None else []
        self.is_robot = is_robot
        
    def __repr__(self):
        return f"Le joueur {self.nom} possède {self.pts} points et a cette liste de carte en main : {self.carte_en_main}"
        
    def __eq__(self, autreJoueur):
        return self.nom == autreJoueur.nom

    # ---------- Gestion des cartes ----------
    # NOTE: cette méthode conserve son comportement (utilisable), mais **ne sera pas**
    # utilisée pour la distribution principale dans la version actuelle.
    def ajouter_n_carte_en_main(self, n: int):
        """Ajoute n cartes de la pioche au joueur courant (ancienne version qui poppe la pioche)."""
        for _ in range(n):
            if liste_animaux:
                self.carte_en_main.append(distribution_de_cartes())
            else:
                print("Plus de cartes à distribuer.")
                break

    def Renvoyer_premiere_carte_du_tas(self):
        # On considère que la "première" carte (celle qu'on montre / joue) est le dernier élément
        return self.carte_en_main[-1]
    
    def Enlever_la_carte_perdue(self):
        # enlève la carte perdue (dernier élément)
        return self.carte_en_main.pop()
    
    def Remettre_carte_jouee(self, carte_joue):
        # on retire la carte jouée (dernier élément) puis on la réinsère aléatoirement dans la main
        if self.carte_en_main:
            self.carte_en_main.pop()
        idx = randint(0, len(self.carte_en_main))
        self.carte_en_main.insert(idx, carte_joue)
        
    def jeu_carte_est_vide(self):
        return len(self.carte_en_main) == 0

    def Ajouter_la_carte_gagnee(self, carte_gagnee):
        # insère la carte gagnée aléatoirement (même si le joueur n'a pas de cartes)
        idx = randint(0, len(self.carte_en_main))
        self.carte_en_main.insert(idx, carte_gagnee)

    # ---------- Caractéristiques de la carte ----------
    def Renvoyer_caracteristiques_premiere_carte_du_tas(self):
        """
        Renvoie un tuple (poids, longueur, longevite) de la carte visible (dernier élément).
        Toujours 3 valeurs numériques.
        """
        c = self.carte_en_main[-1]
        return (c.poids, c.longueur, c.longevite)
    
    def Renvoyer_poids_premiere_carte_du_tas(self):
        return self.carte_en_main[-1].poids
        
    def Renvoyer_longueur_premiere_carte_du_tas(self):
        return self.carte_en_main[-1].longueur
    
    def Renvoyer_longevite_premiere_carte_du_tas(self):
        return self.carte_en_main[-1].longevite
    
    def Renvoyer_nombre_de_carte_du_joueur(self):
        return len(self.carte_en_main)


# ============================================================
#                   FONCTIONS UTILITAIRES
# ============================================================

def distribution_de_cartes():
    """
    Ancienne fonction : renvoie une carte au hasard **sans** la supprimer de la liste.
    (Ne modifie pas liste_animaux)
    """
    if not liste_animaux:
        raise ValueError("La pioche est vide.")
    return choice(liste_animaux)


def medianne_caracteristiques(liste):
    """
    Renvoie un tuple (med_poids, med_longueur, med_longevite).
    Si la liste est vide, renvoie (1,1,1) pour éviter NaN / division par zéro.
    """
    if not liste:
        return (1.0, 1.0, 1.0)
    poids = sorted([float(a.poids) for a in liste])
    longueur = sorted([float(a.longueur) for a in liste])
    longevite = sorted([float(a.longevite) for a in liste])

    # numpy.median gère bien listes de n'importe quelle longueur
    med_p = float(numpy.median(poids))
    med_l = float(numpy.median(longueur))
    med_lo = float(numpy.median(longevite))

    return (med_p, med_l, med_lo)


def meilleur_quotient_caracteristiques(medianne_car, caracteristiques_carte):
    """Retourne le plus grand quotient (valeur/mediane) et la caractéristique correspondante."""
    # debug prints utiles
    # print("DEBUG mediane:", medianne_car)
    # print("DEBUG caractéristiques:", caracteristiques_carte)

    assert len(medianne_car) == len(caracteristiques_carte) == 3
    quotients = [
        caracteristiques_carte[0] / medianne_car[0] if medianne_car[0] != 0 else float('inf'),
        caracteristiques_carte[1] / medianne_car[1] if medianne_car[1] != 0 else float('inf'),
        caracteristiques_carte[2] / medianne_car[2] if medianne_car[2] != 0 else float('inf'),
    ]
    max_quotient = max(quotients)
    index = quotients.index(max_quotient)
    
    if index == 0:
        return max_quotient, "POIDS"
    elif index == 1:
        return max_quotient, "LONGUEUR"
    else:
        return max_quotient, "LONGEVITE"


def distribuer_cartes_sans_modifier_liste(joueur1, joueur2, liste_animaux):
    """
    Distribue les cartes aux deux joueurs sans modifier liste_animaux.
    On fait une copie mélangée et on répartit moitié / moitié.
    """
    if not liste_animaux:
        joueur1.carte_en_main = []
        joueur2.carte_en_main = []
        return

    copie = liste_animaux.copy()
    shuffle(copie)

    total = len(copie)
    moitie = total // 2

    # copie des sous-listes pour que les joueurs aient des listes indépendantes
    joueur1.carte_en_main = copie[:moitie].copy()
    joueur2.carte_en_main = copie[moitie:].copy()


# ============================================================
#                   LISTE DES ANIMAUX
# ============================================================

Elephant_Afrique = Animaux("Éléphant d'Afrique", 5000, 6.0, 65)
Lion = Animaux("Lion", 189, 2.1, 18)
Aigle_royal = Animaux("Aigle royal", 4.8, 0.84, 25)
Panda_geant = Animaux("Panda géant", 97, 1.70, 22)
Loup_rouge = Animaux("Loup rouge", 25, 1.10, 13)
Tigre_de_sibérie = Animaux("Tigre de Sibérie", 300, 2.30, 17)
Panda_rouge = Animaux("Panda rouge", 5, 0.57, 12)
Corail_rouge = Animaux("Corail rouge", 2, 0.40, 60)
Merou_golfe = Animaux("Mérou golfe", 90, 1.98, 48)
Requin_marteau_halicorne = Animaux("Requin-marteau halicorne", 152, 3.30, 55)
Tortue_verte = Animaux("Tortue verte", 175, 1, 70)
Raie_manta = Animaux("Raie manta", 1500, 5.50, 19)
Dragon_de_komodo = Animaux("Dragon de komodo", 165, 3.10, 53)
Tapir = Animaux("Tapir", 200, 2.12, 30)
Cobra_royal = Animaux("Cobra royal", 10, 4, 22)
Protee_anguillard = Animaux("Protée anguillard", 0.02, 0.25, 69)

liste_animaux = [
    Elephant_Afrique, Lion, Aigle_royal, Panda_geant, Loup_rouge, Tigre_de_sibérie,
    Panda_rouge, Corail_rouge, Merou_golfe, Requin_marteau_halicorne, Tortue_verte,
    Raie_manta, Dragon_de_komodo, Tapir, Cobra_royal, Protee_anguillard
]

cartes_jouees = []


# ============================================================
#                   FONCTIONS DE JEU
# ============================================================

def tour(joueur_joue, joueur_subit):
    print("\nC'est au tour de:", joueur_joue.nom)
    
    carte_joueur = joueur_joue.Renvoyer_premiere_carte_du_tas()
    carte_adverse = joueur_subit.Renvoyer_premiere_carte_du_tas()

    cartes_jouees.extend([carte_joueur, carte_adverse])  
    # meilleur affichage : nom + caractéristiques
    c = joueur_joue.carte_en_main[-1]
    print(f"Carte visible : {c.nom} -> (POIDS: {c.poids} kg, LONGUEUR: {c.longueur} m, LONGEVITE: {c.longevite} ans)")

    car_bien_ecris = False
    while not car_bien_ecris:
        car_choisie = input("Quelle caractéristique choisissez-vous ? (POIDS, LONGUEUR, LONGEVITE): ").upper()
        if car_choisie in ["POIDS", "LONGUEUR", "LONGEVITE"]:
            car_bien_ecris = True

    if car_choisie == "POIDS":
        car_adverse = joueur_subit.Renvoyer_poids_premiere_carte_du_tas()
        car_choisie_val = joueur_joue.Renvoyer_poids_premiere_carte_du_tas()
    elif car_choisie == "LONGEVITE":
        car_adverse = joueur_subit.Renvoyer_longevite_premiere_carte_du_tas()
        car_choisie_val = joueur_joue.Renvoyer_longevite_premiere_carte_du_tas()
    else:  # LONGUEUR
        car_adverse = joueur_subit.Renvoyer_longueur_premiere_carte_du_tas()
        car_choisie_val = joueur_joue.Renvoyer_longueur_premiere_carte_du_tas()

    joueur_qui_joue_est_gagnant = car_choisie_val > car_adverse

    if joueur_qui_joue_est_gagnant:
        carte_perdue = joueur_subit.Enlever_la_carte_perdue()
        joueur_joue.Remettre_carte_jouee(joueur_joue.Renvoyer_premiere_carte_du_tas())
        joueur_joue.Ajouter_la_carte_gagnee(carte_perdue)
        print(joueur_joue.nom, "a gagné cette manche !")
        joueur_qui_a_gagne = joueur_joue
    else:
        carte_perdue = joueur_joue.Enlever_la_carte_perdue()
        joueur_subit.Ajouter_la_carte_gagnee(carte_perdue)
        print(joueur_subit.nom, "a gagné cette manche !")
        joueur_qui_a_gagne = joueur_subit
    return joueur_qui_a_gagne


def tour_robot_con(robot_joue, joueur_subit):
    print("\nC'est au tour du robot (mode aléatoire).")
    liste_car = ["POIDS", "LONGUEUR", "LONGEVITE"]
    car_choisie_nom = choice(liste_car)
    
    if car_choisie_nom == "POIDS":
        car_adverse = joueur_subit.Renvoyer_poids_premiere_carte_du_tas()
        car_choisie_val = robot_joue.Renvoyer_poids_premiere_carte_du_tas()
    elif car_choisie_nom == "LONGEVITE":
        car_adverse = joueur_subit.Renvoyer_longevite_premiere_carte_du_tas()
        car_choisie_val = robot_joue.Renvoyer_longevite_premiere_carte_du_tas()
    else:
        car_adverse = joueur_subit.Renvoyer_longueur_premiere_carte_du_tas()
        car_choisie_val = robot_joue.Renvoyer_longueur_premiere_carte_du_tas()

    joueur_qui_joue_est_gagnant = car_choisie_val > car_adverse

    if joueur_qui_joue_est_gagnant:
        carte_perdue = joueur_subit.Enlever_la_carte_perdue()
        robot_joue.Remettre_carte_jouee(robot_joue.Renvoyer_premiere_carte_du_tas())
        robot_joue.Ajouter_la_carte_gagnee(carte_perdue)
        print("Le robot a gagné cette manche !")
        joueur_qui_a_gagne = robot_joue
    else:
        carte_perdue = robot_joue.Enlever_la_carte_perdue()
        joueur_subit.Ajouter_la_carte_gagnee(carte_perdue)
        print("Le robot n'a pas réussi à gagner cette manche.")
        joueur_qui_a_gagne = joueur_subit
    return joueur_qui_a_gagne


def tour_robot(robot_joue, joueur_subit):
    print("\nC'est au tour du robot (mode intelligent).")

    carte_robot = robot_joue.Renvoyer_premiere_carte_du_tas()
    carte_adverse = joueur_subit.Renvoyer_premiere_carte_du_tas()

    cartes_jouees.extend([carte_robot, carte_adverse])  

    mediane = medianne_caracteristiques(cartes_jouees) 

    quot, nom_car = meilleur_quotient_caracteristiques(
        mediane,
        robot_joue.Renvoyer_caracteristiques_premiere_carte_du_tas()
    )

    print(f"Le robot choisit {nom_car} (quotient {quot:.2f})")

    if nom_car == "POIDS":
        val_r = carte_robot.poids
        val_a = carte_adverse.poids
    elif nom_car == "LONGEVITE":
        val_r = carte_robot.longevite
        val_a = carte_adverse.longevite
    else:
        val_r = carte_robot.longueur
        val_a = carte_adverse.longueur

    if val_r > val_a:
        joueur_subit.Enlever_la_carte_perdue()
        robot_joue.Remettre_carte_jouee(carte_robot)
        robot_joue.Ajouter_la_carte_gagnee(carte_adverse)
        print("Le robot a gagné cette manche !")
        return robot_joue
    else:
        robot_joue.Enlever_la_carte_perdue()
        joueur_subit.Ajouter_la_carte_gagnee(carte_robot)
        print("Vous avez gagné cette manche !")
        return joueur_subit

# ============================================================
#                   LANCEMENT DU JEU
# ============================================================

if __name__ == "__main__":
    print('Quel mode de jeu voulez-vous utiliser ? ')
    mode_de_jeu = int(input('Tapez 1 pour le 1 vs 1 et tapez 2 pour affronter notre robot: '))
    assert mode_de_jeu in (1, 2)

    # Création des joueurs
    if mode_de_jeu == 1:
        nom_joueur_1 = input("Entrez le nom du premier joueur: ")
        nom_joueur_2 = input("Entrez le nom du deuxième joueur: ")
        Joueur1 = Joueur(nom_joueur_1, 0, [])
        Joueur2 = Joueur(nom_joueur_2, 0, [])
    else:
        nom_joueur_1 = input("Entrez le nom du joueur: ")
        Joueur1 = Joueur(nom_joueur_1, 0, [])
        Joueur2 = Joueur("ROBOT", 0, [], True)

    # Distribution équilibrée des cartes : on utilise la fonction qui ne modifie pas liste_animaux
    distribuer_cartes_sans_modifier_liste(Joueur1, Joueur2, liste_animaux)

    tour_joueur1 = True

    while not Joueur1.jeu_carte_est_vide() and not Joueur2.jeu_carte_est_vide():
        if tour_joueur1:
            # tour du joueur humain (même si l'adversaire est un robot)
            tour(Joueur1, Joueur2)
            tour_joueur1 = False
        else:
            # tour du second joueur (robot ou humain)
            if Joueur2.is_robot:
                # choix du mode robot : aléatoire ou intelligent
                mode_robot = input("Mode robot ? Tapez A pour aléatoire, I pour intelligent (par défaut I): ").upper()
                if mode_robot == "A":
                    tour_robot_con(Joueur2, Joueur1)
                else:
                    tour_robot(Joueur2, Joueur1)
            else:
                tour(Joueur2, Joueur1)
            tour_joueur1 = True
    
        # Affichage du nombre de cartes restantes
        print(Joueur1.nom, "possède", Joueur1.Renvoyer_nombre_de_carte_du_joueur(), "cartes.")
        print(Joueur2.nom, "possède", Joueur2.Renvoyer_nombre_de_carte_du_joueur(), "cartes.")
    # Fin de partie
    if Joueur1.Renvoyer_nombre_de_carte_du_joueur() > Joueur2.Renvoyer_nombre_de_carte_du_joueur():
        print(f"{Joueur1.nom} a gagné la partie !")
    elif Joueur1.Renvoyer_nombre_de_carte_du_joueur() < Joueur2.Renvoyer_nombre_de_carte_du_joueur():
        print(f"{Joueur2.nom} a gagné la partie !")
    else:
        print("Égalité !")