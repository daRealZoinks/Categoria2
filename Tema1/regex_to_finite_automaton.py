from deterministic_finite_automaton import DeterministicFiniteAutomaton as Dfa


def regex_to_finite_automaton(r):
	# TODO : Obtinerea unui automat Mλ cu λ tranzitii corespunzator expresiei regulate

	fp = forma_poloneza(r)

	SA = []
	contor = 0

	for char in fp:
		if 'a' <= char <= 'c':
			C = Dfa()
			C.Q.add(contor)
			C.Q.add(contor + 1)
			C.sigma.add(char)
			C.delta.add((contor, char, contor + 1))
			C.q0 = contor
			C.F.add(contor + 1)
			SA.append(C)
			contor += 2
		elif char == '|':
			B = SA.pop()
			A = SA.pop()
			C = Dfa()
			C.q0 = contor
			C.Q.add(C.q0)
			C.F.add(contor + 1)
			C.Q.add(list(C.F)[-1])
			C.sigma.add("λ")
			C.delta.add((C.q0, "λ", A.q0))
			C.delta.add((C.q0, "λ", B.q0))
			C.delta.add((list(A.F)[-1], "λ", list(C.F)[-1]))
			C.delta.add((list(B.F)[-1], "λ", list(C.F)[-1]))
			contor += 2
			SA.append(C)
		elif char == '.':
			B = SA.pop()
			A = SA.pop()
			for transition in A.delta:
				if transition[2] == list(A.F)[-1]:
					new_transition = (transition[0], transition[1], B.q0)
					A.delta.remove(transition)
					A.delta.add(new_transition)
			for automaton in SA:
				for transition in automaton.delta:
					if transition[0] == list(A.F)[-1]:
						new_transition = (B.q0, transition[1], transition[2])
						automaton.delta.remove(transition)
						automaton.delta.add(new_transition)
					if transition[2] == list(A.F)[-1]:
						new_transition = (transition[0], transition[1], B.q0)
						automaton.delta.remove(transition)
						automaton.delta.add(new_transition)
			A.Q.remove(list(A.F)[-1])
			A.F = {B.q0}
			A.Q.add(list(A.F)[-1])

			C = Dfa()
			C.q0 = A.q0
			C.F.add(list(B.F)[-1])
			C.Q = A.Q | B.Q
			C.sigma = A.sigma | B.sigma
			C.delta = A.delta | B.delta
			SA.append(C)
		elif char == '*':
			A = SA.pop()
			C = Dfa()
			C.q0 = contor
			C.Q.add(C.q0)
			C.F.add(contor + 1)
			C.Q.add(list(C.F)[-1])
			C.Q.update(A.Q)
			C.sigma = A.sigma | {"λ"}
			C.delta.add((C.q0, "λ", A.q0))
			C.delta.add((list(A.F)[-1], "λ", list(C.F)[-1]))
			C.delta.add((C.q0, "λ", list(C.F)[-1]))
			C.delta.add((list(A.F)[-1], "λ", A.q0))
			contor += 2
			SA.append(C)
	if len(SA) == 1:
		SA.pop().print_automaton()

	# TODO : Obtinerea unui automat finit determinist M echivalent cu Mλ obtinut la punctul anterior


def prec(c):
	if c == '|':
		return 1
	elif c == '.':
		return 2
	elif c == '*':
		return 3
	elif c == '(':
		return 0
	elif c == ')':
		return 0
	else:
		return 4


def forma_poloneza(sir):
	FP = []
	OP = []

	for E in sir:
		if E == ' ' or E == '\t':
			continue
		if 'a' <= E <= 'c':
			FP.append(E)
		elif E == '(':
			OP.append(E)
		elif E == ')':
			while OP[-1] != '(':
				FP.append(OP.pop())
			if len(OP) == 0:
				print("Parantezare incorecta")
				FP = []
				return FP
			OP.pop()
		elif E == '*' or E == '.' or E == '|':
			while not len(OP) == 0 and OP[-1] != '(' and prec(OP[-1]) >= prec(E):
				FP.append(OP.pop())
			OP.append(E)
		else:
			print("Caracter invalid")
			FP = []
			return FP
	while not len(OP) == 0:
		if OP[-1] == '(':
			print("Parantezare incorecta")
			FP = []
			return FP
		FP.append(OP.pop())
	return FP
