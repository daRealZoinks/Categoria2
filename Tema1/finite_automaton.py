class FiniteAutomaton:
	def __init__(self):
		self.Q = set()
		self.sigma = set()
		self.delta = set()
		self.q0 = None
		self.F = set()

	def verify_automaton(self):
		if len(self.Q) == 0:
			print("ERROR: Q is empty")
			return False

		if len(self.sigma) == 0:
			print("ERROR: sigma is empty")
			return False

		if self.q0 not in self.Q:
			print("ERROR: q0 does not exist in Q")
			return False

		for state in self.F:
			if state not in self.Q:
				print("ERROR: F is not in Q")
				return False

		for transition in self.delta:
			if transition[0] not in self.Q or transition[1] not in self.sigma or transition[2] not in self.Q:
				print("ERROR: delta is not a function from Q x sigma to Q")
				return False

		return True

	def __str__(self):
		result = str()
		result += "Q: " + str(self.Q) + "\n"
		result += "sigma: " + str(self.sigma) + "\n"
		result += "delta:\n"
		for rule in self.delta:
			result += "    delta(" + str(rule[0]) + "," + str(rule[1]) + ") = " + str(rule[2]) + "\n"
		result += "q0: " + str(self.q0) + "\n"
		result += "F: " + str(self.F) + "\n"
		return result

	def check_word(self, word):
		if not self.verify_automaton():
			print("ERROR: Automaton is not valid")
			return False

		states = set()
		states.add(self.q0)
		for symbol in word:
			new_states = list()
			for state in states:
				for transition in self.delta:
					if transition[0] == state and transition[1] == symbol:
						new_states.append(transition[2])
			states = new_states

		for state in states:
			if state in self.F:
				return True

		return False

	def is_deterministic(self):
		for transition in self.delta:
			for transition2 in self.delta:
				if transition[0] == transition2[0] and \
						transition[1] == transition2[1] and \
						transition[2] != transition2[2]:
					return False
		return True
