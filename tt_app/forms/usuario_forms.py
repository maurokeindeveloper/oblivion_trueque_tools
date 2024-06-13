from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from ..models import Usuario, Sucursal
from django.core.exceptions import ValidationError
import datetime


def check_cliente(user):
    return {
        "ok": user.is_staff,
        "return": HttpResponse("Debes ser cliente para acceder a esta página."),
    }


def check_empleado(user):
    return {
        "ok": (not user.is_staff) or user.is_admin,
        "return": HttpResponse("Debes ser empleado para acceder a esta página."),
    }


def check_administrador(user):
    return {
        "ok": not user.is_admin,
        "return": HttpResponse("Debes ser administrador para acceder a esta página."),
    }


def validate_age(value):
    birthdate = value
    day = int(birthdate.strftime("%d"))
    month = int(birthdate.strftime("%m"))
    year = int(birthdate.strftime("%Y"))
    today = datetime.date.today()
    age = today.year - year - ((today.month, today.day) < (month, day))
    if age < 18:
        raise ValidationError("Debe ser mayor de edad para registrarte.")


class IngresoForm(forms.Form):
    email = forms.EmailField(
        required=True,
        label="Email",
        widget=forms.TextInput(
            attrs={"autofocus": True, "class": "form-control w-100 mt-2 mb-3"}
        ),
        error_messages={"required": "Ingrese un email."},
    )
    password = forms.CharField(
        required=True,
        label="Contraseña",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "current-password",
                "class": "form-control w-100 mt-2 mb-3",
            }
        ),
        error_messages={"required": "Ingrese una contraseña."},
    )


class RegistrarEmpleado(forms.ModelForm):
    email = forms.EmailField(
        required=True,
        label="Email *",
        max_length=50,
        widget=forms.TextInput(
            attrs={"class": "", "placeholder": "Ingresá un correo electrónico"}
        ),
        error_messages={
            "required": "Debe completar el campo de email.",
        },
    )
    first_name = forms.CharField(
        required=True,
        label="Nombre *",
        max_length=50,
        widget=forms.TextInput(attrs={"class": "", "placeholder": "Ingresá un nombre"}),
        error_messages={
            "required": "Debe completar el campo de nombre.",
        },
    )
    last_name = forms.CharField(
        required=True,
        label="Apellido *",
        max_length=50,
        widget=forms.TextInput(
            attrs={"class": "", "placeholder": "Ingresá un apellido"}
        ),
        error_messages={
            "required": "Debe completar el campo de apellido.",
        },
    )
    password = forms.CharField(
        required=True,
        label="Contraseña *",
        max_length=50,
        widget=forms.PasswordInput(
            attrs={
                "class": "",
                "type": "password",
                "placeholder": "Ingresá tu contraseña",
            }
        ),
        error_messages={
            "required": "Debe completar el campo de contraseña.",
        },
    )
    sucursal = forms.ModelChoiceField(
        required=True,
        label="Sucursal de trabajo",
        queryset=Sucursal.objects.exclude(activo=False).order_by(
            "ciudad"
        ),  # el query del modelo a mostrar como seleccionables (se imprime su def __str__(self) definido en models.py )
        empty_label=None,  # esto es porque el forms.ModelChoiceField por defecto deja elegir vacío.
        widget=forms.Select(attrs={"class": "form-select", "placeholder": ""}),
        error_messages={
            "required": "Debe seleccionar una sucursal.",
        },
    )

    class Meta:
        model = Usuario
        fields = ["email", "first_name", "last_name", "password", "sucursal"]

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        try:
            user = Usuario.objects.get(email=email)
        except Exception as e:
            return email
        raise forms.ValidationError(f"El email {email} ya está registrado.")

    def __init__(self, *args, **kwargs):
        super().__init__(
            *args, **kwargs
        )  # Aca van las clases bootstrap a aplicar en todos los widgets de este form
        for field in self.fields:
            self.fields[field].widget.attrs["class"] += (
                " " + "form-control w-100 mt-2 mb-3"
            )  # IMPORTANTE: += para que no sobreesrciba las clases individuales de cada uno, Y MUY IMPORTANTE el primer espacio en " " porque sino se aplica mal.(se concatena con la ultima letra de la ultima clase individualmente definida)


class RegistrationForm(UserCreationForm):

    email = forms.EmailField(
        required=True,
        label="Correo electrónico *",
        max_length=255,
        widget=forms.TextInput(
            attrs={"class": "", "placeholder": "Ingresá tu correo electrónico"}
        ),
        error_messages={
            "required": "El email es obligatorio.",
        },
    )
    first_name = forms.CharField(
        required=True,
        label="Nombre *",
        max_length=60,
        widget=forms.TextInput(attrs={"class": "", "placeholder": "Ingresá tu nombre"}),
        error_messages={
            "required": "Debe ingresar su nombre.",
        },
    )
    last_name = forms.CharField(
        required=True,
        label="Apellido *",
        max_length=60,
        widget=forms.TextInput(
            attrs={"class": "", "placeholder": "Ingresá tu apellido"}
        ),
        error_messages={
            "required": "Debe ingresar su apellido.",
        },
    )
    dni = forms.CharField(
        required=False,
        label="DNI",
        max_length=20,
        widget=forms.TextInput(
            attrs={"class": "", "type": "number", "placeholder": "Ingresá tu DNI"}
        ),
    )
    phone = forms.CharField(
        required=False,
        label="Teléfono",
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "class": "",
                "type": "tel",
                "placeholder": "Ingresá tu número de teléfono",
            }
        ),
    )
    birthdate = forms.DateField(
        required=True,
        label="Fecha de nacimiento *",
        validators=[validate_age],
        widget=forms.DateInput(attrs={"class": "", "type": "date"}),
        error_messages={
            "required": "Debe ingresar fecha de nacimiento.",
        },
    )

    password1 = forms.CharField(
        required=True,
        label="Contraseña *",
        widget=forms.PasswordInput(
            attrs={
                "class": "",
                "type": "password",
                "placeholder": "Ingresá tu contraseña",
            }
        ),
        error_messages={"required": "La contraseña es obligatoria."},
    )

    password2 = forms.CharField(
        required=True,
        label="Confirmar contraseña *",
        widget=forms.PasswordInput(
            attrs={
                "class": "",
                "type": "password",
                "placeholder": "Confirmá tu contraseña",
            }
        ),
        error_messages={"required": "La confirmación de la contraseña es obligatoria."},
    )

    class Meta:
        model = Usuario
        fields = (
            "email",
            "first_name",
            "last_name",
            "dni",
            "phone",
            "birthdate",
            "password1",
            "password2",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for (
            field
        ) in (
            self.fields
        ):  # Aca van las clases bootstrap a aplicar en todos los widgets de este form
            self.fields[field].widget.attrs["class"] += (
                " " + "form-control w-100 mt-2 mb-3"
            )  # IMPORTANTE: += para que no sobreesrciba las clases individuales de cada uno, Y MUY IMPORTANTE el primer espacio en " " porque sino se aplica mal.(se concatena con la ultima letra de la ultima clase individualmente definida)

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        try:
            user = Usuario.objects.get(email=email)
        except Exception as e:
            return email
        raise forms.ValidationError(f"El email {email} ya está registrado.")
