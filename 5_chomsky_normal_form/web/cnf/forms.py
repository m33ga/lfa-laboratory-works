from django import forms


class GrammarBasicForm(forms.Form):
    non_terminals = forms.CharField(label="Non-terminals (comma-separated)", max_length=500)
    terminals = forms.CharField(label="Terminals (comma-separated)", max_length=500)
    start_symbol = forms.CharField(label="Start Symbol", max_length=100)



def generate_production_form(non_terminals, terminals):
    class ProductionForm(forms.Form):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.valid_symbols = set(non_terminals).union(set(terminals))

        def clean(self):
            cleaned_data = super().clean()

            for nt in non_terminals:
                rhs = cleaned_data.get(nt, "").strip()
                if rhs:
                    productions = [r.strip() for r in rhs.split(",")]
                    for prod in productions:
                        for symbol in prod:
                            if symbol not in self.valid_symbols:
                                self.add_error(nt, f"Invalid symbol '{symbol}' in production for '{nt}'. "
                                                   "Symbols must be from the set of terminals or non-terminals.")
                                break
            return cleaned_data

    for nt in non_terminals:
        ProductionForm.base_fields[nt] = forms.CharField(
            label=f"{nt} → (comma-separated productions)",
            required=False
        )

    return ProductionForm
