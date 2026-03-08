# -*- coding: utf-8 -*-
"""
Stats / simulations (sans pygame).

Objectif :
- Comparer des stratégies entre elles sur N parties.
- Afficher :
  1) le winrate
  2) la vitesse (nombre moyen de manches)
  3) une incertitude (IC 95% sur le winrate)
- IMPORTANT : certaines stratégies sont très longues (Monte Carlo, etc.).
  On adapte automatiquement :
  - Petites stratégies : peu de parties, 1 seule expérience (rapide)
  - Grosses stratégies : plus de parties + répétitions (stat "sérieuse")

Aucune dépendance pygame.
"""

import random
import csv
from pathlib import Path
from typing import Callable, Dict, List, Tuple

from cerveau import (
    Joueur, GameState, LISTE_ANIMAUX, distribuer_cartes,
    choix_robot_aleatoire,
    choix_robot_aleatoire_premiere_caracteristique,
    choix_robot_intelligent,
    choix_robot_intelligent_moyenne,
    choix_robot_triche_absolue,
    choix_robot_intelligent_triche,
    choix_robot_monte_carlo_random,
    choix_robot_monte_carlo_median,
)


# ============================================================
# ======================= STRATEGIES ==========================
# ============================================================

class Strategie:
    """
    Structure simple:

    - nom : nom lisible
    - choisir(etat) : fonction qui renvoie "poids" / "longueur" / "longevite"
    """

    def __init__(self, nom: str, choisir: Callable[[GameState], str]):
        self.nom = nom
        self.choisir = choisir


def _safe_carac(carac: str) -> str:
    """Sécurise la caractéristique (évite crash si stratégie bug)."""
    if isinstance(carac, str):
        c = carac.lower()
        if c in ("poids", "longueur", "longevite"):
            return c
    return "poids"


def _carte_actif(etat: GameState):
    """Raccourci : carte visible du joueur actif."""
    return etat.joueur_actif.carte_visible()


# -----------------------
# Stratégies "naïves"
# -----------------------

def strat_random(etat: GameState) -> str:
    return _safe_carac(choix_robot_aleatoire())


def strat_first(etat: GameState) -> str:
    return _safe_carac(choix_robot_aleatoire_premiere_caracteristique())


# -----------------------
# Stratégies "intermédiaires"
# -----------------------

def strat_median_hist(etat: GameState) -> str:
    carte = _carte_actif(etat)
    if carte is None:
        return _safe_carac(choix_robot_aleatoire())
    return _safe_carac(choix_robot_intelligent(carte, etat.historique_cartes))


def strat_mean_hist(etat: GameState) -> str:
    carte = _carte_actif(etat)
    if carte is None:
        return _safe_carac(choix_robot_aleatoire())
    return _safe_carac(choix_robot_intelligent_moyenne(carte, etat.historique_cartes))


# -----------------------
# Monte Carlo (coûteux)
# -----------------------

def strat_monte_carlo_random(etat: GameState) -> str:
    return _safe_carac(choix_robot_monte_carlo_random(etat, essais=30))


def strat_monte_carlo_median(etat: GameState) -> str:
    return _safe_carac(choix_robot_monte_carlo_median(etat, essais=30))


# -----------------------
# Triche (fort)
# -----------------------

def strat_cheat_absolute(etat: GameState) -> str:
    carte_jouee = etat.joueur_actif.carte_visible()
    carte_subie = etat.joueur_passif.carte_visible()
    if carte_jouee is None or carte_subie is None:
        return _safe_carac(choix_robot_aleatoire())
    return _safe_carac(choix_robot_triche_absolue(carte_jouee, carte_subie))


def strat_cheat_median_allcards(etat: GameState) -> str:
    carte = _carte_actif(etat)
    if carte is None:
        return _safe_carac(choix_robot_aleatoire())
    return _safe_carac(choix_robot_intelligent_triche(carte, LISTE_ANIMAUX))


# Liste des stratégies disponibles
STRATEGIES: List[Strategie] = [
    Strategie("Random", strat_random),
    Strategie("FirstStat(poids)", strat_first),
    Strategie("MedianRatio(hist)", strat_median_hist),
    Strategie("MeanRatio(hist)", strat_mean_hist),
    Strategie("MonteCarlo_random", strat_monte_carlo_random),
    Strategie("MonteCarlo_median", strat_monte_carlo_median),
    Strategie("CheatAbsolute(see both)", strat_cheat_absolute),
    Strategie("CheatMedianAllCards(median global)", strat_cheat_median_allcards),
]

STRATEGIE_PAR_NOM: Dict[str, Strategie] = {s.nom: s for s in STRATEGIES}


# ============================================================
# ======================= GROUPES ============================
# ============================================================

PETITES_STRATS = {
    "Random",
    "FirstStat(poids)",
    "MeanRatio(hist)",
}

GROSSES_STRATS = {
    "MedianRatio(hist)",
    "MonteCarlo_random",
    "MonteCarlo_median",
    "CheatAbsolute(see both)",
}


def est_grosse_strategie(strat: Strategie) -> bool:
    return strat.nom in GROSSES_STRATS


def est_petite_strategie(strat: Strategie) -> bool:
    return strat.nom in PETITES_STRATS


# ============================================================
# ======================= OUTILS STATS ========================
# ============================================================

def ic95_proportion(nb_succes: int, n: int) -> Tuple[float, float]:
    """
    Intervalle de confiance 95% (méthode de Wilson) pour une proportion p = nb_succes/n.
    """
    if n <= 0:
        return 0.0, 1.0

    z = 1.96  # 95%
    p = nb_succes / n

    denom = 1.0 + (z * z) / n
    centre = (p + (z * z) / (2.0 * n)) / denom
    demi_largeur = (z / denom) * ((p * (1.0 - p) / n) + (z * z) / (4.0 * n * n)) ** 0.5

    bas = max(0.0, centre - demi_largeur)
    haut = min(1.0, centre + demi_largeur)
    return bas, haut


def moyenne(liste: List[float]) -> float:
    return (sum(liste) / len(liste)) if liste else float("nan")


def mediane(liste: List[float]) -> float:
    if not liste:
        return float("nan")
    triee = sorted(liste)
    n = len(triee)
    milieu = n // 2
    if n % 2 == 1:
        return triee[milieu]
    return (triee[milieu - 1] + triee[milieu]) / 2.0


def ecart_type(liste: List[float]) -> float:
    """
    Ecart-type empirique:
    - si n < 2, on renvoie 0.0 car il n'y a pas de dispersion mesurable ;
    - sinon on divise par (n - 1).
    """
    if not liste:
        return float("nan")
    if len(liste) == 1:
        return 0.0
    m = moyenne(liste)
    var = sum((x - m) ** 2 for x in liste) / (len(liste) - 1)
    return var ** 0.5


# ============================================================
# ======================= EXPORT CSV ==========================
# ============================================================

def _trouver_racine_projet() -> Path:
    try:
        depart = Path(__file__).resolve().parent
    except Exception:
        depart = Path.cwd()

    for dossier in [depart] + list(depart.parents):
        if (dossier / "data").exists() and (dossier / "assets").exists():
            return dossier

    return depart


def chemin_results_csv() -> Path:
    return _trouver_racine_projet() / "data" / "results.csv"


def ecrire_ligne_csv(res: Dict[str, object]) -> None:
    path = chemin_results_csv()
    path.parent.mkdir(parents=True, exist_ok=True)

    colonnes = [
        "mode",
        "A", "B",
        "n_games",
        "seed",

        "wins_A", "wins_B",
        "n_valid_games",
        "n_total_runs",
        "n_timeouts",

        "winrate_A_pct", "winrate_B_pct",
        "winrate_A_ci95_low_pct", "winrate_A_ci95_high_pct",

        "avg_rounds_overall",
        "avg_rounds_all_runs",
        "avg_rounds_when_A_wins",
        "avg_rounds_when_B_wins",

        "n_repetitions",
        "winrate_A_mean_pct",
        "winrate_A_std_pct",
        "winrate_A_median_pct",
        "winrate_A_min_pct",
        "winrate_A_max_pct",

        "winrate_A_global_pct",
        "winrate_A_global_ci95_low_pct",
        "winrate_A_global_ci95_high_pct",

        "avg_rounds_overall_mean",
        "avg_rounds_overall_std",
        "avg_rounds_all_runs_mean",
        "avg_rounds_all_runs_std",

        "total_wins_A",
        "total_wins_B",
        "total_valid_games",
        "total_timeouts",
    ]

    fichier_existe = path.exists()
    with path.open("a", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=colonnes, delimiter=";")
        if not fichier_existe:
            writer.writeheader()

        ligne = {c: res.get(c, "") for c in colonnes}
        writer.writerow(ligne)


# ============================================================
# ======================= GESTION DU HASARD ==================
# ============================================================

def _executer_avec_seed_globale(seed: int, fonction):
    """
    Le module cerveau.py utilise le hasard via le module random (global).
    Pour obtenir des résultats reproductibles et indépendants de l'ordre,
    on force random.seed(seed) uniquement pendant la partie,
    puis on restaure l'état précédent du hasard.
    """
    etat_hasard = random.getstate()
    try:
        random.seed(seed)
        return fonction()
    finally:
        random.setstate(etat_hasard)


# ============================================================
# ======================= SIMULATION CORE ======================
# ============================================================

def creer_partie_bot_vs_bot() -> GameState:
    """
    Crée une partie BotA vs BotB.
    Le joueur qui commence est tiré au hasard.
    """
    c1, c2 = distribuer_cartes(LISTE_ANIMAUX)
    j1 = Joueur("BotA", c1)
    j2 = Joueur("BotB", c2)
    etat = GameState(j1, j2, mode_robot=None)

    if random.random() < 0.5:
        etat.joueur_actif, etat.joueur_passif = etat.joueur_passif, etat.joueur_actif

    return etat


def jouer_une_partie(
    strat_a: Strategie,
    strat_b: Strategie,
    seed: int,
    max_manches: int = 5000,
) -> Tuple[str, int]:
    """
    Joue UNE partie.
    Retourne (gagnant, nb_manches).
    gagnant ∈ {"BotA","BotB","TIMEOUT"}.
    """

    def _faire_partie():
        etat = creer_partie_bot_vs_bot()
        manches = 0

        while (not etat.terminee) and manches < max_manches:
            if etat.joueur_actif.nom == "BotA":
                carac = strat_a.choisir(etat)
            else:
                carac = strat_b.choisir(etat)

            carac = _safe_carac(carac)
            etat.appliquer_manche(carac)
            manches += 1

        if (not etat.terminee) or (etat.gagnant is None):
            return "TIMEOUT", manches

        return etat.gagnant.nom, manches

    return _executer_avec_seed_globale(seed, _faire_partie)


def _jouer_deux_parties_symetrisees(
    strat_a: Strategie,
    strat_b: Strategie,
    seed: int,
    max_manches: int = 5000,
) -> List[Tuple[str, int]]:
    """
    Comparaison équitable :
    - Partie 1 : A en BotA contre B en BotB avec seed = seed
    - Partie 2 : B en BotA contre A en BotB avec seed = seed

    Retourne une liste de 2 résultats "du point de vue de A" :
    chaque élément = (issue, nb_manches)
    avec issue dans {"A", "B", "TIMEOUT"}.
    """
    resultats = []

    # Partie 1 : A joue BotA
    g1, m1 = jouer_une_partie(strat_a, strat_b, seed=seed, max_manches=max_manches)
    if g1 == "TIMEOUT":
        resultats.append(("TIMEOUT", m1))
    elif g1 == "BotA":
        resultats.append(("A", m1))
    else:
        resultats.append(("B", m1))

    # Partie 2 : swap, mais on reconvertit le résultat du point de vue de A
    g2, m2 = jouer_une_partie(strat_b, strat_a, seed=seed, max_manches=max_manches)
    if g2 == "TIMEOUT":
        resultats.append(("TIMEOUT", m2))
    elif g2 == "BotB":
        # ici A jouait BotB
        resultats.append(("A", m2))
    else:
        resultats.append(("B", m2))

    return resultats


def comparer_deux_strategies(
    strat_a: Strategie,
    strat_b: Strategie,
    n_games: int,
    seed: int,
    print_every: int = 0,
    export_csv: bool = True,
    symetriser: bool = True,
    max_manches: int = 5000,
) -> Dict[str, object]:
    """
    UNE expérience :
    - symetriser=True (recommandé) : on joue 2 parties par seed (A/B puis B/A)
      => plus robuste et indépendant de l'ordre.
    - symetriser=False : une seule partie par seed.

    Les TIMEOUTS sont comptés et exclus du winrate.
    """

    victoires_a = 0
    victoires_b = 0

    manches_total_tous_runs = 0
    manches_parties_valides: List[int] = []
    manches_quand_a_gagne: List[int] = []
    manches_quand_b_gagne: List[int] = []

    nb_timeouts = 0

    generateur = random.Random(seed)

    for k in range(1, n_games + 1):
        s = generateur.randrange(0, 2**31 - 1)

        if symetriser:
            resultats = _jouer_deux_parties_symetrisees(
                strat_a, strat_b, seed=s, max_manches=max_manches
            )

            for issue, nb_manches in resultats:
                manches_total_tous_runs += nb_manches

                if issue == "TIMEOUT":
                    nb_timeouts += 1
                elif issue == "A":
                    victoires_a += 1
                    manches_parties_valides.append(nb_manches)
                    manches_quand_a_gagne.append(nb_manches)
                else:
                    victoires_b += 1
                    manches_parties_valides.append(nb_manches)
                    manches_quand_b_gagne.append(nb_manches)

        else:
            gagnant, m = jouer_une_partie(strat_a, strat_b, seed=s, max_manches=max_manches)
            manches_total_tous_runs += m

            if gagnant == "TIMEOUT":
                nb_timeouts += 1
            elif gagnant == "BotA":
                victoires_a += 1
                manches_parties_valides.append(m)
                manches_quand_a_gagne.append(m)
            else:
                victoires_b += 1
                manches_parties_valides.append(m)
                manches_quand_b_gagne.append(m)

        if print_every > 0 and (k % print_every == 0):
            print("  Parties terminées:", k, "/", n_games)

    nb_total = (2 * n_games) if symetriser else n_games
    nb_valides = nb_total - nb_timeouts

    if nb_valides <= 0:
        winrate_a = float("nan")
        winrate_b = float("nan")
        bas, haut = 0.0, 1.0
    else:
        winrate_a = 100.0 * victoires_a / nb_valides
        winrate_b = 100.0 * victoires_b / nb_valides
        bas, haut = ic95_proportion(victoires_a, nb_valides)

    res = {
        "mode": "simple",
        "A": strat_a.nom,
        "B": strat_b.nom,
        "n_games": n_games,
        "seed": seed,

        "wins_A": victoires_a,
        "wins_B": victoires_b,
        "n_valid_games": nb_valides,
        "n_total_runs": nb_total,
        "n_timeouts": nb_timeouts,

        "winrate_A_pct": winrate_a,
        "winrate_B_pct": winrate_b,
        "winrate_A_ci95_low_pct": 100.0 * bas,
        "winrate_A_ci95_high_pct": 100.0 * haut,

        # avg_rounds_overall = moyenne des parties terminées
        "avg_rounds_overall": moyenne(manches_parties_valides) if manches_parties_valides else float("nan"),

        # avg_rounds_all_runs = moyenne de tous les runs, timeout inclus
        "avg_rounds_all_runs": (manches_total_tous_runs / nb_total) if nb_total > 0 else float("nan"),

        "avg_rounds_when_A_wins": moyenne(manches_quand_a_gagne) if manches_quand_a_gagne else "",
        "avg_rounds_when_B_wins": moyenne(manches_quand_b_gagne) if manches_quand_b_gagne else "",
    }

    if export_csv:
        ecrire_ligne_csv(res)

    return res


def comparer_deux_strategies_repetitions(
    strat_a: Strategie,
    strat_b: Strategie,
    n_games: int,
    seed: int,
    n_repetitions: int,
    print_every: int = 0,
    export_csv: bool = True,
    symetriser: bool = True,
    max_manches: int = 5000,
) -> Dict[str, object]:
    """
    Analyse robuste (répétitions) :
    - On répète l'expérience plusieurs fois.
    - Chaque répétition utilise une seed différente.
    - On résume :
      moyenne / écart-type / médiane / min / max du winrate,
      + agrégation globale sur toutes les répétitions.
    """
    winrates: List[float] = []
    moyennes_manches_finies: List[float] = []
    moyennes_manches_tous_runs: List[float] = []
    timeouts: List[int] = []

    total_wins_a = 0
    total_wins_b = 0
    total_valid_games = 0
    total_timeouts = 0

    for rep in range(n_repetitions):
        seed_locale = seed + 10000 * rep

        if print_every > 0:
            print("Répétition", rep + 1, "/", n_repetitions)

        res_rep = comparer_deux_strategies(
            strat_a,
            strat_b,
            n_games=n_games,
            seed=seed_locale,
            print_every=print_every,
            export_csv=False,
            symetriser=symetriser,
            max_manches=max_manches,
        )

        try:
            winrates.append(float(res_rep["winrate_A_pct"]))
        except Exception:
            pass

        try:
            moyennes_manches_finies.append(float(res_rep["avg_rounds_overall"]))
        except Exception:
            pass

        try:
            moyennes_manches_tous_runs.append(float(res_rep["avg_rounds_all_runs"]))
        except Exception:
            pass

        try:
            total_wins_a += int(res_rep.get("wins_A", 0))
            total_wins_b += int(res_rep.get("wins_B", 0))
            total_valid_games += int(res_rep.get("n_valid_games", 0))
            total_timeouts += int(res_rep.get("n_timeouts", 0))
            timeouts.append(int(res_rep.get("n_timeouts", 0)))
        except Exception:
            pass

    if total_valid_games > 0:
        winrate_global = 100.0 * total_wins_a / total_valid_games
        bas_global, haut_global = ic95_proportion(total_wins_a, total_valid_games)
    else:
        winrate_global = float("nan")
        bas_global, haut_global = 0.0, 1.0

    res = {
        "mode": "repetitions",
        "A": strat_a.nom,
        "B": strat_b.nom,
        "n_games": n_games,
        "seed": seed,
        "n_repetitions": n_repetitions,

        "winrate_A_mean_pct": moyenne(winrates),
        "winrate_A_std_pct": ecart_type(winrates),
        "winrate_A_median_pct": mediane(winrates),
        "winrate_A_min_pct": min(winrates) if winrates else float("nan"),
        "winrate_A_max_pct": max(winrates) if winrates else float("nan"),

        # Agrégation globale : on recombine toutes les répétitions
        "total_wins_A": total_wins_a,
        "total_wins_B": total_wins_b,
        "total_valid_games": total_valid_games,
        "total_timeouts": total_timeouts,
        "n_timeouts": total_timeouts,

        "winrate_A_global_pct": winrate_global,
        "winrate_A_global_ci95_low_pct": 100.0 * bas_global,
        "winrate_A_global_ci95_high_pct": 100.0 * haut_global,

        "avg_rounds_overall_mean": moyenne(moyennes_manches_finies),
        "avg_rounds_overall_std": ecart_type(moyennes_manches_finies),

        "avg_rounds_all_runs_mean": moyenne(moyennes_manches_tous_runs),
        "avg_rounds_all_runs_std": ecart_type(moyennes_manches_tous_runs),
    }

    if export_csv:
        ecrire_ligne_csv(res)

    return res


# ============================================================
# ======================= AFFICHAGE ===========================
# ============================================================

def print_result(res: Dict[str, object]) -> None:
    mode = res.get("mode", "simple")

    if mode == "simple":
        A = res["A"]
        B = res["B"]
        n = res["n_games"]

        print("=" * 72)
        print(f"Match-up (simple):  A = {A}   vs   B = {B}   |   N = {n}")
        print("-" * 72)

        if isinstance(res.get("winrate_A_pct"), float):
            print(
                f"Winrate A: {res['winrate_A_pct']:.2f}%"
                f"   |   IC95 (Wilson): [{res['winrate_A_ci95_low_pct']:.2f}% ; {res['winrate_A_ci95_high_pct']:.2f}%]"
            )
            print(f"Winrate B: {res['winrate_B_pct']:.2f}%")
        else:
            print("Winrate: non disponible (trop de timeouts)")

        print("-" * 72)
        if isinstance(res.get("avg_rounds_overall"), float):
            print(f"Avg rounds overall (parties finies): {res['avg_rounds_overall']:.2f}")
        else:
            print("Avg rounds overall (parties finies): non disponible")

        if isinstance(res.get("avg_rounds_all_runs"), float):
            print(f"Avg rounds all runs (avec timeout): {res['avg_rounds_all_runs']:.2f}")

        if res.get("avg_rounds_when_A_wins") != "":
            print(f"Avg rounds when A wins:            {res['avg_rounds_when_A_wins']:.2f}")
        if res.get("avg_rounds_when_B_wins") != "":
            print(f"Avg rounds when B wins:            {res['avg_rounds_when_B_wins']:.2f}")

        print(f"Valid games: {res.get('n_valid_games', '')}")
        print(f"Timeouts: {res.get('n_timeouts', 0)}")
        print("=" * 72)
        print()

    else:
        A = res["A"]
        B = res["B"]
        n = res["n_games"]
        k = res["n_repetitions"]

        print("=" * 72)
        print(f"Match-up (répétitions):  A = {A}   vs   B = {B}   |   N = {n}   |   K = {k}")
        print("-" * 72)
        print(f"Winrate A (moyenne):     {res['winrate_A_mean_pct']:.2f}%")
        print(f"Winrate A (écart-type):  {res['winrate_A_std_pct']:.2f}%")
        print(f"Winrate A (médiane):     {res['winrate_A_median_pct']:.2f}%")
        print(f"Winrate A (min..max):    [{res['winrate_A_min_pct']:.2f}% ; {res['winrate_A_max_pct']:.2f}%]")
        print("-" * 72)
        print(
            f"Winrate A global:        {res['winrate_A_global_pct']:.2f}%"
            f"   |   IC95 global: [{res['winrate_A_global_ci95_low_pct']:.2f}% ; {res['winrate_A_global_ci95_high_pct']:.2f}%]"
        )
        print("-" * 72)
        print(f"Avg rounds overall mean (parties finies): {res['avg_rounds_overall_mean']:.2f}")
        print(f"Avg rounds overall std  (parties finies): {res['avg_rounds_overall_std']:.2f}")
        print(f"Avg rounds all runs mean (avec timeout):  {res['avg_rounds_all_runs_mean']:.2f}")
        print(f"Avg rounds all runs std  (avec timeout):  {res['avg_rounds_all_runs_std']:.2f}")
        print(f"Total wins A: {res.get('total_wins_A', 0)}")
        print(f"Total wins B: {res.get('total_wins_B', 0)}")
        print(f"Total valid games: {res.get('total_valid_games', 0)}")
        print(f"Timeouts (total): {res.get('total_timeouts', 0)}")
        print("=" * 72)
        print()


# ============================================================
# ======================= COMPARAISON ADAPTATIVE =============
# ============================================================

def comparer_toutes_strategies_adaptatif(
    seed: int = 12345,
    n_games_petit: int = 80,
    n_games_gros: int = 250,
    n_repetitions_gros: int = 5,
    print_every_gros: int = 50,
    export_csv: bool = True,
) -> None:
    """
    Compare toutes les stratégies entre elles, effort adaptatif.
    """
    for i in range(len(STRATEGIES)):
        for j in range(i + 1, len(STRATEGIES)):
            strat1 = STRATEGIES[i]
            strat2 = STRATEGIES[j]

            seed_locale = seed + 1000 * i + j

            strat1_grosse = est_grosse_strategie(strat1)
            strat2_grosse = est_grosse_strategie(strat2)

            if strat1_grosse and strat2_grosse:
                print(">>> GROS vs GROS :", strat1.nom, "vs", strat2.nom)
                res = comparer_deux_strategies_repetitions(
                    strat1,
                    strat2,
                    n_games=n_games_gros,
                    seed=seed_locale,
                    n_repetitions=n_repetitions_gros,
                    print_every=print_every_gros,
                    export_csv=export_csv,
                    symetriser=True,
                )
                print_result(res)
            else:
                res = comparer_deux_strategies(
                    strat1,
                    strat2,
                    n_games=n_games_petit,
                    seed=seed_locale,
                    print_every=0,
                    export_csv=export_csv,
                    symetriser=True,
                )
                print_result(res)


def run_stats() -> None:
    """
    Point d'entrée : python sources/main.py stats
    """
    print("=== MODE STATS (sans pygame) ===")
    print("Stratégies disponibles:")
    for s in STRATEGIES:
        tag = ""
        if est_grosse_strategie(s):
            tag = " (GROSSE)"
        elif est_petite_strategie(s):
            tag = " (petite)"
        print(" -", s.nom + tag)
    print()

    seed = 12345

    comparer_toutes_strategies_adaptatif(
        seed=seed,
        n_games_petit=500,
        n_games_gros=400,
        n_repetitions_gros=6,
        print_every_gros=50,
        export_csv=True,
    )


if __name__ == "__main__":
    run_stats()