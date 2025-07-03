from django import forms
from django.forms import ModelForm
from applications.doctor.models import HorarioAtencion
from applications.doctor.utils.doctor import DiaSemanaChoices

class HorarioAtencionForm(ModelForm):
    # Campo personalizado para seleccionar múltiples días
    dias_semana = forms.MultipleChoiceField(
        choices=DiaSemanaChoices.choices,
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'h-4 w-4 text-cyan-600 focus:ring-cyan-500 border-gray-300 rounded'
        }),
        label="Días de la Semana",
        help_text="Seleccione uno o más días para asignar el mismo horario",
        required=True
    )

    class Meta:
        model = HorarioAtencion
        fields = ['hora_inicio', 'hora_fin', 'intervalo_desde', 'intervalo_hasta', 'activo']
        widgets = {
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si estamos editando, cargar el día actual
        if self.instance and self.instance.pk:
            self.fields['dias_semana'].initial = [self.instance.dia_semana]

    def clean_dias_semana(self):
        """Validar que se haya seleccionado al menos un día"""
        dias = self.cleaned_data.get('dias_semana')
        if not dias:
            raise forms.ValidationError("Debe seleccionar al menos un día de la semana.")
        return dias

    def clean(self):
        """Validaciones generales del formulario"""
        cleaned_data = super().clean()
        hora_inicio = cleaned_data.get('hora_inicio')
        hora_fin = cleaned_data.get('hora_fin')
        intervalo_desde = cleaned_data.get('intervalo_desde')
        intervalo_hasta = cleaned_data.get('intervalo_hasta')

        # Validar que hora_fin sea mayor que hora_inicio
        if hora_inicio and hora_fin:
            if hora_fin <= hora_inicio:
                raise forms.ValidationError("La hora de fin debe ser posterior a la hora de inicio.")

        # Validar intervalo si se proporciona
        if intervalo_desde and intervalo_hasta:
            if intervalo_hasta <= intervalo_desde:
                raise forms.ValidationError("La hora de fin del intervalo debe ser posterior a la hora de inicio del intervalo.")
            
            # El intervalo debe estar dentro del horario de atención
            if hora_inicio and hora_fin:
                if intervalo_desde <= hora_inicio or intervalo_hasta >= hora_fin:
                    raise forms.ValidationError("El intervalo debe estar dentro del horario de atención.")

        return cleaned_data

class HorarioAtencionEditForm(ModelForm):
    """Formulario para editar horarios individuales (un día específico)"""
    
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

    def clean(self):
        """Validaciones generales del formulario"""
        cleaned_data = super().clean()
        hora_inicio = cleaned_data.get('hora_inicio')
        hora_fin = cleaned_data.get('hora_fin')
        intervalo_desde = cleaned_data.get('intervalo_desde')
        intervalo_hasta = cleaned_data.get('intervalo_hasta')

        # Validar que hora_fin sea mayor que hora_inicio
        if hora_inicio and hora_fin:
            if hora_fin <= hora_inicio:
                raise forms.ValidationError("La hora de fin debe ser posterior a la hora de inicio.")

        # Validar intervalo si se proporciona
        if intervalo_desde and intervalo_hasta:
            if intervalo_hasta <= intervalo_desde:
                raise forms.ValidationError("La hora de fin del intervalo debe ser posterior a la hora de inicio del intervalo.")
            
            # El intervalo debe estar dentro del horario de atención
            if hora_inicio and hora_fin:
                if intervalo_desde <= hora_inicio or intervalo_hasta >= hora_fin:
                    raise forms.ValidationError("El intervalo debe estar dentro del horario de atención.")

        return cleaned_data