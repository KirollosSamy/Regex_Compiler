from fsm import FSM,DFA, State, Action
from shunting_yard import ShuntingYard
from typing import Set, Dict
from utils import list_to_string

class RegexParser:
    def parse(self, regex: str) -> FSM:
        regex = self.preprocess(regex)
        NFA = self.regex_to_NFA(regex)
        DFA = self.NFA_to_DFA(NFA)
        DFA_min = self.minmize_DFA(DFA)
        return DFA_min
        
    def preprocess(self, regex: str) -> str:
        pass
    
    def regex_to_NFA(self, regex: str) -> FSM:
        operators = {'*':0, '+':0, '?':0, '&': 1, '|': 2}
        shunting_yard = ShuntingYard(operators)
        postfix = shunting_yard.parse(regex)
        print(postfix)
    
    def NFA_to_DFA(self, NFA: FSM) -> FSM:
        pass

        


    def epsilon_closure(self, nfa: FSM,s: State) -> Set[State]:
        print(f'epsilon closure of state {s}')
        eps = {s}
        new_states = True

        while new_states:
            new_states = False
            for state in eps.copy():
                for action, next_state in nfa.get_transitions(state).items():
                    if action == 'ε':
                        if next_state not in eps:
                            new_states = True
                        eps.add(next_state)


        return eps

    def minmize_DFA(self, DFA: FSM) -> FSM:
        pass