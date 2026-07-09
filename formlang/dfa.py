"""AFD. À COMPLÉTER : run, accepts, minimize (Moore).  -> Jour 1 (E1.1, E1.2)."""
from __future__ import annotations
from dataclasses import dataclass, field
from collections import deque


@dataclass
class DFA:
    transitions: dict            # (state, sym) -> state
    start: str
    accept: set
    alphabet: set = field(default_factory=set)

    def __post_init__(self):
        if not self.alphabet:
            self.alphabet = {a for (_, a) in self.transitions}

    def run(self, w: str):
        """Exécute le DFA sur le mot w. Retourne l'état atteint ou None si bloqué."""
        state = self.start
        for c in w:
            state = self.transitions.get((state, c))
            if state is None:
                return None
        return state

    def accepts(self, w: str) -> bool:
        """Retourne True si le DFA accepte le mot w."""
        final_state = self.run(w)
        return final_state is not None and final_state in self.accept

    # ----- fourni : utilitaires pour la minimisation --------------------------
    def _reachable(self) -> set:
        seen, todo = {self.start}, deque([self.start])
        while todo:
            s = todo.popleft()
            for a in self.alphabet:
                t = self.transitions.get((s, a))
                if t is not None and t not in seen:
                    seen.add(t)
                    todo.append(t)
        return seen

    def _completed(self):
        SINK = "__sink__"
        trans = dict(self.transitions)
        states = self._reachable()
        need = False
        for s in states:
            for a in self.alphabet:
                if (s, a) not in trans:
                    trans[(s, a)] = SINK
                    need = True
        if need:
            states = states | {SINK}
            for a in self.alphabet:
                trans[(SINK, a)] = SINK
        return states, trans

    def minimize(self) -> "DFA":
        """Minimise le DFA par l'algorithme de Moore (raffinement de partition)."""
        states, trans = self._completed()

        # Initialiser les partitions : acceptants vs non-acceptants
        reachable = self._reachable()
        accepting = self.accept & reachable
        non_accepting = reachable - self.accept

        if not non_accepting:
            partitions = [accepting]
        elif not accepting:
            partitions = [non_accepting]
        else:
            partitions = [non_accepting, accepting]

        # Raffiner jusqu'à stabilisation
        changed = True
        while changed:
            changed = False
            new_partitions = []

            for part in partitions:
                # Pour chaque symbole, vérifier si on peut subdiviser la partition
                splits = {}
                for state in part:
                    key = tuple(
                        next((i for i, p in enumerate(partitions)
                              if trans.get((state, a)) in p), None)
                        for a in sorted(self.alphabet)
                    )
                    if key not in splits:
                        splits[key] = []
                    splits[key].append(state)

                # Ajouter les sous-partitions
                for sub_part in splits.values():
                    new_partitions.append(frozenset(sub_part))
                    if len(splits) > 1:
                        changed = True

            partitions = new_partitions

        # Construire le DFA minimal
        part_map = {}
        for i, part in enumerate(partitions):
            for state in part:
                part_map[state] = f"q{i}"

        new_trans = {}
        for (s, a), t in trans.items():
            if part_map[s] != part_map.get(t, None):  # seulement si dans reachable
                new_trans[(part_map[s], a)] = part_map[t]

        new_start = part_map[self.start]
        new_accept = {part_map[s] for s in accepting}

        return DFA(new_trans, new_start, new_accept, self.alphabet)

    def num_states(self) -> int:
        st = {self.start}
        for (s, _), t in self.transitions.items():
            st.add(s)
            st.add(t)
        return len(st)
