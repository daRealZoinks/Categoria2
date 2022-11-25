class DeterministicFiniteAutomaton:
	def __init__(self):
		self.Q = set()
		self.sigma = set()
		self.delta = set()
		self.q0 = str
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

	def print_automaton(self):
		print("Q: ", self.Q)
		print("sigma: ", self.sigma)
		print("delta:")
		for rule in self.delta:
			print("    delta(", rule[0], ",", rule[1], ") =", rule[2])
		print("q0: ", self.q0)
		print("F: ", self.F)

	def check_word(self, word):
		if not self.verify_automaton():
			print("ERROR: Automaton is not valid")
			return False

		states = list(self.q0)
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

	def __add__(self, other):
		nfa = {}

		nfa["states"] = []
		nfa["states"].extend(self["states"])
		nfa["states"].extend(other["states"])

		nfa["initial_state"] = self["initial_state"]
		nfa["final_states"] = other["final_states"]
		nfa["alphabets"] = list(set(self["alphabets"]) | set(other["alphabets"]))

		nfa["transition_function"] = {}
		for state in nfa["states"]:
			if state in self["states"]:
				nfa["transition_function"][state] = self["transition_function"][state]
			elif state in other["states"]:
				nfa["transition_function"][state] = other["transition_function"][state]

		# connect final states of nfa1 with start state of other using epsilon transition
		for state in self["final_states"]:
			nfa["transition_function"][state][Consts.EPSILON].append(
				other["initial_state"])

		return nfa

	def __mul__(self, other):
		nfa = {}

		nfa["states"] = [uuid.uuid4()]
		nfa["states"].extend(self["states"])
		nfa["states"].extend(other["states"])

		nfa["initial_state"] = nfa["states"][0]
		nfa["final_states"] = []
		nfa["final_states"].extend(self["final_states"])
		nfa["final_states"].extend(other["final_states"])
		nfa["alphabets"] = list(set(self["alphabets"]) | set(other["alphabets"]))

		nfa["transition_function"] = {}
		for state in nfa["states"]:
			if state in self["states"]:
				nfa["transition_function"][state] = self["transition_function"][state]
			elif state in other["states"]:
				nfa["transition_function"][state] = other["transition_function"][state]
			else:
				nfa["transition_function"][state] = {}
				for alphabet in nfa["alphabets"]:
					nfa["transition_function"][state][alphabet] = []

		# connecting start state to start state of nfa 1 and nfa 2 through epsilon move
		nfa["transition_function"][nfa["initial_state"]][Consts.EPSILON].extend(
			[self["initial_state"], other["initial_state"]])
		return nfa

	def __pow__(self, power, modulo=None):
		nfa = {}

		nfa["states"] = [uuid.uuid4()]
		nfa["states"].extend(self["states"])
		nfa["states"].append(uuid.uuid4())

		nfa["initial_state"] = nfa["states"][0]
		nfa["final_states"] = [nfa["states"][len(nfa["states"])-1]]
		nfa["alphabets"] = self["alphabets"]

		nfa["transition_function"] = {}
		for state in nfa["states"]:
			if state in self["states"]:
				nfa["transition_function"][state] = self["transition_function"][state]
			else:
				nfa["transition_function"][state] = {}
				for alphabet in nfa["alphabets"]:
					nfa["transition_function"][state][alphabet] = []

		# connecting start state to start state of nfa 1 through epsilon move
		nfa["transition_function"][nfa["initial_state"]
								   ][Consts.EPSILON].append(self["initial_state"])

		for final_state in self["final_states"]:
			# connecting final states of nfa1 to start state of nfa1 through epsilon move
			nfa["transition_function"][final_state][Consts.EPSILON].append(
				self["initial_state"])
			# connecting final states of nfa1 to final states of nfa through epsilon move
			nfa["transition_function"][final_state][Consts.EPSILON].extend(
				nfa["final_states"])

		# connecting start state to final state of nfa through epsilon move
		nfa["transition_function"][nfa["initial_state"]
								   ][Consts.EPSILON].extend(nfa["final_states"])
		return nfa
