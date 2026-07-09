"""Hash-consing : partage de structure (DAG) sur formlang.tree.Term. À COMPLÉTER.
-> TP arbres (E4 intern/partage, E5 round-trip, Q5 compression).

Règle « gate » : INSTANCIER formlang.tree.Term, ne pas le réécrire."""
from __future__ import annotations
from formlang.tree import Term

NodeId = int


class CompactStore:
    def __init__(self):
        self._nodes: list[tuple] = []          # id -> (symbol, label, kids_ids)
        self._table: dict[tuple, NodeId] = {}   # clé canonique -> id
        self._total = 0

    def intern(self, t: Term) -> NodeId:
        """Interne un arbre avec partage de structure (DAG)."""
        # Interner récursivement les enfants
        kids_ids = tuple(self.intern(child) for child in t.children)
        
        # Incrémenter le compteur total
        self._total += 1
        
        # Clé canonique
        key = (t.symbol, t.label, kids_ids)
        
        # Vérifier si déjà internalisé
        if key in self._table:
            return self._table[key]
        
        # Créer un nouvel ID
        nid = len(self._nodes)
        self._nodes.append((t.symbol, t.label, kids_ids))
        self._table[key] = nid
        
        return nid

    def get(self, nid: NodeId) -> Term:
        """Reconstruit l'arbre original à partir de son ID (round-trip exact)."""
        symbol, label, kids_ids = self._nodes[nid]
        
        # Reconstruire récursivement les enfants
        children = tuple(self.get(kid_id) for kid_id in kids_ids)
        
        return Term(symbol, children, label)

    def total_nodes(self) -> int:
        return self._total

    def unique_nodes(self) -> int:
        return len(self._nodes)

    def compression(self) -> float:
        """Mesure le taux de compression: 1 - uniques/total."""
        total = self.total_nodes()
        if total == 0:
            return 0.0
        return 1.0 - self.unique_nodes() / total
