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

        # Partition initiale : acceptants vs non-acceptants (sur TOUS les
        # états complétés, y compris le puits, sinon le puits ne serait
        # jamais distingué correctement pendant le raffinement).
        accepting = {s for s in states if s in self.accept}
        non_accepting = states - accepting
        partitions = [p for p in (non_accepting, accepting) if p]

        # Raffiner jusqu'à stabilisation : on sépare un bloc dès que deux de
        # ses états atterrissent, pour une même lettre, dans des blocs
        # DIFFERENTS.
        changed = True
        while changed:
            changed = False
            block_of = {s: i for i, part in enumerate(partitions) for s in part}
            new_partitions = []
            for part in partitions:
                splits: dict = {}
                for state in part:
                    key = tuple(block_of[trans[(state, a)]] for a in sorted(self.alphabet))
                    splits.setdefault(key, []).append(state)
                if len(splits) > 1:
                    changed = True
                new_partitions.extend(frozenset(g) for g in splits.values())
            partitions = new_partitions

        # Construire le DFA minimal : un état par bloc. On enregistre TOUTES
        # les transitions (y compris les boucles internes à un bloc), sinon
        # le DFA minimisé serait incomplet et rejetterait à tort des mots
        # valides dès qu'il faudrait rester dans le même bloc. On ne
        # parcourt que les états RÉELLEMENT ATTEIGNABLES (states) : trans
        # peut contenir des transitions issues d'états non atteignables
        # depuis self.start, qui n'appartiennent à aucun bloc de partitions.
        part_map = {s: f"q{i}" for i, part in enumerate(partitions) for s in part}

        new_trans = {}
        for s in states:
            for a in self.alphabet:
                t = trans[(s, a)]
                new_trans[(part_map[s], a)] = part_map[t]

        new_start = part_map[self.start]
        new_accept = {part_map[s] for s in accepting}

        return DFA(new_trans, new_start, new_accept, set(self.alphabet))

    def num_states(self) -> int:
        st = {self.start}
        for (s, _), t in self.transitions.items():
            st.add(s)
            st.add(t)
        return len(st)
