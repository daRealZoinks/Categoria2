import unittest
from GrammarToAutomaton import *
import GrammarIDC

class MyTestCase(unittest.TestCase):

	def test_finite_automaton(self):
		finite_automaton = PushDownAutomaton.FiniteAutomaton()

		finite_automaton.Q = {"q0", "q1", "q2"}
		finite_automaton.sigma = {"a", "b"}
		finite_automaton.gama = {"Z0", "A"}
		finite_automaton.q0 = "q0"
		finite_automaton.Z0 = "Z0"
		finite_automaton.F = {"q2"}

		finite_automaton.delta = [PushDownAutomaton.Production(["q0", "a", "Z0"], ("q0", ["A", "Z0"]))]
		finite_automaton.delta.append(PushDownAutomaton.Production(["q0", "a", "A"], ("q0", ["A", "A"])))
		finite_automaton.delta.append(PushDownAutomaton.Production(["q0", "b", "A"], ("q1", [" "])))
		finite_automaton.delta.append(PushDownAutomaton.Production(["q1", "b", "A"], ("q1", [" "])))
		finite_automaton.delta.append(PushDownAutomaton.Production(["q1", " ", "Z0"], ("q2", ["Z0"])))

		self.assertTrue(finite_automaton.verify_automaton())
		self.assertTrue(finite_automaton.check_word("aaabbb"))
		self.assertTrue(finite_automaton.check_word("aaaaaaabbbbbbb"))
		self.assertFalse(finite_automaton.check_word("aaabbbb"))
		self.assertFalse(finite_automaton.check_word("aaabbbbbbb"))

	def test_grammar_to_automaton(self):

		grammar = GrammarIDC.Grammar()

		grammar.VN = {"S", "B"}
		grammar.VT = {"a", "b"}
		grammar.S = "S"

		production1 = GrammarIDC.Production()
		production1.left = "S"
		production1.right = ["a", "S", "B"]
		production2 = GrammarIDC.Production()
		production2.left = "S"
		production2.right = ["a", "B"]
		production3 = GrammarIDC.Production()
		production3.left = "B"
		production3.right = ["b"]

		grammar.P.append(production1)
		grammar.P.append(production2)
		grammar.P.append(production3)

		automaton = grammar_to_automaton(grammar)

		print(automaton)

		self.assertTrue(automaton.verify_automaton())
		self.assertTrue(automaton.check_word("abb"))
		self.assertTrue(automaton.check_word("abbbbbbb"))
		self.assertFalse(automaton.check_word("abbbb"))
		self.assertFalse(automaton.check_word("abbbbbbbb"))

		pass

if __name__ == '__main__':
	unittest.main()
