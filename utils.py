from typing import List
from fsm import State


def list_to_string(lst: List[State]) -> str:
    names = [state.name for state in lst]   
    return ' '.join(names)

def set_to_string(s: 'set[State]') -> str:
    names = [state.name for state in s]    
    return ' '.join(names)