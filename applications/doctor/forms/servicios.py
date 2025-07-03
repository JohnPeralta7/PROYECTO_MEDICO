from django import forms
from django.forms import ModelForm
from applications.doctor.models import ServiciosAdicionales

class ServiciosAdicionalesForm(ModelForm):
    class Meta:
        model = ServiciosAdicionales
        fields = '__all__'
        widgets = {
            'nombre_servicio': forms.TextInput(attrs={
                'class': 'form-input w-full rounded-lg border-cyan-300 focus:ring focus:ring-cyan-200'
            }),
            'costo_servicio': forms.NumberInput(attrs={
                'class': 'form-input w-full rounded-lg border-cyan-300 focus:ring focus:ring-cyan-200',
                'step': '0.01',
                'min': '0'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-textarea w-full rounded-lg border-cyan-300 focus:ring focus:ring-cyan-200',
                'rows': 3
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-checkbox h-5 w-5 text-cyan-600'
            }),
        }