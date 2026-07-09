"""Opérations comme VRAIES machines de Turing.  -> Jour 4 (E4.3)."""
from formlang.turing import TuringMachine

ADD = TuringMachine(
    transitions={
        # Scan à droite jusqu'à +
        ('q0', '1'): ('q0', '1', 'R'),
        ('q0', '+'): ('q1', '1', 'R'),  # Remplacer + par 1
        
        # Atteint le blanc après les m 1s, revenir
        ('q1', '1'): ('q1', '1', 'R'),
        ('q1', '_'): ('q2', '_', 'L'),
        
        # Revenir à gauche jusqu'au début
        ('q2', '1'): ('q2', '1', 'L'),
        ('q2', '_'): ('q3', '_', 'R'),  # Atteint le début
        
        # Effacer un 1 pour compenser (puisqu'on a changé + en 1)
        ('q3', '1'): ('qf', '_', 'S'),
    },
    start="q0", accept={"qf"},
)

SUB = TuringMachine(
    transitions={
        # Scan à droite jusqu'à -
        ('q0', '1'): ('q0', '1', 'R'),
        ('q0', '-'): ('q1', '-', 'R'),
        
        # Essayer de marquer un 1 après -, ignorer les X
        ('q1', '1'): ('q2', 'X', 'L'),  # Marquer ce 1
        ('q1', 'X'): ('q1', 'X', 'R'),  # Ignorer les 1s déjà marqués
        ('q1', '_'): ('q5', '_', 'L'),  # Pas de 1 après, aller nettoyer
        
        # Revenir à gauche au -
        ('q2', '1'): ('q2', '1', 'L'),
        ('q2', 'X'): ('q2', 'X', 'L'),
        ('q2', '_'): ('q2', '_', 'L'),  # Ignorer les blancs (du nettoyage précédent)
        ('q2', '-'): ('q3', '-', 'L'),
        
        # Chercher un 1 avant le - à effacer (continue même sur blancs)
        ('q3', '1'): ('q4', '_', 'R'),  # Trouvé! L'effacer et revenir
        ('q3', '_'): ('q3', '_', 'L'),  # Continuer à gauche sur les blancs
        
        # Revenir à droite vers -
        ('q4', '_'): ('q4', '_', 'R'),
        ('q4', '1'): ('q4', '1', 'R'),
        ('q4', '-'): ('q1', '-', 'R'),  # Boucle pour prochaine itération
        
        # Nettoyer: d'abord revenir à gauche jusqu'à la fin (avant les 1s du début)
        ('q5', '1'): ('q5', '1', 'L'),
        ('q5', 'X'): ('q5', 'X', 'L'),
        ('q5', '_'): ('q5', '_', 'L'),  # Continuer à gauche
        ('q5', '-'): ('q6', '_', 'R'),  # Effacer le - et aller à droite pour les X
        
        # Effacer tous les X en allant à droite
        ('q6', 'X'): ('q6', '_', 'R'),  # Effacer chaque X
        ('q6', '_'): ('qf', '_', 'S'),  # Atteint le blanc, terminé
    },
    start="q0", accept={"qf"},
)
