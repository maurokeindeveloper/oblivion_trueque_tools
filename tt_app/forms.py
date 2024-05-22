from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from .models import CustomUser, Producto
from django.core.exceptions import ValidationError
import datetime


def validate_age(value):
    birthdate = value
    day = int(birthdate.strftime("%d"))
    month = int(birthdate.strftime("%m"))
    year = int(birthdate.strftime("%Y"))
    today = datetime.date.today()
    age = today.year - year - ((today.month, today.day) < (month, day))
    if age < 18:
        raise ValidationError("Tenés que ser mayor de edad para registrarte.")


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        max_length=255,
        help_text="Ingresá tu dirección de correo.",
        widget=forms.TextInput(attrs={"class": "input mb-2", "style": "width: 100%;"}),
        error_messages={
            "required": "Tenés que completar el campo con tu email",
        },
    )
    first_name = forms.CharField(
        max_length=60,
        widget=forms.TextInput(attrs={"class": "input mb-2", "style": "width: 100%;"}),
        error_messages={
            "required": "Tenés que completar el campo con tu nombre",
        },
    )
    last_name = forms.CharField(
        max_length=60,
        widget=forms.TextInput(attrs={"class": "input mb-2", "style": "width: 100%;"}),
        error_messages={
            "required": "Tenés que completar el campo con tu apellido",
        },
    )
    dni = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={"class": "input mb-2", "style": "width: 100%;"}),
    )
    phone = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={"class": "input mb-2", "style": "width: 100%;"}),
    )
    birthdate = forms.DateField(
        validators=[validate_age],
        widget=forms.TextInput(attrs={"class": "input mb-2", "style": "width: 100%;"}),
        error_messages={
            "required": "Tu fecha de nacimiento es obligatoria",
        },
    )

    class Meta:
        model = CustomUser
        fields = (
            "email",
            "password1",
            "password2",
            "first_name",
            "last_name",
            "dni",
            "phone",
            "birthdate",
        )

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields["dni"].required = False
        self.fields["phone"].required = False

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        try:
            user = CustomUser.objects.get(email=email)
        except Exception as e:
            return email
        raise forms.ValidationError(f"El email {email} ya posee una cuenta.")


class CreacionDeProducto(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ["nombre", "descripcion", "categoria", "imagen"]

    nombre = forms.CharField(
        label="Nombre del producto",
        max_length=50,
        widget=forms.TextInput(attrs={"class": "input mb-2", "style": "width: 100%;"}),
        error_messages={
            "required": "Debe completar el campo de nombre del producto",
        },
    )
    descripcion = forms.CharField(
        label="Descripción",
        max_length=1000,
        min_length=10,
        widget=forms.Textarea(attrs={"class": "input mb-2", "style": "width: 100%;"}),
        error_messages={
            "required": "Debe completar el campo de descripción.",
            "min_length": "La descripción debe tener al menos 10 caracteres.",
        },
    )
    categoria = forms.ChoiceField(
        label="Categoria",
        choices=Producto.Categoria.choices,
        widget=forms.Select(
            attrs={"class": "form-select mb-2", "style": "width: 100%;"}
        ),
    )
    imagen = forms.ImageField(
        label="Imagen",
        required=False,
        widget=forms.FileInput(
            attrs={"class": "btn btn-outline-dark mb-4", "style": "width: 100%;"}
        ),
    )
    aceptar_terminos = forms.BooleanField(
        label="Aceptar términos y condiciones",
        required=True,
        error_messages={
            "required": "Debe aceptar los términos y condiciones para continuar.",
        },
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )
