from django import forms
from django.forms import ModelForm
from applications.core.models import Doctor, Especialidad


class DoctorForm(ModelForm):
    """Formulario para crear y editar doctores"""
    
    # Campo adicional para especialidades como texto
    especialidad_texto = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: Medicina General, Pediatría, Cardiología...'
        }),
        help_text='Separa múltiples especialidades con comas'
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Si estamos editando, cargar especialidades existentes como texto
        if self.instance and self.instance.pk:
            especialidades_existentes = list(self.instance.especialidad.values_list('nombre', flat=True))
            self.fields['especialidad_texto'].initial = ', '.join(especialidades_existentes)
        
        # Aplicar clases CSS con widget_tweaks
        self.fields['nombres'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Nombres del doctor'
        })
        self.fields['apellidos'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Apellidos del doctor'
        })
        self.fields['ruc'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'RUC del doctor'
        })
        self.fields['fecha_nacimiento'].widget.attrs.update({
            'class': 'form-control',
            'type': 'date'
        })
        self.fields['direccion'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Dirección de trabajo'
        })
        self.fields['latitud'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Latitud (opcional)'
        })
        self.fields['longitud'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Longitud (opcional)'
        })
        self.fields['codigo_unico_doctor'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Código único del doctor'
        })
        # Ocultar el campo original de especialidad
        self.fields['especialidad'].widget = forms.HiddenInput()
        
        self.fields['telefonos'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Teléfonos de contacto'
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'correo@ejemplo.com'
        })
        self.fields['horario_atencion'].widget.attrs.update({
            'class': 'form-control',
            'rows': '3',
            'placeholder': 'Ej: Lunes a Viernes, 08h00 - 13h00'
        })
        self.fields['duracion_atencion'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Minutos por cita'
        })
        self.fields['curriculum'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['firma_digital'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['foto'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['imagen_receta'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['activo'].widget.attrs.update({
            'class': 'form-check-input'
        })

    class Meta:
        model = Doctor
        fields = [
            'nombres', 'apellidos', 'ruc', 'fecha_nacimiento', 'direccion',
            'latitud', 'longitud', 'codigo_unico_doctor', 'especialidad',
            'telefonos', 'email', 'horario_atencion', 'duracion_atencion',
            'curriculum', 'firma_digital', 'foto', 'imagen_receta', 'activo',
            'especialidad_texto'  # Añadir el campo de texto
        ]
        widgets = {
            'horario_atencion': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_especialidad_texto(self):
        """Validar y procesar especialidades desde texto"""
        especialidad_texto = self.cleaned_data.get('especialidad_texto', '')
        
        if especialidad_texto:
            # Limpiar y dividir especialidades
            especialidades_nombres = [
                nombre.strip().title() 
                for nombre in especialidad_texto.split(',') 
                if nombre.strip()
            ]
            
            # Validar que no estén vacías
            if not especialidades_nombres:
                raise forms.ValidationError("Debe ingresar al menos una especialidad válida.")
            
            # Validar longitud de nombres
            for nombre in especialidades_nombres:
                if len(nombre) > 100:
                    raise forms.ValidationError(f"El nombre '{nombre}' es demasiado largo (máximo 100 caracteres).")
            
            return especialidades_nombres
        
        return []

    def save(self, commit=True):
        """Guardar doctor y manejar especialidades desde texto"""
        # Remover especialidad_texto de cleaned_data para que no cause error
        if 'especialidad_texto' in self.cleaned_data:
            especialidad_texto_value = self.cleaned_data.pop('especialidad_texto')
        else:
            especialidad_texto_value = ''
        
        doctor = super().save(commit=False)
        
        if commit:
            doctor.save()
            
            # Procesar especialidades desde el campo de texto
            if especialidad_texto_value:
                # Si viene como string, procesarlo
                if isinstance(especialidad_texto_value, str):
                    especialidades_nombres = [
                        nombre.strip().title() 
                        for nombre in especialidad_texto_value.split(',') 
                        if nombre.strip()
                    ]
                else:
                    especialidades_nombres = especialidad_texto_value
                
                # Limpiar especialidades existentes
                doctor.especialidad.clear()
                
                # Crear/obtener especialidades y asignarlas
                for nombre_especialidad in especialidades_nombres:
                    if nombre_especialidad:  # Verificar que no esté vacío
                        especialidad, created = Especialidad.objects.get_or_create(
                            nombre=nombre_especialidad,
                            defaults={'descripcion': f'Especialidad en {nombre_especialidad}'}
                        )
                        doctor.especialidad.add(especialidad)
                        if created:
                            print(f"✅ Especialidad '{nombre_especialidad}' creada exitosamente")
        
        return doctor

    def clean_ruc(self):
        """Validación personalizada para el RUC"""
        ruc = self.cleaned_data.get('ruc')
        if ruc:
            # Limpiar el RUC de espacios y caracteres especiales
            ruc = ruc.strip().replace('-', '').replace(' ', '')
            
            # Validar longitud básica
            if len(ruc) < 10 or len(ruc) > 13:
                raise forms.ValidationError("El RUC debe tener entre 10 y 13 dígitos.")
            
            # Validar que solo contenga números
            if not ruc.isdigit():
                raise forms.ValidationError("El RUC debe contener solo números.")
            
            # Verificar si el RUC ya existe (excepto para el mismo doctor en edición)
            existing = Doctor.objects.filter(ruc=ruc)
            if self.instance and self.instance.pk:
                existing = existing.exclude(pk=self.instance.pk)
            
            if existing.exists():
                raise forms.ValidationError("Ya existe un doctor con este RUC.")
        
        return ruc

    def clean_codigo_unico_doctor(self):
        """Validación personalizada para el código único"""
        codigo = self.cleaned_data.get('codigo_unico_doctor')
        if codigo:
            # Verificar si el código ya existe (excepto para el mismo doctor en edición)
            existing = Doctor.objects.filter(codigo_unico_doctor=codigo)
            if self.instance and self.instance.pk:
                existing = existing.exclude(pk=self.instance.pk)
            
            if existing.exists():
                raise forms.ValidationError("Ya existe un doctor con este código único.")
        return codigo

    def clean_email(self):
        """Validación personalizada para el email"""
        email = self.cleaned_data.get('email')
        if email:
            # Verificar si el email ya existe (excepto para el mismo doctor en edición)
            existing = Doctor.objects.filter(email=email)
            if self.instance and self.instance.pk:
                existing = existing.exclude(pk=self.instance.pk)
            
            if existing.exists():
                raise forms.ValidationError("Ya existe un doctor con este email.")
        return email
