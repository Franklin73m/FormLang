"""Grammaire hors-contexte : génération bornée.  -> Jour 2 (E2.2)."""
from __future__ import annotations
from dataclasses import dataclass


@dataclass
class CFG:
    rules: dict
    start: str
    nonterminals: set

    def generate(self, max_len: int) -> set:
        """Énumère les mots TERMINAUX dérivables de longueur <= max_len par BFS."""
        terminals = set()
        visited = set()
        queue = [(self.start,)]  # tuple de symboles (forme sentencielle)
        max_nonterms = 100  # limite de non-terminaux pour éviter l'explosion
        
        while queue:
            form = queue.pop(0)
            form_key = form
            if form_key in visited:
                continue
            visited.add(form_key)
            
            # Si c'est un mot terminal complet
            if all(s not in self.nonterminals for s in form):
                word = ''.join(form)
                if len(word) <= max_len:
                    terminals.add(word)
                continue
            
            # Limiter l'exploration si trop de non-terminaux
            nonterminal_count = sum(1 for s in form if s in self.nonterminals)
            if nonterminal_count > max_nonterms:
                continue
            
            # Limiter si le mot est déjà trop long
            if len(''.join(str(s) for s in form)) > max_len + 10:
                continue
            
            # Expansion : trouver le premier non-terminal et appliquer les règles
            for i, sym in enumerate(form):
                if sym in self.nonterminals:
                    for production in self.rules.get(sym, []):
                        new_form = form[:i] + production + form[i+1:]
                        if len(''.join(str(s) for s in new_form)) <= max_len + 10:
                            queue.append(new_form)
                    break
        
        return terminals


def balanced_cfg() -> "CFG":
    # FOURNI : S -> S S | [ S ] | ( S ) | a | o | r | eps
    return CFG(
        rules={"S": [("S", "S"), ("[", "S", "]"), ("(", "S", ")"),
                     ("a",), ("o",), ("r",), ()]},
        start="S", nonterminals={"S"},
    )
