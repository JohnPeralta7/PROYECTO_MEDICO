from django import forms
from django.core.exceptions import ValidationError
from applications.core.models import GastoMensual, TipoGasto


class GastoMensualForm(forms.ModelForm):
    """
    Formulario para crear y editar gastos mensuales
    """
    
    class Meta:
        model = GastoMensual
        fields = [
            'tipo_gasto', 'fecha', 'valor', 'observacion'
        ]
        
        widgets = {
            'tipo_gasto': forms.Select(attrs={
                'class': 'pl-10 block w-full py-3 px-4 border border-gray-200 rounded-lg bg-white focus:ring-2 focus:ring-red-500 focus:border-red-500 text-sm shadow-sm',
                'required': True
            }),
            'fecha': forms.DateInput(attrs={
                'class': 'pl-10 block w-full py-3 px-4 border border-gray-200 rounded-lg bg-white focus:ring-2 focus:ring-red-500 focus:border-red-500 text-sm shadow-sm',
                'type': 'date',
                'required': True
            }),
            'valor': forms.NumberInput(attrs={
                'class': 'pl-10 block w-full py-3 px-4 border border-gray-200 rounded-lg bg-white focus:ring-2 focus:ring-red-500 focus:border-red-500 text-sm shadow-sm',
                'step': '0.01',
                'min': '0',
                'placeholder': '0.00',
                'required': True
            }),
            'observacion': forms.Textarea(attrs={
                'class': 'block w-full py-3 px-4 border border-gray-200 rounded-lg bg-white focus:ring-2 focus:ring-red-500 focus:border-red-500 text-sm shadow-sm resize-none',
                'rows': 3,
                'placeholder': 'Comentario adicional sobre este gasto (opcional)'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar solo tipos de gasto activos
        self.fields['tipo_gasto'].queryset = TipoGasto.objects.filter(activo=True).order_by('nombre')
        
        # Añadir labels personalizados
        self.fields['tipo_gasto'].label = 'Tipo de Gasto'
        self.fields['fecha'].label = 'Fecha del Gasto'
        self.fields['valor'].label = 'Valor (USD)'
        self.fields['observacion'].label = 'Observación'
        
        # Help text
        self.fields['valor'].help_text = 'Ingrese el monto en dólares'
        self.fields['observacion'].help_text = 'Información adicional sobre este gasto'
    
    def clean_valor(self):
        valor = self.cleaned_data.get('valor')
        if valor is not None and valor <= 0:
            raise ValidationError('El valor debe ser mayor a 0')
        return valor


class GastoMensualBusquedaForm(forms.Form):
    """
    Formulario para búsqueda y filtrado de gastos mensuales
    """
    
    q = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por tipo de gasto...'
        })
    )
    
    tipo_gasto = forms.ModelChoiceField(
        queryset=TipoGasto.objects.filter(activo=True).order_by('nombre'),
        required=False,
        empty_label='Todos los tipos',
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    
    fecha_desde = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    fecha_hasta = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
