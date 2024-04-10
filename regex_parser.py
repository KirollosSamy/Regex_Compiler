from fsm import FSM, State, Action
from shunting_yard import ShuntingYard
from thompson import Thompson
from exceptions import ParserSyntaxError
from preprocessor import RegexPreprocessor
from typing import List, Set, Dict

class RegexParser:
    def parse(self, regex: str) -> FSM:
        regex = RegexPreprocessor.preprocess(regex)
        NFA = self.regex_to_NFA(regex)
        DFA = self.NFA_to_DFA(NFA)
        DFA_min = self.minmize_DFA(DFA)
        return DFA_min
    
    def regex_to_NFA(self, regex: str) -> FSM:
        operators = {'*':0, '+':0, '?':0, '&': 1, '|': 2}
        shunting_yard = ShuntingYard(operators)
        postfix = shunting_yard.parse(regex)
        thompson = Thompson()
        NFA = thompson.construct_NFA(postfix)
        return NFA
    
    def NFA_to_DFA(self, NFA: FSM) -> FSM:
        '''
            algorithm for converting NFA to DFA (powerset construction):

                1. create a new start state and add it to the DFA states
                    a. each state is a set of NFA states
                    b. the start state is the epsilon closure of the start state of the NFA

                2. add the epsilon closure of the new start state to the DFA states
                    a. begin with epsilon closure of the start state of the NFA

                3. while there is an unmarked state in the DFA states:
                    a. mark the state as visited.

                    b. for each possible action in the alphabet:
                        i. find the epsilon closure of the union of the next states of the current state
                           in the NFA for the action
                        ii. if the closure is not in the DFA states, add it
                        iii. add a transition from the current state to the closure
                    
                    c. repeat step 3 until all states are marked

                4. the acceptance states of the DFA are the states that contain an acceptance state of the NFA
                    a. if a state contains an acceptance state of the NFA, it is an acceptance state of the DFA

                5. return the DFA          

        '''
        DFA = FSM()
        start_state = State('start', self.epsilon_closure(NFA, NFA.initial_state))
        # convert set of states to Frozenset to make it hashable
        start_state.elements = frozenset(start_state.elements)
        DFA.add_state(start_state)
        DFA.initial_state = start_state

        unmarked_states = [start_state]
        marked_states = set()
        # iterate over unmarked states
        while unmarked_states:
            current_state = unmarked_states.pop()
            marked_states.add(current_state)

            # iterate over each action in each state
            for state in current_state.elements:
                for action in NFA.get_transitions(state).keys():
                    if action == 'ε':
                        continue
                    next_states = set()
                    for next_state in NFA.get_transitions(state)[action]:
                        next_states |= self.epsilon_closure(NFA, next_state)
                    next_states = frozenset(next_states)

                    if next_states not in [state.elements for state in DFA._states.keys()]:
                        new_state = State(self.set_to_string(next_states), next_states)
                        DFA.add_state(new_state)
                        unmarked_states.append(new_state)

                    DFA.add_transition(current_state, new_state, action)
        # check for acceptance states    
        for state in DFA._states.keys():
            for nfa_state in state.elements:
                if NFA.is_acceptance(nfa_state):
                    DFA._acceptance_states.add(state)
                    break

        return DFA


    def epsilon_closure(self, nfa: FSM,s: State) -> Set[State]:
        # print(f'epsilon closure of state {s.name}')
        eps = {s}
        new_states = True

        while new_states:
            new_states = False
            for state in eps.copy():
                for action, next_states in nfa.get_transitions(state).items():
                    if action == 'ε':
                        for next_state in next_states:
                            if next_state not in eps:
                                new_states = True
                            eps.add(next_state)


        return eps

    def minmize_DFA(self, DFA: FSM) -> FSM:
        pass
    
    def list_to_string(self,lst: List[State]) -> str:
        names = [state.name for state in lst]   
        return ' '.join(names)

    def set_to_string(self,s: 'set[State]') -> str:
        names = [state.name for state in s]    
        return ' '.join(names)
