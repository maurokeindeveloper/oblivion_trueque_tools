from django import forms
from .models import Producto

class CreacionDeProducto(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'categoria', 'imagen']

    nombre = forms.CharField(
        label='Nombre del producto', 
        max_length=50, 
        widget=forms.TextInput(attrs={'class': 'input mb-2', 'style': 'width: 100%;'})
    ) 
    descripcion = forms.CharField(
        label='Descripción',
        max_length=200,
        min_length=10,
        widget=forms.Textarea(attrs={'class': 'input mb-2', 'style': 'width: 100%;'})
    )
    categoria = forms.ChoiceField(
        label='Categoria',
        choices=Producto.Categoria.choices,
        widget=forms.Select(attrs={'class': 'form-select mb-2', 'style': 'width: 100%;'})
    )
    imagen = forms.ImageField(
        label="Imagen",
        required=False,
        widget=forms.FileInput(attrs={'class': 'btn btn-outline-dark mb-4', 'style': 'width: 100%;'})
    )