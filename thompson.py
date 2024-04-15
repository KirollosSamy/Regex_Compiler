from collections import deque
from fsm import FSM, State
from exceptions import ParserSyntaxError

EPSILON_MOVE = 'ε'

class Thompson:
    BINARY_OPERATORS = ('&', '|', '-')
    UNARY_OPERATORS = ('*', '+', '?')
    
    _state_index = 0
        
    def construct_NFA(self, postfix: str) -> FSM:
        NFA = FSM()
        stack = deque()
        
        for symbol in postfix:
            if symbol.isalnum():
                NFA = self.base(symbol)
            elif self.is_binary_operator(symbol):
                if len(stack) < 2:
                    raise ParserSyntaxError("Invalid Regex")
                B = stack.pop()
                A = stack.pop()
                if symbol == '&':
                    NFA = self.concat(A, B)
                elif symbol == '|':
                    NFA = self.union(A, B)
                elif symbol == '-':
                    NFA = self.range(A, B)
            elif self.is_unary_operator(symbol):
                if len(stack) < 1:
                    raise ParserSyntaxError("Invalid Regex")
                A = stack.pop()
                if symbol == '*':
                    NFA = self.kleene_star(A)
                elif symbol == '+':
                    NFA = self.kleene_plus(A) 
                if symbol == '?':
                    NFA = self.zero_or_one(A)         
            stack.append(NFA)   
            
        return NFA           
    
    def is_binary_operator(self, symbol: str) -> bool:
        return symbol in self.BINARY_OPERATORS
    
    def is_unary_operator(self, symbol: str) -> bool:
        return symbol in self.UNARY_OPERATORS
    
    def base(self, symbol: str) -> FSM:
        NFA = FSM()
        source, destination = self.make_state(), self.make_state()
        NFA.add_state(source)
        NFA.add_state(destination)
        NFA.initial_state = source
        NFA.set_acceptance(destination)
        NFA.add_transition(source, destination, symbol)
        return NFA
    
    def concat(self, A: FSM, B: FSM) -> FSM:
        NFA = FSM()
        NFA.extend(A)
        NFA.extend(B)
        NFA.initial_state = A.initial_state
        NFA.set_acceptance(B.acceptance_state)
        NFA.add_transition(A.acceptance_state, B.initial_state, EPSILON_MOVE)
        return NFA
    
    def union(self, A: FSM, B: FSM) -> FSM:
        NFA = FSM()
        NFA.extend(A)
        NFA.extend(B)
        
        initial, terminal = self.make_state(), self.make_state()
        NFA.add_state(initial)
        NFA.add_state(terminal)
        NFA.initial_state = initial
        NFA.set_acceptance(terminal)
        
        NFA.add_transition(initial, A.initial_state, EPSILON_MOVE)
        NFA.add_transition(initial, B.initial_state, EPSILON_MOVE)
        NFA.add_transition(A.acceptance_state, terminal, EPSILON_MOVE)
        NFA.add_transition(B.acceptance_state, terminal, EPSILON_MOVE)
        return NFA
    
    def kleene_plus(self, A: FSM) -> FSM:
        NFA = FSM()
        NFA.extend(A)
        
        initial, terminal = self.make_state(), self.make_state()
        NFA.add_state(initial)
        NFA.add_state(terminal)
        NFA.initial_state = initial
        NFA.set_acceptance(terminal)
        
        NFA.add_transition(initial, A.initial_state, EPSILON_MOVE)
        NFA.add_transition(A.acceptance_state, terminal, EPSILON_MOVE)
        NFA.add_transition(A.acceptance_state, initial, EPSILON_MOVE)

        return NFA
    
    def kleene_star(self, A: FSM) -> FSM:
        NFA = self.kleene_plus(A)
        NFA.add_transition(NFA.initial_state, NFA.acceptance_state, EPSILON_MOVE)
        return NFA
    
    def zero_or_one(self, A: FSM) -> FSM:
        NFA = FSM()
        NFA.extend(A)
        
        initial = self.make_state()
        NFA.add_state(initial)
        NFA.initial_state = initial
        NFA.set_acceptance(A.acceptance_state)
        
        NFA.add_transition(NFA.initial_state, NFA.acceptance_state, EPSILON_MOVE)
        NFA.add_transition(NFA.initial_state, A.initial_state, EPSILON_MOVE)
        return NFA
    
    def range(self, A: FSM, B: FSM):
        start = next(iter(A.get_transitions(A.initial_state)))
        end = next(iter(B.get_transitions(B.initial_state)))
        
        NFA = FSM()
        source, destination = self.make_state(), self.make_state()
        NFA.add_state(source)
        NFA.add_state(destination)
        NFA.initial_state = source
        NFA.set_acceptance(destination)
        NFA.add_transition(source, destination, f'{start}-{end}')
        return NFA
        
            
    def make_state(self) -> State:
        state = State(f'S{self._state_index}')
        self._state_index += 1
        return state
    