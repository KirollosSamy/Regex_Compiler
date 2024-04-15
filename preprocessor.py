import string
from exceptions import ParserSyntaxError

class RegexPreprocessor:
    @staticmethod
    def preprocess(regex: str) -> str:
        RegexPreprocessor.validate_alphapet(regex)
        processed_regex = RegexPreprocessor._handle_ranges(regex)
        processed_regex = RegexPreprocessor._inject_concat(processed_regex)
        return processed_regex
    
    @staticmethod    
    def _inject_concat(regex: str) -> str:
        if not regex: return ""
        
        SPECIAL_SYMBOLS = ('*', '+', '?', ')')
        CONCAT_OPERATOR = '&'
        
        processed_regex = ""
        for i in range(len(regex)-1):
            char, next_char = regex[i], regex[i+1]
            processed_regex += char
            
            if (char in SPECIAL_SYMBOLS and 
                next_char not in SPECIAL_SYMBOLS and 
                next_char != '|') \
                or (char.isalnum() and (
                    next_char.isalnum() or
                    next_char == '('
                )):
                processed_regex += CONCAT_OPERATOR
        
        processed_regex += regex[-1]       
        return processed_regex

    @staticmethod
    def _handle_ranges(regex: str) -> str:
        n = len(regex)
        preprocessed_regex = ""
        
        i = 0
        while i < n:
            if regex[i] == '[':
                i = i+1
                preprocessed_regex += '('
                while i < n and regex[i] != ']':
                    if i+1 >= n: raise ParserSyntaxError("Unmatched sqaure parentheses")
                    if regex[i+1] == '-':
                        if not (i+2 < n): raise ParserSyntaxError("Invalid range")
                        if (regex[i].islower() and regex[i+2].islower()) \
                                or (regex[i].isupper() and regex[i+2].isupper()) \
                                or (regex[i].isdigit() and regex[i+2].isdigit()):
                            start, end = ord(regex[i]), ord(regex[i+2])
                            if start >= end: raise ParserSyntaxError("Invalid range")
                            # expanded_range = [chr(c) for c in range(start, end)]
                            # preprocessed_regex += '|'.join(expanded_range) + '|'
                            # i += 1
                            preprocessed_regex += f'{regex[i]}-{regex[i+2]}'
                            if i+3 < n and regex[i+3].isalnum():
                                preprocessed_regex += '|'
                            i += 2
                        else: raise ParserSyntaxError("Invalid range")
                    elif regex[i].isalnum() and regex[i+1].isalnum():
                        preprocessed_regex += regex[i] + '|'
                    elif regex[i].isalnum() and regex[i+1] == ']':
                        preprocessed_regex += regex[i]
                    else: raise ParserSyntaxError("Invalid range")
                    i += 1
                if i >= n or regex[i] != ']': 
                    raise ParserSyntaxError("Unmatched sqaure parentheses")
                preprocessed_regex += ')'
            else: 
                if regex[i] == ']': 
                    raise ParserSyntaxError("Unmatched sqaure parentheses")
                elif regex[i] == '.':
                    # alphanum_chars = string.ascii_letters + string.digits
                    # preprocessed_regex += '(' + '|'.join(alphanum_chars) + ')'
                    preprocessed_regex += '(a-z|A-Z|0-9)'
                else:
                    preprocessed_regex += regex[i]
            i += 1
        return preprocessed_regex
    
    @staticmethod
    def validate_alphapet(regex: str):
        allowed_symbols = {'*', '+', '?', '(', ')', '[', ']', '.', '|', '-'}
        for symbol in regex:
            if not (symbol.isalnum() or symbol in allowed_symbols):
                raise ParserSyntaxError(f"Invalid symbol {symbol}")