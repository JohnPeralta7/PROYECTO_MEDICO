import re
from django import forms
from django.forms import ModelForm

from applications.core.models import Paciente

class PacienteForm(ModelForm):
    class Meta:
        model = Paciente
        fields = [
            "nombres",
            "apellidos",
            "cedula_ecuatoriana",
            "dni",
            "fecha_nacimiento",
            "telefono",
            "email",
            "sexo",
            "direccion",
            "estado_civil",
            "latitud",
            "longitud",
            "tipo_sangre",
            "foto",
            "antecedentes_personales",
            "antecedentes_familiares",
            "antecedentes_quirurgicos",
            "alergias",
            "medicamentos_actuales",
            "habitos_toxicos",
            "vacunas",
            "antecedentes_gineco_obstetricos",
            "activo",
        ]
        error_messages = {
            "cedula_ecuatoriana": {
                "unique": "Ya existe un paciente con esta cédula.",
            },
            "dni": {
                "unique": "Ya existe un paciente con este DNI.",
            },
            "email": {
                "unique": "Ya existe un paciente con este email.",
            },
        }
        widgets = {
            "nombres": forms.TextInput(attrs={
                "placeholder": "Ingrese nombres",
                "class": "form-control",
            }),
            "apellidos": forms.TextInput(attrs={
                "placeholder": "Ingrese apellidos",
                "class": "form-control",
            }),
            "cedula_ecuatoriana": forms.TextInput(attrs={
                "placeholder": "Ingrese cédula ecuatoriana",
                "class": "form-control",
            }),
            "dni": forms.TextInput(attrs={
                "placeholder": "Ingrese DNI",
                "class": "form-control",
            }),
            "fecha_nacimiento": forms.DateInput(
    format='%Y-%m-%d',
    attrs={"type": "date", "class": "form-control"}
),
            "telefono": forms.TextInput(attrs={
                "placeholder": "Ingrese teléfono",
                "class": "form-control",
            }),
            "email": forms.EmailInput(attrs={
                "placeholder": "Ingrese email",
                "class": "form-control",
            }),
            "sexo": forms.Select(attrs={
                "class": "form-control",
            }),
            "direccion": forms.TextInput(attrs={
                "placeholder": "Ingrese dirección",
                "class": "form-control",
            }),
            "estado_civil": forms.Select(attrs={
                "class": "form-control",
            }),
            "latitud": forms.TextInput(attrs={
                "placeholder": "Latitud",
                "class": "form-control",
            }),
            "longitud": forms.TextInput(attrs={
                "placeholder": "Longitud",
                "class": "form-control",
            }),
            "tipo_sangre": forms.Select(attrs={
                "class": "form-control",
            }),
            "foto": forms.ClearableFileInput(attrs={
                "class": "form-control",
            }),
            "antecedentes_personales": forms.Textarea(attrs={
                "placeholder": "Antecedentes personales",
                "class": "form-control",
                "rows": 2,
            }),
            "antecedentes_familiares": forms.Textarea(attrs={
                "placeholder": "Antecedentes familiares",
                "class": "form-control",
                "rows": 2,
            }),
            "antecedentes_quirurgicos": forms.Textarea(attrs={
                "placeholder": "Antecedentes quirúrgicos",
                "class": "form-control",
                "rows": 2,
            }),
            "alergias": forms.Textarea(attrs={
                "placeholder": "Alergias",
                "class": "form-control",
                "rows": 2,
            }),
            "medicamentos_actuales": forms.Textarea(attrs={
                "placeholder": "Medicamentos actuales",
                "class": "form-control",
                "rows": 2,
            }),
            "habitos_toxicos": forms.Textarea(attrs={
                "placeholder": "Hábitos tóxicos",
                "class": "form-control",
                "rows": 2,
            }),
            "vacunas": forms.Textarea(attrs={
                "placeholder": "Vacunas",
                "class": "form-control",
                "rows": 2,
            }),
            "antecedentes_gineco_obstetricos": forms.Textarea(attrs={
                "placeholder": "Antecedentes gineco-obstétricos",
                "class": "form-control",
                "rows": 2,
            }),
            "activo": forms.CheckboxInput(attrs={
                "class": "form-check-input",
            }),
        }
        labels = {
            "nombres": "Nombres",
            "apellidos": "Apellidos",
            "cedula_ecuatoriana": "Cédula Ecuatoriana",
            "dni": "DNI",
            "fecha_nacimiento": "Fecha de Nacimiento",
            "telefono": "Teléfono",
            "email": "Email",
            "sexo": "Sexo",
            "direccion": "Dirección",
            "estado_civil": "Estado Civil",
            "latitud": "Latitud",
            "longitud": "Longitud",
            "tipo_sangre": "Tipo de Sangre",
            "foto": "Foto",
            "antecedentes_personales": "Antecedentes Personales",
            "antecedentes_familiares": "Antecedentes Familiares",
            "antecedentes_quirurgicos": "Antecedentes Quirúrgicos",
            "alergias": "Alergias",
            "medicamentos_actuales": "Medicamentos Actuales",
            "habitos_toxicos": "Hábitos Tóxicos",
            "vacunas": "Vacunas",
            "antecedentes_gineco_obstetricos": "Antecedentes Gineco-Obstétricos",
            "activo": "Activo",
        }

    def clean_nombres(self):
        nombres = self.cleaned_data.get("nombres")
        return nombres.upper() if nombres else nombres

    def clean_apellidos(self):
        apellidos = self.cleaned_data.get("apellidos")
        return apellidos.upper() if apellidos else apellidos
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk and self.instance.fecha_nacimiento:
            self.initial['fecha_nacimiento'] = self.instance.fecha_nacimiento.strftime('%Y-%m-%d')