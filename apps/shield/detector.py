"""SingularityDetector. À COMPLÉTER : table de l'AFD 'or'.  -> Jour 1 (E1.1)."""
from formlang.dfa import DFA

_DFA_OR = DFA(
    transitions={
        # État A (initial): aucun "o" vu
        ('A', 'a'): 'A',
        ('A', 'o'): 'B',
        ('A', 'r'): 'A',
        
        # État B: un "o" vu, "r" le termine
        ('B', 'a'): 'A',  # réinitialiser
        ('B', 'o'): 'B',  # rester armé
        ('B', 'r'): 'C',  # trouvé "or"!
        
        # État C (acceptant): "or" vu, absorbant
        ('C', 'a'): 'C',
        ('C', 'o'): 'C',
        ('C', 'r'): 'C',
    },
    start="A", accept={"C"}, alphabet={"a", "o", "r"},
)


def contains_or(w: str) -> bool:
    return _DFA_OR.accepts(w)


def detector_dfa() -> DFA:
    return _DFA_OR
