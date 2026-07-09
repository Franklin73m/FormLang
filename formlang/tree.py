"""Automate d'arbres ascendant (BUTA) générique. À COMPLÉTER : run, accepts,
product.  -> Jour 3 (E3.1, E3.4)."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Hashable


@dataclass(frozen=True)
class Term:
    symbol: str
    children: tuple["Term", ...] = ()
    label: Optional[str] = None


class _Reject:
    __slots__ = ()
    def __repr__(self):
        return "REJECT"


REJECT = _Reject()


class TreeAutomaton:
    def __init__(self, final_states):
        self.delta: dict[tuple[str, tuple], Hashable] = {}
        self.final: set = set(final_states)

    def add_rule(self, symbol: str, child_states, result) -> None:
        # FOURNI
        self.delta[(symbol, tuple(child_states))] = result

    def run(self, t: "Term"):
        """Étiquette le terme en POST-ORDRE (bottom-up). Retourne l'état de la racine
        ou REJECT si impossible."""
        # Cas base: feuille
        if not t.children:
            # Une feuille est une règle terminal -> état
            result = self.delta.get((t.symbol, ()))
            return result if result is not None else REJECT
        
        # Cas récursif: appliquer run aux enfants d'abord
        child_states = []
        for child in t.children:
            child_state = self.run(child)
            if child_state is REJECT:
                return REJECT
            child_states.append(child_state)
        
        # Chercher la règle pour ce symbole et ces états enfants
        result = self.delta.get((t.symbol, tuple(child_states)))
        return result if result is not None else REJECT

    def accepts(self, t: "Term") -> bool:
        """Accepte si run(t) est un état final."""
        state = self.run(t)
        return state is not REJECT and state in self.final


def product(a1: "TreeAutomaton", a2: "TreeAutomaton") -> "TreeAutomaton":
    """Construit l'automate produit A1 × A2 pour l'intersection.
    Les états du produit sont des paires (q1, q2)."""
    
    # États finaux du produit: paires de finaux
    final_states = {
        (f1, f2) for f1 in a1.final for f2 in a2.final
    }
    
    prod = TreeAutomaton(final_states)
    
    # Ajouter les règles du produit
    # Pour chaque règle de a1: (symbol, child_states1) -> q1
    # Et chaque règle de a2: (symbol, child_states2) -> q2
    # Créer une règle du produit: (symbol, (q1,...), (q2,...)) -> (q1_result, q2_result)
    
    seen = set()
    
    for (sym1, states1), q1_result in a1.delta.items():
        for (sym2, states2), q2_result in a2.delta.items():
            if sym1 == sym2 and len(states1) == len(states2):
                # Compatible
                prod_states = tuple((s1, s2) for s1, s2 in zip(states1, states2))
                prod_result = (q1_result, q2_result)
                key = (sym1, prod_states, prod_result)
                if key not in seen:
                    prod.add_rule(sym1, prod_states, prod_result)
                    seen.add(key)
    
    return prod
