"""Machine universelle. À COMPLÉTER : encode/decode et run.  -> Jour 4 (E4.2)."""
from __future__ import annotations
import json
from .turing import TuringMachine, TMResult


def encode(machine: "TuringMachine") -> str:
    """Encode une machine de Turing en JSON injectif."""
    # Créer des mappings pour les états et symboles
    all_states = {machine.start} | machine.accept | machine.reject
    all_symbols = {machine.blank}
    
    for (s, a), (ns, b, d) in machine.transitions.items():
        all_states.add(s)
        all_states.add(ns)
        all_symbols.add(a)
        all_symbols.add(b)
    
    state_list = sorted(all_states)
    symbol_list = sorted(all_symbols)
    
    state_map = {s: i for i, s in enumerate(state_list)}
    symbol_map = {a: i for i, a in enumerate(symbol_list)}
    
    # Créer la description
    desc = {
        "states": state_list,
        "symbols": symbol_list,
        "start": state_map[machine.start],
        "accept": sorted(state_map[s] for s in machine.accept),
        "reject": sorted(state_map[s] for s in machine.reject),
        "blank_idx": symbol_map[machine.blank],
        "transitions": []
    }
    
    # Ajouter les transitions en ordre trié pour l'injectivité
    for (s, a), (ns, b, d) in sorted(machine.transitions.items()):
        desc["transitions"].append([
            state_map[s],
            symbol_map[a],
            state_map[ns],
            symbol_map[b],
            d
        ])
    
    return json.dumps(desc, sort_keys=True, separators=(',', ':'))


def decode(desc: str) -> "TuringMachine":
    """Décode une machine depuis sa description JSON."""
    d = json.loads(desc)
    
    # Récupérer les mappings
    state_list = d["states"]
    symbol_list = d["symbols"]
    
    # Reconstruire les transitions
    transitions = {}
    for s_id, a_id, ns_id, b_id, d_dir in d["transitions"]:
        s = state_list[s_id]
        a = symbol_list[a_id]
        ns = state_list[ns_id]
        b = symbol_list[b_id]
        transitions[(s, a)] = (ns, b, d_dir)
    
    # Récupérer l'état initial et les états acceptants/rejetants
    start = state_list[d["start"]]
    accept = {state_list[i] for i in d["accept"]}
    reject = {state_list[i] for i in d["reject"]}
    blank = symbol_list[d["blank_idx"]]
    
    return TuringMachine(transitions, start, accept, blank=blank, reject=reject)


class UniversalTM:
    def run(self, encoded_machine: str, word: str, **kw) -> "TMResult":
        """Décode la machine encodée et la simule sur le mot."""
        machine = decode(encoded_machine)
        return machine.run(word, **kw)
