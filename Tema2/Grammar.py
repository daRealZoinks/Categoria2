import random

class Production:
    def __init__(self, argument, rezultate):
        self.argument = argument
        self.rezultate = rezultate

    def __str__(self):
        return str(self.argument) + " -> " + str(self.rezultate)

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
            if rule.argument not in self.VN:
                return False

        # exista cel putin o productie care sa-l aiba pe S in stanga
        if len([rule for rule in self.P if rule.argument == self.S]) == 0:
            return False

        # toate productiile au cel putin un element din VN si VT
        for rule in self.P:
            for symbol in rule.rezultate:
                if symbol not in self.VN.union(self.VT):
                    return False

        return True

    def is_regular(self):
        for rule in self.P:
            if len(rule.rezultate) > 2:
                return False

        for rule in self.P:
            if rule.rezultate[0] not in self.VT:
                return False
            if len(rule.rezultate) == 2:
                if rule.rezultate[1] not in self.VN:
                    return False

        return True

    def generate_word(self):
        word = self.S
        print(self.S, end=" ")
        while True:
            applicable_rules = [rule for rule in self.P if rule.argument in word]
            if len(applicable_rules) == 0:
                print()
                return word
            chosen_rule = random.choice(applicable_rules)
            if chosen_rule.argument in word:
                word = word.replace(chosen_rule.argument, "".join(chosen_rule.rezultate), 1)
                print(" -> ", word, end=" ")

    def read_grammar(self, file_name):
        file = open(file_name, "r")

        self.VN = set(file.readline().split())
        self.VT = set(file.readline().split())
        self.S = file.readline().strip()
        file.readline()

        for line in file:
            argument = line.split("->")[0].strip()
            result = list(line.split("->")[1].strip())
            self.P.append(Production(argument, result))

        file.close()

    def is_idc(self):
        for rule in self.P:
            if rule.argument not in self.VN:
                return False
            for symbol in rule.rezultate:
                if symbol not in self.VN and symbol not in self.VT:
                    return False

        return True

    def simplify(self):

        g = None

        # daca nu este IDC, nu se poate simplifica
        if not self.is_idc():
            return g

        # daca nu exista nicio productie care sa aiba S in stanga, nu se poate simplifica
        if not len([rule for rule in self.P if rule.argument == self.S]) > 0:
            return g

        g = Grammar()
        g.VN = self.VN.copy()
        g.VT = self.VT.copy()
        g.S = self.S
        g.P = self.P.copy()

        g.VN = set()

        # TODO : elimina simbolurile neutilizabile

        V = []

        i = 0
        V0 = set()
        V.append(V0)

        while True:
            i = i + 1

            valid_symbols = set()
            for tpl in g.P:
                if tpl[1] in V[i-1].union(g.VT):
                    valid_symbols.add(tpl[0])

            Vi = V[i - 1].union(valid_symbols)
            V.append(Vi)

            if V[i] == V[i-1]:
                g.VN = Vi
                break

        newP = []
        for tpl in g.P:
            if tpl[0] in g.VN:
                newP.append(tpl)

        g.P = newP

        # TODO : elimina simbolurile inaccesibile

        V = []

        i = 0
        V0 = set()
        V0.add(g.S)
        V.append(V0)

        while True:
            i = i+1

            valid_symbols = set()
            for tpl in g.P:
                if tpl[0] in V[i-1]:
                    for A in g.VN:
                        if A in tpl[1]:
                            valid_symbols.add(A)

            Vi = V[i-1].union(valid_symbols)
            V.append(Vi)

            if V[i] == V[i-1]:
                g.VN = Vi
                break

        newP = []
        for tpl in g.P:
            if tpl[0] in g.VN:
                newP.append(tpl)

        g.P = newP

        # TODO : elimina redenumirile

        P = []
        R = set()

        i = 0
        P0 = set()

        for tpl in g.P:
            if tpl[1] not in g.VN:
                P0.add(tpl)
            else:
                R.add(tpl)

        while True:
            i=i+1

            if P[i] == P[i-1]:
                g.P = P[i]
                break

        return g

    def to_fng(self):
        # daca nu este IDC, nu se poate transforma in FNG
        if not self.is_idc():
            return False

        pass