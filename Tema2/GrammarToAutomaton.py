import GrammarIDC
import PushDownAutomaton


def grammar_to_automaton(g: GrammarIDC.Grammar):
	g = g.to_fng()

	m = PushDownAutomaton.FiniteAutomaton()
	m.Q = set()
	m.Q.add("q0")
	m.sigma = g.VT
	m.gama = g.VN
	m.q0 = "q0"
	m.Z0 = g.S
	m.F = set()
	m.delta = list()

	for grammar_production in g.P:
		if (len(grammar_production.right) == 1):
			m.delta.append(PushDownAutomaton.Production(["q0", grammar_production.right[0], grammar_production.left],
														("q0", [" "])))
		else:
			m.delta.append(PushDownAutomaton.Production(["q0", grammar_production.right[0], grammar_production.left],
														("q0", [grammar_production.right[1:]])))

	return m
