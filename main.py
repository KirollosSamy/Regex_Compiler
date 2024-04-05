from fsm import FSM
from regex import Regex
from regex_parser import RegexParser

def main():
    # fsm = FSM.from_json("json/fsm.json")
    # fsm.visualize("output/fsm")
    # fsm.to_json("json/out.json")
    
    regex_parser = RegexParser()
    regex = Regex("a(a|b)*b", regex_parser)
    regex.compile()
    # regex_parser.regex_to_NFA("a&(a|b)*&b")

if __name__ == "__main__":
    main()