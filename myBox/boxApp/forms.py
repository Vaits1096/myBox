from django import forms
from .models import Exercise


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
