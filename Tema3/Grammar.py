class Grammar:
    def __init__(self):
        self.nonterminals = []
        self.terminals = []
        self.rules = []
        self.start = None

    def print(self):
        print("Nonterminals: ", self.nonterminals)
        print("Terminals: ", self.terminals)
        print("Rules: ", self.rules)
        print("Start: ", self.start)