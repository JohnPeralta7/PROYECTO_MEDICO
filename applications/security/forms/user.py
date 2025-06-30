from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from applications.security.models import User
from django.contrib.auth.models import Group, Permission

class UserForm(forms.ModelForm):
    """
    Formulario para la creación y edición de usuarios
    """
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(
            attrs={
                'class': 'block w-full pl-10 pr-4 py-3 border border-gray-200 rounded-lg bg-white focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm shadow-sm',
                'placeholder': 'Ingrese la contraseña'
            }
        ),
        required=False
    )
    
    password_confirmation = forms.CharField(
        label='Confirmar contraseña',
        widget=forms.PasswordInput(
            attrs={
                'class': 'block w-full pl-10 pr-4 py-3 border border-gray-200 rounded-lg bg-white focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm shadow-sm',
                'placeholder': 'Confirme la contraseña'
            }
        ),
        required=False
    )
    
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        widget=forms.SelectMultiple(
            attrs={
                'class': 'block w-full py-3 px-4 border border-gray-200 rounded-lg bg-white focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm shadow-sm',
                'size': '5'
            }
        ),
        required=False,
        label="Grupos"
    )
    
    class Meta:
        model = User
        fields = [
            'username', 
            'email', 
            'first_name', 
            'last_name', 
            'dni', 
            'image',
            'direction',
            'phone',
            'is_active',
            'is_staff',
            'is_superuser',
            'groups',
            'user_permissions'
        ]
        widgets = {
            'username': forms.TextInput(
                attrs={
                    'class': 'block w-full pl-10 pr-4 py-3 border border-gray-200 rounded-lg bg-white focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm shadow-sm',
                    'placeholder': 'Nombre de usuario'
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'class': 'block w-full pl-10 pr-4 py-3 border border-gray-200 rounded-lg bg-white focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm shadow-sm',
                    'placeholder': 'correo@ejemplo.com'
                }
            ),
            'first_name': forms.TextInput(
                attrs={
                    'class': 'block w-full pl-10 pr-4 py-3 border border-gray-200 rounded-lg bg-white focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm shadow-sm',
                    'placeholder': 'Nombre'
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'class': 'block w-full pl-10 pr-4 py-3 border border-gray-200 rounded-lg bg-white focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm shadow-sm',
                    'placeholder': 'Apellido'
                }
            ),
            'dni': forms.TextInput(
                attrs={
                    'class': 'block w-full pl-10 pr-4 py-3 border border-gray-200 rounded-lg bg-white focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm shadow-sm',
                    'placeholder': 'DNI/Cédula'
                }
            ),
            'direction': forms.TextInput(
                attrs={
                    'class': 'block w-full pl-10 pr-4 py-3 border border-gray-200 rounded-lg bg-white focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm shadow-sm',
                    'placeholder': 'Dirección'
                }
            ),
            'phone': forms.TextInput(
                attrs={
                    'class': 'block w-full pl-10 pr-4 py-3 border border-gray-200 rounded-lg bg-white focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm shadow-sm',
                    'placeholder': 'Teléfono'
                }
            ),
            'image': forms.FileInput(
                attrs={
                    'class': 'block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100',
                }
            ),
            'is_active': forms.CheckboxInput(
                attrs={
                    'class': 'w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 focus:ring-2',
                }
            ),
            'is_staff': forms.CheckboxInput(
                attrs={
                    'class': 'w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 focus:ring-2',
                }
            ),
            'is_superuser': forms.CheckboxInput(
                attrs={
                    'class': 'w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 focus:ring-2',
                }
            ),
        }
    
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        # Agregar filtros para permisos
        self.fields['user_permissions'].queryset = Permission.objects.filter(
            content_type__model__in=['user', 'group', 'menu', 'module', 'groupmodulepermission']
        ).order_by('content_type__model', 'name')
        
        # Si estamos editando un usuario existente
        if self.instance.pk:
            self.fields['password'].required = False
            self.fields['password_confirmation'].required = False
            self.initial['groups'] = self.instance.groups.all()
            self.initial['user_permissions'] = self.instance.user_permissions.all()
        else:
            self.fields['password'].required = True
            self.fields['password_confirmation'].required = True

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirmation = cleaned_data.get('password_confirmation')

        if self.instance.pk:  # Si es una actualización
            if password:
                if password != password_confirmation:
                    raise forms.ValidationError('Las contraseñas no coinciden')
        else:  # Si es una creación
            if not password:
                self.add_error('password', 'Debe ingresar una contraseña')
            elif not password_confirmation:
                self.add_error('password_confirmation', 'Debe confirmar la contraseña')
            elif password != password_confirmation:
                self.add_error('password_confirmation', 'Las contraseñas no coinciden')

        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        
        # Solo actualiza la contraseña si se proporcionó una nueva
        if password:
            user.set_password(password)
            
        if commit:
            user.save()
            
            # Guardar los grupos y permisos
            self.save_m2m()
            
        return user