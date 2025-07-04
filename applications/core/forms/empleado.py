from django import forms
from django.forms import ModelForm
from applications.core.models import Empleado

class EmpleadoForm(ModelForm):
    class Meta:
        model = Empleado
        fields = [
            "nombres",
            "apellidos",
            "cedula_ecuatoriana",
            "dni",
            "fecha_nacimiento",
            "cargo",
            "sueldo",
            "fecha_ingreso",
            "direccion",
            "latitud",
            "longitud",
            "foto",
            "activo",
        ]
        widgets = {
            "nombres": forms.TextInput(attrs={"placeholder": "Ingrese nombres", "class": "form-control"}),
            "apellidos": forms.TextInput(attrs={"placeholder": "Ingrese apellidos", "class": "form-control"}),
            "cedula_ecuatoriana": forms.TextInput(attrs={"placeholder": "Ingrese cédula ecuatoriana", "class": "form-control"}),
            "dni": forms.TextInput(attrs={"placeholder": "Ingrese DNI", "class": "form-control"}),
            "fecha_nacimiento": forms.DateInput(format='%Y-%m-%d', attrs={"type": "date", "class": "form-control"}),
            "cargo": forms.Select(attrs={"class": "form-control"}),
            "sueldo": forms.NumberInput(attrs={"placeholder": "Ingrese sueldo", "class": "form-control"}),
            "fecha_ingreso": forms.DateInput(format='%Y-%m-%d', attrs={"type": "date", "class": "form-control"}),
            "direccion": forms.TextInput(attrs={"placeholder": "Ingrese dirección", "class": "form-control"}),
            "latitud": forms.NumberInput(attrs={"placeholder": "Latitud", "class": "form-control"}),
            "longitud": forms.NumberInput(attrs={"placeholder": "Longitud", "class": "form-control"}),
            "foto": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "activo": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
        labels = {
            "nombres": "Nombres",
            "apellidos": "Apellidos",
            "cedula_ecuatoriana": "Cédula Ecuatoriana",
            "dni": "DNI",
            "fecha_nacimiento": "Fecha de Nacimiento",
            "cargo": "Cargo",
            "sueldo": "Sueldo",
            "fecha_ingreso": "Fecha de Ingreso",
            "direccion": "Dirección",
            "latitud": "Latitud",
            "longitud": "Longitud",
            "foto": "Foto",
            "activo": "Activo",
        }