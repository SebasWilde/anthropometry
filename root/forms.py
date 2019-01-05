from django import forms
from .models import Deportista


class DeportistaForm(forms.ModelForm):
    class Meta:
        model = Deportista
        exclude = ['fecha_registro']
