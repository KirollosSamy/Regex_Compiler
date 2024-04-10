from fsm import FSM
from regex import Regex
from regex_parser import RegexParser
from preprocessor import RegexPreprocessor

def main():
    regex_parser = RegexParser()
    # regex = Regex("a(a|b)*b", regex_parser)
    preprocessed_regex = RegexPreprocessor.preprocess("[a-z]")
    NFA = regex_parser.regex_to_NFA(preprocessed_regex)
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