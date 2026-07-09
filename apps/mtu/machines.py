"""Opérations comme VRAIES machines de Turing. À COMPLÉTER : tables ADD, SUB.
-> Jour 4 (E4.3)."""
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
        # q0 : balaie tout le ruban vers la droite jusqu'au bout.
        ('q0', '1'): ('q0', '1', 'R'),
        ('q0', 'X'): ('q0', 'X', 'R'),
        ('q0', '-'): ('q0', '-', 'R'),
        ('q0', '_'): ('q1', '_', 'L'),

        # q1 : depuis la fin, cherche vers la GAUCHE le 1 non marqué le plus
        # à droite dans m (saute les X déjà consommés). Trouvé -> le marque
        # X et passe en q2. Rencontre '-' sans trouver de 1 -> m est épuisé,
        # direction nettoyage (q_clean_n).
        ('q1', 'X'): ('q1', 'X', 'L'),
        ('q1', '1'): ('q2', 'X', 'L'),
        ('q1', '-'): ('q_clean_n', '-', 'L'),

        # q2 : continue vers la gauche jusqu'au séparateur '-'.
        ('q2', '1'): ('q2', '1', 'L'),
        ('q2', 'X'): ('q2', 'X', 'L'),
        ('q2', '-'): ('q3', '-', 'L'),

        # q3 : cherche vers la gauche le 1 non marqué le plus à droite
        # dans n (saute les X déjà consommés). Trouvé -> le marque X,
        # repart vers la droite (q0) pour la prochaine paire. Si on atteint
        # le bord gauche sans trouver de 1 : n est épuisé alors que m ne
        # l'était pas -> résultat forcé à 0 (q_zero).
        ('q3', 'X'): ('q3', 'X', 'L'),
        ('q3', '1'): ('q0', 'X', 'R'),
        ('q3', '_'): ('q_zero', '_', 'R'),

        # q_zero : m > n, le résultat est 0. On efface tout ce qui reste.
        ('q_zero', 'X'): ('q_zero', '_', 'R'),
        ('q_zero', '-'): ('q_zero', '_', 'R'),
        ('q_zero', '1'): ('q_zero', '_', 'R'),
        ('q_zero', '_'): ('qf', '_', 'S'),

        # q_clean_n : m est épuisé (tous ses 1 sont marqués X). On nettoie
        # n en remontant vers la gauche : X -> blanc (unité consommée),
        # 1 -> inchangé (unité survivante = résultat), jusqu'au bord gauche.
        ('q_clean_n', '1'): ('q_clean_n', '1', 'L'),
        ('q_clean_n', 'X'): ('q_clean_n', '_', 'L'),
        ('q_clean_n', '_'): ('q_recross', '_', 'R'),

        # q_recross : retraverse n (mélange de 1 et de blancs) sans y
        # toucher, jusqu'à retrouver '-'.
        ('q_recross', '1'): ('q_recross', '1', 'R'),
        ('q_recross', '_'): ('q_recross', '_', 'R'),
        ('q_recross', '-'): ('q_clean_m', '_', 'R'),

        # q_clean_m : efface les X restants de l'ancien m jusqu'au bord
        # droit -> terminé, résultat = les 1 survivants de n.
        ('q_clean_m', 'X'): ('q_clean_m', '_', 'R'),
        ('q_clean_m', '_'): ('qf', '_', 'S'),
    },
    start="q0", accept={"qf"},
)
