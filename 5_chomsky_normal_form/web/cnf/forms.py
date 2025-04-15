from django import forms

class GrammarForm(forms.Form):
    non_terminals = forms.CharField(label="Non-terminals (comma-separated)", max_length=500)
    terminals = forms.CharField(label="Terminals (comma-separated)", max_length=500)
    start_symbol = forms.CharField(label="Start Symbol", max_length=100)
    production_rules = forms.CharField(
        label="Production Rules (format: S->A; A->aX,bX; ...)",
        widget=forms.Textarea
    )
