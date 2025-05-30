from django.shortcuts import render, get_object_or_404, redirect
from .models import Recept, Recenze
from django.db.models import Q
from .forms import RecenzeForm

def index(request):
    recepty = Recept.objects.all()
    dotaz = request.GET.get("q")
    if dotaz:
        recepty = recepty.filter(Q(nazev__icontains=dotaz))

    obtiznost = request.GET.get("obtiznost")
    if obtiznost:
        recepty = recepty.filter(obtiznost=obtiznost)

    razeni = request.GET.get("razeni")
    if razeni == "hodnoceni":
        recepty = recepty.order_by("-hodnoceni")
    elif razeni == "obtiznost":
        recepty = recepty.order_by("obtiznost")

    return render(request, "recepty/index.html", {"recepty": recepty})

def detail(request, pk):
    recept = get_object_or_404(Recept, pk=pk)
    recenze = recept.recenze.all().order_by('-datum')  # Nejdřív nejnovější

    if request.method == 'POST':
        form = RecenzeForm(request.POST)
        if form.is_valid():
            nova_recenze = form.save(commit=False)
            nova_recenze.recept = recept
            if request.user.is_authenticated:
                nova_recenze.uzivatel = request.user
            nova_recenze.save()
            return redirect('recepty:detail', pk=recept.pk)
    else:
        form = RecenzeForm()

    return render(request, 'recepty/detail.html', {
        'recept': recept,
        'recenze': recenze,
        'form': form,
    })
