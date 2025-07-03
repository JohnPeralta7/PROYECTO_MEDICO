from django import forms
from django.core.exceptions import ValidationError
from applications.core.models import Medicamento, TipoMedicamento, MarcaMedicamento
from applications.core.utils.medicamento import ViaAdministracion


class MedicamentoForm(forms.ModelForm):
    """
    Formulario para crear y editar medicamentos
    """
    
    class Meta:
        model = Medicamento
        fields = [
            'tipo', 'marca_medicamento', 'nombre', 'descripcion',
            'concentracion', 'via_administracion', 'cantidad',
            'precio', 'comercial', 'foto', 'activo'
        ]
        
        widgets = {
            'tipo': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'marca_medicamento': forms.Select(attrs={
                'class': 'form-select'
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Ibuprofeno',
                'required': True
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descripción del medicamento, indicaciones, precauciones...'
            }),
            'concentracion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 500mg, 1g, 5%'
            }),
            'via_administracion': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'cantidad': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'required': True
            }),
            'precio': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': 0,
                'required': True
            }),
            'comercial': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'foto': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
        
        labels = {
            'tipo': 'Tipo de Medicamento *',
            'marca_medicamento': 'Marca',
            'nombre': 'Nombre del Medicamento *',
            'descripcion': 'Descripción',
            'concentracion': 'Concentración',
            'via_administracion': 'Vía de Administración *',
            'cantidad': 'Stock Disponible *',
            'precio': 'Precio Unitario *',
            'comercial': 'Es Comercial',
            'foto': 'Foto del Medicamento',
            'activo': 'Activo'
        }
        
        help_texts = {
            'tipo': 'Seleccione el tipo de medicamento (Analgésico, Antibiótico, etc.)',
            'marca_medicamento': 'Marca comercial del medicamento (opcional)',
            'nombre': 'Nombre comercial o genérico del medicamento',
            'descripcion': 'Información sobre uso, indicaciones o precauciones',
            'concentracion': 'Ejemplo: 500mg, 1g, 5%',
            'via_administracion': 'Forma de administración del medicamento',
            'cantidad': 'Cantidad actual disponible en inventario',
            'precio': 'Precio unitario en dólares',
            'comercial': 'Marque si es un medicamento comercial (no genérico)',
            'foto': 'Imagen del medicamento (opcional)',
            'activo': 'Desmarque para inactivar el medicamento'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Filtrar solo tipos y marcas activas
        self.fields['tipo'].queryset = TipoMedicamento.objects.filter(activo=True)
        self.fields['marca_medicamento'].queryset = MarcaMedicamento.objects.filter(activo=True)
        
        # Hacer algunos campos opcionales en la interfaz
        self.fields['marca_medicamento'].required = False
        self.fields['descripcion'].required = False
        self.fields['concentracion'].required = False
        self.fields['foto'].required = False
        
        # Agregar opción vacía para marca
        self.fields['marca_medicamento'].empty_label = "Seleccione una marca (opcional)"

    def clean_nombre(self):
        """
        Validación personalizada para el nombre del medicamento
        """
        nombre = self.cleaned_data.get('nombre')
        if nombre:
            nombre = nombre.strip().title()
            
            # Verificar si ya existe otro medicamento con el mismo nombre (excluyendo el actual si estamos editando)
            medicamentos_existentes = Medicamento.objects.filter(nombre__iexact=nombre)
            if self.instance.pk:
                medicamentos_existentes = medicamentos_existentes.exclude(pk=self.instance.pk)
            
            if medicamentos_existentes.exists():
                raise ValidationError(f'Ya existe un medicamento con el nombre "{nombre}"')
                
        return nombre

    def clean_cantidad(self):
        """
        Validación para la cantidad/stock
        """
        cantidad = self.cleaned_data.get('cantidad')
        if cantidad is not None and cantidad < 0:
            raise ValidationError('La cantidad no puede ser negativa')
        return cantidad

    def clean_precio(self):
        """
        Validación para el precio
        """
        precio = self.cleaned_data.get('precio')
        if precio is not None and precio <= 0:
            raise ValidationError('El precio debe ser mayor a 0')
        return precio

    def clean_foto(self):
        """
        Validación para la foto del medicamento
        """
        foto = self.cleaned_data.get('foto')
        if foto:
            # Validar tamaño del archivo (máximo 5MB)
            if foto.size > 5 * 1024 * 1024:
                raise ValidationError('La imagen no puede ser mayor a 5MB')
            
            # Validar tipo de archivo
            allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif']
            if foto.content_type not in allowed_types:
                raise ValidationError('Solo se permiten archivos de imagen (JPEG, PNG, GIF)')
                
        return foto

    def save(self, commit=True):
        """
        Método personalizado para guardar el medicamento
        """
        medicamento = super().save(commit=False)
        
        # Capitalizar el nombre correctamente
        if medicamento.nombre:
            medicamento.nombre = medicamento.nombre.strip().title()
            
        if commit:
            medicamento.save()
            
        return medicamento


class MedicamentoBusquedaForm(forms.Form):
    """
    Formulario para búsqueda y filtrado de medicamentos
    """
    
    q = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por nombre o marca...',
            'id': 'search-input'
        }),
        label='Buscar'
    )
    
    tipo = forms.ModelChoiceField(
        queryset=TipoMedicamento.objects.filter(activo=True),
        required=False,
        empty_label="Todos los tipos",
        widget=forms.Select(attrs={
            'class': 'form-select'
        }),
        label='Tipo'
    )
    
    marca = forms.ModelChoiceField(
        queryset=MarcaMedicamento.objects.filter(activo=True),
        required=False,
        empty_label="Todas las marcas",
        widget=forms.Select(attrs={
            'class': 'form-select'
        }),
        label='Marca'
    )
    
    status = forms.ChoiceField(
        choices=[
            ('', 'Todos'),
            ('active', 'Activos'),
            ('inactive', 'Inactivos'),
        ],
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select'
        }),
        label='Estado'
    )
    
    stock_minimo = forms.IntegerField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Stock mínimo'
        }),
        label='Stock mínimo'
    )
