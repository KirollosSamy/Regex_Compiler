from typing import Set
from fsm import FSM, State
from utils import set_to_string

class SubsetConstruction:

    def execute(self, NFA: FSM) -> FSM:
        '''
            algorithm for converting NFA to DFA (power set construction):

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
                        new_state = State(set_to_string(next_states), next_states)
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

