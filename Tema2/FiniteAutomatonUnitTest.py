import unittest
from FiniteAutomaton import *

class MyTestCase(unittest.TestCase):

	def test_finite_automaton(self):

		finite_automaton = FiniteAutomaton()

		finite_automaton.Q = {"q0", "q1", "q2"}
		finite_automaton.sigma = {"a", "b"}
		finite_automaton.gama = {"Z0", "A"}
		finite_automaton.q0 = "q0"
		finite_automaton.Z0 = "Z0"
		finite_automaton.F = {"q2"}

		finite_automaton.delta = [Production(["q0", "a", "Z0"], ("q0", ["A", "Z0"]))]
		finite_automaton.delta.append(Production(["q0", "a", "A"], ("q0", ["A", "A"])))
		finite_automaton.delta.append(Production(["q0", "b", "A"], ("q1", [" "])))
		finite_automaton.delta.append(Production(["q1", "b", "A"], ("q1", [" "])))
		finite_automaton.delta.append(Production(["q1", " ", "Z0"], ("q2", ["Z0"])))

		self.assertTrue(finite_automaton.verify_automaton())
		self.assertTrue(finite_automaton.check_word("aaabbb"))








		finite_automaton.Q = {"q0", "q1"}
		finite_automaton.sigma = {"a", "b"}
		finite_automaton.gama = {"A", "Z0"}
		finite_automaton.q0 = "q0"
		finite_automaton.Z0 = "Z0"
		finite_automaton.F = {}

		finite_automaton.delta = [Production(["q0", "a", "Z0"], ("q0", ["A", "A", "Z0"]))]
		finite_automaton.delta.append(Production(["q0", "a", "A"], ("q0", ["A", "A", "A"])))
		finite_automaton.delta.append(Production(["q0", "b", "A"], ("q1", [" "])))
		finite_automaton.delta.append(Production(["q1", "b", "A"], ("q1", [" "])))
		finite_automaton.delta.append(Production(["q1", " ", "Z0"], ("q1", [" "])))

		self.assertFalse(finite_automaton.check_word("aabbbb"))



if __name__ == '__main__':
	unittest.main()
