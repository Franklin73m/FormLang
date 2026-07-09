"""AttackDecomposer (instancie formlang.tree). À COMPLÉTER : règles Delta.
-> Jour 3 (E3.3). 100% structurel. Constructeurs FOURNIS."""
from formlang.tree import Term, TreeAutomaton

SAFE, OVR, ROLE, DANGER = "safe", "ovr", "role", "danger"
_SEV = {SAFE: 0, OVR: 1, ROLE: 2}
_BY_SEV = {0: SAFE, 1: OVR, 2: ROLE}
_ALL = (SAFE, OVR, ROLE, DANGER)


def _seq(x, y):
    """Fusion pour seq: DANGER si l'un est DANGER ou si {OVR, ROLE}."""
    if x == DANGER or y == DANGER:
        return DANGER
    # Si les deux contiennent OVR et ROLE ensemble
    states = {x, y}
    if OVR in states and ROLE in states:
        return DANGER
    # Sinon, prendre le max de sévérité
    return _BY_SEV[max(_SEV.get(x, 3), _SEV.get(y, 3))]


def shield_automaton() -> TreeAutomaton:
    A = TreeAutomaton(final_states={DANGER})
    
    # Feuilles
    A.add_rule("txt", (), SAFE)
    A.add_rule("enc", (), SAFE)
    A.add_rule("ovr", (), OVR)
    A.add_rule("role", (), ROLE)
    
    # Fusion de seq
    for x in _ALL:
        for y in _ALL:
            result = _seq(x, y)
            A.add_rule("seq", (x, y), result)
    
    # frame et sys: SAFE → SAFE, autre → DANGER
    for state in _ALL:
        result = SAFE if state == SAFE else DANGER
        A.add_rule("frame", (state,), result)
        A.add_rule("sys", (state,), result)
    
    return A


# ----- constructeurs FOURNIS ------------------------------------------------
def txt():  return Term("txt")
def enc():  return Term("enc")
def ovr():  return Term("ovr")
def role(): return Term("role")
def seq(a, b): return Term("seq", (a, b))
def frame(a):  return Term("frame", (a,))
def sys(a):    return Term("sys", (a,))


def is_blocked(A: TreeAutomaton, t: Term) -> bool:
    return A.accepts(t)

# ----- P4.5 : « dangereux ET doublement encodé » (produit A x A_enc) ---------
def enc_automaton() -> TreeAutomaton:
    """Automate qui compte les feuilles `enc` (plafonné à 2)."""
    A = TreeAutomaton(final_states={2})
    
    # Feuilles : txt/ovr/role -> 0, enc -> 1
    A.add_rule("txt", (), 0)
    A.add_rule("enc", (), 1)
    A.add_rule("ovr", (), 0)
    A.add_rule("role", (), 0)
    
    # seq(x, y) -> min(2, x + y)
    for x in range(3):
        for y in range(3):
            result = min(2, x + y)
            A.add_rule("seq", (x, y), result)
    
    # frame(x) -> x
    for x in range(3):
        A.add_rule("frame", (x,), x)
    
    # sys(x) -> x
    for x in range(3):
        A.add_rule("sys", (x,), x)
    
    return A


def dangerous_and_double_encoded() -> TreeAutomaton:
    """Intersection de shield_automaton et enc_automaton."""
    from formlang.tree import product
    return product(shield_automaton(), enc_automaton())
