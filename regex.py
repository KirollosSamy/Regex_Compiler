from regex_parser import RegexParser
from fsm import FSM

class Regex:
    _pattern: str
    _parser: RegexParser
    _fsm: FSM
    
    def __init__(self, pattern: str, parser: RegexParser):
        self._pattern = pattern
        self._parser = parser
        
    @property
    def pattern(self):
        return self._pattern
    
    def compile(self):
        self._fsm = self._parser.parse(self._pattern)
        
    def search(self, string: str):
        pass
        