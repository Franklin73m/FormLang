"""Automate à pile (acceptation pile vide). À COMPLÉTER.  -> Jour 2 (E2.1)."""
from __future__ import annotations


class DelimiterPDA:
    def __init__(self, pairs=(("[", "]"), ("(", ")")), ignore=("a", "o", "r", "e")):
        self.open = {o for o, _ in pairs}
        self.match = {c: o for o, c in pairs}     # fermant -> ouvrant attendu
        self.ignore = set(ignore)

    def accepts(self, w: str) -> bool:
        """Accepte par pile vide. Empile sur délimiteur ouvrant,
        dépile sur délimiteur fermant s'il correspond, ignore les autres."""
        stack = []
        for char in w:
            if char in self.open:
                stack.append(char)
            elif char in self.match:
                # Délimiteur fermant
                expected = self.match[char]
                if not stack or stack[-1] != expected:
                    return False  # Pas d'ouvrant correspondant
                stack.pop()
            # Ignorer les caractères de ignore
        
        # Accepter ssi la pile est vide
        return len(stack) == 0
