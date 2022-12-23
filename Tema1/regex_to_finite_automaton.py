from deterministic_finite_automaton import DeterministicFiniteAutomaton as Dfa


def regex_to_finite_automaton(r):
	fp = forma_poloneza(r)

	SA = []
	contor = 0

	for char in fp:
		if 'a' <= char <= 'z':
			C = Dfa()

			C.q0 = "q" + str(contor)
			C.F.add("q" + str(contor+ 1))
			C.Q.add(C.q0)
			C.Q.add(list(C.F)[-1])
			C.sigma.add(char)
			C.delta.add((C.q0, char, list(C.F)[-1]))

			contor += 2
			SA.append(C)

		elif char == '|':
			B = SA.pop()
			A = SA.pop()
			C = Dfa()

			C.q0 = "q" + str(contor)
			C.Q = A.Q | B.Q
			C.Q.add(C.q0)
			C.F.add("q" + str(contor + 1))
			C.Q.add(list(C.F)[-1])
			C.Q.update({A.q0, B.q0, list(A.F)[-1], list(B.F)[-1]})
			C.sigma = A.sigma | B.sigma
			C.sigma.add("λ")
			C.delta = A.delta | B.delta
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

			C.q0 = "q" + str(contor)
			C.Q = A.Q
			C.Q.add(C.q0)
			C.F.add("q" + str(contor + 1))
			C.Q.add(list(C.F)[-1])
			C.Q.update({A.q0, list(A.F)[-1]})
			C.sigma = A.sigma | {"λ"}
			C.delta = A.delta
			C.delta.add((C.q0, "λ", A.q0))
			C.delta.add((list(A.F)[-1], "λ", list(C.F)[-1]))
			C.delta.add((C.q0, "λ", list(C.F)[-1]))
			C.delta.add((list(A.F)[-1], "λ", A.q0))

			contor += 2
			SA.append(C)

	if len(SA) == 1:
		SA.pop().print_automaton()
	else:
		print("OROARE")

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
