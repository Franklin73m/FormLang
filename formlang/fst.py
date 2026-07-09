"""Transducteur fini séquentiel. À COMPLÉTER : transduce.  -> Jour 1 (E1.4)."""
from __future__ import annotations
from dataclasses import dataclass


@dataclass
class SequentialFST:
    transitions: dict            # (state, in_sym) -> (next_state, out_sym)
    start: str
    finals: set
    identity_on_missing: bool = False

    def transduce(self, w: str) -> str:
        """Transduit le mot w. Accumule les sorties de chaque transition."""
        state = self.start
        output = ""
        for c in w:
            transition = self.transitions.get((state, c))
            if transition is None:
                if self.identity_on_missing:
                    output += c
                else:
                    return None
            else:
                next_state, out_sym = transition
                state = next_state
                output += out_sym
        
        # Vérifier que l'état final est acceptant
        if state not in self.finals:
            return None
        
        return output


def compose(t1: "SequentialFST", t2: "SequentialFST") -> "SequentialFST":
    # FOURNI : t(w) = t2(t1(w)). États = paires.
    trans = {}
    for (s1, a), (s1n, b) in t1.transitions.items():
        for (s2, x), (s2n, c) in t2.transitions.items():
            if x == b:
                trans[((s1, s2), a)] = ((s1n, s2n), c)
    finals = {(f1, f2) for f1 in t1.finals for f2 in t2.finals}
    return SequentialFST(trans, (t1.start, t2.start), finals)


def leet_fst() -> "SequentialFST":
    """Crée un FST qui remplace le leetspeak par des lettres normales.
    Mappings: 4→a, 3→e, 0→o, 1→i, 5→s
    Identité sur les autres symboles.
    """
    mappings = {
        '4': 'a',
        '3': 'e',
        '0': 'o',
        '1': 'i',
        '5': 's'
    }
    
    trans = {}
    for char, replacement in mappings.items():
        trans[('q0', char)] = ('q0', replacement)
    
    # Les autres caractères restent inchangés (identity_on_missing=True)
    return SequentialFST(trans, 'q0', {'q0'}, identity_on_missing=True)


def reverse_twoway(w: str) -> str:
    # FOURNI : renversement (modélise une transduction bidirectionnelle).
    return w[::-1]
