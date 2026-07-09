"""Grammaire hors-contexte : génération bornée. À COMPLÉTER.  -> Jour 2 (E2.2)."""
from __future__ import annotations
from dataclasses import dataclass


@dataclass
class CFG:
    rules: dict
    start: str
    nonterminals: set

    def generate(self, max_len: int) -> set:
        """Énumère les mots TERMINAUX dérivables de longueur <= max_len.

        Approche ascendante par longueur (dans l'esprit de CYK) : pour k
        croissant de 0 à max_len, on calcule l'ensemble EXACT des mots de
        longueur k dérivables de chaque non-terminal, en combinant les
        résultats déjà connus pour des longueurs plus courtes.

        Piège classique du sujet (cf. énoncé jour 2) : avec S -> S S | ... |
        eps, explorer les formes sententielles (S, SS, SSS, ...) explose
        combinatoirement, car il existe énormément de façons distinctes de
        combiner des non-terminaux avant même de produire un seul terminal.
        En travaillant directement sur des MOTS CONCRETS indexés par
        longueur, on évite ce problème à la racine : chaque combinaison
        calculée correspond déjà à un résultat utile, jamais à une forme
        intermédiaire redondante.
        """
        # words[A][k] = ensemble des mots de longueur EXACTE k dérivables de A
        words = {nt: [set() for _ in range(max_len + 1)] for nt in self.nonterminals}

        def symbol_words(sym):
            # Pour un terminal, un seul mot de longueur 1 (lui-même) ;
            # pour un non-terminal, la table déjà calculée (par longueur).
            if sym in self.nonterminals:
                return words[sym]
            return [set(), {sym}]

        changed = True
        while changed:
            changed = False
            for nt in self.nonterminals:
                for production in self.rules.get(nt, []):
                    # "Convolution" le long de la production : on combine les
                    # mots possibles symbole par symbole, en ne conservant
                    # que les longueurs totales <= max_len.
                    partial = {0: {""}}
                    for sym in production:
                        sym_words = symbol_words(sym)
                        new_partial: dict = {}
                        for len_so_far, prefixes in partial.items():
                            max_add = max_len - len_so_far
                            for len_sym in range(0, min(len(sym_words) - 1, max_add) + 1):
                                suffixes = sym_words[len_sym]
                                if not suffixes:
                                    continue
                                bucket = new_partial.setdefault(len_so_far + len_sym, set())
                                for p in prefixes:
                                    for s in suffixes:
                                        bucket.add(p + s)
                        partial = new_partial
                        if not partial:
                            break  # plus aucune combinaison ne tient dans max_len

                    for k, ws in partial.items():
                        before = len(words[nt][k])
                        words[nt][k] |= ws
                        if len(words[nt][k]) != before:
                            changed = True

        result = set()
        for k in range(max_len + 1):
            result |= words[self.start][k]
        return result


def balanced_cfg() -> "CFG":
    # FOURNI : S -> S S | [ S ] | ( S ) | a | o | r | eps
    return CFG(
        rules={"S": [("S", "S"), ("[", "S", "]"), ("(", "S", ")"),
                     ("a",), ("o",), ("r",), ()]},
        start="S", nonterminals={"S"},
    )
