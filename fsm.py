from dataclasses import dataclass
from typing import Dict, Set,List
import json
from graphviz import Digraph

Action = str
    
class State:
    name: str
    # frozenset is an immutable version of set (once created can never be modified)
    elements: frozenset
    
    def __init__(self, name: str, elements=None):
        self.name = name
        self.elements = elements if elements is not None else frozenset()
        
    # In order to use State object as python dict, we need to implement both __hash__ and __eq__
    # If the state has elements, we use it to define both __hash__ and __eq__, otherwise we use the state name
    def __hash__(self):
        if self.elements: return hash(self.elements)
        else: return hash(self.name)
    
    def __eq__(self, other: 'State'):
        if self.elements: return self.elements == other.elements
        else: return self.name == other.name
        
class FSM():
    # The internal representation of the FSM. 
    _states: Dict[State, Dict[Action, List[State]]]
    initial_state: State
    _acceptance_states: Set[State]
    
    def __init__(self):
        self._states = {}
        self._acceptance_states = set()
        
    def extend(self, other: 'FSM'):
        self._states.update(other._states)
    
    def add_state(self, state: State):
        self._states[state] = {}
        
    def add_transition(self, source: State, destination: State, action: Action):
        if action in self._states[source]:    
            self._states[source][action].append(destination)
        else:
            self._states[source][action] = [destination]
        
    def get_transitions(self, state: State) -> Dict[Action, List[State]]:
        return self._states[state]
    
    # Returns only one acceptance state
    @property
    def acceptance_state(self) -> State:
        return next(iter(self._acceptance_states))
    
    @property
    def acceptance_states(self) -> Set[State]:
        return self._acceptance_states
    
    def is_acceptance(self, state: State):
        return state in self._acceptance_states
    
    def set_acceptance(self, state: State):
        self._acceptance_states.add(state)
    
    
    # Deserialize FSM object from json file
    # I slightly changed the json file structure to enhance data encapsulation
    @classmethod
    def from_json(cls, filename: str) -> "FSM":
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
                  
        fsm = cls()
        fsm.initial_state = State(data["startingState"])
        del data["startingState"] # deleting is done for easy parsing
        
        for state_name, state_data in data.items():
            state = State(state_name)
            fsm.add_state(state)
            if state_data["isTerminatingState"]:
                fsm.set_acceptance(state)
            del state_data["isTerminatingState"]  # deleting is done for easy parsing
            for action, destinations in state_data.items():
                if isinstance(destinations, list):
                    for destination in destinations:
                        fsm.add_transition(state, State(destination), action)
                else:
                    fsm.add_transition(state, State(destinations), action)
        return fsm
     
    # Serialize FSM object into json file   
    def to_json(self, filename: str):
        data = {}
        data["startingState"] = self.initial_state.name
        
        for state, transitions in self._states.items():
            data[state.name] = {}
            data[state.name]["isTerminatingState"] = self.is_acceptance(state)
            for action, destinations in transitions.items():
                if len(destinations) == 1:
                    data[state.name][action] = destinations[0].name
                else:
                    data[state.name][action] = [destination.name for destination in destinations]
        
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2, ensure_ascii=False)
            
    def visualize(self, filename: str, label: str=None):
        label = label if label is not None else filename
        graph = Digraph(comment=label)
        graph.attr(rankdir='LR')
        # Add graph nodes
        for state in self._states:
            if state in self.acceptance_states:
                graph.node(state.name, shape='doublecircle')
            else:
                if state == self.initial_state:
                    graph.node(state.name, shape='circle', color='blue', style='filled', fillcolor='lightblue')
                else:
                    graph.node(state.name, shape='circle')

        # Add graph edges
        for source, transitions in self._states.items():
            for action, destinations in transitions.items():
                for destination in destinations:
                    graph.edge(source.name, destination.name, action)
        graph.render(filename, format='png', cleanup=True)