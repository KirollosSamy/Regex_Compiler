from fsm import FSM
from regex import Regex
from regex_parser import RegexParser
from preprocessor import RegexPreprocessor

def main():
    regex_parser = RegexParser()
    
    while True:
        regex = input("Enter regex: ")
        regex_parser.parse(regex)

    # (a|b)*[ab]? fails
    # (a+a+)+b fails
    # [bc]*(cd)+ fails

if __name__ == "__main__":
    main()