from regex_parser import RegexParser
from fsm import FSM
from exceptions import ParserSyntaxError

class Regex:
    _pattern: str
    _fsm: FSM
    
    _parser: RegexParser
    
    @classmethod
    def set_parser(cls, parser: RegexParser):
        cls._parser = parser
    
    def __init__(self, pattern: str):
        self._pattern = pattern
        
    @property
    def pattern(self):
        return self._pattern
    
    def compile(self) -> Exception:
        try:
            self._fsm = self._parser.parse(self._pattern)
        except ParserSyntaxError as e:
            return e
        
    def search(self, string: str):
        pass
        