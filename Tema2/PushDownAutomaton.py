class Production:
	def __init__(self, left: list, right: tuple[str, list[str]]):
		self.left = left
		self.right = right

	def __str__(self):
		return str(self.left) + " -> " + str(self.right)


class FiniteAutomaton:
	def __init__(self):
		self.Q = set()
		self.sigma = set()
		self.gama = set()
		self.q0 = str
		self.Z0 = str
		self.F = set()
		self.delta = list()

	def __str__(self):
		result = ""
		result += "Q: " + str(self.Q) + "\n"
		result += "sigma: " + str(self.sigma) + "\n"
		result += "gama: " + str(self.gama) + "\n"
		result += "q0: " + str(self.q0) + "\n"
		result += "Z0: " + str(self.Z0) + "\n"
		result += "F: " + str(self.F) + "\n"
		result += "delta:\n"
		for transition in self.delta:
			result += str(transition) + "\n"
		return result

	def verify_automaton(self):
		if len(self.Q) == 0:
			print("ERROR: Q e gol")
			return False

		if len(self.sigma) == 0:
			print("ERROR: sigma e gol")
			return False

		if len(self.gama) == 0:
			print("ERROR: gama e gol")
			return False

		if self.q0 not in self.Q:
			print("ERROR: q0 nu e in Q")
			return False

		if self.Z0 not in self.gama:
			print("ERROR: Z0 nu e in gama")
			return False

		if not self.F.issubset(self.Q):
			print("ERROR: F nu e inclus in Q")
			return False

		return True

	def check_word(self, word):
		if not self.verify_automaton():
			print("ERROR: Automatul nu e valid")
			return False

		word = word + " "

		state = self.q0
		stack = [self.Z0]

		# psuhdown automaton
		for symbol in word:
			# transition is a Production
			transitions = [transition for transition in self.delta if
						   transition.left[0] == state and transition.left[1] == symbol and transition.left[2] == stack[
							   -1]]
			if len(transitions) == 0:
				return False

			transition = transitions[0]
			state = transition.right[0]
			stack.pop()
			for symbol in transition.right[1]:
				stack.append(symbol)

		#     check if F is empty or not
		if len(self.F) == 0:
			return True

		return state in self.F

	def is_deterministic(self):
		for state in self.Q:
			for symbol in self.sigma:
				transitions = [transition for transition in self.delta if
							   transition[0] == state and transition[1] == symbol]
				if len(transitions) > 1:
					return False

		# pt fiecare q din Q si Z din gama, daca delta(q, lambda, Z) = multime vida atunci delta(q, a, Z) = multimea vida pt orice a din gama
		for state in self.Q:
			for symbol in self.gama:
				if len([transition for transition in self.delta if
						transition[0] == state and transition[1] == symbol]) == 0:
					for symbol2 in self.gama:
						if len([transition for transition in self.delta if
								transition[0] == state and transition[1] == symbol2]) != 0:
							return False

		return True
