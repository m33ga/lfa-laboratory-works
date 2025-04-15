from django.shortcuts import render
from .forms import GrammarForm
from fa import Grammar


def grammar_view(request):
    result = None
    if request.method == "POST":
        form = GrammarForm(request.POST)
        if form.is_valid():
            V_n = set(form.cleaned_data["non_terminals"].replace(" ", "").split(","))
            V_t = set(form.cleaned_data["terminals"].replace(" ", "").split(","))
            S = {form.cleaned_data["start_symbol"].strip()}

            raw_rules = form.cleaned_data["production_rules"]
            P = {}
            for rule in raw_rules.strip().split(";"):
                if "->" in rule:
                    lhs, rhs = rule.split("->")
                    lhs = lhs.strip()
                    rhs_list = [r.strip() for r in rhs.split(",")]
                    P[lhs] = rhs_list

            grammar = Grammar(V_n, V_t, P, S)
            print(grammar)
            grammar.normalize_cnf()

            result = str(grammar)

    else:
        form = GrammarForm()

    return render(request, "grammar_form.html", {"form": form, "result": result})
