from finite_automaton import FiniteAutomaton as Fa

def regex_to_finite_automaton(r):
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

	def forma_poloneza(text):
		FP = []
		OP = []

		for E in text:
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
					print("Parantezare invalida")
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
				print("Parantezare invalida")
				FP = []
				return FP
			FP.append(OP.pop())
		return FP

	fp = forma_poloneza(r)

	SA = []
	contor = 0

	for char in fp:
		if 'a' <= char <= 'z':
			C = Fa()

			C.q0 = "q" + str(contor)
			C.F.add("q" + str(contor + 1))
			C.Q.add(C.q0)
			C.Q.add(list(C.F)[-1])
			C.sigma.add(char)
			C.delta.add((C.q0, char, list(C.F)[-1]))

			contor += 2
			SA.append(C)

		elif char == '|':
			B = SA.pop()
			A = SA.pop()
			C = Fa()

			C.q0 = "q" + str(contor)

			C.F.add("q" + str(contor + 1))

			C.Q = A.Q | B.Q
			C.Q.add(C.q0)
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

			C = Fa()
			C.q0 = A.q0
			C.F.add(list(B.F)[-1])
			C.Q = A.Q | B.Q
			C.sigma = A.sigma | B.sigma
			C.delta = A.delta | B.delta

			SA.append(C)

		elif char == '*':
			A = SA.pop()
			C = Fa()

			C.q0 = "q" + str(contor)

			C.F.add("q" + str(contor + 1))

			C.Q = A.Q
			C.Q.add(C.q0)
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

	if len(SA) != 1:
		print("Eroare la conversie")
		exit(1)

	rezultat = SA.pop()

	elemente = dict()
	def lambda_inchidere(automat, stari):
		stari_lambda = set(stari)

		caracter_gasit = True
		while caracter_gasit:
			caracter_gasit = False
			for tranzitie in automat.delta:
				if tranzitie[0] in stari_lambda and tranzitie[1] == "λ":
					if tranzitie[2] not in stari_lambda:
						stari_lambda.add(tranzitie[2])
						caracter_gasit = True
		return stari_lambda

	elemente["q'0"] = lambda_inchidere(rezultat, [rezultat.q0])

	contor = 1

	i = 0
	gata = False

	def delta_prim(lambda_inchidere_set, automat, litera):
		delta_prim_set = set()
		for tranzitie in automat.delta:
			if tranzitie[0] in lambda_inchidere_set and tranzitie[1] == litera:
				delta_prim_set.add(tranzitie[2])
		return delta_prim_set

	while True:
		for char in sorted(rezultat.sigma - {"λ"}):
			delta = delta_prim(elemente["q'" + str(i)], rezultat, char)
			if delta != set() and lambda_inchidere(rezultat, delta) not in elemente.values():
				if "q'" + str(contor) not in elemente.keys():
					elemente["q'" + str(contor)] = lambda_inchidere(rezultat, delta)
					if rezultat.F.intersection(elemente["q'" + str(contor)]) != set():
						gata = True
					if not gata:
						contor += 1
		if i == contor and gata:
			break
		i += 1

	M = Fa()
	M.q0 = "q'0"
	M.Q = set(elemente.keys())
	M.F = {list(elemente.keys())[-1]}
	M.sigma = rezultat.sigma

	for key in elemente.keys():
		for litera in rezultat.sigma - {"λ"}:
			delta = delta_prim(elemente[key], rezultat, litera)
			for key2 in elemente.keys():
				if elemente[key2] == lambda_inchidere(rezultat, delta):
					M.delta.add((key, litera, key2))

	return M
