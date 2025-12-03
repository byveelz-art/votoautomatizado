from django import forms
from adminApp.models import CandidatoOpcion

class CandidatoOpcionForm(forms.ModelForm):
    class Meta:
        model = CandidatoOpcion
        fields = ['eleccion', 'nombre_candidato', 'cargo', 'partido', 'lista']
        labels = {
            'eleccion': 'Elección',
            'nombre_candidato': 'Nombre del candidato',
            'cargo': 'Cargo',
            'partido': 'Partido',
            'lista': 'Lista',
        }
        widgets = {
            'eleccion': forms.Select(attrs={'class': 'form-select'}),
            'nombre_candidato': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Juan Pérez'}),
            'cargo': forms.Select(attrs={'class': 'form-select'}),
            'partido': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Partido Verde'}),
            'lista': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: A'}),
        }