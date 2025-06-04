from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db import models
from .models import Recept, Recenze
from django.db.models import Q
from .forms import RecenzeForm, RegistrationForm, ReceptForm, SurovinaFormSet

def index(request):
    recepty = Recept.objects.all()
    
    # Filtrování podle obtížnosti
    obtiznost = request.GET.get('obtiznost')
    if obtiznost:
        recepty = recepty.filter(obtiznost=obtiznost)
    
    # Filtrování podle vyhledávání
    q = request.GET.get('q')
    if q:
        recepty = recepty.filter(nazev__icontains=q)
    
    # Řazení
    razeni = request.GET.get('razeni')
    if razeni == 'hodnoceni':
        recepty = recepty.order_by('-hodnoceni')
    elif razeni == 'obtiznost':
        recepty = recepty.order_by('obtiznost')
    
    return render(request, 'recepty/index.html', {'recepty': recepty})

def detail(request, pk):
    recept = get_object_or_404(Recept, pk=pk)
    recenze = recept.recenze.all().order_by('-datum')
    
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'Pro přidání recenze se musíte přihlásit.')
            return redirect('recepty:login')
        
        form = RecenzeForm(request.POST)
        if form.is_valid():
            recenze = form.save(commit=False)
            recenze.recept = recept
            recenze.uzivatel = request.user
            recenze.save()
            
            # Aktualizace průměrného hodnocení receptu
            prumer = recept.recenze.aggregate(models.Avg('hodnoceni'))['hodnoceni__avg']
            recept.hodnoceni = round(prumer, 1) if prumer else 0
            recept.save()
            
            messages.success(request, 'Recenze byla úspěšně přidána.')
            return redirect('recepty:detail', pk=pk)
    else:
        form = RecenzeForm()
    
    context = {
        'recept': recept,
        'recenze': recenze,
        'form': form
    }
    return render(request, 'recepty/detail.html', context)

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registrace proběhla úspěšně!')
            return redirect('recepty:index')
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

class ReceptCreateView(LoginRequiredMixin, CreateView):
    model = Recept
    form_class = ReceptForm
    template_name = 'recepty/recept_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['suroviny_formset'] = SurovinaFormSet(self.request.POST, instance=self.object)
        else:
            context['suroviny_formset'] = SurovinaFormSet(instance=self.object)
        return context
    
    def form_valid(self, form):
        context = self.get_context_data()
        suroviny_formset = context['suroviny_formset']
        form.instance.autor = self.request.user
        form.instance.hodnoceni = 0  # Výchozí hodnocení pro nový recept
        self.object = form.save()
        if suroviny_formset.is_valid():
            suroviny_formset.instance = self.object
            suroviny_formset.save()
            messages.success(self.request, 'Recept byl úspěšně vytvořen!')
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

class ReceptUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Recept
    form_class = ReceptForm
    template_name = 'recepty/recept_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['suroviny_formset'] = SurovinaFormSet(self.request.POST, instance=self.object)
        else:
            context['suroviny_formset'] = SurovinaFormSet(instance=self.object)
        return context
    
    def form_valid(self, form):
        context = self.get_context_data()
        suroviny_formset = context['suroviny_formset']
        if suroviny_formset.is_valid():
            self.object = form.save()
            suroviny_formset.instance = self.object
            suroviny_formset.save()
            messages.success(self.request, 'Recept byl úspěšně upraven!')
            return super().form_valid(form)
        else:
            return self.form_invalid(form)
    
    def test_func(self):
        recept = self.get_object()
        return self.request.user == recept.autor

class ReceptDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Recept
    success_url = reverse_lazy('recepty:index')
    template_name = 'recepty/recept_confirm_delete.html'
    
    def test_func(self):
        recept = self.get_object()
        return self.request.user == recept.autor
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Recept byl úspěšně smazán!')
        return super().delete(request, *args, **kwargs)
