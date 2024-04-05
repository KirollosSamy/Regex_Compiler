from typing import List, Dict
from collections import deque
from exceptions import ParserSyntaxError

class ShuntingYard:
    # A list of allowed operators with decreasing precedence
    _operators: Dict[str, int]
    
    def __init__(self, operators: Dict[str, int]):
        self._operators = operators
            
    def is_operator(self, symbol: str) -> bool:
        return symbol in self._operators
    
    def precedes(self, op1: str, op2: str) -> bool:
        return self._operators[op1] <= self._operators[op2]
        
    def parse(self, infix: str) -> str:        
        stack = deque()
        output_queue = deque()
        
        for symbol in infix:
            if symbol.isalnum():
                output_queue.append(symbol)
                
            elif self.is_operator(symbol):
                while len(stack) != 0 and stack[-1] != '(' and self.precedes(stack[-1], symbol):
                    operator = stack.pop()
                    output_queue.append(operator)
                stack.append(symbol)
                
            elif symbol == '(':
                stack.append(symbol)
                
            elif symbol == ')':
                while len(stack) != 0 and stack[-1] != '(':
                    operator = stack.pop()
                    output_queue.append(operator)
                if len(stack) == 0:
                    raise ParserSyntaxError("Unmatched Parenthesis")
                else: stack.pop()
        
        while len(stack) != 0:
            operator = stack.pop()
            if operator == '(':
                raise ParserSyntaxError("Unmatched Parenthesis")
            output_queue.append(operator)
            
        postfix = ''.join(output_queue) 
        return postfix