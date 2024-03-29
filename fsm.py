from dataclasses import dataclass
from typing import Dict, TypeAlias, Set
import json
from graphviz import Digraph

Action: TypeAlias = str
State: TypeAlias = str
    
class FSM():
    # The internal representation of the FSM. 
    _states: Dict[State, Dict[Action, State]]
    _initial_state: State
    _acceptance_states: Set[State]
    
    def __init__(self):
        self._states = {}
        self._acceptance_states = set()
    
    @property
    def initial_state(self) -> State:
        return self._initial_state
    
    @property
    def acceptance_states(self) -> Set[State]:
        return self._acceptance_states
    
    def is_acceptance(self, state: State):
        return state in self._acceptance_states
    
    def add_state(self, state: State):
        self._states[state] = {}
        
    def remove_state(self, state: State):
        del self._states[state]
        
    def add_transition(self, source: State, destination: State, action: Action):
        self._states[source][action] = destination
        
    def remove_transition(self, source: State, destination: State, action: Action):
        del self._states[source][action]
        
    def get_transitions(self, state: State) -> Dict[Action, State]:
        return self._states[state]
        
    
    # Deserialize FSM object from json file
    # I slightly changed the json file structure to enhance data encapsulation
    @classmethod
    def from_json(cls, filename: str) -> "FSM":
        with open(filename, "r") as file:
            data = json.load(file)
                  
        fsm = cls()
        fsm._initial_state = data["startingState"]
        
        for state, state_data in data["states"].items():
            fsm._states[state] = state_data["transitions"]
            if state_data["isTerminatingState"]:
                fsm._acceptance_states.add(state)
            
        return fsm
     
    # Serialize FSM object into json file   
    def to_json(self, filename: str):
        data = {}
        data[startingState] = self._initial_state
        
        for state, transitions in self._states.items():
            data[state] = transitions.copy()
            data[state]["isTerminatingState"] = self.is_acceptance(state)
        
        with open(filename, "w") as file:
            json.dump(data, file)
            
    def visualize(self, filename):
        graph = Digraph(comment='Finite State Machine')
        for state in self._states:
            graph.node(state)
        for source, transitions in self._states.items():
            for destination, action in transitions.items():
                graph.edge(source, destination, action)
        graph.render(filename, format='png', cleanup=True)
        

# @dataclass(frozen=True)
# class State:
#     name: str
#     is_acceptance: bool
    
#     def __init__(self, name, is_acceptance=False):
#         self.name = name
#         self.is_acceptance = is_acceptance
        
#     # Define how to hash a State object (For use in _graph Dict in FSM class)
#     def __hash__(self):
#         return hash(self.name)