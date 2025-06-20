from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Recenze, Recept, Surovina

class RecenzeForm(forms.ModelForm):
    class Meta:
        model = Recenze
        fields = ['text', 'hodnoceni']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'hodnoceni': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 5})
        }

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class SurovinaForm(forms.ModelForm):
    class Meta:
        model = Surovina
        fields = ['nazev', 'mnozstvi']
        widgets = {
            'nazev': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Např. mouka'
            }),
            'mnozstvi': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Např. 500g'
            })
        }

SurovinaFormSet = forms.inlineformset_factory(
    Recept,
    Surovina,
    form=SurovinaForm,
    extra=3,
    can_delete=True,
    fields=['nazev', 'mnozstvi']
)

class ReceptForm(forms.ModelForm):
    hodnoceni = forms.FloatField(
        widget=forms.HiddenInput(),
        initial=0,
        required=False
    )
    
    class Meta:
        model = Recept
        fields = ['nazev', 'postup', 'kategorie', 'obtiznost', 'doba_pripravy', 'obrazek', 'hodnoceni']
        widgets = {
            'nazev': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Např. Svíčková na smetaně'}),
            'postup': forms.Textarea(attrs={'class': 'form-control', 'rows': 10, 'placeholder': 'Popište postup přípravy krok za krokem...'}),
            'kategorie': forms.Select(attrs={'class': 'form-control'}),
            'obtiznost': forms.Select(attrs={'class': 'form-control'}),
            'doba_pripravy': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'obrazek': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['obrazek'].required = False
        
    def clean_doba_pripravy(self):
        doba = self.cleaned_data.get('doba_pripravy')
        if doba < 1:
            raise forms.ValidationError('Doba přípravy musí být alespoň 1 minuta.')
        return doba

    def clean(self):
        cleaned_data = super().clean()
        if 'hodnoceni' not in cleaned_data:
            cleaned_data['hodnoceni'] = 0
        return cleaned_data
