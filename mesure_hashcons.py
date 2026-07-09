"""Mesure bonus du hash-consing (Jour 3, Q3.5) sur un corpus d'environ 10 000 mots.

Usage :
    python mesure_hashcons.py

Utilise les corpus déjà fournis dans apps/morpho/corpora.py (PREFIXES_A,
SUFFIXES_B, roots) pour générer un corpus réaliste mélangeant une "langue
préfixante" (chaque racine + chaque préfixe de PREFIXES_A) et une "langue
suffixante" (chaque racine + chaque suffixe de SUFFIXES_B), en plus des
racines nues.
"""
from apps.morpho.corpora import PREFIXES_A, SUFFIXES_B, roots
from apps.morpho.automaton import build_word
from apps.hashcons.store import CompactStore


def main():
    R = roots(600)  # 600 racines (le générateur peut en fournir jusqu'à 2500)
    store = CompactStore()
    count = 0

    for r in R:
        store.intern(build_word([], r, []))          # racine seule
        count += 1
        for p in PREFIXES_A:                          # racine + préfixe
            store.intern(build_word([p], r, []))
            count += 1
        for s in SUFFIXES_B:                           # racine + suffixe
            store.intern(build_word([], r, [s]))
            count += 1

    print(f"mots internés (appels à intern)              : {count}")
    print(f"total_nodes (nœuds internes, y compris partages) : {store.total_nodes()}")
    print(f"unique_nodes (nœuds réellement distincts stockés) : {store.unique_nodes()}")
    print(f"compression = 1 - unique/total                : {store.compression():.4f}")


if __name__ == "__main__":
    main()
