from django import forms
from .models import Producto, Fabricante, Profile

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['codigo', 'modelo', 'nombre', 'descripcion', 'fabricante', 'estado', 'costo', 'precio', 'stock', 'imagen']

class FabricanteForm(forms.ModelForm):
    class Meta:
        model = Fabricante
        fields = ['fabricante', 'numero_productos', 'estado']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']


