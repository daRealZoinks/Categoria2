import random


class Grammar:
    def __init__(self):
        self.VN = set()
        self.VT = set()
        self.S = None
        self.P = []

    def verify_grammar(self):
        # elementele din VN nu apartin lui VT
        for symbol_n in self.VN:
            for symbol_t in self.VT:
                if symbol_n == symbol_t:
                    return False

        # S nu se afla in VN
        if self.S not in self.VN:
            return False

        # pt fiecare productie, partea stanga contine cel putin un element din VN
        for rule in self.P:
            if rule[0] not in self.VN:
                return False

        # exista cel putin o productie care sa-l aiba pe S in stanga
        rule_containing_S = len([rule for rule in self.P if rule[0] == self.S]) > 0
        if not rule_containing_S:
            return False

        # toate productiile au cel putin un element din VN si VT
        for rule in self.P:
            for symbol in rule[1]:
                if symbol not in self.VT and symbol not in self.VN:
                    return False

        return True

    def is_regular(self):
        for rule in self.P:
            if len(rule[1]) > 2:
                return False

        for rule in self.P:
            if rule[1][0] not in self.VT:
                return False
            if len(rule[1]) == 2:
                if rule[1][1] not in self.VN:
                    return False

        return True

    def generate_word(self):
        word = self.S
        print(self.S, end=" ")
        while True:
            applicable_rules = [rule for rule in self.P if rule[0] in word]
            if len(applicable_rules) == 0:
                print()
                return word
            chosen_rule = random.choice(applicable_rules)
            if chosen_rule[0] in word:
                word = word.replace(chosen_rule[0], chosen_rule[1], 1)
                print(" -> ", word, end=" ")

    def print_grammar(self):
        print("VN: ", self.VN)
        print("VT: ", self.VT)
        print("S: ", self.S)
        print("P:")
        for rule in self.P:
            print("    ", rule[0], " -> ", rule[1])

    def read_grammar(self, file_name):
        file = open(file_name, "r")

        self.VN = set(file.readline().split())
        self.VT = set(file.readline().split())
        self.S = file.readline().strip()
        file.readline()

        for line in file:
            self.P.append(tuple(line.strip().split(" -> ")))

        file.close()
