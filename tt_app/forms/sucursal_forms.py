from django import forms
from django.contrib.auth import authenticate
from ..models import Sucursal
from django.core.exceptions import ValidationError
import datetime
from django.db import models

class CrearSucursal(forms.ModelForm):
    ciudad = forms.CharField(
        required=True,
        label="Ciudad de la sucursal *",
        max_length=30,
        widget=forms.TextInput(
            attrs={"class": "", "placeholder": "Ingresá una ciudad"}
        ),
        error_messages={
            "required": "Debe ingresar la ciudad de la sucursal",
        },
    )
    direccion = forms.CharField(
        required=True,
        label="Dirección de la sucursal *",
        max_length=70,
        widget=forms.TextInput(
            attrs={"class": "", "placeholder": "Ingresá una dirección"}
        ),
        error_messages={
            "required": "Debe ingresar la dirección de la sucursal",
        },
    )

    class Meta:
        model = Sucursal
        fields = ["ciudad", "direccion"]

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs["class"] += " " + "form-control w-100 mt-2 mb-3" 

