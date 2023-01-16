import random

class Production:
	def __init__(self):
		self.left = str
		self.right = list[str]

	def __str__(self):
		return str(self.left) + " -> " + str(''.join(self.right))

	def __eq__(self, other):
		return self.left == other.left and self.right == other.right

	def __hash__(self):
		return hash(str(self))

	def __lt__(self, other):
		if self.left == other.left:
			return self.right < other.right
		return self.left < other.left

class Grammar:
	def __init__(self):
		self.VN = set()
		self.VT = set()
		self.S = str()
		self.P = list()

	def __str__(self):
		result = ""
		result += "VN: " + str(self.VN) + "\n"
		result += "VT: " + str(self.VT) + "\n"
		result += "S: " + str(self.S) + "\n"
		result += "P:\n"
		self.P.sort()
		for rule in self.P:
			result += str(rule) + "\n"
		return result

	def verify_grammar(self):
		# elementele din VN nu apartin lui VT
		if self.VN.intersection(self.VT) != set():
			return False

		# S nu se afla in VN
		if self.S not in self.VN:
			return False

		# pt fiecare productie, partea stanga contine cel putin un element din VN
		for rule in self.P:
			if rule.left not in self.VN:
				return False

		# exista cel putin o productie care sa-l aiba pe S in stanga
		if len([rule for rule in self.P if rule.left == self.S]) == 0:
			return False

		# toate productiile au cel putin un element din VN si VT
		for rule in self.P:
			for symbol in rule.right:
				if symbol not in self.VN.union(self.VT):
					return False

		return True

	def is_regular(self):
		for rule in self.P:
			if len(rule.right) > 2:
				return False

		for rule in self.P:
			if rule.right[0] not in self.VT:
				return False
			if len(rule.right) == 2:
				if rule.right[1] not in self.VN:
					return False

		return True

	def generate_word(self):
		word = self.S
		print(self.S, end=" ")
		while True:
			applicable_rules = [rule for rule in self.P if rule.left in word]
			if len(applicable_rules) == 0:
				print()
				return word
			chosen_rule = random.choice(applicable_rules)
			if chosen_rule.left in word:
				word = word.replace(chosen_rule.left, "".join(chosen_rule.right), 1)
				print(" -> ", word, end=" ")

	def read_grammar(self, file_name):
		file = open(file_name, "r")

		self.VN = set(file.readline().split())
		self.VT = set(file.readline().split())
		self.S = file.readline().strip()
		file.readline()

		for line in file:
			left = line.split("->")[0].strip()
			right = list(line.split("->")[1].strip())
			rule = Production()
			rule.left = left
			rule.right = right
			self.P.append(rule)

		file.close()

	def is_idc(self):
		for rule in self.P:
			if rule.left not in self.VN:
				return False
			for symbol in rule.right:
				if symbol not in self.VN and symbol not in self.VT:
					return False

		return True

	def simplify(self):
		# daca nu este IDC, nu se poate simplifica
		if not self.is_idc():
			return None

		# daca nu exista nicio productie care sa aiba S in stanga, nu se poate simplifica
		if not len([rule for rule in self.P if rule.left == self.S]) > 0:
			return None

		g = Grammar()
		g.VN = set()
		g.VT = self.VT.copy()
		g.S = self.S
		g.P = self.P.copy()


		# pasul 1: elimina simbolurile neutilizabile

		V = []

		i = 0
		V.append(set())

		while True:
			i = i + 1

			valid_symbols = set()
			for rule in g.P:
				valid = True
				for letter in rule.right:
					if letter not in V[i - 1].union(g.VT):
						valid = False
				if valid:
					valid_symbols.add(rule.left)

			Vi = V[i - 1].union(valid_symbols)
			V.append(Vi)

			if V[i] == V[i-1]:
				g.VN = Vi
				break

		newP = []
		for rule in g.P:
			if rule.left in g.VN:
				valid = True
				for letter in rule.right:
					if letter not in g.VN.union(g.VT):
						valid = False
				if valid:
					newP.append(rule)

		g.P = newP


		# pasul 2: elimina simbolurile inaccesibile

		V = []

		i = 0
		V0 = set()
		V0.add(g.S)
		V.append(V0)

		while True:
			i = i+1

			valid_symbols = set()
			for rule in g.P:
				if rule.left in V[i - 1]:
					for A in g.VN:
						if A in rule.right:
							valid_symbols.add(A)

			Vi = V[i-1].union(valid_symbols)
			V.append(Vi)

			if V[i] == V[i-1]:
				g.VN = Vi
				break

		newP = []
		for rule in g.P:
			if rule.left in g.VN:
				newP.append(rule)

		g.P = newP

		return g

	def to_fng(self):
		g = self.simplify()

		# pasul 3: elimina redenumirile

		def has_derivation(A):
			for rule in g.P:
				if A in rule.right:
					return True
			return False

		def is_rename(rule):
			return len(rule.right) == 1 and rule.right[0] in g.VN

		P = []
		R = set()  # set that keeps all the renames

		i = 0
		P0 = set()

		for rule in g.P:
			if not is_rename(rule):
				P0.add(rule)
			else:
				R.add(rule)

		P.append(P0)
		while True:
			i = i + 1
			Pi = P[i - 1].copy()

			# for rename in R:
			for rename in R:
				for symbol in rename.right:
					for rule in P[i - 1]:
						if rule.left == symbol:
							new_rule = Production()
							new_rule.left = rename.left
							new_rule.right = rule.right
							Pi.add(new_rule)

			if Pi == P[i - 1]:
				g.P = list(Pi)
				break
			P.append(Pi)

		# transformam in forma normala chomsky
		contor = 1
		for rule in g.P:
			if len(rule.right) >= 2:
				if rule.right[-1] in g.VT:
					new_rule = Production()
					new_rule.left = rule.left
					new_rule.right = rule.right[:-1] + [str("A" + str(contor))]

					new_rule2 = Production()
					new_rule2.left = "A" + str(contor)
					new_rule2.right = [rule.right[-1]]
					g.P.append(new_rule2)

					g.VN.add("A" + str(contor))
					contor += 1
					g.P.remove(rule)
					g.P.append(new_rule)

		contor = 1
		for rule in g.P:
			if len(rule.right) > 2:
				if rule.right[-1] in g.VN and rule.right[-2] in g.VN:
					new_rule = Production()
					new_rule.left = rule.left
					new_rule.right = rule.right[:-2] + [str("D" + str(contor))]

					new_rule2 = Production()
					new_rule2.left = "D" + str(contor)
					new_rule2.right = [rule.right[-2], rule.right[-1]]
					g.P.append(new_rule2)

					contor += 1
					g.P.remove(rule)
					g.P.append(new_rule)

		contor = 1

		for rule in g.P:
			# dilema 1
			if rule.right[0] in g.VT and rule.right[-1] in g.VT:
				new_rule = Production()
				new_rule.left = rule.left
				new_rule.right = [str("B" + str(contor)), rule.right[-1]]

				new_rule2 = Production()
				new_rule2.left = "B" + str(contor)
				new_rule2.right = [rule.right[0]]
				g.P.append(new_rule2)

				contor += 1
				g.P.remove(rule)
				g.P.append(new_rule)




			# dilema 2
			if rule.left == rule.right[0]:
				a_reguli = list()
				for rule2 in g.P:
					if rule2.left == rule.left and rule2 != rule:
						a_reguli.append(rule2)
				if len(a_reguli) > 0:
					for rule2 in a_reguli:
						print(rule2.left + "-regulile " + str(rule2))
						new_rule = Production()
						new_rule.left = rule2.left
						new_rule.right = rule2.right + [str("Z"+str(contor))]
						g.P.append(new_rule)
						g.VN.add("Z"+str(contor))
					new_rule = Production()
					new_rule.left = "Z"+str(contor)
					new_rule.right = [rule.left]
					g.P.append(new_rule)

					new_rule = Production()
					new_rule.left = "Z" + str(contor)
					new_rule.right = [rule.left] + [str("Z" + str(contor))]
					g.P.append(new_rule)

					contor += 1
		print(g)

		exit()

		return g
