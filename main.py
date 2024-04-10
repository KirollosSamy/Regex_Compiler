from fsm import FSM
from regex import Regex
from regex_parser import RegexParser

def main():
    
    regex_parser = RegexParser()
    regex = regex_parser.preprocess("(a|b)*")
    NFA = regex_parser.regex_to_NFA(regex)
    NFA.visualize('output/simple_regex')
    NFA.to_json('json/NFA.json')

    # test epsilon closure
    for state in NFA._states.keys():
        temp = regex_parser.epsilon_closure(NFA, state)
        closure = [state.name for state in temp]
        print(f"for state {state.name} : " + ' '.join(closure))

    # test NFA to DFA
    DFA = regex_parser.NFA_to_DFA(NFA)
    DFA.visualize('output/simple_regex_DFA')

if __name__ == "__main__":
    main()