from fsm import FSM
from regex import Regex
from regex_parser import RegexParser

def main():
    # fsm = FSM.from_json("json/fsm.json")
    # fsm.visualize("output/fsm", label='test')
    # fsm.to_json("json/out.json")
    
    regex_parser = RegexParser()
    regex = Regex("a(a|b)*b", regex_parser)
    NFA = regex_parser.regex_to_NFA("a&(a|b)*&b")
    NFA.visualize('output/simple_regex')
    NFA.to_json('json/NFA.json')

if __name__ == "__main__":
    main()