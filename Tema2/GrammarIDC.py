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
        g.VN = self.VN.copy()
        g.VT = self.VT.copy()
        g.S = self.S
        g.P = self.P.copy()

        g.VN = set()

        # pasul 1: elimina simbolurile neutilizabile

        V = []

        i = 0
        V0 = set()
        V.append(V0)

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

        # pasul 3: elimina redenumirile

        def has_derivation(A):
            for rule in g.P:
                if A in rule.right:
                    return True
            return False
        def is_rename(rule):
            return len(rule.right) == 1 and rule.right[0] in g.VN

        P = []
        R = set() # set that keeps all the renames

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
                    for rule in P[i-1]:
                        if rule.left == symbol:
                            new_rule = Production()
                            new_rule.left = rename.left
                            new_rule.right = rule.right
                            Pi.add(new_rule)

            if Pi == P[i - 1]:
                g.P = list(Pi)
                break
            P.append(Pi)

        return g

    def to_fng(self):
        # daca nu este IDC, nu se poate transforma
        if not self.is_idc():
            return None

        # daca nu exista nicio productie care sa aiba S in stanga, nu se poate transforma
        if not len([rule for rule in self.P if rule.left == self.S]) > 0:
            return None

        # TODO : FA mizeria asta ordinara

        # forma normala chomsky

        g = self.simplify()

        # void Grammar::ToFNG()
        # {
        # // luam pe rand fiecare neterminal din VN
        # std::vector < Production > Zprod;
        # char lastNonterminal = m_VN[m_VN.size() - 1];
        # for (int index = 0; index < m_VN.size(); index++)
        # {
        #   // luam fiecare neterminal-productie
        #   // avem doua cazuri, daca gasim o neterminal-productie care se duce
        #   for (int jndex = 0; jndex < m_P.size(); jndex++)
        #   {
        #       int Rang = m_VN.find(m_P[jndex].right[0]);
        #       //Caz 1: din neterminal in neterminal cu rang mai mic
        # 		//daca scoatem ultima conditie din if, face si pasul 3 in care modificam productiile [...]
        # 		//[...] care au in stanga Z, Z1 etc.
        #       if (Rang != std::string::npos & & Rang < index & & m_P[jndex].left[0] == m_VN[index] & & m_P[jndex].left[0] <= lastNonterminal)
        #       {
        #           std:: string nt;
        #           nt.push_back(m_P[jndex].right[0]);
        #           std::vector < int > indices;
        #           FindAllLeftSideProdIndices(nt, indices);
        #           //aici are loc inlocuirea productiilor (adaugare productii noi + stergere productie parcursa)
        #           for (auto k: indices)
        #           {
        #               Production newP;
        #               newP.left = m_P[jndex].left;
        #               newP.right = m_P[k].right + m_P[jndex].right.substr(1, m_P[jndex].right.size() - 1);
        #               m_P.push_back(newP);
        #           }
        #
        #           m_P.erase(m_P.begin() + jndex);
        #           jndex--;
        #       }
        #
        #       // Caz 2: din neterminal in neterminal cu rang egal
        #       if (Rang != std::string::npos & & Rang == index & &
        #           m_P[jndex].left[0] == m_VN[index] & &
        #           m_P[jndex].left[0] == m_P[jndex].right[0]
        #           )
        #       {
        #           std:: string nt;
        #           nt.push_back(m_P[jndex].right[0]);
        #           std::vector < int > indices;
        #           FindAllLeftSideProdIndicesT(nt, indices);
        #           std::string
        #           Z;
        #           Z.push_back(FindNewNonTerminal(m_VN));
        #           //aici are loc inlocuirea pentru al doilea caz
        #           Production newP;
        #           newP.left = Z;
        #           newP.right = m_P[jndex].right.substr(1, m_P[jndex].right.size() - 1) + Z;
        #           m_P.push_back(newP);
        #           Zprod.push_back(newP);
        #           newP.right = m_P[jndex].right.substr(1, m_P[jndex].right.size() - 1);
        #           m_P.push_back(newP);
        #           Zprod.push_back(newP);
        #           for (auto k: indices)
        #           {
        #               newP.left = m_P[jndex].left;
        #               newP.right = m_P[k].right + Z;
        #               m_P.push_back(newP);
        #               Zprod.push_back(newP);
        #           }
        #
        #           m_P.erase(m_P.begin() + jndex);
        #           jndex--;
        #       }
        #   }
        # }
        # // Pas 2 si 3
        # for (int index = 0; index < m_P.size(); index++)
        # {
        #   int ok = 0;
        #   char rightFirstPos = m_P[index].right[0];
        #   if (m_VN.find(rightFirstPos) != std::string::npos)
        #       for (int jndex = 0; jndex < m_P.size(); jndex++)
        #           if (m_P[jndex].left[0] == rightFirstPos)
        #           {
        #               ok = 1;
        #               Production newP;
        #               newP.left = m_P[index].left;
        #               newP.right = m_P[jndex].right + m_P[index].right.substr(1, m_P[index].right.size() - 1);
        #               m_P.push_back(newP);
        #           }
        #   if (ok == 1)
        #   {
        #       m_P.erase(m_P.begin() + index);
        #       index--;
        #   }
        # }
        # }

        # tradu in python
