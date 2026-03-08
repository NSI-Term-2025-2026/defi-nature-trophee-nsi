# -*- coding: utf-8 -*-
"""
Tests simples (niveau Terminale NSI) pour vérifier le cœur du projet.

Exécution :
    python tests/test_projet.py
"""

import sys
import unittest
from pathlib import Path

# Permet d'importer les modules depuis sources/
RACINE = Path(__file__).resolve().parents[1]
SOURCES = RACINE / "sources"
if str(SOURCES) not in sys.path:
    sys.path.insert(0, str(SOURCES))

import cerveau
import stats


class TestProjetDefiNature(unittest.TestCase):
    def test_liste_animaux_non_vide(self):
        self.assertTrue(len(cerveau.LISTE_ANIMAUX) >= 10)

    def test_animal_a_descriptif(self):
        a = cerveau.LISTE_ANIMAUX[0]
        self.assertTrue(hasattr(a, "descriptif"))
        self.assertIsInstance(a.descriptif, str)

    def test_distribution_cartes_conserve_total(self):
        c1, c2 = cerveau.distribuer_cartes(cerveau.LISTE_ANIMAUX)
        self.assertEqual(len(c1) + len(c2), len(cerveau.LISTE_ANIMAUX))

    def test_creation_partie_pvp(self):
        game = cerveau.creer_partie("PVP")
        self.assertIsNotNone(game)
        self.assertEqual(len(game.joueurs), 2)
        self.assertIsNone(game.mode_robot)

    def test_creation_partie_robot(self):
        game = cerveau.creer_partie("RA", prenom="Test")
        self.assertEqual(game.joueurs[0].nom, "Test")
        self.assertEqual(game.joueurs[1].nom, "Robot")
        self.assertEqual(game.mode_robot, "A")

    def test_partie_avance_apres_une_manche(self):
        game = cerveau.creer_partie("PVP")
        hist_avant = len(game.historique_cartes)
        game.appliquer_manche("poids")
        hist_apres = len(game.historique_cartes)
        self.assertGreaterEqual(hist_apres, hist_avant)

    def test_clone_monte_carlo_copie_historique(self):
        game = cerveau.creer_partie("PVP")
        game.appliquer_manche("poids")
        clone = cerveau.copie_partie_simple(game)
        self.assertEqual(len(clone.historique_cartes), len(game.historique_cartes))
        self.assertEqual(len(clone.historique_manches), len(game.historique_manches))

    def test_stats_retourne_resultat(self):
        strat_a = stats.STRATEGIE_PAR_NOM["Random"]
        strat_b = stats.STRATEGIE_PAR_NOM["FirstStat(poids)"]
        res = stats.comparer_deux_strategies(
            strat_a,
            strat_b,
            n_games=3,
            seed=123,
            export_csv=False,
            symetriser=True,
            max_manches=200,
        )
        self.assertIn("winrate_A_pct", res)
        self.assertIn("n_timeouts", res)


if __name__ == "__main__":
    unittest.main(verbosity=2)
