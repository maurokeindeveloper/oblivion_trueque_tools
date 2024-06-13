from django import forms
from django.contrib.auth import authenticate
from ..models import Venta
from django.core.exceptions import ValidationError
import datetime
from django.db import models

class CrearVenta(forms.ModelForm):
    nombre_producto = forms.CharField(
        required=True,
        label="Nombre del producto vendido *",
        max_length=50,
        widget=forms.TextInput(
            attrs={"class": "", "placeholder": "Ingresá un nombre"}
        ),
        error_messages={
            "required": "Debe ingresar nombre del producto",
        },
    )
    precio_unitario = forms.FloatField(
        required=True,
        label="Precio unitario*",
        min_value=0,
        widget=forms.NumberInput(
            attrs={"class": "", "placeholder": "Ingrese el precio"}
        ),
        error_messages={
            "required": "Debe ingresar un precio.",
            "min_value": "El precio debe ser un valor positivo.",
            # "invalid": "Debe ingresar un número válido.",
        },
    )
    cantidad_unidades = forms.FloatField(
        required=True,
        label="Cantidad de unidades*",
        min_value=0,
        widget=forms.NumberInput(
            attrs={"class": "", "placeholder": "Ingrese la cantidad de unidades"}
        ),
        error_messages={
            "required": "Debe ingresar una cantidad.",
            "min_value": "El precio debe ser un valor positivo.",
            # "invalid": "Debe ingresar un número válido.",
        },
    )

    class Meta:
        model = Venta
        fields = ["nombre_producto", "precio_unitario", "cantidad_unidades"]

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs["class"] += " " + "form-control w-100 mt-2 mb-3" 

