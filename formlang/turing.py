"""Machine de Turing déterministe (ruban dict bi-infini). À COMPLÉTER : run.
-> Jour 4 (E4.1)."""
from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class TMResult:
    accepted: bool
    tape: str
    steps: int
    trace: list = field(default_factory=list)


@dataclass
class TuringMachine:
    transitions: dict           # (q, a) -> (q', b, d in {'L','R','S'})
    start: str
    accept: set
    blank: str = "_"
    reject: set = field(default_factory=set)

    # ----- fourni -------------------------------------------------------------
    def _read(self, tape: dict) -> str:
        if not tape:
            return ""
        lo, hi = min(tape), max(tape)
        return "".join(tape.get(i, self.blank) for i in range(lo, hi + 1)).strip(self.blank)

    def _window(self, tape: dict) -> str:
        if not tape:
            return ""
        lo, hi = min(tape), max(tape)
        return "".join(tape.get(i, self.blank) for i in range(lo, hi + 1))

    # ----- à compléter --------------------------------------------------------
    def run(self, word: str, max_steps: int = 1_000_000, trace: bool = False) -> "TMResult":
        """Simule la machine de Turing sur le mot donné."""
        # Initialiser le ruban (dict: position -> symbole)
        tape = {i: c for i, c in enumerate(word)}
        head = 0  # Position de la tête de lecture
        state = self.start  # État courant
        steps = 0
        trace_list = []
        
        while steps < max_steps:
            # Ajouter à la trace si demandé
            if trace:
                tape_str = self._window(tape) if tape else ""
                trace_list.append((head, state, tape_str))
            
            # Vérifier si état d'arrêt (acceptant ou rejeté)
            if state in self.accept:
                tape_str = self._read(tape)
                return TMResult(accepted=True, tape=tape_str, steps=steps, trace=trace_list)
            
            if state in self.reject:
                tape_str = self._read(tape)
                return TMResult(accepted=False, tape=tape_str, steps=steps, trace=trace_list)
            
            # Lire le symbole courant
            current = tape.get(head, self.blank)
            
            # Chercher la transition
            if (state, current) not in self.transitions:
                # Pas de transition: arrêter (rejet)
                tape_str = self._read(tape)
                return TMResult(accepted=False, tape=tape_str, steps=steps, trace=trace_list)
            
            # Appliquer la transition
            next_state, write_sym, direction = self.transitions[(state, current)]
            
            # Écrire
            tape[head] = write_sym
            
            # Déplacer la tête
            if direction == 'L':
                head -= 1
            elif direction == 'R':
                head += 1
            # 'S' ne fait rien
            
            # Changer d'état
            state = next_state
            steps += 1
        
        # Dépassement du nombre d'étapes max
        tape_str = self._read(tape)
        return TMResult(accepted=False, tape=tape_str, steps=steps, trace=trace_list)
