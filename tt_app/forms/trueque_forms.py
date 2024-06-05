from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from ..models import Sucursal, Usuario, Producto, Pregunta, Respuesta
from django.core.exceptions import ValidationError
import datetime
from django.db import models

class AceptarSolicitud(forms.ModelForm):