import GrammarIDC
import PushDownAutomaton


def grammar_to_automaton(g: GrammarIDC.Grammar):
    # g = g.to_fng()
    m = PushDownAutomaton.FiniteAutomaton()
    m.Q = set()
    m.Q.add("q0")
    m.sigma = g.VT
    m.gama = g.VN
    m.q0 = "q0"
    m.Z0 = g.S
    m.F = set()
    m.delta = list()

    p: GrammarIDC.Production
    for p in g.P:
        production = PushDownAutomaton.Production(["q0", p.right[0], p.left], ("q0", p.right[1:] if len(p.right) > 1 else [" "]))
        m.delta.append(production)

    return m
