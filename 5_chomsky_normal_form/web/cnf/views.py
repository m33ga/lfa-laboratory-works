from django.shortcuts import render
from .forms import GrammarBasicForm, generate_production_form
from fa import Grammar


def grammar_view(request):
    step = 1
    result = None
    form = GrammarBasicForm()
    production_form = None

    if request.method == "POST":
        if "step" in request.POST and request.POST["step"] == "2":
            non_terminals = request.POST.get("non_terminals").replace(" ", "").split(",")
            terminals = request.POST.get("terminals").replace(" ", "").split(",")
            start_symbol = request.POST.get("start_symbol").strip()
            ProductionForm = generate_production_form(non_terminals)
            production_form = ProductionForm(request.POST)

            if production_form.is_valid():
                V_n = set(non_terminals)
                V_t = set(terminals)
                S = {start_symbol}
                P = {}

                for nt in non_terminals:
                    rhs = production_form.cleaned_data.get(nt, "")
                    if rhs.strip() == "":
                        P[nt] = [""]
                    else:
                        P[nt] = [r.strip() if r.strip() else "" for r in rhs.split(",")]

                grammar = Grammar(V_n, V_t, P, S)
                print(grammar)
                grammar.normalize_cnf()
                result = str(grammar)

                form = GrammarBasicForm()
                production_form = None
            else:
                step = 2

        else:
            form = GrammarBasicForm(request.POST)
            if form.is_valid():
                step = 2
                non_terminals = form.cleaned_data["non_terminals"].replace(" ", "").split(",")
                ProductionForm = generate_production_form(non_terminals)
                production_form = ProductionForm()
    else:
        form = GrammarBasicForm()

    return render(
        request,
        "grammar_form.html",
        {
            "form": form,
            "production_form": production_form,
            "step": step,
            "result": result,
        }
    )
