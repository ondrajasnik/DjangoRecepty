from django.shortcuts import render, get_object_or_404
from .models import Recept
from django.db.models import Q

def index(request):
    recepty = Recept.objects.all()
    return render(request, 'recepty/index.html', {'recepty': recepty})

def detail(request, pk):
    recept = get_object_or_404(Recept, pk=pk)
    return render(request, 'recepty/detail.html', {'recept': recept})

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
