from django import forms
from .models import Exercise, Athlete


class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ['name', 'text', 'difficulty', 'img']
        widgets = {'name': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombre',
        }), 'text': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Texto',
        }), 'difficulty': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Dificultad',
        })
        }


class create_athlete_form(forms.Form):
    email       = forms.CharField(label='', 
                                widget=forms.TextInput(attrs={"placeholder": "Email del atleta"}))
    name        = forms.CharField(label='', 
                                widget=forms.TextInput(attrs={"placeholder": "Nombre del atleta"}))
    last_name   = forms.CharField(label='', 
                                widget=forms.TextInput(attrs={"placeholder": "Apellido del atleta"}))