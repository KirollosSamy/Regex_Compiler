from collections import defaultdict
from fsm import FSM, State, Action
from shunting_yard import ShuntingYard
from thompson import Thompson
from exceptions import ParserSyntaxError
from preprocessor import RegexPreprocessor
from typing import List, Set, Dict, Tuple

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
                        i. find the epsilon closure of the union of the next states of the current state in the NFA for the action
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
        # iterate over unmarked states
        while unmarked_states:
            current_state = unmarked_states.pop()

            # iterate over each action in each state
            for state in current_state.elements:
                for action in NFA.get_transitions(state).keys():
                    if action == 'ε':
                        continue
                    next_states = set()
                    for next_state in NFA.get_transitions(state)[action]:
                        next_states |= self.epsilon_closure(NFA, next_state)
                    next_states = frozenset(next_states)

                    # Check if the next states are not already in the DFA states
                    new_state = None
                    if next_states not in frozenset([s_.elements for s_ in DFA._states.keys()]):
                        # If not, create a new state with the next states
                        new_state = State(self.set_to_string(next_states), next_states)
                        DFA.add_state(new_state)
                        unmarked_states.append(new_state)
                    else:
                        # If the next states are already in the DFA states, find the existing state to reuse it
                        for state_ in DFA._states.keys():
                            if state_.elements == next_states:
                                new_state = state_
                                break

                    DFA.add_transition(current_state, new_state, action)

        # check for acceptance states    
        for state in DFA._states.keys():
            for nfa_state in state.elements:
                if NFA.is_acceptance(nfa_state):
                    DFA._acceptance_states.add(state)
                    break

        # rename states
        for state in DFA._states.keys():
            state.name = "S" + str(list(DFA._states.keys()).index(state))
        
        return DFA


    def epsilon_closure(self, nfa: FSM,s: State) -> Set[State]:
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
    
    def minimize_DFA(self, DFA: FSM) -> FSM:

        P, Q = self._create_initial_sets(DFA)
        print(f'P: {self.set_to_string(P)}')
        print(f'Q: {self.set_to_string(Q)}')

        sets = [P, Q]

        new_states = True

        while new_states:
            new_states = False

            for set in sets:
                if len(set) > 1:
                    split_states = {}
                    for state in set:
                        transition_table = {}

                        for action, transitions in DFA.get_transitions(state).items():
                            transition_table[action] = frozenset(transitions)

                        transition_key = frozenset(transition_table.items())  
                        if transition_key not in split_states:
                            split_states[transition_key] = {state}
                        else:
                            split_states[transition_key].add(state)

                    if len(split_states) > 1:
                        sets.remove(set)
                        for split_state in split_states.values():
                            sets.append(split_state)
                            new_states = True
                        break

        for s in sets:
            print(f'splited set: {self.set_to_string(s)}')

        # remove empty sets
        sets = [s for s in sets if s]

        minimized_DFA = self._create_minimized_DFA(DFA, sets)

        return minimized_DFA

    

    # create initial sets [acceptance] and [not acceptance] states
    def _create_initial_sets(self, DFA: FSM) -> Tuple[Set[State], Set[State]]:
        P = set()
        Q = set()
        for state in DFA._states.keys():
            if DFA.is_acceptance(state):
                P.add(state)
            else:
                Q.add(state)
        return P, Q

    # create and save the minimized DFA
    def _create_minimized_DFA(self, DFA: FSM, merged_sets: List[Set[State]]) -> FSM:
        minimized_DFA = FSM()

        # Create a mapping from original states to new states in the minimized DFA
        state_mapping = {}
        for idx, states_set in enumerate(merged_sets):
            #assume choosing the first state as representative of the set
            new_state = State("S" + str(idx),frozenset(states_set))
            minimized_DFA.add_state(new_state)
            for state in states_set:
                state_mapping[state.name] = new_state

            # Set the initial state of the minimized DFA
            if DFA.initial_state in states_set:
                minimized_DFA.initial_state = new_state


            # If any state in the set is an acceptance state, the set is an acceptance state
            if any(DFA.is_acceptance(state) for state in states_set):
                minimized_DFA._acceptance_states.add(new_state)

        # print state_mapping
        for k, v in state_mapping.items():
            print(f'{k}: {v}')

        # Add transitions to the minimized DFA
        for from_state, transitions in DFA._states.items():
            for action, to_state in transitions.items():
                # Map original states to new states
                new_from_state = state_mapping[from_state.name]
                
                # Add transition to the minimized DFA
                for state in set(to_state):
                    new_to_state = state_mapping[state.name]

                    # if transition with the same action already exists, skip
                    if action in minimized_DFA.get_transitions(new_from_state).keys():
                        if new_to_state in minimized_DFA.get_transitions(new_from_state)[action]:
                            continue
                    minimized_DFA.add_transition(new_from_state, new_to_state, action)

        return minimized_DFA





    
    
    def list_to_string(self,lst: List[State]) -> str:
        names = [state.name for state in lst]   
        return ' '.join(names)

    def set_to_string(self,s: 'set[State]') -> str:
        names = [state.name for state in s]    
        return ' '.join(names)
