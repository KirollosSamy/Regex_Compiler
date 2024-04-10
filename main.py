from fsm import *
from regex import Regex
from regex_parser import RegexParser

def main():
    # fsm = FSM.from_json("json/fsm.json")
    # fsm.visualize("output/fsm", label='test')
    # fsm.to_json("json/out.json")
    
    regex_parser = RegexParser()
    regex = Regex("a(a|b)*b", regex_parser)
    NFA = regex_parser.regex_to_NFA("a&(a|b)*&b")
    NFA.visualize('output/simple_regex')
    NFA.to_json('json/NFA.json')

    # test epsilon closure
    for state in NFA._states.keys():
        temp = regex_parser.epsilon_closure(NFA, state)
        closure = [state.name for state in temp]
        print(f"for state {state.name} : " + ' '.join(closure))

if __name__ == "__main__":
    main()