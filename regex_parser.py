from fsm import FSM
from minimizer import Minimizer
from shunting_yard import ShuntingYard
from thompson import Thompson
from preprocessor import RegexPreprocessor
from subset_construction import SubsetConstruction

class RegexParser:
    def parse(self, regex: str) -> FSM:
        processed_regex = RegexPreprocessor.preprocess(regex)

        NFA = self.regex_to_NFA(processed_regex)
        NFA.visualize('output/NFA')
        NFA.to_json('json/NFA.json')

        DFA = self.NFA_to_DFA(NFA)
        DFA.visualize('output/DFA')
        DFA.to_json('json/DFA.json')

        DFA_min = self.minimize_DFA(DFA)
        DFA_min.visualize('output/minimized_DFA')
        DFA_min.to_json('json/minimized_DFA.json')

        return DFA_min
    
    def regex_to_NFA(self, regex: str) -> FSM:
        operators = {'*':0, '+':0, '?':0, '&': 1, '-': 1, '|': 2}
        shunting_yard = ShuntingYard(operators)
        postfix = shunting_yard.parse(regex)
        thompson = Thompson()
        NFA = thompson.construct_NFA(postfix)
        return NFA
    
    def NFA_to_DFA(self, NFA: FSM) -> FSM:
        power_set = SubsetConstruction()
        DFA = power_set.execute(NFA)
        return DFA
    
    def minimize_DFA(self, DFA: FSM) -> FSM:
        minimizer = Minimizer()
        minimized_DFA = minimizer.execute(DFA)
        return minimized_DFA