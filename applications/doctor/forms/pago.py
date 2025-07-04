from django import forms
from applications.doctor.models import Pago, DetallePago, ServiciosAdicionales
from applications.core.models import Paciente

class PagoForm(forms.ModelForm):
    # Campo para seleccionar paciente
    paciente = forms.ModelChoiceField(
        queryset=Paciente.objects.filter(activo=True),
        widget=forms.Select(attrs={
            'class': 'w-full border rounded px-4 py-2',
            'placeholder': 'Seleccione un paciente'
        }),
        empty_label="Seleccione un paciente...",
        required=False
    )
    
    # Campo para monto de consulta
    monto_consulta = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'w-full border rounded px-4 py-2',
            'placeholder': '0.00',
            'step': '0.01'
        })
    )
    
    class Meta:
        model = Pago
        fields = ['nombre_pagador', 'observaciones']
        widgets = {
            'nombre_pagador': forms.TextInput(attrs={
                'class': 'w-full border rounded px-4 py-2',
                'placeholder': 'Nombre completo del pagador'
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'w-full border rounded px-4 py-2',
                'rows': 3,
                'placeholder': 'Observaciones adicionales (opcional)'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Agregar campos dinámicamente solo si existen en el modelo
        try:
            from applications.core.models import Paciente
            if hasattr(Pago, 'paciente'):
                self.fields['paciente'] = forms.ModelChoiceField(
                    queryset=Paciente.objects.filter(activo=True),
                    widget=forms.Select(attrs={
                        'class': 'w-full border rounded px-4 py-2',
                    }),
                    empty_label="Seleccione un paciente...",
                    required=False
                )
        except:
            pass
        
        try:
            if hasattr(Pago, 'monto_consulta'):
                self.fields['monto_consulta'] = forms.DecimalField(
                    max_digits=10,
                    decimal_places=2,
                    required=False,
                    widget=forms.NumberInput(attrs={
                        'class': 'w-full border rounded px-4 py-2',
                        'placeholder': '0.00',
                        'step': '0.01'
                    })
                )
        except:
            pass