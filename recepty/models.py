from django.db import models
from django.contrib.auth.models import User

class Recept(models.Model):
    KATEGORIE_VOLBY = [
        ('hlavni', 'Hlavní jídlo'),
        ('dezert', 'Dezert'),
        ('polevka', 'Polévka'),
        ('predkrm', 'Předkrm'),
        ('napoj', 'Nápoj'),
    ]

    OBTIZNOST_VOLBY = [
        ('lehka', 'Lehká'),
        ('stredni', 'Střední'),
        ('tezka', 'Těžká'),
    ]

    nazev = models.CharField(max_length=200)
    postup = models.TextField() 
    kategorie = models.CharField(max_length=20, choices=KATEGORIE_VOLBY)
    obtiznost = models.CharField(max_length=20, choices=OBTIZNOST_VOLBY)
    hodnoceni = models.FloatField(
        help_text="Hodnocení od 0 do 5",
    )
    doba_pripravy = models.PositiveIntegerField(help_text="Doba v minutách")
    obrazek = models.ImageField(upload_to='recepty/', blank=True, null=True)

    def __str__(self):
        return self.nazev

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.hodnoceni < 0 or self.hodnoceni > 5:
            raise ValidationError('Hodnocení musí být mezi 0 a 5.')

class Surovina(models.Model):
    recept = models.ForeignKey(Recept, related_name='suroviny', on_delete=models.CASCADE)
    nazev = models.CharField(max_length=100)
    mnozstvi = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.mnozstvi} {self.nazev}"

class Recenze(models.Model):
    recept = models.ForeignKey(Recept, related_name='recenze', on_delete=models.CASCADE)
    uzivatel = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # volitelné
    text = models.TextField()
    hodnoceni = models.PositiveSmallIntegerField(
        help_text="Hodnocení od 1 do 5",
        choices=[(i, str(i)) for i in range(1, 6)]
    )
    datum = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Recenze k {self.recept.nazev} od {self.uzivatel} ({self.hodnoceni}/5)"