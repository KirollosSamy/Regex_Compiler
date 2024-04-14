from fsm import FSM
from regex import Regex
from regex_parser import RegexParser
from preprocessor import RegexPreprocessor

def main():
    while True:
        regex_parser = RegexParser()
        regex = input("Enter regex: ")
        preprocessed_regex = RegexPreprocessor.preprocess(regex)
        NFA = regex_parser.regex_to_NFA(preprocessed_regex)
        NFA.visualize('output/NFA_'+ regex)
        NFA.to_json('json/NFA.json')

        # test NFA to DFA
        DFA = regex_parser.NFA_to_DFA(NFA)
        DFA.visualize('output/DFA_'+ regex)

        # test DFA minimization
        DFA = regex_parser.minimize_DFA(DFA)
        DFA.visualize('output/minimized_DFA_'+ regex)
    
    # (a|b)*[ab]? fails
    # (a+a+)+b fails
    # [bc]*(cd)+ fails


if __name__ == "__main__":
    main()