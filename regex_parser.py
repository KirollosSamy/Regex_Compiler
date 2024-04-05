from fsm import FSM
from shunting_yard import ShuntingYard

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

    def minmize_DFA(self, DFA: FSM) -> FSM:
        pass