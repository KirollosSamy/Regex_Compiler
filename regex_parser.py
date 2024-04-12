from collections import defaultdict
from fsm import FSM, State, Action
from shunting_yard import ShuntingYard
from thompson import Thompson
from typing import List, Set, Dict, Tuple

class RegexParser:
    def parse(self, regex: str) -> FSM:
        regex = self.preprocess(regex)
        NFA = self.regex_to_NFA(regex)
        DFA = self.NFA_to_DFA(NFA)
        DFA_min = self.minmize_DFA(DFA)
        return DFA_min
        
    def preprocess(self, regex: str) -> str:
        processed_regex = self._inject_concat(regex)
        return processed_regex
    
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
        '''
        algorithm for minimizing DFA:

            1. create two sets of states P and Q
                a. P contains all acceptance states
                b. Q contains all non-acceptance states

            2. create initially two sets to be split
                a. P and Q

            3. while there are states in any of the sets:
                a. check if a state has transitions to different sets
                    i. if yes, split the set
                b. repeat step 3 until no more states are split

                c. keep track of split sets and merge the ones that have the same transitions

            4. return the minimized DFA
        '''

        P, Q = self._create_initial_sets(DFA)
        print(f'P: {self.set_to_string(P)}')
        print(f'Q: {self.set_to_string(Q)}')

        sets = [P, Q]
        new_sets = True
        while new_sets:
            new_sets = False
            for s in sets.copy():
                if len(s) > 1:
                    new_sets = self._split_set(DFA, s, sets)
                    if new_sets:
                        break # break the loop if a set is splitted to start over 

        for s in sets:
            print(f'splited set: {self.set_to_string(s)}')

        # merged_sets = self._merge_sets(DFA, sets)

        # for s in merged_sets:
        #     print(f'merged set: {self.set_to_string(s)}')

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

    # split sets that have transitions to different sets
    def _split_set(self, DFA: FSM, s: Set[State], sets: List[Set[State]]) -> bool:
        new_sets = False
        set_next_states = set()  # The next states of the current set

        for state in s:
            transitions = DFA.get_transitions(state)
            for action, next_states in transitions.items():
                set_next_states |= set(next_states)  # Union of all next states in this set

        # Compare the next states of the current set with other sets
        for other in sets:
            # Skip the current set and any empty sets
            if other == s:
                continue

            # Check if all next states of the current set exist in the other set
            if all(next_state in other for next_state in set_next_states):
                # No need to split the sets
                continue

            # Check if no next states of the current set exist in the other set
            elif not set_next_states & other:
                # No need to split the sets
                continue

            else: # some next states of the current set exist in the other set
                # If not, split the set and update new_sets flag

                # Remove the current set from the sets list
                print(f's: {self.set_to_string(s)}')
                print(f'other: {self.set_to_string(other)}')
                print(f'next states: {self.set_to_string(set_next_states)}')
                sets.remove(s)
                # Split the set s into two sets and add them to the sets list if they are not empty
                common_states = set_next_states & other
                # get s elements having transition to common_states
                s_split = set()
                new_split = set()
                for state in s:
                    for action, next_states in DFA.get_transitions(state).items():
                        if set(next_states) & common_states:
                            s_split.add(state)
                            break
                        else:
                            new_split.add(state)
                if s_split:
                    new_sets = True
                    print(f'split states: {self.set_to_string(s_split)}')
                    sets.append(s_split)

                if new_split:
                    print(f'new split states: {self.set_to_string(new_split)}')
                    sets.append(new_split)


                break  # Break the loop if a set is split

        return new_sets




    # merge sets that have the same transitions
    def _merge_sets(self, DFA: FSM, sets: List[Set[State]]) -> List[Set[State]]:
        merged_sets = []
        merged = False
        for set_ in sets:
            for state in set_:
                transitions = DFA.get_transitions(state)
                for action, next_states in transitions.items():
                    for other in sets:
                        for next_state in next_states:
                            if next_state in other and set_ != other:
                                merged = merged & True
                        if merged:
                            merged_set = set_ | other
                            merged_sets.append(merged_set)
                            break
                    if merged:
                        break
                if merged:
                    break

            if not merged:
                merged_sets.append(set_)

            merged = False

        return merged_sets

    # create and save the minimized DFA
    def _create_minimized_DFA(self, DFA: FSM, merged_sets: List[Set[State]]) -> FSM:
        minimized_DFA = FSM()

        # Create a mapping from original states to new states in the minimized DFA
        state_mapping = {}
        for idx, states_set in enumerate(merged_sets):
            new_state = State("S_new" + str(idx),frozenset(states_set))
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
                for state in to_state:
                    new_to_state = state_mapping[state.name]
                    minimized_DFA.add_transition(new_from_state, new_to_state, action)

        return minimized_DFA





    
    
    def _inject_concat(self, regex: str) -> str:
        SPECIAL_SYMBOLS = ('*', '+', '?', ')', ']')
        CONCAT_OPERATOR = '&'
        
        processed_regex = ""
        for i in range(len(regex)-1):
            char, next_char = regex[i], regex[i+1]
            processed_regex += char
            if (char in SPECIAL_SYMBOLS and next_char not in SPECIAL_SYMBOLS) \
                    or (char.isalnum() and (
                            next_char.isalnum() or
                            next_char == '(' or
                            next_char == '['
                    )):
                processed_regex += CONCAT_OPERATOR
        
        processed_regex += regex[-1]       
        return processed_regex
    
    def list_to_string(self,lst: List[State]) -> str:
        names = [state.name for state in lst]   
        return ' '.join(names)

    def set_to_string(self,s: 'set[State]') -> str:
        names = [state.name for state in s]    
        return ' '.join(names)
