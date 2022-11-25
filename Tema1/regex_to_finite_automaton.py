from DeterministicFiniteAutomaton import DeterministicFiniteAutomaton as DFA


def regex_to_finite_automaton(r: str) -> DFA:
	automat = DFA()

	# TODO : Obtinerea unui automat Mλ cu λ tranzitii corespunzator expresiei regulate

	fp = forma_poloneza(r)

	SA = []
	contor = 0

	A = DFA()
	B = DFA()
	C = DFA()

	for char in fp:
		if 'a' <= char <= 'c':
			C = DFA()
			C.Q.add("q" + str(contor))
			C.Q.add("q" + str(contor + 1))
			C.sigma.add(char)
			C.delta.add(("q" + str(contor), char, "q" + str(contor + 1)))
			C.q0 = "q" + str(contor)
			C.F.add("q" + str(contor + 1))
			SA.append(C)
			contor += 2
		elif char == '|':
			B = SA.pop()
			A = SA.pop()
			C = DFA()

			C.Q.add("q" + str(contor))
			C.q0 = "q" + str(contor)
			C.Q.add("q" + str(contor + 1))
			C.F.add("q" + str(contor + 1))

			C.sigma.add("λ")

			C.delta.add(("q" + str(contor), "λ", A.q0))
			C.delta.add(("q" + str(contor), "λ", B.q0))
			C.delta.add((A.F.pop(), "λ", "q" + str(contor + 1)))
			C.delta.add((B.F.pop(), "λ", "q" + str(contor + 1)))

			contor += 2
			SA.append(C)
		elif char == '.':
			B = SA.pop()
			A = SA.pop()

			C = DFA()

			C.q0 = A.q0
			C.F.add(B.F.pop())

			C.Q = C.q0 | C.F
			C.sigma = A.sigma | B.sigma

			SA.append(C)
		elif char == '*':
			A = SA.pop()
			C = A**2
			contor += 2
			SA.append(C)
	if len(SA) == 1:
		return SA.pop()

	# TODO : Obtinerea unui automat finit determinist M echivalent cu Mλ obtinut la punctul anterior

	return SA[-1]


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
