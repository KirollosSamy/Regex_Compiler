from fsm import FSM,DFA, State, Action
from shunting_yard import ShuntingYard
from thompson import Thompson
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
        processed_regex = self._inject_concat(regex)
        return processed_regex
    
    def regex_to_NFA(self, regex: str) -> FSM:
        operators = {'*':0, '+':0, '?':0, '&': 1, '|': 2}
        shunting_yard = ShuntingYard(operators)
        postfix = shunting_yard.parse(regex)
        thompson = Thompson()
        NFA = thompson.construct_NFA(postfix)
        return NFA
    
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
    
    def _inject_concat(self, regex: str) -> str:
        SPECIAL_SYMBOLS = ('*', '+', '?', ')', ']')
        CONCAT_OPERATOR = '&'
        
        processed_regex = ""
        for i in range(len(regex)-1):
            char, next_char = regex[i], regex[i+1]
            processed_regex += char
            if (char in SPECIAL_SYMBOLS and next_char not in SPECIAL_SYMBOLS) \
                    or (char.isalnum() and (
                            next_char.isalnum() or
                            next_char == '(' or
                            next_char == '['
                    )):
                processed_regex += CONCAT_OPERATOR
        
        processed_regex += regex[-1]       
        return processed_regex
