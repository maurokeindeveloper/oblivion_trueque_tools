from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from .models import Sucursal, Usuario, Producto, Pregunta, Respuesta
from django.core.exceptions import ValidationError
import datetime
from django.db import models


def validate_age(value):
    birthdate = value
    day = int(birthdate.strftime("%d"))
    month = int(birthdate.strftime("%m"))
    year = int(birthdate.strftime("%Y"))
    today = datetime.date.today()
    age = today.year - year - ((today.month, today.day) < (month, day))
    if age < 18:
        raise ValidationError("Debe ser mayor de edad para registrarte.")



class RegistrarEmpleado(forms.ModelForm):
    email = forms.EmailField(
        required=True,
        label="Email *",
        max_length=50,
        widget=forms.TextInput(
            attrs={ "class": "",
                    "placeholder":"Ingresá un correo electrónico"}
        ),
        error_messages={
            "required": "Debe completar el campo de email.",
        },
    )
    first_name = forms.CharField(
        required=True,
        label="Nombre *",
        max_length=50,
        widget=forms.TextInput(
            attrs={ "class": "",
                    "placeholder":"Ingresá un nombre"}
        ),
        error_messages={
            "required": "Debe completar el campo de nombre.",
        },
    )
    last_name = forms.CharField(
        required=True,
        label="Apellido *",
        max_length=50,
        widget=forms.TextInput(
            attrs={ "class": "",
                    "placeholder":"Ingresá un apellido"}
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
            attrs={ "class": "",
                    "type":"password",
                    "placeholder":"Ingresá tu contraseña"}
        ),
        error_messages={
            "required": "Debe completar el campo de contraseña.",
        },
    )

    class Meta:
        model = Usuario
        fields = ["email", "first_name", "last_name", "password"]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)              #Aca van las clases bootstrap a aplicar en todos los widgets de este form
        for field in self.fields:
            self.fields[field].widget.attrs["class"] += " " + "form-control w-100 mt-2 mb-3" #IMPORTANTE: += para que no sobreesrciba las clases individuales de cada uno, Y MUY IMPORTANTE el primer espacio en " " porque sino se aplica mal.(se concatena con la ultima letra de la ultima clase individualmente definida)
        
        
class RegistrationForm(UserCreationForm):

    email = forms.EmailField(
        required=True,
        label="Correo electrónico *",
        max_length=255,
        widget=forms.TextInput(
            attrs={ "class": "",
                    "placeholder":"Ingresá tu correo electrónico"}
        ),
        error_messages={
            "required": "El email es obligatorio.",
        },
    )
    first_name = forms.CharField(
        required=True,
        label="Nombre *",
        max_length=60,
        widget=forms.TextInput(
            attrs={ "class": "",
                    "placeholder":"Ingresá tu nombre"}
        ),
        error_messages={
            "required": "Debe ingresar su nombre.",
        },
    )
    last_name = forms.CharField(
        required=True,
        label="Apellido *",
        max_length=60,
        widget=forms.TextInput(
            attrs={ "class": "",
                    "placeholder":"Ingresá tu apellido"}
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
            attrs={ "class": "",
                    "placeholder":"Ingresá tu DNI"}
        ),
    )
    phone = forms.CharField(
        required=False,
        label="Teléfono",
        max_length=30,
        widget=forms.TextInput(
            attrs={ "class": "",
                    "placeholder":"Ingresá tu número de teléfono"}
        ),
    )
    birthdate = forms.DateField(
        required=True,
        label="Fecha de nacimiento *",
        validators=[validate_age],
        widget=forms.DateInput(
            attrs={ "class": "",
                    "type":"date"}
        ),
        error_messages={
            "required": "Debe ingresar fecha de nacimiento.",
        },
    )

    password1 = forms.CharField(
        required=True,
        label="Contraseña *",
        widget=forms.PasswordInput(
            attrs={ "class": "",
                    "type":"password",
                    "placeholder":"Ingresá tu contraseña"}
        ),
        error_messages={
            "required": "La contraseña es obligatoria."
        },
    )

    password2 = forms.CharField(
        required=True,
        label="Confirmar contraseña *",
        widget=forms.PasswordInput(
            attrs={ "class": "",
                    "type":"password",
                    "placeholder":"Confirmá tu contraseña"}
        ),
        error_messages={
            "required": "La confirmación de la contraseña es obligatoria."
        },
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
        for field in self.fields:                       #Aca van las clases bootstrap a aplicar en todos los widgets de este form
            self.fields[field].widget.attrs["class"] += " " + "form-control w-100 mt-2 mb-3" #IMPORTANTE: += para que no sobreesrciba las clases individuales de cada uno, Y MUY IMPORTANTE el primer espacio en " " porque sino se aplica mal.(se concatena con la ultima letra de la ultima clase individualmente definida)

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        try:
            user = Usuario.objects.get(email=email)
        except Exception as e:
            return email
        raise forms.ValidationError(f"El email {email} ya está registrado.")


class CreacionDeProducto(forms.ModelForm):

    nombre = forms.CharField(
        required=True,
        label="Nombre del producto *",
        max_length=50,
        widget=forms.TextInput(
            attrs={ "class": "form-control",
                    "placeholder":"Ingresá un nombre"}
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
            attrs={ "class": "form-control",
                    "placeholder":"Describí tu producto"}
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
            attrs={ "class": "form-select",
                    "placeholder":"Seleccioná una categoría"}
        ),
        error_messages={
            "required": "Debe seleccionar una categoría.",
        }
    )
    sucursal = forms.ModelChoiceField(
        required=True,
        label="Sucursal de preferencia *",
        queryset=Sucursal.objects.exclude(activo=False).order_by("ciudad"), #el query del modelo a mostrar como seleccionables (se imprime su def __str__(self) definido en models.py )
        empty_label=None, #esto es porque el forms.ModelChoiceField por defecto deja elegir vacío.
        widget=forms.Select(
            attrs={ "class": "form-select",
                    "placeholder":""}
        ),
        error_messages={
            "required": "Debe seleccionar una sucursal.",
        }
    )
    imagen = forms.ImageField(
        required=False,
        label="Imagen",
        widget=forms.FileInput(
            attrs={"class": "btn btn-outline-dark"}
        ),
    )
    aceptar_terminos = forms.BooleanField(
        required=True,
        label="Aceptar términos y condiciones *",
        widget=forms.CheckboxInput(
            attrs={"class": "form-check-input mb-3"}
        ),
        error_messages={
            "required": "Debe aceptar los términos y condiciones para continuar.",
        },
    )

    class Meta:
        model = Producto
        fields = ["nombre", "descripcion", "categoria", "sucursal", "imagen"]

    def __init__(self, *args, **kwargs):
        super(CreacionDeProducto,self).__init__(*args, **kwargs)              #Aca van las clases bootstrap a aplicar en todos los widgets de este form
        fields = self.fields.copy()     #Esto es para no afectar el dict que usa la pagina (sino se borra el ultimo item)
        fields.pop("aceptar_terminos")  #Aca sacamos el ultimo item(aceptar terminos) para no aplicarle los cambios
        for field in fields:
            self.fields[field].widget.attrs["class"] += " " + "w-100 mt-2 mb-3" #IMPORTANTE: += para que no sobreesrciba las clases individuales de cada uno, Y MUY IMPORTANTE el primer espacio en " " porque sino se aplica mal.(se concatena con la ultima letra de la ultima clase individualmente definida)

class FormularioDePregunta(forms.ModelForm):
    class Meta:
        model = Pregunta
        fields = ["texto"]
