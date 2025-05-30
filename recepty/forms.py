from django import forms
from .models import Recenze  # pokud se jmenuje model Recenze

class RecenzeForm(forms.ModelForm):
    class Meta:
        model = Recenze
        fields = ['hodnoceni', 'text']  # podle polí v modelu Recenze
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4}),
            'hodnoceni': forms.NumberInput(attrs={'min': 0, 'max': 5, 'step': 0.1}),
        }
