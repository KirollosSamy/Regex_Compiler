from typing import List, Set, Tuple
from fsm import FSM, State

class Minimizer:

    def execute(self, DFA: FSM) -> FSM:
        '''
            algorithm for minimizing a DFA:
                1. create initial sets [acceptance] and [not acceptance] states

                2. create a list of sets containing the initial sets

                3. while there are new states:
                    a. for each set in the list:
                        i. create a dictionary of transitions for each state in the set
                        ii. create a key for the dictionary
                        iii. if the key is not in the dictionary, add it
                        iv. if the key is in the dictionary, add the state to the set

                    b. if the set has more than one state, split the set

                    c. if the set was split, remove the old set and add the new sets

                4. remove empty sets
                
                5. create and save the minimized DFA
        '''
        P, Q = self._create_initial_sets(DFA)
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
   