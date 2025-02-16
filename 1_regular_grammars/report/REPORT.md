# Intro to formal languages. Regular grammars. Finite Automata.


### Course: Formal Languages & Finite Automata
### Author: Mihai Gurduza

----

## Theory
#### Some important definitions:
* An **alphabet** is a finite non-empty set of symbols.
* A **string/word** is a finite sequence of symbols from the *alphabet*
* A **language** is a set of words made from an alphabet



## Objectives:

* Understand the concept of formal languages and their defining components.
* Set up a GitHub repository for project storage and updates.
* Choose a programming language that simplifies problem-solving.
* Implement a *Grammar* class with:
  * A method to generate 5 valid strings.
  * A conversion function to transform it into a Finite Automaton.
* Implement a *Finite Automaton* class with a method to check if a string belongs to the language.


## Implementation description

* Following the implementation tips from the task, I started by defining the Grammar class in order to represent a regular grammar. To initialize the grammar instance 
with the given symbols, rules and start symbol, the constructor is used. 

```python
class Grammar:
    def __init__(self, V_n, V_t, P, S):
        self.V_n = V_n
        self.V_t = V_t
        self.P = P
        self.S = S
```

* Next, in order to generate valid strings, I defined the *generate_string* method.
It starts with initial starting symbol 
* keeps replacing a random non-terminal from the string with one of the associated
production rules
* until it gets to maximum length(default=10) or only terminal symbols remain.
* ***This is currently a weak point, because if no max length constraint is defined, then, because some production rules are recursive, they may infinitely loop and never finish generating a word. On the other hand, if the max length constraint is set, some generated words are not valid ones and will contain non-terminal symbol.***
```python
# Grammar class
def generate_string(self, max_length=10):
    current_string = self.S

    for i in range(max_length):
        non_terminals = [c for c in current_string if c in self.V_n]
        if not non_terminals:
            break

        nt = random.choice(non_terminals)
        replacement = random.choice(self.P[nt])
        print(f"{current_string} ->")
        current_string = current_string.replace(nt, replacement, 1)

    return current_string
```
* The *FiniteAutomaton* class has a constructor to initialize an instance with states, alphabet, transitions, starting state and accepting states.

```python
class FiniteAutomaton:
    def __init__(self, states, alphabet, transitions, start_state, accept_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.accept_states = accept_states
```

* The *to_finite_automaton method* inside the **Grammar** class
converts the grammar to a finite automaton
* It defines the *states* as all nonterminals and also adds an *accept state*
* Also, it creates the *transitions* based on the production rules:
  * If rule produces only a terminal -> it gets mapped to accept state (*q_accept*)
  * If rule contains terminal and non-terminal -> it maps the terminal to the remaining part.
```python
# Grammar class
def to_finite_automaton(self):
    states = self.V_n | {"q_accept"}
    alphabet = self.V_t
    transitions = {}
    start_state = self.S
    accept_states = {"q_accept"}

    for nt, productions in self.P.items():
        for production in productions:
            if len(production) == 1 and production in self.V_t:
                transitions.setdefault((nt, production), set()).add("q_accept")
            elif len(production) > 1:
                transitions.setdefault((nt, production[0]), set()).add(production[1:])

    return FiniteAutomaton(states, alphabet, transitions, start_state, accept_states)
```

* To check if a given string is accepted by the finite automaton, the *string_belongs_to_language* method is used.
* It starts at initial state (S)
* then, for each char in the string checks if a transition exists
* it keeps moving to the next state
* at the end, if the active state is an accept state, then the string is accepted.
```python
def string_belongs_to_language(self, input_string):
    current_states = {self.start_state}

    for symbol in input_string:
        next_states = set()
        for state in current_states:
            if (state, symbol) in self.transitions:
                next_states.update(self.transitions[(state, symbol)])
        if not next_states:
            return False
        current_states = next_states

    return any(state in self.accept_states for state in current_states)
```
* Next, I introduce the given alphabet and production rules (variant 12)
* I instantiate the grammar object
* And then i generate 5 valid words using the *generate_string* method

```python
# variant 12
vn = {"S", "F", "D"}
vt = {"a", "b", "c"}
p = {
    "S": ["aF", "bS"],
    "F": ["bF", "cD", "a"],
    "D": ["cS", "a"]
}

grammar = Grammar(vn, vt, p, "S")
generated_words = []
print("generating words:")
for i in range(5):
    generated_words.append(grammar.generate_string())
    print(generated_words[i])
    print()

print("generated words:")
for word in generated_words:
    print(word)
```

* Next, I convert the grammar to a finite automaton
* And then, I test if some simple strings are accepted by the finite automaton
* Also, I verify if the previously generated strings are accepted.

```python
fa = grammar.to_finite_automaton()
# some simple test cases
test_strings = ["aa", "abb", "aac", "baba", "bca"]
for test in test_strings:
    print(f"'{test}' accepted: {fa.string_belongs_to_language(test)}")

print('checking the previously generated words:')
for word in generated_words:
    print(f"'{word}' accepted: {fa.string_belongs_to_language(word)}")
```


## Conclusions / Screenshots / Results
* First, I will present one output 
  * variant information is displayed:
```
Non-terminals: {'F', 'S', 'D'}
Terminals: {'b', 'c', 'a'}
Rules:
S -> ['aF', 'bS']
F -> ['bF', 'cD', 'a']
D -> ['cS', 'a']
```
  * Next, I start generating 5 words and display the process in a familiar manner:
```
generating words:
S ->
bS ->
baF ->
babF ->
baba

S ->
aF ->
acD ->
aca

S ->
bS ->
baF ->
bacD ->
baca

S ->
bS ->
baF ->
baa

S ->
aF ->
acD ->
accS ->
accaF ->
accaa

generated words:
baba
aca
baca
baa
accaa
```

* After that, I check if some simple strings belong to the language:
```commandline
checking some simple strings belong to language
'aa' accepted: True
'abb' accepted: False
'aac' accepted: False
'baba' accepted: True
'bca' accepted: False
```

* Also, I check if the previously generated strings are accepted by the FA.
```commandline
checking the previously generated words:
'baba' accepted: True
'aca' accepted: True
'baca' accepted: True
'baa' accepted: True
'accaa' accepted: True
```

* #### In conclusion I can say that I successfully completed the given tasks. Also, by creating a Grammar and a Finite automaton, I got a better understanding of the concept of regular grammars, how words are formed and generated by the grammar and how grammars can be converted to FAs. 
## References

<a id="ref1"></a>[1] Formal Languages and Finite Automata Guide for practical lessons (TUM)

<a id="ref2"></a>[2] Converting	Regular	Grammar to DFA (JFLAP) - https://www.jflap.org/modules/ConvertedFiles/Regular%20Grammar%20to%20DFA%20Conversion%20Module.pdf

<a id="ref3"></a>[3] Transforming Regular Grammars to Equivalent Finite State Automata (UM) - http://www.cs.um.edu.mt/gordon.pace/Research/Software/Relic/Transformations/RG/toFSA.html


