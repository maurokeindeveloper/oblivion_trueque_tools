from django import forms
from .models import Producto

class CreacionDeProducto(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'categoria', 'imagen']

    nombre = forms.CharField(label='Nombre del producto', max_length=50, widget=forms.TextInput(attrs={'class': 'input'})) 
    descripcion = forms.CharField(
        label='Descripción',
        max_length=200,
        min_length=10,
        widget=forms.Textarea(attrs={'rows': 3, 'cols': 40})
    )
    categoria = forms.ChoiceField(choices=Producto.Categoria.choices)
    imagen = forms.ImageField(required=False)