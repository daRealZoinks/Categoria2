import re
from regex_to_finite_automaton import regex_to_finite_automaton as R2FA
from DeterministicFiniteAutomaton import DeterministicFiniteAutomaton as DFA
def main():
    a:DFA = R2FA("^The.*Spain$")
    a.print_automaton()


if __name__ == '__main__':
    main()
