from django import forms
from django.forms import ModelForm
from applications.core.models import Diagnostico

class DiagnosticoForm(ModelForm):
    class Meta:
        model = Diagnostico
        fields = [
            "codigo",
            "descripcion",
            "datos_adicionales",
            "activo",
        ]
        error_messages = {
            "codigo": {
                "unique": "Ya existe un diagnóstico con este código.",
            },
        }
        widgets = {
            "codigo": forms.TextInput(attrs={
                "placeholder": "Ingrese el código del diagnóstico (Ej: A09, J00, K35.2)",
                "class": "form-control",
            }),
            "descripcion": forms.TextInput(attrs={
                "placeholder": "Ingrese la descripción del diagnóstico",
                "class": "form-control",
            }),
            "datos_adicionales": forms.Textarea(attrs={
                "placeholder": "Observaciones clínicas u otra información útil.",
                "class": "form-control",
                "rows": 3,
            }),
            "activo": forms.CheckboxInput(attrs={
                "class": "form-check-input",
            }),
        }
        labels = {
            "codigo": "Código del Diagnóstico",
            "descripcion": "Descripción",
            "datos_adicionales": "Datos Adicionales",
            "activo": "Activo",
        }