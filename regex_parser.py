from fsm import FSM
from shunting_yard import ShuntingYard
from thompson import Thompson
from exceptions import ParserSyntaxError
from preprocessor import RegexPreprocessor

class RegexParser:
    def parse(self, regex: str) -> FSM:
        regex = RegexPreprocessor.preprocess(regex)
        NFA = self.regex_to_NFA(regex)
        DFA = self.NFA_to_DFA(NFA)
        DFA_min = self.minmize_DFA(DFA)
        return DFA_min
    
    def regex_to_NFA(self, regex: str) -> FSM:
        operators = {'*':0, '+':0, '?':0, '&': 1, '|': 2}
        shunting_yard = ShuntingYard(operators)
        postfix = shunting_yard.parse(regex)
        thompson = Thompson()
        NFA = thompson.construct_NFA(postfix)
        return NFA
    
    def NFA_to_DFA(self, NFA: FSM) -> FSM:
        pass

    def minmize_DFA(self, DFA: FSM) -> FSM:
        pass
