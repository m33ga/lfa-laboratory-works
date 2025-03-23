# Regular Expressions

### Course: Formal Languages & Finite Automata
### Author: Mihai Gurduza
### Academic Group: FAF-233
### Variant: 4

----

## Theory
* `Regular Expression` (regex or regexp) - a sequence of characters that defines a pattern for text matching. [[1]](#ref1)

Used for:
* Searching for patterns in large bodies of text, often used in tools like grep and sed. 
* Ensuring user input matches a required format, such as email addresses or phone numbers. 
* Extracting relevant data from documents, logs, or web pages. 
* Performing "find and replace" operations or reformatting strings in text-processing tasks. 
* Identifying vulnerabilities in text data such as SQL injection patterns or malicious code.

## Objectives:

1. Write and cover what regular expressions are, what they are used for;

2. Below you will find 3 complex regular expressions per each variant. Take a variant depending on your number in the list of students and do the following:

    a. Write a code that will generate valid combinations of symbols conform given regular expressions (examples will be shown).

    b. In case you have an example, where symbol may be written undefined number of times, take a limit of 5 times (to evade generation of extremely long combinations);

    c. **Bonus point**: write a function that will show sequence of processing regular expression (like, what you do first, second and so on)


## Implementation description

* The `RegexGenerator` class is designed to parse a simplified regular expression and generate all possible strings that match the regex. It achieves this by breaking down the regex into its components, processing quantifiers (*, +, {}), alternations (|), and single characters, and then generating combinations of these components from their cartesian product.
---

* The following block in the `parse` method handles alternations (|) within parentheses. When encountering an opening parenthesis (, the code extracts the substring between the parentheses and splits it by the | character to identify alternative options. For example, (a|b|c) would be parsed into ['a', 'b', 'c']. These options are stored as a list in self.parsed_components for later use in generating combinations. The process step is logged in self.process_steps to provide a trace of how the regex was processed.

```python
if char == '(':
    group_end = self.regex.find(')', i)
    group = self.regex[i + 1:group_end]
    options = group.split('|')
    self.parsed_components.append(options)
    self.process_steps.append(f"alternation: {options}")
    i = group_end + 1
```

* The next section processes quantifiers, which specify how many times a preceding element should be repeated.
For example, the `*` Kleene Star matches zero or more repetitions of the preceding element. The code generates up to 5 repetitions (as specified in task) of the previous component and stores them as a list.
For the `+` operator it is similar to *, but ensures at least one repetition. The code generates repetitions from 1 to 5 (as specified in task). For the `{n}` operator it matches exactly n repetitions of the preceding element. If the previous component is a list (from alternation), the code uses itertools.product to compute the cartesian product of the list repeated n times. Otherwise, it simply repeats the string n times.
Each quantifier's expansion is logged in self.process_steps for transparency.

```python
elif char in ('*', '+') or char == '{':
    prev = self.parsed_components.pop()
    if char == '*':
        expanded = [''.join(prev) * n for n in range(6)]  # limit to 5 reps
        self.parsed_components.append(expanded)
        self.process_steps.append(f"expanded '*' for {prev} -> {expanded}")
        i += 1
    elif char == '+':
        expanded = [''.join(prev) * n for n in range(1, 6)]
        self.parsed_components.append(expanded)
        self.process_steps.append(f"expanded '+' for {prev} -> {expanded}")
        i += 1
    elif char == '{':
        repeat_end = self.regex.find('}', i)
        num_repeats = int(self.regex[i + 1:repeat_end])
        if isinstance(prev, list):
            expanded = [''.join(comb) for comb in product(prev, repeat=num_repeats)]
        else:
            expanded = [prev * num_repeats]

        self.parsed_components.append(expanded)
        self.process_steps.append(f"expanded '{{{num_repeats}}}' for {prev} -> {expanded}")
        i = repeat_end + 1
```
---

* The method `get_combinations` is used to generate all possible strings that match the regex by combining the parsed components. The self.parsed_components list contains the parsed elements of the regex, including alternations and expanded quantifiers.
Each component is flattened into a list of strings. For example, if a component is ['a', ['b', 'c']], it is flattened into ['a', 'b', 'c'].
Using itertools.product, the method computes the Cartesian product of all flattened components. This effectively generates all possible combinations of the regex components.
Each combination is joined into a single string, resulting in a list of all possible matches.

```python
def get_combinations(self):
    if not self.parsed_components:
        return []

    flattened = []
    for component in self.parsed_components:
        if isinstance(component, list):
            flattened_component = []
            for item in component:
                if isinstance(item, str):
                    flattened_component.append(item)
                elif isinstance(item, list):
                    flattened_component.extend(item)
            flattened.append(flattened_component)
        else:
            flattened.append([component])

    combinations_ = []
    for comb in product(*flattened):
        combinations_.append(''.join(comb))

    return combinations_
```

Finally, the `show_processing_sequence` method displays the steps taken in analyzing the regular expression provided.

---
## Results

Analyzing the results for each expression, we can see that it successfully identifies the rules and processes them accordingly. The resulting strings are all the possible combinations that follow the given expression (with number of `*` and `+`repetitions limited to 5)
```
example : (S|T)(U|V)W*Y+24
strings: ['SUY24', 'SUYY24', 'SUYYY24', 'SUYYYY24', 'SUYYYYY24', 'SUWY24', 'SUWYY24', 'SUWYYY24', 'SUWYYYY24', 'SUWYYYYY24', 'SUWWY24', 'SUWWYY24', 'SUWWYYY24', 'SUWWYYYY24', 'SUWWYYYYY24', 'SUWWWY24', 'SUWWWYY24', 'SUWWWYYY24', 'SUWWWYYYY24', 'SUWWWYYYYY24', 'SUWWWWY24', 'SUWWWWYY24', 'SUWWWWYYY24', 'SUWWWWYYYY24', 'SUWWWWYYYYY24', 'SUWWWWWY24', 'SUWWWWWYY24', 'SUWWWWWYYY24', 'SUWWWWWYYYY24', 'SUWWWWWYYYYY24', 'SVY24', 'SVYY24', 'SVYYY24', 'SVYYYY24', 'SVYYYYY24', 'SVWY24', 'SVWYY24', 'SVWYYY24', 'SVWYYYY24', 'SVWYYYYY24', 'SVWWY24', 'SVWWYY24', 'SVWWYYY24', 'SVWWYYYY24', 'SVWWYYYYY24', 'SVWWWY24', 'SVWWWYY24', 'SVWWWYYY24', 'SVWWWYYYY24', 'SVWWWYYYYY24', 'SVWWWWY24', 'SVWWWWYY24', 'SVWWWWYYY24', 'SVWWWWYYYY24', 'SVWWWWYYYYY24', 'SVWWWWWY24', 'SVWWWWWYY24', 'SVWWWWWYYY24', 'SVWWWWWYYYY24', 'SVWWWWWYYYYY24', 'TUY24', 'TUYY24', 'TUYYY24', 'TUYYYY24', 'TUYYYYY24', 'TUWY24', 'TUWYY24', 'TUWYYY24', 'TUWYYYY24', 'TUWYYYYY24', 'TUWWY24', 'TUWWYY24', 'TUWWYYY24', 'TUWWYYYY24', 'TUWWYYYYY24', 'TUWWWY24', 'TUWWWYY24', 'TUWWWYYY24', 'TUWWWYYYY24', 'TUWWWYYYYY24', 'TUWWWWY24', 'TUWWWWYY24', 'TUWWWWYYY24', 'TUWWWWYYYY24', 'TUWWWWYYYYY24', 'TUWWWWWY24', 'TUWWWWWYY24', 'TUWWWWWYYY24', 'TUWWWWWYYYY24', 'TUWWWWWYYYYY24', 'TVY24', 'TVYY24', 'TVYYY24', 'TVYYYY24', 'TVYYYYY24', 'TVWY24', 'TVWYY24', 'TVWYYY24', 'TVWYYYY24', 'TVWYYYYY24', 'TVWWY24', 'TVWWYY24', 'TVWWYYY24', 'TVWWYYYY24', 'TVWWYYYYY24', 'TVWWWY24', 'TVWWWYY24', 'TVWWWYYY24', 'TVWWWYYYY24', 'TVWWWYYYYY24', 'TVWWWWY24', 'TVWWWWYY24', 'TVWWWWYYY24', 'TVWWWWYYYY24', 'TVWWWWYYYYY24', 'TVWWWWWY24', 'TVWWWWWYY24', 'TVWWWWWYYY24', 'TVWWWWWYYYY24', 'TVWWWWWYYYYY24']
steps:
- alternation: ['S', 'T']
- alternation: ['U', 'V']
- single char: W
- expanded '*' for ['W'] -> ['', 'W', 'WW', 'WWW', 'WWWW', 'WWWWW']
- single char: Y
- expanded '+' for ['Y'] -> ['Y', 'YY', 'YYY', 'YYYY', 'YYYYY']
- single char: 2
- single char: 4

example : L(M|N)O{3}P*Q(2|3)
strings: ['LMOOOQ2', 'LMOOOQ3', 'LMOOOPQ2', 'LMOOOPQ3', 'LMOOOPPQ2', 'LMOOOPPQ3', 'LMOOOPPPQ2', 'LMOOOPPPQ3', 'LMOOOPPPPQ2', 'LMOOOPPPPQ3', 'LMOOOPPPPPQ2', 'LMOOOPPPPPQ3', 'LNOOOQ2', 'LNOOOQ3', 'LNOOOPQ2', 'LNOOOPQ3', 'LNOOOPPQ2', 'LNOOOPPQ3', 'LNOOOPPPQ2', 'LNOOOPPPQ3', 'LNOOOPPPPQ2', 'LNOOOPPPPQ3', 'LNOOOPPPPPQ2', 'LNOOOPPPPPQ3']
steps:
- single char: L
- alternation: ['M', 'N']
- single char: O
- expanded '{3}' for ['O'] -> ['OOO']
- single char: P
- expanded '*' for ['P'] -> ['', 'P', 'PP', 'PPP', 'PPPP', 'PPPPP']
- single char: Q
- alternation: ['2', '3']

example : R*(S|T|U|V)W(X|Y|Z){2}
strings: ['SWXX', 'SWXY', 'SWXZ', 'SWYX', 'SWYY', 'SWYZ', 'SWZX', 'SWZY', 'SWZZ', 'TWXX', 'TWXY', 'TWXZ', 'TWYX', 'TWYY', 'TWYZ', 'TWZX', 'TWZY', 'TWZZ', 'UWXX', 'UWXY', 'UWXZ', 'UWYX', 'UWYY', 'UWYZ', 'UWZX', 'UWZY', 'UWZZ', 'VWXX', 'VWXY', 'VWXZ', 'VWYX', 'VWYY', 'VWYZ', 'VWZX', 'VWZY', 'VWZZ', 'RSWXX', 'RSWXY', 'RSWXZ', 'RSWYX', 'RSWYY', 'RSWYZ', 'RSWZX', 'RSWZY', 'RSWZZ', 'RTWXX', 'RTWXY', 'RTWXZ', 'RTWYX', 'RTWYY', 'RTWYZ', 'RTWZX', 'RTWZY', 'RTWZZ', 'RUWXX', 'RUWXY', 'RUWXZ', 'RUWYX', 'RUWYY', 'RUWYZ', 'RUWZX', 'RUWZY', 'RUWZZ', 'RVWXX', 'RVWXY', 'RVWXZ', 'RVWYX', 'RVWYY', 'RVWYZ', 'RVWZX', 'RVWZY', 'RVWZZ', 'RRSWXX', 'RRSWXY', 'RRSWXZ', 'RRSWYX', 'RRSWYY', 'RRSWYZ', 'RRSWZX', 'RRSWZY', 'RRSWZZ', 'RRTWXX', 'RRTWXY', 'RRTWXZ', 'RRTWYX', 'RRTWYY', 'RRTWYZ', 'RRTWZX', 'RRTWZY', 'RRTWZZ', 'RRUWXX', 'RRUWXY', 'RRUWXZ', 'RRUWYX', 'RRUWYY', 'RRUWYZ', 'RRUWZX', 'RRUWZY', 'RRUWZZ', 'RRVWXX', 'RRVWXY', 'RRVWXZ', 'RRVWYX', 'RRVWYY', 'RRVWYZ', 'RRVWZX', 'RRVWZY', 'RRVWZZ', 'RRRSWXX', 'RRRSWXY', 'RRRSWXZ', 'RRRSWYX', 'RRRSWYY', 'RRRSWYZ', 'RRRSWZX', 'RRRSWZY', 'RRRSWZZ', 'RRRTWXX', 'RRRTWXY', 'RRRTWXZ', 'RRRTWYX', 'RRRTWYY', 'RRRTWYZ', 'RRRTWZX', 'RRRTWZY', 'RRRTWZZ', 'RRRUWXX', 'RRRUWXY', 'RRRUWXZ', 'RRRUWYX', 'RRRUWYY', 'RRRUWYZ', 'RRRUWZX', 'RRRUWZY', 'RRRUWZZ', 'RRRVWXX', 'RRRVWXY', 'RRRVWXZ', 'RRRVWYX', 'RRRVWYY', 'RRRVWYZ', 'RRRVWZX', 'RRRVWZY', 'RRRVWZZ', 'RRRRSWXX', 'RRRRSWXY', 'RRRRSWXZ', 'RRRRSWYX', 'RRRRSWYY', 'RRRRSWYZ', 'RRRRSWZX', 'RRRRSWZY', 'RRRRSWZZ', 'RRRRTWXX', 'RRRRTWXY', 'RRRRTWXZ', 'RRRRTWYX', 'RRRRTWYY', 'RRRRTWYZ', 'RRRRTWZX', 'RRRRTWZY', 'RRRRTWZZ', 'RRRRUWXX', 'RRRRUWXY', 'RRRRUWXZ', 'RRRRUWYX', 'RRRRUWYY', 'RRRRUWYZ', 'RRRRUWZX', 'RRRRUWZY', 'RRRRUWZZ', 'RRRRVWXX', 'RRRRVWXY', 'RRRRVWXZ', 'RRRRVWYX', 'RRRRVWYY', 'RRRRVWYZ', 'RRRRVWZX', 'RRRRVWZY', 'RRRRVWZZ', 'RRRRRSWXX', 'RRRRRSWXY', 'RRRRRSWXZ', 'RRRRRSWYX', 'RRRRRSWYY', 'RRRRRSWYZ', 'RRRRRSWZX', 'RRRRRSWZY', 'RRRRRSWZZ', 'RRRRRTWXX', 'RRRRRTWXY', 'RRRRRTWXZ', 'RRRRRTWYX', 'RRRRRTWYY', 'RRRRRTWYZ', 'RRRRRTWZX', 'RRRRRTWZY', 'RRRRRTWZZ', 'RRRRRUWXX', 'RRRRRUWXY', 'RRRRRUWXZ', 'RRRRRUWYX', 'RRRRRUWYY', 'RRRRRUWYZ', 'RRRRRUWZX', 'RRRRRUWZY', 'RRRRRUWZZ', 'RRRRRVWXX', 'RRRRRVWXY', 'RRRRRVWXZ', 'RRRRRVWYX', 'RRRRRVWYY', 'RRRRRVWYZ', 'RRRRRVWZX', 'RRRRRVWZY', 'RRRRRVWZZ']
steps:
- single char: R
- expanded '*' for ['R'] -> ['', 'R', 'RR', 'RRR', 'RRRR', 'RRRRR']
- alternation: ['S', 'T', 'U', 'V']
- single char: W
- alternation: ['X', 'Y', 'Z']
- expanded '{2}' for ['X', 'Y', 'Z'] -> ['XX', 'XY', 'XZ', 'YX', 'YY', 'YZ', 'ZX', 'ZY', 'ZZ']

```

## Conclusions

The laboratory work demonstrates the successful implementation of a `RegexGenerator` class capable of parsing simple regular expressions and generating almost all possible matching strings. The generator handles regex components such as alternations (|), quantifiers (*, +, {}), and combinations of these elements, producing comprehensive sets of valid strings. Each step of the parsing process is logged, providing a way to see how the regex is interpreted and processed. However, the current approach has some limitations compared to more formal methods, such as converting the regex to a Non-Deterministic Finite Automaton (`Thompson's construction` [[2]](#ref2)). While the generator works well for small-scale examples, it may struggle with scalability for complex or deeply nested regex patterns due to its reliance on explicit enumeration of possibilities. Additionally, the current implementation lacks support for advanced regex features like character classes ([a-z]) or lookaheads/lookbehinds, which are naturally handled by NFA-based algorithms. Despite these limitations, the RegexGenerator served as a good starting tool for understanding regex behavior.

## References

<a id="ref1"></a>[1] "Regular expression"
 https://en.wikipedia.org/wiki/Regular_expression#

<a id="ref2"></a>[2] "Thompson's construction"
 https://en.wikipedia.org/wiki/Thompson%27s_construction