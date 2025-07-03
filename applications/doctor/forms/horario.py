from django import forms
from django.forms import ModelForm
from applications.doctor.models import HorarioAtencion

class HorarioAtencionForm(ModelForm):
    class Meta:
        model = HorarioAtencion
        fields = '__all__'
        widgets = {
            'dia_semana': forms.Select(attrs={
                'class': 'form-select w-full rounded-lg border-cyan-300 focus:ring focus:ring-cyan-200'
            }),
            'hora_inicio': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-input w-full rounded-lg border-cyan-300 focus:ring focus:ring-cyan-200'
            }),
            'hora_fin': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-input w-full rounded-lg border-cyan-300 focus:ring focus:ring-cyan-200'
            }),
            'intervalo_desde': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-input w-full rounded-lg border-cyan-300 focus:ring focus:ring-cyan-100'
            }),
            'intervalo_hasta': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-input w-full rounded-lg border-cyan-300 focus:ring focus:ring-cyan-100'
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-checkbox h-5 w-5 text-cyan-600'
            }),
        }