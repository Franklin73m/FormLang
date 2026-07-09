"""AFN (eps = ''). À COMPLÉTER : to_dfa par sous-ensembles.  -> Jour 1 (E1.3)."""
from __future__ import annotations
from dataclasses import dataclass, field
from .dfa import DFA


@dataclass
class NFA:
    transitions: dict            # (state, sym|'') -> set(states)
    start: str
    accept: set
    alphabet: set = field(default_factory=set)

    def __post_init__(self):
        if not self.alphabet:
            self.alphabet = {a for (_, a) in self.transitions if a != ""}

    # ----- fourni -------------------------------------------------------------
    def _eps_closure(self, states: frozenset) -> frozenset:
        stack, clos = list(states), set(states)
        while stack:
            s = stack.pop()
            for t in self.transitions.get((s, ""), ()):
                if t not in clos:
                    clos.add(t)
                    stack.append(t)
        return frozenset(clos)

    def _move(self, states: frozenset, a: str) -> frozenset:
        out = set()
        for s in states:
            out |= self.transitions.get((s, a), set())
        return frozenset(out)

    def accepts(self, w: str) -> bool:
        cur = self._eps_closure(frozenset({self.start}))
        for c in w:
            cur = self._eps_closure(self._move(cur, c))
        return any(s in self.accept for s in cur)

    # ----- à compléter --------------------------------------------------------
    def to_dfa(self) -> DFA:
        """Convertit le NFA en DFA par la construction des sous-ensembles."""
        # État initial du DFA : fermeture eps de l'état initial du NFA
        dfa_start = self._eps_closure(frozenset({self.start}))
        
        # BFS pour explorer tous les états du DFA
        dfa_states = {}  # frozenset -> nom d'état
        dfa_states[dfa_start] = "q0"
        queue = [dfa_start]
        state_counter = 1
        
        dfa_trans = {}
        
        while queue:
            nfa_states_set = queue.pop(0)
            dfa_state_name = dfa_states[nfa_states_set]
            
            # Pour chaque symbole d'entrée, calculer l'image
            for sym in self.alphabet:
                # Déplacer dans les états du NFA
                next_nfa = self._move(nfa_states_set, sym)
                # Fermeture eps
                next_nfa_closed = self._eps_closure(next_nfa)
                
                if next_nfa_closed:  # non vide
                    if next_nfa_closed not in dfa_states:
                        dfa_states[next_nfa_closed] = f"q{state_counter}"
                        state_counter += 1
                        queue.append(next_nfa_closed)
                    
                    next_dfa_state = dfa_states[next_nfa_closed]
                    dfa_trans[(dfa_state_name, sym)] = next_dfa_state
        
        # États acceptants du DFA : ceux qui contiennent un état acceptant du NFA
        dfa_accept = {
            dfa_states[nfa_set]
            for nfa_set in dfa_states
            if any(s in self.accept for s in nfa_set)
        }
        
        return DFA(dfa_trans, dfa_states[dfa_start], dfa_accept, self.alphabet)
