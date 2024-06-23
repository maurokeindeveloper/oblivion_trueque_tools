from datetime import datetime, date
from django import forms
from ..models import Sucursal, Producto, Pregunta, Respuesta
from django.core.validators import RegexValidator


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
    texto = forms.CharField(
        required=True,
        max_length=1000,
        widget=forms.Textarea(
            attrs={"class": "form-control", "placeholder": "Escribí tu pregunta sobre este producto"}
        ),
        error_messages={
            "required": "Debe ingresar un texto para registrar la pregunta",
        },
    )
    class Meta:
        model = Pregunta
        fields = ["texto"]


class FormularioDeRespuesta(forms.ModelForm):
    texto = forms.CharField(
        required=True,
        max_length=1000,
        widget=forms.Textarea(
            attrs={"class": "form-control", "placeholder": "Respondé la consulta que hicieron sobre tu producto"}
        ),
        error_messages={
            "required": "Debe ingresar un texto para registrar la respuesta",
        },
    )
    class Meta:
        model = Respuesta
        fields = ["texto"]

class FormularioPagarPromocion(forms.ModelForm):
    numero_tarjeta = forms.CharField(
        label='Número de Tarjeta de Crédito',
        max_length=16,
        min_length=16,
        validators=[RegexValidator(r'^\d+$', message='Ingresar solo dígitos numéricos.')],
        widget=forms.TextInput(attrs={
            "class": "form-control", 
            'placeholder': '1234 5678 9012 3456',
            'id': 'id_numero_tarjeta'
            }),
        error_messages={
            "required": "Debe ingresar su número de tarjeta",
            "min_length": "La descripción debe tener 16 caracteres.",
            "max_length": "La descripción debe tener 16 caracteres.",
        },
    )
    codigo_seguridad = forms.CharField(
        label='Código de Seguridad (CVV)',
        max_length=3,
        min_length=3,
        validators=[RegexValidator(r'^\d+$', message='Ingresar solo dígitos numéricos.')],
        widget=forms.TextInput(attrs={
            "class": "form-control", 
            'placeholder': '123',
            "min_length": "La descripción debe tener 3 caracteres.",
            "max_length": "La descripción debe tener 3 caracteres.",
            'id': 'id_codigo_seguridad'})
    )
    fecha_vencimiento = forms.CharField(
        label='Fecha de Vencimiento (MM/AA)',
        #input_formats=['%m/%y', '%m/%Y'],
        max_length=5,
        min_length=5,
        validators=[RegexValidator(r'^(0[1-9]|1[0-2])\/\d{2}$', message='La fecha de vencimiento debe estar en formato MM/AA.')],
        widget=forms.TextInput(attrs={
            "class": "form-control", 
            'placeholder': 'MM/AA',
            'id': 'id_fecha_vencimiento'
        })
    )
    def clean_fecha_vencimiento(self):
        datos = self.cleaned_data['fecha_vencimiento']
        month, year = datos.split('/')
        month = int(month)
        year = int(year) + 2000  # Asumiendo que el año está en formato de dos dígitos

        expiration_date = date(year, month, 1)
        print(expiration_date)

        if expiration_date < date.today().replace(day=1):
            raise forms.ValidationError("La tarjeta ha expirado.")        
        return datos    
    class Meta:
        model = Producto
        fields = ["numero_tarjeta", "codigo_seguridad", "fecha_vencimiento"]