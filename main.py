from fsm import FSM
from regex import Regex
from regex_parser import RegexParser

def main():
    fsm = FSM.from_json("json/test1.json")
    fsm.visualize("output/fsm")
    
    regex_parser = RegexParser()

    for state in fsm._states:
        epsilon_closure = regex_parser.epsilon_closure(fsm,state)
        print(f'state : {state} has epsilon closure : {epsilon_closure}')


    print(regex_parser.NFA_to_DFA(fsm))

    

if __name__ == "__main__":
    main()