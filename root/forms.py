from django import forms
from .models import (
    Deportista,
    Deporte,
    Asociacion,
    Medida,
)


class DeportistaForm(forms.ModelForm):
    class Meta:
        model = Deportista
        exclude = ['fecha_registro']


class DeporteForm(forms.ModelForm):
    class Meta:
        model = Deporte
        fields = '__all__'


class AsociacionForm(forms.ModelForm):
    class Meta:
        model = Asociacion
        fields = '__all__'


class MedidaForm(forms.ModelForm):
    class Meta:
        model = Medida
        fields = '__all__'
