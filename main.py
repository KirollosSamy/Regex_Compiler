from fsm import FSM
from regex import Regex
from regex_parser import RegexParser
from preprocessor import RegexPreprocessor

def main():
    regex_parser = RegexParser()
    # regex = Regex("a(a|b)*b", regex_parser)
    preprocessed_regex = RegexPreprocessor.preprocess("[a-z]")
    NFA = regex_parser.regex_to_NFA(preprocessed_regex)
    NFA.visualize('output/simple_regex')
    NFA.to_json('json/NFA.json')

if __name__ == "__main__":
    main()