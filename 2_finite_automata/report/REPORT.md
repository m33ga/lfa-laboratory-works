# Determinism in Finite Automata. Conversion from NDFA 2 DFA. Chomsky Hierarchy.

### Course: Formal Languages & Finite Automata
### Author: Mihai Gurduza
### Academic Group: FAF-233

----

## Theory
* ### Definitions:
  * **Grammar**: A grammar is a set of rules used to generate strings in a formal language. It consists of a finite set of symbols called the alphabet, along with a set of production rules that specify how symbols from the alphabet can be combined to form strings.
  * **Finite Automaton**: A finite automaton is a mathematical model used to recognize patterns within strings. It consists of a finite set of states, a set of transitions between these states, and a set of input symbols. Finite automata can be deterministic (DFA) or nondeterministic (NFA) depending on the rules governing the transitions.
  * **NFA**: A Nondeterministic Finite Automaton (NFA) is a type of finite automaton where for some transitions, there may be multiple possible next states for a given input symbol. This allows for greater flexibility in recognizing patterns compared to deterministic finite automata.
  * **DFA**: A Deterministic Finite Automaton (DFA) is a type of finite automaton where each transition is uniquely determined by the current state and the input symbol. DFAs are simpler than NFAs but have equivalent recognition power.
  * **Chomsky Hierarchy**: The Chomsky Hierarchy is a classification of formal grammars into four types based on their generative power. These types are Type 0 (unrestricted grammars), Type 1 (context-sensitive grammars), Type 2 (context-free grammars), and Type 3 (regular grammars), arranged in increasing order of generative power. This hierarchy is named after the linguist Noam Chomsky, who introduced it in the 1950s.


## Objectives:

* Understand what an automaton is and what it can be used for;
* Continuing the work in the same repository and the same project, the following need to be added: 
  1. Provide a function in your grammar type/class that could classify the grammar based on Chomsky hierarchy.
  2. For this you can use the variant (11) from the previous lab;
* According to my variant number (11), get the finite automaton definition and do the following tasks:
  1. Implement conversion of a finite automaton to a regular grammar;
  2. Determine whether your FA is deterministic or non-deterministic;
  3. Implement some functionality that would convert an NDFA to a DFA;
  4. Represent the finite automaton graphically (Optional, and can be considered as a **_bonus point_**);
     1. You can use external libraries, tools or APIs to generate the figures/diagrams;
     2. Your program needs to gather and send the data about the automaton and the lib/tool/API return the visual representation.

## Implementation description

* The `get_grammar_type` method is responsible for determining the classification of a given grammar according to the Chomsky hierarchy. It begins by initializing several boolean variables, assuming at first that the grammar satisfies all types (Type 0, Type 1, Type 2, and Type 3), and then gradually ruling out categories that the grammar does not fit into. Additionally, two flags, `is_left_linear` and `is_right_linear`, are used to check whether the grammar follows a strict left-linear or right-linear form, which is essential for identifying regular grammars (Type 3). Another flag, `is_invalid`, is used to determine whether the input grammar contains any invalid rules that do not adhere to the basic structure of a formal grammar.

```python
def get_grammar_type(self):
    # assume all types are satisfied, and then eliminate incorrect ones
    is_type_3 = True
    is_type_2 = True
    is_type_1 = True
    is_type_0 = True

    is_left_linear = True
    is_right_linear = True
    is_invalid = False
    ...
```

* After initialization, the method iterates through each production rule in the grammar, analyzing both the left-hand side (LHS) and right-hand side (RHS). The first check ensures that all symbols in the LHS are either non-terminals or terminals. If any invalid symbol is found, the grammar is marked as invalid, and the iteration stops immediately. The next validation ensures that the LHS of each rule does not contain more than one symbol. If the LHS consists of more than one symbol, the grammar cannot be classified as a Type 2 or Type 3 grammar, as those grammars must have exactly one non-terminal on the LHS.

```python
def get_grammar_type(self):
    ...
    for lhs, rhs_list in self.P.items():
        if not all(symbol in self.V_n or symbol in self.V_t for symbol in lhs):
            is_invalid = True
            break

    if len(lhs) > 1:
        is_type_3 = False
        is_type_2 = False
    ...
```

* For each RHS, the method verifies that all symbols belong to the grammar's defined terminal and non-terminal sets. If any symbol is outside these sets, the grammar is marked as invalid. Furthermore, it checks whether the RHS is at least as long as the LHS. If the RHS is shorter than the LHS, the grammar fails to meet the criteria for Type 1 grammars (context-sensitive grammars), which require that the length of the RHS must be greater than or equal to the LHS.
```python
def get_grammar_type(self):
    ...
    for rhs in rhs_list:
        if not all(symbol in self.V_n or symbol in self.V_t for symbol in rhs):
            is_invalid = True
            break
    
        if len(rhs) < len(lhs):
            is_type_1 = False
    
        if lhs not in self.V_n:
            is_type_2 = False
            is_type_3 = False
    ...
```

* Next, the method examines whether the grammar follows a regular (Type 3) structure. A Type 3 grammar is either left-linear or right-linear, meaning its production rules must follow a strict pattern. If a rule follows `A → aB`, it must be consistently right-linear, and if it follows `A → Ba`, it must be consistently left-linear. If the method encounters a rule that does not conform to either of these patterns, it disqualifies the grammar from being Type 3.
```python
def get_grammar_type(self):
    ...
    if len(rhs) == 1 and rhs[0] in self.V_t:
        continue
    elif len(rhs) == 2:
        if rhs[0] in self.V_t and rhs[1] in self.V_n:
            is_left_linear = False
        elif rhs[0] in self.V_n and rhs[1] in self.V_t:
            is_right_linear = False
        else:
            is_type_3 = False
    else:
        is_type_3 = False
    ...
```

* After all the checks, the method returns the highest valid grammar classification. If the grammar remains valid as Type 3, it distinguishes between left-linear and right-linear grammars. Otherwise, it returns the appropriate type based on the conditions satisfied. If any rule is found to be invalid, the function returns `-1`, indicating that the given grammar does not conform to a valid formal grammar structure.
```python
def get_grammar_type(self):
    ...
    if not is_invalid:
        if is_type_3:
            if is_left_linear:
                return 3, "Type 3 - Left Linear Regular Grammar"
            elif is_right_linear:
                return 3, "Type 3 - Right Linear Regular Grammar"
        elif is_type_2:
            return 2, "Type 2 - Context-Free Grammar"
        elif is_type_1:
            return 1, "Type 1 - Context-Sensitive Grammar"
        elif is_type_0:
            return 0, "Type 0 - Unrestricted Grammar"
    else:
        return -1, "Invalid"
    ...
```
---

* The `to_grammar` method converts a finite automaton into an equivalent regular grammar. This is done by translating each transition from the automaton into a corresponding production rule in the grammar. The method first initializes the sets of non-terminals (which correspond to the states of the automaton) and terminals (which are the input symbols of the automaton). It then prepares an empty dictionary `P` to store the production rules. Next, the method iterates through each state in the automaton's transition function. For each state, it processes the transitions for every input symbol. If a transition leads to a final (accepting) state, a production rule of the form `A → a` is added, where `A` is the current state and `a` is the terminal symbol. If the transition leads to a non-final state, the production rule takes the form `A → aB`, where `B` represents the next state.
```python
def to_grammar(self):
    ...
    for state, transitions in self.transitions.items():
        for symbol, next_states in transitions.items():
            for next_state in next_states:
                if state not in P:
                    P[state] = []
                if next_state in self.accept_states:
                    P[state].append(symbol)
                else:
                    P[state].append(f"{symbol}{next_state}")
    ...
```
---

* The `is_nfa` method determines whether the finite automaton is a nondeterministic finite automaton (NFA). It iterates through the transition function and checks if any state has multiple transitions for the same input symbol. If such transitions exist, the automaton is classified as an NFA.

```python
def is_nfa(self):
    for transitions in self.transitions.values():
        for next_states in transitions.values():
            if len(next_states) > 1 and next_states not in self.states:
                return True
    return False
```
---

* The `nfa_to_dfa()` method begins by checking whether the given finite automaton is already a deterministic finite automaton (DFA). This is achieved by calling the `is_nfa()` method, which determines if the automaton contains nondeterministic transitions (i.e., multiple possible next states for a single input symbol). If the automaton is already deterministic, the method simply returns the current automaton without performing any conversion. This early exit ensures efficiency by avoiding unnecessary computations.
```python
    def nfa_to_dfa(self):
        if not self.is_nfa():
            return self
        ...
```

* If the automaton is nondeterministic, the conversion process begins by initializing key data structures. The list `dfa_states` will store all the newly created DFA states. The dictionary `dfa_transitions` will hold the state transition mappings for the resulting DFA. To manage unprocessed states, `unprocessed_states` is initialized with a copy of the NFA's start state, treating it as the first DFA state. Additionally, `processed_states` is initialized as an empty set to keep track of states that have already been explored in the conversion process. The method enters a loop that continues until all states have been processed. In each iteration, a state is dequeued from `unprocessed_states` and marked as processed by adding it to `processed_states`. This state is then added to `dfa_states`, as it now forms part of the final DFA. The method then iterates over each symbol in the automaton’s alphabet to determine transitions from the current state. Since NFAs can transition to multiple states for a single symbol, the `next_state` set is used to collect all possible resulting states. For each state `s` in the current composite state, if a transition exists for the given symbol, the target states are added to `next_state`.
```python
def nfa_to_dfa(self):
    ...
        while unprocessed_states:
            current_state = unprocessed_states.pop(0)
            processed_states.add(frozenset(current_state))
            dfa_states.append(current_state)

            for symbol in self.alphabet:
                next_state = set()
                for s in current_state:
                    if s in self.transitions and symbol in self.transitions[s]:
                        next_state.update(self.transitions[s][symbol])
    ...
```

* If `next_state` is not empty (i.e., the current state has a valid transition for the symbol), it is first converted into a frozen set (`next_state_frozen`). This ensures that states are treated as unique entities, preventing duplicate processing. If this state has not yet been processed or added to `unprocessed_states`, it is appended to the queue for future processing. The `dfa_transitions` dictionary is then updated to record the transition from the current state to the new state under the given input symbol. Once all states and transitions have been processed, the method identifies the accepting states in the resulting DFA. Since an NFA can have multiple accept states, any DFA state that contains at least one of the original NFA’s accept states is marked as an accept state in the DFA. This ensures that the language recognized by the DFA remains the same as that of the original NFA.
```python
def nfa_to_dfa(self):
    ...
                if next_state:
                    next_state_frozen = frozenset(next_state)
                    if next_state_frozen not in processed_states and next_state not in unprocessed_states:
                        unprocessed_states.append(next_state.copy())

                    dfa_transitions[frozenset(current_state)] = dfa_transitions.get(frozenset(current_state), {})
                    dfa_transitions[frozenset(current_state)][symbol] = next_state.copy()

        dfa_accept_states = [
            state for state in dfa_states if any(s in self.accept_states for s in state)
        ]
    ...
```

---

* The `draw_graph` method begins by importing the necessary libraries, `graphviz.Digraph` for creating graphical representations of the automaton and `os` for handling file operations. A `Digraph` object named `dot` is created with the specified `name`, and the output format is set to PNG. This initializes a directed graph where nodes represent states, and edges represent transitions between states based on input symbols. A nested function, `format_state(state)`, is defined to ensure consistent representation of states in the graph. This function sorts the elements of a state (which may be a set of NFA states in a DFA conversion scenario) and returns a string enclosed in curly braces `{}` to improve readability. The sorting ensures that state names remain consistent across multiple executions, making the graph easier to interpret.

```python
def draw_graph(self, name):

    ...
  
    def format_state(state):
        sorted_states = sorted(state)
        return "{{{}}}".format(", ".join(sorted_states))  # if sorted_states else "∅"
    ...
```

* The method iterates over all states in the automaton, formatting each state using `format_state(state)`. If a state is an accepting state (i.e., it belongs to `self.accept_states`), it is added to the graph as a "doublecircle" node, a common convention for denoting accepting states in automaton diagrams. Otherwise, it is added as a normal "circle" node. This distinction visually differentiates accepting states from regular states. An additional node is created without a label (`""`) and is assigned a "plaintext" shape. This node acts as an entry point to visually indicate the starting state of the automaton. An edge is drawn from this start node to the formatted representation of `self.start_state`, labeled `"start"`, clarifying the automaton’s initial configuration.

```python
def draw_graph(self, name):
    for state in self.states:

        formatted_state = format_state(state)
        if any(state == accept for accept in self.accept_states):
            dot.node(formatted_state, shape="doublecircle")
        else:
            dot.node(formatted_state, shape="circle")

    dot.node("", shape="plaintext")
    formatted_start = format_state(self.start_state)
    dot.edge("", formatted_start, label="start")
    
```

* The method iterates through the `self.transitions` dictionary, which maps each state to its transitions. The `from_state` (source state) is first formatted for consistency. Then, for each transition symbol, the method checks whether `to_states` represents a single state (as in a DFA) or multiple states (as in an NFA). If `to_states` is directly a valid state in `self.states`, an edge is drawn from `from_state` to `to_states` with the corresponding transition symbol as a label. Otherwise, when `to_states` contains multiple destination states, the method iterates through each destination state separately, drawing individual edges. The method determines the directory path where the generated graph will be saved. It constructs a `graph_drawings` directory in the script’s directory using `os.path.join(os.path.dirname(os.path.realpath(__file__)), "graph_drawings")`. If the directory does not already exist, `os.makedirs(dir_path, exist_ok=True)` ensures it is created. The complete file path is then generated using `os.path.join(dir_path, name)`, and the `dot.render()` method is called to generate the PNG file. The `view=True` argument automatically opens the rendered graph for visualization.

```python
def draw_graph(self, name):
    ...
    for from_state, transitions in self.transitions.items():
        formatted_from = format_state(from_state)
        for symbol, to_states in transitions.items():
            if to_states in self.states:
                formatted_to = format_state(to_states)
                dot.edge(formatted_from, formatted_to, label=symbol)
            else:
                for inner_state in to_states:
                    formatted_to = format_state(inner_state)
                    dot.edge(formatted_from, formatted_to, label=symbol)
    ...
```




## Conclusions / Screenshots / Results

```
Variant 12
Previous grammar:
Non-terminals: {'S', 'D', 'F'}
Terminals: {'b', 'c', 'a'}
Start symbol: {'S'}
Production Rules:
{'S'} -> ['aF', 'bS'];
{'F'} -> ['bF', 'cD', 'a'];
{'D'} -> ['cS', 'a']
Type 3 - Right Linear Regular Grammar
```
The initial grammar provided follows a **Type 3 - Right Linear Regular Grammar**, containing three non-terminal symbols (`S`, `D`, `F`), three terminal symbols (`a`, `b`, `c`), and a set of production rules defining valid transitions. This grammar serves as the foundation for constructing an equivalent finite automaton.  


```
Finite Automaton:
States: {'X', 'S', 'D', 'F'}
Alphabet: {'b', 'a', 'c'}
Start State: {'S'}
Accept States: {'X'}
Transitions:
{'S'} --(a)--> {'F'}
{'S'} --(b)--> {'S'}
{'F'} --(b)--> {'F'}
{'F'} --(c)--> {'D'}
{'F'} --(a)--> {'X'}
{'D'} --(c)--> {'S'}
{'D'} --(a)--> {'X'}
FA is NFA: False
```

The corresponding **finite automaton** is then derived, consisting of four states (`S`, `D`, `F`, `X`), with `S` as the start state and `X` as the sole accepting state. The transition function is clearly defined for each input symbol, and it is confirmed that the automaton is **not a non-deterministic finite automaton (NFA),** meaning it follows deterministic transition rules. A graphical representation of this finite automaton is available in `FA1.png`. Graph representation for the finite automaton given in previouos laboratory work can be seen at ['FA1.png'](../graph_drawings/FA1.png)

```
Converted to DFA
States: {'S', 'D', 'F', 'X'}
Alphabet: {'b', 'c', 'a'}
Start State: {'S'}
Accept States: {'X'}
Transitions:
{'S'} --(a)--> {'F'}
{'S'} --(b)--> {'S'}
{'F'} --(b)--> {'F'}
{'F'} --(c)--> {'D'}
{'F'} --(a)--> {'X'}
{'D'} --(c)--> {'S'}
{'D'} --(a)--> {'X'}
FA is NFA: False
```
Next, the **conversion from NFA to DFA** is performed, yielding a deterministic finite automaton with the same set of states, transitions, and accept states. The transition structure remains unchanged, reinforcing that the original automaton was already deterministic.  

```
Grammar converted from DFA
Non-terminals: {'S', 'D', 'F', 'X'}
Terminals: {'b', 'c', 'a'}
Start symbol: {'S'}
Production Rules:
{'S'} -> ['aF', 'bS'];
{'F'} -> ['bF', 'cD', 'a'];
{'D'} -> ['cS', 'a']
```
From the DFA, the **corresponding grammar** is reconstructed. This grammar consists of four non-terminal symbols (`S`, `D`, `F`, `X`), three terminal symbols (`a`, `b`, `c`), and production rules that map onto the DFA transitions. The structure closely mirrors the original right-linear grammar, confirming the correctness of the finite automaton conversion process.  

```
Checking some grammar types
Non-terminals: {'S', 'B', 'A', 'C'}
Terminals: {'b', 'c', 'a'}
Start symbol: {'S'}
Production Rules:
{'S'} -> ['AB', 'aS'];
{'A'} -> ['aA', 'bB'];
{'B'} -> ['bB', 'cC'];
{'B', 'A'} -> ['bAB', 'c'];
{'C'} -> ['cA', 'a']
Type 0 - Unrestricted Grammar

Non-terminals: {'S', 'B', 'A', 'C'}
Terminals: {'b', 'c', 'a'}
Start symbol: {'S'}
Production Rules:
{'S'} -> ['aAB', 'bS'];
{'A'} -> ['bAB', 'bC'];
{'B'} -> ['cB', 'aC'];
{'C', 'B'} -> ['cB', 'aC'];
{'C'} -> ['cA', 'a']
Type 1 - Context-Sensitive Grammar

Non-terminals: {'S', 'D', 'F'}
Terminals: {'b', 'c', 'a'}
Start symbol: {'S'}
Production Rules:
{'S'} -> ['aFaa', 'bS'];
{'F'} -> ['bF', 'bD', 'a'];
{'D'} -> ['cS', 'a']
Type 2 - Context-Free Grammar

Non-terminals: {'S', 'D', 'F'}
Terminals: {'b', 'c', 'a'}
Start symbol: {'S'}
Production Rules:
{'S'} -> ['Fa', 'Sb'];
{'F'} -> ['Fb', 'Dc', 'a'];
{'D'} -> ['Sc', 'a']
Type 3 - Left Linear Regular Grammar
```
Additionally, various **grammar classifications** are examined, including **Type 0 (Unrestricted), Type 1 (Context-Sensitive), Type 2 (Context-Free), and Type 3 (Regular)** grammars. The distinctions between them highlight differences in production rule constraints and structural characteristics, demonstrating a deeper exploration of grammar classifications beyond the initially provided regular grammar.  
```
Task from Lab 2
States: {'C', 'D', 'B', 'A'}
Alphabet: {'b', 'c', 'a'}
Start State: {'A'}
Accept States: {'C'}
Transitions:
{'A'} --(a)--> {'B'}
{'A'} --(b)--> {'A'}
{'B'} --(a)--> {'C'}
{'B'} --(c)--> {'B'}
{'C'} --(a)--> {'D'}
{'D'} --(a)--> {'D', 'B'}
FA is NFA: True
```

The **non-deterministic finite automaton (NFA)** from current lab task is analyzed, consisting of four states (`A`, `B`, `C`, `D`) with `A` as the start state and `C` as the accept state. The transitions include cases where a state moves to multiple possible next states, confirming its non-deterministic nature. Graph representation for this non-deterministic finite automaton can be seen at ['NFA.png'](../graph_drawings/NFA.png)

```
Converted to DFA
States: [{'A'}, {'B'}, {'C'}, {'D'}, {'D', 'B'}, {'C', 'D', 'B'}]
Alphabet: {'b', 'c', 'a'}
Start State: {'A'}
Accept States: [{'C'}, {'C', 'D', 'B'}]
Transitions:
{'A'} --(b)--> {'A'}
{'A'} --(a)--> {'B'}
{'B'} --(c)--> {'B'}
{'B'} --(a)--> {'C'}
{'C'} --(a)--> {'D'}
{'D'} --(a)--> {'D', 'B'}
{'D', 'B'} --(c)--> {'B'}
{'D', 'B'} --(a)--> {'C', 'D', 'B'}
{'C', 'D', 'B'} --(c)--> {'B'}
{'C', 'D', 'B'} --(a)--> {'C', 'D', 'B'}
FA is NFA: False
```

Finally, the **NFA is converted into a DFA**, expanding the number of states to include combinations of the original NFA states (`{A}`, `{B}`, `{C}`, `{D}`, `{D, B}`, `{C, D, B}`) while ensuring deterministic transitions. The accept states now include `{C}` and `{C, D, B}`, ensuring proper recognition of the language. Graph representation for the converted deterministic finite automaton can be seen at ['DFA.png'](../graph_drawings/DFA.png)

### **Conclusion**  
The results demonstrate a complete workflow for converting a regular grammar into a finite automaton, verifying determinism, transforming between NFA and DFA, and reconstructing the grammar from a DFA. The exploration of different grammar classifications provides additional insight into formal language theory. This structured approach ensures that the theoretical concepts of finite automata and formal grammars are well understood and correctly applied.
## References

<a id="bib1"></a>[1] Formal Languages and Finite Automata Guide for practical lessons Chapter 2 - TUM - https://else.fcim.utm.md/pluginfile.php/64791/mod_resource/content/0/Chapter_2.pdf