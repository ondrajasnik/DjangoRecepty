from django.contrib import admin
from .models import Recept, Surovina

class SurovinaInline(admin.TabularInline):
    model = Surovina
    extra = 1

@admin.register(Recept)
class ReceptAdmin(admin.ModelAdmin):
    list_display = ('nazev', 'kategorie', 'obtiznost', 'doba_pripravy', 'hodnoceni')
    list_filter = ('kategorie', 'obtiznost')
    search_fields = ('nazev', 'postup')
    inlines = [SurovinaInline]
