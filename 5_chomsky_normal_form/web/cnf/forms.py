from django import forms


class GrammarBasicForm(forms.Form):
    non_terminals = forms.CharField(label="Non-terminals (comma-separated)", max_length=500)
    terminals = forms.CharField(label="Terminals (comma-separated)", max_length=500)
    start_symbol = forms.CharField(label="Start Symbol", max_length=100)


def generate_production_form(non_terminals):
    class ProductionForm(forms.Form):
        pass

    for nt in non_terminals:
        ProductionForm.base_fields[nt] = forms.CharField(
            label=f"{nt} → (comma-separated productions)",
            required=False
        )
    return ProductionForm
