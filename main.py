from fsm import FSM
from regex import Regex
from regex_parser import RegexParser

def main():
    
    regex_parser = RegexParser()
    regex = regex_parser.preprocess("a+b")
    NFA = regex_parser.regex_to_NFA(regex)
    NFA.visualize('output/NFA')
    NFA.to_json('json/NFA.json')

    # test NFA to DFA
    DFA = regex_parser.NFA_to_DFA(NFA)
    DFA.visualize('output/DFA')

    # test DFA minimization
    DFA = regex_parser.minimize_DFA(DFA)
    DFA.visualize('output/minimized_DFA')
    

if __name__ == "__main__":
    main()