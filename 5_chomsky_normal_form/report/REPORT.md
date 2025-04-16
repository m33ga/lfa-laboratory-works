# Chomsky Normal Form

### Course: Formal Languages & Finite Automata
### Author: Mihai Gurduza
### Academic Group: FAF-233
### Variant: 12

----

## Theory
Chomsky Normal Form (CNF) is a standardized way of representing context-free grammars, where every production rule must follow one of two specific patterns: a rule that produces exactly two non-terminal symbols (e.g., A -> BC), a rule that produces a single terminal symbol (e.g., A -> a). [[1]](#ref1)

To transform a grammar into CNF, several steps are typically followed: removing null (epsilon) productions, eliminating unit productions (where a non-terminal directly leads to another non-terminal), discarding useless symbols (which are either unreachable or do not contribute to terminal strings), and converting long or mixed rules into simpler binary or terminal-only forms. [[3]](#ref3) For example, a rule like A -> BCD would be broken down into intermediate steps using new non-terminal symbols to ensure each production has only two non-terminals on the right-hand side. Similarly, terminals in longer rules are replaced with new non-terminals that directly produce those terminals. [[2]](#ref2)These transformations do not change the language of the grammar but ensure it fits the CNF structure, making it easier to analyze and implement algorithms for language recognition and parsing.

## Objectives:

1. Learn about Chomsky Normal Form (CNF) [[1]](#ref1).
2. Get familiar with the approaches of normalizing a grammar.
3. Implement a method for normalizing an input grammar by the rules of CNF.
    1. The implementation needs to be encapsulated in a method with an appropriate signature (also ideally in an appropriate class/type).
    2. The implemented functionality needs executed and tested.
    3. Also, another **BONUS point** would be given if the student will make the aforementioned function to accept any grammar, not only the one from the student's variant.

## Implementation Description

In the same `Grammar` class from the `fa` package, some new methods have been implemented to follow the next Chomsky normalization steps:

#### Step 1: Eliminate epsilon-productions
The first step in transforming a grammar into Chomsky Normal Form (CNF) is to eliminate epsilon-productions, which are productions that derive the empty string. This is crucial because CNF does not allow epsilon-productions except for the start symbol under specific conditions. The method `get_nullable` identifies nullable non-terminals—those that can derive epsilon—and the `eliminate_epsilon_productions` function removes these productions by generating all possible combinations of productions with nullable symbols removed. This ensures that the grammar remains equivalent while adhering to CNF requirements.

```python
def get_nullable(self):
    nullable = set()
    for lhs, rhs_list in self.P.items():
        for prod in rhs_list:
            if (prod == "" or prod in nullable) and lhs not in nullable:
                nullable.add(lhs)
                rhs_list.remove("")
    found = True
    while found:
        found = False
        for lhs, rhs_list in self.P.items():
            for prod in rhs_list:
                if prod in nullable and lhs not in nullable:
                    nullable.add(lhs)
                    found = True
    return nullable

def eliminate_epsilon_productions(self, nullable):
    for lhs, rhs_list in self.P.items():
        for idx, rhs in enumerate(rhs_list):
            if any(c in rhs for c in nullable):
                rhs_list[idx:idx+1] = self._get_combinations_replacing_epsilon(rhs, nullable)
```

---

#### Step 2: Eliminate Unit Productions
Unit productions, which are of the form A -> B where both A and B are non-terminals, are eliminated to simplify the grammar. These productions are replaced by directly including all productions derivable from B in A. The method `eliminate_unit_productions` achieves this by iteratively finding reachable states and adding their corresponding productions to the current non-terminal. This step ensures that the grammar no longer contains indirect derivations through unit productions.

```python
def eliminate_unit_productions(self):
    for lhs, rhs_list in self.P.items():
        reachable_states = set()
        additional_transitions = set()
        analyzed_states = set()
        found = False
        for rhs in rhs_list:
            if rhs in self.V_n:
                reachable_states.add(rhs)
                found = True
        while found:
            found = False
            for state in reachable_states.copy():
                if state not in analyzed_states:
                    for production in self.P[state]:
                        if production in self.V_n and production not in analyzed_states and production not in reachable_states:
                            found = True
                            reachable_states.add(production)
                        elif production not in additional_transitions:
                            additional_transitions.add(production)
                    analyzed_states.add(state)
        if len(additional_transitions) > 0:
            additional_transitions -= set(rhs_list)
            for element in additional_transitions:
                if element not in rhs_list:
                    rhs_list.append(element)
            for element in reachable_states:
                if element in rhs_list:
                    rhs_list.remove(element)
```

---

#### Step 3: Remove Non-Productive Symbols
Non-productive symbols are those that do not lead to any terminal strings. These symbols are redundant and must be removed to ensure that every non-terminal in the grammar contributes to deriving valid strings. The method `eliminate_nonproductive` identifies productive symbols by iteratively checking which non-terminals can derive terminals or other productive symbols. Any non-terminal that fails this check is removed from the grammar.

```python
def eliminate_nonproductive(self):
    productive = set()
    change_detected = True
    while change_detected:
        change_detected = False
        for lhs, rhs_list in self.P.items():
            for rhs in rhs_list:
                for symbol in rhs:
                    if ((symbol in self.V_t and len(rhs) == 1) or (symbol in productive)) and lhs not in productive:
                        productive.add(lhs)
                        change_detected = True
    unproductive = set(self.V_n) - productive
    for state in unproductive:
        del self.P[state]
        self.V_n.remove(state)
        if state in self.S:
            self.S.remove(state)
```

---

#### Step 4: Remove Inaccessible Symbols
Inaccessible symbols are those that cannot be reached from the start symbol through any sequence of productions. These symbols are also redundant and are removed to simplify the grammar. The method `eliminate_inaccessible` identifies accessible symbols by performing a reachability analysis starting from the start symbol. Any symbol not reachable is removed from the grammar.

```python
def eliminate_inaccessible(self):
    accessible = self.S.copy()
    change_detected = True
    while change_detected:
        change_detected = False
        for state in accessible.copy():
            for production in self.P[state]:
                for symbol in production:
                    if symbol in self.V_n and symbol not in accessible:
                        accessible.add(symbol)
                        change_detected = True
    inaccessible = set(self.V_n) - accessible
    for state in inaccessible:
        if state in self.P:
            del self.P[state]
        if state in self.V_n:
            self.V_n.remove(state)
```

---

#### Step 5: Replace Terminals and Long Productions
Finally, to achieve CNF, terminals in productions are replaced with new non-terminals, and long productions (with more than two symbols on the right-hand side) are broken down into binary productions. The method `replace_terminals` introduces new non-terminals for each terminal, while `replace_long_productions` recursively splits long productions into smaller binary rules. This ensures that all productions are either of the form A -> BC or A -> a.

```python
def replace_terminals(self):
    terminal_dict = {}
    if not self.V_n == set():
        for terminal in self.V_t:
            new_state = f"T_{terminal}"
            self.V_n.add(new_state)
            self.P[new_state] = list(terminal)
            terminal_dict[terminal] = new_state
        for lhs, rhs_list in self.P.items():
            new_rhs = []
            for rhs in rhs_list:
                if len(rhs) > 1:
                    new_rhs.append([terminal_dict.get(symbol, symbol) for symbol in rhs])
                else:
                    new_rhs.append(rhs)
            self.P[lhs] = new_rhs

def replace_long_productions(self):
    additional_productions = {}
    additional_productions_number = 0
    change_detected = True
    while change_detected:
        change_detected = False
        new_transitions = {}
        for lhs, rhs_list in self.P.items():
            for rhs in rhs_list:
                if len(rhs) > 2:
                    end_part_list = rhs[1:]
                    end_part = "".join(end_part_list)
                    if end_part in additional_productions:
                        new_state = additional_productions[end_part]
                    else:
                        new_state = f"X{additional_productions_number}"
                        additional_productions_number += 1
                        additional_productions[end_part] = new_state
                        new_transitions[new_state] = [end_part_list]
                        change_detected = True
                        self.V_n.add(new_state)
                    new_rhs = [rhs[0], new_state]
                    rhs_list.remove(rhs)
                    rhs_list.append(new_rhs)
        for lhs, rhs_list in new_transitions.items():
            self.P[lhs] = rhs_list
```

---

## Results
Given input for variant 12:
```
V_n = {S, A, B, C, D, X}
V_t = {a, b}
P = {
    "S": ["A"],
    "A": ["aX", "bX"],
    "X": ["", "BX", "b"],
    "B": ["AD"],
    "D": ["aD", "a"],
    "C": ["Ca"],
}
```

Results after normalization:
```
Step 1: Remove Epsilon Productions
Non-terminals: {'A', 'C', 'X', 'D', 'B', 'S'}
Terminals: {'b', 'a'}
Start symbol: {'S'}
Production Rules:
{S} -> ['A'];
{A} -> ['aX', 'bX'];
{B} -> ['BX', 'X', 'b'];
{C} -> ['AD'];
{D} -> ['aD', 'a'];
{X} -> ['Ca']

Step 2: Remove Unit Productions
Non-terminals: {'A', 'C', 'X', 'D', 'B', 'S'}
Terminals: {'b', 'a'}
Start symbol: {'S'}
Production Rules:
{S} -> ['aX', 'bX'];
{A} -> ['aX', 'bX'];
{B} -> ['BX', 'b', 'Ca'];
{C} -> ['AD'];
{D} -> ['aD', 'a'];
{X} -> ['Ca']

Step 3: Remove Non-Productive Symbols
Non-terminals: {'A', 'C', 'X', 'D', 'B', 'S'}
Terminals: {'b', 'a'}
Start symbol: {'S'}
Production Rules:
{S} -> ['aX', 'bX'];
{A} -> ['aX', 'bX'];
{B} -> ['BX', 'b', 'Ca'];
{C} -> ['AD'];
{D} -> ['aD', 'a'];
{X} -> ['Ca']

Step 4: Remove Inaccessible Symbols
Non-terminals: {'A', 'C', 'X', 'D', 'S'}
Terminals: {'b', 'a'}
Start symbol: {'S'}
Production Rules:
{S} -> ['aX', 'bX'];
{A} -> ['aX', 'bX'];
{C} -> ['AD'];
{D} -> ['aD', 'a'];
{X} -> ['Ca']

Result: Bring to Chomsky Normal Form (CNF)
Non-terminals: {'A', 'T_b', 'C', 'X', 'D', 'S', 'T_a'}
Terminals: {'b', 'a'}
Start symbol: {'S'}
Production Rules:
{S} -> [['T_a', 'X'], ['T_b', 'X']];
{A} -> [['T_a', 'X'], ['T_b', 'X']];
{C} -> [['A', 'D']];
{D} -> [['T_a', 'D'], 'a'];
{X} -> [['C', 'T_a']];
{T_b} -> ['b'];
{T_a} -> ['a']

```

The transformation of the grammar into Chomsky Normal Form (CNF) demonstrates a systematic normalization process. Initially, the grammar contained epsilon-productions, unit productions, and long productions that violated CNF requirements. After eliminating epsilon-productions, the nullable non-terminal X was handled, ensuring no empty derivations remained. The removal of unit productions simplified the grammar by replacing indirect derivations with direct ones, as seen in the elimination of S->A. Non-productive symbols like B were removed since they did not contribute to generating terminal strings, and inaccessible symbols were also eliminated to streamline the grammar. Finally, terminals were replaced with new non-terminals (T_a and T_b), and long productions were broken down into binary rules. For instance, the production X->Ca was transformed into X->[C,T_a], adhering to CNF's requirement that all productions be either of the form A->BC or A->a.

---

Additionally, a simple Django application has been created with some crispy forms which collect the set of terminals, non-terminals and starting state. Inputs are validated, and then a form for productions for each non-terminal is created. All normalization steps are displayed. Initially, only single-character states are accepted.  

![Input Step 1](/5_chomsky_normal_form/images/input_step_1.PNG)

![Input Step 2](/5_chomsky_normal_form/images/input_step_2.PNG)

![Result Part 1](/5_chomsky_normal_form/images/result_1.PNG)

![Result Part 2](/5_chomsky_normal_form/images/result_2.PNG)

![Result Part 3](/5_chomsky_normal_form/images/result_3.PNG)


## Conclusions
This laboratory work successfully implemented and demonstrated the transformation of a context-free grammar into Chomsky Normal Form (CNF). By systematically addressing epsilon-productions, unit productions, non-productive and inaccessible symbols, and restructuring terminals and long productions, the grammar was normalized while preserving its generative capacity. The modular design of the methods ensured clarity and correctness at each step, making the implementation robust and adaptable for any input grammar. This exercise not only reinforced the theoretical understanding of CNF but also highlighted its practical significance in simplifying grammars for applications such as parsing algorithms and compiler design. The final CNF grammar is now suitable for use in computational models that require strict adherence to CNF constraints.

## References
<a id="ref1"></a>[1] "Chomsky normal form"
 https://en.wikipedia.org/wiki/Chomsky_normal_form

<a id="ref2"></a>[2] "Chomsky normalization example, TUM "
 https://else.fcim.utm.md/pluginfile.php/66784/mod_resource/content/1/LabN3exemplu_engl.pdf

<a id="ref3"></a>[3] "Chomsky Normal Form, Clemson University"
 https://people.computing.clemson.edu/~goddard/texts/theoryOfComputation/9a.pdf
