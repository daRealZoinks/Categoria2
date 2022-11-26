from Grammar import Grammar
from FiniteAutomaton import FiniteAutomaton


def grammar_to_automaton(g: Grammar) -> FiniteAutomaton | None:
    if not g.is_regular():
        return None

    m = FiniteAutomaton()

    m.Q = g.VN
    m.Q.add("T")
    m.q0 = g.S
    m.sigma = g.VT

    m.F = ["T"]
    if "λ" in g.VN or "λ" in g.VT:
        m.F.append("S")

    for rule in g.P:
        for symbol in rule[1]:
            if len(rule[1]) == 1:
                m.delta.add((rule[0], symbol, "T"))
            else:
                m.delta.add((rule[0], rule[1][0], rule[1][1]))

    return m
