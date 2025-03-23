from itertools import product


class RegexGenerator:
    def __init__(self, regex):
        self.regex = regex
        self.parsed_components = []
        self.process_steps = []

    def parse(self):
        i = 0
        while i < len(self.regex):
            char = self.regex[i]
            if char == '(':
                group_end = self.regex.find(')', i)
                group = self.regex[i + 1:group_end]
                options = group.split('|')
                self.parsed_components.append(options)
                self.process_steps.append(f"alternation: {options}")
                i = group_end + 1
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
            else:
                self.parsed_components.append([char])
                self.process_steps.append(f"single char: {char}")
                i += 1

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

    def show_processing_sequence(self):
        print("steps:")
        for step in self.process_steps:
            print(f"- {step}")
