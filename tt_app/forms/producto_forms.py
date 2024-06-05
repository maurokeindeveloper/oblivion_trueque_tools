from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from ..models import Sucursal, Usuario, Producto, Pregunta, Respuesta
from django.core.exceptions import ValidationError
import datetime
from django.db import models


class CreacionDeProducto(forms.ModelForm):
    nombre = forms.CharField(
        required=True,
        label="Nombre del producto *",
        max_length=50,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Ingresá un nombre"}
        ),
        error_messages={
            "required": "Debe ingresar nombre del producto",
        },
    )
    descripcion = forms.CharField(
        required=True,
        label="Descripción *",
        max_length=1000,
        min_length=10,
        widget=forms.Textarea(
            attrs={"class": "form-control", "placeholder": "Describí tu producto"}
        ),
        error_messages={
            "required": "Debe ingresar una descripción.",
            "min_length": "La descripción debe tener al menos 10 caracteres.",
        },
    )
    categoria = forms.ChoiceField(
        required=True,
        label="Categoria *",
        choices=Producto.Categoria.choices,
        widget=forms.Select(
            attrs={"class": "form-select", "placeholder": "Seleccioná una categoría"}
        ),
        error_messages={
            "required": "Debe seleccionar una categoría.",
        },
    )
    sucursal = forms.ModelChoiceField(
        required=True,
        label="Sucursal de preferencia *",
        queryset=Sucursal.objects.exclude(activo=False).order_by(
            "ciudad"
        ),  # el query del modelo a mostrar como seleccionables (se imprime su def __str__(self) definido en models.py )
        empty_label=None,  # esto es porque el forms.ModelChoiceField por defecto deja elegir vacío.
        widget=forms.Select(attrs={"class": "form-select", "placeholder": ""}),
        error_messages={
            "required": "Debe seleccionar una sucursal.",
        },
    )
    imagen = forms.ImageField(
        required=False,
        label="Imagen",
        widget=forms.FileInput(attrs={"class": "btn btn-outline-dark"}),
    )
    aceptar_terminos = forms.BooleanField(
        required=True,
        label="Aceptar términos y condiciones *",
        widget=forms.CheckboxInput(attrs={"class": "form-check-input mb-3"}),
        error_messages={
            "required": "Debe aceptar los términos y condiciones para continuar.",
        },
    )

    class Meta:
        model = Producto
        fields = ["nombre", "descripcion", "categoria", "sucursal", "imagen"]

    def __init__(self, *args, **kwargs):
        super(CreacionDeProducto, self).__init__(
            *args, **kwargs
        )  # Aca van las clases bootstrap a aplicar en todos los widgets de este form
        fields = (
            self.fields.copy()
        )  # Esto es para no afectar el dict que usa la pagina (sino se borra el ultimo item)
        fields.pop(
            "aceptar_terminos"
        )  # Aca sacamos el ultimo item(aceptar terminos) para no aplicarle los cambios
        for field in fields:
            self.fields[field].widget.attrs["class"] += (
                " " + "w-100 mt-2 mb-3"
            )  # IMPORTANTE: += para que no sobreesrciba las clases individuales de cada uno, Y MUY IMPORTANTE el primer espacio en " " porque sino se aplica mal.(se concatena con la ultima letra de la ultima clase individualmente definida)


class FormularioDePregunta(forms.ModelForm):
    class Meta:
        model = Pregunta
        fields = ["texto"]


class FormularioDeRespuesta(forms.ModelForm):
    class Meta:
        model = Respuesta
        fields = ["texto"]
