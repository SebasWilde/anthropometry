from django import forms
from .models import (
    Deportista,
    DeportistaInfo,
    Deporte,
    Categoria,
    Institucion,
    Medida,
)


class DeportistaForm(forms.ModelForm):
    class Meta:
        model = Deportista
        exclude = ['fecha_registro']


class DeportistaInfoForm(forms.ModelForm):
    class Meta:
        model = DeportistaInfo
        exclude = ['deportista']


class DeporteForm(forms.ModelForm):
    class Meta:
        model = Deporte
        fields = '__all__'


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = '__all__'


class InstitucionForm(forms.ModelForm):
    class Meta:
        model = Institucion
        fields = '__all__'


class MedidaForm(forms.ModelForm):
    class Meta:
        model = Medida
        fields = '__all__'
