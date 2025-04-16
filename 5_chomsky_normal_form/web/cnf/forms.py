from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field
from crispy_bootstrap5.bootstrap5 import FloatingField


class GrammarBasicForm(forms.Form):
    non_terminals = forms.CharField(
        label="Non-terminals (comma-separated)",
        max_length=500,
    )
    terminals = forms.CharField(
        label="Terminals (comma-separated)",
        max_length=500,
    )
    start_symbol = forms.CharField(
        label="Start Symbol",
        max_length=100,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            FloatingField("non_terminals"),
            FloatingField("terminals"),
            FloatingField("start_symbol"),
            Submit("submit", "Next: Add Productions", css_class="btn btn-primary"),
        )

    def clean(self):
        cleaned_data = super().clean()

        raw_nt = cleaned_data.get("non_terminals", "")
        raw_s = cleaned_data.get("start_symbol", "")

        non_terminals = set(raw_nt.replace(" ", "").split(","))

        if raw_s.strip() not in non_terminals:
            self.add_error(
                "start_symbol",
                f"The start symbol '{raw_s}' must be one of the non-terminals: {', '.join(non_terminals)}."
            )

        return cleaned_data


def generate_production_form(non_terminals, terminals):
    class ProductionForm(forms.Form):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.valid_symbols = set(non_terminals).union(set(terminals))

            self.helper = FormHelper()
            self.helper.form_method = "post"
            self.helper.layout = Layout(
                *[Field(nt) for nt in non_terminals],
                Submit("submit", "Normalize to CNF", css_class="btn btn-success"),
            )

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
            label=f"Productions for {nt} ->",
            required=False,
            widget=forms.TextInput(attrs={"placeholder": f"ex: Aa, Bb, b"}),
        )

    return ProductionForm