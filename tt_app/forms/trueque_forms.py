from django import forms
from django.shortcuts import get_object_or_404
from ..models import Sucursal, Trueque, Producto

class SolicitarForm(forms.ModelForm):
    producto_solicitante = forms.ModelChoiceField(
        required=True,
        label="Qué producto quieres ofrecer?",
        queryset=Producto.objects.none(),  # el query del modelo a mostrar como seleccionables (se imprime su def __str__(self) definido en models.py )
        empty_label=None,  # esto es porque el forms.ModelChoiceField por defecto deja elegir vacío.
        widget=forms.Select(
            attrs={ "class": "form-select",
                    "placeholder": "Que producto quieres ofrecer?"}
        ),
        error_messages={
            "required": "Debe seleccionar un producto.",
        },
    )
    producto_solicitado = forms.ModelChoiceField(
        required=True,
        label="Qué producto quieres obtener a cambio?",
        queryset=Producto.objects.none(),  # el query del modelo a mostrar como seleccionables (se imprime su def __str__(self) definido en models.py )
        empty_label=None,  # esto es porque el forms.ModelChoiceField por defecto deja elegir vacío.
        widget=forms.Select(
            attrs={ "class": "form-select",
                    "placeholder": "Que producto quieres ofrecer?"}
        ),
        error_messages={
            "required": "Debe seleccionar un producto.",
        },
    )
    fecha_programada = forms.DateField(
        required=True,
        label="Fecha de intercambio",
        widget=forms.DateInput(
            attrs={ "class": "form-control",
                    "placeholder": "Ingresá una fecha de intercambio",
                    "type":"date"}
        ),
        error_messages={
            "required": "Debe ingresar una fecha de intercambio.",
        },
    )
    horario = forms.ChoiceField(
        required=True,
        label="Horario",
        choices=Trueque.Rango_Horario.choices,
        widget=forms.Select(
            attrs={ "class": "form-select",
                    "placeholder": "Seleccioná un horario"}
        ),
        error_messages={
            "required": "Debe seleccionar un horario.",
        },
    )
    sucursal = forms.ModelChoiceField(
        required=True,
        label="Sucursal asignada",
        queryset=Sucursal.objects.none(),  # el query del modelo a mostrar como seleccionables (se imprime su def __str__(self) definido en models.py )
        empty_label=None,  # esto es porque el forms.ModelChoiceField por defecto deja elegir vacío.
        widget=forms.Select(attrs={"class": "form-select", "placeholder": ""}),
        error_messages={
            "required": "Debe seleccionar una sucursal.",
        },
    )
    class Meta:
        model = Trueque
        fields = ["producto_solicitante", "producto_solicitado", "fecha_programada", "horario", "sucursal"]
    
    def __init__ (self,*args, **kwargs):
        usuario = kwargs.pop('user')
        id_p = kwargs.pop('id')
        p = get_object_or_404(Producto,id=id_p)
        super().__init__(*args, **kwargs) 
        self.fields['producto_solicitante'].queryset = Producto.objects.exclude(activo=False).filter(usuario=usuario,categoria=p.categoria)
        self.fields['producto_solicitado'].queryset = Producto.objects.exclude(activo=False).filter(id=id_p).all()
        self.fields['sucursal'].queryset = Sucursal.objects.exclude(activo=False).filter(id=p.sucursal.id).all()
        for field in self.fields:                       #Aca van las clases bootstrap a aplicar en todos los widgets de este form
            self.fields[field].widget.attrs["class"] += " " + "w-100 mt-2 mb-3" #IMPORTANTE: += para que no sobreesrciba las clases individuales de cada uno, Y MUY IMPORTANTE el primer espacio en " " porque sino se aplica mal.(se concatena con la ultima letra de la ultima clase individualmente definida)